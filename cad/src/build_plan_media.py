"""MicroMold prototype build plan pictures (MMD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/MMD-DWG-101 to 114        making sketches for the made components
    docs/05-build-plan/base-holes.png      hole positions in the base plate
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
A single sheet, joint or step can be drawn with, for example, "sheets:103" or "steps:4".
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, bx  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
BT = D["bt"]

COL = {"base": "#78716C", "column": "#1F2937", "frame": "#334155", "head": "#374151", "ram": "#6B7280",
       "adapter": "#B45309", "ratchet": "#111827", "cell": "#7C3AED", "spacer": "#A16207", "coupling": "#0E7490",
       "plunger": "#9CA3AF", "barrel": "#57534E", "heaters": "#C2410C", "nozzle": "#D4A017", "pads": "#F5F5F4",
       "screws": "#111827", "guard": "#94A3B8", "table": "#115E59", "handwheel": "#B91C1C", "washer": "#D6D3D1",
       "mold": "#B8C4CE", "mold2": "#8FA3B5", "dowel": "#374151", "shield": "#A8A29E", "front": "#D6D3D1",
       "hinge": "#44403C", "fan": "#0369A1", "fanbr": "#475569", "hood": "#CBD5E1", "arm": "#B45309",
       "ctrl": "#2563EB", "wiring": "#111827", "bench": "#E7E5E4"}


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


S = lambda *ks: _fuse([C[k].shape for k in ks])  # noqa: E731


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def bench(x0=-260, x1=260, y0=-200, y1=200):
    return part("Bench top (40 mm)", bx(x0, x1, y0, y1, -P["bench_t"], 0) - bx(-12.5, 12.5, -12.5, 12.5, -50, 5), COL["bench"])


def win(shape, x0, x1, y0, y1, z0, z1):
    return shape & bx(x0, x1, y0, y1, z0, z1)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "base": part("Base plate", C["base"].shape, COL["base"]),
        "frame": part("Column with shelf, back plate and head plate (welded)", S("column", "shelf", "back_plate", "head_plate"), COL["frame"]),
        "table": part("Lift table and screw", C["table"].shape, COL["table"]),
        "handwheel": part("Handwheel nut and thrust washer", S("handwheel", "washer"), COL["handwheel"]),
        "head": part("Arbor press head, rack ram, head screws", S("press_head", "ram", "head_screws"), COL["head"]),
        "drive": part("Ratchet adapter and ratchet handle", S("adapter", "adapter_pin", "ratchet"), COL["adapter"]),
        "nozzle": part("Nozzle and nozzle heater", S("nozzle", "nozzle_heater"), COL["nozzle"]),
        "barrel": part("Barrel and band heaters", S("barrel", "heaters"), COL["barrel"]),
        "pads": part("Mica pads and flange screws", S("pads", "flange_screws"), COL["pads"]),
        "guard": part("Jacket and guard, hangers", S("guard", "hangers"), COL["guard"]),
        "cell": part("Load cell, thermal spacer, coupling", S("loadcell", "spacer", "coupling"), COL["cell"]),
        "plunger": part("Plunger and ball-lock pin", S("plunger", "coupling_pin"), COL["plunger"]),
        "shield": part("Nozzle zone shield", S("shield_sides", "shield_front", "hinges"), COL["shield"]),
        "fan": part("Fan bracket and mold cooling fan", S("fan_bracket", "fan"), COL["fan"]),
        "hood": part("Fume hood and hood arm", S("hood", "hood_arm"), COL["hood"]),
        "mold": part("Test plaque mold", S("mold_lower", "mold_upper", "mold_screws", "dowels"), COL["mold"]),
        "ctrl": part("Control box and wiring", S("ctrl", "wiring"), COL["ctrl"]),
    }


ORDER = ["base", "frame", "table", "handwheel", "head", "drive", "nozzle", "barrel", "pads", "guard", "cell",
         "plunger", "shield", "fan", "hood", "mold", "ctrl"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"base": (0, 0, -220), "frame": (0, 220, 0), "table": (0, -200, -150), "handwheel": (0, -200, -300),
           "head": (0, 0, 260), "drive": (260, 0, 260), "nozzle": (0, 0, -90), "barrel": (0, 0, 20),
           "pads": (0, 0, 90), "guard": (-200, 0, -60), "cell": (0, 0, 170), "plunger": (0, 0, 90),
           "shield": (0, -620, -60), "fan": (330, 0, -40), "hood": (-320, 0, 180), "mold": (0, -360, -90),
           "ctrl": (720, -420, -260)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "MicroMold prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the operator stands at the front",
                       elev=16, azim=-52, size=(11, 9), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
SHEETS = {}


def sheet(n):
    def deco(f):
        SHEETS[n] = f
        return f
    return deco


BASE = dict(project="MicroMold", date=DATE)


def _sheet(key, name, shape, color, neigh, dwg, title, material, notes, view_shape=None, inset=(24, -58)):
    return bv.component_sheet(Part(name, shape, color), neigh, dwg_no=dwg, title=title, material=material,
                              notes=notes, view_shape=view_shape, inset_view=inset, out_dir=str(DWG), **BASE)


def _zero(shape):
    """Move a part so its bounding box starts at the origin (for the three views)."""
    import build123d as b
    bb = shape.bounding_box()
    return b.Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * shape


@sheet(101)
def s101():
    M = made()
    return _sheet("base", "Base plate", C["base"].shape, COL["base"], [M["frame"], M["shield"], M["fan"], M["handwheel"]],
                  "MMD-DWG-101", "MicroMold base plate: making sketch", "Steel plate 8 mm, S235 or A36",
                  ["Cut 320 x 260 mm from 8 mm steel plate; square the edges, round the",
                   "  corners to about 5 mm and deburr.",
                   "Measure from the front edge (the operator's side) and sideways from",
                   "  the centre line. The hole picture in the plan repeats every position.",
                   "Lift screw hole 25 mm on the centre line, 110 mm from the front edge.",
                   "Bench bolt holes 11 mm, 145 mm each side, 15 and 245 mm from the front.",
                   "Shield feet: drill 5.0 and tap M6, 126 mm each side, 40 and 160 mm",
                   "  from the front. Fan bracket: drill 5.0, tap M6, 146 mm right, 70 and",
                   "  150 mm from the front.",
                   "Mark the column outline: 80 x 60 mm, centred, 175 to 235 mm from the",
                   "  front edge. The column is welded here in assembly step 1.",
                   "Check: lay the shield feet and fan bracket on it; the holes line up."],
                  inset=(30, -60))


@sheet(102)
def s102():
    M = made()
    fr = S("column", "shelf", "back_plate", "head_plate")
    return _sheet("frame", "Column weldment", fr, COL["frame"], [M["base"], M["head"], M["barrel"]],
                  "MMD-DWG-102", "MicroMold column with shelf, back plate and head plate: making sketch",
                  "Steel tube 80 x 60 x 3 mm; steel plate 20 and 8 mm",
                  ["Column: cut 907 mm of 80 x 60 x 3 mm tube, ends square. In the front and",
                   "  back walls drill four 22 mm access holes, 30 mm each side of centre,",
                   "  25 and 115 mm below the top. In the left wall drill two 9 mm holes",
                   "  for M6 rivnuts, 477 mm up, 20 and 45 mm back from the front face.",
                   "Shelf: 110 x 150 x 20 mm. 46 mm hole centred 65 mm from its back edge;",
                   "  four M8 tapped holes on an 82 mm circle at 45 degrees; three M5 holes",
                   "  10 deep underneath on a 132 mm circle (front, back left, back right).",
                   "Back plate 110 x 120 x 8 mm. Head plate 120 x 140 x 8 mm with four 11 mm",
                   "  holes at 30 mm each side, 25 mm from top and bottom, countersunk on the",
                   "  back so the screw heads sit flush against the column.",
                   "Weld: shelf top 479 mm up the column, back edge on the front face; back",
                   "  plate on the shelf and the column corners; head plate flush with the",
                   "  top, holes on the access holes. Fillet welds 5 mm.",
                   "Check: the shelf is square to the column within 0.5 mm over 100 mm."],
                  view_shape=_zero(fr), inset=(20, -50))


@sheet(103)
def s103():
    M = made()
    return _sheet("barrel", "Barrel", C["barrel"].shape, COL["barrel"], [M["frame"], M["nozzle"], M["pads"]],
                  "MMD-DWG-103", "MicroMold barrel: making sketch (machine shop)", "Steel bar 42 mm and 100 mm, C45 or 1045",
                  ["A machine shop part. The tube is 42 mm bar, 260 mm long, bored and",
                   "  honed to 22 mm H8 right through; the flange and funnel collar may be",
                   "  turned from 100 mm bar and welded on, then the bore finish-honed.",
                   "Flange 100 mm across, 10 mm thick, at the top of the tube; four 8.5 mm",
                   "  holes on an 82 mm circle at 45 degrees to the front.",
                   "Funnel 64 mm across, 12 mm above the flange; cone from 56 to 22 mm.",
                   "Lower end: M30 x 1.5 thread, 15 mm deep, for the nozzle; face square.",
                   "Thermocouple well: 3.2 mm, 8 mm deep, on the left side, 120 mm above",
                   "  the lower end, between the two band heaters.",
                   "Fit: the flange sits on four mica pads on the shelf, held by four M8",
                   "  cap screws; the tube passes the shelf hole with 2 mm all round.",
                   "Check: the plunger slides through the whole bore by hand, cold."],
                  view_shape=_zero(C["barrel"].shape), inset=(20, -55))


@sheet(104)
def s104():
    M = made()
    return _sheet("nozzle", "Nozzle", C["nozzle"].shape, COL["nozzle"], [M["barrel"], M["mold"]],
                  "MMD-DWG-104", "MicroMold nozzle: making sketch (machine shop)", "Steel bar 32 mm, C45 or 1045",
                  ["A lathe part, from 32 mm steel bar.",
                   "Tip: 12 mm spherical radius, 24 mm across where it meets the body.",
                   "Body 24 mm across, 20 mm long, for the 100 W nozzle heater band.",
                   "Hex 27 mm across the flats, 8 mm long, for a spanner.",
                   "Spigot: M30 x 1.5 thread, 15 mm long, above the hex.",
                   "Orifice 4 mm, 20 mm deep from the tip; then 18 mm bore through the",
                   "  rest, so melt meets no step bigger than 2 mm.",
                   "Fit: screws into the barrel's lower end with copper anti-seize until",
                   "  the hex face is tight on the barrel face; the bores line up.",
                   "The tip seats in the mold's 12.5 mm spherical seat; it touches at the",
                   "  centre, around the sprue.",
                   "Check: blow through it; the tip has no burr or flat."],
                  view_shape=_zero(C["nozzle"].shape), inset=(10, -55))


@sheet(105)
def s105():
    M = made()
    return _sheet("guard", "Jacket and guard", C["guard"].shape, COL["guard"], [M["barrel"], M["frame"]],
                  "MMD-DWG-105", "MicroMold insulation jacket and guard: making sketch",
                  "Perforated steel sheet 1 mm; aluminium sheet 0.5 mm; mineral wool 25 mm",
                  ["Made as two half shells, front and back, that close round the barrel",
                   "  (it cannot slide on over the nozzle). Each half, 217 mm long:",
                   "Guard: 1 mm perforated steel rolled to a half tube 116 mm across.",
                   "Skin: 0.5 mm aluminium rolled to a half tube 60 mm across.",
                   "Fill between with 25 mm mineral wool rated above 600 degrees C; close",
                   "  the ends and the two split faces with aluminium strip, riveted.",
                   "Back half: a 20 x 40 mm notch in skin and wool at each heater band,",
                   "  for its leads and terminal block.",
                   "Hanger tabs: two per half, 16 x 14 mm, 2 mm steel, riveted to the top",
                   "  edge pointing out at 45 degrees to the split (132 mm circle);",
                   "  drill each 5.5 mm.",
                   "Fit: each half hangs from the shelf on two M5 screws through 14 mm",
                   "  spacers; the halves meet left and right; bottom edge 6 mm above the hex.",
                   "Check: the guard does not touch the barrel or the heaters anywhere."],
                  view_shape=_zero(C["guard"].shape), inset=(20, -55))


@sheet(106)
def s106():
    M = made()
    return _sheet("plunger", "Plunger", C["plunger"].shape, COL["plunger"], [M["cell"], M["barrel"]],
                  "MMD-DWG-106", "MicroMold plunger: making sketch", "Ground steel rod 22 mm (f7), bought to length",
                  ["Buy 22 mm ground rod, f7 tolerance, 200 mm long.",
                   "Chamfer the tip 0.5 mm; the tip face stays flat and square.",
                   "Drill a 7 mm cross hole 18 mm below the top end, through the centre;",
                   "  the 6 mm ball-lock pin passes through it with 1 mm of play, so the",
                   "  plunger can float in line with the bore.",
                   "Deburr the cross hole so it cannot score the bore.",
                   "Fit: the top 30 mm goes into the coupling; the rest runs in the bore",
                   "  with 0.05 to 0.10 mm diametral clearance and no seal.",
                   "Check: measure the rod at three places; 21.95 to 21.98 mm."],
                  view_shape=_zero(C["plunger"].shape), inset=(10, -55))


@sheet(107)
def s107():
    M = made()
    sh = S("coupling", "spacer")
    return _sheet("cell", "Coupling and spacer", sh, COL["coupling"], [M["head"], M["plunger"], part("Load cell", C["loadcell"].shape, COL["cell"])],
                  "MMD-DWG-107", "MicroMold plunger coupling and thermal spacer: making sketch",
                  "Steel bar 40 mm; glass-epoxy (G-11) sheet 10 mm",
                  ["Coupling: cut 35 mm of 40 mm steel bar, faces square (drill press).",
                   "  Drill a 22.2 mm hole 30 mm deep in one face (step up from 10 mm).",
                   "  Cross drill 6.2 mm through the centre, 12 mm from that face.",
                   "  In the other face drill and tap three M5 holes 8 deep on a 28 mm circle.",
                   "Spacer: cut a 56 mm disc from 10 mm G-11. Three 5.5 mm holes on a",
                   "  28 mm circle, counterbored 10 mm across and 4 deep from the top face.",
                   "  Three M5 holes tapped 6 deep in the top face, on the circle of the",
                   "  load cell's flange holes (46 mm assumed), 60 degrees from the others.",
                   "Fit: three M5 x 12 low-head screws hold the coupling under the spacer,",
                   "  heads 1 mm below its top; three M5 screws through the cell's flange",
                   "  into the spacer. No screw crosses the spacer.",
                   "Check: no metal path from the coupling to the cell."],
                  view_shape=_zero(sh), inset=(10, -55))


@sheet(108)
def s108():
    M = made()
    sh = S("adapter")
    return _sheet("drive", "Ratchet adapter", sh, COL["adapter"], [M["head"], part("Ratchet handle", C["ratchet"].shape, COL["ratchet"])],
                  "MMD-DWG-108", "MicroMold ratchet adapter: making sketch", "The press's own lever hub; a 1/2 in drive extension bar",
                  ["Start from the lever hub that comes on the press's pinion shaft (36 mm",
                   "  across, bored to the shaft, 28 mm in the model). Remove its lever.",
                   "Cut the square end off a 1/2 in drive extension bar, 16 mm long.",
                   "Weld it to the hub's outer face, square and on the shaft's centre line.",
                   "  Let it cool slowly; check it runs true when the hub is on the shaft.",
                   "Drill 6 mm through the hub and shaft together, 12 mm from the head's",
                   "  side face, and fit a 6 mm roll pin.",
                   "Fit: the ratchet handle's square drive pushes on; set the ratchet so a",
                   "  pull toward you drives the ram down.",
                   "Check: a 250 N pull turns the shaft with no slip at the pin."],
                  view_shape=_zero(sh), inset=(15, 30))


@sheet(109)
def s109():
    M = made()
    return _sheet("table", "Lift table and screw", C["table"].shape, COL["table"], [M["base"], M["handwheel"], M["mold"]],
                  "MMD-DWG-109", "MicroMold lift table and screw: making sketch", "Steel plate 12 mm; Tr20 x 4 lead screw, 150 mm",
                  ["Table: cut 170 x 126 mm from 12 mm steel plate; deburr.",
                   "Drill a 20.5 mm hole in the centre (85 and 63 mm from the edges).",
                   "Screw: cut 150 mm of Tr20 x 4 lead screw, ends square.",
                   "Push the screw into the hole flush with the table top. Clamp it square",
                   "  to the table with an engineer's square both ways.",
                   "Weld a 5 mm fillet all round underneath; plug weld the top and grind",
                   "  it flush and flat. Keep weld spatter off the thread.",
                   "Fit: the screw runs down through the handwheel nut, the thrust washer,",
                   "  the 25 mm hole in the base plate and the hole in the bench.",
                   "The table's back edge runs 2 mm in front of the column face; the column",
                   "  stops the table turning when the handwheel turns.",
                   "Check: the screw is square to the table within 0.2 mm over 100 mm."],
                  view_shape=_zero(C["table"].shape), inset=(20, -55))


@sheet(110)
def s110():
    M = made()
    sh = S("handwheel")
    return _sheet("handwheel", "Handwheel nut", sh, COL["handwheel"], [M["base"], M["table"]],
                  "MMD-DWG-110", "MicroMold handwheel nut: making sketch", "Bought 120 mm handwheel; Tr20 x 4 nut",
                  ["Buy a 120 mm cast or steel handwheel with a spinner knob and a hub",
                   "  about 40 mm across and 30 mm long.",
                   "Bore the hub to take a round Tr20 x 4 nut (bronze or steel) as a",
                   "  press fit; or weld a steel hex nut into the hub, square to its face.",
                   "Pin the nut with a 4 mm pin across the hub if it is pressed in.",
                   "Face the hub's bottom flat so it bears evenly on the thrust washer.",
                   "Fit: sits on a 2 mm thrust washer on the base plate, round the screw.",
                   "  Turning it raises or lowers the table 4 mm a turn.",
                   "The rim is 2.5 mm clear of the column. Reach it under the shield front.",
                   "Check: the table runs the full 100 mm with light hand force."],
                  view_shape=_zero(sh), inset=(25, -60))


@sheet(111)
def s111():
    M = made()
    sh = S("mold_lower", "mold_upper")
    return _sheet("mold", "Test plaque mold", sh, COL["mold"], [M["table"], M["nozzle"]],
                  "MMD-DWG-111", "MicroMold test plaque mold (two plates): making sketch (machine shop)",
                  "Aluminium 6061-T6 plate 45 mm",
                  ["Two plates 120 x 90 x 45 mm, faces flat to 0.02 mm (milled).",
                   "Lower plate: cavity 64 x 50 x 6 mm deep, centred in the top face, 1 degree",
                   "  draft, 1 mm corner radius. Four M10 thread inserts at 48 mm each side",
                   "  and 33 mm each side of centre (drill and tap for the insert, 25 deep).",
                   "Upper plate: four 11 mm holes on the same positions; sprue through",
                   "  the centre, 5 mm at the top to 7 mm at the parting line, polished.",
                   "  Spherical seat for the nozzle in the top face: 12.5 mm radius, 2 mm deep.",
                   "Dowels: two 6 mm holes at 48 mm each side on the centre line, 12 deep in",
                   "  each plate; press fit in the lower plate, slip fit in the upper.",
                   "Vents: two 0.03 mm deep, 5 mm wide, from the cavity's far end.",
                   "Fit: four M10 x 70 cap screws at 20 kN preload (about 40 N m).",
                   "Check: blue on the parting faces shows full contact round the cavity."],
                  view_shape=_zero(sh), inset=(25, -55))


@sheet(112)
def s112():
    M = made()
    sh = S("shield_sides", "shield_front", "hinges")
    return _sheet("shield", "Nozzle zone shield", sh, COL["shield"], [M["base"], M["mold"], M["fan"], M["table"]],
                  "MMD-DWG-112", "MicroMold nozzle zone shield: making sketch", "Perforated steel sheet 1.5 mm, 10 mm square holes",
                  ["Sides (make 2, a left and a right): 170 x 282 mm blanks; fold a 20 mm",
                   "  foot outward along the bottom; the side stands 262 mm tall.",
                   "  Drill each foot 6.5 mm, 10 mm out from the fold, 25 and 145 mm from",
                   "  its front end.",
                   "Front: 233 x 210 mm, with a window 170 x 130 mm, 30 mm up from its",
                   "  bottom edge; rivet a perforated panel behind the window.",
                   "Hinges: two 30 mm butt hinges riveted to the left side and the front,",
                   "  40 mm from the top and bottom of the front. Latch on the right.",
                   "Fit: the feet sit on the base plate with two M6 screws each; the sides",
                   "  stand 115 mm each side of the axis, 75 mm behind it to 95 mm in front.",
                   "The front's bottom edge is 60 mm above the bench, so the handwheel is",
                   "  reached under it with the front shut.",
                   "Check: the front swings open and latches; deburr every cut edge."],
                  view_shape=_zero(sh), inset=(25, -55))


@sheet(113)
def s113():
    M = made()
    return _sheet("fan", "Fan bracket", C["fan_bracket"].shape, COL["fanbr"], [M["base"], part("Mold cooling fan", C["fan"].shape, COL["fan"])],
                  "MMD-DWG-113", "MicroMold mold cooling fan bracket: making sketch", "Steel sheet 3 mm",
                  ["Blank 120 x 215 mm of 3 mm steel. Fold an 18 mm foot at one end, 90 degrees,",
                   "  toward the fan side; the upright then stands 197 mm tall.",
                   "Intake hole 112 mm across, centre 137 mm above the underside of the foot,",
                   "  centred across the width. Cut with a hole saw or by chain drilling.",
                   "Four 4.4 mm holes on a 105 mm square round the intake hole, for the",
                   "  fan's own corner holes.",
                   "Foot: two 6.5 mm holes, 9 mm from the upright, 40 mm each side of centre.",
                   "Fit: the fan's back face sits flat on the upright, held by four M4 x 45",
                   "  screws and nuts; the fan blows through the shield side onto the mold.",
                   "  Two M6 screws hold the foot to the base plate.",
                   "Check: the fan is 1 mm clear of the shield side; its guard is fitted."],
                  view_shape=_zero(C["fan_bracket"].shape), inset=(25, 30))


@sheet(114)
def s114():
    M = made()
    sh = S("hood", "hood_arm")
    return _sheet("hood", "Fume hood and arm", sh, COL["hood"], [M["frame"], M["barrel"]],
                  "MMD-DWG-114", "MicroMold fume hood and hood arm: making sketch",
                  "Aluminium sheet 1 mm; steel flat bar 30 x 5 mm",
                  ["Hood: fold 1 mm aluminium into a box 120 deep, 150 wide and 100 tall with",
                   "  one 150 x 100 face open (toward the funnel), seams pop riveted.",
                   "Cut a 100 mm hole in the top for the duct stub; rivet on a 100 mm round",
                   "  stub (a square stub is drawn) for the flexible duct.",
                   "Arm: 30 x 5 mm flat bar, 200 mm long; bend 90 degrees 45 mm from one",
                   "  end, flat way. Long leg: two 5.5 mm holes 20 and 70 mm from its free",
                   "  end. Short leg: two 6.5 mm holes 10 and 35 mm from the bend's outside.",
                   "Fit: the short leg bolts to the column's left face with two M6 screws",
                   "  into rivnuts; the long leg lies on the hood's back face, two M5",
                   "  screws and nuts. The hood's open face is 100 mm from the funnel axis,",
                   "  its centre level with the flange.",
                   "Check: the hood stays put when pushed by hand."],
                  view_shape=_zero(sh), inset=(25, -40))


def sheets(which=None):
    out = []
    for n, f in sorted(SHEETS.items()):
        if which and n not in which:
            continue
        out.append(f())
    return out


# ----------------------------------------------------------------- base plate hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    yf = P["base_y"] - P["base"][1] / 2
    face = [f for f in C["base"].shape.faces() if abs(f.center().Z - BT) < 0.01 and f.area > 1e4][0]
    holes = []
    for w in face.inner_wires():
        bb = w.bounding_box()
        holes.append((bb.center().X, bb.center().Y - yf, bb.size.X))
    names = {5: ("tapped M6 (drill 5.0)", "#1D4ED8"), 11: ("11, bench bolt", INK), 25: ("25, lift screw", "#B91C1C")}
    fig = plt.figure(figsize=(11, 9.5), dpi=150)
    ax = fig.add_axes([0.06, 0.08, 0.66, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-160, 0), 320, 260, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-40, 175), 80, 60, fc="none", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, 205, "column\n(welded)", ha="center", va="center", fontsize=8, color=MUT)
    for xs in (-1, 1):
        ax.plot([xs * 115.75, xs * 115.75], [15, 185], color=MUT, lw=0.6, ls=":")
    ax.text(-112, 100, "shield side", rotation=90, ha="left", va="center", fontsize=7, color=MUT)
    ax.axvline(0, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    xs_, ys_ = set(), set()
    for x, y, dd in holes:
        k = round(dd) if round(dd) in names else 5
        col = names[k][1]
        ax.add_patch(plt.Circle((x, y), dd / 2, fc="white", ec=col, lw=1.1))
        ax.plot([x - dd / 2 - 3, x + dd / 2 + 3], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - dd / 2 - 3, y + dd / 2 + 3], color=MUT, lw=0.4)
        if x > -0.5:
            xs_.add(round(abs(x), 1))
        ys_.add(round(y, 1))
    for i, x in enumerate(sorted(xs_)):
        yl = -10 - 10 * (i % 2)
        ax.plot([x, x], [0, yl + 4], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{x:g}", ha="center", va="top", fontsize=8, color=AC)
    ax.text(0, -34, "sideways from the centre line, mm (each side where holes are paired)", ha="center", fontsize=8, color=MUT)
    for i, y in enumerate(sorted(ys_)):
        xl = -166 - 18 * (i % 2)
        ax.plot([xl + 2, -160], [y, y], color=AC, lw=0.4, ls=":")
        ax.text(xl, y, f"{y:g}", ha="right", va="center", fontsize=8, color=AC)
    ax.text(-205, 130, "from the front edge (operator side), mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.text(0, -50, "FRONT EDGE: THE OPERATOR STANDS HERE", ha="center", fontsize=8, color=INK, fontweight="bold")
    ax.set_xlim(-212, 170); ax.set_ylim(-58, 268)
    fig.text(0.04, 0.975, "Base plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.948, "Seen from above. Full size figures in mm, taken from the model. 320 x 260 x 8 mm steel plate.", fontsize=8.5, color=MUT, va="top")
    key = ["Lift screw hole 25, on the centre line", "  (the bench gets a 25 mm hole under it)",
           "Bench bolt holes 11, at 145 each side", "Shield feet: tapped M6 at 126", "  each side",
           "Fan bracket: tapped M6 at 146,", "  right side only", "", "Column outline 80 x 60, welded",
           "  in assembly step 1"]
    fig.text(0.74, 0.86, "What each hole is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(key):
        fig.text(0.74, 0.83 - i * 0.024, t, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, "github.com/BoujeeEnjinia1701/micromold", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "base-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "base-holes.png"


# ----------------------------------------------------------------- joints
JOINTS = {}


def jnt(n):
    def deco(f):
        JOINTS[n] = f
        return f
    return deco


def _j(n, parts, title, sub, **kw):
    kw.setdefault("size", (8, 6))
    return bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, **kw)


@jnt(1)
def j1():
    w = (-70, 70, 0, 130, D["brk0"] - 25, D["brk1"] + 70)
    return _j(1, [part("Column", win(C["column"].shape, *w), COL["column"]),
                  part("Shelf, welded to the column face", win(C["shelf"].shape, *w), COL["frame"]),
                  part("Back plate, welded to shelf and column", win(C["back_plate"].shape, *w), "#64748B"),
                  part("Barrel flange", win(C["barrel"].shape, *w), COL["barrel"]),
                  part("Mica pad", win(C["pads"].shape, *w), "#E7E5E4"),
                  part("M8 cap screw with mica washer", win(C["flange_screws"].shape, *w), COL["screws"])],
              "barrel flange on the shelf (cut on the axis)",
              "Seen from the left, cut through the middle. The flange sits on mica pads; the screws only hold it down",
              elev=12, azim=-150)


@jnt(2)
def j2():
    w = (-20, 30, -20, 130, D["head0"] - 10, D["head1"] + 5)
    return _j(2, [part("Column (access holes front and back)", win(C["column"].shape, *w), "#475569"),
                  part("Head plate, welded to the column", win(C["head_plate"].shape, *w), "#0F766E"),
                  part("Press head casting", win(C["press_head"].shape, *w), "#9CA3AF"),
                  part("M10 countersunk screws", win(C["head_screws"].shape, *w), "#B91C1C")],
              "press head on the head plate (cut through the right-hand screws)",
              "Seen from the right. Screw heads sit flush in the plate; a hex key reaches them through the column holes",
              elev=12, azim=15)


@jnt(3)
def j3():
    w = (-80, 80, -0.01, 80, D["mold1"] - 30, D["bar0"] + 40)
    return _j(3, [part("Barrel (M30 x 1.5 thread)", win(C["barrel"].shape, *w), COL["barrel"]),
                  part("Nozzle", win(C["nozzle"].shape, *w), COL["nozzle"]),
                  part("Nozzle heater band", win(C["nozzle_heater"].shape, *w), COL["heaters"]),
                  part("Mold upper plate (spherical seat, sprue)", win(C["mold_upper"].shape, *w), COL["mold"]),
                  part("Jacket and guard", win(C["guard"].shape, *w), COL["guard"])],
              "nozzle in the barrel and on the mold (cut on the axis)",
              "Seen from the front, cut through the middle. The tip sits in the mold's seat around the sprue",
              elev=8, azim=-75)


@jnt(4)
def j4():
    w = (10, 80, 0, 80, D["brk0"] - 40, D["brk1"] + 5)
    return _j(4, [part("Shelf (underside, tapped M5)", win(C["shelf"].shape, *w), COL["frame"]),
                  part("Spacer and M5 screw", win(C["hangers"].shape, *w), COL["screws"]),
                  part("Guard with hanger tab", win(C["guard"].shape, *w), COL["guard"])],
              "jacket hanger (back right of four)",
              "Seen from the right, slightly below. Each half hangs on two tabs, each on a 14 mm spacer and an M5 screw",
              elev=-12, azim=10)


@jnt(5)
def j5():
    w = (-50, 50, -0.01, 50, D["cp0"] - 25, D["lc1"] + 30)
    return _j(5, [part("Rack ram", win(C["ram"].shape, *w), COL["ram"]),
                  part("Load cell", win(C["loadcell"].shape, *w), COL["cell"]),
                  part("Thermal spacer (G-11)", win(C["spacer"].shape, *w), "#EAB308"),
                  part("Coupling", win(C["coupling"].shape, *w), COL["coupling"]),
                  part("Ball-lock pin", win(C["coupling_pin"].shape, *w), "#B91C1C"),
                  part("Plunger", win(C["plunger"].shape, *w), COL["plunger"])],
              "load cell, spacer, coupling and plunger (cut on the axis)",
              "Seen from the front. Pull the pin and the plunger comes out; no metal path crosses the spacer",
              elev=10, azim=-75)


@jnt(6)
def j6():
    w = (-75, 75, -0.01, 70, -P["bench_t"] - 60, D["table_top"] + 5)
    return _j(6, [part("Bench (25 mm hole)", win(bench().shape, *w), "#D6D3D1"),
                  part("Base plate (25 mm hole)", win(C["base"].shape, *w), COL["base"]),
                  part("Thrust washer", win(C["washer"].shape, *w), "#A8A29E"),
                  part("Handwheel nut", win(C["handwheel"].shape, *w), COL["handwheel"]),
                  part("Lift table and screw", win(C["table"].shape, *w), COL["table"])],
              "lift screw, handwheel nut and base (cut on the axis)",
              "Seen from the front. The nut turns on the washer; the screw rises and falls through the base and bench",
              elev=10, azim=-75)


@jnt(7)
def j7():
    w = (-95, 95, -70, 130, D["table_top"] - 20, D["table_top"] + 2)
    return _j(7, [part("Column", win(C["column"].shape, *w), COL["column"]),
                  part("Lift table", win(C["table"].shape, *w), COL["table"])],
              "lift table beside the column (seen from above)",
              "The table's back edge runs 2 mm from the column face; the column stops it turning with the nut",
              elev=70, azim=-90)


@jnt(8)
def j8():
    w = (-5, 70, -0.01, 50, D["mold0"] - 2, D["mold1"] + 12)
    return _j(8, [part("Lift table", win(C["table"].shape, *w), COL["table"]),
                  part("Mold lower plate (thread inserts)", win(C["mold_lower"].shape, *w), COL["mold"]),
                  part("Mold upper plate", win(C["mold_upper"].shape, *w), COL["mold2"]),
                  part("M10 cap screw", win(C["mold_screws"].shape, *w), COL["screws"]),
                  part("Dowel pin", win(C["dowels"].shape, *w), "#B91C1C")],
              "mold plates, screws and dowels (cut through the dowels)",
              "Seen from the front right. The dowels line up the plates; four screws hold them shut",
              elev=15, azim=-70, cut=None)


@jnt(9)
def j9():
    w = (-140, -90, -105, -40, BT - 5, 130)
    return _j(9, [part("Base plate", win(C["base"].shape, *w), COL["base"]),
                  part("Shield side with foot", win(C["shield_sides"].shape, *w), COL["shield"]),
                  part("Shield front", win(C["shield_front"].shape, *w), COL["front"]),
                  part("Hinge", win(C["hinges"].shape, *w), COL["hinge"])],
              "shield foot and lower hinge (front left corner)",
              "The foot is folded out from the side and screwed to the base; the front swings on two hinges",
              elev=25, azim=-130)


@jnt(10)
def j10():
    w = (100, 165, -70, 70, BT - 2, 215)
    return _j(10, [part("Base plate", win(C["base"].shape, *w), COL["base"]),
                   part("Fan bracket", win(C["fan_bracket"].shape, *w), COL["fanbr"]),
                   part("Mold cooling fan", win(C["fan"].shape, *w), COL["fan"]),
                   part("Shield side (perforated)", win(C["shield_sides"].shape, *w), COL["shield"])],
               "fan bracket on the base plate",
               "Seen from the back right. Fan on the bracket's upright, foot on the base, 1 mm from the shield side",
               elev=20, azim=40)


@jnt(11)
def j11():
    hz = D["fl1"] - 15
    w = (-215, 45, 40, 130, hz - 60, hz + 70)
    return _j(11, [part("Column (left face, rivnuts)", win(C["column"].shape, *w), COL["column"]),
                   part("Hood arm", win(C["hood_arm"].shape, *w), COL["arm"]),
                   part("Fume hood", win(C["hood"].shape, *w), COL["hood"])],
               "hood arm on the column (seen from behind)",
               "The short leg bolts to the column's left face; the long leg lies on the hood's back",
               elev=25, azim=125)


def _mid_anchor(v):
    """For close-ups: the part's own vertex nearest its centre, so a leader ends on the part it names."""
    import numpy as np
    return v[np.argmin(np.linalg.norm(v - v.mean(0), axis=1))]


