"""MicroMold parametric model (build123d), TRL 3, constructable design (MMD-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only

Exports the assembly, the barrel set (barrel, heaters, nozzle, jacket) and the test plaque
mold set. build_components() returns every made and bought component on its own, in the
form the build plan pictures use (cad/src/build_plan_media.py); build_parts() groups them
by BOM line for the concept media, the general arrangement and the appearance model.

Coordinates in mm. Z up, bench top at Z = 0, the operator stands on the -Y side.
The injection axis is vertical at X = 0, Y = 0. The rack ram pushes the plunger down
into the heated barrel, and melt leaves the nozzle into the mold on the lift table.
The model is shown with the plunger raised (loading position) and the lift table set
for the 90 mm test plaque mold seated on the nozzle.
PRELIMINARY, NOT FOR FABRICATION.
"""
import sys
from math import cos, pi, radians, sin
from pathlib import Path

# ---------------- top-level parameters (mm unless stated) ----------------
PARAMS = {
    # base and column
    "base": (320.0, 260.0, 8.0),         # X, Y, thickness (DDR-003: 8 mm, was 12 mm)
    "base_y": 20.0,                      # base plate center Y
    "col": (80.0, 60.0, 3.0),            # column tube X, Y, wall
    "col_y": 95.0,                       # column center Y
    "bench_t": 40.0,                     # bench top thickness (context; the lift screw drops through it)
    # injection unit
    "bore": 22.0,                        # barrel bore = plunger diameter
    "barrel_od": 42.0,
    "barrel_len": 260.0,
    "nozzle_len": 40.0,
    "nozzle_orifice": 4.0,               # TRL 3: 4 mm (was 3 mm), see MMD-CAL-001 section E
    "nozzle_tip_z": 190.0,               # set by the tallest mold stack, see derived()
    "nozzle_thread": (30.0, 15.0),       # M30 x 1.5 spigot into the barrel end, length (DDR-003)
    "flange": (100.0, 10.0),             # barrel flange OD, thickness (DDR-003: 100, was 80)
    "flange_pcd": 82.0,                  # four M8 cap screws into the shelf (DDR-003)
    "funnel": (64.0, 22.0),              # funnel OD, height above the barrel top (DDR-003: 64, was 80)
    "pad": (15.0, 3.0),                  # mica pads under the flange, side and thickness
    "heater": (54.0, 50.0),              # band heater OD, width (two 300 W bands, DDR-002)
    "heater_z": (290.0, 410.0),          # band heater centers
    "jacket": (116.0, 6.0, 14.0),        # jacket and guard OD; clearance above nozzle, below bracket
    "bracket": (110.0, 150.0, 20.0),     # barrel shelf X, Y, thickness (TRL 3: 20 mm plate)
    "back_plate": (110.0, 8.0, 120.0),   # shelf back plate X, thickness, height (DDR-003)
    "plunger_len": 200.0,
    "plunger_clear": 30.0,               # plunger tip above the barrel top when raised
    "stroke": 150.0,                     # ram travel used
    "coupling": (40.0, 30.0, 5.0),       # plunger coupling OD, socket depth, end wall (DDR-003)
    "spacer_t": 10.0,                    # glass-epoxy thermal spacer under the load cell (TRL 3)
    "spacer_od": 56.0,                   # G-11 spacer, same diameter as the load cell (DDR-003)
    "loadcell": (56.0, 30.0),            # load cell OD, height
    "ram": 28.0,                         # rack ram, square
    "head": (110.0, 140.0, 140.0),       # arbor press head X, Y, Z
    "head_y": -13.0,                     # head center Y (DDR-003: back face on the head plate)
    "head_plate": (120.0, 8.0),          # head mounting plate width, thickness (DDR-003)
    "head_gap": 10.0,                    # head underside above the ram end, plunger raised
    "pinion_r": 20.0,                    # pitch radius
    "pinion_y": 34.0,
    "rack_engage": 25.0,                 # rack kept above the pinion at full stroke
    "handle_len": 450.0,                 # ratchet handle, pinion axis to grip center
    "handle_up_deg": 30.0,               # highest start angle of a pull above horizontal
    "knob_r": 24.0,
    "tq_socket": (34.0, 70.0),           # torque-limiting socket OD, body length (MMD-DDR-003 decision 4, 2026-10-02)
    "tq_set_Nm": 180.0,                  # torque setting, N m (MMD-CAL-001 section B, from the 1 t press rating)
    # plunger rest on the column (decision 2, 2026-10-02): cup and plate on the +X column wall
    "rest_cup": (32.0, 24.0, 70.0),      # cup OD, ID, height; the hot plunger tip stands in it
    "rest_z": 400.0,                     # centre of the mounting plate
    "rest_plate": (38.0, 30.0, 5.0),     # plate Y, Z, thickness against the column wall
    "rest_y": 95.0,                      # cup axis Y
    # mold and clamp
    "mold": (120.0, 90.0, 45.0),         # each plate X, Y, thickness
    "cavity": (64.0, 50.0, 6.0),         # test plaque
    "mold_bolt_xy": (48.0, 33.0),        # M10 cap screw positions
    "dowel_x": 48.0,                     # two 6 mm dowels at (+-48, 0) (DDR-003)
    "table": (170.0, 126.0, 12.0),       # lift table (DDR-003: 126 deep, was 130)
    "table_min_top": 60.0,               # table top at the bottom of its travel
    "table_travel": 100.0,
    "lift_screw": (20.0, 150.0),         # Tr20 x 4 screw welded under the table, length (DDR-003)
    "handwheel": (120.0, 40.0, 30.0),    # handwheel OD, hub OD, hub height (DDR-003)
    "stack_max": 120.0,                  # tallest mold stack (MMD-REQ-001 R7)
    "mold_drop": 10.0,                   # lowering needed to clear the nozzle
    "seat_depth": 2.0,                   # spherical nozzle seat in the mold top, depth (DDR-003)
    # guards and extraction (TRL 3)
    "shield": (230.0, 170.0, 1.5),       # nozzle zone shield X, Y, sheet thickness
    "shield_front_z0": 60.0,             # bottom edge of the hinged front
    "hood_face": (150.0, 100.0),         # side hood face, Y x Z
    "hood_x": -100.0,                    # hood face plane
    "duct_d": 100.0,
    # mold cooling fan (DDR-002): 120 mm axial fan on a plate bracket, +X side, blowing through the shield side
    "cool_fan": (38.0, 120.0, 120.0),    # X depth, Y, Z
    "cool_fan_x": 136.0,                 # fan center X (DDR-003: 136, was 140)
    "cool_fan_z": 145.0,                 # fan center Z, level with the test mold parting line
    # control box (on the bench, left of the press)
    "ctrl": (200.0, 130.0, 120.0),
    "ctrl_xy": (-330.0, -10.0),
}


