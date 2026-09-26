"""MicroMold sizing calculations, MMD-CAL-001 v0.2 (TRL 3, with the MMD-DDR-002 decisions).

Run from the repo root:  python docs/04-calcs/sizing.py
Imports PARAMS and derived() from cad/src/model.py, reads bom/bom.csv and project.yaml,
and prints every number quoted in docs/04-calcs/01-sizing.md. Tags in brackets, for
example [B3], match the note. All values are first-principles estimates.
"""
import csv
import sys
from math import cosh, exp, log, pi, sqrt, tanh
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
OUT = []


def out(tag, text):
    line = f"[{tag}] {text}"
    OUT.append(line)
    print(line)


# ---------------- assumptions ----------------
A = {
    "rho_melt": 0.75,        # g/cm3, HDPE melt at 200 to 220 C
    "rho_solid": 0.95,       # g/cm3, HDPE solid
    "cp_pe": 2.3,            # kJ/(kg K), HDPE average
    "h_fus": 205.0,          # kJ/kg, crystalline fraction of HDPE (about 70 % of 293 kJ/kg)
    "k_melt": 0.25,          # W/(m K), HDPE melt
    "k_flake": 0.12,         # W/(m K), tamped flake with air gaps
    "rho_flake": 450.0,      # kg/m3, tamped flake
    "alpha_part": 0.11e-6,   # m2/s, HDPE for cooling time
    "T_melt": 210.0, "T_set": 220.0, "T_amb": 25.0, "T_eject": 95.0, "T_core": 180.0,
    "handle_N": 250.0, "handle_max_N": 700.0,   # design pull; body weight hanging on the handle
    "eta_design": 0.60,      # TRL 2 design value for the drive
    "mu": 0.15,              # steel on steel or bronze, greased
    "journal_r": 10.0,       # mm, pinion journal radius
    "mesh_eff": 0.95,
    "pull_deg": 90.0,        # comfortable ratchet pull, +30 to -60 deg
    "E_steel": 200e3, "E_al": 69e3, "fy_steel": 235.0,   # MPa
    "K": 9464.0, "n": 0.40,  # power law for injection-grade HDPE at 210 C (150 Pa s at 1000 1/s)
    "fill_s": 10.0,          # hand fill time
    "shot_g": 34.0, "charge_g": 36.0, "part_g": 30.0, "sprue_g": 4.0,
    "cp_steel": 0.49, "rho_steel": 7.85, "cp_al": 0.90, "rho_al": 2.70,
    "k_wool": 0.045, "h_air": 10.0, "h_fan": 30.0,
    "k_steel": 50.0, "k_mica": 0.5, "k_g11": 0.30,
    "approach": 1.20,        # PID approach and heater lag on warm-up
    "fan_W": 25.0, "ctrl_W": 10.0,
    "heater_W": 300.0,       # each barrel band (DDR-002; was 250 W)
    "cool_fan_W": 18.0,      # 120 mm mains axial fan at the mold (DDR-002)
    "mass_target": 40.0,     # kg, R9 (DDR-002; was 35 kg)
    "V_capture": 0.40,       # m/s capture velocity at the funnel (quiet air, low release velocity)
    "x_capture": 0.10,       # m, funnel axis to hood face
}

pm = yaml.safe_load((ROOT / "project.yaml").read_text())
budget = float(pm["budget_usd"])
R = {}  # requirement results: id -> (value, target, status)

