"""MicroMold parametric model (build123d), TRL 3 (updated for MMD-DDR-002: mold cooling fan).

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl for the assembly, the barrel set
(barrel, heaters, nozzle, jacket) and the test plaque mold set.

Massing-plus detail: correct interfaces and main dimensions, not fabrication detail.
PRELIMINARY, NOT FOR FABRICATION.

Coordinates in mm. Z up, bench top at Z = 0, the operator stands on the -Y side.
The injection axis is vertical at X = 0, Y = 0. The rack ram pushes the plunger down
into the heated barrel, and melt leaves the nozzle into the mold on the lift table.
The model is shown with the plunger raised (loading position) and the lift table set
for the 90 mm test plaque mold seated on the nozzle.
"""
from math import cos, pi, radians, sin
from pathlib import Path

# ---------------- top-level parameters (mm unless stated) ----------------
PARAMS = {
    # base and column
    "base": (320.0, 260.0, 12.0),        # X, Y, thickness
    "base_y": 20.0,                      # base plate center Y
    "col": (80.0, 60.0, 3.0),            # column tube X, Y, wall
    "col_y": 95.0,                       # column center Y
    # injection unit
    "bore": 22.0,                        # barrel bore = plunger diameter
    "barrel_od": 42.0,
    "barrel_len": 260.0,
    "nozzle_len": 40.0,
    "nozzle_orifice": 4.0,               # TRL 3: 4 mm (was 3 mm), see MMD-CAL-001 section E
    "nozzle_tip_z": 190.0,               # set by the tallest mold stack, see derived()
    "flange": (80.0, 10.0),              # barrel flange OD, thickness (sits on the bracket)
    "funnel": (80.0, 22.0),              # funnel OD, height above the flange
    "heater": (54.0, 50.0),              # band heater OD, width (two 300 W bands, DDR-002)
    "heater_z": (290.0, 410.0),          # band heater centers
    "jacket": (116.0, 6.0, 14.0),        # jacket and guard OD; clearance above nozzle, below bracket
    "bracket": (110.0, 150.0, 20.0),     # barrel bracket X, Y, thickness (TRL 3: 20 mm plate)
    "plunger_len": 200.0,
    "plunger_clear": 30.0,               # plunger tip above the barrel top when raised
    "stroke": 150.0,                     # ram travel used
    "spacer_t": 10.0,                    # glass-epoxy thermal spacer under the load cell (TRL 3)
    "loadcell": (56.0, 30.0),            # load cell OD, height
    "ram": 28.0,                         # rack ram, square
    "head": (110.0, 140.0, 140.0),       # arbor press head X, Y, Z
    "head_y": 25.0,
    "head_gap": 10.0,                    # head underside above the ram end, plunger raised
    "pinion_r": 20.0,                    # pitch radius
    "pinion_y": 30.0,
    "rack_engage": 25.0,                 # rack kept above the pinion at full stroke
    "handle_len": 450.0,                 # ratchet handle, pinion axis to grip center
    "handle_up_deg": 30.0,               # highest start angle of a pull above horizontal
    "knob_r": 24.0,
    # mold and clamp
    "mold": (120.0, 90.0, 45.0),         # each plate X, Y, thickness
    "cavity": (64.0, 50.0, 6.0),         # test plaque
    "mold_bolt_xy": (48.0, 33.0),        # M10 bolt positions
    "table": (170.0, 130.0, 12.0),       # lift table
    "table_min_top": 60.0,               # table top with the jack collapsed
    "table_travel": 100.0,
    "stack_max": 120.0,                  # tallest mold stack (MMD-REQ-001 R7)
    "mold_drop": 10.0,                   # lowering needed to clear the nozzle
    # guards and extraction (TRL 3)
    "shield": (230.0, 170.0, 1.5),       # nozzle zone shield X, Y, sheet thickness
    "hood_face": (150.0, 100.0),         # side hood face, Y x Z
    "hood_x": -100.0,                    # hood face plane
    "duct_d": 100.0,
    # mold cooling fan (DDR-002): 120 mm axial fan on an angle bracket, +X side, blowing through the shield side
    "cool_fan": (38.0, 120.0, 120.0),    # X depth, Y, Z
    "cool_fan_x": 140.0,                 # fan center X (shield side at 115 mm, base edge at 160 mm)
    "cool_fan_z": 145.0,                 # fan center Z, level with the test mold parting line
    # control box (on the bench, left of the press)
    "ctrl": (200.0, 130.0, 120.0),
    "ctrl_xy": (-330.0, -10.0),
}