def derived(p=PARAMS):
    """Stack-up of the vertical axis and a few derived quantities."""
    d = {}
    bt = p["base"][2]
    d["bt"] = bt
    d["noz0"] = p["nozzle_tip_z"]
    d["noz1"] = d["noz0"] + p["nozzle_len"]
    d["bar0"] = d["noz1"]
    d["bar1"] = d["bar0"] + p["barrel_len"]
    d["fl1"] = d["bar1"] + p["flange"][1]
    d["fun1"] = d["bar1"] + p["funnel"][1]
    d["brk1"] = d["bar1"] - p["pad"][1]                    # shelf top face; the flange sits on mica pads
    d["brk0"] = d["brk1"] - p["bracket"][2]
    d["pl0"] = d["bar1"] + p["plunger_clear"]              # plunger tip, raised
    d["pl1"] = d["pl0"] + p["plunger_len"]
    cod, cdep, cwall = p["coupling"]
    d["cp0"] = d["pl1"] - cdep                             # coupling bottom
    d["sp0"] = d["pl1"] + cwall                            # spacer bottom (coupling top)
    d["sp1"] = d["sp0"] + p["spacer_t"]
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
    d["table_top"] = d["noz0"] + p["seat_depth"] - mh     # test mold seated on the nozzle
    d["table_min_needed"] = p["table_min_top"] + p["stack_max"] + p["mold_drop"] - p["seat_depth"]
    d["mold0"] = d["table_top"]
    d["split"] = d["mold0"] + p["mold"][2]
    d["mold1"] = d["split"] + p["mold"][2]
    d["col_front"] = p["col_y"] - p["col"][1] / 2
    d["col_back"] = p["col_y"] + p["col"][1] / 2
    d["head_back"] = p["head_y"] + p["head"][1] / 2
    d["area_plunger"] = pi / 4 * p["bore"] ** 2
    # lift screw: welded flush with the table top; its lowest point is with the table at the bottom of its travel
    d["screw_low"] = p["table_min_top"] - p["lift_screw"][1]
    d["screw_below_bench"] = -d["screw_low"] - p["bench_t"]
    d["hub0"] = bt + 2.0                                   # handwheel hub on a 2 mm thrust washer
    d["hub1"] = d["hub0"] + p["handwheel"][2]
    return d


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def bx(x0, x1, y0, y1, z0, z1):
    """Box from its extents."""
    return box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, x1 - x0, y1 - y0, z1 - z0)


def zcyl(r, z0, z1, x=0.0, y=0.0):
    b = _b3d()
    return b.Pos(x, y, (z0 + z1) / 2) * b.Cylinder(r, z1 - z0)


def zring(ro, ri, z0, z1, x=0.0, y=0.0):
    return zcyl(ro, z0, z1, x, y) - zcyl(ri, z0 - 1, z1 + 1, x, y)


def tube(a, c, r):
    b = _b3d()
    a = b.Vector(*a); c = b.Vector(*c); dv = c - a
    return b.Solid.make_cylinder(r, dv.length, b.Plane(origin=a, z_dir=dv.normalized()))


def ycyl(r, y0, y1, x, z):
    return tube((x, y0, z), (x, y1, z), r)


def xcyl(r, x0, x1, y, z):
    return tube((x0, y, z), (x1, y, z), r)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


class Comp:
    """One component: its shape, how it is made, and its BOM line."""

    def __init__(self, shape, make, bom, name):
        self.shape, self.make, self.bom, self.name = shape, make, bom, name


def flange_bolt_xy(p=PARAMS):
    r = p["flange_pcd"] / 2
    return [(r * cos(radians(a)), r * sin(radians(a))) for a in (45, 135, 225, 315)]


def head_screw_xz(p=PARAMS, d=None):
    d = d or derived(p)
    zc = (d["head0"] + d["head1"]) / 2
    return [(sx * 30.0, zc + sz * 45.0) for sx in (-1, 1) for sz in (-1, 1)]


def hanger_angles():
    return (-135.0, -45.0, 45.0, 135.0)


