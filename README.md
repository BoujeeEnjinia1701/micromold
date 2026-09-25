# MicroMold

**Area:** Advanced Manufacturing · **Status:** Concept · **Prototype budget:** about $400 USD · **Difficulty:** 3 of 5

A desktop injection molding press for recycled plastic: a lever or screw press with a heated barrel and interchangeable aluminum molds, turning shredded waste plastic into small useful parts.

## Concept rationale

Molding gives recycled plastic a higher value than sheet or filament and makes spare parts locally.

## Burning platform

Plastic waste in lower-income cities is mostly unmanaged, and local recycling needs products that pay for collection.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. It extends the circular economy work of WasteWise and PotPress into manufacturing.

## Problem

Community recycling produces shredded plastic with few local uses, and small-batch molding of parts is out of reach without an injection press.

## Concept

A desktop injection molding press for recycled plastic: a lever or screw press with a heated barrel and interchangeable aluminum molds, turning shredded waste plastic into small useful parts.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Heated barrel with band heater and PID controller
- Lever or screw plunger frame
- Nozzle and mold clamp
- CNC-machined aluminum mold set
- Insulation and guard
- Temperature and pressure indication

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Hot barrel and molten plastic: use guards, heat-resistant gloves and ventilation. Some plastics release harmful fumes when overheated. Mains wiring must be done or checked by a qualified electrician and follow local electrical code.

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