def derived(p=PARAMS):
    """Stack-up of the vertical axis and a few derived quantities."""
    d = {}
    d["noz0"] = p["nozzle_tip_z"]
    d["noz1"] = d["noz0"] + p["nozzle_len"]
    d["bar0"] = d["noz1"]
    d["bar1"] = d["bar0"] + p["barrel_len"]
    d["fl1"] = d["bar1"] + p["flange"][1]
    d["fun1"] = d["bar1"] + p["funnel"][1]
    d["brk1"] = d["bar1"]                                  # bracket top face carries the flange
    d["brk0"] = d["brk1"] - p["bracket"][2]
    d["pl0"] = d["bar1"] + p["plunger_clear"]              # plunger tip, raised
    d["pl1"] = d["pl0"] + p["plunger_len"]
    d["sp1"] = d["pl1"] + p["spacer_t"]
    d["lc1"] = d["sp1"] + p["loadcell"][1]
    d["ram0"] = d["lc1"]                                   # ram end, raised
    d["head0"] = d["ram0"] + p["head_gap"]
    d["head1"] = d["head0"] + p["head"][2]
    d["pin_z"] = d["head0"] + p["head"][2] / 2
    d["ram1"] = d["pin_z"] + p["rack_engage"] + p["stroke"]  # ram top, raised
    d["ram_len"] = d["ram1"] - d["ram0"]
    d["tip_low"] = d["pl0"] - p["stroke"]                  # plunger tip, full stroke
    d["in_bore"] = d["bar1"] - d["tip_low"]                # stroke inside the bore
    d["reservoir"] = d["tip_low"] - d["bar0"]              # bore left below the tip at full stroke
    a = radians(p["handle_up_deg"])
    d["knob"] = (p["handle_len"] * -cos(a), d["pin_z"] + p["handle_len"] * sin(a))  # (y offset, z)
    d["handle_top"] = d["knob"][1] + p["knob_r"]
    d["overall_h"] = max(d["handle_top"], d["ram1"], d["head1"])
    mh = 2 * p["mold"][2]
    d["mold_h"] = mh
    d["table_top"] = d["noz0"] - mh                        # test mold seated on the nozzle
    d["table_min_needed"] = p["table_min_top"] + p["stack_max"] + p["mold_drop"]
    d["mold0"] = d["table_top"]
    d["split"] = d["mold0"] + p["mold"][2]
    d["mold1"] = d["split"] + p["mold"][2]
    d["col_front"] = p["col_y"] - p["col"][1] / 2
    d["area_plunger"] = pi / 4 * p["bore"] ** 2
    return d


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    b = _b3d()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def zring(ro, ri, z0, z1, x=0.0, y=0.0):
    return zcyl(ro, z0, z1, x, y) - zcyl(ri, z0 - 1, z1 + 1, x, y)


def tube(a, c, r):
    b = _b3d()
    a = b.Vector(*a); c = b.Vector(*c); dv = c - a
    return b.Solid.make_cylinder(r, dv.length, b.Plane(origin=a, z_dir=dv.normalized()))


