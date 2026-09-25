"""MicroMold concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. Z up, bench top at Z = 0, the operator stands on the -Y side.
The injection axis is vertical at X = 0, Y = 0: the rack ram pushes the plunger down
into the heated barrel, and melt leaves the nozzle into the mold on the clamp table.
Shown with the plunger raised (loading position).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, human_figure

# ---------------- key dimensions (mm) ----------------
BORE = 22.0            # barrel bore = plunger diameter
BARREL_OD = 42.0
Z_MOLD0, Z_SPLIT, Z_MOLD1 = 62.0, 107.0, 152.0   # mold bottom, parting plane, top
Z_NOZ0, Z_NOZ1 = 152.0, 192.0                    # nozzle
Z_BAR0, Z_BAR1 = 192.0, 452.0                    # heated barrel, 260 mm
Z_PL0, Z_PL1 = 482.0, 682.0                      # plunger, raised (150 mm stroke available)
Z_LC0, Z_LC1 = 682.0, 712.0                      # load cell
Z_RAM0, Z_RAM1 = 712.0, 975.0                    # rack ram
Z_HEAD0, Z_HEAD1 = 760.0, 900.0                  # drive head
COL_Y = 95.0                                     # column centre line
PIN = (0.0, 30.0, 830.0)                         # pinion shaft (x, y, z)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def zcyl(r, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def zring(ro, ri, z0, z1, x=0.0, y=0.0):
    return zcyl(ro, z0, z1, x, y) - zcyl(ri, z0 - 1, z1 + 1, x, y)


# 1 Base plate, bolted to the bench
base = Pos(0, 20, 6) * Box(320, 260, 12)

# 2 Column and drive head: rack-and-pinion head from a 1 t arbor press on a taller steel column
column = Pos(0, COL_Y, (12 + Z_HEAD1) / 2) * Box(80, 60, Z_HEAD1 - 12)
head = Pos(0, 25, (Z_HEAD0 + Z_HEAD1) / 2) * Box(110, 140, Z_HEAD1 - Z_HEAD0)
shaft = tube3((-70, PIN[1], PIN[2]), (70, PIN[1], PIN[2]), 14)
handle = tube3((70, PIN[1], PIN[2]), (70, PIN[1] - 390, PIN[2] + 225), 11) \
    + Pos(70, PIN[1] - 390, PIN[2] + 225) * Sphere(24)
drive = column + head + shaft + handle

# 3 Rack ram (from the arbor press)
ram = Pos(0, 0, (Z_RAM0 + Z_RAM1) / 2) * Box(28, 28, Z_RAM1 - Z_RAM0)

# 4 Plunger force load cell with coupling
loadcell = zcyl(28, Z_LC0, Z_LC1)

# 5 Plunger, 22 mm ground steel rod
plunger = zcyl(BORE / 2, Z_PL0, Z_PL1)

# 6 Heated barrel with loading funnel at the top
barrel = zring(BARREL_OD / 2, BORE / 2, Z_BAR0, Z_BAR1) \
    + (zring(40, BORE / 2, Z_BAR1, Z_BAR1 + 22) - Pos(0, 0, Z_BAR1 + 30) * Cylinder(36, 30))

# 7 Band heaters, two zones of 250 W on the barrel
heaters = zring(27, BARREL_OD / 2, 222, 272) + zring(27, BARREL_OD / 2, 332, 382)

# 8 Nozzle with 100 W nozzle heater
nozzle = zring(12, 2.5, Z_NOZ0, Z_NOZ1) + zring(20, 12, Z_NOZ0 + 8, Z_NOZ1 - 4)

# 9 Barrel bracket and heat break (mica washers) tying the barrel to the column
bracket = Pos(0, 32, 462) * Box(110, 150, 20) - zcyl(BARREL_OD / 2 + 2, 440, 480)

# 10 Insulation jacket and perforated guard
guard = zring(58, 30, Z_BAR0 + 6, Z_BAR1 - 14)

# 11 Mold clamp: lift table on a screw jack, raised to seat the mold on the nozzle
clamp = Pos(0, 0, 28) * Box(70, 70, 32) + Pos(0, 0, 53) * Box(170, 130, 14) \
    + tube3((0, -35, 28), (0, -150, 28), 8) + tube3((-45, -150, 28), (45, -150, 28), 7)

# 12 Aluminum mold set: two plates with four M10 clamp bolts and a sprue bushing
mold = Pos(0, 0, (Z_MOLD0 + Z_SPLIT) / 2) * Box(120, 90, Z_SPLIT - Z_MOLD0 - 1) \
    + Pos(0, 0, (Z_SPLIT + Z_MOLD1) / 2) * Box(120, 90, Z_MOLD1 - Z_SPLIT - 1)
for sx in (-48, 48):
    for sy in (-33, 33):
        mold = mold + zcyl(8, Z_MOLD1, Z_MOLD1 + 8, sx, sy)
cavity = Pos(0, 0, Z_SPLIT - 4) * Box(64, 50, 6)   # test plaque cavity, shows in the cutaway
mold = mold - cavity - zcyl(3, Z_SPLIT, Z_MOLD1 + 1)

# 13 Control box: two PID controllers, two SSRs, fused mains inlet, switch and force display
CB = (-330.0, -10.0)
ctrl = Pos(CB[0], CB[1], 60) * Box(200, 130, 120)
faces = Pos(CB[0] - 45, CB[1] - 67, 80) * Box(60, 6, 36) + Pos(CB[0] + 45, CB[1] - 67, 80) * Box(60, 6, 36)
ctrl = ctrl + faces

# 14 Wiring: heater and thermocouple harness in sleeving, control box to barrel
wiring = tube3((CB[0] + 100, CB[1] + 30, 100), (-160, 60, 100), 6) + tube3((-160, 60, 100), (-60, 30, 300), 6)

MOLD_C = "#9CA3AF"
parts = [
    Part("Base plate", base, "#4B5563", 1, (0, 140, -220)),
    Part("Column and rack-and-pinion drive head", drive, "#1F2937", 2, (0, 280, 0)),
    Part("Rack ram", ram, "#6B7280", 3, (0, 0, 380)),
    Part("Plunger load cell", loadcell, "#7C3AED", 4, (-170, 0, 230)),
    Part("Plunger, 22 mm", plunger, "#D1D5DB", 5, (0, 0, 200)),
    Part("Heated barrel", barrel, "#78716C", 6, (0, 0, 80)),
    Part("Band heaters, 2 x 250 W", heaters, "#C2410C", 7, (200, -60, 80)),
    Part("Nozzle and nozzle heater", nozzle, "#D4A017", 8, (0, 0, 10)),
    Part("Barrel bracket and heat break", bracket, "#0F766E", 9, (0, 170, 150)),
    Part("Insulation jacket and guard", guard, "#94A3B8", 10, (380, -80, 80), alpha=1.0),
    Part("Mold clamp (screw lift table)", clamp, "#115E59", 11, (0, -220, -90)),
    Part("Aluminum mold set", mold, "#B8C4CE", 12, (0, -270, 40)),
    Part("Control box with PID and SSR", ctrl, "#2563EB", 13, (-160, -80, 0)),
    Part("Heater and sensor wiring", wiring, "#111827", 14, (-120, -200, -60)),
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
    key_figures=["22 mm bore, 150 mm stroke: about 34 g HDPE shot (estimate)",
                 "Rack drive: about 9 MPa (90 bar) at 250 N on the handle (estimate)",
                 "600 W heaters, two PID zones; about 12 min warm-up (estimate)",
                 "About 6 min per shot, 10 shots per hour (estimate)",
                 "HDPE, PP, LDPE, PS only; never PVC",
                 "About $489 in parts with one mold (indicative)"],
    scale_figure=False, context=context, cut_exclude=("Control box with PID and SSR", "Heater and sensor wiring"),
    flow={"title": "material flow per shot, grams (estimates, 30 g HDPE test part)", "unit": "g",
          "stages": [("Sorted, washed flake", 36), ("Melt in barrel", 36), ("Injected shot", 34),
                     ("Part out of mold", 30)],
          "losses": [(1, "Purge and drool, to regrind", 2), (2, "Sprue, to regrind", 4)]},
)
