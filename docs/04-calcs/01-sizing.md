---
doc_id: MMD-CAL-001
title: MicroMold sizing calculations
project: MicroMold
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (shot size, drive and ratchet, structure, mold clamp, fill pressure, plunger clearance, heat, melt soak and cycle, power, fume hood, mass, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($520, MMD-DDR-002); R14 from not met to at risk
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: "Constructable design (MMD-DDR-003): mass, heights, heat and cost updated; budget treated as a value-engineering target"
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: Decisions of 2026-10-02 carried in - torque-limiting socket set to 180 N m from the press rating (overload now 8.3 kN, B4a and B4b), plunger rest, BOM 21 lines, mass 39.8 kg, press USD 590
---

# MicroMold sizing calculations

On paper, MicroMold meets twelve of its sixteen requirements (eight by calculation, four by design), has two at risk, misses none, is over its value-engineering target on cost and leaves one requirement that only hardware can show. Version 0.5 carries the decisions Amish approved on 2026-10-02: a torque-limiting socket set to 180 N m on the ratchet adapter, which caps the overload at 8.3 kN, and a plunger rest on the column. Version 0.4 followed the constructable design of MMD-DDR-003 (2026-10-01): plates and fixings added, an 8 mm base plate, a 100 mm flange, a screw lift with a handwheel nut and a plunger coupling. This issue includes the decisions Amish made on 2026-09-25 (MMD-DDR-002): a 40 kg mass target, two 300 W barrel bands, a mold cooling fan and injection-grade feedstock in R1. On 2026-09-26 Amish approved a `budget_usd` of $520 to cover the priced BOM (MMD-DDR-002). `budget_usd` is a hypothetical value-engineering target, not a limit (Amish, 2026-10-01). Value-engineering target: USD 520. Estimated cost of the constructable design: USD 590 (USD 70 over the target) for the press, and USD 684 with the first mold, which is tooling (R14). The two at risk are mass (R9, 39.8 kg against 40 kg with an assumed 8 kg arbor press head) and shot size (R2, if the fresh charge is not tamped). The 300 W bands bring warm-up to 12.3 min (R5), and the fan keeps the mold near 47 °C, so throughput (R6) is 11.6 parts per hour, limited by melt soak. The v0.1 calculations also showed that the TRL 2 concept could not work as drawn: a single pull of the arbor press handle moves the plunger only about 31 mm, not the 120 mm a shot needs, so a ratchet handle drives the pinion. Five more changes followed: a 4 mm nozzle orifice with a tapered sprue, a glass-epoxy spacer that keeps the load cell cool, a 20 mm bracket plate on mica pads, a nozzle zone shield, and a nozzle tip raised to 190 mm so that 120 mm mold stacks fit. Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B5], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not replace a pressure and electrical safety review of a built press. The barrel, nozzle and mold reach 180 to 260 °C, the melt is under pressure, the heaters run at mains voltage and without the torque-limiting socket an operator can load the press to about 1.35 times its rating; with it set to 180 N m the limit is 0.85 times. See MMD-PRC-001, Safety.

## Scope and method

The note checks every requirement in MMD-REQ-001 v0.7 against the design in MMD-PRC-001 v0.8 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()` stack-up, so the bore, stroke, nozzle height, table travel, bracket, mold and hood used here are those in the STEP files and in drawing MMD-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`.