def build_parts(p=PARAMS):
    """Return {name: shape} for every modeled BOM item."""
    b = _b3d()
    d = derived(p)
    m = {}
    bx, by, bt = p["base"]
    m["base"] = box(0, p["base_y"], bt / 2, bx, by, bt)

    # 2 column, arbor press head, pinion shaft and ratchet handle
    cx, cy, cw = p["col"]
    col = box(0, p["col_y"], (bt + d["head1"]) / 2, cx, cy, d["head1"] - bt)
    col = col - box(0, p["col_y"], (bt + d["head1"]) / 2, cx - 2 * cw, cy - 2 * cw, d["head1"] - bt + 2)
    hx, hy, hz = p["head"]
    head = box(0, p["head_y"], (d["head0"] + d["head1"]) / 2, hx, hy, hz)
    head = head - box(0, 0, (d["head0"] + d["head1"]) / 2, p["ram"] + 2, p["ram"] + 2, hz + 2)
    py, pz = p["pinion_y"], d["pin_z"]
    shaft = tube((-hx / 2 - 20, py, pz), (hx / 2 + 25, py, pz), 14)
    hxp = hx / 2 + 25
    ky, kz = d["knob"]
    ratchet = tube((hxp, py, pz), (hxp + 20, py, pz), 20)     # ratchet head on the shaft
    handle = tube((hxp + 10, py, pz), (hxp + 10, py + ky, kz), 11) + b.Pos(hxp + 10, py + ky, kz) * b.Sphere(p["knob_r"])
    m["drive"] = col + head + shaft + ratchet + handle

    # 3 rack ram
    m["ram"] = box(0, 0, (d["ram0"] + d["ram1"]) / 2, p["ram"], p["ram"], d["ram_len"])

    # 4 load cell with glass-epoxy thermal spacer
    lr, lh = p["loadcell"]
    m["loadcell"] = zcyl(lr / 2, d["sp1"], d["lc1"]) + zcyl(p["bore"] / 2 + 4, d["pl1"], d["sp1"])

    # 5 plunger
    m["plunger"] = zcyl(p["bore"] / 2, d["pl0"], d["pl1"])

    # 6 barrel with flange and funnel
    R = p["bore"] / 2
    fod, ft = p["flange"]
    barrel = zring(p["barrel_od"] / 2, R, d["bar0"], d["bar1"]) + zring(fod / 2, R, d["bar1"], d["fl1"])
    funnel = zring(p["funnel"][0] / 2, R, d["fl1"], d["fun1"]) - b.Pos(0, 0, d["fun1"] + 2) * b.Cone(R, p["funnel"][0] / 2 - 4, d["fun1"] - d["fl1"] + 0.01, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MAX))
    m["barrel"] = barrel + funnel

    # 7 band heaters
    ho, hw = p["heater"]
    m["heaters"] = zring(ho / 2, p["barrel_od"] / 2, p["heater_z"][0] - hw / 2, p["heater_z"][0] + hw / 2) \
        + zring(ho / 2, p["barrel_od"] / 2, p["heater_z"][1] - hw / 2, p["heater_z"][1] + hw / 2)

    # 8 nozzle and nozzle heater
    ro = p["nozzle_orifice"] / 2
    m["nozzle"] = zring(12, ro, d["noz0"], d["noz1"]) + zring(20, 12, d["noz0"] + 8, d["noz1"] - 4)

    # 9 barrel bracket (flange sits on it through mica pads)
    kx, ky_, kt = p["bracket"]
    brk_len = ky_
    brk = box(0, d["col_front"] + cw - brk_len / 2 + 0, (d["brk0"] + d["brk1"]) / 2, kx, brk_len, kt)
    m["bracket"] = brk - zcyl(p["barrel_od"] / 2 + 2, d["brk0"] - 1, d["brk1"] + 1)

    # 10 insulation jacket and perforated guard
    jo, jlo, jhi = p["jacket"]
    m["guard"] = zring(jo / 2, p["heater"][0] / 2 + 3, d["bar0"] + jlo, d["brk0"] - jhi)

    # 11 mold clamp: screw jack and lift table
    tx, ty, tt = p["table"]
    tt_top = d["table_top"]
    jack = box(0, 0, (bt + tt_top - tt) / 2, 70, 70, tt_top - tt - bt)
    m["clamp"] = jack + box(0, 0, tt_top - tt / 2, tx, ty, tt) \
        + tube((0, -35, bt + 22), (0, -150, bt + 22), 8) + tube((-45, -150, bt + 22), (45, -150, bt + 22), 7)

    # 12 mold set: two plates, four M10 bolts, test plaque cavity, sprue
    mx, my, mt = p["mold"]
    mold = box(0, 0, (d["mold0"] + d["split"]) / 2, mx, my, mt - 0.5) + box(0, 0, (d["split"] + d["mold1"]) / 2, mx, my, mt - 0.5)
    bxo, byo = p["mold_bolt_xy"]
    for sx in (-bxo, bxo):
        for sy in (-byo, byo):
            mold = mold + zcyl(8, d["mold1"] - 0.25, d["mold1"] + 7, sx, sy)          # bolt heads; nuts below in table slots
    cvx, cvy, cvz = p["cavity"]
    mold = mold - box(0, 0, d["split"] - cvz / 2, cvx, cvy, cvz) - zcyl(3, d["split"], d["mold1"] + 1)
    m["mold"] = mold

    # 13 control box
    ccx, ccy = p["ctrl_xy"]
    qx, qy, qz = p["ctrl"]
    m["ctrl"] = box(ccx, ccy, qz / 2, qx, qy, qz) + box(ccx - 45, ccy - qy / 2 - 3, 80, 60, 6, 36) + box(ccx + 45, ccy - qy / 2 - 3, 80, 60, 6, 36)

    # 14 wiring harness
    m["wiring"] = tube((ccx + qx / 2, ccy + 30, 100), (-160, 60, 120), 6) + tube((-160, 60, 120), (-60, 30, 330), 6)

    # 16 nozzle zone shield: sides and hinged front, open at the back (column side)
    sx_, sy_, st = p["shield"]
    z0s, z1s = bt + 40, d["bar0"] + 40
    zc, zh = (z0s + z1s) / 2, z1s - z0s
    yf = -sy_ / 2 - 10
    side = lambda x: box(x, yf + sy_ / 2, zc, st, sy_, zh)
    front = box(0, yf, zc, sx_, st, zh) - box(0, yf, zc - 10, sx_ - 60, st + 2, zh - 80)   # window opening
    m["shield"] = side(-sx_ / 2) + side(sx_ / 2) + front          # perforated window panel not modeled so the mold shows

    # 17 side hood and duct stub on the -X side, level with the funnel
    fy, fz = p["hood_face"]
    hxf = p["hood_x"]
    hz = d["fl1"]
    hood = box(hxf - 60, 0, hz, 120, fy, fz) - box(hxf - 58, 0, hz, 118, fy - 4, fz - 4)
    hood = hood - box(hxf + 1, 0, hz, 6, fy - 4, fz - 4)                                  # open face
    hood = hood + box(hxf - 60, 0, hz + fz / 2 + 60, p["duct_d"], p["duct_d"], 120)       # duct stub (massing)
    m["hood"] = hood

    # 18 mold cooling fan on an angle bracket bolted to the base plate (DDR-002)
    fx, fyy, fzz = p["cool_fan"]
    xc, zc2 = p["cool_fan_x"], p["cool_fan_z"]
    fan = box(xc, 0, zc2, fx, fyy, fzz) - b.Pos(xc, 0, zc2) * b.Rotation(0, 90, 0) * b.Cylinder(fyy / 2 - 4, fx + 2)
    fan = fan + b.Pos(xc, 0, zc2) * b.Rotation(0, 90, 0) * b.Cylinder(20, fx - 4)       # hub
    z_leg0 = bt
    leg = box(xc, 0, (z_leg0 + zc2 - fzz / 2) / 2, 3, 60, zc2 - fzz / 2 - z_leg0) + box(xc - 10, 0, bt + 1.5, 20, 60, 3)
    m["coolfan"] = fan + leg
    return m


