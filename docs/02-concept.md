---
doc_id: MMD-PRC-001
title: MicroMold design precis
project: MicroMold
doc_type: Design precis
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (architecture, components, first-order numbers, design choices, safety, open questions, media)
---

# MicroMold design precis

## Summary

MicroMold is a bench-top, hand-operated plunger injection press for recycled HDPE, PP, LDPE and PS. The rack-and-pinion head of a 1 t arbor press, mounted on a taller steel column, drives a 22 mm plunger down a vertical steel barrel heated by two 250 W band heaters. Melt leaves a heated nozzle into a two-plate aluminum mold that a screw lift table holds against the nozzle. First-order numbers suggest a shot of about 34 g at about 9 MPa (90 bar) with 250 N on the handle, a warm-up of about 12 min and about 10 parts per hour, from about 600 W of single-phase power. The press costs about $399 in parts and about $489 with one mold, which is over the $400 budget. All figures are estimates.

![MicroMold on a workbench](../media/hero.png)

*Figure 1. MicroMold on a 0.9 m workbench with a 1.75 m person for scale. Plunger raised for loading. Massing model.*

## How it works

1. **Heat.** Two PID controllers drive the barrel zone (two 250 W band heaters) and the nozzle zone (a 100 W band heater) to the set point for the resin, for example 210 °C for HDPE. An insulation jacket and a perforated guard keep the outer surface near 50 °C.
2. **Load.** With the plunger raised, the operator pours washed, dried flake into the funnel at the top of the barrel and tamps it down with the plunger in two or three top-ups, because loose flake has about a third to a half of the density of melt.
3. **Soak.** The fresh charge melts above the melt left from the last shot. The barrel holds about two shots, so each charge has at least one cycle to melt through.
4. **Clamp.** The operator bolts the two mold plates together, sets the mold on the lift table and turns the screw until the sprue bushing seats on the nozzle.
5. **Inject and hold.** A steady pull on the handle drives the plunger 120 to 150 mm and fills the cavity. The operator holds pressure for about 30 s while the gate freezes. A load cell under the ram shows plunger force, so the melt pressure (force divided by 380 mm² of plunger area) can be read and logged.
6. **Cool and eject.** The mold is lowered, cooled for one to two minutes, unbolted and opened. Sprue and purge go back to the regrind bin.

![Material flow per shot](../media/flow.png)

*Figure 2. Material flow per shot for the 30 g reference part. All values are estimates: about 2 g of purge and drool and 4 g of sprue return to regrind.*

## Main components

Table 1. Main components. Numbers match `bom/bom.csv` and Figure 4.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Base plate | 320 x 260 x 12 mm steel, bolted to the bench | Carries the column and the mold clamp |
| 2 | Column and drive head | Rack-and-pinion head, pinion and 450 mm handle from a 1 t arbor press, on an 80 x 60 x 3 mm steel tube column about 0.9 m tall | Proposed drive, awaiting Amish (see design choices) |
| 3 | Rack ram | From the arbor press, 28 mm square | Needs about 150 mm of travel; to be checked on the chosen press |
| 4 | Plunger load cell | 10 kN (1 t) compression cell with HX711 amplifier and display | Reads plunger force; pressure indication |
| 5 | Plunger | 22 mm ground steel rod, 200 mm | Close sliding fit in the bore; no seal |
| 6 | Heated barrel | 42 mm steel bar bored and honed to 22 mm, 260 mm long, loading funnel on top | Only lathe part besides the nozzle |
| 7 | Band heaters | Two 250 W mica band heaters, 42 mm ID x 50 mm | Barrel zone, one PID loop |
| 8 | Nozzle and nozzle heater | Steel nozzle with 3 mm orifice, radiused tip; 100 W band heater | Second PID loop; stops the nozzle freezing |
| 9 | Barrel bracket and heat break | Steel plate clamping the barrel flange to the column, with mica washers | Carries the full plunger reaction into the column |
| 10 | Insulation jacket and guard | 25 mm mineral wool in an aluminum skin, perforated steel guard | Keeps the outer surface near 50 °C |
| 11 | Mold clamp | Screw jack and lift table, 170 x 130 mm | Seats the sprue bushing on the nozzle |
| 12 | Aluminum mold set | Two 6061 plates, 120 x 90 x 45 mm each, four M10 bolts, sprue bushing | First mold: test plaque (proposed) |
| 13 | Control box | Two PID controllers, two 25 A SSRs on a heat sink, fused IEC inlet, double-pole switch, independent thermal cut-out, force display | Mains enclosure; earthed |
| 14 | Heater and sensor wiring | High-temperature wire in glass-fiber sleeving, two K-type thermocouples | 250 °C rated at the barrel |