# ---------------- A. Geometry, shot size and mold stack (R2, R7) ----------------
area = D["area_plunger"]                      # mm2
swept = area * D["in_bore"] / 1000            # cm3
shot = swept * A["rho_melt"]
out("A1", f"Plunger area {area:.1f} mm2; stroke {P['stroke']:.0f} mm of which {D['in_bore']:.0f} mm in the bore; swept {swept:.1f} cm3")
out("A2", f"Ideal shot {shot:.1f} g HDPE at {A['rho_melt']} g/cm3 (target 30 g, margin {100 * (shot / 30 - 1):.0f} %)")
reserv = area * D["reservoir"] / 1000
out("A3", f"Bore below the tip at full stroke {D['reservoir']:.0f} mm, {reserv:.1f} cm3, {reserv * A['rho_melt']:.0f} g; barrel holds {(reserv + swept) * A['rho_melt'] / A['shot_g']:.1f} shots")
comp_allow = D["in_bore"] - 30.0 / A["rho_melt"] * 1000 / area
comp_worst = D["in_bore"] * (1 - 0.55 / A["rho_melt"])
shot_worst = (D["in_bore"] - comp_worst) * area / 1000 * A["rho_melt"]
out("A4", f"Stroke left for compacting the fresh charge while still giving the 30 g target: {comp_allow:.0f} mm; an unmelted charge at 0.55 g/cm3 needs {comp_worst:.0f} mm, leaving a {shot_worst:.0f} g shot")
table_max = P["table_min_top"] + P["table_travel"]
out("A5", f"Nozzle tip at {D['noz0']:.0f} mm; lift table {P['table_min_top']:.0f} to {table_max:.0f} mm; stacks from {D['noz0'] - table_max:.0f} to {D['noz0'] - P['table_min_top'] - P['mold_drop']:.0f} mm fit with {P['mold_drop']:.0f} mm drop; test mold {D['mold_h']:.0f} mm sits at {D['table_top']:.0f} mm")
out("A6", f"Column front face at Y = {D['col_front']:.0f} mm: mold depth up to {2 * D['col_front'] - 10:.0f} mm across Y with 5 mm clearance, so a 150 x 120 mm mold goes in with its 150 mm side along X")
R["R2"] = (f"{shot:.1f} g ideal; {shot_worst:.0f} g if the fresh charge is still loose flake", "30 g or more", "At risk")

# ---------------- B. Drive, force and pressure (R3, R2) ----------------
ratio = P["handle_len"] / P["pinion_r"]
eta_j = 1 / (1 + A["mu"] * A["journal_r"] / P["pinion_r"])
eta_g = 1 / (1 + A["mu"] * 0.364)            # guide friction from the 20 deg separating force
eta_calc = A["mesh_eff"] * eta_j * eta_g
out("B1", f"Ratio {ratio:.1f}:1; efficiency by parts: mesh {A['mesh_eff']:.2f} x journal {eta_j:.3f} x ram guide {eta_g:.3f} = {eta_calc:.2f}; design value kept at {A['eta_design']:.2f}")
F_d = A["handle_N"] * ratio * A["eta_design"]
F_c = A["handle_N"] * ratio * eta_calc
p_d, p_c = F_d / area, F_c / area
out("B2", f"At {A['handle_N']:.0f} N: plunger force {F_d / 1000:.2f} kN and melt pressure {p_d:.1f} MPa ({p_d * 10:.0f} bar, {p_d * 145.04:.0f} psi) at eta {A['eta_design']}; {F_c / 1000:.2f} kN and {p_c:.1f} MPa at eta {eta_calc:.2f}")
eta_need = 8.0 * area / (A["handle_N"] * ratio)
out("B3", f"Efficiency needed for 8 MPa at 250 N: {eta_need:.2f}; margin at the design value {100 * (p_d / 8 - 1):.0f} %")
F_max = A["handle_max_N"] * ratio * eta_calc
p_max = F_max / area
out("B4", f"Overload: {A['handle_max_N']:.0f} N (body weight) gives {F_max / 1000:.1f} kN and {p_max:.1f} MPa, {F_max / 9807:.2f} times the 1 t press rating")
rot = D["in_bore"] / P["pinion_r"]
per_pull = P["pinion_r"] * A["pull_deg"] * pi / 180
pulls = D["in_bore"] / per_pull
hand_path = D["in_bore"] * ratio / 1000
out("B5", f"Filling {D['in_bore']:.0f} mm of bore turns the pinion {rot:.2f} rad ({rot * 180 / pi:.0f} deg) and moves the handle grip {hand_path:.2f} m; one {A['pull_deg']:.0f} deg pull gives {per_pull:.1f} mm, so {pulls:.1f} ratchet pulls")
W_hold = p_d * swept                          # J (MPa x cm3 = J)
out("B6", f"Work at full pressure over the whole shot: {W_hold:.0f} J at the melt, {W_hold / A['eta_design']:.0f} J at the handle; one {A['pull_deg']:.0f} deg pull at 250 N gives {A['handle_N'] * P['handle_len'] / 1000 * A['pull_deg'] * pi / 180:.0f} J")