def joints(which=None):
    keep = bv._anchor
    bv._anchor = _mid_anchor
    try:
        return [f() for n, f in sorted(JOINTS.items()) if not which or n in which]
    finally:
        bv._anchor = keep


# ----------------------------------------------------------------- assembly steps
STEPS = {}


def stp(n):
    def deco(f):
        STEPS[n] = f
        return f
    return deco


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def st(n, done, new, title, sub, **kw):
    kw.setdefault("label_done", False)
    return bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw)


def _state(upto):
    M = made()
    keys = {1: ["base", "frame"], 2: ["table", "handwheel"], 3: [], 4: ["nozzle", "pads"], 5: ["barrel", "guard"],
            6: ["head"], 7: ["drive"], 8: [], 9: ["cell", "plunger"], 10: ["shield"], 11: ["fan"], 12: ["hood"], 13: ["ctrl"]}
    out = []
    for k in range(1, upto + 1):
        out += [M[x] for x in keys[k]]
    if 4 <= upto < 5:
        out.append(part("Barrel", C["barrel"].shape, COL["barrel"]))
    return out


@stp(1)
def p1():
    M = made()
    return st(1, [M["base"]], [mv(M["frame"], (0, 0, 160))], "weld the column to the base plate",
              "Column on its outline, square both ways; tack, check, then a 5 mm fillet weld all round",
              elev=20, azim=-55, label_done=True)


