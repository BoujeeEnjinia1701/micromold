# BOM notes

Costs are indicative USD prices for TRL 3, not quotations. Every line has a unit cost and a supplier or supplier type. Checked against `budget_usd`, a hypothetical value-engineering target (not a limit), in MMD-CAL-001, section L.

- Line numbers match the callouts in `media/exploded.png` and Table 1 of MMD-PRC-001. Item 15 (hardware) is not modeled.
- Total $638.00 with one mold; $544.00 for the press alone; $94.00 for the test plaque mold.
- Value-engineering target: USD 520. Estimated cost of the constructable design: USD 544 for the press (USD 24 over the target). Cost drivers and savings worth trying are in MMD-DEC-001.
- Changed by MMD-DDR-003 (design for construction, 2026-10-01): line 1 is 8 mm plate; lines 9, 10, 11, 12, 16, 17 and 18 respecified for the buildable design (shelf back plate and cap screws, split jacket and hangers, screw lift with handwheel nut, mold cap screws, inserts and dowels, shield feet, hinges and latch, hood arm, fan plate bracket); line 19 (construction parts, $30.00) added. Item 15 and line 19 hardware are not all modeled.
- Under MMD-DDR-001 D8 and MMD-DDR-002 (decided by Amish, 2026-09-25) the budget covers the press, molds are tooling (R8), and `budget_usd` is $520 (was $500, and $400 before that), approved by Amish on 2026-09-26 to cover the priced BOM. Since MMD-DDR-003 the press is $24.00 over the target; with one mold the total is $118.00 over, the mold being tooling.
- Changed by MMD-DDR-002: the band heaters (item 7) are 300 W instead of 250 W at a similar price, and a mold cooling fan (item 18, $12.00) is added.
- Added at TRL 3 from the calculations: the ratchet handle and socket (in item 2), the G-11 spacer (in item 4), the 20 mm bracket plate and mica pads (item 9), the nozzle zone shield (item 16) and the fume hood and duct fan (item 17, MMD-DDR-001 D9). Together about $96.
- Line 3 (rack ram) comes with the arbor press in line 2 and has no separate cost. The ram must be 255 mm or longer with 150 mm of engaged travel; confirm on the chosen press.
- Heater and fan voltages must match the regional supply (230 V or 120 V).
- Feedstock is not in the BOM. Use flake from injection-molded items; bottle-grade HDPE is too stiff for a hand press (MMD-CAL-001, E6).
