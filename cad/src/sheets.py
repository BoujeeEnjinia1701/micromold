"""MicroMold general arrangement sheet MMD-DWG-001, Rev P5 (TRL 3, constructable design MMD-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/MMD-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions are taken from PARAMS and derived(), so
they follow any parameter change. The press is drawn without the control box and wiring,
which sit loose on the bench. The concept blueprint in media/ is MMD-DWG-010.
PRELIMINARY, NOT FOR FABRICATION.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, derived  # noqa: E402

DATE = "2026-10-02"
PRESS = ["base", "drive", "ram", "loadcell", "plunger", "barrel", "heaters", "nozzle", "bracket",
         "guard", "clamp", "mold", "shield", "hood", "coolfan", "rest", "tqsocket"]


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic for a front and right view pair (no top view
    above the front, so that the sheet can be drawn at 1:10). Returns {name: (x, y, w, h)}."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab, dl = 14, 12, 11
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (fw + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * max(fh, rh) + gap + 2 * lab + dl)) / 2 + dl
    front_y = ay + lab + gap
    row_h = k * max(fh, rh)
    return {"front": (ax, front_y, k * fw, row_h), "right": (ax + k * fw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    parts = build_parts()
    from build123d import Box, Pos
    above = Pos(0, 0, 2500) * Box(5000, 5000, 5000)          # the lift screw's end below the bench top is left off
    asm = Compound(children=[(parts[k] & above) if k == "clamp" else parts[k] for k in PRESS])
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="MicroMold", title="General arrangement", dwg_no="MMD-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE, scale=0.1, theme="technical",
              material="Steel frame and barrel; 6061 mold; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", "2026-09-25", "AC"),
                         ("P2", "Mold cooling fan added; 300 W bands (MMD-DDR-002)", "2026-09-25", "AC"),
                         ("P3", "Layout and labels tidied", "2026-09-30", "AC"),
                         ("P4", "Design made constructable (MMD-DDR-003)", "2026-10-01", "AC"),
                         ("P5", "Plunger rest and torque-limiting socket added (decisions of 2026-10-02)", "2026-10-02", "AC")])
    s.add_ortho(views, names=("front", "right"))
    k = s.scale
    c = ortho_cells(s, views)
    # top view, relocated to the right of the right view at the same scale (labeled as such)
    tw, th = _viewbox(Path(views["top"]).read_text())[2:]
    rx, ry, rw_, rh_ = c["right"]
    c["top"] = (rx + rw_ + 22, ry, k * tw, k * th)
    s.add_svg(views["top"], *c["top"], scale=k, label="Top view (relocated)", sublabel="Scale 1:10")
    L = []

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zb = Z(0)
    L.append(f'<line x1="{X(bb.min.X) - 4:.2f}" y1="{zb:.2f}" x2="{X(bb.max.X) + 4:.2f}" y2="{zb:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(X(bb.max.X) + 4, zb + 3.5, "BENCH TOP", 2.0, 600, MUTED, "end"))
    xr = X(bb.min.X) - 14     # the kit draws the overall height at 7 mm
    for i, (zz, label) in enumerate(((D["noz0"], f"{D['noz0']:.0f} nozzle tip"),
                                     (D["bar1"], f"{D['bar1']:.0f} barrel top"),
                                     (D["pin_z"], f"{D['pin_z']:.0f} pinion"))):
        xd = xr - 6 * i
        L += [ext(X(0), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, Z(zz), zb, label)
    xl = X(-P["base"][0] / 2) - 3
    L += [ext(X(-P["table"][0] / 2), Z(D["table_top"]), xl - 1, Z(D["table_top"]))]
    L += dim_v(xl, Z(D["table_top"]), zb, f"{D['table_top']:.0f} table")
    L += leader(X(0), Z(D["pl0"] + 100), X(bb.min.X) - 30, Z(D["pl0"] + 250), f"PLUNGER {P['bore']:.0f}, RAISED; STROKE {P['stroke']:.0f}", "end")
    L += leader(X(P["hood_x"] - 60), Z(D["fl1"] + 50), X(bb.min.X) - 30, Z(D["fl1"] + 120), "SIDE FUME HOOD", "end")
    L += leader(X(0), Z(D["bar0"] + 150), X(bb.min.X) - 30, Z(D["bar0"] + 60), "BARREL, HEATERS, JACKET", "end")
    L += leader(X(-P["shield"][0] / 2), Z(D["noz0"] - 60), X(bb.min.X) - 30, Z(D["noz0"] - 60), "NOZZLE ZONE SHIELD", "end")
    L += leader(X(-40), Z(D["split"]), X(bb.min.X) - 30, Z(D["split"] - 60), "TEST MOLD ON LIFT TABLE", "end")
    L += leader(X(P["cool_fan_x"]), Z(P["cool_fan_z"] - 40), X(bb.max.X) + 6, Z(P["cool_fan_z"] - 100), "MOLD COOLING FAN")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    bx, by, _ = P["base"]
    y0b, y1b = P["base_y"] - by / 2, P["base_y"] + by / 2
    L += [ext(Xt(-bx / 2), Yt(y1b), Xt(-bx / 2), Yt(bb.max.Y) - 5), ext(Xt(bx / 2), Yt(y1b), Xt(bx / 2), Yt(bb.max.Y) - 5)]
    L += dim_h(Xt(-bx / 2), Xt(bx / 2), Yt(bb.max.Y) - 4, f"{bx:.0f} base")
    L += [ext(Xt(bx / 2), Yt(y0b), Xt(bb.max.X) + 7, Yt(y0b)), ext(Xt(bx / 2), Yt(y1b), Xt(bb.max.X) + 7, Yt(y1b))]
    L += dim_v(Xt(bb.max.X) + 6, Yt(y1b), Yt(y0b), f"{by:.0f}")
    L.append(_t(Xt(bb.min.X), Yt(bb.min.Y) - 1, "OPERATOR SIDE (-Y)", 1.9, 400, MUTED, "start"))

    # right view (from +X): Y to the right... looking along -X, +Y appears to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += [ext(Yr(0), Zr(D["head1"]) - 1, Yr(0), Zr(bb.max.Z) - 6), ext(Yr(P["col_y"]), Zr(D["head1"]) - 1, Yr(P["col_y"]), Zr(bb.max.Z) - 6)]
    L += dim_h(Yr(0), Yr(P["col_y"]), Zr(bb.max.Z) - 5, f"{P['col_y']:.0f} axis to column")
    L += leader(Yr(D["knob"][0] + P["pinion_y"]), Zr(D["knob"][1]), Yr(D["knob"][0] + P["pinion_y"]) + 2, Zr(bb.max.Z) - 14,
                f"RATCHET HANDLE {P['handle_len']:.0f}, {P['handle_up_deg']:.0f} DEG UP TO 60 DEG DOWN")

    s._layers += L
    s.add_svg(views["iso"], 276, 44, 140, 82, label="Isometric view", sublabel="Not to scale; control box not shown")
    fo, _ = P["flange"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Barrel {P['barrel_od']:.0f} OD, bore {P['bore']:.0f} (22 H8/f7 plunger fit), {P['barrel_len']:.0f} long",
        f"Flange {fo:.0f} OD, 4 x M8 on mica pads; {P['bracket'][2]:.0f} mm shelf at {D['brk1']:.0f}",
        f"Nozzle orifice {P['nozzle_orifice']:.0f}; sprue 5 to 7 taper; tip at {D['noz0']:.0f}",
        f"Stroke {P['stroke']:.0f}, {D['in_bore']:.0f} in the bore; ram {D['ram_len']:.0f} long, 28 square",
        f"Pinion r {P['pinion_r']:.0f}; ratchet handle {P['handle_len']:.0f}; {P['handle_len'] / P['pinion_r']:.1f}:1",
        f"Torque socket {P['tq_set_Nm']:.0f} N m; plunger rest cup {P['rest_cup'][0]:.0f} OD, {P['rest_z']:.0f} up",
        f"Lift table {P['table'][0]:.0f} x {P['table'][1]:.0f}, top {P['table_min_top']:.0f} to {P['table_min_top'] + P['table_travel']:.0f}; Tr20 screw, handwheel nut",
        f"Test mold {P['mold'][0]:.0f} x {P['mold'][1]:.0f} x {2 * P['mold'][2]:.0f}; four M10 8.8 in inserts at 20 kN",
        f"Load cell 10 kN on a {P['spacer_t']:.0f} mm G-11 thermal spacer",
        f"Hood face {P['hood_face'][0]:.0f} x {P['hood_face'][1]:.0f}, {-P['hood_x']:.0f} from the axis; {P['duct_d']:.0f} duct",
        f"Mold cooling fan {P['cool_fan'][1]:.0f} x {P['cool_fan'][2]:.0f} x {P['cool_fan'][0]:.0f} at X {P['cool_fan_x']:.0f}; barrel bands 2 x 300 W",
        f"Lift screw runs on {-(D['table_top'] - P['lift_screw'][1]):.0f} below the bench top (not drawn), through a 25 mm hole",
        "Third-angle; front view from -Y (operator side)",
    ], x=276, y=142, width=140)
    out = s.save(ROOT / "cad" / "drawings" / "MMD-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