ORDER = ["base", "drive", "ram", "loadcell", "plunger", "barrel", "heaters", "nozzle", "bracket",
         "guard", "clamp", "mold", "ctrl", "wiring", "shield", "hood", "coolfan"]


def assembly(p=PARAMS, parts=None):
    b = _b3d()
    parts = parts or build_parts(p)
    return b.Compound(children=[parts[k] for k in ORDER])


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    P, D = PARAMS, derived()
    parts = build_parts()
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    sets = {
        "micromold-assembly": assembly(parts=parts),
        "barrel-set": Compound(children=[parts[k] for k in ("barrel", "heaters", "nozzle", "guard")]),
        "mold-set": Compound(children=list(parts["mold"].solids())),
    }
    for name, c in sets.items():
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"nozzle tip {D['noz0']:.0f}, barrel {D['bar0']:.0f} to {D['bar1']:.0f}, pinion {D['pin_z']:.0f}, "
          f"ram {D['ram_len']:.0f} long, handle top {D['handle_top']:.0f}, overall {D['overall_h']:.0f} mm")
    print(f"stroke in bore {D['in_bore']:.0f} mm, reservoir {D['reservoir']:.0f} mm, "
          f"table top {D['table_top']:.0f} (min {P['table_min_top']:.0f}, max {P['table_min_top'] + P['table_travel']:.0f})")