# ---------------- C. Structure and overload ----------------
ro, ri = P["barrel_od"] / 2, P["bore"] / 2
lame = (ro ** 2 + ri ** 2) / (ro ** 2 - ri ** 2)
out("C1", f"Barrel hoop stress {lame:.2f} x p: {lame * p_d:.1f} MPa at design, {lame * p_max:.1f} MPa at overload; factor {A['fy_steel'] * 0.85 / (lame * p_max):.1f} on 85 % of yield at 220 C")
cx, cy, cw = P["col"]
I_col = (cx * cy ** 3 - (cx - 2 * cw) * (cy - 2 * cw) ** 3) / 12
A_col = cx * cy - (cx - 2 * cw) * (cy - 2 * cw)
Z_col = I_col / (cy / 2)
e = P["col_y"]
L_col = D["pin_z"] - D["brk1"]
for tag, F in (("C2", F_c), ("C3", F_max)):
    M = F * e
    s = M / Z_col + F / A_col
    out(tag, f"Column {cx:.0f} x {cy:.0f} x {cw:.0f} tube, offset {e:.0f} mm: {F / 1000:.2f} kN gives {M / 1e6:.2f} kN m and {s:.1f} MPa (factor {A['fy_steel'] / s:.1f} on yield)")
defl = F_c * e * L_col ** 2 / (2 * A["E_steel"] * I_col)
out("C4", f"Column opening between bracket and pinion over {L_col:.0f} mm: {defl:.2f} mm lateral at the ram at {F_c / 1000:.2f} kN; a pinned floating coupling takes it up")
kx, ky, kt = P["bracket"]
arm = D["col_front"]
for tag, F in (("C5", F_c), ("C6", F_max)):
    for t in (10.0, kt):
        s = F * arm / (kx * t ** 2 / 6)
        out(tag + ("a" if t == 10 else "b"), f"Bracket {t:.0f} mm plate, {arm:.0f} mm arm, {F / 1000:.2f} kN: {s:.0f} MPa (factor {A['fy_steel'] / s:.1f})")
Ipl = pi * P["bore"] ** 4 / 64
Pcr = pi ** 2 * A["E_steel"] * Ipl / P["plunger_len"] ** 2
out("C7", f"Plunger buckling (pinned, {P['plunger_len']:.0f} mm): {Pcr / 1000:.0f} kN, {Pcr / F_max:.0f} times the overload force")
out("C8", f"Load cell: {F_c / 1000:.2f} kN in use and {F_max / 1000:.1f} kN at overload against 10 kN rated and a typical 15 kN (150 %) safe overload")

# ---------------- D. Mold clamp (R7) ----------------
As_M10 = 58.0
proof = 600.0 * As_M10
pre = 20000.0
total_pre = 4 * pre
A_max = total_pre / (2 * p_d) / 100          # cm2
cav = P["cavity"][0] * P["cavity"][1] / 100
out("D1", f"Four M10 8.8 bolts at {pre / 1000:.0f} kN preload ({100 * pre / proof:.0f} % of the {proof / 1000:.1f} kN proof load), torque about {0.2 * pre * 10 / 1000:.0f} N m each")
out("D2", f"Projected area held with a factor of 2 at {p_d:.1f} MPa: {A_max:.0f} cm2; test plaque {cav:.0f} cm2 ({cav * p_d / 10:.1f} kN)")
sep_max = cav * 100 * p_max
out("D3", f"At overload the plaque sees {sep_max / 1000:.0f} kN against {total_pre / 1000:.0f} kN preload: the parting line flashes, bolts stay below proof ({sep_max / 4 / 1000:.1f} kN each)")
mx, my, mt = P["mold"]
span = 2 * P["mold_bolt_xy"][0]
Ip = my * mt ** 3 / 12
F_cav = cav * 100 * p_d
d_pl = F_cav * span ** 3 / (48 * A["E_al"] * Ip)
s_pl = F_cav * span / 4 / (my * mt ** 2 / 6)
out("D4", f"Plate bending between bolt rows ({span:.0f} mm span): {s_pl:.0f} MPa, deflection {d_pl * 1000:.0f} um (HDPE flash begins at about 20 to 30 um)")
R["R7"] = (f"{A_max:.0f} cm2 at {p_d:.1f} MPa; stacks {D['noz0'] - table_max:.0f} to {D['noz0'] - P['table_min_top'] - P['mold_drop']:.0f} mm; 170 x 130 mm table", "150 x 120 mm, 40 to 120 mm stack, 40 cm2", "Met on paper")


