"""MicroMold concept media (TRL 3, constructable design of MMD-DDR-003), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Takes the parts from cad/src/model.py (PARAMS), adds a 0.9 m workbench and a 1.75 m person
as context for the hero and blueprint isometric, and renders the media set with
.kit/concept.py. Parts are colored and numbered to match bom/bom.csv (item 15, hardware,
is not modeled). Key figures come from docs/04-calcs/sizing.py (MMD-CAL-001).
CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. Z up, bench top at Z = 0, the operator stands on the -Y side.
Shown with the plunger raised (loading position) and the test mold seated on the nozzle.
"""
import contextlib
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src"), str(ROOT / "docs" / "04-calcs")]
from build123d import Box, Pos  # noqa: E402
import concept  # noqa: E402
from concept import Part, render_all, human_figure  # noqa: E402
from model import build_parts  # noqa: E402

with contextlib.redirect_stdout(io.StringIO()):
    from sizing import RESULTS as S  # noqa: E402


def cut_on_axis(parts, keep="+Y"):
    """Like concept.cutaway_parts, but cut on Y = 0, the injection axis, so the bore, plunger,
    heaters, nozzle and mold cavity show (the kit cuts at the mean Y of the parts, about 20 mm
    behind the axis here). The kit is unchanged."""
    big = 20000.0
    cutter = Pos(0, big / 2, 0) * Box(big, big, big)
    out = []
    for p in parts:
        s = p.shape & cutter
        if s.volume > 1e-6:
            out.append(Part(p.name, s, p.color, p.bom, p.explode, p.alpha))
    return out


concept.cutaway_parts = cut_on_axis
m = build_parts()
m["clamp"] = m["clamp"] & (Pos(0, 0, 2500) * Box(5000, 5000, 5000))   # lift screw end below the bench top left off (MMD-DDR-003)
parts = [
    Part("Base plate", m["base"], "#4B5563", 1, (0, 140, -220)),
    Part("Column, drive head and ratchet handle", m["drive"], "#1F2937", 2, (0, 280, 0)),
    Part("Rack ram", m["ram"], "#6B7280", 3, (0, 0, 380)),
    Part("Plunger load cell and spacer", m["loadcell"], "#7C3AED", 4, (-170, 0, 250)),
    Part("Plunger, 22 mm", m["plunger"], "#D1D5DB", 5, (0, 0, 200)),
    Part("Heated barrel", m["barrel"], "#78716C", 6, (0, 0, 80)),
    Part("Band heaters, 2 x 300 W", m["heaters"], "#C2410C", 7, (220, -60, 80)),
    Part("Nozzle and nozzle heater", m["nozzle"], "#D4A017", 8, (0, 0, 10)),
    Part("Barrel bracket and heat break", m["bracket"], "#0F766E", 9, (0, 170, 170)),
    Part("Insulation jacket and guard", m["guard"], "#94A3B8", 10, (400, -80, 80)),
    Part("Mold clamp (screw lift table)", m["clamp"], "#115E59", 11, (0, -220, -110)),
    Part("Aluminum mold set", m["mold"], "#B8C4CE", 12, (0, -300, 30)),
    Part("Control box with PID and SSR", m["ctrl"], "#2563EB", 13, (-160, -80, 0)),
    Part("Heater and sensor wiring", m["wiring"], "#111827", 14, (-120, -200, -60)),
    Part("Nozzle zone shield", m["shield"], "#A8A29E", 16, (0, -520, -40), alpha=1.0),
    Part("Fume hood and duct", m["hood"], "#CBD5E1", 17, (-260, 0, 120)),
    Part("Mold cooling fan", m["coolfan"], "#0369A1", 18, (260, 0, 0)),
]

# Context for scale: workbench and a 1.75 m person (hero and blueprint isometric only)
bench = Pos(0, 20, -20) * Box(1300, 650, 40)
for lx in (-610, 610):
    for ly in (-270, 310):
        bench = bench + Pos(lx, ly, -470) * Box(50, 50, 860)
context = [Part("workbench (0.9 m)", bench, "#D6D3D1"),
           human_figure(1750.0, x=-950.0, y=-420.0, z=-900.0)]
context[1].name = "1.75 m person"

render_all(
    parts, project="MicroMold", title="Desktop injection press concept", dwg_no="MMD-DWG-010",
    key_figures=[f"22 mm bore, 120 mm in the bore: {S['shot']:.0f} g HDPE shot (ideal)",
                 f"{S['p_design']:.1f} MPa ({S['p_design'] * 10:.0f} bar) at 250 N, ratchet drive, {S['pulls']:.0f} pulls",
                 f"{S['P_heat']:.0f} W heaters, two PID zones; about {S['t_warm']:.0f} min warm-up",
                 f"About {S['cycle']:.1f} min per shot with mold fan, {60 / S['cycle']:.0f} per hour (estimate)",
                 f"Side fume hood, about {S['Qh']:.0f} m3/h; HDPE, PP, LDPE, PS only",
                 f"${S['press_cost']:.0f} press, ${S['total_cost']:.0f} with one mold (indicative)"],
    scale_figure=False, context=context,
    cut_exclude=("Control box with PID and SSR", "Heater and sensor wiring", "Fume hood and duct"),
    flow={"title": "material flow per shot, grams (estimates, 30 g HDPE test part)", "unit": "g",
          "stages": [("Sorted, washed flake", 36), ("Melt in barrel", 36), ("Injected shot", 34),
                     ("Part out of mold", 30)],
          "losses": [(1, "Purge and drool, to regrind", 2), (2, "Sprue, to regrind", 4)]},
)
