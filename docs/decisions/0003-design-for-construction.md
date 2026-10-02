---
doc_id: MMD-DDR-003
title: MicroMold design for construction
project: MicroMold
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: Accepted by Amish on 2026-10-02 with P1 to be confirmed against the bought press before cutting, including the recommendations for A1 to A3 (plunger rest added to A1)
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted, with one condition. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations in Table 3 (A1 to A3), which are now decided as recommended and recorded in the design decisions register (MMD-DEC-001). Condition: P1 (cutting the head from the arbor press casting and tapping four M10 holes in its back) is confirmed against the bought press before it is cut. A1 adds a plunger rest on the column, and A3 adds a torque-limiting socket on the ratchet adapter; neither is in the model yet.

## Context

On 2026-09-30 Amish asked for every repo to have a build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of MicroMold (MMD-DDR-001 and MMD-DDR-002) showed what the press does but was a massing model: several parts overlapped, floated or had no fixing, and the screw lift could not fit where it was drawn.

The model was checked with build123d: every pair of components for shared volume, every pair that must touch for contact, the gaps that must stay open, the plunger at full stroke and the lift table at both ends of its travel. The changes below fix every problem found and keep what the press does: the same drive, ratio, stroke, bore, shot, heaters, nozzle position, mold, stack range, shield, hood and fan. Every change is in `cad/src/model.py`, which now runs 155 constructability checks, including the assembly order (`python cad/src/model.py --check`); all pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The arbor press head overlapped the column by 30 mm and had no fixing. A 1 t arbor press is one casting, frame and head together. | The head is cut from its frame and bolted to an 8 mm head mounting plate (120 x 140 mm) welded to the column front, flush with its top, by four M10 countersunk screws into holes drilled and tapped 20 mm deep in the casting's back face. The screw heads sit flush against the column; four 22 mm holes through the column's front and back walls let a hex key reach them. The head now sits 2 mm further forward (its back face at the plate); the ram axis is unchanged. | The plate takes the head's reaction into the column corners, not its thin front wall. Countersunk screws keep the plate flat on the column, and the access holes let the head come off for repair. |
| P2 | The barrel bracket cut 3 mm into the column wall, was fixed only along the 3 mm front wall (which would bend under the 13.2 kN overload), and the flange's mica pads were not in the stack, so the flange sat directly on the steel. | The bracket is now a 20 mm shelf (110 x 150 mm) whose back edge is welded to the column face, plus an 8 mm back plate (110 x 120 mm) welded on the shelf and down both column corners. Four 15 x 15 x 3 mm mica pads sit between the shelf and the flange; the shelf top is 3 mm lower to suit. | The back plate turns the shelf's bending into a couple carried by welds on the column's side walls. The mica pads are now in the stack, as the heat-break calculation assumes. |
| P3 | The flange had no fixing, and its 80 mm diameter left no room for screws inside the funnel. | Flange 100 mm across with four M8 cap screws on an 82 mm circle into tapped holes in the shelf, with mica washers under the heads; funnel 64 mm across (was 80 mm) so a hex key reaches the screws. | The screws only hold the barrel down; the injection load goes through the pads. The narrower funnel still takes flake from a scoop. |
| P4 | The nozzle had no joint to the barrel; it just stood under it. | The nozzle screws into an M30 x 1.5 thread, 15 mm deep, in the barrel's lower end, with a 27 mm hex to tighten it; its 18 mm bore meets the 22 mm barrel bore. The tip is a 12 mm spherical radius that seats in a 12.5 mm spherical seat, 2 mm deep, in the mold top. | A threaded nozzle can be removed for cleaning. The spherical seat locates the mold on the nozzle and seals at the centre, so the test mold now sits 2 mm higher (table at 102 mm). |
| P5 | The jacket and guard floated round the barrel, and as one sleeve it could not be fitted: the barrel goes in from above through the shelf, and a sleeve cannot pass the nozzle from below. | Two half shells, front and back, that close round the barrel; each hangs on two 2 mm tabs, each on a 14 mm spacer and an M5 screw into the underside of the shelf. | Hangs the jacket from a cool part, clear of the barrel, the heaters and the nozzle, and lets it be fitted with the barrel in place. |
| P6 | The load cell, spacer and plunger were stacked with no fixings and no way to lift the plunger, and a screw through the glass-epoxy spacer would have carried heat round it. | The cell's M12 stud screws into the ram end. A plunger coupling (40 mm steel, a 22.2 mm socket 30 mm deep) hangs under a 56 mm glass-epoxy spacer on three low-head M5 screws whose heads sit in counterbores 1 mm below the spacer's top; the spacer hangs from the cell's flange on three M5 screws into blind tapped holes that stop 4 mm short of the coupling, so no metal crosses the spacer. The plunger hangs in the coupling on a 6 mm ball-lock pin through a 7 mm hole, which lets it float in line with the bore. | Keeps the thermal break the load cell needs and the floating coupling the column deflection needs. The stack is 5 mm taller; the handle top rises from 1,089 to 1,094 mm, still under the 1,100 mm limit (R9). |
| P7 | The screw lift could not be built as drawn: a 70 mm block with a crank and no mechanism, under a table whose lowest top is 60 mm above the bench. A screw jack with 100 mm of travel cannot collapse to the 50 mm between the base plate and the table. | A Tr20 x 4 screw, 150 mm long, is welded under the lift table. It runs through a handwheel nut that turns on a thrust washer on the base plate, and drops through a 25 mm hole in the base plate and the bench, up to 50 mm below the underside of a 40 mm bench. The table (now 126 mm deep) runs 2 mm in front of the column face, which stops it turning. | The only screw lift that keeps the 60 to 160 mm table range, the 120 mm stack (R7) and the nozzle height. The handwheel stays at the base, where it is reached under the closed shield front, as the concept's crank was. |
| P8 | The mold bolts ended in nuts under the lower plate, so the mold could not sit flat on the table. There was no way to line the plates up. | Four M10 x 70 cap screws into steel thread inserts in the lower plate; two 6 mm dowels; the sprue now tapers from 5 mm at the seat to 7 mm at the parting line (it was drawn the wrong way round). | The mold sits flat on the table and opens the same way each time. Inserts stop the aluminium threads wearing. |
| P9 | The shield sides started 52 mm above the bench with nothing holding them; the front had no hinge. | The sides stand on the base plate on 20 mm folded feet, two M6 screws each; the front hangs on two hinges on the left side and shuts on a latch; its bottom edge is 60 mm above the bench. | A fixed, removable guard; the handwheel is reached under the closed front. |
| P10 | The mold fan's bracket only touched the fan's lower edge. | A 3 mm plate bracket, 120 mm wide, behind the fan with a 112 mm intake hole and four M4 screws through the fan's corners; an 18 mm foot with two M6 screws into the base. The fan is 4 mm closer to the mold. | The fan is held on all four corners and can still draw air. |
| P11 | The fume hood floated beside the funnel. | An L-shaped hood arm of 30 x 5 mm flat bar: the short leg to the column's left face on two M6 rivnuts, the long leg to the hood's back on two M5 screws. | A tube wall cannot be reached from inside; rivnuts give it threads. |
| P12 | The heater wiring ran through the shield side. | Rerouted from the control box up and over the shield into the jacket. | Clears the guard and keeps the leads away from the mold zone. |
| P13 | The ratchet socket on the pinion shaft was not defined. | Ratchet adapter: the press's own lever hub with the square end of a 1/2 in drive extension welded to it, pinned to the shaft with a 6 mm roll pin. | No lathe work; the ratchet pushes onto a standard square drive. |
| P14 | Mass rose with the parts added for construction (40.7 kg against the 40 kg target). | Base plate 8 mm thick (was 12 mm); head and back plates 8 mm. | The base plate no longer carries the injection force (the force loop closes in the column), so 8 mm is enough for a bench-bolted press. The press is 39.0 kg [K1]. |
| P15 | Assembly order: the barrel's flange and band heaters cannot pass the shelf hole, so the barrel must go in from above; with the press head fitted there is too little room above the shelf. | The barrel, with its nozzle and nozzle heater, is lowered through the shelf before the press head is fitted; the band heaters clamp on afterwards; the plunger unit is assembled on the bench and screwed onto the ram as one piece. | Recorded in the build plan's step order; checked in the model. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 39.0 kg (was 39.2 kg) with the parts added for construction, 1.0 kg under the 40 kg target [K1]. R9 stays at risk: the 8 kg head is still an assumption. | Plates and fixings added; base plate thinner. |
| Cost | BOM lines 1, 9, 10, 11, 12, 16, 17 and 18 respecified, lines 9, 12 and 16 repriced, and line 19 added (construction parts, USD 30). Value-engineering target: USD 520. Estimated cost of the constructable design: USD 544 for the press (USD 24 over the target); USD 638 with the test mold [L1, L2]. | Parts added for construction. `budget_usd` is unchanged. |
| Heat | Flange 100 mm and funnel 64 mm: the barrel zone's steel is 0.72 kg (was 0.70 kg); warm-up 12.3 min (was 12.2 min) [G1, G4]. Standing losses unchanged at 103 W. | Follows the model. |
| Height | Handle top 1,094 mm (was 1,089 mm); ram top 1,020 mm [K2]. Test mold table at 102 mm (was 100 mm) [A5]. | Coupling and nozzle seat. |
| Drawing | MMD-DWG-001 Rev P4; making sketches MMD-DWG-101 to 114 added. | Follows the model. |
| Documents | MMD-CAL-001 v0.4, MMD-REQ-001 v0.6, MMD-PRC-001 v0.6. | Follows the model. |