# ---------------- E. Fill pressure through nozzle and sprue (R3) ----------------
def dp_pipe(Rm, L, Q):
    """Power-law pressure drop in a round channel, Pa. Rm and L in m, Q in m3/s."""
    n, K = A["n"], A["K"]
    gw = (3 * n + 1) / n * Q / (pi * Rm ** 3)
    return 2 * K * L / Rm * gw ** n


def dp_slit(h, w, L, Q):
    n, K = A["n"], A["K"]
    gw = (2 * n + 1) / n * 6 * Q / (w * h ** 2)
    return 2 * K * L / h * gw ** n


def fill(noz_d, sprue_r, t):
    Q = swept * 1e-6 / t
    a = dp_pipe(noz_d / 2000, 0.010, Q)
    b = dp_pipe(sprue_r / 1000, P["mold"][2] / 1000, Q)
    c = dp_slit(P["cavity"][2] / 1000, P["cavity"][1] / 1000, P["cavity"][0] / 2000, Q)
    return a / 1e6, b / 1e6, c / 1e6


for tag, nd, sr, t in (("E1", 3.0, 2.5, 3.0), ("E2", 3.0, 2.5, A["fill_s"]), ("E3", 4.0, 3.0, A["fill_s"]), ("E4", 4.0, 3.0, 20.0)):
    a, b, c = fill(nd, sr, t)
    out(tag, f"Nozzle {nd:.0f} mm, sprue {2 * sr - 1:.0f} to {2 * sr + 1:.0f} mm, fill {t:.0f} s: nozzle {a:.1f} + sprue {b:.1f} + cavity {c:.1f} = {a + b + c:.1f} MPa (available {p_d:.1f})")
fa, fb, fc = fill(4.0, 3.0, A["fill_s"])
p_fill = fa + fb + fc
t_frz = 0.3 * 3.0e-3 ** 2 / A["alpha_part"]
out("E5", f"A 6 mm sprue core in a 50 C mold freezes in about {t_frz:.0f} s, so pauses of about 1 s between ratchet pulls are tolerable")
out("E6", f"Bottle-grade HDPE (melt flow index below 1) is about five times as viscous: fill would need about {5 * p_fill:.0f} MPa, beyond the press; R1 now requires flake from injection-molded items")
R["R3"] = (f"{p_d:.1f} MPa at eta {A['eta_design']} ({p_c:.1f} at {eta_calc:.2f}); fill needs about {p_fill:.1f} MPa in {A['fill_s']:.0f} s", "8 MPa at 250 N or less", "Met on paper")

# ---------------- F. Plunger clearance ----------------
mu0 = 1000.0   # Pa s, low-shear viscosity, low end
for c_d in (0.05, 0.10, 0.20):
    h = c_d / 2 / 1000
    Q = pi * P["bore"] / 1000 * h ** 3 * p_d * 1e6 / (12 * mu0 * 0.030)
    out(f"F{int(c_d * 100)}", f"Diametral clearance {c_d:.2f} mm: backflow {Q * 1e9:.2f} mm3/s at {p_d:.1f} MPa over 30 mm of seal, {Q * 1e9 * 30:.0f} mm3 in a 30 s hold")
grow = P["bore"] * 12e-6 * (A["T_set"] - 25) - P["bore"] * 12e-6 * (100 - 25)
out("F9", f"Hot bore grows {grow * 1000:.0f} um more than a 100 C plunger: recommended cold clearance 0.05 to 0.10 mm diametral (22 H8/f7 gives 0.020 to 0.074 mm)")