The design case is the reference part of MMD-REQ-001: a 30 g HDPE test plaque, 64 x 50 x 6 mm, molded from washed, dried flake of 3 to 8 mm at a 220 °C barrel set point in a 25 °C workshop.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| HDPE properties | Melt density 0.75 g/cm³, solid 0.95 g/cm³; cp 2.3 kJ/(kg K); 205 kJ/kg to melt the crystalline fraction; melt conductivity 0.25 W/(m K); tamped flake 0.12 W/(m K) at 450 kg/m³; diffusivity 0.11 mm²/s for part cooling | Typical handbook values; estimates to confirm for the chosen feedstock |
| Melt flow | Power law, n = 0.40, 150 Pa s at 1,000 s⁻¹ (K = 9,464 Pa sⁿ) at 210 °C, typical of injection-grade HDPE; 1,000 Pa s at low shear for leakage | Estimate; bottle-grade HDPE is several times more viscous |
| Drive | 450 mm handle on a 20 mm pinion pitch radius; design efficiency 0.60 (TRL 2 value); friction 0.15 for the journal and ram guide; mesh 0.95 | Arbor press dimensions to confirm on the chosen press |
| Operator | 250 N design pull; 700 N when the operator hangs body weight on the handle, limited to the socket's 180 N m (+10 % tolerance, about 440 N); a comfortable ratchet pull of 90° (from 30° above horizontal to 60° below) | Ergonomic judgment |
| Structure | S235 steel, yield 235 MPa, 85 % of yield at 220 °C; E 200 GPa steel, 69 GPa aluminum | Handbook |
| Mold clamp | Four M10 class 8.8 bolts (58 mm², proof 600 MPa) at 20 kN preload each; factor 2 against opening | As at TRL 2 |
| Heat | Combined convection and radiation 10 W/(m² K) in still air, 30 W/(m² K) with a fan; mineral wool 0.045 W/(m K); mica 0.5 W/(m K); G-11 glass-epoxy 0.30 W/(m K); steel cp 0.49 kJ/(kg K); a factor of 1.2 on warm-up for PID approach and heater lag | Handbook ranges |
| Cycle | Ejection at 95 °C; step times in Table 3 | Estimates, to be timed later |
| Fume capture | Flanged side hood, capture velocity 0.40 m/s at 100 mm from the funnel axis (low-velocity release into quiet air) | Common design range for hoods |
| Mass | Arbor press head, ram and ratchet 8.0 kg; jacket 1.0 kg; lift screw and handwheel nut 1.0 kg; plunger rest 0.3 kg; torque-limiting socket 0.6 kg (assumed); hood on the press 0.6 kg; mold cooling fan and bracket 0.7 kg; hardware 1.0 kg | Assumed; the head mass depends on the chosen press |

## A. Shot size and mold stack (R2, R7)

- **Swept volume.** The 22 mm plunger has 380.1 mm² of area. Of the 150 mm stroke, the first 30 mm clears the funnel and 120 mm is in the bore, sweeping 45.6 cm³ [A1], or 34.2 g of HDPE melt, 14 % above the 30 g target [A2].
- **Reservoir.** At full stroke 140 mm of bore (53.2 cm³, 40 g) stays below the plunger tip, so the barrel holds 2.2 shots [A3], and each charge soaks for about two cycles before it is injected.
- **Compaction eats stroke.** Only 15 mm of stroke is spare once 30 g has been delivered. If the fresh charge on top is still loose flake at 0.55 g/cm³ when the operator injects, compacting it takes about 32 mm and the shot falls to about 25 g [A4]. Tamping each top-up with the press while loading is therefore part of the process, and R2 is **at risk** until a trial shows the charge is dense enough.
- **Mold stack.** With the nozzle tip at 190 mm and a lift table that travels from 60 to 160 mm, mold stacks from 30 to 120 mm fit with 10 mm to drop clear of the nozzle; the 90 mm test mold sits at 102 mm, because the nozzle tip seats 2 mm deep in the mold's spherical seat [A5]. The TRL 2 layout, with the nozzle at 152 mm, could not take a 120 mm stack.
- **Mold footprint.** The column face is 65 mm behind the axis, so molds up to 120 mm deep across Y fit, and a 150 x 120 mm mold goes in with its long side along X [A6].

## B. Drive, force and the ratchet (R3, R2)

