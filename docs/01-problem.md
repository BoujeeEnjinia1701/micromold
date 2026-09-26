---
doc_id: MMD-PRB-001
title: MicroMold problem statement
project: MicroMold
doc_type: Problem statement
version: "0.5"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (users, context, constraints, out of scope, prior work with sources)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 update (budget covers the press with molds as tooling, fume extraction, feedstock grade, co-design partner type; MMD-DDR-001)
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($520)
---

# MicroMold problem statement

Small recycling groups can collect, sort, wash and shred plastic, but they struggle to turn the flake into products that people will pay for. Selling baled or shredded plastic returns little, and injection molding, the process that makes most small plastic parts, normally needs machines and steel tooling far beyond a community budget. MicroMold aims to close that gap with a bench-top injection press that a local workshop can build for a few hundred dollars and that runs aluminum molds a small machine shop can cut. The target is $520 for the press, with molds counted as tooling (MMD-DDR-002, approved by Amish on 2026-09-26); the TRL 3 estimate is $507 (MMD-CAL-001).

## The problem in numbers

- Only about 9 % of plastic waste was recycled worldwide in 2019, after losses in recycling; the rest was landfilled, incinerated or leaked into the environment ([OECD, *Global Plastics Outlook*, 2022](https://www.oecd.org/en/publications/global-plastics-outlook_de747aef-en.html)).
- Municipal solid waste reached 2.56 billion tonnes in 2022 and is heading for 3.86 billion tonnes by 2050. Collection covers only 31 % of waste in sub-Saharan Africa and 67 % in South Asia, and most uncollected waste is dumped in the open ([World Bank, *What a Waste 3.0*](https://www.worldbank.org/en/publication/what-a-waste)).
- Even in a high-income country the rate is low: the United States generated 35.7 million tons of plastics in 2018 and recycled 8.7 % ([US EPA](https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/plastics-material-specific-data)).
- Exporting scrap is getting harder. Since 1 January 2021 the Basel Convention plastic waste amendments require prior informed consent for most mixed or contaminated plastic waste shipments ([Basel Convention](https://www.basel.int/implementation/plasticwaste/amendments/overview/tabid/8426/default.aspx)), so value has to be added closer to where waste is collected.

## Users and context

Primary users (to be confirmed through co-design):

- **Community recycling groups and waste picker cooperatives** that already sort and shred HDPE and PP and want a product line (hooks, knobs, clips, spare parts, tiles) rather than selling flake by weight.
- **Precious Plastic style workspaces and makerspaces** that want a smaller, cheaper and more precise injection press than the community's lever machine, for short runs of small parts.
- **Schools, technical and vocational colleges and design courses** teaching polymer processing, mold design and the circular economy.
- **Repair shops and small workshops** that need short runs of simple replacement parts (knobs, spacers, bushings, clips) that are no longer sold.

Typical context: a covered workshop or container with single-phase mains (230 V or 120 V), a bench, hand tools, a drill press and access to a local machine shop with a lathe and a mill. Feedstock is washed, dried and shredded flake of one resin type from injection-molded items such as caps, crates and buckets (MMD-REQ-001 R1), because bottle-grade HDPE flows too stiffly for a hand press (MMD-CAL-001, E6), sorted by the group itself or with tools such as WasteWise Scan. MicroMold sits at the end of the plastics line described in the ReflowEconomy playbook.

## Constraints

- Garage-buildable prototype for $520 USD in parts for the press, with molds counted as tooling (`project.yaml`; MMD-DDR-001 D8, MMD-DDR-002); see MMD-REQ-001 R14 for the current estimate.
- Single-phase mains, 1 kW or less, so it runs from an ordinary socket or a small generator.
- Only the barrel and the molds may need machining; everything else built with hand tools, a drill press and optional welding.
- Molds in aluminum, cut on a manual mill or small CNC, so a new product costs tens to low hundreds of dollars in tooling rather than thousands.
- Safe processing only: HDPE, PP, LDPE and PS. PVC must never be heated, because it releases hydrogen chloride and other harmful products ([Precious Plastic Academy, "Plastic basics"](https://onearmy.github.io/academy/plastic/basics)).
- Hand-operated injection, so no hydraulics or motors are needed; the only motor is the fume extraction fan.
- Fumes must be captured at the press (a side hood and duct fan) or the press run outdoors (MMD-DDR-001 D9).

## Out of scope

- Production molding at industrial pressures (50 MPa and above) or cycle times of seconds.
- PET, PVC, engineering plastics (PA, PC, ABS blends) and mixed or unknown plastics.
- Shredding, washing and drying equipment (covered by other open machines and the ReflowEconomy playbook).
- Food-contact, medical or safety-critical parts. Recycled feedstock of unknown history cannot support those claims.

## Prior work

- **Precious Plastic injection machine.** The open reference design: a floor-standing lever press, 830 x 700 x 1,300 mm and 23 kg, with a 150 cm³ barrel, a 3:1 lever giving about 45 bar (4.5 MPa), 10 to 30 injections per hour and about €300 in new materials in the Netherlands. It runs HDPE, LDPE, PP and PS ([Precious Plastic Academy, "Injection"](https://onearmy.github.io/academy/build/injection)). MicroMold trades shot size for about twice the pressure and a bench footprint.
- **Commercial bench-top injection presses** for hobby and lab use exist, with lever or pneumatic drives. They are closed designs and usually sized for virgin pellets rather than irregular flake. No figures are cited here until sources are checked at TRL 3.
- **Processing data.** Published melt temperature ranges are 190 to 230 °C for HDPE, 200 to 240 °C for PP, 220 to 245 °C for LDPE and 180 to 260 °C for PS ([RJC Mold, "Plastic Melting Point Chart"](https://rjcmold.com/guides/plastic-melting-point-chart)).
- **Portfolio links.** WasteWise Scan (resin identification), WasteWise-ml (material classification) and ReflowEconomy (micro-factory playbook) supply sorted feedstock and the operating context.

> **Safety:** The problem involves mains-powered heaters, surfaces and melt at 180 to 260 °C, pressurized molten plastic and fumes. See the safety section of MMD-PRC-001.

## User research and co-design

This design is for communities the author is not part of, so requirements come from the people who will use it.

- [ ] Identify a local partner organization (Helpful Engineering network, NGO or university). Decided by Amish, 2026-09-25: the first partner is to be a group that already shreds HDPE or PP (MMD-DDR-001 D10); the specific partner and place are proposed, awaiting Amish. Recruiting is on hold while TRL 4 is on hold.
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate load, distance, terrain and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design

Questions to take to users: which parts would sell locally and at what price; the part size and shot size they need; how many parts per day make the press worth running; who in the group would machine molds; and what power supply is reliable.