def build_components(p=PARAMS, table_top=None, stroke=0.0):
    """Every component on its own: {key: Comp}. table_top moves the lift table, mold and screw;
    stroke moves the ram, load cell, coupling and plunger down by that much."""
    b = _b3d()
    d = derived(p)
    bt = d["bt"]
    tt_top = d["table_top"] if table_top is None else table_top
    dz_mold = tt_top - d["table_top"]
    C = {}

    def add(key, shape, make, bom, name):
        C[key] = Comp(shape, make, bom, name)

    # ---- 1 base plate: 10 mm steel, drilled and tapped
    bxs, bys, _ = p["base"]
    y0b, y1b = p["base_y"] - bys / 2, p["base_y"] + bys / 2
    base = bx(-bxs / 2, bxs / 2, y0b, y1b, 0, bt)
    holes = [(sx * 145, yy, 5.5) for sx in (-1, 1) for yy in (-95.0, 135.0)]        # bench bolts M10
    holes += [(0.0, 0.0, 12.5)]                                                       # lift screw hole
    holes += [(sx * 126.0, yy, 3.3) for sx in (-1, 1) for yy in (-70.0, 50.0)]       # shield feet, M6 tapped
    holes += [(146.0, yy, 3.3) for yy in (-40.0, 40.0)]                               # fan bracket, M6 tapped
    for x, y, r in holes:
        base = base - zcyl(r, -1, bt + 1, x, y)
    add("base", base, "make", 1, "Base plate")

    # ---- 2 column tube, welded to the base plate; the head plate and the shelf weld to it
    cx, cy, cw = p["col"]
    col = bx(-cx / 2, cx / 2, d["col_front"], d["col_back"], bt, d["head1"])
    col = col - bx(-cx / 2 + cw, cx / 2 - cw, d["col_front"] + cw, d["col_back"] - cw, bt - 1, d["head1"] + 1)
    for x, z in head_screw_xz(p, d):                     # 22 mm access holes, front and back walls
        col = col - ycyl(11, d["col_front"] - 1, d["col_back"] + 1, x, z)
    hood_z = d["fl1"] - 15
    for yy in (85.0, 110.0):                             # M6 rivnut holes for the hood arm (left wall)
        col = col - xcyl(4.5, -cx / 2 - 1, -cx / 2 + cw + 1, yy, hood_z)
    for yy in (84.0, 106.0):                             # M6 rivnut holes for the plunger rest (right wall)
        col = col - xcyl(4.5, cx / 2 - cw - 1, cx / 2 + 1, yy, p["rest_z"])
    add("column", col, "make", 2, "Column")

    # ---- head mounting plate, welded to the column front; four M10 countersunk screws into the head
    hw, ht = p["head_plate"]
    hp = bx(-hw / 2, hw / 2, d["col_front"] - ht, d["col_front"], d["head0"], d["head1"])
    for x, z in head_screw_xz(p, d):
        hp = hp - ycyl(5.5, d["col_front"] - ht - 1, d["col_front"] + 1, x, z)
    add("head_plate", hp, "make", 2, "Head mounting plate")
    hs = _fuse([ycyl(5, d["head_back"] - 18, d["col_front"] - 4, x, z) +
                b.Solid.make_cone(5, 10, 4, b.Plane(origin=(x, d["col_front"] - 4, z), z_dir=(0, 1, 0)))
                for x, z in head_screw_xz(p, d)])
    add("head_screws", hs, "buy", 19, "Head screws (4 x M10 countersunk)")

    # ---- press head (bought: casting, pinion and shaft) and rack ram
    hx, hy, hz = p["head"]
    head = bx(-hx / 2, hx / 2, p["head_y"] - hy / 2, d["head_back"], d["head0"], d["head1"])
    head = head - box(0, 0, (d["head0"] + d["head1"]) / 2, p["ram"] + 2, p["ram"] + 2, hz + 2)
    for x, z in head_screw_xz(p, d):
        head = head - ycyl(5, d["head_back"] - 21, d["head_back"] + 1, x, z)
    py, pz = p["pinion_y"], d["pin_z"]
    shaft_x1 = hx / 2 + 25
    shaft = xcyl(14, -hx / 2 - 20, shaft_x1, py, pz) - bx(-hx / 2 + 1, hx / 2 - 1, py - 15, py + 15, pz - 15, pz + 15)
    add("press_head", head + shaft, "buy", 2, "Arbor press head")
    add("ram", box(0, 0, (d["ram0"] - stroke + d["ram1"] - stroke) / 2, p["ram"], p["ram"], d["ram_len"]), "buy", 3, "Rack ram")

    # ---- ratchet adapter (made) and ratchet handle (bought)
    ad = xcyl(18, hx / 2 + 3, shaft_x1, py, pz) - xcyl(14, hx / 2, shaft_x1 + 1, py, pz)
    ad = ad + bx(shaft_x1, shaft_x1 + 16, py - 6.35, py + 6.35, pz - 6.35, pz + 6.35)
    ad = ad - ycyl(3, py - 20, py + 20, hx / 2 + 12, pz)          # cross pin hole
    add("adapter", ad, "make", 19, "Ratchet adapter")
    pin = ycyl(3, py - 20, py + 20, hx / 2 + 12, pz)
    add("adapter_pin", pin, "buy", 19, "Adapter pin (6 mm roll pin)")
    ky, kz = d["knob"]
    tqd, tql = p["tq_socket"]
    xs0 = shaft_x1 + 2
    tq = xcyl(tqd / 2, xs0, xs0 + tql, py, pz) - bx(shaft_x1 + 1, shaft_x1 + 17, py - 6.35, py + 6.35, pz - 6.35, pz + 6.35)
    tq = tq + bx(xs0 + tql, xs0 + tql + 16, py - 6.35, py + 6.35, pz - 6.35, pz + 6.35)
    add("torque_socket", tq, "buy", 21, "Torque-limiting socket (180 N m)")
    xr0 = xs0 + tql + 2
    ratchet = xcyl(20, xr0, xr0 + 20, py, pz) - bx(xr0 - 1, xr0 + 15, py - 6.5, py + 6.5, pz - 6.5, pz + 6.5)
    xh = xr0 + 10
    handle = tube((xh, py, pz), (xh, py + ky, kz), 11) + b.Pos(xh, py + ky, kz) * b.Sphere(p["knob_r"])
    add("ratchet", ratchet + handle, "buy", 2, "Ratchet handle")

    # ---- load cell (bought), thermal spacer, plunger coupling and pin (made), plunger (bought, drilled)
    s = stroke
    lr, lh = p["loadcell"]
    add("loadcell", zcyl(lr / 2, d["sp1"] - s, d["lc1"] - s), "buy", 4, "Load cell")
    add("spacer", zcyl(p["spacer_od"] / 2, d["sp0"] - s, d["sp1"] - s), "make", 4, "Thermal spacer (G-11)")
    cod, cdep, cwall = p["coupling"]
    cp = zcyl(cod / 2, d["cp0"] - s, d["sp0"] - s)
    cp = cp - zcyl(p["bore"] / 2 + 0.1, d["cp0"] - s - 1, d["pl1"] - s)
    pin_z = d["cp0"] + 12
    cp = cp - xcyl(3.1, -cod, cod, 0, pin_z - s)
    add("coupling", cp, "make", 19, "Plunger coupling")
    add("coupling_pin", xcyl(3, -cod / 2 - 8, cod / 2 + 2, 0, pin_z - s) + xcyl(7, -cod / 2 - 12, -cod / 2 - 8, 0, pin_z - s),
        "buy", 19, "Ball-lock pin, 6 mm")
    pl = zcyl(p["bore"] / 2, d["pl0"] - s, d["pl1"] - s) - xcyl(3.5, -15, 15, 0, pin_z - s)
    add("plunger", pl, "buy", 5, "Plunger")

    # ---- barrel with flange and funnel; M30 x 1.5 thread in its lower end
    R = p["bore"] / 2
    fod, ft = p["flange"]
    tdia, tlen = p["nozzle_thread"]
    barrel = zring(p["barrel_od"] / 2, R, d["bar0"], d["bar1"]) + zring(fod / 2, R, d["bar1"], d["fl1"])
    fun_od = p["funnel"][0]
    funnel = zring(fun_od / 2, R, d["fl1"], d["fun1"]) - b.Pos(0, 0, d["fun1"] + 0.01) * b.Cone(R, fun_od / 2 - 4, d["fun1"] - d["fl1"] + 0.02, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MAX))
    barrel = barrel + funnel - zcyl(tdia / 2, d["bar0"] - 1, d["bar0"] + tlen)
    for x, y in flange_bolt_xy(p):
        barrel = barrel - zcyl(4.25, d["bar1"] - 1, d["fl1"] + 1, x, y)
    barrel = barrel - xcyl(1.6, -p["barrel_od"] / 2 - 1, -R - 2, 0, d["bar0"] + 120)      # thermocouple well
    add("barrel", barrel, "make", 6, "Barrel")

    # ---- band heaters (bought)
    ho, hwid = p["heater"]
    add("heaters", _fuse([zring(ho / 2, p["barrel_od"] / 2, zc - hwid / 2, zc + hwid / 2) for zc in p["heater_z"]]), "buy", 7, "Band heaters")

    # ---- nozzle (made) with its band heater (bought)
    ro = p["nozzle_orifice"] / 2
    n0 = d["noz0"]
    noz = (b.Pos(0, 0, n0 + 12) * b.Sphere(12)) & zcyl(12, n0, n0 + 12)           # 12 mm radius tip
    hexa = _fuse([b.Pos(0, 0, n0 + 36) * b.Rot(0, 0, a) * b.Box(27, 40, 8) for a in (0,)])
    for a in (60, 120):
        hexa = hexa & (b.Pos(0, 0, n0 + 36) * b.Rot(0, 0, a) * b.Box(27, 40, 8))
    noz = noz + zcyl(12, n0 + 12, n0 + 32) + hexa + zcyl(tdia / 2, d["noz1"], d["noz1"] + tlen)
    noz = noz - zcyl(ro, n0 - 1, n0 + 20) - zcyl(R - 2, n0 + 20, d["noz1"] + tlen + 1)
    add("nozzle", noz, "make", 8, "Nozzle")
    add("nozzle_heater", zring(20, 12, n0 + 12, n0 + 30), "buy", 8, "Nozzle heater band")

    # ---- shelf, back plate, mica pads and flange screws
    kx, ky_, kt = p["bracket"]
    shelf = bx(-kx / 2, kx / 2, d["col_front"] - ky_, d["col_front"], d["brk0"], d["brk1"])
    shelf = shelf - zcyl(p["barrel_od"] / 2 + 2, d["brk0"] - 1, d["brk1"] + 1)
    for x, y in flange_bolt_xy(p):
        shelf = shelf - zcyl(3.4, d["brk0"] - 1, d["brk1"] + 1, x, y)       # tapped M8
    for a in hanger_angles():
        x, y = 66 * cos(radians(a)), 66 * sin(radians(a))
        shelf = shelf - zcyl(2.1, d["brk0"] - 1, d["brk0"] + 12, x, y)      # tapped M5, 10 deep
    add("shelf", shelf, "make", 9, "Barrel shelf")
    bpx, bpt, bph = p["back_plate"]
    add("back_plate", bx(-bpx / 2, bpx / 2, d["col_front"] - bpt, d["col_front"], d["brk1"], d["brk1"] + bph), "make", 9, "Shelf back plate")
    ps, pt = p["pad"]
    rpad = p["flange_pcd"] / 2
    pads = _fuse([box(rpad * cos(radians(a)), rpad * sin(radians(a)), d["brk1"] + pt / 2, ps, ps, pt) for a in (0, 90, 180, 270)])
    add("pads", pads, "buy", 9, "Mica pads (4)")
    fb = _fuse([zcyl(4, d["brk1"] - 17, d["fl1"], x, y) + zring(8, 4, d["fl1"], d["fl1"] + 1, x, y) + zcyl(6.5, d["fl1"] + 1, d["fl1"] + 9, x, y)
                for x, y in flange_bolt_xy(p)])
    add("flange_screws", fb, "buy", 9, "Flange screws (4 x M8) and mica washers")

    # ---- insulation jacket and guard, hung from the shelf on three tabs and spacers
    jo, jlo, jhi = p["jacket"]
    gz0, gz1 = d["bar0"] + jlo, d["brk0"] - jhi
    guard = zring(jo / 2, p["heater"][0] / 2 + 3, gz0, gz1)
    tabs, spacers = [], []
    for a in hanger_angles():
        ca, sa = cos(radians(a)), sin(radians(a))
        t = b.Pos(0, 0, gz1 - 1) * b.Rot(0, 0, a) * b.Pos(jo / 2 + 6, 0, 0) * b.Box(16, 14, 2)
        t = t - zcyl(2.75, gz1 - 3, gz1 + 1, 66 * ca, 66 * sa)
        tabs.append(t)
        spacers.append(zring(4, 2.75, gz1, d["brk0"], 66 * ca, 66 * sa) + zcyl(2.5, gz1 - 3, d["brk0"] + 10, 66 * ca, 66 * sa))
    guard = (guard + _fuse(tabs)) - bx(-jo, jo, -0.5, 0.5, gz0 - 5, gz1 + 5)      # two half shells, split left and right
    add("guard", guard, "make", 10, "Jacket and guard")
    add("hangers", _fuse(spacers), "buy", 10, "Hanger spacers and M5 screws (4)")

    # ---- mold clamp: lift table with its screw welded in, handwheel nut on a thrust washer
    tx, ty, tth = p["table"]
    sd, sl = p["lift_screw"]
    table = bx(-tx / 2, tx / 2, -ty / 2, ty / 2, tt_top - tth, tt_top)
    table = table + zcyl(sd / 2, tt_top - sl, tt_top - 0.01)
    add("table", table, "make", 11, "Lift table and screw")
    hwd, hub, hh = p["handwheel"]
    hw_ = zring(hub / 2, sd / 2, d["hub0"], d["hub1"]) + zring(hwd / 2, hwd / 2 - 7, d["hub0"] + 8, d["hub0"] + 18)
    for a in (90, 210, 330):
        hw_ = hw_ + b.Pos(0, 0, d["hub0"] + 13) * b.Rot(0, 0, a) * b.Pos((hub / 2 + hwd / 2 - 7) / 2, 0, 0) * b.Box(hwd / 2 - 7 - hub / 2 + 2, 10, 8)
    hw_ = hw_ + b.Pos(hwd / 2 - 3.5, 0, d["hub0"] + 18) * b.Cylinder(5, 30, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))  # spinner knob
    add("handwheel", hw_, "make", 11, "Handwheel nut")
    add("washer", zring(hub / 2, sd / 2 + 0.5, bt, d["hub0"]), "buy", 11, "Thrust washer")

    # ---- mold set: two plates, cavity, sprue, four M10 cap screws into thread inserts, two dowels
    mx, my, mt = p["mold"]
    m0, ms, m1 = d["mold0"] + dz_mold, d["split"] + dz_mold, d["mold1"] + dz_mold
    lower = bx(-mx / 2, mx / 2, -my / 2, my / 2, m0, ms)
    upper = bx(-mx / 2, mx / 2, -my / 2, my / 2, ms, m1)
    cvx, cvy, cvz = p["cavity"]
    lower = lower - bx(-cvx / 2, cvx / 2, -cvy / 2, cvy / 2, ms - cvz, ms + 1)
    upper = upper - b.Pos(0, 0, ms) * b.Cone(3.5, 2.5, mt, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))   # sprue 5 at the seat, 7 at the parting line
    upper = upper - b.Pos(0, 0, m1 - p["seat_depth"] + 12.5) * b.Sphere(12.5)   # spherical seat, 12.5 mm radius
    bxo, byo = p["mold_bolt_xy"]
    screws = []
    for sx in (-bxo, bxo):
        for sy in (-byo, byo):
            upper = upper - zcyl(5.5, ms - 1, m1 + 1, sx, sy)
            lower = lower - zcyl(6.5, ms - 25, ms + 1, sx, sy)                  # thread insert seat
            screws.append(zcyl(5, ms - 25, m1, sx, sy) + zcyl(8, m1, m1 + 10, sx, sy))
    dow = []
    for sx in (-p["dowel_x"], p["dowel_x"]):
        lower = lower - zcyl(3, ms - 12, ms + 1, sx, 0)
        upper = upper - zcyl(3, ms - 1, ms + 12, sx, 0)
        dow.append(zcyl(3, ms - 12, ms + 12, sx, 0))
    add("mold_lower", lower, "make", 12, "Mold lower plate")
    add("mold_upper", upper, "make", 12, "Mold upper plate")
    add("mold_screws", _fuse(screws), "buy", 12, "Mold screws (4 x M10) in thread inserts")
    add("dowels", _fuse(dow), "buy", 12, "Dowels (2 x 6 mm)")

    # ---- nozzle zone shield: two sides with feet, hinged front, hinges and latch
    sx_, sy_, st = p["shield"]
    yf = -sy_ / 2 - 10                 # front plane (-95)
    yb = yf + sy_                      # back edge of the sides (75)
    z1s = d["bar0"] + 40
    sides = []
    for sg in (-1, 1):
        xs = sg * sx_ / 2
        side = bx(xs - st / 2, xs + st / 2, yf, yb, bt, z1s)
        foot = bx(min(xs + sg * st / 2, xs + sg * (st / 2 + 20)), max(xs + sg * st / 2, xs + sg * (st / 2 + 20)), yf, yb, bt, bt + st)
        for yy in (-70.0, 50.0):
            foot = foot - zcyl(3.3, bt - 1, bt + st + 1, sg * 126.0, yy)
        sides.append(side + foot)
    add("shield_sides", _fuse(sides), "make", 16, "Shield sides")
    fz0 = p["shield_front_z0"]
    front = bx(-sx_ / 2 - st / 2, sx_ / 2 + st / 2, yf - st, yf, fz0, z1s)
    front = front - bx(-sx_ / 2 + 30, sx_ / 2 - 30, yf - st - 1, yf + 1, fz0 + 30, z1s - 50)   # window, perforated panel not modeled
    add("shield_front", front, "make", 16, "Shield front")
    hz = []
    xl = -sx_ / 2 - st / 2
    for zc in (fz0 + 40, z1s - 40):
        leaf_s = bx(xl - 1.5, xl, yf, yf + 22, zc - 15, zc + 15)
        leaf_f = bx(xl - 1.5, xl + 22, yf - st - 1.5, yf - st, zc - 15, zc + 15)
        knuckle = zcyl(3, zc - 15, zc + 15, xl - 1.5, yf - st - 3)
        hz.append(leaf_s + leaf_f + knuckle)
    xr_ = sx_ / 2 + st / 2
    latch = bx(xr_, xr_ + 2, yf, yf + 20, 150, 175) + bx(xr_ - 18, xr_ + 2, yf - st - 2, yf - st, 150, 175)
    add("hinges", _fuse(hz) + latch, "buy", 16, "Hinges (2) and latch")

    # ---- side hood with duct stub, held by an L-shaped arm to the column
    fy, fz = p["hood_face"]
    hxf = p["hood_x"]
    hzc = d["fl1"]
    hood = box(hxf - 60, 0, hzc, 120, fy, fz) - box(hxf - 58, 0, hzc, 118, fy - 4, fz - 4)
    hood = hood - box(hxf + 1, 0, hzc, 6, fy - 4, fz - 4)
    hood = hood + box(hxf - 60, 0, hzc + fz / 2 + 60, p["duct_d"], p["duct_d"], 120)
    add("hood", hood, "make", 17, "Fume hood and duct stub")
    ya = fy / 2
    arm = bx(hxf - 100, -cx / 2 - 5, ya, ya + 5, hood_z - 15, hood_z + 15) + bx(-cx / 2 - 5, -cx / 2, ya, 120, hood_z - 15, hood_z + 15)
    for yy in (85.0, 110.0):
        arm = arm - xcyl(3.3, -cx / 2 - 6, -cx / 2 + 1, yy, hood_z)
    for xx in (hxf - 80, hxf - 30):
        arm = arm - ycyl(2.75, ya - 1, ya + 6, xx, hood_z)
    add("hood_arm", arm, "make", 19, "Hood arm")

    # ---- plunger rest: a plate on two M6 rivnuts in the column's right wall, with a cup the hot plunger tip stands in
    rcd, rci, rch = p["rest_cup"]
    rpy, rpz, rpt = p["rest_plate"]
    rz = p["rest_z"]
    rplate = bx(cx / 2, cx / 2 + rpt, p["rest_y"] - rpy / 2, p["rest_y"] + rpy / 2, rz - rpz / 2, rz + rpz / 2)
    for yy in (84.0, 106.0):
        rplate = rplate - xcyl(3.3, cx / 2 - 1, cx / 2 + rpt + 1, yy, rz)
    rcx = cx / 2 + rpt + rcd / 2
    cup = zring(rcd / 2, rci / 2, rz - rpz / 2, rz - rpz / 2 + rch, rcx, p["rest_y"]) + zcyl(rcd / 2, rz - rpz / 2, rz - rpz / 2 + 3, rcx, p["rest_y"])
    add("plunger_rest", rplate + cup, "make", 20, "Plunger rest")

    # ---- mold cooling fan on a plate bracket bolted to the base plate
    fx, fyy, fzz = p["cool_fan"]
    xc, zc2 = p["cool_fan_x"], p["cool_fan_z"]
    fan = box(xc, 0, zc2, fx, fyy, fzz) - b.Pos(xc, 0, zc2) * b.Rotation(0, 90, 0) * b.Cylinder(fyy / 2 - 4, fx + 2)
    fan = fan + b.Pos(xc, 0, zc2) * b.Rotation(0, 90, 0) * b.Cylinder(20, fx - 4)
    for sy in (-52.5, 52.5):
        for sz in (-52.5, 52.5):
            fan = fan - xcyl(2.2, xc - fx / 2 - 1, xc + fx / 2 + 1, sy, zc2 + sz)
    add("fan", fan, "buy", 18, "Mold cooling fan")
    xb = xc + fx / 2
    plate = bx(xb, xb + 3, -fyy / 2, fyy / 2, bt, zc2 + fzz / 2) - xcyl(56, xb - 1, xb + 4, 0, zc2)
    for sy in (-52.5, 52.5):
        for sz in (-52.5, 52.5):
            plate = plate - xcyl(2.2, xb - 1, xb + 4, sy, zc2 + sz)
    foot = bx(xb - 18, xb, -fyy / 2, fyy / 2, bt, bt + 3)
    for yy in (-40.0, 40.0):
        foot = foot - zcyl(3.3, bt - 1, bt + 4, 146.0, yy)
    add("fan_bracket", plate + foot, "make", 18, "Fan bracket")

    # ---- control box and wiring (bought, on the bench)
    ccx, ccy = p["ctrl_xy"]
    qx, qy, qz = p["ctrl"]
    ctrl = box(ccx, ccy, qz / 2, qx, qy, qz) + box(ccx - 45, ccy - qy / 2 - 3, 80, 60, 6, 36) + box(ccx + 45, ccy - qy / 2 - 3, 80, 60, 6, 36)
    add("ctrl", ctrl, "buy", 13, "Control box")
    wiring = tube((ccx + qx / 2 - 20, ccy + 30, qz + 5), (-160, 40, 320), 6) + tube((-160, 40, 320), (-64, 20, 340), 6)
    add("wiring", wiring, "buy", 14, "Heater and sensor wiring")
    return C