- **Ratio and efficiency.** The handle and pinion give 22.5:1. Friction losses at the mesh, the pinion journals and the ram guide give an efficiency of about 0.84; the design keeps the TRL 2 value of 0.60 as a margin for a worn or dirty press [B1].
- **Pressure.** At 250 N on the handle the plunger force is 3.38 kN and the melt pressure 8.9 MPa (89 bar, 1,288 psi) at 0.60 efficiency, or 4.71 kN and 12.4 MPa at 0.84 [B2]. R3 (8 MPa) needs an efficiency of 0.54, a margin of 11 % at the design value [B3].
- **Overload.** Without a limiter, an operator hanging 700 N of body weight on the handle produces 13.2 kN, 1.35 times the 1 t rating of the press [B4]. A torque-limiting socket on the ratchet adapter (decided by Amish, 2026-10-02) removes that case. The press reaches its rating at 234 N m at the pinion (9.8 kN at 0.84 efficiency and a 20 mm pitch radius); the socket is set to 180 N m, 77 % of that, or 198 N m at its worst tolerance of plus 10 % [B4a]. The ram force is then at most 8.3 kN and the melt pressure 21.8 MPa, 0.85 times the press rating and 0.83 of the load cell's 10 kN range; the socket slips at a pull of about 400 N on the 450 mm handle, while the 250 N working pull is 62 % of the setting and does not trip it [B4b]. Sections C and D size the parts for this limited case. The setting is checked against the load cell at TRL 4.
- **Stroke per pull (finding).** Filling the 120 mm of bore turns the pinion 344° and moves the grip 2.70 m. One comfortable 90° pull moves the plunger 31.4 mm, so a shot takes 3.8 pulls [B5]. No single sweep of a 450 mm handle can deliver the shot; the TRL 2 statement that "a steady pull drives the plunger 120 to 150 mm" was wrong. The work confirms it: at full pressure a shot needs 405 J at the melt and 675 J at the handle, while one 90° pull at 250 N gives 177 J [B6].
- **Change.** A 1/2 in drive ratchet handle, 450 mm long, on a socket fitted to the pinion shaft replaces the press's fixed handle (BOM item 2, about $25), with the torque-limiting socket (BOM item 21, about $40) between the adapter and the ratchet. The pawl holds the ram between pulls, so the melt stays under pressure while the operator resets. This is within the rack-and-pinion drive (MMD-DDR-001 D1), decided by Amish on 2026-09-25.

## C. Structure and overload

- **Barrel.** The thick-walled barrel (42 mm OD, 22 mm bore) sees a hoop stress of 1.76 times the melt pressure: 15.6 MPa at design and 38.3 MPa at the torque limit, a factor of 5.2 on 85 % of yield at 220 °C [C1].
- **Column.** The barrel axis is 95 mm in front of the column center, so the 80 x 60 x 3 mm tube carries a bending moment between the bracket and the drive head: 34.5 MPa at 4.71 kN (factor 6.8) and 60.7 MPa at the 8.3 kN torque limit (factor 3.9; 96.6 MPa, factor 2.4, at 13.2 kN without the socket) [C2, C3]. The frame opens about 0.31 mm at the ram in use, over the 358 mm between the shelf and the pinion [C4], so the plunger joins the load cell through a pinned floating coupling and is guided only by the bore.
- **Bracket (change).** The bracket cantilevers 65 mm from the column face. A 10 mm plate, as in the TRL 2 BOM, reaches 167 MPa in use (factor 1.4) and would reach 294 MPa at the torque limit (factor 0.8), above yield. A 20 mm plate gives 42 MPa in use and 74 MPa at the torque limit, a factor of 3.2 [C5a, C5b, C6a, C6b]. BOM item 9 is now a 20 mm plate.
- **Plunger and load cell.** Plunger buckling is not a concern (567 kN, 68 times the force at the torque limit) [C7]. The 10 kN load cell sees 4.71 kN in use and 8.3 kN at the torque limit, inside its rated range; without the socket it would see 13.2 kN, above the range but inside the 150 % safe overload typical of such cells [C8].

## D. Mold clamp (R7)

