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

1. **Drive:** (a) simple lever, (b) rack and pinion from a 1 t arbor press on a taller column, (c) screw press. Recommendation: (b), with (c) as a variant for small, thick parts.
2. **Layout:** vertical barrel with the mold below. Recommendation: vertical.
3. **Injection:** plunger rather than a reciprocating screw for the first build.
4. **Heating:** two PID zones (barrel and nozzle), about $15 more than one zone. Recommendation: two zones.
5. **Mold clamping:** bolted two-plate molds on a screw lift table now; a toggle clamp frame (about $40 more) as an upgrade.
6. **Pressure indication:** a 10 kN load cell under the ram (about $30) rather than a spring-scale reading on the handle.
7. **First mold:** a 64 x 50 x 6 mm test plaque; product molds after co-design.
8. **Budget:** (a) keep $400 and count molds as tooling outside the machine budget; (b) raise to about $500 to include one mold; (c) drop the load cell and nozzle zone to reach about $450 with a mold. Recommendation: (a). `project.yaml` stays at $400 until Amish decides.
9. **Fume control:** add a small hood and duct fan (about $40 to $60) at TRL 3, and keep a written condition to operate under extraction or outdoors. Recommendation: both.
10. **First co-design partner:** a Precious Plastic workspace, a waste picker cooperative or a technical college. Recommendation: a group that already shreds HDPE or PP.

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