@stp(2)
def p2():
    w = part("Thrust washer", C["washer"].shape, "#A8A29E")
    h = part("Handwheel nut", C["handwheel"].shape, COL["handwheel"])
    t = part("Lift table and screw", build_components(P, table_top=160)["table"].shape, COL["table"])
    return st(2, _state(1), [mv(w, (0, -60, 60)), mv(h, (0, -60, 100)), mv(t, (0, 0, 180))], "lift table and handwheel nut",
              "Washer and nut on the base hole; screw the table down into the nut, table at its highest for now",
              elev=22, azim=-55)


@stp(3)
def p3():
    nz = part("Nozzle", C["nozzle"].shape, COL["nozzle"])
    hb = part("Nozzle heater band", C["nozzle_heater"].shape, COL["heaters"])
    return st(3, [part("Barrel", C["barrel"].shape, COL["barrel"])], [mv(nz, (0, 0, -80)), mv(hb, (0, 0, -150))],
              "nozzle onto the barrel (on the bench)",
              "Nozzle screwed in with copper anti-seize until the hex is tight; nozzle heater band clamped on",
              elev=20, azim=-55)


@stp(4)
def p4():
    bar = part("Barrel with nozzle", S("barrel", "nozzle", "nozzle_heater"), COL["barrel"])
    pads = part("Mica pads and flange screws", S("pads", "flange_screws"), COL["pads"])
    return st(4, _state(2), [mv(bar, (0, 0, 330)), mv(pads, (0, -120, 60))], "barrel into the shelf, from above",
              "Before the press head is fitted. Nozzle end first through the shelf; flange on four mica pads; four M8 cap screws",
              elev=18, azim=-40)


