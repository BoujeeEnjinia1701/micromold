---
doc_id: MMD-DDR-001
title: MicroMold TRL 2 review decisions
project: MicroMold
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations for items D1 to D10 are adopted for TRL 3 work pending Amish's review; items O1 to O2 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish", each with options and a recommendation, and MMD-PRC-001 v0.2 listed the same key design choices. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's items one by one. Every item that carries a recommendation is therefore adopted as recommended for TRL 3 under that instruction and stays open for his review. Items without a recommendation stay open.

MicroMold uses none of the batch's shared components (FieldNode, CellGuard, MotionCore, ThermaCart, TwinKit, CalRig), so no cross-repo interface applies.

## Options considered

The options for each item are those in `docs/REVIEW.md` (session 2026-09-25, /populate) and in MMD-PRC-001 v0.2, Key design choices.

## Decision

*Table 1. Items adopted for TRL 3.*

| # | Item | Recommendation adopted |
| --- | --- | --- |
| D1 | Drive | Option (b): the rack, pinion and head of a 1 t arbor press on a taller steel column, with a screw press kept as a variant for small, thick parts. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D2 | Layout | Vertical barrel with the mold below. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D3 | Injection | A plunger rather than a reciprocating screw for the first build. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D4 | Heating | Two PID zones, barrel and nozzle. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D5 | Mold clamping | Bolted two-plate molds on a screw lift table, with a toggle clamp frame as a later upgrade. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D6 | Pressure indication | A 10 kN load cell under the ram rather than a spring-scale reading on the handle. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D7 | First mold | A 64 x 50 x 6 mm test plaque; product molds after co-design. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D8 | Budget | Option (a): keep $400 and count molds as tooling outside the machine budget, reporting the mold cost separately. This redefines what the budget covers, so R14 in MMD-REQ-001 now reads "parts for the press, excluding molds, $400 or less", and R8 covers the mold. `budget_usd` in `project.yaml` is unchanged at $400; no new figure was recommended. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D9 | Fume control | Both: a small side hood with a duct fan in the BOM, and a written condition to run only under extraction or outdoors. Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |
| D10 | First co-design partner type | A group that already shreds HDPE or PP (for example a Precious Plastic workspace, a waste picker cooperative or a technical college that does). Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | The specific first co-design partner and its city or region. D10 sets only the type of group; no partner or place was recommended. | Proposed, awaiting Amish |
| O2 | First product molds after the test plaque. These depend on what sells locally, which must come from co-design; no recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields change. No pitch or problem rewording was recommended, and the rack-and-pinion drive is a lever-driven press, so the pitch ("a lever or screw press") still holds. `budget_usd` stays at $400.
- MMD-PRB-001, MMD-PRC-001 and MMD-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed"; they are adopted for TRL 3 pending Amish's review. R14 is redefined (D8), and R13 now names the hood as well as the written condition (D9).
- The TRL 3 calculations (MMD-CAL-001) led to design changes within these items, also open for Amish's review: a ratchet handle on the pinion (D1), a 4 mm nozzle orifice and a 5 to 7 mm tapered sprue (D7), a glass-epoxy thermal spacer under the load cell (D6), a 20 mm bracket plate on mica pads, a nozzle zone shield and a nozzle tip raised to 190 mm so that 120 mm mold stacks fit (D5). With the hood, they bring the press to $495, over the $400 budget even under the redefined scope. New items raised by the calculations (budget, mass target, heater rating, mold cooling and feedstock grade) are listed in `docs/REVIEW.md` as "Proposed, awaiting Amish".