*Table 3. Items that change what the press does, how it is installed or its safety case: proposed, then accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Loading. With the plunger raised its tip is only 8 mm above the funnel rim (the concept's stack), too little to pour flake under it. This changes how the press is used, so it is not made here. | (a) pull the ball-lock pin and lift the plunger out to load, then refit it to tamp and inject (the coupling already allows this); (b) a press with 40 mm more ram travel and a taller column (handle top about 1,134 mm, over R9's 1.1 m); (c) a side loading chute into the funnel. | (a): no new part. The plunger's top end runs at about 94 °C [G6], so it is handled in the heat-resistant gloves already required. Accepted 2026-10-02, with a simple plunger rest on the column so the hot plunger is never laid on the bench. |
| A2 | The lift screw drops through a 25 mm hole in the bench, up to 50 mm below a 40 mm bench top, so the press needs a bench it may drill. | (a) accept; (b) a 60 mm riser frame under the base plate, which raises the handle top over 1.1 m (R9). | (a). Accepted 2026-10-02. |
| A3 | Handle stop or pull limit. Recommended since TRL 3 (a 700 N pull reaches about 35 MPa and 1.35 times the press rating) but never decided, and not in the model. | (a) a stop on the ratchet arc; (b) a torque-limiting socket on the adapter; (c) rely on the written procedure and the shield. | (b): it limits force whoever pulls. Accepted 2026-10-02: the socket is set so the ram cannot exceed the press rating and is checked against the load cell at TRL 4. |

## Consequences

- Accepted by Amish on 2026-10-02 with the condition on P1. With A1 to A3 accepted: flake is loaded with the plunger lifted out and laid on a plunger rest on the column; the bench is drilled for the lift screw; a torque-limiting socket on the ratchet adapter limits the ram force to the press rating. The plunger rest and the socket are still to be added to the model, the BOM and the build plan.

- `design_state: constructable` in `project.yaml`. The build plan MMD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status (MMD-CAL-001 v0.4): none not met, 2 at risk (R2, R9), 8 met on paper, 4 met by design, 1 not verifiable at TRL 3, and R14 over the value-engineering target by USD 24.
- The appearance model `cad/src/product_model.py` and the photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept head position, flange, funnel, screw lift, mold bolts with nuts and fan bracket. They need updating on Amish's Mac, where Blender is.
- The arbor press is chosen at TRL 4: its ram length and travel, whether its head can be cut from the frame and drilled, and its mass must be checked then (design decisions register, items to confirm).