# ---------------- G. Heat: warm-up, losses, skin, load cell (R5, R11, R4) ----------------
steel_barrel = pi / 4 * (P["barrel_od"] ** 2 - P["bore"] ** 2) * P["barrel_len"] / 1000 * A["rho_steel"] / 1000
steel_top = (pi / 4 * (P["flange"][0] ** 2 - P["bore"] ** 2) * (P["flange"][1] + P["funnel"][1]) * 0.6) / 1000 * A["rho_steel"] / 1000
nozzle_kg = 0.30
m_barrel_zone = steel_barrel + steel_top + 0.30               # plus two heaters
wool_kg = pi / 4 * (P["jacket"][0] ** 2 - 60 ** 2) * 240 / 1e9 * 100
E_barrel = m_barrel_zone * A["cp_steel"] * (A["T_set"] - 20) + 0.040 * (A["cp_pe"] * 190 + A["h_fus"]) + wool_kg * 0.84 * 100
out("G1", f"Barrel zone: steel {steel_barrel:.2f} kg barrel + {steel_top:.2f} kg flange and funnel + 0.30 kg heaters; {E_barrel:.0f} kJ to 220 C with 40 g of cold plastic and the wool")
L_jk = (D["brk0"] - P["jacket"][2]) - (D["bar0"] + P["jacket"][1])
r1, r2 = 0.030, 0.055
Rc = log(r2 / r1) / (2 * pi * A["k_wool"])
Rv = 1 / (A["h_air"] * 2 * pi * r2)
q_l = (A["T_set"] - A["T_amb"]) / (Rc + Rv)
Q_jacket = q_l * L_jk / 1000
T_skin = A["T_amb"] + q_l * Rv
out("G2", f"Jacket, {L_jk:.0f} mm of 25 mm mineral wool: {Q_jacket:.0f} W; skin {T_skin:.0f} C at 220 C set point and 25 C ambient")
Q_fun = 0.012 * 12 * (150 - A["T_amb"])
Q_noz = 0.006 * 14 * (A["T_set"] - A["T_amb"]) + 0.15 * (A["T_set"] - 50) / 6
G_pad = A["k_mica"] * 4 * 225e-6 / 0.003
G_brk = G_pad + 0.10
Q_brk = G_brk * (180 - 40)
mfin = sqrt(4 * A["h_air"] / (A["k_steel"] * P["bore"] / 1000))
mL = mfin * P["plunger_len"] / 1000
Q_pl = A["k_steel"] * area * 1e-6 * mfin * (150 - A["T_amb"]) * tanh(mL)
Q_loss = Q_jacket + Q_fun + Q_noz + Q_brk + Q_pl
out("G3", f"Standing losses at 220 C: jacket {Q_jacket:.0f}, funnel {Q_fun:.0f}, nozzle {Q_noz:.0f}, bracket heat break {Q_brk:.0f} (mica pads {G_brk:.2f} W/K), plunger {Q_pl:.0f}: {Q_loss:.0f} W")
P_bar = 2 * A["heater_W"]
t_bar = E_barrel * 1000 / (P_bar - 0.5 * (Q_loss - Q_noz)) * A["approach"] / 60
E_noz = nozzle_kg * A["cp_steel"] * (A["T_set"] - 20)
t_noz = E_noz * 1000 / (100 - 0.5 * Q_noz) * A["approach"] / 60
out("G4", f"Warm-up: barrel zone {t_bar:.1f} min, nozzle zone {t_noz:.1f} min (with a {A['approach']:.1f} allowance for PID approach)")
R["R5"] = (f"{t_bar:.1f} min (barrel zone, 2 x {A['heater_W']:.0f} W)", "15 min or less", "At risk" if t_bar > 0.9 * 15 else "Met on paper")
t_250 = E_barrel * 1000 / (500.0 - 0.5 * (Q_loss - Q_noz)) * A["approach"] / 60
out("G4b", f"With the former two 250 W bands (TRL 3 v0.1) the barrel zone took {t_250:.1f} min; the {A['heater_W']:.0f} W bands save {t_250 - t_bar:.1f} min")
wd = A["heater_W"] / (pi * 4.2 * 5.0)
out("G5", f"Band heater watt density {wd:.1f} W/cm2 (mica bands are commonly rated to about 7.7 W/cm2, 50 W/in2)")
theta = 1 / cosh(mL)
T_top = A["T_amb"] + theta * (150 - A["T_amb"])
R_sp = P["spacer_t"] / 1000 / (A["k_g11"] * area * 1e-6)
T_lc = A["T_amb"] + (T_top - A["T_amb"]) * 3.0 / (R_sp + 3.0)
out("G6", f"Plunger as a fin (mL = {mL:.2f}): top end {T_top:.0f} C with its tip at 150 C; load cell directly on it about {T_top:.0f} C, with the {P['spacer_t']:.0f} mm G-11 spacer ({R_sp:.0f} K/W) about {T_lc:.0f} C")
R["R11"] = (f"Jacket skin {T_skin:.0f} C; nozzle zone shield added", "60 C or less; nozzle and mold zone guarded", "Met on paper")
R["R4"] = ("Two PID zones, 150 to 260 C set range, set point limit, 280 C cut-out", "150 to 260 C, within 5 C; cut-out above 280 C", "Met by design")

