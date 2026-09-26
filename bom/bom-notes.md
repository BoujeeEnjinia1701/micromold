# BOM notes

Costs are indicative USD prices for TRL 3, not quotations. Every line has a unit cost and a supplier or supplier type. Checked against `budget_usd` in MMD-CAL-001, section L.

- Line numbers match the callouts in `media/exploded.png` and Table 1 of MMD-PRC-001. Item 15 (hardware) is not modeled.
- Total $585.00 with one mold; $495.00 for the press alone; $90.00 for the test plaque mold.
- Under MMD-DDR-001 D8 (adopted for TRL 3, open for Amish's review) the $400 budget covers the press, and molds are tooling (R8). The press is over by $95.00, so MMD-REQ-001 R14 is not met; with one mold the total is over by $185.00. `budget_usd` in `project.yaml` is unchanged; options are in `docs/REVIEW.md`.
- Added at TRL 3 from the calculations: the ratchet handle and socket (in item 2), the G-11 spacer (in item 4), the 20 mm bracket plate and mica pads (item 9), the nozzle zone shield (item 16) and the fume hood and duct fan (item 17, MMD-DDR-001 D9). Together about $96.
- Line 3 (rack ram) comes with the arbor press in line 2 and has no separate cost. The ram must be 255 mm or longer with 150 mm of engaged travel; confirm on the chosen press.
- Heater and fan voltage must match the regional supply (230 V or 120 V).
- Feedstock is not in the BOM. Use flake from injection-molded items; bottle-grade HDPE is too stiff for a hand press (MMD-CAL-001, E6).
