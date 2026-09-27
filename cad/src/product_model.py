"""MicroMold product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders of the bench-top injection press: a filleted,
painted base plate with bench bolts; the steel column with an end cap; the arbor press head with
pinion bosses, gib screws and a name badge; the rack ram with its teeth; the ratchet handle with a
rubber grip and ball knob; the load cell on its glass-epoxy spacer, with a label and lead; the
ground plunger; the barrel, flange and funnel; the two mica band heaters with clamp lugs and
terminal blocks; the nozzle with its radiused tip and heater band; the aluminum-skinned jacket
inside a slotted guard; the two-plate aluminum test mold with a visible parting line, pry slots,
washers, hex bolts and nuts; the screw jack, guide rods, slotted lift table and tommy bar; the
perforated nozzle zone shield with hinges, latch and a hot-surface label; the side fume hood,
duct stub, band clamp and a short run of flexible duct; the mold cooling fan with blades, finger
guard and bracket; and the control box with two lit PID controllers, a lit force display, a lit
rocker switch, a cut-out reset button, a name plate, vents and glands. Heater wiring is in
glass-fiber sleeving. Accessories are a tray of recycled flake and three molded test plaques.
Context is a compact section of workbench top.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS, derived() and build_parts() in model.py.
Axes as model.py: Z up, bench top at Z = 0, the operator on the -Y side, injection axis at
X = 0, Y = 0. Shown with the plunger raised and the test mold seated on the nozzle.
Appearance-only departures from model.py are listed in docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import random
import sys
from math import cos, radians, sin
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cone, Cylinder, Plane, Polygon, Pos, RegularPolygon, Rot, Solid,
                       Sphere, Vector, extrude, fillet)
from model import PARAMS, build_parts, derived

TITLE = "MicroMold: desktop injection molding press for recycled plastic"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False,
     "el": 28, "az": -40,
     "note": "Product render from the front right and above (about 28 deg elevation); ratchet handle "
             "raised toward the viewer, heated barrel in its slotted guard, test mold behind the "
             "perforated shield, control box with lit controllers at left, flake and molded plaques "
             "on the bench"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): base plate, "
             "column and drive head, ram, load cell and plunger, barrel, band heaters, jacket and "
             "guard, nozzle, mold halves and bolts, lift table, shield, fume hood, cooling fan and "
             "control box"},
]

# Colours (restrained product palette; kit accent)
C_FRAME = "#2F343B"      # painted column and head
C_BASE = "#3A4048"       # painted base plate
C_ACCENT = "#0F766E"
C_STEEL = "#A9AFB6"
C_BRIGHT = "#C9CED3"     # ground or plated steel
C_ALU = "#CDD2D7"
C_SKIN = "#D9DDE1"       # jacket aluminum skin
C_GUARD = "#8E959D"      # perforated steel guard
C_SHIELD = "#B4BAC0"     # zinc-plated perforated sheet
C_BLACK = "#1C1F24"
C_DARK = "#2B2F36"
C_BARREL = "#6F6A66"     # heat-tinted steel barrel
C_HEATER = "#B8BCC0"
C_CERAMIC = "#EDEBE4"
C_G11 = "#B7B27C"
C_BRASS = "#C9A227"
C_BOX = "#E6E7E9"        # control box powder coat
C_LABEL = "#F4F4F2"
C_WARN = "#F2C230"
C_RED_LIT = "#FF4B3A"
C_GRN_LIT = "#4ADE80"
C_AMB_LIT = "#FFB020"
C_GLASS = "#0E1216"
C_SLEEVE = "#E7E1CF"     # glass-fiber sleeving
C_WOOD = "#D8C6A5"


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _zring(x, y, z0, z1, ro, ri):
    return _zcyl(x, y, (z0 + z1) / 2, ro, z1 - z0) - _zcyl(x, y, (z0 + z1) / 2, ri, z1 - z0 + 2)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _hex_z(x, y, z0, af, h):
    return Pos(x, y, z0) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x0, y, z, af, length):
    return Pos(x0, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _front(s):
    return s.faces().sort_by(Axis.Y)[0].edges()


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd",
       "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}


def _digits(text, x0, y, zc, h, t=None, proud=0.3):
    """Seven-segment readout facing -Y: thin raised bars, left edge x0, centre height zc."""
    t = t or h * 0.14
    w = h * 0.55
    gap = h * 0.28
    bars = []
    x = x0
    for ch in text:
        if ch == ".":
            bars.append(_box(x - gap * 0.5, y, zc - h / 2 + t / 2, t, proud, t))
            continue
        cx = x + w / 2
        hz = h / 2 - t / 2
        seg = {"a": (cx, zc + hz, w - t, t), "g": (cx, zc, w - t, t), "d": (cx, zc - hz, w - t, t),
               "f": (x + t / 2, zc + h / 4, t, h / 2 - t), "b": (x + w - t / 2, zc + h / 4, t, h / 2 - t),
               "e": (x + t / 2, zc - h / 4, t, h / 2 - t), "c": (x + w - t / 2, zc - h / 4, t, h / 2 - t)}
        for s in SEG[ch]:
            sx, sz, lx, lz = seg[s]
            bars.append(_box(sx, y, sz, lx * 0.92, proud, lz * 0.92))
        x += w + gap
    return _union(bars)


def _plate_holes(plate, centers, size, axis):
    """Cut square perforations of `size` through a thin plate normal to `axis` ('x' or 'y')."""
    tools = []
    for (a, b, c) in centers:
        if axis == "x":
            tools.append(_box(a, b, c, 10, size, size))
        else:
            tools.append(_box(a, b, c, size, 10, size))
    return plate.cut(*tools)


# ---------------------------------------------------------------- model
def product_parts(P=PARAMS):
    D = derived(P)
    m = build_parts(P)
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    bx, by, bt = P["base"]
    base_y = P["base_y"]

    # ------------------------------------------------------------ explode offsets
    E_BASE = (0, 0, -170)
    E_FRAME = (0, 240, 60)
    E_RAM = (0, 0, 330)
    E_CELL = (0, 0, 230)
    E_PLUNGER = (0, 0, 150)
    E_BARREL = (0, 0, 70)
    E_HEAT = (330, 0, 70)
    E_JACKET = (0, -260, 90)
    E_NOZZLE = (0, 0, 25)
    E_MOLD_UP = (0, -40, -20)
    E_MOLD_LO = (0, -40, -70)
    E_BOLTS = (0, -40, 140)
    E_CLAMP = (0, 0, -120)
    E_SHIELD = (0, -300, -60)
    E_HOOD = (-160, 0, 160)
    E_FAN = (200, 0, 0)
    E_CTRL = (-140, -60, 0)
    E_WIRE = (-70, -60, 0)

    # ------------------------------------------------------------ 1 base plate
    base = _box(0, base_y, bt / 2, bx, by, bt)
    base = _fillet_try(base, _edges_par(base, Axis.Z), [12.0, 8.0, 5.0])
    base = _fillet_try(base, _top(base), [2.0, 1.2])
    add("Base plate (painted steel)", base, C_BASE, "painted", 1, "shell", E_BASE)
    bolts = []
    for (x, y) in [(-140, -90), (140, -90), (-140, 130), (140, 130)]:
        w = _zcyl(x, y, bt + 0.8, 11.0, 1.6)
        h = _hex_z(x, y, bt + 1.6, 17.0, 6.5)
        h = _fillet_try(h, _top(h), [1.0, 0.6])
        bolts.append(w + h)
    add("Bench bolts and washers", _union(bolts), C_BRIGHT, "metal", 15, "shell", E_BASE)

    # ------------------------------------------------------------ 2 column and drive head
    cx, cy, cw = P["col"]
    col_y = P["col_y"]
    zc0, zc1 = bt, D["head1"]
    col_o = _box(0, col_y, (zc0 + zc1) / 2, cx, cy, zc1 - zc0)
    col_o = _fillet_try(col_o, _edges_par(col_o, Axis.Z), [6.0, 4.0])
    col_i = _box(0, col_y, (zc0 + zc1) / 2, cx - 2 * cw, cy - 2 * cw, zc1 - zc0 + 2)
    col_i = _fillet_try(col_i, _edges_par(col_i, Axis.Z), [3.0, 2.0])
    column = col_o - col_i
    add("Column (painted steel tube)", column, C_FRAME, "painted", 2, "shell", E_FRAME)
    cap = _box(0, col_y, zc1 + 2.5, cx - 2, cy - 2, 5.0)
    cap = _fillet_try(cap, _edges_par(cap, Axis.Z), [5.0, 3.0])
    cap = _fillet_try(cap, _top(cap), [1.5, 1.0])
    add("Column end cap", cap, C_BLACK, "plastic", 2, "shell", E_FRAME)

    hx, hy, hz = P["head"]
    head_y = P["head_y"]
    h0, h1 = D["head0"], D["head1"]
    head = _box(0, head_y, (h0 + h1) / 2, hx, hy, hz)
    head = _fillet_try(head, _edges_par(head, Axis.Z), [12.0, 8.0, 5.0])
    head = _fillet_try(head, _top(head), [4.0, 2.5])
    py, pz = P["pinion_y"], D["pin_z"]
    head += _xcyl(0, py, pz, 34.0, hx + 16)                    # pinion bosses, 8 mm each side
    head -= _box(0, 0, (h0 + h1) / 2, P["ram"] + 2, P["ram"] + 2, hz + 40)
    add("Arbor press head (painted casting)", head, C_FRAME, "painted", 2, "shell", E_FRAME)
    gib = []
    for z in (h0 + 30, h1 - 30):
        for sx in (-1, 1):
            n = Pos(sx * 26, head_y - hy / 2, z) * Rot(90, 0, 0) * extrude(RegularPolygon(13 / 1.732, 6), amount=6)
            s = _ycyl(sx * 26, head_y - hy / 2 - 9, z, 4.0, 6)
            gib.append(n + s)
    add("Gib screws and lock nuts", _union(gib), C_BRIGHT, "metal", 2, "shell", E_FRAME)
    badge = _box(0, head_y - hy / 2 - 0.2, pz - 10, 64, 0.4, 16)
    badge = _fillet_try(badge, _edges_par(badge, Axis.Y), [2.0, 1.0])
    add("Head name badge", badge, C_ACCENT, "painted", 2, "shell", E_FRAME)
    badge_ink = _box(-12, head_y - hy / 2 - 0.5, pz - 7, 30, 0.3, 3) + _box(-17, head_y - hy / 2 - 0.5, pz - 13, 20, 0.3, 2) \
        + Pos(20, head_y - hy / 2 - 0.5, pz - 10) * Rot(90, 0, 0) * Cylinder(5, 0.3)
    add("Badge print", badge_ink, C_LABEL, "paper", 2, "shell", E_FRAME)

    shaft = _xcyl(0, py, pz, 14.0, 155.0)                       # x -75 .. 80, as model.py
    shaft = Pos(2.5, 0, 0) * shaft
    shaft += _hex_x(-hx / 2 - 8 - 7, py, pz, 30.0, 7.0)        # retaining nut, left
    add("Pinion shaft and nut", shaft, C_STEEL, "metal", 2, "shell", E_FRAME)

    hxp = hx / 2 + 25
    ky, kz = D["knob"]
    ratchet = _xcyl(hxp + 10, py, pz, 20.0, 20.0)
    ratchet = _fillet_try(ratchet, ratchet.edges(), [3.0, 2.0])
    ratchet += _box(hxp + 21, py + 6, pz + 16, 3, 8, 10)       # reversing lever
    A = Vector(hxp + 10, py, pz)
    K = Vector(hxp + 10, py + ky, kz)
    u = (K - A).normalized()
    L = (K - A).length
    arm = Solid.make_cylinder(11.0, L - 10, Plane(origin=A, z_dir=u))
    add("Ratchet head and handle", ratchet + arm, C_BRIGHT, "metal", 2, "shell", E_FRAME)
    g0 = A + u * (L - 24 - 135)
    grip = Solid.make_cylinder(14.5, 135.0, Plane(origin=g0, z_dir=u))
    grip = _fillet_try(grip, grip.edges(), [3.0, 2.0])
    rings = [Solid.make_cylinder(15.3, 3.0, Plane(origin=g0 + u * (14 + 14 * k), z_dir=u)) for k in range(8)]
    add("Handle grip (rubber)", grip + _union(rings), C_ACCENT, "rubber", 2, "shell", E_FRAME)
    knob = Pos(*K) * Sphere(P["knob_r"])
    add("Handle ball knob", knob, C_BLACK, "plastic", 2, "shell", E_FRAME)

    # ------------------------------------------------------------ 3 rack ram
    r = P["ram"]
    ram = _box(0, 0, (D["ram0"] + D["ram1"]) / 2, r, r, D["ram_len"])
    ram = _fillet_try(ram, _top(ram), [2.0, 1.0])
    teeth = [_box(0, r / 2, z, r - 6, 4.0, 3.2) for z in [D["ram0"] + 30 + 6.28 * k for k in range(34)]]
    ram = ram.cut(*teeth)
    add("Rack ram", ram, C_STEEL, "metal", 3, "shell", E_RAM)

    # ------------------------------------------------------------ 4 load cell and spacer
    lr, lh = P["loadcell"]
    cell = _zcyl(0, 0, (D["sp1"] + D["lc1"]) / 2, lr / 2, lh)
    cell = _fillet_try(cell, cell.edges(), [2.0, 1.0])
    cell -= _zring(0, 0, D["lc1"] - 6, D["lc1"] - 4, lr / 2 + 1, lr / 2 - 1.0)     # seam groove
    add("Plunger load cell", cell, C_BRIGHT, "metal", 4, "internal", E_CELL)
    clab = _zcyl(0, 0, (D["sp1"] + D["lc1"]) / 2 - 3, lr / 2 + 0.3, 12) - _zcyl(0, 0, (D["sp1"] + D["lc1"]) / 2 - 3, lr / 2 - 0.5, 14)
    clab &= _box(0, -lr / 2, (D["sp1"] + D["lc1"]) / 2, 30, lr, 20)
    add("Load cell label", clab, C_LABEL, "paper", 4, "internal", E_CELL)
    spacer = _zcyl(0, 0, (D["pl1"] + D["sp1"]) / 2, P["bore"] / 2 + 4, P["spacer_t"])
    add("Glass-epoxy thermal spacer", spacer, C_G11, "plastic", 4, "internal", E_CELL)
    cz = (D["sp1"] + D["lc1"]) / 2
    lead = _xcyl(-lr / 2 - 5, 0, cz, 4.0, 12) + _pipe([(-lr / 2 - 10, 0, cz), (-62, 12, cz - 6), (-62, 100, cz - 60),
                                                       (-62, 100, 150), (-150, 70, 90), (-229, 40, 60)], 2.6)
    add("Load cell lead", lead, C_BLACK, "plastic", 4, "shell", E_CELL)

    # ------------------------------------------------------------ 5 plunger
    pl = _zcyl(0, 0, (D["pl0"] + D["pl1"]) / 2, P["bore"] / 2, P["plunger_len"])
    pl = _fillet_try(pl, _bottom(pl), [1.5, 1.0])
    pl -= _xcyl(0, 0, D["pl1"] - 12, 3.0, P["bore"] + 2)                        # coupling cross hole
    add("Plunger (ground steel)", pl, C_BRIGHT, "metal", 5, "internal", E_PLUNGER)

    # ------------------------------------------------------------ 6 barrel, flange and funnel
    barrel = m["barrel"]
    add("Heated barrel, flange and funnel", barrel, C_BARREL, "metal", 6, "internal", E_BARREL)

    # ------------------------------------------------------------ 7 band heaters
    ho, hw = P["heater"]
    heaters = []
    lugs = []
    terms = []
    for zc in P["heater_z"]:
        band = _zring(0, 0, zc - hw / 2, zc + hw / 2, ho / 2, P["barrel_od"] / 2)
        band -= _zring(0, 0, zc - hw / 2 + 4, zc - hw / 2 + 5, ho / 2 + 1, ho / 2 - 0.6)
        band -= _zring(0, 0, zc + hw / 2 - 5, zc + hw / 2 - 4, ho / 2 + 1, ho / 2 - 0.6)
        heaters.append(band)
        lug = _box(-6, ho / 2 + 5, zc, 4, 12, hw - 10) + _box(6, ho / 2 + 5, zc, 4, 12, hw - 10)
        lug += _xcyl(0, ho / 2 + 7, zc, 3.0, 24) + _hex_x(10, ho / 2 + 7, zc, 10, 5)
        lugs.append(lug)
        tb = _box(-ho / 2 - 6, 0, zc, 12, 18, 22)
        tb = _fillet_try(tb, tb.edges(), [1.5, 1.0])
        tb += _xcyl(-ho / 2 - 13, -5, zc, 2.2, 4) + _xcyl(-ho / 2 - 13, 5, zc, 2.2, 4)
        terms.append(tb)
    add("Band heaters, 2 x 300 W", _union(heaters), C_HEATER, "metal", 7, "internal", E_HEAT)
    add("Heater clamp lugs and screws", _union(lugs), C_STEEL, "metal", 7, "internal", E_HEAT)
    add("Heater terminal blocks", _union(terms), C_CERAMIC, "plastic", 7, "internal", E_HEAT)

    # ------------------------------------------------------------ 8 nozzle and nozzle heater
    n0, n1 = D["noz0"], D["noz1"]
    ro = P["nozzle_orifice"] / 2
    noz = _zcyl(0, 0, (n0 + 8 + n1) / 2, 12.0, n1 - n0 - 8)
    tip = Pos(0, 0, n0 + 4) * Cone(6.5, 12.0, 8.0)
    noz = noz + tip
    noz = _fillet_try(noz, _bottom(noz), [2.0, 1.2, 0.8])
    noz -= _zcyl(0, 0, (n0 + n1) / 2, ro, n1 - n0 + 2)
    add("Nozzle, 4 mm orifice", noz, C_STEEL, "metal", 8, "internal", E_NOZZLE)
    nh = _zring(0, 0, n0 + 8, n1 - 4, 20.0, 12.0)
    nh += _box(0, 23, (n0 + n1) / 2 + 2, 10, 8, 20) + _xcyl(0, 25, (n0 + n1) / 2 + 2, 2.2, 18)
    add("Nozzle heater band, 100 W", nh, C_HEATER, "metal", 8, "internal", E_NOZZLE)

    # ------------------------------------------------------------ 9 barrel bracket
    kx, ky_, kt = P["bracket"]
    brk_y = D["col_front"] + cw - ky_ / 2
    brk = _box(0, brk_y, (D["brk0"] + D["brk1"]) / 2, kx, ky_, kt)
    brk = _fillet_try(brk, _edges_par(brk, Axis.Z), [10.0, 6.0])
    brk = _fillet_try(brk, _top(brk), [1.5, 1.0])
    brk -= _zcyl(0, 0, (D["brk0"] + D["brk1"]) / 2, P["barrel_od"] / 2 + 2, kt + 2)
    add("Barrel bracket (heat break plate)", brk, C_ACCENT, "painted", 9, "shell", E_FRAME)

    # ------------------------------------------------------------ 10 insulation jacket and guard
    jo, jlo, jhi = P["jacket"]
    j0, j1 = D["bar0"] + jlo, D["brk0"] - jhi
    skin = _zring(0, 0, j0, j1, jo / 2 - 2.0, P["heater"][0] / 2 + 3)
    add("Insulation jacket (aluminum skin)", skin, C_SKIN, "metal", 10, "shell", E_JACKET)
    guard = _zring(0, 0, j0, j1, jo / 2, jo / 2 - 1.5)
    slots = []
    nband = 4
    bh = (j1 - j0 - 16) / nband
    for b in range(nband):
        zc = j0 + 8 + bh * (b + 0.5)
        for k in range(28):
            a = 360.0 / 28 * (k + 0.5 * (b % 2))
            slots.append(Rot(0, 0, a) * _box(jo / 2 - 0.5, 0, zc, 6, 5.0, bh - 9))
    guard = guard.cut(*slots)
    add("Perforated steel guard", guard, C_GUARD, "metal", 10, "shell", E_JACKET)

    # ------------------------------------------------------------ 11 mold clamp: jack, rods, table, tommy bar
    tx, ty, tt = P["table"]
    t_top = D["table_top"]
    jack = _box(0, 0, bt + 25, 70, 70, 50)
    jack = _fillet_try(jack, _edges_par(jack, Axis.Z), [8.0, 5.0])
    jack = _fillet_try(jack, _top(jack), [3.0, 2.0])
    jack += _zcyl(0, 0, (bt + 50 + t_top - tt) / 2, 20.0, t_top - tt - bt - 50 + 0.5)
    jack += _ycyl(0, -35 - 6, bt + 22, 14.0, 12)                  # input shaft boss on the front face
    add("Screw jack", jack, C_FRAME, "painted", 11, "shell", E_CLAMP)
    rods = _zcyl(-62, 0, (bt + t_top - tt) / 2, 7.0, t_top - tt - bt) + _zcyl(62, 0, (bt + t_top - tt) / 2, 7.0, t_top - tt - bt)
    rods += _zring(-62, 0, bt, bt + 8, 12, 6.9) + _zring(62, 0, bt, bt + 8, 12, 6.9)
    add("Guide rods and bushes", rods, C_BRIGHT, "metal", 11, "shell", E_CLAMP)
    table = _box(0, 0, t_top - tt / 2, tx, ty, tt)
    table = _fillet_try(table, _edges_par(table, Axis.Z), [6.0, 4.0])
    table = _fillet_try(table, _top(table), [1.2, 0.8])
    bxo, byo = P["mold_bolt_xy"]
    table = table.cut(_box(-bxo, 0, t_top - tt / 2, 17, 2 * byo + 24, tt + 2), _box(bxo, 0, t_top - tt / 2, 17, 2 * byo + 24, tt + 2))
    add("Lift table", table, C_ACCENT, "painted", 11, "shell", E_CLAMP)
    bar = _pipe([(0, -35, bt + 22), (0, -150, bt + 22)], 8.0)
    bar += _xcyl(0, -150, bt + 22, 7.0, 90.0) + _ycyl(0, -150, bt + 22, 11.0, 18.0)
    add("Tommy bar", bar, C_BRIGHT, "metal", 11, "shell", E_CLAMP)
    tgrips = _xcyl(-38, -150, bt + 22, 9.0, 24) + _xcyl(38, -150, bt + 22, 9.0, 24)
    tgrips = _fillet_try(tgrips, tgrips.edges(), [2.5, 1.5])
    add("Tommy bar grips", tgrips, C_BLACK, "rubber", 11, "shell", E_CLAMP)

    # ------------------------------------------------------------ 12 mold set
    mx, my, mt = P["mold"]
    cvx, cvy, cvz = P["cavity"]
    m0, ms, m1 = D["mold0"], D["split"], D["mold1"]

    def plate(z0, z1):
        p = _box(0, 0, (z0 + z1) / 2, mx, my, z1 - z0)
        p = _fillet_try(p, _edges_par(p, Axis.Z), [3.0, 2.0])
        p = _fillet_try(p, _top(p) + _bottom(p), [1.2, 0.8])
        for sx in (-bxo, bxo):
            for sy in (-byo, byo):
                p -= _zcyl(sx, sy, (z0 + z1) / 2, 5.5, z1 - z0 + 2)
        return p

    lower = plate(m0 + 0.25, ms - 0.25)
    lower -= _box(0, 0, ms - cvz / 2, cvx, cvy, cvz + 0.5)
    lower = lower.cut(_box(-mx / 2 + 16, -my / 2, ms - 2, 18, 6, 4.5), _box(mx / 2 - 16, -my / 2, ms - 2, 18, 6, 4.5))
    add("Mold lower half (aluminum)", lower, C_ALU, "metal", 12, "shell", E_MOLD_LO)
    upper = plate(ms + 0.25, m1 - 0.25)
    upper -= _zcyl(0, 0, (ms + m1) / 2, 3.0, m1 - ms + 2)
    upper -= _zcyl(0, 0, m1 - 1.5, 7.0, 3.2)                  # sprue bushing seat
    upper = upper.cut(_box(-mx / 2 + 16, -my / 2, ms + 2, 18, 6, 4.5), _box(mx / 2 - 16, -my / 2, ms + 2, 18, 6, 4.5))
    add("Mold upper half (aluminum)", upper, C_ALU, "metal", 12, "shell", E_MOLD_UP)
    stamp = _box(-24, -my / 2 - 0.15, ms + 26, 40, 0.3, 5) + _box(-30, -my / 2 - 0.15, ms + 18, 28, 0.3, 3)
    add("Mold stamp", stamp, "#5B6168", "paper", 12, "shell", E_MOLD_UP)
    mb = []
    for sx in (-bxo, bxo):
        for sy in (-byo, byo):
            w = _zcyl(sx, sy, m1 - 0.25 + 0.8, 10.0, 1.6)
            h = _hex_z(sx, sy, m1 + 1.35, 16.0, 5.9)
            h = _fillet_try(h, _top(h), [1.0, 0.6])
            shank = _zcyl(sx, sy, (m0 - tt + 1 + m1) / 2, 5.0, m1 - m0 + tt - 1)
            nut = _hex_z(sx, sy, m0 - tt + 0.5, 16.0, 8.0)
            mb.append(w + h + shank + nut)
    add("Mold bolts, washers and nuts (M10)", _union(mb), "#3E4349", "metal", 12, "shell", E_BOLTS)

    # ------------------------------------------------------------ 13 control box
    ccx, ccy = P["ctrl_xy"]
    qx, qy, qz = P["ctrl"]
    fy = ccy - qy / 2
    box_o = _box(ccx, ccy, qz / 2, qx, qy, qz)
    box_o = _fillet_try(box_o, _edges_par(box_o, Axis.Y), [8.0, 6.0, 4.0])
    box_o = _fillet_try(box_o, _top(box_o), [3.0, 2.0])
    body = box_o.cut(*[_box(ccx + sx * qx / 2, ccy + dy, 50, 2.0, 5.0, 40) for sx in (-1, 1) for dy in range(-40, 41, 12)])
    seam = _box(ccx, ccy, qz - 10, qx + 2, qy + 2, 0.8) - _box(ccx, ccy, qz - 10, qx - 3, qy - 3, 2)
    body -= seam
    add("Control box enclosure", body, C_BOX, "painted", 13, "shell", E_CTRL)
    EP = E_CTRL
    for k, xo in enumerate((-45, 45)):
        xc = ccx + xo
        bez = _box(xc, fy - 3, 80, 60, 6, 36)
        bez = _fillet_try(bez, _edges_par(bez, Axis.Y), [2.0, 1.0])
        bez = _fillet_try(bez, _front(bez), [0.8, 0.5])
        add(f"PID controller {k + 1} bezel", bez, C_BLACK, "plastic", 13, "shell", EP)
        glass = _box(xc - 5, fy - 6.2, 81, 42, 0.4, 28)
        add(f"PID controller {k + 1} display", glass, C_GLASS, "screen", 13, "shell", EP)
        pv = _digits("210" if k == 0 else "225", xc - 23, fy - 6.5, 88, 10.0)
        add(f"PID controller {k + 1} process value (lit)", pv, C_RED_LIT, "emissive", 13, "shell", EP)
        sv = _digits("210" if k == 0 else "225", xc - 17, fy - 6.5, 74, 6.5)
        add(f"PID controller {k + 1} set value (lit)", sv, C_GRN_LIT, "emissive", 13, "shell", EP)
        keys = _union([_ycyl(xc + 22, fy - 6.5, 80 + dz, 2.6, 1.2) for dz in (-9, 0, 9)])
        add(f"PID controller {k + 1} keys", keys, "#4B5057", "rubber", 13, "shell", EP)
    # force display (load cell readout), rocker switch, cut-out reset, name plate
    fd = _box(ccx, fy - 2, 34, 56, 4, 24)
    fd = _fillet_try(fd, _edges_par(fd, Axis.Y), [2.0, 1.0])
    add("Force display bezel", fd, C_BLACK, "plastic", 4, "shell", EP)
    add("Force display glass", _box(ccx, fy - 4.2, 34, 46, 0.4, 16), C_GLASS, "screen", 4, "shell", EP)
    add("Force display readout (lit)", _digits("0.00", ccx - 17, fy - 4.5, 34, 10.0), C_RED_LIT, "emissive", 4, "shell", EP)
    rk = _box(ccx - 70, fy - 2, 34, 22, 4, 30)
    rk = _fillet_try(rk, _edges_par(rk, Axis.Y), [2.5, 1.5])
    add("Mains switch bezel", rk, C_BLACK, "plastic", 13, "shell", EP)
    rocker = Pos(ccx - 70, fy - 4, 34) * Rot(8, 0, 0) * Box(16, 4, 24)
    rocker = _fillet_try(rocker, _edges_par(rocker, Axis.Y), [1.5, 1.0])
    add("Mains switch rocker (lit)", rocker, C_AMB_LIT, "emissive", 13, "shell", EP)
    rs = _ycyl(ccx + 70, fy - 2, 34, 11.0, 4)
    rs = _fillet_try(rs, _front(rs), [1.0, 0.6])
    add("Thermal cut-out reset bezel", rs, C_BLACK, "plastic", 13, "shell", EP)
    rb = _ycyl(ccx + 70, fy - 6, 34, 7.0, 5)
    rb = _fillet_try(rb, _front(rb), [2.0, 1.2])
    add("Thermal cut-out reset button", rb, "#B42318", "plastic", 13, "shell", EP)
    npl = _box(ccx, fy - 0.2, 104, 110, 0.4, 7)
    add("Control box name plate", npl, C_ACCENT, "painted", 13, "shell", EP)
    # side glands (wiring and load cell lead), rear inlet and outlet
    gl = _union([_hex_x(ccx + qx / 2, ccy + 30, 100, 20, 5) + _xcyl(ccx + qx / 2 + 9, ccy + 30, 100, 8.5, 8),
                 _hex_x(ccx + qx / 2, ccy + 50, 60, 14, 4) + _xcyl(ccx + qx / 2 + 6, ccy + 50, 60, 5.5, 5)])
    add("Control box cable glands", gl, C_DARK, "plastic", 13, "shell", EP)
    iec = _box(ccx + 50, ccy + qy / 2 + 1.5, 60, 32, 3, 26) - _box(ccx + 50, ccy + qy / 2 + 2, 60, 24, 3, 16)
    iec += _box(ccx - 40, ccy + qy / 2 + 1.5, 60, 40, 3, 40)
    add("Fused IEC inlet and fan outlet", iec, C_BLACK, "plastic", 13, "shell", EP)

    # ------------------------------------------------------------ 14 wiring in glass-fiber sleeving
    harness = _pipe([(ccx + qx / 2 + 12, ccy + 30, 100), (-170, 55, 120), (-120, 60, 240), (-66, 30, 330)], 6.0)
    add("Heater and sensor wiring (glass-fiber sleeving)", harness, C_SLEEVE, "fabric", 14, "shell", E_WIRE)

    # ------------------------------------------------------------ 16 nozzle zone shield
    sx_, sy_, st = P["shield"]
    z0s, z1s = bt + 40, D["bar0"] + 40
    zc, zh = (z0s + z1s) / 2, z1s - z0s
    yf = -sy_ / 2 - 10
    sides = []
    for sgn in (-1, 1):
        s = _box(sgn * sx_ / 2, yf + sy_ / 2, zc, st, sy_, zh)
        cen = [(sgn * sx_ / 2, yf + 20 + 12 * i, z0s + 22 + 12 * j) for i in range(12) for j in range(15)]
        sides.append(_plate_holes(s, cen, 8.5, "x"))
    wx0, wz0, wz1 = sx_ / 2 - 30, zc - 10 - (zh - 80) / 2, zc - 10 + (zh - 80) / 2
    front = _box(0, yf, zc, sx_, st, zh) - _box(0, yf, zc - 10, sx_ - 60, st + 2, zh - 80)
    add("Nozzle zone shield sides", _union(sides), C_SHIELD, "metal", 16, "shell", E_SHIELD)
    add("Nozzle zone shield hinged front", front, C_SHIELD, "metal", 16, "shell", E_SHIELD)
    win = _box(0, yf + 0.2, zc - 10, sx_ - 58, 1.0, zh - 78)
    cen = [(-wx0 + 9 + 13 * i, yf, wz0 + 8 + 13 * j) for i in range(13) for j in range(11)]
    win = _plate_holes(win, cen, 10.0, "y")
    add("Shield perforated window", win, C_SHIELD, "metal", 16, "shell", E_SHIELD)
    hinge = _union([_zcyl(-sx_ / 2 - 1, yf - 3, z, 3.5, 30) for z in (z0s + 35, z1s - 35)])
    latch = _ycyl(sx_ / 2 - 14, yf - 6, zc, 6.0, 10) + _box(sx_ / 2 - 14, yf - 1.5, zc, 16, 2, 16)
    add("Shield hinges", hinge, C_BRIGHT, "metal", 16, "shell", E_SHIELD)
    add("Shield latch knob", latch, C_BLACK, "plastic", 16, "shell", E_SHIELD)
    tri = Pos(sx_ / 2 - 30, yf - st / 2 - 0.2, z1s - 25) * Rot(90, 0, 0) * extrude(
        Polygon((-13, -11), (13, -11), (0, 12)), amount=0.4, both=True)
    add("Hot surface warning label", tri, C_WARN, "paper", 16, "shell", E_SHIELD)
    mark = _box(sx_ / 2 - 30, yf - st / 2 - 0.5, z1s - 25, 3, 0.3, 10) + _box(sx_ / 2 - 30, yf - st / 2 - 0.5, z1s - 33, 3, 0.3, 2.4)
    add("Warning label print", mark, C_BLACK, "paper", 16, "shell", E_SHIELD)

    # ------------------------------------------------------------ 17 fume hood and duct
    fyh, fzh = P["hood_face"]
    hxf = P["hood_x"]
    hz = D["fl1"]
    ho_ = _box(hxf - 60, 0, hz, 120, fyh, fzh)
    ho_ = _fillet_try(ho_, _edges_par(ho_, Axis.X), [8.0, 5.0])
    hi_ = _box(hxf - 59, 0, hz, 120, fyh - 2, fzh - 2)
    hi_ = _fillet_try(hi_, _edges_par(hi_, Axis.X), [7.0, 4.0])
    hood = ho_ - hi_
    lip = _box(hxf - 1, 0, hz, 2, fyh + 12, fzh + 12) - _box(hxf - 1, 0, hz, 4, fyh - 2, fzh - 2)
    lip = _fillet_try(lip, _edges_par(lip, Axis.X), [8.0, 4.0])
    hood += lip
    dr = P["duct_d"] / 2
    d0, d1 = hz + fzh / 2, hz + fzh / 2 + 120
    hood += _zring(hxf - 60, 0, d0 - 1, d1, dr, dr - 1.0)
    add("Side fume hood and duct stub (aluminum)", hood, C_ALU, "metal", 17, "shell", E_HOOD)
    clamp = _zring(hxf - 60, 0, d1 - 22, d1 - 10, dr + 2.5, dr - 0.5) + _box(hxf - 60, dr + 4, d1 - 16, 10, 8, 12)
    add("Duct band clamp", clamp, C_BRIGHT, "metal", 17, "shell", E_HOOD)
    # flexible duct: corrugated elbow toward the back (+Y), cut short for the render
    R = 80.0
    ctr = Vector(hxf - 60, R, d1 - 18)
    segs = []
    n = 16
    pts = [ctr + Vector(0, -R * cos(radians(90 * k / n)), R * sin(radians(90 * k / n))) for k in range(n + 1)]
    pts = [Vector(hxf - 60, 0, d1 - 25)] + pts + [ctr + Vector(0, 45, R)]
    for k, (a, c) in enumerate(zip(pts, pts[1:])):
        d = c - a
        segs.append(Solid.make_cylinder(dr + (3.0 if k % 2 else 1.8), d.length, Plane(origin=a, z_dir=d.normalized())))
    flex = _union(segs) - Solid.make_cylinder(dr - 2, 30, Plane(origin=pts[-1] - Vector(0, 20, 0), z_dir=(0, 1, 0)))
    add("Flexible duct to inline fan (cut short)", flex, "#C3C8CD", "metal", 17, "shell", E_HOOD)

    # ------------------------------------------------------------ 18 mold cooling fan
    fx, fyy, fzz = P["cool_fan"]
    xc, zc2 = P["cool_fan_x"], P["cool_fan_z"]
    frame = _box(xc, 0, zc2, fx, fyy, fzz)
    frame = _fillet_try(frame, _edges_par(frame, Axis.X), [8.0, 5.0])
    frame -= _xcyl(xc, 0, zc2, fyy / 2 - 4, fx + 2)
    for sy in (-1, 1):
        for sz in (-1, 1):
            frame -= _xcyl(xc, sy * 52.5, zc2 + sz * 52.5, 2.2, fx + 2)
    add("Cooling fan frame", frame, C_BLACK, "plastic", 18, "shell", E_FAN)
    hub = _xcyl(xc, 0, zc2, 20.0, fx - 6)
    blades = []
    for k in range(7):
        bl = Pos(xc, 0, zc2) * Rot(360 / 7 * k, 0, 0) * Pos(0, 0, 37) * Rot(0, 0, 32) * Box(2.5, 26, 36)
        blades.append(bl)
    rotor = hub + (_union(blades) & _xcyl(xc, 0, zc2, fyy / 2 - 6, fx))
    add("Cooling fan rotor", rotor, "#24282E", "plastic", 18, "shell", E_FAN)
    add("Cooling fan hub label", _xcyl(xc + (fx - 6) / 2 + 0.2, 0, zc2, 13.0, 0.4), C_ACCENT, "paper", 18, "shell", E_FAN)
    gx = xc + fx / 2 + 1.5
    fg = _union([_xcyl(gx, 0, zc2, rr + 1.0, 2.0) - _xcyl(gx, 0, zc2, rr - 1.0, 3.0) for rr in (54, 42, 30, 18)])
    for a in (45, 135, 225, 315):
        fg += Pos(gx, 0, zc2) * Rot(a, 0, 0) * Pos(0, 0, 38) * Box(2.0, 2.0, 76)
    add("Cooling fan finger guard", fg, C_BRIGHT, "metal", 18, "shell", E_FAN)
    z_leg0 = bt
    leg = _box(xc, 0, (z_leg0 + zc2 - fzz / 2) / 2, 3, 60, zc2 - fzz / 2 - z_leg0)
    leg += _box(xc - 10, 0, bt + 1.5, 20, 60, 3)
    add("Cooling fan bracket", leg, C_FRAME, "painted", 18, "shell", E_FAN)
    fb = _union([_hex_z(xc - 12, sy * 20, bt + 3, 10, 4) for sy in (-1, 1)])
    add("Fan bracket bolts", fb, C_BRIGHT, "metal", 15, "shell", E_FAN)

    # ------------------------------------------------------------ accessories (not in the BOM)
    rng = random.Random(7)
    trx, try_ = -320.0, -185.0
    tray = _box(trx, try_, 11, 170, 110, 22)
    tray = _fillet_try(tray, _edges_par(tray, Axis.Z), [14.0, 10.0])
    tin = _box(trx, try_, 13, 164, 104, 22)
    tin = _fillet_try(tin, _edges_par(tin, Axis.Z), [11.0, 7.0])
    tray -= tin
    tray = _fillet_try(tray, _top(tray), [0.8, 0.5])
    add("Flake tray", tray, C_ALU, "metal", None, "accessory", (0, 0, 0))
    Rh = 330.0
    heap = Pos(trx, try_, 2 + 15 - Rh) * Sphere(Rh) & _box(trx, try_, 11, 162, 102, 18)
    add("Recycled HDPE flake (heap)", heap, "#7F8E9E", "plastic", None, "accessory", (0, 0, 0))
    cols = [("#2F6DB5", "blue"), ("#E9E7E0", "white"), ("#3E8E5A", "green"), ("#E07B28", "orange")]
    groups = {c: [] for c, _ in cols}
    for i in range(96):
        c = cols[i % 4][0]
        x = trx + rng.uniform(-70, 70)
        y = try_ + rng.uniform(-42, 42)
        zs = 2 + 15 - Rh + (Rh ** 2 - (x - trx) ** 2 - (y - try_) ** 2) ** 0.5
        f = Pos(x, y, zs + 0.3) * Rot(rng.uniform(-18, 18), rng.uniform(-18, 18), rng.uniform(0, 180)) * \
            Box(rng.uniform(5, 10), rng.uniform(4, 8), 1.2)
        groups[c].append(f)
    for i in range(10):                                        # a few spilled on the bench
        c = cols[i % 4][0]
        x = trx + rng.uniform(95, 140)
        y = try_ + rng.uniform(-60, 40)
        groups[c].append(Pos(x, y, 0.6) * Rot(0, 0, rng.uniform(0, 180)) * Box(rng.uniform(5, 9), rng.uniform(4, 7), 1.2))
    for c, nm in cols:
        add(f"Recycled flake ({nm})", _union(groups[c]), c, "plastic", None, "accessory", (0, 0, 0))

    def plaque(x, y, z, rz, ry=0.0):
        pq = Box(cvx, cvy, cvz)
        pq = _fillet_try(pq, _edges_par(pq, Axis.Z), [3.0, 2.0])
        pq = _fillet_try(pq, _top(pq), [0.8, 0.5])
        pq += Pos(0, 0, cvz / 2 + 2.5) * Cone(2.5, 3.5, 5.0)
        return Pos(x, y, z) * Rot(0, ry, rz) * pq

    add("Molded test plaque (recycled HDPE, blue)", plaque(235, -150, cvz / 2, 18), "#2E5E8C", "plastic", None, "accessory", (0, 0, 0))
    add("Molded test plaque (recycled PP, green)", plaque(250, -60, cvz / 2, -12), "#3F7F5E", "plastic", None, "accessory", (0, 0, 0))
    add("Molded test plaque (natural HDPE)", plaque(222, -108, cvz + cvz / 2 + 0.2, 40), "#E3DED3", "plastic", None, "accessory", (0, 0, 0))

    # ------------------------------------------------------------ context: workbench top section
    bench = _box(-100, -10, -18, 780, 520, 36)
    bench = _fillet_try(bench, _top(bench), [3.0, 2.0])
    add("Workbench top (section)", bench, C_WOOD, "wood", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:50s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
