---
doc_id: MMD-REQ-001
title: MicroMold requirements
project: MicroMold
doc_type: Requirements
version: "0.8"
status: Draft
date: '2026-10-03'
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
  change: First measurable requirements for TRL 2, with status against first-order estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from MMD-CAL-001; R14 redefined to the press excluding molds and R13 to name the hood (MMD-DDR-001 D8, D9)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from MMD-CAL-001 v0.4 for the constructable design (MMD-DDR-003); R14 measured against the value-engineering target
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: Figures brought into line with MMD-CAL-001 v0.5 - R9 mass 39.8 kg, R14 press USD 590 (USD 70 over the target); no requirement status changed
- version: "0.8"
  date: '2026-10-03'
  author: Amish Chadha
  change: "R9 mass margin of 0.2 kg and the 180 N m socket setting accepted by Amish on 2026-10-03"
---

# MicroMold requirements

These are the requirements for the concept, checked by calculation at TRL 3 in MMD-CAL-001. Targets are proposals for review, not yet validated with users, and will be revised after co-design sessions (see MMD-PRB-001). "Met on paper" means met by calculation, and "met by design" means met by a stated feature; neither is demonstrated on hardware. Two targets changed in v0.3 under MMD-DDR-001: R14 covers the press without molds (D8), and R13 names the hood (D9). Three more changed in v0.4 under MMD-DDR-002, decided by Amish on 2026-09-25: R1 requires injection-grade flake, R9 allows 40 kg (was 35 kg) and R14 allows $500 (was $400). In v0.5 R14 allows $520, the budget Amish approved on 2026-09-26 to cover the priced BOM (MMD-DDR-002). In v0.6 that figure is read as a hypothetical value-engineering target, not a limit (Amish, 2026-10-01), and status is from MMD-CAL-001 v0.4, for the constructable design of MMD-DDR-003.

The **reference part** used throughout is a 30 g HDPE test plaque, 64 x 50 x 6 mm, molded from washed, dried flake of 3 to 8 mm.

Table 1. Requirements.

| ID | Requirement | Target | Status (MMD-CAL-001) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Process the safe recycled thermoplastics | HDPE, PP, LDPE and PS flake of 3 to 8 mm from injection-molded items (caps, crates, buckets); bottle-grade HDPE and PVC excluded by procedure and labeling | Met by design (bottle grade would need about 24 MPa, CAL E6) | Design review; material trials later |
| R2 | Shot size | 30 g or more of HDPE per injection | **At risk:** 34.2 g ideal, about 25 g if the fresh charge is not tamped | Swept-volume calculation; later weighed shots |
| R3 | Injection pressure | 8 MPa (80 bar) or more at the melt with 250 N or less on the handle | Met on paper: 8.9 MPa at 0.60 drive efficiency (12.4 MPa at 0.84); fill needs about 4.8 MPa | Force and friction calculation; later load cell reading |
| R4 | Temperature control | Barrel and nozzle zones each settable from 150 to 260 °C, held within ±5 °C at the thermocouple; independent cut-out above 280 °C | Met by design, unverified | Controller and heater datasheets; later logging |
| R5 | Warm-up | Cold start to 220 °C in 15 min or less | Met on paper: 12.3 min with two 300 W bands | Heat capacity calculation; later timed start |
| R6 | Throughput | 8 or more reference parts per hour with one mold | Met on paper: 11.6 per hour with the mold cooling fan, mold about 47 °C (soak limited) | Cycle-time estimate; later timed trials |
| R7 | Mold envelope | Molds up to 150 x 120 mm footprint and 40 to 120 mm stack height; 40 cm² or more projected area at full pressure | Met on paper: 45 cm²; stacks of 30 to 120 mm fit | Clamp force calculation; model |
| R8 | Low-cost tooling | A two-plate aluminum mold for the reference part machinable on a manual mill or small CNC for $100 or less | Met on paper: $94 (indicative) | Quotation from a local shop |
| R9 | Bench size and mass | Press footprint 350 x 300 mm or less, top of handle 1.1 m or less above the bench, mass 40 kg or less without the control box | **At risk on mass:** 39.8 kg with an assumed 8 kg press head (0.2 kg margin accepted by Amish, 2026-10-03; 180 N m socket setting accepted the same day); 320 x 260 mm and 1,094 mm met | Model and mass estimate |
| R10 | Power supply | Single-phase 230 V or 120 V, 1 kW or less, 10 A or less at 120 V | Met on paper: 753 W, 6.3 A at 120 V | Heater and fan ratings |
| R11 | Touch-safe outer surfaces | Guard and jacket 60 °C or less at 220 °C set point and 25 °C ambient; nozzle and mold zone guarded | Met on paper: skin 48 °C; nozzle zone shield added | Thermal calculation |
| R12 | Electrical safety | Earthed frame, fused inlet, double-pole switch, RCD or GFCI supply, heaters and wiring rated for 250 °C at the barrel | Met by design, unverified | Design review against IEC 60204-1 principles |
| R13 | Fume control | A side hood with a duct fan at the funnel, and operation only under it or outdoors; set points above 260 °C blocked in the controller | Met on paper: about 124 m³/h | Hood calculation; design review |
| R14 | Affordable | Parts for the press, excluding molds (tooling, see R8), at or under the $520 value-engineering target (a hypothetical control target) | **Over the value-engineering target: $590, USD 70 over** ($684 with one mold) | Priced BOM (`bom/bom.csv`) |
| R15 | Garage-buildable | Everything except the barrel and the mold built with hand tools, a drill press and optional welding | Met by design: the barrel with its nozzle and the molds come from a local machine shop; the plunger is only cross-drilled | Build sequence review |
| R16 | Repeatable parts | Part mass within ±3 % over 10 consecutive shots | Not verifiable at TRL 3 | Later bench trials (TRL 4, not in the current phase) |

## Assumptions

- HDPE melt density about 0.75 g/cm³ at 200 to 220 °C; solid density about 0.95 g/cm³ (typical handbook values, estimates). The other property values are in MMD-CAL-001, Table 1.
- Arbor press drive: pinion pitch radius about 20 mm, 450 mm ratchet handle, design efficiency 0.60 (0.84 calculated), to be checked on the chosen press.
- Processing temperatures follow published melt ranges: HDPE 190 to 230 °C, PP 200 to 240 °C, LDPE 220 to 245 °C, PS 180 to 260 °C ([RJC Mold](https://rjcmold.com/guides/plastic-melting-point-chart)).
- Four M10 class 8.8 cap screws in thread inserts, preloaded to about 20 kN each, clamp the mold plates, with a factor of 2 against melt pressure opening the parting plane.

## Requirements not met or at risk

- **R14 cost:** value-engineering target: USD 520. Estimated cost of the constructable design: USD 590 (USD 70 over the target) for the press, with molds counted as tooling; USD 684 with the first mold. The parts added to make the design buildable account for USD 37 (MMD-DDR-003) and the plunger rest and torque-limiting socket for USD 46 (decisions of 2026-10-02); cost drivers and savings are in MMD-DEC-001.
- **R9 mass:** 39.8 kg against 40 kg, with an assumed 8 kg arbor press head; the margin depends on the real press.
- **R2 shot size:** met only if each top-up of flake is tamped with the press while loading.
- **R16** cannot be assessed until hardware exists (TRL 4, on hold).