- **Bolts.** Four M10 class 8.8 bolts at 20 kN preload each (57 % of proof) need about 40 N m of torque [D1].
- **Area.** With a factor of 2 at 8.9 MPa the bolts hold 45 cm² of projected area, against the 40 cm² target; the 32 cm² plaque pushes the plates apart with 28.4 kN [D2]. R7 is met on paper.
- **Overload.** At the torque limit (21.8 MPa) the plaque pushes with 70 kN against 80 kN of preload, so the parting line should stay shut, and each bolt carries 17.5 kN, below its proof load [D3]. Without the socket, 34.7 MPa would push with 111 kN and the parting line would flash and spit melt. The nozzle zone shield is still there for a failure of the limit.
- **Plates.** The 45 mm plates bend 11 µm between bolt rows, at 22 MPa, below the 20 to 30 µm at which HDPE starts to flash [D4].

## E. Fill pressure through the nozzle and sprue (R3)

*Table 2. Pressure needed to fill the plaque [E1 to E4].*

| Nozzle orifice | Sprue | Fill time | Nozzle | Sprue | Cavity | Total | Available at 250 N |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 mm (TRL 2) | 4 to 6 mm | 3 s | 4.6 MPa | 6.7 MPa | 0.9 MPa | 12.1 MPa | 8.9 MPa |
| 3 mm (TRL 2) | 4 to 6 mm | 10 s | 2.8 MPa | 4.1 MPa | 0.5 MPa | 7.5 MPa | 8.9 MPa |
| 4 mm | 5 to 7 mm | 10 s | 1.5 MPa | 2.8 MPa | 0.5 MPa | 4.8 MPa | 8.9 MPa |
| 4 mm | 5 to 7 mm | 20 s | 1.1 MPa | 2.1 MPa | 0.4 MPa | 3.6 MPa | 8.9 MPa |

- **Change.** A shear-thinning melt needs almost as much pressure for a slow fill as for a fast one, so the TRL 2 nozzle left little margin. A 4 mm orifice and a sprue tapering from 5 to 7 mm bring a 10 s hand fill down to 4.8 MPa, about half the pressure available. BOM items 8 and 12 are updated.
- **Pauses.** A 6 mm sprue core in a 50 °C mold takes about 25 s to freeze, so the pauses of about 1 s between ratchet pulls do not stop the fill [E5].
- **Feedstock.** HDPE from blow-molded bottles (melt flow index below 1) is about five times as viscous and would need about 24 MPa, beyond the press [E6]. Flake from injection-molded items (caps, crates, buckets) suits it; R1 now requires it (MMD-DDR-002).

## F. Plunger clearance

- **Backflow.** At 8.9 MPa over 30 mm of seal, a diametral clearance of 0.05 mm leaks 1 mm³ during a 30 s hold, 0.10 mm leaks 6 mm³ and 0.20 mm leaks 51 mm³, all negligible against a 45,600 mm³ shot [F5, F10, F20]. The charge above the melt also seals the gap.
- **Fit.** The hot bore grows about 32 µm more than a plunger at 100 °C, so the gap opens as the barrel heats. A cold diametral clearance of 0.05 to 0.10 mm is recommended; 22 H8/f7 gives 0.020 to 0.074 mm [F9]. This answers the TRL 2 open question on clearance.

## G. Heat: warm-up, losses, skin and load cell (R5, R11, R4)

