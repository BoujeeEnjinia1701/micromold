# Review note: MicroMold

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (MMD-PRB-001 v0.2): the problem in numbers with sources, users and context, constraints, out of scope, prior work (Precious Plastic injection machine, processing data, portfolio links); co-design checklist kept, with questions for users.
- `docs/03-requirements.md` (MMD-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, status against first-order estimates and planned verification; assumptions; requirements not met.
- `docs/02-concept.md` (MMD-PRC-001 v0.2): how it works, components table numbered to the BOM, first-order numbers with assumptions, design choices with options, safety section, open questions.
- `cad/src/concept_media.py`: massing model of 14 parts (base plate, column and drive head, rack ram, load cell, plunger, barrel, band heaters, nozzle, bracket, jacket and guard, mold clamp, mold set, control box, wiring), shown on a 0.9 m workbench with a 1.75 m person for scale.
- `media/`: hero, blueprint sheet (PNG, PDF, SVG), cutaway, exploded view with BOM callouts, material flow per shot (estimates marked), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 15 lines with indicative prices, numbered to match the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, industry and region tables and the idea's trigger expanded with sources; problem, concept, key components and safety updated.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch says "a lever or screw press"; the proposed rack-and-pinion drive is a lever-driven press, so the pitch still holds.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Shot size | about 34 g HDPE (46 cm³ swept) | R2 met |
| Melt pressure at 250 N on the handle | about 8.9 MPa (89 bar) | R3 met, about 10 % margin |
| Mold clamp limit | about 45 cm² projected area | R7 met |
| Warm-up to 220 °C | about 10 to 12 min | R5 met |
| Cycle | about 6 min, 10 parts per hour | R6 met on paper; melt soak unverified |
| Power | about 600 W; 2.6 A at 230 V | R10 met |
| Energy | about 14 Wh per shot, about 0.5 kWh per kg of parts | |
| Mass and size | about 32 kg; 320 x 260 mm base; about 1.06 m to the handle | R9 met |
| Parts cost | about $399 press; about $489 with one mold | R14 **not met** |

Requirements not met or at risk:

- **R14 cost:** about $489 with one mold against the $400 budget (press alone about $399, no margin).
- **R13 fume control:** no extraction in the concept or BOM.
- **R15 garage-buildable:** partly met; the barrel needs a lathe and the mold a mill.
- **R11:** met on paper for the jacket, but the nozzle and mold zone guard is not yet designed.
- **R3** and **R6** are at risk: R3 depends on the assumed 60 % drive efficiency, R6 on how fast flake melts in a 22 mm bore.
- **R16** (part repeatability) cannot be assessed until hardware exists (TRL 4, outside the current phase).

### Proposed, awaiting Amish

Update 2026-09-25: Amish accepted all recommendations (MMD-DDR-002). Items 1 to 10 are decided as marked below; item 8 was later superseded by the $500 figure.

1. **Drive:** (a) simple lever, (b) rack and pinion from a 1 t arbor press on a taller column, (c) screw press. Recommendation: (b), with (c) as a variant for small, thick parts. **Decided by Amish, 2026-09-25: go with recommendation.**
2. **Layout:** vertical barrel with the mold below. Recommendation: vertical. **Decided by Amish, 2026-09-25: go with recommendation.**
3. **Injection:** plunger rather than a reciprocating screw for the first build. **Decided by Amish, 2026-09-25: go with recommendation.**
4. **Heating:** two PID zones (barrel and nozzle), about $15 more than one zone. Recommendation: two zones. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **Mold clamping:** bolted two-plate molds on a screw lift table now; a toggle clamp frame (about $40 more) as an upgrade. **Decided by Amish, 2026-09-25: go with recommendation.**
6. **Pressure indication:** a 10 kN load cell under the ram (about $30) rather than a spring-scale reading on the handle. **Decided by Amish, 2026-09-25: go with recommendation.**
7. **First mold:** a 64 x 50 x 6 mm test plaque; product molds after co-design. **Decided by Amish, 2026-09-25: go with recommendation.**
8. **Budget:** (a) keep $400 and count molds as tooling outside the machine budget; (b) raise to about $500 to include one mold; (c) drop the load cell and nozzle zone to reach about $450 with a mold. Recommendation: (a). `project.yaml` stays at $400 until Amish decides. **Decided by Amish, 2026-09-25: go with recommendation.**
9. **Fume control:** add a small hood and duct fan (about $40 to $60) at TRL 3, and keep a written condition to operate under extraction or outdoors. Recommendation: both. **Decided by Amish, 2026-09-25: go with recommendation.**
10. **First co-design partner:** a Precious Plastic workspace, a waste picker cooperative or a technical college. Recommendation: a group that already shreds HDPE or PP. **Decided by Amish, 2026-09-25: go with recommendation.**

### Safety concerns

- Molten plastic at up to 260 °C under pressure can spit from the nozzle or parting line; the nozzle and mold zone need a shield, which the concept does not yet show.
- Fumes: PVC and unknown plastics must never be heated; overheated PS releases styrene. Extraction is not yet in the design (R13).
- Mains-voltage band heaters on a steel frame: earthing, a fused inlet, an RCD or GFCI supply and an independent thermal cut-out are required, with wiring done or checked by a qualified electrician.
- The handle and rack store force and can pinch; a handle stop is needed.
- Recycled parts of unknown history must not be sold for food contact, young children's toys, medical or safety-critical use.

### Gaps and notes

- The session's web search budget was used up before this repo, so sources were checked by fetching pages directly. Figures that could not be verified were left out: commercial bench-top press specifications, the ram travel of 1 t arbor presses, and a cited fact for the Latin America row of the README table.
- Material property values (HDPE melt density, heat capacity, heat of fusion) are typical handbook values stated as estimates, to be sourced in the TRL 3 calculation note.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3` to calculate the drive force and efficiency, plunger clearance, melt soak time, heater and insulation sizing, and bolt clamp limits; choose a specific arbor press and confirm its ram travel; add a nozzle shield and fume hood; and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed this repo's TRL 2 items one by one, so every item with a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. This session ran `/advance-trl3` on that basis and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (MMD-DDR-001 v0.1, status proposed): ten items adopted as recommended for TRL 3 (D1 to D10), two left open (O1, O2).
- `docs/04-calcs/01-sizing.md` (MMD-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: shot size and mold stack, drive and ratchet, structure at design and overload, mold clamp, fill pressure through the nozzle and sprue, plunger clearance, heat (warm-up, losses, skin, load cell), melt soak, mold heat and cycle, power and energy, fume hood, mass, cost, and a status for every requirement. The script imports the model's parameters and reads the BOM and `project.yaml`; every number in the note is printed by it.
- `cad/src/model.py`: parametric build123d model of the press (16 modeled BOM items) with the vertical stack derived from the parameters. Exports `cad/step/` and `cad/stl/` for `micromold-assembly`, `barrel-set` and `mold-set`.
- `cad/src/sheets.py` and `cad/drawings/MMD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, 1:10, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". MMD-DWG-001 was free because the concept blueprint is MMD-DWG-010. To fit 1:10, the top view is placed beside the right view and labeled "relocated".
- `bom/bom.csv` (17 lines, all priced with a supplier type, $585.00) and `bom/bom-notes.md`.
- `cad/src/concept_media.py` now builds from the model; all of `media/` was re-rendered and every image checked. The cutaway now cuts on the injection axis (a project-side wrapper; the kit is unchanged), because the kit's cutter sat about 20 mm behind the axis and showed the barrel whole.
- MMD-PRB-001, MMD-PRC-001 and MMD-REQ-001 revised to v0.3; `README.md` and `project.yaml` (`trl: 3`, `trl_target: 3`, evidence list) updated. PDFs rebuilt in `docs/pdf/`.

Design changes found necessary by the calculations, applied for TRL 3 within the adopted items and open for Amish's review: a 450 mm ratchet handle on the pinion (one pull moves the plunger only about 31 mm, and a shot needs 120 mm); a 4 mm nozzle orifice and a sprue tapering from 5 to 7 mm (the 3 mm nozzle needed up to 12.1 MPa to fill); a 10 mm G-11 spacer under the load cell (otherwise about 94 °C); a 20 mm bracket plate on four mica pads (a 10 mm plate yields at overload); a perforated nozzle zone shield; the nozzle tip raised from 152 to 190 mm so that 120 mm mold stacks fit; a 255 mm ram; M10 x 110 mold bolts; and a pinned floating coupling on the plunger.

### Requirement status (MMD-CAL-001, Table 4)

2 not met, 3 at risk, 6 met on paper, 4 met by design, 1 not verifiable at TRL 3.

| ID | Status | Key number |
| --- | --- | --- |
| R14 Affordable | **Not met** | Press $495 against $400 (redefined scope, molds as tooling); $585 with one mold against the same $400 |
| R9 Bench size and mass | **Not met** (mass) | 38.5 kg against 35 kg, with an assumed 8 kg arbor press head; footprint 320 x 260 mm and handle 1,089 mm met |
| R2 Shot size | At risk | 34.2 g ideal; about 25 g if the fresh charge is not tamped with the press |
| R5 Warm-up | At risk | 14.8 min against 15 min |
| R6 Throughput | At risk | 9.4 parts per hour, but the mold settles at about 92 °C in still air |
| R3, R7, R8, R10, R11, R13 | Met on paper | 8.9 MPa at 250 N (11 % margin; fill needs 4.8 MPa); 45 cm²; $90 mold; 635 W; skin 48 °C; 124 m³/h hood |
| R1, R4, R12, R15 | Met by design | Safe resins; two PID zones with limits; electrical features; only the barrel and molds machined |
| R16 Repeatable parts | Not verifiable at TRL 3 | Needs hardware |

Key numbers: 22.5:1 drive, 3.8 ratchet pulls per shot; 13.2 kN and 34.7 MPa if an operator hangs 700 N on the handle (1.35 times the press rating); column 96.6 MPa and bracket 117 MPa at that overload; 103 W standing losses; about 21 Wh per shot.

### Decisions recorded (MMD-DDR-001)

Decided by Amish, 2026-09-25: go with recommendation (MMD-DDR-002; recorded at the time as adopted for TRL 3 and open for his review): D1 rack-and-pinion drive from a 1 t arbor press, screw press as a variant; D2 vertical barrel, mold below; D3 plunger injection; D4 two PID zones; D5 bolted two-plate molds on a screw lift table, toggle clamp later; D6 10 kN load cell; D7 test plaque first; D8 keep $400 with molds as tooling outside the machine budget (applied as a redefinition of R14; `budget_usd` unchanged, no new figure was recommended); D9 side hood with duct fan plus a written condition to run under it or outdoors; D10 first co-design partner to be a group that already shreds HDPE or PP. No pitch or problem rewording was recommended, so none was applied. MicroMold uses none of the batch's shared components, so no cross-repo interface applies.

### Still awaiting Amish

1. **O1, the specific first co-design partner and its city or region.** No recommendation was made.
2. **O2, first product molds after the test plaque.** For co-design; no recommendation was made.
3. **New, budget (R14).** Options: (a) raise `budget_usd` to $500 for the press, molds still as tooling; (b) count the fume extraction ($48) as workshop equipment outside the budget, which leaves the press at $447, still over; (c) drop the load cell and the ratchet, which would break R3's pressure reading and the shot. Recommendation: (a). Not applied; `budget_usd` stays at $400. **Decided by Amish, 2026-09-25: go with recommendation** (applied, MMD-DDR-002).
4. **New, mass target (R9).** Options: (a) relax to 40 kg for a bench-bolted press; (b) keep 35 kg and lighten the base plate, bracket and clamp. Recommendation: (a), after the head mass of a real press is known. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (applied, MMD-DDR-002).
5. **New, heater rating (R5).** Recommendation: two 300 W bands instead of 250 W, giving 12.2 min (700 W in all, R10 still met). Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (applied, MMD-DDR-002).
6. **New, mold cooling (R6).** Recommendation: a small fan at the mold cooling station, which keeps the mold near 47 °C. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (applied, MMD-DDR-002).
7. **New, feedstock grade (R1).** Recommendation: add to R1 that flake comes from injection-molded items (caps, crates, buckets), because bottle-grade HDPE would need about 24 MPa. Not applied. **Decided by Amish, 2026-09-25: go with recommendation** (applied, MMD-DDR-002).

### Safety concerns

- Overload: body weight on the handle takes the press to 1.35 times its rating and about 35 MPa of melt pressure, enough to open the test mold's parting line and spit melt. The shield is essential, and a handle stop or pull limit is recommended before any build.
- The ratchet holds the ram under load; releasing the pawl can let the handle spring back.
- Fumes: capture from the nozzle zone relies on the plume rising to the side hood, which is assumed, not calculated. PVC and unknown plastics stay excluded.
- Hot funnel top (about 150 °C) is a working surface; gloves are required when loading.
- Mains heaters on a steel frame: earthing, fused inlet, RCD or GFCI and an independent cut-out remain required, with wiring done or checked by a qualified electrician.

### Gaps and notes

- Citations: WebFetch could not be used in this session (the fetch permission was not granted in time) and the WebSearch quota is exhausted, so the ram travel and head mass of 1 t arbor presses, commercial bench-top press figures and the Latin America fact in the README table remain unverified and are left out. Material and flow properties in MMD-CAL-001 are typical handbook values stated as assumptions, not cited.
- Kit cutaway: the kit cuts at the mean Y of the parts; `cad/src/concept_media.py` replaces it with a cut on Y = 0 so the bore shows.
- The hood is drawn floating beside the funnel; its bracket to the column is not modeled.
- Existing material beyond TRL 3: `build-log/README.md` (scaffold) is present, untouched and not extended. No test, build, firmware or PCB material exists.

### Recommended next step

TRL 4 is on hold by Amish's instruction; this repo stops at TRL 3. Amish's review is needed on the adopted items D1 to D10, the TRL 3 design changes and the new items 3 to 7 above, above all the budget and mass targets. For the record only, TRL 4 would need: a chosen arbor press with its ram measured, a built barrel, nozzle and test mold, a lab test report (TST, `environment: lab`) of warm-up, shot mass and repeatability (R16), melt pressure from the load cell, mold temperature over a run and fume capture, and build log entries. None of this has been started.

## Session 2026-09-25: recommendations accepted

Amish wrote, in chat on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every MicroMold item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation", recorded in `docs/decisions/0002-recommendations-accepted.md` (MMD-DDR-002 v0.1). Items without a recommendation stay open. `trl: 3` and `trl_target: 3` are unchanged.

### Decisions applied and what changed

- **D1 to D10 (MMD-DDR-001, now v0.2):** drive, layout, plunger injection, two PID zones, bolted molds on a lift table, load cell, test plaque, molds as tooling, side hood plus written condition, and a partner that already shreds HDPE or PP. Wording only; the design already followed them.
- **N1, budget:** `budget_usd` $400 to $500 in `project.yaml`; R14 target $400 to $500; README budget line updated.
- **N2, mass target:** R9 35 kg to 40 kg.
- **N3, heaters:** barrel bands 2 x 250 W to 2 x 300 W (BOM item 7, same price); warm-up 14.8 to 12.2 min; heaters 600 to 700 W.
- **N4, mold cooling:** new BOM item 18, a 120 mm mains axial fan on an angle bracket on the base plate ($12.00, 0.7 kg assumed), added to `cad/src/model.py`, STEP and STL, drawing MMD-DWG-001 (Rev P1 to P2) and all media. Mold about 92 to 47 °C; cycle 6.4 to 5.2 min (now soak limited); 9.4 to 11.6 parts per hour.
- **N5, feedstock:** R1 now requires flake from injection-molded items (caps, crates, buckets) and excludes bottle-grade HDPE.
- Knock-on numbers (MMD-CAL-001 v0.1 to v0.2): press cost $495 to $507, with one mold $585 to $597; mass 38.5 to 39.2 kg; connected load 635 to 753 W (5.3 to 6.3 A at 120 V); energy about 21 to 20 Wh per shot.
- Documents: MMD-PRB-001 v0.4, MMD-PRC-001 v0.4, MMD-REQ-001 v0.4, MMD-CAL-001 v0.2 (script `docs/04-calcs/sizing.py` updated), MMD-DDR-001 v0.2, new MMD-DDR-002 v0.1; `bom/bom-notes.md`; PDFs rebuilt.
- Also this session: every generated file re-rendered so the footer shows designmolecule.com; README "What sparked the idea" rewritten around the Hyatt brothers' 1872 plunger molding patent (US 133,229).

### Requirement status (MMD-CAL-001 v0.2)

1 not met, 2 at risk, 8 met on paper, 4 met by design, 1 not verifiable at TRL 3 (was 2, 3, 6, 4, 1).

| ID | Status | Key number |
| --- | --- | --- |
| R14 Affordable | **Not met** | $507 press against $500, over by $7 (the mold fan); $597 with one mold |
| R9 Bench size and mass | At risk | 39.2 kg against 40 kg, with an assumed 8 kg press head |
| R2 Shot size | At risk | 34.2 g ideal; about 25 g if the fresh charge is not tamped |
| R3, R5, R6, R7, R8, R10, R11, R13 | Met on paper | 8.9 MPa; 12.2 min; 11.6 per hour; 45 cm²; $90 mold; 753 W; skin 48 °C; 124 m³/h |
| R1, R4, R12, R15 | Met by design | Injection-grade flake only; two PID zones; electrical features; only barrel and molds machined |
| R16 Repeatable parts | Not verifiable at TRL 3 | Needs hardware |

### Still awaiting Amish

1. **O1:** the specific first co-design partner and its city or region. No recommendation.
2. **O2:** first product molds after the test plaque. No recommendation.
3. **O3 (new):** the press is $507 against $500. Options: (a) raise `budget_usd` to $520; (b) keep $500 and recheck against real quotations at TRL 4, since $7 is within the accuracy of indicative prices; (c) count the mold cooling fan as workshop equipment outside the press budget, as the molds are. Recommendation: (b). **Decided by Amish, 2026-09-26: `budget_usd` $520 (option (a)); see "Session 2026-09-26: budget approved".**

### Cross-repo actions

None. MicroMold uses none of the shared components, and no decision needs another repo to change.

### Safety concerns

- The mold cooling fan adds a mains-voltage fan beside the hot zone: keep its finger guard, route its lead away from the barrel and nozzle, and earth its bracket.
- Unchanged: overload on the handle (about 35 MPa), the ratchet holding the ram under load, fume capture assumed rather than calculated, and mains heaters. A handle stop or pull limit is still recommended before any build.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: recruiting the co-design partner (D10), choosing and weighing a real arbor press to confirm the head mass behind R9 (N2), and any build, purchase or trial of the press, heaters or fan. No test, build, firmware or PCB material was created.

## Session 2026-09-26: sources strengthened

- README, "By country or region": the uncited "Latin America (Brazil, Colombia)" row is replaced by a Brazil row citing the National Solid Waste Policy, Law 12,305 of 2010, on the official Planalto site (arts. 36 and 42: priority for cooperatives of low-income waste pickers and federal support for their equipment). Colombia is dropped because no source was verified for it.
- README, South Asia row: the uncited reference to large informal recycling sectors is removed.
- README, burning platform: the OECD 9 % recycling figure now also cites the OECD February 2022 press release, which states the figure directly; wording trimmed to what that release says.
- All other README links (World Bank *What a Waste 3.0*, Basel Convention, NEMA, US EPA, Precious Plastic Academy, US Patent 133,229) were fetched and confirmed. "What sparked the idea" unchanged; it already rests on the patent record.
- No controlled document changed; no budget change (O3 remains open).

## Session 2026-09-26: budget approved

Amish wrote, in chat on 2026-09-26: "i approve all the budget items." O3 is decided: budget set to $520 to cover the priced BOM (MMD-DDR-002 v0.2).

- `project.yaml` `budget_usd` $500 to $520; README budget and cost lines updated.
- R14 target $500 to $520; status **not met to at risk** ($507 press, $13 or 2.5 % margin on indicative prices; $597 with one mold, the mold being tooling).
- Requirement counts (MMD-CAL-001 v0.3): 0 not met, 3 at risk, 8 met on paper, 4 met by design, 1 not verifiable (was 1, 2, 8, 4, 1).
- Documents: MMD-PRB-001 v0.5, MMD-PRC-001 v0.5, MMD-REQ-001 v0.5, MMD-CAL-001 v0.3 (`sizing.py` now reports the margin when under budget), MMD-DDR-002 v0.2; `bom/bom-notes.md`; PDFs rebuilt. No media shows the budget, so none was regenerated.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose MicroMold on 2026-09-26 for the first batch of product renders, in the style of a product-design portfolio shot: finished-product geometry, studio lighting and a light seamless background.

### What was added

- `cad/src/product_model.py`: an appearance model for photoreal renders, built on `PARAMS`, `derived()` and `build_parts()` in `cad/src/model.py`. It exposes `product_parts()` (84 parts: 64 shell, 10 internal, 9 accessory, 1 context), `TITLE` and `RENDER_VIEWS` (hero and exploded). It adds:
  - Fillets on the base plate, column tube, press head, bracket, lift table, mold plates, control box and fan frame.
  - Fasteners: bench bolts and washers, gib screws with lock nuts on the head, a pinion shaft nut, M10 mold bolts with washers and nuts, heater clamp screws and fan bracket bolts.
  - Rack teeth on the ram, a ratchet head with a reversing lever, a ribbed rubber grip and a ball knob on the handle.
  - A visible mold parting line with pry slots, a sprue bushing seat and a stamp; nut slots in the lift table; guide rods and bushes on the screw jack; rubber grips on the tommy bar.
  - Mica band heaters with clamp lugs and ceramic terminal blocks; a nozzle with a radiused tip and its heater band; the jacket as an aluminum skin inside a slotted steel guard.
  - Perforated sides and a perforated window in the nozzle zone shield, hinges, a latch knob and a hot-surface warning label.
  - The fume hood with a face lip, round duct stub, band clamp and a short run of flexible duct; the cooling fan with blades, finger guard and bracket.
  - The control box with two lit PID controllers (process and set values), a lit force display for the load cell, a lit mains rocker switch, a cut-out reset button, a name plate, side vents, glands and a rear inlet; heater wiring in glass-fiber sleeving (fabric material) and a load cell lead.
  - Accessories: a tray of recycled flake and three molded test plaques. Context: a compact section of workbench top.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately by the render pipeline.

### Differences from model.py

Each is appearance only; none changes a main dimension or interface.

1. **Fume duct.** `model.py` shows a square 100 mm massing block for the duct stub. The appearance model uses a round 100 mm duct stub of the same height with a band clamp, then a short run of flexible duct bending toward the back, cut short, because the inline fan and its 3 m of duct (BOM 17) have no position in the model. Proposed, awaiting Amish. Recommendation: accept for renders; place the inline fan in `model.py` only if a later layout needs it.
2. **Guide rods.** BOM 11 lists two guide rods that `model.py` does not model. The appearance model shows them under the lift table at X = ±62 mm with bushes on the base plate. Proposed, awaiting Amish. Recommendation: accept; confirm their positions when the clamp is detailed.
3. **Shield window.** `model.py` leaves the window opening in the shield front empty so the mold shows. The appearance model fills it with the perforated panel that BOM 16 specifies (10 mm square holes), so the mold is partly hidden in the hero render. Proposed, awaiting Amish. Recommendation: keep the perforated panel, since it is the safety guard as specified.
4. **Mold bolts.** `model.py` shows only the bolt heads. The appearance model shows full M10 bolts with washers, hex heads and nuts in slots in the lift table; the head top sits at the same height. Proposed, awaiting Amish. Recommendation: accept.
5. **Control box front.** The two PID envelopes are kept. A force display, mains rocker switch and cut-out reset button are added below them, in the box front, from BOM 4 and BOM 13. Proposed, awaiting Amish. Recommendation: accept; the panel layout is illustrative.
6. **Display values.** The lit readouts show illustrative set points (210 °C barrel, 225 °C nozzle) and 0.00 kN force with the plunger raised. These are not recommendations. Proposed, awaiting Amish. Recommendation: accept as illustrative.

### Status

This is an appearance model only: no tolerances, no fabrication detail and no change to `model.py`, the BOM or the controlled documents. `trl` stays 3, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: kit 1.7.0, constructable design and prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept in a separate register. He also wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." This session brought MicroMold to that standard. Nothing was built or bought; `trl` stays 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced by `.kit/CLAUDE.md`.
- Constructability review with build123d checks: `cad/src/model.py` rewritten as separate components (`build_components()`), grouped by BOM line for the existing media (`build_parts()`), with `python cad/src/model.py --check`: 155 checks (no unintended overlap, every joint touching, clearances, full stroke, table at both ends of travel, assembly order, a process and BOM line for every part). All pass.
- `docs/decisions/0003-design-for-construction.md` (MMD-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `bom/bom.csv` (19 lines; line 19 added) and `bom/bom-notes.md`; `docs/04-calcs/sizing.py` and MMD-CAL-001 v0.4 (mass, heights, heat, cost against the value-engineering target); MMD-REQ-001 v0.6; MMD-PRC-001 v0.6; `README.md` (links line, "Building the prototype"); `project.yaml` (`design_state: constructable`, new evidence).
- STEP and STL regenerated; general arrangement MMD-DWG-001 Rev P4; concept media regenerated from the new model.
- `cad/src/build_plan_media.py`: overview, base plate hole layout, 14 making sketches (MMD-DWG-101 to 114), 11 joint close-ups and 14 assembly step pictures.
- `docs/05-build-plan.md` (MMD-BLD-001 v0.1) and `docs/06-design-decisions.md` (MMD-DEC-001 v0.1). PDFs rebuilt in `docs/pdf/`.

### Design changes made for construction (MMD-DDR-003)

1. Press head: cut from its frame and bolted to an 8 mm head plate welded to the column, four M10 countersunk screws reached through holes in the column (it overlapped the column by 30 mm, with no fixing).
2. Barrel bracket: a 20 mm shelf welded to the column face plus an 8 mm back plate welded up the column corners (it cut into the 3 mm wall and was fixed only to it); mica pads now in the stack.
3. Barrel flange 100 mm with four M8 cap screws; funnel 64 mm (was 80 mm) so the screws can be reached.
4. Nozzle screws into an M30 x 1.5 thread in the barrel; spherical tip in a 2 mm spherical seat in the mold (test mold table now at 102 mm).
5. Jacket made as two half shells hung on four tabs, spacers and M5 screws (it floated, and as one sleeve could not be fitted with the barrel in place).
6. Load cell, 56 mm G-11 spacer and a drilled plunger coupling on screws that never cross the spacer; ball-lock pin for the plunger (stack 5 mm taller; handle top 1,094 mm).
7. Screw lift: a Tr20 screw welded under the table, turned by a handwheel nut on the base plate, dropping through a hole in the bench; the column face stops the table turning (the concept's 100 mm jack could not fit in 50 mm).
8. Mold: M10 cap screws into thread inserts, two dowels; sprue taper turned the right way.
9. Shield sides on folded feet screwed to the base; front on two hinges and a latch.
10. Mold fan on a plate bracket with an intake hole; fan 4 mm closer to the mold.
11. Hood held by an L-shaped arm on rivnuts in the column.
12. Heater wiring rerouted over the shield.
13. Ratchet adapter made from the press's lever hub with a welded 1/2 in square drive.
14. Base plate 8 mm (was 12 mm) and head and back plates 8 mm, keeping mass under 40 kg.
15. Assembly order fixed: barrel in from above before the press head; band heaters clamp on after; plunger unit fitted as one piece.

### Key results

- Mass 39.0 kg against 40 kg (R9 at risk; head mass assumed). Handle top 1,094 mm (R9 met on height).
- Value-engineering target: USD 520. Estimated cost of the constructable design: USD 544 for the press (USD 24 over the target); USD 638 with the test mold. The construction parts added USD 37.
- Warm-up 12.3 min (was 12.2 min); other results unchanged. Counts: none not met, 2 at risk (R2, R9), 8 met on paper, 4 met by design, 1 not verifiable at TRL 3, R14 over the value-engineering target.

### Proposed, awaiting Amish

All in the design decisions register (MMD-DEC-001): accept the changes above; how flake is loaded with only 8 mm between the raised plunger and the funnel (recommend lifting the plunger out on its ball-lock pin); the hole through the bench for the lift screw; a handle stop or torque-limiting socket; and the earlier open items (partner, product molds, appearance model differences).

### Stale media (made on Amish's Mac, not regenerated here)

The design changed visibly, so these need redoing with `/render-product` after `cad/src/product_model.py` is updated: `media/render-hero.png`, `media/render-exploded.png` (and any other `media/render-*.png`), `media/card.png` and `media/social-preview.png`. They show the concept's head position, 80 mm flange and funnel, the screw jack block with a front crank, mold bolts with nuts, guide rods, and the old fan bracket.

### Safety concerns

- Overload on the handle is still unlimited (about 35 MPa at 700 N); a torque-limiting socket is recommended (register item 4).
- Loading flake with the plunger lifted out means handling a plunger whose top end is about 94 °C; heat-resistant gloves are required.
- The barrel is fitted from above and the press weighs 39 kg: two people to lift it, and the bench must be drilled.

### Recommended next step

Amish reviews MMD-DDR-003 and the register. TRL 4 (buying the arbor press, confirming the items listed for purchase, building and testing) stays on hold.

## Session 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This approves the recommendation written for each open decision in the design decisions register (MMD-DEC-001 v0.1). trl stays 3; no build or test work was done, and the model, BOM quantities and prices, and pictures are unchanged.

### Decisions recorded

Seven decisions, all moved to Decisions made in MMD-DEC-001, dated 2026-10-02:

1. MMD-DDR-003 accepted, P1 to P15, with one condition: P1 (cutting the head from the arbor press casting and tapping four M10 holes in its back) is confirmed against the bought press before it is cut.
2. Loading: option (a), lift the plunger out on its ball-lock pin to load, with a simple plunger rest on the column so the hot plunger is never laid on the bench.
3. Lift screw: option (a), a 25 mm hole through the bench.
4. Overload: option (b), a torque-limiting socket on the ratchet adapter, set so the ram cannot exceed the press rating, checked against the load cell at TRL 4.
5. First co-design partner: a community plastic recycling workspace that already shreds HDPE or PP; a Precious Plastic workspace near Irving, Texas, is the first candidate to approach.
6. First product mold: a flat, single-cavity part of 25 g or less that fits the 120 x 90 mm plates, such as a coaster, tile or cable clip, chosen with the partner.
7. Appearance model: accept differences 1, 3, 5 and 6; update 2 and 4 to the constructable design and add the screw lift, flange and fan bracket at the same time.

### Documents changed

- `docs/06-design-decisions.md` (MMD-DEC-001 v0.2): open decisions moved to Decisions made; the 2026-09-30 row updated.
- `docs/decisions/0003-design-for-construction.md` (MMD-DDR-003 v0.2, status Draft): accepted with the P1 condition; A1 to A3 accepted, with the plunger rest added to A1; consequence added.
- `docs/decisions/0001-trl2-review-decisions.md` (MMD-DDR-001 v0.3) and `docs/decisions/0002-recommendations-accepted.md` (MMD-DDR-002 v0.3): O1 and O2 recorded as decided.
- `docs/02-concept.md` (MMD-PRC-001 v0.7): loading step with the plunger rest; pressure safety rule (torque-limiting socket replaces "fit a handle stop or a pull limit"); a hot plunger safety note; first product mold; first candidate partner.
- `docs/01-problem.md` (MMD-PRB-001 v0.6): first candidate partner.

### Follow-up actions to carry approved decisions into the design

1. Decision 1 (model and drawings): before cutting, check the bought press head against P1 (casting thickness behind the four M10 holes, 20 mm thread depth) and revise `cad/src/model.py` and MMD-DWG-001 if it differs.
2. Decision 2 (model, BOM, build plan pictures): add the plunger rest on the column to the model, a BOM line, the build plan (component, joint and step pictures) and its loading step.
3. Decision 4 (model, BOM, build plan pictures, calculations): add the torque-limiting socket to the ratchet adapter in the model and the BOM, set its torque in MMD-CAL-001 from the press rating, and update build plan section 3.6 and safety stop S4.
4. Decision 6 (drawings): sketch the first product mold (flat, single cavity, 25 g or less, on the 120 x 90 mm plates) once the partner picks the part.
5. Decision 7 (pictures): update `cad/src/product_model.py` (no guide rods; cap screws into inserts; the screw lift, flange and fan bracket as built) and re-render the photoreal renders, card and social preview on Amish's Mac.

### Points found in the review

- Value engineering counts moving the duct fan and duct (USD 48) into shared workshop extraction as a saving that brings the press to USD 496; that removes cost from scope rather than saving it, so it does not compare like with like with the USD 520 target.
- Overload protection (decision 4) had been recommended since TRL 3 and is still not in the model or BOM; it must be added before any build (follow-up 3).

## Session 2026-10-02: approved follow-ups carried out

Amish, 2026-10-02, approved that every follow-up action from the open-decision sign-off be carried out. trl stays 3; no build or test work was done. Documents changed, with new versions: MMD-CAL-001 v0.5, MMD-REQ-001 v0.7, MMD-PRC-001 v0.8, MMD-BLD-001 v0.2, MMD-DEC-001 v0.3; also `bom/bom.csv` and `bom/bom-notes.md`, `README.md`, `cad/src/model.py`, `docs/04-calcs/sizing.py`, `cad/src/build_plan_media.py`, `cad/src/sheets.py` (MMD-DWG-001 Rev P5), `cad/src/concept_media.py` and `cad/src/product_model.py`.

### Approved follow-ups carried out

1. **Decision 1, check the bought head against P1: not done in full.** The bought press does not exist yet (buying it is TRL 4, on hold). On paper: the model now checks the nominal values the head must have (10 mm of casting between each M10 hole and the ram bore, 21 mm hole depth for a 20 mm thread in a 140 mm deep head), and build plan section 3.5 has a step to check the bought head before the cut and to stop if it differs. The model and drawing MMD-DWG-102 are revised only if the bought head differs.
2. **Decision 2, plunger rest: done.** Plunger rest on the column's right wall in the model (cup 32 mm across, plate on two M6 rivnuts, 400 mm above the bench, with the rested plunger checked for clearance); BOM line 20 (USD 6, estimate by parts); making sketch MMD-DWG-115, joint 12, step 12 and the loading routine in build plan section 3.16; the column sketch MMD-DWG-102 gained the right-wall rivnut holes.
3. **Decision 4, torque-limiting socket: done.** Socket between the ratchet adapter and the ratchet in the model (BOM line 21, USD 40, estimate at the midpoint of a USD 30 to 50 retail band). Torque set in MMD-CAL-001 section B: the press reaches its rating at 234 N m, the socket is set to 180 N m (198 N m at plus 10 per cent), which limits the ram to 8.3 kN (0.85 times the rating) and the melt to 21.8 MPa; the script stops if a setting would let the ram pass the rating. Build plan section 3.6, step 7, safety stops S3 and S4 and the first checks table updated. Checking the setting against the load cell is TRL 4.
4. **Decision 6, sketch of the first product mold: not done.** It waits for the partner to choose the part (outreach by Amish).
5. **Decision 7, appearance model: done.** `cad/src/product_model.py` updated: guide rods, screw jack and tommy bar removed; lift table with its welded Tr20 screw, handwheel nut and thrust washer; M10 cap screws into inserts, no nuts; shelf, back plate, mica pads and flange screws, head plate and screws, coupling, fan bracket and screws, hood arm, torque-limiting socket and plunger rest as built. Render scenes exported (hero, exploded) to `/home/claude/renders/micromold`. The photoreal renders, card and social preview are made on Amish's Mac next.

### Key results

- Requirement status changes: none. R9 stays at risk (39.8 kg against 40 kg, was 39.0 kg); R14 stays over the value-engineering target.
- Value-engineering target: USD 520. Estimated cost of the constructable design: USD 590 (USD 70 over the target); USD 684 with the test mold. The two lines added USD 46.
- Model: 186 constructability checks pass (was 155). STEP and STL regenerated.
- Pictures regenerated: MMD-DWG-001 (Rev P5), MMD-DWG-102, 108 and 115 (new), joint 12 (new), overview, steps 7 to 14, concept media (hero, cutaway, exploded, flow, blueprint, viewer).
- Appearance deviations of the appearance model from the model (2 and 4 of the 2026-09-26 list) are now removed; items 1, 3, 5 and 6 stay accepted.

### Cross-repo actions

None for this repo from the follow-up list.

### Points for Amish

- Mass is 0.2 kg under the 40 kg target; any real arbor press head heavier than the assumed 8 kg takes R9 to not met.
- The torque setting of 180 N m is a paper figure from the press rating at an assumed 0.84 efficiency; it is confirmed against the load cell at TRL 4.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.

## 2026-10-03: decisions recorded

Amish decided on 2026-10-03: "TIght Margins - i accept the margins". For MicroMold this is the 180 N m torque-limiting socket setting and the R9 mass margin of 0.2 kg (39.8 kg against 40 kg, with an assumed 8 kg press head).

- `docs/06-design-decisions.md` (MMD-DEC-001) and `docs/03-requirements.md` (MMD-REQ-001) updated.