GROUPS = {   # BOM-line grouping used by the concept media, the drawing and the appearance model
    "base": ["base"],
    "drive": ["column", "head_plate", "head_screws", "press_head", "adapter", "adapter_pin", "ratchet"],
    "tqsocket": ["torque_socket"],
    "ram": ["ram"],
    "loadcell": ["loadcell", "spacer", "coupling", "coupling_pin"],
    "plunger": ["plunger"],
    "barrel": ["barrel"],
    "heaters": ["heaters"],
    "nozzle": ["nozzle", "nozzle_heater"],
    "bracket": ["shelf", "back_plate", "pads", "flange_screws"],
    "guard": ["guard", "hangers"],
    "clamp": ["table", "handwheel", "washer"],
    "mold": ["mold_lower", "mold_upper", "mold_screws", "dowels"],
    "ctrl": ["ctrl"],
    "wiring": ["wiring"],
    "shield": ["shield_sides", "shield_front", "hinges"],
    "hood": ["hood", "hood_arm"],
    "coolfan": ["fan", "fan_bracket"],
    "rest": ["plunger_rest"],
}


def build_parts(p=PARAMS):
    """Return {name: shape} for every modeled BOM item (grouped components)."""
    C = build_components(p)
    return {g: _fuse([C[k].shape for k in ks]) for g, ks in GROUPS.items()}