# ---------------- H. Melt soak, mold heat and cycle (R6) ----------------
cp_eff = (A["cp_pe"] * (200 - A["T_amb"]) + A["h_fus"]) / (200 - A["T_amb"]) * 1000
theta_c = (A["T_core"] - A["T_set"]) / (A["T_amb"] - A["T_set"])
Fo = log(1.602 / theta_c) / 5.783
Rb = P["bore"] / 2000
t_melt = Fo * Rb ** 2 / (A["k_melt"] / (A["rho_melt"] * 1000 * cp_eff)) / 60
t_flake = Fo * Rb ** 2 / (A["k_flake"] / (A["rho_flake"] * cp_eff)) / 60
out("H1", f"Soak for a 22 mm bore to bring the center to {A['T_core']:.0f} C (Fo = {Fo:.2f}, effective cp {cp_eff / 1000:.2f} kJ/(kg K)): {t_melt:.1f} min as melt, {t_flake:.1f} min as tamped flake")
steps = [("Load and tamp the fresh charge", 1.0), ("Bolt the mold and raise the table", 0.75), ("Inject in four ratchet pulls", 0.25),
         ("Hold", 0.5), ("Cool in the mold", None), ("Lower, unbolt, open and eject", 1.0), ("Clean and reassemble", 0.75)]
Q_shot = (A["part_g"] + A["sprue_g"]) / 1000 * (A["cp_pe"] * (A["T_melt"] - 50) + A["h_fus"]) * 1000
m_mold = 2 * mx * my * mt / 1e3 * A["rho_al"] / 1000
area_mold = 2 * 2 * (mx * my + mx * mt + my * mt) / 1e6
cyc = 6.0
res = {}
fixed = sum(s for _, s in steps if s)
for tag, hh, name in (("H2", A["h_air"], "still air"), ("H3", A["h_fan"], "fan")):
    Tw = A["T_amb"] + Q_shot / (cyc * 60) / (hh * area_mold)
    tc = (P["cavity"][2] / 1000) ** 2 / (pi ** 2 * A["alpha_part"]) * log(4 / pi * (A["T_melt"] - Tw) / (A["T_eject"] - Tw)) / 60
    res[name] = (Tw, tc)
    out(tag, f"Mold {m_mold:.2f} kg takes {Q_shot / 1000:.1f} kJ a shot ({Q_shot / (cyc * 60):.0f} W at 6 min cycles); in {name} it settles at {Tw:.0f} C and the 6 mm plaque needs {tc:.1f} min to reach {A['T_eject']:.0f} C")
for nm in ("still air", "fan"):
    tc = res[nm][1]
    tot = sum(s for _, s in steps if s) + tc
    out("H4" if nm == "still air" else "H5", f"Cycle with {nm} mold cooling: {tot:.1f} min, {60 / tot:.1f} parts per hour; fresh charge soaks about {2 * tot - 1:.0f} min over two cycles (needs {t_flake:.1f})")