@stp(5)
def p5():
    bh = part("Band heaters (2), clamped on", C["heaters"].shape, COL["heaters"])
    g = C["guard"].shape
    gf = part("Jacket front half", g & bx(-100, 100, -100, 0, 0, 600), COL["guard"])
    gb = part("Jacket back half", g & bx(-100, 100, 0, 100, 0, 600), "#64748B")
    hg = part("Hangers (4)", C["hangers"].shape, COL["screws"])
    return st(5, _state(4), [mv(bh, (150, 0, 0)), mv(gf, (0, -170, 0)), mv(gb, (-170, 120, 0)), mv(hg, (0, -170, -150))],
              "band heaters and jacket",
              "Heater bands clamped round the barrel; the two jacket halves close round it and hang on four M5 screws",
              elev=18, azim=-40)


@stp(6)
def p6():
    M = made()
    return st(6, _state(5), [mv(M["head"], (0, -160, 0))], "press head onto the head plate",
              "Four M10 countersunk screws from behind, through the column's access holes, threadlocker",
              elev=18, azim=-40)


@stp(7)
def p7():
    M = made()
    return st(7, _state(6), [mv(M["drive"], (180, 0, 0))], "ratchet adapter and handle",
              "Adapter onto the pinion shaft, 6 mm roll pin; ratchet onto the square, set to drive the ram down on a pull",
              elev=18, azim=-40)