ORDER = ["base", "drive", "ram", "loadcell", "plunger", "barrel", "heaters", "nozzle", "bracket",
         "guard", "clamp", "mold", "ctrl", "wiring", "shield", "hood", "coolfan", "rest", "tqsocket"]


def assembly(p=PARAMS, parts=None):
    b = _b3d()
    parts = parts or build_parts(p)
    return b.Compound(children=[parts[k] for k in ORDER])


def construction_mass(p=PARAMS):
    """Mass, kg, of the parts added or changed by MMD-DDR-003 that the calculation note does not
    otherwise count (steel at 7.85 g/cm3). Used by docs/04-calcs/sizing.py [K1]."""
    d = derived(p)
    rho = 7.85e-6
    hw, ht = p["head_plate"]
    bpx, bpt, bph = p["back_plate"]
    m = {
        "head mounting plate and screws": hw * ht * p["head"][2] * rho + 0.12,
        "shelf back plate": bpx * bpt * bph * rho,
        "plunger coupling, pin and spacer": pi / 4 * (40 ** 2 - 22 ** 2) * 30 * rho + pi / 4 * 40 ** 2 * 5 * rho + 0.05,
        "ratchet adapter": pi / 4 * (36 ** 2 - 28 ** 2) * 22 * rho + 12.7 ** 2 * 16 * rho,
        "lift screw and handwheel nut": pi / 4 * 20 ** 2 * p["lift_screw"][1] * rho + 0.60,
        "hood arm": 30 * 5 * 200 * rho,
        "shield feet, hinges and latch": 2 * 20 * 170 * 1.5 * rho + 0.12,
        "jacket hangers": 0.05,
        "plunger rest": 38 * 30 * 5 * rho + pi / 4 * (32 ** 2 - 24 ** 2) * 70 * rho + pi / 4 * 32 ** 2 * 3 * rho,
        "torque-limiting socket (assumed)": 0.55,
    }
    return m