tot_air = fixed + res["still air"][1]
tot_fan = fixed + res["fan"][1]
cyc_soak = (t_flake + 1) / 2                  # fresh charge must soak about two cycles
cyc_design = max(tot_fan, cyc_soak)
out("H6", f"Design cycle with the mold cooling fan (DDR-002): {cyc_design:.1f} min ({'soak' if cyc_soak > tot_fan else 'cooling'} limited), {60 / cyc_design:.1f} parts per hour, mold about {res['fan'][0]:.0f} C")
R["R6"] = (f"{60 / cyc_design:.1f} per hour with the mold fan, mold about {res['fan'][0]:.0f} C", "8 per hour or more", "Met on paper")

# ---------------- I. Power and energy (R10) ----------------
P_heat = P_bar + 100
aux = A["fan_W"] + A["ctrl_W"] + A["cool_fan_W"]
P_tot = P_heat + aux
out("I1", f"Connected load {P_tot:.0f} W ({P_heat:.0f} W heaters, {A['fan_W']:.0f} W duct fan, {A['cool_fan_W']:.0f} W mold fan, {A['ctrl_W']:.0f} W controls): {P_tot / 230:.1f} A at 230 V, {P_tot / 120:.1f} A at 120 V")
E_plastic = A["charge_g"] / 1000 * (A["cp_pe"] * (A["T_melt"] - A["T_amb"]) + A["h_fus"]) / 3.6
E_shot = E_plastic + (Q_loss + aux) * cyc_design / 60
out("I2", f"Energy per shot: {E_plastic:.1f} Wh into the plastic + {(Q_loss + aux) * cyc_design / 60:.1f} Wh losses and auxiliaries over {cyc_design:.1f} min = {E_shot:.0f} Wh, {E_shot / A['part_g']:.2f} kWh per kg of parts")
duty = (Q_loss - Q_noz + E_plastic * 60 / cyc_design) / P_bar
out("I3", f"Barrel zone duty at steady running about {100 * duty:.0f} %")
R["R10"] = (f"{P_tot:.0f} W; {P_tot / 120:.1f} A at 120 V", "1 kW or less; 10 A or less at 120 V", "Met on paper")

# ---------------- J. Fume hood (R13) ----------------
fy, fz = P["hood_face"]
Af = fy * fz / 1e6
Qh = 0.75 * A["V_capture"] * (10 * A["x_capture"] ** 2 + Af)
vd = Qh / (pi / 4 * (P["duct_d"] / 1000) ** 2)
out("J1", f"Flanged side hood {fy:.0f} x {fz:.0f} mm, {A['x_capture'] * 1000:.0f} mm from the funnel axis, {A['V_capture']:.2f} m/s capture: {Qh * 3600:.0f} m3/h; duct velocity {vd:.1f} m/s in {P['duct_d']:.0f} mm duct")
R["R13"] = (f"Hood and fan {Qh * 3600:.0f} m3/h; set point limit 260 C", "Exhaust hood or outdoors; set points above 260 C blocked", "Met on paper")

