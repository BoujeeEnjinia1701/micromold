# MicroMold

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Advanced Manufacturing · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

A desktop injection molding press for recycled plastic: a lever or screw press with a heated barrel and interchangeable aluminum molds, turning shredded waste plastic into small useful parts.

![MicroMold concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/MMD-DWG-001.pdf) · [Sizing calculations](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Concept rationale

Molding turns sorted flake into finished parts, which sell for far more than flake sold by weight, and it lets a community make the small parts it would otherwise import. MicroMold uses the simplest injection process that still gives useful pressure: a heated barrel, a hand-driven plunger and a bolted aluminum mold. The drive is the rack and pinion of a 1 t arbor press on a taller column, turned by a ratchet handle, which gives a long stroke and 22.5:1 advantage from one bought tool (the brief allows a lever or screw drive; this choice is adopted for TRL 3 and open for Amish's review).

It is open and garage-buildable because the value is in local making. Only the barrel and the molds need a lathe or mill, which most towns have in a machine shop, and a new mold costs tens of dollars in aluminum and machining rather than thousands for steel tooling. Open drawings let groups repair the press, share molds and adapt it, as the Precious Plastic community has done for its own machines.

## Burning platform

Only about 9 % of plastic waste was recycled worldwide in 2019, after losses in recycling ([OECD, *Global Plastics Outlook*, 2022](https://www.oecd.org/en/publications/global-plastics-outlook_de747aef-en.html)). Municipal solid waste reached 2.56 billion tonnes in 2022 and is projected to reach 3.86 billion tonnes by 2050, while collection covers only 31 % of waste in sub-Saharan Africa and 67 % in South Asia ([World Bank, *What a Waste 3.0*](https://www.worldbank.org/en/publication/what-a-waste)).

Recycling groups need products that pay for collection, and exporting scrap is getting harder: since 1 January 2021 the Basel Convention plastic waste amendments have required prior informed consent for most mixed or contaminated plastic waste shipments ([Basel Convention](https://www.basel.int/implementation/plasticwaste/amendments/overview/tabid/8426/default.aspx)). Adding value locally, by molding parts, is one of the few routes left for small operators.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| Community recycling and social enterprise | Turn sorted HDPE and PP flake into hooks, clips, knobs and tiles for local sale |
| Education and vocational training | Teach polymer processing, mold design and the circular economy with a press students can take apart |
| Repair and maintenance | Short runs of discontinued knobs, spacers, bushings and clips |
| Product design and prototyping | Low-cost aluminum bridge tooling to test a part in real thermoplastic before paying for steel molds |
| Agriculture and construction | Non-structural items such as cable clips, tile spacers, plant labels and hose guides (not food contact) |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| Kenya | Single-use plastic carrier and flat bags have been banned since 2017 ([NEMA](https://www.nema.go.ke/index.php?option=com_content&view=article&id=241)); durable recycled products are a natural outlet for collected HDPE and PP |
| Sub-Saharan Africa | Collection covers only 31 % of waste ([World Bank](https://www.worldbank.org/en/publication/what-a-waste)); products that pay for collection make it viable |
| South Asia (India, Bangladesh) | Collection reaches 67 % ([World Bank](https://www.worldbank.org/en/publication/what-a-waste)), with large informal recycling sectors that could add value to sorted flake |
| Latin America (Brazil, Colombia) | Organized waste picker cooperatives already sort plastics and look for higher-value outlets |
| United States | Plastics recycling was 8.7 % in 2018 ([US EPA](https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/plastics-material-specific-data)); makerspaces and schools can use it for local recycling programs |
| Europe (Netherlands and wider EU) | Precious Plastic workspaces already run open lever presses ([Precious Plastic Academy](https://onearmy.github.io/academy/build/injection)); a bench press with higher pressure widens what they can mold |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the circular economy work of WasteWise and PotPress into manufacturing. The trigger was the open Precious Plastic injection machine: a proven design, but a floor-standing lever press of 1.3 m and 23 kg that reaches about 45 bar ([Precious Plastic Academy](https://onearmy.github.io/academy/build/injection)). A smaller press with about twice the pressure would suit schools, repair shops and groups with a single bench.

## Problem

Community recycling produces shredded plastic with few local uses, and small-batch molding of parts is out of reach without an injection press. Only about 9 % of plastic waste is recycled worldwide, and groups that do collect and shred plastic often sell flake by weight for little return. Design with, not for: requirements must come from co-design sessions with recycling groups through a local partner.

## Concept

A bench-top, hand-operated plunger injection press. The rack-and-pinion head of a 1 t arbor press, on a taller steel column and turned by a ratchet handle, drives a 22 mm plunger down a vertical barrel heated by two 250 W band heaters and a 100 W nozzle heater, each zone under PID control. Melt fills a bolted two-plate aluminum mold held against a 4 mm nozzle by a screw lift table inside a perforated shield, a load cell under the ram shows the injection force, and a side hood with a duct fan draws fumes from the funnel. The TRL 3 calculations give up to 34 g of HDPE per shot at 8.9 MPa (89 bar) with 250 N on the handle in about four ratchet pulls, a 14.8 min warm-up, about 9 parts per hour and 635 W from a single-phase socket. Parts cost $495 for the press and $585 with one mold, over the $400 budget, and the press weighs about 38.5 kg, over its 35 kg target (see the [sizing calculations](docs/04-calcs/01-sizing.md) and the [review note](docs/REVIEW.md)).

![Material flow](media/flow.png)

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Heated steel barrel (22 mm bore) with two 250 W band heaters, and a 4 mm nozzle with a 100 W heater
- Rack-and-pinion drive head from a 1 t arbor press on a steel column, with a 450 mm ratchet handle
- 22 mm plunger with a load cell, on a glass-epoxy thermal spacer, for force and pressure indication
- Two-plate aluminum mold set on a screw lift table
- Insulation jacket and perforated guard; perforated nozzle zone shield
- Side fume hood with a 100 mm inline duct fan
- Control box with two PID controllers, SSRs, fused inlet and independent thermal cut-out

The priced bill of materials is in [bom/bom.csv](bom/bom.csv); the parametric model is [cad/src/model.py](cad/src/model.py), with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> **Safety:** Hot barrel, nozzle and molten plastic at up to 260 °C: use guards, heat-resistant gloves, long sleeves and eye protection, and keep faces off the injection axis. Close the nozzle zone shield before injecting. Process only HDPE, PP, LDPE and PS; never heat PVC or unknown plastics, and run the hood fan whenever the heaters are on, or work outdoors. Mains-voltage heaters: earth all metal parts, use a fused inlet and an RCD or GFCI supply, and have mains wiring done or checked by a qualified electrician to local electrical code. Keep hands clear of the rack, and release the ratchet pawl only with the handle in hand. See the safety section of the [design precis](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (MMD-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `MMD-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