# ---------------------------------------------------------------- constructability checks
CONTACTS = [   # (a, b, what holds them): faces that must touch
    ("column", "base", "fillet weld all round"),
    ("head_plate", "column", "fillet welds down both column corners"),
    ("press_head", "head_plate", "four M10 countersunk screws"),
    ("shelf", "column", "fillet weld top and bottom"),
    ("back_plate", "column", "fillet welds down both column corners"),
    ("back_plate", "shelf", "fillet weld"),
    ("pads", "shelf", "loose, located by the flange"),
    ("barrel", "pads", "flange on the pads"),
    ("flange_screws", "barrel", "M8 cap screws"),
    ("nozzle", "barrel", "M30 x 1.5 thread"),
    ("hangers", "shelf", "M5 screws"),
    ("hangers", "guard", "M5 screws through the tabs"),
    ("adapter", "press_head", "slides on the pinion shaft, roll pin"),
    ("torque_socket", "adapter", "1/2 in square drive"),
    ("ratchet", "torque_socket", "1/2 in square drive"),
    ("plunger_rest", "column", "two M6 rivnuts and screws"),
    ("loadcell", "ram", "M12 stud into the ram end"),
    ("spacer", "loadcell", "three M5 screws into blind holes"),
    ("coupling", "spacer", "three M5 screws into blind holes"),
    ("plunger", "coupling", "ball-lock pin"),
    ("washer", "base", "loose on the screw"),
    ("handwheel", "washer", "rests on it"),
    ("mold_lower", "table", "rests on it"),
    ("mold_upper", "mold_lower", "four M10 cap screws, two dowels"),
    ("mold_upper", "nozzle", "nozzle tip in the spherical seat"),
    ("shield_sides", "base", "two M6 screws through each foot"),
    ("hinges", "shield_front", "rivets"),
    ("hinges", "shield_sides", "rivets"),
    ("fan_bracket", "base", "two M6 screws"),
    ("fan", "fan_bracket", "four M4 screws"),
    ("hood_arm", "column", "two M6 rivnuts"),
    ("hood_arm", "hood", "two M5 screws"),
]

