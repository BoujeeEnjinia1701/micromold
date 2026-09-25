---
doc_id: MMD-REQ-001
title: MicroMold requirements
project: MicroMold
doc_type: Requirements
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
  change: First measurable requirements for TRL 2, with status against first-order estimates
---

# MicroMold requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see MMD-PRB-001). The status column compares each target with the first-order estimates in MMD-PRC-001; "met" means met on paper by an estimate, not demonstrated.

The **reference part** used throughout is a 30 g HDPE test plaque with a 64 x 50 mm projected area, molded from washed, dried flake of 3 to 8 mm.

Table 1. Requirements.

| ID | Requirement | Target | Status (estimate) | Verification (TRL 3 or later) |
| --- | --- | --- | --- | --- |
| R1 | Process the safe recycled thermoplastics | HDPE, PP, LDPE and PS flake of 3 to 8 mm; PVC excluded by procedure and labeling | Met by design | Design review; material trials later |
| R2 | Shot size | 30 g or more of HDPE per injection | Met: about 34 g | Swept-volume calculation |
| R3 | Injection pressure | 8 MPa (80 bar) or more at the melt with 250 N or less on the handle | Met, thin margin: about 8.9 MPa | Force and friction calculation; later load cell reading |
| R4 | Temperature control | Barrel and nozzle zones each settable from 150 to 260 °C, held within ±5 °C at the thermocouple; independent cut-out above 280 °C | Met by design, unverified | Controller and heater datasheets; thermal model |
| R5 | Warm-up | Cold start to 220 °C in 15 min or less | Met: about 12 min | Heat capacity calculation |
| R6 | Throughput | 8 or more reference parts per hour with one mold | Met on paper: about 10 per hour; melt soak time is the main uncertainty | Cycle-time estimate; later timed trials |
| R7 | Mold envelope | Molds up to 150 x 120 mm footprint and 40 to 120 mm stack height; 40 cm² or more projected area at full pressure | Met: about 45 cm² with four M10 bolts | Clamp force calculation |
| R8 | Low-cost tooling | A two-plate aluminum mold for the reference part machinable on a manual mill or small CNC for $100 or less | Met: about $90 (indicative) | Quotation from a local shop |
| R9 | Bench size and mass | Press footprint 350 x 300 mm or less, top of handle 1.1 m or less above the bench, mass 35 kg or less without the control box | Met: 320 x 260 mm, about 1.06 m, about 32 kg | Model and mass estimate |
| R10 | Power supply | Single-phase 230 V or 120 V, 1 kW or less, 10 A or less at 120 V | Met: about 600 W, 2.6 A at 230 V, 5 A at 120 V | Heater ratings |
| R11 | Touch-safe outer surfaces | Guard and jacket 60 °C or less at 220 °C set point and 25 °C ambient; nozzle and mold zone guarded | Met on paper for the jacket; nozzle zone guard not yet designed | Thermal calculation |
| R12 | Electrical safety | Earthed frame, fused inlet, double-pole switch, RCD or GFCI supply, heaters and wiring rated for 250 °C at the barrel | Met by design, unverified | Design review against IEC 60204-1 principles |
| R13 | Fume control | Operation only under a local exhaust hood or outdoors; set points above 260 °C blocked in the controller | Not met: no extraction in the concept or BOM | Design review |
| R14 | Affordable | Parts for the press and one mold $400 or less | **Not met: about $489** (press alone about $399) | Priced BOM (`bom/bom.csv`) |
| R15 | Garage-buildable | Everything except the barrel and the mold built with hand tools, a drill press and optional welding | Partly met: the barrel needs a lathe and the mold a mill, both from a local shop | Build sequence review |
| R16 | Repeatable parts | Part mass within ±3 % over 10 consecutive shots | Unknown at TRL 2 | Later bench trials (TRL 4, not in the current phase) |

## Assumptions

- HDPE melt density about 0.75 g/cm³ at 200 to 220 °C; solid density about 0.95 g/cm³ (typical handbook values, estimates).
- Arbor press drive: pinion pitch radius about 20 mm, handle 450 mm long, overall efficiency of rack, guides and plunger about 60 % (estimates to be checked on the chosen press).
- Processing temperatures follow published melt ranges: HDPE 190 to 230 °C, PP 200 to 240 °C, LDPE 220 to 245 °C, PS 180 to 260 °C ([RJC Mold](https://rjcmold.com/guides/plastic-melting-point-chart)).
- Four M10 class 8.8 bolts preloaded to about 20 kN each clamp the mold plates, with a safety factor of 2 against melt pressure opening the parting plane.

## Requirements not met

- **R13 fume control:** the concept has no extraction. Proposed, awaiting Amish: add a small hood with a duct fan (about $40 to $60) or make outdoor or hooded operation a written condition of use.
- **R14 cost:** about $489 with one mold against $400. See the budget options in MMD-PRC-001.
- **R15 garage-buildable:** partly met; the barrel and molds depend on a local machine shop.
- **R3** is met by a margin of about 10 %, which depends on the assumed drive efficiency.