- **Heat to store.** The barrel zone holds 2.05 kg of barrel, about 0.72 kg of flange and funnel and 0.30 kg of heaters, and needs 342 kJ to reach 220 °C including 40 g of cold plastic and the mineral wool [G1].
- **Jacket.** 217 mm of 25 mm mineral wool loses 17 W, with the skin at 48 °C at a 220 °C set point [G2]. R11's 60 °C limit is met on paper for the jacket.
- **Standing losses.** At 220 °C: jacket 18 W, funnel 18 W, nozzle 21 W, bracket heat break 35 W through four mica pads (0.25 W/K) and plunger 12 W, 103 W in all [G3]. The TRL 2 figure was about 80 W.
- **Warm-up.** With two 300 W bands (MMD-DDR-002) the barrel zone reaches 220 °C in 12.3 min and the nozzle zone in 6.6 min [G4]. R5 (15 min) is met on paper. The 250 W bands of v0.1 would take 14.9 min, 2.7 min longer [G4b].
- **Heater loading.** The 300 W bands run at 4.5 W/cm², well inside the roughly 7.7 W/cm² (50 W/in²) usual for mica bands [G5].
- **Load cell (change).** The plunger behaves as a fin: with its tip at 150 °C its top end reaches about 94 °C, too hot for a strain-gauge load cell. A 10 mm G-11 glass-epoxy spacer (88 K/W) under the cell keeps it at about 27 °C [G6]. The spacer is added to BOM item 4 (about $5).
- **Temperature control (R4).** Two PID loops with a 150 to 260 °C set range, a set point limit and an independent 280 °C cut-out meet R4 by design; the ±5 °C hold needs a test later.

## H. Melt soak, mold heat and cycle (R6)

- **Soak.** For the center of a 22 mm column to reach 180 °C with the wall at 220 °C takes 7.5 min as melt and 9.3 min as tamped flake [H1]. Each charge soaks for about two cycles, so cycles shorter than about 5 min would starve the melt.
- **Mold heat (finding).** Each shot puts 19.5 kJ into the 2.62 kg aluminum mold, 54 W at 6 min cycles. In still air the mold settles at about 92 °C and the 6 mm plaque needs 2.1 min to cool to 95 °C [H2]. With the mold cooling fan (BOM item 18, MMD-DDR-002) blowing on it through the shield side it settles at about 47 °C and needs 0.8 min [H3].

*Table 3. Cycle steps [H4, H5].*

| Step | Time |
| --- | --- |
| Load and tamp the fresh charge | 1.0 min |
| Bolt the mold and raise the table | 0.75 min |
| Inject in four ratchet pulls | 0.25 min |
| Hold | 0.5 min |
| Cool in the mold | 0.8 min (fan) or 2.1 min (still air, v0.1) |
| Lower, unbolt, open and eject | 1.0 min |
| Clean and reassemble | 0.75 min |
| **Cycle** | **5.1 min (fan), 5.2 min with the soak limit; 6.4 min (still air)** |

- **Throughput.** In still air the cycle would be 6.4 min, 9.4 parts per hour, with the plaque leaving a 92 °C mold barely below its ejection temperature [H4]. With the fan the cooling steps allow 5.1 min, but each fresh charge must soak about two cycles for 9.3 min, so the design cycle is 5.2 min, 11.6 parts per hour, with the mold near 47 °C [H5, H6]. R6 (8 per hour) is met on paper.

## I. Power and energy (R10)

- **Load.** 700 W of heaters, a 25 W duct fan, an 18 W mold fan and about 10 W of controls give 753 W: 3.3 A at 230 V and 6.3 A at 120 V [I1]. R10 is met on paper.
- **Energy.** A shot takes 6.3 Wh into the plastic and 13.4 Wh of losses and auxiliaries over a 5.2 min cycle, about 20 Wh, or 0.66 kWh per kg of parts [I2]. The barrel zone runs at about 26 % duty [I3].

## J. Fume hood (R13)

A flanged side hood with a 150 x 100 mm face, 100 mm from the funnel axis, needs about 124 m³/h for a capture velocity of 0.40 m/s; in a 100 mm duct that is 4.4 m/s [J1]. A 100 mm inline duct fan rated 170 m³/h or more of free air covers this with margin for 3 m of flexible duct. Fumes from the nozzle rise inside the shield and along the warm jacket to the hood; that path is assumed, not calculated. With the set point limit of 260 °C in both controllers and the written condition to run only under the hood or outdoors, R13 is met on paper.