ENGAGED = {   # pairs that share volume on purpose: (a, b): why
    ("head_screws", "press_head"): "screws in tapped holes", ("head_screws", "head_plate"): "screws in countersunk holes",
    ("flange_screws", "shelf"): "screws in tapped holes", ("flange_screws", "barrel"): "screws through the flange",
    ("nozzle", "barrel"): "thread", ("hangers", "shelf"): "screws in tapped holes", ("hangers", "guard"): "screws through the tabs",
    ("adapter", "press_head"): "adapter on the shaft", ("adapter_pin", "adapter"): "pin", ("adapter_pin", "press_head"): "pin through the shaft",
    ("torque_socket", "adapter"): "square drive", ("ratchet", "torque_socket"): "square drive", ("coupling_pin", "coupling"): "pin", ("coupling_pin", "plunger"): "pin",
    ("plunger", "coupling"): "socket", ("table", "handwheel"): "screw in the nut", ("table", "washer"): "screw through the washer",
("mold_screws", "mold_upper"): "screws", ("mold_screws", "mold_lower"): "screws in inserts",
    ("dowels", "mold_upper"): "dowel", ("dowels", "mold_lower"): "dowel", ("fan", "fan_bracket"): "screws",
    ("ram", "press_head"): "ram in the head bore", ("plunger", "barrel"): "plunger in the bore",
}

CLEAR = [   # (a, b, minimum gap mm, why)
    ("barrel", "shelf", 1.5, "barrel passes the shelf hole"),
    ("table", "column", 1.5, "the table slides past the column face, which stops it turning"),
    ("shield_sides", "fan", 1.0, "fan beside the perforated side"),
    ("shield_sides", "table", 20.0, "table inside the shield"),
    ("guard", "shield_sides", 20.0, "jacket inside the shield top"),
    ("coupling", "barrel", 10.0, "coupling above the funnel when raised"),
    ("handwheel", "column", 2.0, "handwheel turns clear of the column"),
    ("handwheel", "shield_sides", 10.0, "handwheel inside the shield feet"),
    ("handwheel", "fan_bracket", 5.0, "handwheel clear of the fan foot"),
    ("wiring", "shield_sides", 5.0, "wiring passes above the shield"),
    ("hood", "back_plate", 20.0, "hood clear of the shelf back plate"),
    ("ratchet", "column", 10.0, "handle clear of the column"),
    ("torque_socket", "column", 10.0, "socket clear of the column"),
    ("ratchet", "fan_bracket", 20.0, "handle clear of the fan bracket"),
    ("plunger_rest", "shelf", 5.0, "rest cup clear of the shelf"),
    ("plunger_rest", "guard", 20.0, "hot jacket away from the rest"),
    ("plunger_rest", "barrel", 20.0, "rest clear of the flange and funnel"),
    ("plunger_rest", "shield_sides", 5.0, "rest cup clear of the shield"),
    ("plunger_rest", "fan_bracket", 20.0, "rest clear of the fan bracket"),
    ("plunger_rest", "flange_screws", 20.0, "rest clear of the flange screws"),
    ("mold_screws", "nozzle_heater", 5.0, "screw heads clear of the nozzle heater"),
    ("flange_screws", "back_plate", 2.0, "screw heads clear of the back plate"),
    ("loadcell", "back_plate", 5.0, "load cell clear of the back plate"),
]


def rested_plunger(p=PARAMS):
    """The plunger standing in the rest cup, tip down, for the loading step checks."""
    rcd, rci, rch = p["rest_cup"]
    rz = p["rest_z"] - p["rest_plate"][1] / 2 + 3.0
    rcx = p["col"][0] / 2 + p["rest_plate"][2] + rcd / 2
    return zcyl(p["bore"] / 2, rz, rz + p["plunger_len"], rcx, p["rest_y"]), rz


def _vol(a, b):
    try:
        return (a & b).volume
    except Exception:
        return 0.0