Item 15 (hardware and consumables) is in the BOM but not modeled.

![Cutaway](../media/cutaway.png)

*Figure 3. Section through the injection axis: drive head and ram at the top, load cell (purple), plunger raised above the funnel, barrel with the two band heaters inside the jacket and guard, nozzle (gold) seated on the mold, and the lift table on the base plate.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions are stated in each row and in MMD-REQ-001.

Table 2. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Plunger area | 380 mm² | 22 mm bore | |
| Swept volume per shot | about 46 cm³ | 120 mm usable of 150 mm stroke; the rest is lost to compressing the melt and closing gaps | |
| Shot mass | about 34 g HDPE | 46 cm³ at a melt density of about 0.75 g/cm³ | R2 met |
| Drive ratio | about 22:1 | 450 mm handle on a pinion of about 20 mm pitch radius | |
| Plunger force | about 3.4 kN | 250 N on the handle x 22.5 x 60 % efficiency | Within the 1 t (9.8 kN) press rating |
| Melt pressure | about 8.9 MPa (89 bar, 1,290 psi) | 3.4 kN on 380 mm²; about twice the 45 bar of the Precious Plastic lever machine ([Precious Plastic Academy](https://onearmy.github.io/academy/build/injection)) | R3 met, about 10 % margin |
| Mold clamp limit | about 45 cm² projected area | Four M10 bolts at about 20 kN preload, safety factor 2, against 8.9 MPa | R7 met; the 32 cm² reference part fits |
| Barrel and nozzle mass | about 2.7 kg steel | Barrel 2.05 kg, nozzle, funnel and flange about 0.6 kg | |
| Warm-up to 220 °C | about 10 to 12 min | 2.7 kg x 0.49 kJ/(kg K) x 200 K = 260 kJ at about 540 W net | R5 met |
| Heat to melt one shot | about 6.3 Wh (23 kJ) | 36 g HDPE, cp about 2.3 kJ/(kg K) over 185 K plus about 205 kJ/kg to melt the crystalline fraction (typical values) | |
| Standing losses at 220 °C | about 80 W | Jacket about 22 W by conduction through 25 mm mineral wool; funnel, nozzle and bracket about 60 W | Outer jacket about 48 °C: R11 met on paper |
| Cycle time | about 6 min | Load and tamp 1 min, soak overlapped with the previous cycle, inject and hold 0.5 min, cool 1.5 to 2 min, open, eject and reassemble 1.5 to 2 min | R6 met on paper (10 per hour); melt soak unverified |
| Energy per shot | about 14 Wh | 6.3 Wh into the plastic plus 8 Wh of standing loss over 6 min | About 0.5 kWh per kg of parts |
| Electrical load | about 600 W; 2.6 A at 230 V, 5 A at 120 V | 2 x 250 W barrel, 100 W nozzle | R10 met |
| Mass | about 32 kg without the control box | Base 7.8, column 5.9, arbor press head and ram about 8, barrel set 2.7, mold 2.6, clamp 2, guard 1, other 2 kg | R9 met |
| Size | 320 x 260 mm base; handle knob about 1.06 m above the bench at rest | Model | R9 met |
| Parts cost | about $399 for the press; about $489 with one mold | Indicative prices, see `bom/bom.csv` | R14 **not met** |

## Key design choices

All are proposed, awaiting Amish.

- **Drive: rack and pinion from an arbor press.** Options: (a) a simple lever, as in the Precious Plastic machine, which is cheapest but gives a short stroke or low force at a bench size; (b) the rack, pinion and handle from a 1 t arbor press on a taller column, which gives a long stroke and about 22:1 advantage from one bought part; (c) a screw press, which gives high, steady pressure but injects slowly, so the melt can freeze in the nozzle. Recommendation: (b), with (c) kept as a variant for small, thick parts.
- **Vertical barrel, mold below.** Gravity keeps the melt at the nozzle and the operator loads from the top. The mold is changed at bench height. Recommendation: vertical.
- **Plunger, not screw.** A reciprocating screw would mix and melt better but needs a motor, gearbox and a much more complex barrel. Recommendation: plunger for the first build.
- **Two heat zones.** A separate nozzle zone stops the nozzle freezing between shots at the cost of a second PID and SSR (about $15). Recommendation: two zones.
- **Bolted two-plate aluminum molds on a lift table.** Bolts are slow but cheap, and hold about 45 cm² of projected area at full pressure. A toggle clamp frame would be faster and cost about $40 more. Recommendation: bolts for the first mold, toggle clamp as an upgrade.
- **Load cell for pressure indication.** A load cell under the ram gives a number for each shot, which helps a group learn settings and record them. A spring-scale reading on the handle would save about $25. Recommendation: load cell.
- **First mold: a test plaque.** A 64 x 50 x 6 mm plaque (about 30 g) shows fill, shrinkage and surface quality and can be cut into test bars. Product molds follow co-design. Recommendation: test plaque first.
- **Budget.** Options: (a) keep $400 and count molds as tooling outside the machine budget (the press alone is about $399, with no margin); (b) raise the budget to about $500 to include one mold; (c) cut the load cell and nozzle zone to reach about $450 with a mold. Recommendation: (a), and report the mold cost separately. `project.yaml` is unchanged at $400.
- **Fume control.** Options: a small hood with a duct fan (about $40 to $60) in the BOM, or a written condition to run under existing extraction or outdoors. Recommendation: add the hood at TRL 3 and keep the written condition.

![Exploded view](../media/exploded.png)

*Figure 4. Exploded view with BOM numbers.*

## Safety

> **Safety:** MicroMold combines mains voltage, surfaces and molten plastic at up to 260 °C, stored pressure in the melt, a long lever and plastic fumes. It is a concept for a supervised workshop, not a consumer appliance.

- **Hot surfaces and melt.** The barrel, nozzle, mold and purge reach 180 to 260 °C, and molten plastic sticks to skin. Guard the barrel, keep the nozzle zone behind a shield, wear heat-resistant gloves, long sleeves and eye protection, and never look down the barrel.
- **Pressure.** Trapped melt can spit from the nozzle or the parting line when the plunger is pushed or when a cold plug lets go. Keep the nozzle pointed into the mold or a purge tray, and keep faces away from the axis.
- **Fumes.** Process only HDPE, PP, LDPE and PS within their published ranges. Never heat PVC, which releases hydrogen chloride, or unknown and mixed plastics ([Precious Plastic Academy](https://onearmy.github.io/academy/plastic/basics)). Overheated PS can release styrene. Work under local exhaust or outdoors (R13, not yet met). Set points above 260 °C are to be blocked.
- **Mains electricity.** Heaters run at mains voltage next to steel parts. Earth the frame and every metal part, use a fused inlet, double-pole switch and an RCD (30 mA) or GFCI supply, rate wiring at the barrel for 250 °C, and fit an independent thermal cut-out. Mains wiring must be done or checked by a qualified electrician to local electrical code.
- **Moving parts and lever.** The handle stores force and can spring back; the ram and pinion can pinch. Keep hands clear of the rack and fit a handle stop.
- **Fire.** Unattended heaters are a fire risk. Switch off at the inlet after use; keep flake and rags away from the barrel.
- **Product use.** Recycled parts of unknown history are not suitable for food contact, toys for young children, medical or safety-critical uses.

## Open questions for TRL 3

- How long does fresh flake take to melt through in a 22 mm bore, and does the two-shot reservoir give enough soak at 6 min cycles? This sets R6.
- Ram travel and rack strength of real 1 t arbor presses: is 150 mm available, or is a longer rack needed?
- Plunger clearance: what diametral gap stops backflow of HDPE and PP melt at 9 MPa without galling?
- Nozzle and sprue geometry for a hand-held injection speed, and the best nozzle temperature for each resin.
- Mold design rules for the group's own machinists: draft, venting, gate size, ejection and cooling time.
- Hood and fan sizing for fume capture at the funnel and nozzle.
- Which first products would sell locally? This needs a co-design partner.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
