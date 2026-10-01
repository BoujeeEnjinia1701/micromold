---
doc_id: MMD-DEC-001
title: MicroMold design decisions register
project: MicroMold
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# MicroMold design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | The design changes made for construction | Accept, or change any of P1 to P15 | Accept | Every component; the build plan is drawn to them | MMD-DDR-003, Table 1 |
| 2 | How flake is loaded: with the plunger raised its tip is only 8 mm above the funnel rim | (a) pull the ball-lock pin and lift the plunger out to load, refit it to tamp and inject; (b) a press with 40 mm more ram travel and a taller column (handle top about 1,134 mm, over R9); (c) a side loading chute | (a): no new part; the plunger's top end is about 94 °C, handled in the gloves already required | The operating procedure; nothing in the build changes for (a) | MMD-DDR-003, A1 |
| 3 | The lift screw needs a 25 mm hole through the bench and drops up to 50 mm below it | (a) accept; (b) a 60 mm riser frame under the base plate (handle top over 1.1 m) | (a) | Step 13 (bench hole) | MMD-DDR-003, A2 |
| 4 | Handle stop or pull limit against overload (a 700 N pull gives about 35 MPa, 1.35 times the press rating) | (a) a stop on the ratchet arc; (b) a torque-limiting socket on the ratchet adapter; (c) written procedure and the shield only | (b): it limits force whoever pulls | Ratchet adapter (section 3.6) | MMD-DDR-003, A3; `docs/REVIEW.md`, TRL 3 safety concerns |
| 5 | The specific first co-design partner and its city or region | Any group that already shreds HDPE or PP (D10) | None yet | Not part of the TRL 3 build; needed at TRL 4 | MMD-DDR-001, O1 |
| 6 | First product molds after the test plaque | To come from co-design | None yet | A new mold sketch per product; the press is unchanged | MMD-DDR-001, O2 |
| 7 | Appearance model differences from the engineering model (2026-09-26): round duct stub, guide rods under the table, perforated shield window, full mold bolts, control box front, illustrative display values | Accept each, or change the appearance model | Accept 1, 3, 5 and 6 (the build plan also uses a round stub); for 2 and 4 the constructable design differs (no guide rods; cap screws, no nuts), so update the appearance model to it | The renders only, not the build | `docs/REVIEW.md`, 2026-09-26, items 1 to 6 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The arbor press: a 28 mm ram 255 mm or longer with 150 mm of engaged travel; a head that can be cut from its frame with a flat back face and enough metal for four M10 holes 20 deep; the head's mass (8 kg assumed) | Sets the stroke, the head fixing and R9's mass margin (1.0 kg) | MMD-DDR-003, P1; MMD-CAL-001 [K1] |
| 2 | The press's lever hub: its outside diameter and bore, to take the welded square drive | The ratchet adapter is made from it | MMD-DDR-003, P13 |
| 3 | The load cell is about 56 mm across, has a top M12 stud and a base flange with three M5 through holes (46 mm circle assumed) | The spacer's tapped holes are drilled to match it | MMD-DDR-003, P6 |
| 4 | The handwheel's hub takes a Tr20 x 4 nut (about 36 mm across) | The handwheel nut is made from it | MMD-DDR-003, P7 |
| 5 | The mold cooling fan's corner holes are on a 105 mm square | The fan bracket's holes | MMD-DDR-003, P10 |
| 6 | The nozzle heater band fits a 24 mm body and is no more than 18 mm wide | The nozzle body length | MMD-DDR-003, P4 |
| 7 | The bench top's thickness and the clear space under it (60 mm or more below the hole) | The lift screw drops through it | MMD-DDR-003, P7 |

## Value engineering

Value-engineering target: USD 520 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 544 for the press (USD 24 over the target); USD 638 with the test mold, which is tooling outside the target (USD 94, R8). Main cost drivers and savings worth trying:

- The largest lines are the arbor press head with column tube and ratchet (USD 110), the control box (USD 55), the fume hood and duct fan (USD 48), the barrel (USD 45), the load cell and display (USD 35) and the lift table, screw and handwheel (USD 30).
- Making the design constructable added USD 37: the construction parts of line 19 (USD 30: head mounting plate and screws, plunger coupling and ball-lock pin, ratchet adapter, hood arm and rivnuts), the bracket's back plate and cap screws (USD 4) and the shield's hinges and latch (USD 3). The mold rose USD 4 for screws, inserts and dowels.
- Savings worth trying: a used arbor press (often under half the new price); counting the duct fan and duct (USD 48) as workshop extraction shared with other machines, as the molds are counted as tooling, which would bring the press to USD 496; buying the two PID controllers and relays as a pre-wired dual-zone controller; and a ball-lock pin replaced by a plain clevis pin and R-clip (about USD 4 less).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D10: rack-and-pinion drive from a 1 t arbor press on a taller column, vertical barrel with the mold below, plunger injection, two PID zones, bolted two-plate molds on a screw lift table, 10 kN load cell, test plaque first, molds as tooling, side hood with duct fan, a partner that already shreds HDPE or PP | Amish: "i accept all your recommendations, go with them across all repos." | MMD-DDR-001, MMD-DDR-002 |
| 2026-09-25 | N1 to N5: budget USD 500 for the press, 40 kg mass target, two 300 W barrel bands, a mold cooling fan, injection-grade flake only | Amish, same instruction | MMD-DDR-002 |
| 2026-09-26 | Budget USD 520 to cover the priced BOM (O3, option (a)) | Amish: "i approve all the budget items." | MMD-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable as the build plan is drawn; changes recorded as draft for review | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | MMD-DDR-003 (its changes are open, item 1 above) |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it." | This register |
| 2026-10-01 | `budget_usd` is a hypothetical value-engineering target, not a spending limit | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register; MMD-REQ-001 R14 |
