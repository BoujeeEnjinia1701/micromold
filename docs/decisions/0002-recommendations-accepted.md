---
doc_id: MMD-DDR-002
title: MicroMold recommendations accepted
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
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below with a recommendation is "Decided by Amish, 2026-09-25: go with recommendation". Items without a recommendation remain "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote, in chat: "i accept all your recommendations, go with them across all repos." This record lists every MicroMold item that carried a recommendation in `docs/REVIEW.md` (all sessions) or in MMD-DDR-001, what changed in the repo because of it, and the items still open. Where a recommendation offered several options, the recommended option is the decision. TRL 4 remains on hold by Amish's instruction, so any part of a decision that needs a build, a test, a measurement or purchasing is recorded here as decided but on hold. `trl` and `trl_target` stay at 3.

## Options considered

The options for D1 to D10 are in MMD-DDR-001 and `docs/REVIEW.md` (session 2026-09-25, /populate). The options for N1 to N5 are in `docs/REVIEW.md` (session 2026-09-25, TRL 3, "Still awaiting Amish", items 3 to 7).

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| D1 | Drive | Rack, pinion and head of a 1 t arbor press on a taller column; screw press kept as a variant. Includes the TRL 3 ratchet handle. | Wording only (MMD-DDR-001 v0.2, MMD-PRC-001 v0.4); design already in the model |
| D2 | Layout | Vertical barrel, mold below | Wording only |
| D3 | Injection | Plunger, not a reciprocating screw | Wording only |
| D4 | Heating | Two PID zones, barrel and nozzle | Wording only |
| D5 | Mold clamping | Bolted two-plate molds on a screw lift table; toggle clamp frame later. Includes the nozzle tip at 190 mm and the nozzle zone shield. | Wording only |
| D6 | Pressure indication | 10 kN load cell under the ram, on a G-11 spacer | Wording only |
| D7 | First mold | 64 x 50 x 6 mm test plaque; 4 mm nozzle and 5 to 7 mm sprue | Wording only |
| D8 | Budget scope | Molds are tooling outside the machine budget (R14 covers the press) | Wording only; the figure is set by N1 |
| D9 | Fume control | Side hood with a duct fan, plus a written condition to run only under it or outdoors | Wording only |
| D10 | Co-design partner type | A group that already shreds HDPE or PP | Wording only. Recruiting the partner is on hold with TRL 4 |
| N1 | Budget figure (R14) | Option (a): raise `budget_usd` to $500 for the press, molds still as tooling | `project.yaml` `budget_usd` $400 to $500; README; R14 target $400 to $500 (MMD-REQ-001 v0.4) |
| N2 | Mass target (R9) | Option (a): relax to 40 kg for a bench-bolted press | R9 mass target 35 kg to 40 kg (MMD-REQ-001 v0.4). Confirming the head mass of a real arbor press needs purchasing and a measurement: decided but on hold (TRL 4) |
| N3 | Heater rating (R5) | Two 300 W barrel bands instead of 250 W | BOM item 7; MMD-PRC-001 v0.4; MMD-CAL-001 v0.2; media and drawing labels; heaters 600 W to 700 W |
| N4 | Mold cooling (R6) | A small fan at the mold | New BOM item 18 ($12.00), modeled in `cad/src/model.py`, on drawing MMD-DWG-001 Rev P2 and in the media; MMD-CAL-001 v0.2 |
| N5 | Feedstock grade (R1) | R1 requires flake from injection-molded items (caps, crates, buckets); bottle-grade HDPE excluded | R1 text (MMD-REQ-001 v0.4) |

## Effect on the numbers

*Table 2. Before and after (MMD-CAL-001 v0.1 to v0.2).*

| Quantity | Before | After |
| --- | --- | --- |
| `budget_usd` | $400 | $500 |
| Press parts cost (R14) | $495, over by $95 | $507, over by $7 |
| Press with one mold | $585 | $597 |
| Mass target and estimate (R9) | 35 kg; 38.5 kg, not met | 40 kg; 39.2 kg, at risk (98 % of the target, with an assumed 8 kg press head) |
| Warm-up (R5) | 14.8 min, at risk | 12.2 min, met on paper |
| Cycle and throughput (R6) | 6.4 min, 9.4 per hour, mold about 92 °C, at risk | 5.2 min (soak limited), 11.6 per hour, mold about 47 °C, met on paper |
| Connected load (R10) | 635 W, 5.3 A at 120 V | 753 W, 6.3 A at 120 V, still met |
| Energy per shot | About 21 Wh | About 20 Wh |
| Requirement counts | 2 not met, 3 at risk, 6 met on paper, 4 met by design, 1 not verifiable | 1 not met, 2 at risk, 8 met on paper, 4 met by design, 1 not verifiable |

## Consequences

- Controlled documents revised: MMD-PRC-001 v0.4, MMD-REQ-001 v0.4, MMD-CAL-001 v0.2 and MMD-DDR-001 v0.2. Drawing MMD-DWG-001 is at Rev P2. `bom/bom.csv` has 18 lines. No pitch or problem rewording was recommended, so the pitch and problem in `project.yaml` are unchanged.
- R14 is still not met, by $7, because the mold cooling fan (N4) was added after the $500 figure (N1) was recommended. This is a new item for Amish (below); it is not decided here.
- No decision needs another repo to change, so there are no cross-repo actions.
- Decided but on hold because TRL 4 is on hold: recruiting the co-design partner (D10), choosing and weighing a real arbor press (N2), and any build or trial of the heaters, fan or press.

## Items still open

*Table 3. Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| O1 | The specific first co-design partner and its city or region. No recommendation was made. | Proposed, awaiting Amish |
| O2 | First product molds after the test plaque. For co-design; no recommendation was made. | Proposed, awaiting Amish |
| O3 | New: the press is $507 against $500. Options: (a) raise `budget_usd` to $520; (b) keep $500 and recheck against real quotations at TRL 4, since a $7 overrun is within the accuracy of indicative prices; (c) count the mold cooling fan as workshop equipment outside the press budget, as the molds are. Recommendation: (b). | Proposed, awaiting Amish |
