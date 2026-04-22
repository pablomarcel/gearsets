# Transmissions

**Universal planetary-gearset automatic transmission analyzer for gearheads.**

Transmissions is a Python-based analyzer for **planetary automatic transmissions** that lets you define a transmission as data, not hardcoded logic. You describe the **topology** and the **shift schedule** in JSON, and the solver computes **gear ratios** and **member speeds** across transmission states using a generic kinematic core.

That makes it practical for exploring and comparing real-world automatic transmissions such as:

- Ford C4 3-speed
- ZF 4HP22 4-speed
- ZF 5HP24 5-speed
- Mercedes W5A-580 5-speed
- Allison 2000 series 6-speed
- Mercedes W7A-700 7-speed
- ZF 8HP 8-speed
- Mercedes W9A-700 9-speed
- Ford 10R80 10-speed

## Why this is cool

Most transmission scripts are one-off throwaways tied to one architecture. This package aims to be different.

Here, the transmission is modeled through:

- a **transmission spec JSON**
- a **shift schedule JSON**

So instead of writing a brand-new solver for every gearbox, you can describe the machine and let the app solve it.

This is especially appealing if you like:

- automatic transmissions
- planetary gearsets
- gear ratio analysis
- kinematic architecture studies
- reverse engineering production transmissions
- comparing multiple OEM transmission families

## What it does

The app solves for:

- **gear ratios**
- **member speeds**
- **state-by-state applied elements**
- **topology summaries**
- **clean CLI tables**

It works well for **3, 4, 5, 6, 7, 8, 9, and 10-speed planetary automatic transmissions** built from simple planetary sets and shift elements.

## What it does not do yet

- **Ravigneaux gearsets are not yet truly supported in the universal core**
- the included Ravigneaux JSONs were handled with a dedicated workaround/script path
- this is currently a **kinematic analyzer**, not a torque-capacity, efficiency, hydraulics, or durability simulator

## Example CLI output

The CLI produces clean tabular summaries that are actually pleasant to read.

Example style:

```text
╭───────────────────────── Ford C4 3-Speed ─────────────────────────╮
│ input=input   output=front_carrier   speed=1.0   geometry=relaxed │
╰───────────────────────────────────────────────────────────────────╯
Tooth counts: PG_front(Ns=33, Nr=72), PG_rear(Ns=33, Nr=72)
┏━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ State   ┃     Ratio ┃ Status            ┃ Elems                                 ┃
┡━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 1st     │  2.458333 │ output_determined │ forward_clutch+sprag                  │
│ 2nd     │  1.458333 │ output_determined │ forward_clutch+intermediate_band      │
│ 3rd     │  1.000000 │ output_determined │ forward_clutch+high_reverse_clutch    │
│ Rev     │ -2.181818 │ output_determined │ high_reverse_clutch+low_reverse_band  │
│ Manual1 │  2.458333 │ output_determined │ forward_clutch+low_reverse_band+sprag │
│ Manual2 │  1.458333 │ output_determined │ forward_clutch+intermediate_band      │
└─────────┴───────────┴───────────────────┴───────────────────────────────────────┘
```

That gives you, in one glance:

- the transmission being analyzed
- the tooth counts used
- every gear state
- the calculated ratio
- the active elements for that state

When you enable speed display mode, the app can also print **member-by-member speed tables**, which is great for understanding what each sun, ring, carrier, or shaft is doing in each gear.

## Real transmission examples included

The repository includes JSON-defined examples for transmissions such as:

- **Ford C4**
- **Ford 10R80**
- **ZF 4HP**
- **ZF 5HP**
- **ZF 8HP**
- **Mercedes W5A-580**
- **Mercedes W7A-700**
- **Mercedes W9A-700**
- **Allison 2000 series**

That alone makes the package interesting to transmission enthusiasts, because names like **ZF 8HP** and **Ford 10R80** immediately connect the tool to real production hardware.

## How the model works

The universal solver is based on a generic transmission representation:

1. **Gearsets** define each planetary set by tooth counts and member names.
2. **Clutches / brakes / sprags** define the shift elements.
3. **Permanent ties** define members that are always connected.
4. **Shift schedule states** define which constraints are active in each gear.

The core then assembles the kinematic equations and solves the system.

## Input JSON structure

### 1) Transmission spec JSON

The transmission spec describes the physical architecture.

Typical fields include:

- `name`
- `input_member`
- `output_member`
- `strict_geometry`
- `members`
- `speed_display_order`
- `speed_display_labels`
- `gearsets`
- `clutches` or richer clutch schema
- `brakes`
- `sprags`
- `permanent_ties`
- `display_order`
- `state_aliases`
- `presets`
- `notes`
- `meta`

Example:

```json
{
  "name": "Ford C4 3-Speed",
  "input_member": "input",
  "output_member": "front_carrier",
  "strict_geometry": false,
  "members": [
    "input",
    "front_ring",
    "sun",
    "front_carrier",
    "rear_ring",
    "rear_carrier"
  ],
  "gearsets": [
    {
      "name": "PG_front",
      "Ns": 33,
      "Nr": 72,
      "sun": "sun",
      "ring": "front_ring",
      "carrier": "front_carrier"
    },
    {
      "name": "PG_rear",
      "Ns": 33,
      "Nr": 72,
      "sun": "sun",
      "ring": "rear_ring",
      "carrier": "rear_carrier"
    }
  ],
  "clutches": [
    { "name": "forward_clutch", "a": "input", "b": "front_ring" },
    { "name": "high_reverse_clutch", "a": "input", "b": "sun" }
  ],
  "brakes": [
    { "name": "intermediate_band", "member": "sun" },
    { "name": "low_reverse_band", "member": "rear_carrier" }
  ],
  "sprags": [
    {
      "name": "sprag",
      "member": "rear_carrier",
      "hold_direction": "negative",
      "locked_when_engaged": true
    }
  ],
  "permanent_ties": [
    ["front_carrier", "rear_ring"]
  ]
}
```

### 2) Shift schedule JSON

The shift schedule describes what is applied in each gear.

Typical fields include:

- `states`
- `display_order`
- `notes`

Rich-state example:

```json
{
  "states": {
    "1st": {
      "active_constraints": ["forward_clutch", "sprag"],
      "display_elements": ["forward_clutch", "sprag"],
      "manual_neutral": false,
      "notes": "Drive 1st"
    },
    "2nd": {
      "active_constraints": ["forward_clutch", "intermediate_band"],
      "display_elements": ["forward_clutch", "intermediate_band"],
      "manual_neutral": false,
      "notes": "Drive 2nd"
    },
    "3rd": {
      "active_constraints": ["forward_clutch", "high_reverse_clutch"],
      "display_elements": ["forward_clutch", "high_reverse_clutch"],
      "manual_neutral": false,
      "notes": "Drive 3rd"
    }
  },
  "display_order": ["1st", "2nd", "3rd"]
}
```

This schema is practical because it lets you define:

- traditional forward gears
- reverse
- manual ranges
- rich display labels
- neutral-like states when needed

## Why the JSON approach matters

The JSON-driven architecture is the main selling point.

Instead of baking a Ford C4 solver, a ZF 8HP solver, and a 10R80 solver into separate piles of hardcoded logic, this app lets you reuse the same engine across many transmissions.

That means you can:

- experiment with tooth counts
- swap topologies
- compare architectures
- test candidate ratios
- build reference cases
- create your own transmission studies

## CLI usage

Typical run:

```bash
python -m cli \
  --spec in/transmission_spec_ford_c4.json \
  --schedule in/shift_schedule_ford_c4.json
```

Show member speeds:

```bash
python -m cli \
  --spec in/transmission_spec_zf_8hp.json \
  --schedule in/shift_schedule_zf_8hp.json \
  --show-speeds
```

Solve one state only:

```bash
python -m cli \
  --spec in/transmission_spec_ford_10R80.json \
  --schedule in/shift_schedule_ford_10R80.json \
  --state 8th \
  --show-speeds
```

Use a preset:

```bash
python -m cli \
  --spec in/transmission_spec_zf_8hp.json \
  --schedule in/shift_schedule_zf_8hp.json \
  --preset base \
  --ratios-only
```

Override tooth counts from the CLI:

```bash
python -m cli \
  --spec in/transmission_spec_zf_8hp.json \
  --schedule in/shift_schedule_zf_8hp.json \
  --set P4.Ns=23 P4.Nr=85
```

## GUI

A Dear PyGui frontend is included for interactive use.

Run:

```bash
python -m gui_core_trans
```

The GUI supports:

- picking existing spec and schedule files
- building new transmission specs
- building new shift schedules
- running the analyzer
- browsing topology, payload, logs, and report outputs

## Why someone else might care

This project can be useful for:

- transmission enthusiasts
- geartrain hobbyists
- automotive engineers
- students studying automatic transmissions
- anyone reverse engineering planetary gearbox layouts
- anyone who wants a reusable transmission kinematics sandbox

If you have ever looked at a **ZF 8HP**, **Ford 10R80**, or **Mercedes 9-speed** and wanted to understand the geartrain in a programmable way, this package is aimed directly at that kind of curiosity.

## Current status

The app is already useful and interesting right now for universal planetary transmission studies.

It is especially good at:

- solving real named automatic transmissions
- printing attractive ratio tables
- exposing member speeds
- making transmission architecture data-driven instead of hardcoded

## Roadmap ideas

Natural future upgrades include:

- real universal support for **Ravigneaux** gearsets
- compound architecture expansion
- improved sprag behavior modeling
- richer topology visualization
- exportable reports
- ratio comparison utilities
- torque flow and power flow extensions

## Disclaimer

This tool is a **kinematic analyzer**. It does not yet model:

- clutch capacity
- hydraulic controls
- dynamic shifts
- losses/efficiency
- durability
- thermal behavior

Use it as a topology-and-ratio engine, not as a full transmission design validation suite.

## Summary

Transmissions is a **universal planetary automatic transmission analyzer** that turns JSON-defined topology and shift schedules into practical gear-ratio and member-speed results.

If production transmission names like **Ford 10R80**, **ZF 8HP**, **Mercedes W9A-700**, and **Allison 2000** catch your attention, this repo gives you a programmable way to explore how those machines behave.