@stp(8)
def p8():
    sp = part("Thermal spacer", C["spacer"].shape, "#EAB308")
    cp = part("Coupling", C["coupling"].shape, COL["coupling"])
    pl = part("Plunger", C["plunger"].shape, COL["plunger"])
    pn = part("Ball-lock pin", C["coupling_pin"].shape, "#B91C1C")
    return st(8, [part("Load cell", C["loadcell"].shape, COL["cell"])],
              [mv(sp, (0, 0, -25)), mv(cp, (0, 0, -60)), mv(pl, (0, 0, -120)), mv(pn, (-70, 0, 0))],
              "plunger unit (on the bench)",
              "Spacer to the cell, coupling to the spacer, three M5 screws each; plunger into the coupling, ball-lock pin",
              elev=15, azim=-55, label_done=True)


@stp(9)
def p9():
    unit = part("Plunger unit (load cell, spacer, coupling, plunger)", S("loadcell", "spacer", "coupling", "plunger", "coupling_pin"), COL["cell"])
    return st(9, _state(8), [mv(unit, (0, -170, 0))], "plunger unit onto the ram",
              "Plunger tip into the funnel; turn the whole unit to screw the cell's stud into the ram end. Lead to the control box",
              elev=18, azim=-40)


@stp(10)
def p10():
    sd = part("Shield sides (2)", C["shield_sides"].shape, COL["shield"])
    fr = part("Front with hinges and latch", S("shield_front", "hinges"), COL["front"])
    return st(10, _state(9), [mv(sd, (0, -40, 160)), mv(fr, (0, -200, 0))], "nozzle zone shield",
              "Sides on the base, two M6 screws through each foot; front hinged to the left side, latch on the right",
              elev=18, azim=-40)