## K. Mass and size (R9)

- **Mass (at risk).** Base plate 5.2 kg (8 mm, MMD-DDR-003), column 5.7 kg, arbor press head, ram and ratchet 8.0 kg (assumed), shelf 2.6 kg, barrel set and heaters 3.4 kg, plunger and load cell 1.0 kg, jacket and guard 1.0 kg, lift table plate 2.0 kg, mold set 3.0 kg, shield 0.9 kg, hood 0.6 kg, mold cooling fan and bracket 0.7 kg and hardware 1.0 kg, plus the parts added for construction: head mounting plate and screws 1.2 kg, shelf back plate 0.8 kg, plunger coupling, pin and spacer 0.3 kg, ratchet adapter 0.1 kg, lift screw and handwheel nut 1.0 kg, hood arm 0.2 kg, shield feet, hinges and latch 0.2 kg, jacket hangers 0.1 kg, plunger rest 0.3 kg and the torque-limiting socket 0.6 kg (assumed): 39.8 kg without the control box [K1], 0.2 kg under the 40 kg target set by MMD-DDR-002 (99 % of it) [K3]. With the head mass still assumed, R9 is **at risk**. The TRL 2 figure of 32 kg left out the bracket, the table and the mold bolts and had a lighter bracket.
- **Size.** The footprint is 320 x 260 mm and the handle reaches 1,094 mm above the bench at the highest start of a pull; the ram top is at 1,020 mm [K2]. Both meet R9.

## L. Cost (R14, R8)

The BOM has 21 lines, all priced: $684.00 with one mold, of which the press is $590.00, the test mold $94.00 and the fume extraction $48.00 [L1]. `budget_usd` is a hypothetical value-engineering target, not a spending limit (Amish, 2026-10-01; $520 since 2026-09-26, MMD-DDR-002):

- **Value-engineering target: USD 520. Estimated cost of the constructable design: USD 590 (USD 70 over the target)**, the press alone with molds counted as tooling [L2]. R14 is over the value-engineering target; the cost drivers and savings worth trying are in the design decisions register (MMD-DEC-001).
- **Press and one mold:** $684.00, $164.00 over the target; the mold is tooling outside it [L2].
- Without the fume extraction the press would be $542.00 [L2].