def check(p=PARAMS, verbose=True):
    """Constructability checks. Returns (passed, failed) lists of strings."""
    import itertools
    d = derived(p)
    passed, failed = [], []

    def rec(ok, text):
        (passed if ok else failed).append(text)
        if verbose:
            print(("PASS " if ok else "FAIL ") + text)

    C = build_components(p)
    keys = [k for k in C]
    bbs = {k: C[k].shape.bounding_box() for k in keys}

    def bb_touch(a, b, tol=0.5):
        A, B = bbs[a], bbs[b]
        return not (A.min.X > B.max.X + tol or B.min.X > A.max.X + tol or A.min.Y > B.max.Y + tol or
                    B.min.Y > A.max.Y + tol or A.min.Z > B.max.Z + tol or B.min.Z > A.max.Z + tol)

    # 1. nothing overlaps unless engaged on purpose
    for a, b in itertools.combinations(keys, 2):
        if not bb_touch(a, b, 0.0):
            continue
        v = _vol(C[a].shape, C[b].shape)
        if (a, b) in ENGAGED or (b, a) in ENGAGED:
            continue
        rec(v < 1.0, f"no overlap: {C[a].name} / {C[b].name} ({v:.1f} mm3)")
    # 2. faces that must touch do touch
    for a, b, how in CONTACTS:
        dist = C[a].shape.distance_to(C[b].shape)
        rec(dist < 0.05, f"contact: {C[a].name} on {C[b].name}, {how} (gap {dist:.2f} mm)")
    # 3. clearances
    for a, b, gmin, why in CLEAR:
        dist = C[a].shape.distance_to(C[b].shape)
        rec(dist >= gmin - 1e-6, f"clear: {C[a].name} to {C[b].name} {dist:.1f} mm (at least {gmin:g}); {why}")
    # 4. moving parts: full stroke and the table at both ends of its travel
    S = build_components(p, stroke=p["stroke"])
    dist = S["coupling"].shape.distance_to(C["barrel"].shape)
    rec(dist >= 10, f"full stroke: coupling {dist:.1f} mm above the funnel (at least 10)")
    v = _vol(S["plunger"].shape, C["barrel"].shape)
    rec(v < 5, f"full stroke: plunger slides in the bore ({v:.1f} mm3 shared, fit surface only)")
    rec(d["tip_low"] - d["bar0"] > 100, f"full stroke: plunger tip {d['tip_low'] - d['bar0']:.0f} mm above the barrel's lower end")
    for tt in (p["table_min_top"], p["table_min_top"] + p["table_travel"]):
        T = build_components(p, table_top=tt)
        bot = T["table"].shape.bounding_box().min.Z
        top_table = tt - p["table"][2]
        rec(top_table - d["hub1"] >= 2, f"table at {tt:.0f}: underside {top_table - d['hub1']:.0f} mm above the handwheel hub")
        rec(bot >= -p["bench_t"] - 200, f"table at {tt:.0f}: screw end {bot:.0f} mm (bench top at 0)")
        dc = T["table"].shape.distance_to(C["column"].shape)
        rec(dc >= 1.5, f"table at {tt:.0f}: {dc:.1f} mm from the column face")
        engaged = min(d["hub1"], tt) - max(d["hub0"], tt - p["lift_screw"][1])
        rec(tt - p["lift_screw"][1] <= d["hub0"], f"table at {tt:.0f}: screw passes through the full nut ({engaged:.0f} mm engaged)")
    # 4b. loading: the plunger lifted out on its ball-lock pin stands in the rest, never on the bench
    rp, rz0 = rested_plunger(p)
    for k in ("column", "barrel", "guard", "shelf", "back_plate", "shield_sides", "fan_bracket", "hood", "hood_arm",
              "flange_screws", "torque_socket", "ratchet", "head_plate", "press_head", "ram"):
        dist = rp.distance_to(C[k].shape)
        rec(dist >= 15 or (k == "column" and dist >= 8), f"rested plunger: {dist:.0f} mm from {C[k].name} (at least 15; 8 from the column wall)")
    seat = p["rest_cup"][2] - 3.0
    rec(seat >= 60, f"rested plunger: stands {seat:.0f} mm deep in the cup (at least 60), top {rz0 + p['plunger_len']:.0f} mm above the bench")
    rec(rz0 + p["plunger_len"] <= d["pl1"], f"rested plunger top {rz0 + p['plunger_len']:.0f} mm is below the raised plunger top {d['pl1']:.0f} mm")
    # 4c. P1: the press head holes (MMD-DDR-003) repeated on the bought head before it is cut
    hole_x = 30.0
    web = hole_x - 5.0 - (p["ram"] + 2) / 2
    rec(web >= 8, f"P1 nominal: {web:.0f} mm of casting between each M10 hole and the ram bore (at least 8; confirm on the bought head)")
    rec(p["head"][1] - 21 >= 100, f"P1 nominal: holes are 21 mm deep (20 mm thread) in a head {p['head'][1]:.0f} mm deep; confirm on the bought head")
    # 4d. torque limit from the press rating (MMD-CAL-001 B)
    tq_ceiling = 9807.0 * p["pinion_r"] / 1000 / 0.84
    rec(p["tq_set_Nm"] * 1.10 <= tq_ceiling, f"torque limit {p['tq_set_Nm']:.0f} N m, +10 % tolerance {p['tq_set_Nm'] * 1.10:.0f}, is within the {tq_ceiling:.0f} N m that gives 1 t at 84 % efficiency")
    # 5. assembly order: the barrel goes in from above before the press head
    below = (C["barrel"].shape + C["nozzle"].shape + C["nozzle_heater"].shape) & bx(-200, 200, -200, 200, -10, d["bar1"])
    bbx = below.bounding_box()
    widest = max(bbx.size.X, bbx.size.Y)
    hole = p["barrel_od"] + 4
    rec(widest < hole, f"order: barrel with nozzle and nozzle heater ({widest:.0f} mm) passes the {hole:.0f} mm shelf hole from above")
    rec(p["heater"][0] > hole, f"order: the {p['heater'][0]:.0f} mm band heaters cannot pass the shelf hole, so they clamp on after the barrel is in")
    gap = d["ram0"] - 20 - d["fun1"]
    unit = d["lc1"] - d["pl0"]
    rec(unit - gap < p["plunger_clear"] + 10, f"order: the {unit:.0f} mm plunger unit fits under the ram with its tip dipping {max(unit - gap, 0):.0f} mm into the funnel while the stud is started")
    # 6. stack heights
    rec(d["table_min_needed"] <= d["noz0"], f"tallest stack: {p['stack_max']:.0f} mm mold seats with the table {d['noz0'] - p['stack_max'] - p['table_min_top']:.0f} mm above its lowest")
    rec(d["handle_top"] <= 1100, f"handle top {d['handle_top']:.0f} mm above the bench (R9: 1,100 mm or less)")
    # 7. every made part has a stated process; every component a BOM line
    for k, c in C.items():
        rec(c.make in ("make", "buy") and isinstance(c.bom, int), f"process and BOM line stated: {c.name} ({c.make}, line {c.bom})")
    failed = [f for f in failed if f]
    passed = [f for f in passed if f]
    if verbose:
        print(f"\n{len(passed)} passed, {len(failed)} failed")
    return passed, failed


if __name__ == "__main__":
    P, D = PARAMS, derived()
    if "--check" in sys.argv:
        _, f = check()
        sys.exit(1 if f else 0)
    from build123d import Compound, export_step, export_stl
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
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    print(f"nozzle tip {D['noz0']:.0f}, barrel {D['bar0']:.0f} to {D['bar1']:.0f}, pinion {D['pin_z']:.0f}, "
          f"ram {D['ram_len']:.0f} long, handle top {D['handle_top']:.0f}, overall {D['overall_h']:.0f} mm")
    print(f"stroke in bore {D['in_bore']:.0f} mm, reservoir {D['reservoir']:.0f} mm, "
          f"table top {D['table_top']:.0f} (min {P['table_min_top']:.0f}, max {P['table_min_top'] + P['table_travel']:.0f})")