@stp(11)
def p11():
    M = made()
    return st(11, _state(10), [mv(M["fan"], (150, 0, 0))], "mold cooling fan",
              "Fan on the bracket with four M4 screws, then the bracket foot to the base with two M6 screws",
              elev=18, azim=-40)


@stp(12)
def p12():
    M = made()
    return st(12, _state(11), [mv(M["hood"], (-160, 0, 0))], "fume hood",
              "Arm to the column's left face, two M6 screws into rivnuts; hood face 100 mm from the funnel axis",
              elev=18, azim=-55)


@stp(13)
def p13():
    M = made()
    return st(13, _state(12), [mv(M["ctrl"], (-150, -100, 0))], "onto the bench, and wiring",
              "Bolt the base over the bench hole with four M10 bolts; control box to its left; heaters, thermocouples, fans",
              context=[bench(-480, 260, -220, 200)], elev=20, azim=-50)


@stp(14)
def p14():
    M = made()
    done = [p for p in _state(12) if p.name != "Nozzle zone shield"]
    done.append(part("Shield sides (front open)", C["shield_sides"].shape, COL["shield"]))
    return st(14, done, [mv(part("Test plaque mold", M["mold"].shape, "#0369A1"), (0, -220, 0))], "test mold onto the table",
              "Front open (not drawn); mold on the table; table raised with the handwheel until the nozzle seats; front shut",
              context=[bench(-480, 260, -220, 200)], elev=22, azim=-65)


def steps(which=None):
    return [f() for n, f in sorted(STEPS.items()) if not which or n in which]


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps}
    for w in what:
        name, _, sel = w.partition(":")
        sel = {int(x) for x in sel.split(",")} if sel else None
        r = fns[name](sel) if sel is not None else fns[name]()
        print(w, "->", r)