# ---------------- K. Mass and size (R9) ----------------
bx, by, bt = P["base"]
mass = {
    "base plate": bx * by * bt / 1e6 * A["rho_steel"],
    "column tube": A_col * (D["head1"] - bt) / 1e6 * A["rho_steel"],
    "arbor press head, ram and ratchet (assumed)": 8.0,
    "bracket": kx * ky * kt / 1e6 * A["rho_steel"],
    "barrel set and heaters": steel_barrel + steel_top + 0.30 + nozzle_kg,
    "plunger, load cell and spacer": area * P["plunger_len"] / 1e6 * A["rho_steel"] + 0.40,
    "jacket and guard (assumed)": 1.0,
    "clamp (table plus jack, assumed 1.5 kg)": P["table"][0] * P["table"][1] * P["table"][2] / 1e6 * A["rho_steel"] + 1.5,
    "mold set with bolts": m_mold + 0.35,
    "nozzle zone shield": 0.9,
    "hood on the press (assumed)": 0.6,
    "mold cooling fan and bracket (assumed)": 0.7,
    "hardware (assumed)": 1.0,
}
m_tot = sum(mass.values())
out("K1", "Mass: " + "; ".join(f"{k} {v:.1f}" for k, v in mass.items()) + f"; total {m_tot:.1f} kg without the control box")
out("K2", f"Footprint {bx:.0f} x {by:.0f} mm; top of the handle {D['handle_top']:.0f} mm above the bench at the highest start of a pull ({P['handle_up_deg']:.0f} deg); ram top {D['ram1']:.0f} mm")
mt_ = A["mass_target"]
out("K3", f"Mass {mt_ - m_tot:.1f} kg under the {mt_:.0f} kg target (DDR-002; was 35 kg), {100 * m_tot / mt_:.0f} % of it; the largest items are the base plate, the assumed 8 kg arbor press head and the column")
R["R9"] = (f"{bx:.0f} x {by:.0f} mm; {D['handle_top']:.0f} mm; {m_tot:.1f} kg", f"350 x 300 mm; 1.1 m; {mt_:.0f} kg", "Not met" if m_tot > mt_ else ("At risk" if m_tot > 0.95 * mt_ else "Met on paper"))

# ---------------- L. Cost (R14, R8) ----------------
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
mold_cost = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if r["item"].startswith("12 "))
fume = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows if r["item"].startswith("17 "))
press = tot - mold_cost
out("L1", f"BOM {len(rows)} lines, all priced: ${tot:.2f} with one mold; press alone ${press:.2f}; mold ${mold_cost:.2f}; fume extraction ${fume:.2f}")
out("L2", f"Against budget_usd ${budget:.0f}: press alone (redefined R14 scope) over by ${press - budget:.2f}; press and one mold (original scope) over by ${tot - budget:.2f}; press without fume extraction ${press - fume:.2f}")
R["R14"] = (f"${press:.0f} press; ${tot:.0f} with one mold", f"Press ${budget:.0f} or less, molds as tooling", "Not met" if press > budget else ("At risk" if press > 0.95 * budget else "Met on paper"))
R["R8"] = (f"${mold_cost:.0f} (indicative)", "$100 or less", "Met on paper")
R["R1"] = ("HDPE, PP, LDPE, PS within 150 to 260 C from injection-molded items; PVC and bottle-grade HDPE excluded by label and procedure", "Four resins, injection grade; PVC excluded", "Met by design")
R["R12"] = ("Earthed frame, fused inlet, DP switch, RCD or GFCI, 250 C wiring", "As listed", "Met by design")
R["R15"] = ("Only the barrel set and molds need a lathe or mill (local shop)", "Hand tools, drill press, optional welding", "Met by design")
R["R16"] = ("Needs hardware", "Mass within 3 % over 10 shots", "Not verifiable at TRL 3")

# ---------------- M. Results table ----------------
order = {"Not met": 0, "At risk": 1, "Met on paper": 2, "Met by design": 3, "Not verifiable at TRL 3": 4}
ids = sorted(R, key=lambda k: (order[R[k][2]], int(k[1:])))
print("[M] Requirement status")
for k in ids:
    v, t, s = R[k]
    print(f"    {k:4s} {s:24s} {v}  | target: {t}")
counts = {}
for k in R:
    counts[R[k][2]] = counts.get(R[k][2], 0) + 1
print("[M] Counts: " + ", ".join(f"{counts.get(s, 0)} {s}" for s in order))
assert len(R) == 16

RESULTS = {"shot": shot, "p_design": p_d, "p_calc": p_c, "eta_calc": eta_calc, "pulls": pulls, "t_warm": t_bar,
           "cycle_air": tot_air, "cycle": cyc_design, "T_mold": res["fan"][0], "P_heat": P_heat, "loss_W": Q_loss, "P_tot": P_tot, "mass": m_tot, "press_cost": press, "total_cost": tot,
           "A_max": A_max, "E_shot": E_shot, "E_plastic": E_plastic, "p_fill": p_fill, "Qh": Qh * 3600}