The mold at $94.00 meets R8 ($100) on an indicative price. MMD-DDR-002 added the mold cooling fan ($12.00, item 18). MMD-DDR-003 added $37.00 of parts for construction (line 19, the shelf back plate and cap screws, the shield's hinges and latch) and $4.00 of mold screws, inserts and dowels. The decisions of 2026-10-02 added $46.00: the plunger rest (line 20, $6.00, an estimate by parts: tube and flat bar offcuts about $3, two M6 rivnuts and screws about $2, welding and cutting about $1) and the torque-limiting socket (line 21, $40.00, an estimate at the midpoint of a $30 to $50 retail band for a 1/2 in drive torque limiter).

## M. Results against every requirement

*Table 4. Requirement status from this note [M].*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R14 | Affordable | $590 press, $70 over the target; $684 with one mold | Press at or under the $520 value-engineering target, molds as tooling | **Over the value-engineering target** |
| R9 | Bench size and mass | 320 x 260 mm; 1,094 mm; 39.8 kg | 350 x 300 mm; 1.1 m; 40 kg | **At risk** (mass) |
| R2 | Shot size | 34.2 g ideal; about 25 g if the fresh charge is loose flake | 30 g or more | **At risk** |
| R3 | Injection pressure | 8.9 MPa at 0.60 efficiency (12.4 MPa at 0.84); fill needs about 4.8 MPa in 10 s | 8 MPa at 250 N or less | Met on paper |
| R5 | Warm-up | 12.3 min (barrel zone, 2 x 300 W) | 15 min or less | Met on paper |
| R6 | Throughput | 11.6 per hour with the mold fan, mold about 47 °C | 8 per hour or more | Met on paper |
| R7 | Mold envelope | 45 cm² at 8.9 MPa; stacks 30 to 120 mm; 170 x 126 mm table | 150 x 120 mm, 40 to 120 mm stack, 40 cm² | Met on paper |
| R8 | Low-cost tooling | $94 (indicative) | $100 or less | Met on paper |
| R10 | Power supply | 753 W; 6.3 A at 120 V | 1 kW or less; 10 A or less at 120 V | Met on paper |
| R11 | Touch-safe surfaces | Jacket skin 48 °C; nozzle zone shield added | 60 °C or less; nozzle and mold zone guarded | Met on paper |
| R13 | Fume control | Hood and fan, 124 m³/h; set point limit 260 °C | Exhaust hood or outdoors; set points above 260 °C blocked | Met on paper |
| R1 | Safe thermoplastics | HDPE, PP, LDPE and PS within 150 to 260 °C from injection-molded items; PVC and bottle-grade HDPE excluded by label and procedure | Four resins, injection grade; PVC excluded | Met by design |
| R4 | Temperature control | Two PID zones, 150 to 260 °C set range, set point limit, 280 °C cut-out | 150 to 260 °C, ±5 °C; cut-out above 280 °C | Met by design |
| R12 | Electrical safety | Earthed frame, fused inlet, double-pole switch, RCD or GFCI, 250 °C wiring | As listed | Met by design |
| R15 | Garage-buildable | Only the barrel set and molds need a lathe or mill (local shop) | Hand tools, drill press, optional welding | Met by design |
| R16 | Repeatable parts | Needs hardware | Mass within ±3 % over 10 shots | Not verifiable at TRL 3 |

Counts: 0 not met, 2 at risk, 8 met on paper, 4 met by design, 1 not verifiable at TRL 3; R14 over the value-engineering target.

## Checks against the TRL 2 figures

| TRL 2 claim (MMD-PRC-001 v0.2) | This note | Action |
| --- | --- | --- |
| About 34 g per shot | 34.2 g ideal; about 25 g with an untamped charge | Stands; tamping made part of the process |
| One steady pull drives the plunger 120 to 150 mm | 31.4 mm per 90° pull; 3.8 pulls | Ratchet handle added, precis corrected |
| About 8.9 MPa at 250 N, R3 met with about 10 % margin | 8.9 MPa at 0.60 (11 % margin); 12.4 MPa at 0.84 | Stands |
| 3 mm nozzle orifice | Needs up to 12.1 MPa to fill | 4 mm orifice and 5 to 7 mm sprue |
| About 45 cm² clamp limit | 45 cm² | Stands |
| Nozzle at 152 mm; 40 to 120 mm stacks | 120 mm stacks did not fit | Nozzle tip raised to 190 mm |
| 10 mm bracket plate | Yields at overload | 20 mm plate |
| Load cell on the plunger | About 94 °C | G-11 spacer added |
| Warm-up about 10 to 12 min | 14.8 min in v0.1; 12.3 min with 300 W bands and the constructable flange | 300 W bands (MMD-DDR-002) |
| Standing losses about 80 W | 103 W | Precis updated |
| About 6 min per shot, 10 per hour | 6.4 min in still air (mold about 92 °C); 5.2 min, 11.6 per hour with a fan | Mold cooling fan (MMD-DDR-002) |
| About 600 W | 753 W with 300 W bands and both fans | Precis updated |
| About 14 Wh per shot, 0.5 kWh per kg | About 20 Wh, 0.66 kWh per kg | Precis updated |
| About 32 kg | 39.8 kg with the fan, the parts added for construction, the plunger rest and the torque-limiting socket | R9 target 40 kg (MMD-DDR-002); at risk |
| Handle knob about 1.06 m | 1,094 mm at the start of a pull | Precis updated |
| $399 press, $489 with one mold | $590 press, $684 with one mold | Value-engineering target $520; $70 over (MMD-DDR-003 and the decisions of 2026-10-02) |
