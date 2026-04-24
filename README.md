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
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ State   ┃ Elems                                 ┃  Ratio ┃ Input ┃ front_ring ┃    sun ┃ Output ┃ rear_carrier ┃ rear_ring ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1st     │ forward_clutch+sprag                  │  2.458 │ 1.000 │      1.000 │ -0.888 │  0.407 │        0.000 │     0.407 │
│ 2nd     │ forward_clutch+intermediate_band      │  1.458 │ 1.000 │      1.000 │  0.000 │  0.686 │        0.470 │     0.686 │
│ 3rd     │ forward_clutch+high_reverse_clutch    │  1.000 │ 1.000 │      1.000 │  1.000 │  1.000 │        1.000 │     1.000 │
│ Rev     │ high_reverse_clutch+low_reverse_band  │ -2.182 │ 1.000 │     -1.127 │  1.000 │ -0.458 │        0.000 │    -0.458 │
│ Manual1 │ forward_clutch+low_reverse_band+sprag │  2.458 │ 1.000 │      1.000 │ -0.888 │  0.407 │        0.000 │     0.407 │
│ Manual2 │ forward_clutch+intermediate_band      │  1.458 │ 1.000 │      1.000 │  0.000 │  0.686 │        0.470 │     0.686 │
└─────────┴───────────────────────────────────────┴────────┴───────┴────────────┴────────┴────────┴──────────────┴───────────┘
```

```text
╭─────────────────── ZF 4HP22/24 4-Speed ────────────────────╮
│ input=input   output=output   speed=1.0   geometry=relaxed │
╰────────────────────────────────────────────────────────────╯
Tooth counts: PG_overdrive(Ns=31, Nr=83), PG_front(Ns=35, Nr=73), PG_rear(Ns=35, Nr=73)
┏━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems            ┃  Ratio ┃ Input ┃ od_sun ┃ od_out ┃     r1 ┃ simpson_sun ┃ rear_carrier ┃ Output ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1st   │ A+E+J+K          │  2.479 │ 1.000 │  1.000 │  1.000 │  1.000 │      -0.841 │        0.000 │  0.403 │
│ 2nd   │ A+Cprime+C+E+H+K │  1.479 │ 1.000 │  1.000 │  1.000 │  1.000 │       0.000 │        0.457 │  0.676 │
│ 3rd   │ A+B+Cprime+E+K   │  1.000 │ 1.000 │  1.000 │  1.000 │  1.000 │       1.000 │        1.000 │  1.000 │
│ 4th   │ A+B+Cprime+F     │  0.728 │ 1.000 │  0.000 │  1.373 │  1.373 │       1.373 │        1.373 │  1.373 │
│ Rev   │ B+D+E+K          │ -2.086 │ 1.000 │  1.000 │  1.000 │ -1.189 │       1.000 │        0.000 │ -0.479 │
└───────┴──────────────────┴────────┴───────┴────────┴────────┴────────┴─────────────┴──────────────┴────────┘
```

```text
╭────────────── Mercedes-Benz W5A-580 5-Speed ───────────────╮
│ input=input   output=output   speed=1.0   geometry=relaxed │
╰────────────────────────────────────────────────────────────╯
Tooth counts: PG_forward(Ns=46, Nr=72), PG_rear(Ns=68, Nr=122), PG_middle(Ns=37, Nr=91)
┏━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems          ┃  Ratio ┃ Input ┃ forward_sun ┃ forward_carrier ┃ rear_sun ┃ rear_carrier ┃ middle_sun ┃ Output ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━┩
│ 1st   │ C3+B1+B2+F1+F2 │  3.590 │ 1.000 │       0.000 │           0.610 │    0.000 │        0.392 │      0.000 │  0.279 │
│ 2nd   │ C1+C3+B2+F2    │  2.191 │ 1.000 │       1.000 │           1.000 │    0.000 │        0.642 │      0.000 │  0.456 │
│ 3rd   │ C1+C2+B2       │  1.407 │ 1.000 │       1.000 │           1.000 │    1.000 │        1.000 │      0.000 │  0.711 │
│ 4th   │ C1+C2+C3       │  1.000 │ 1.000 │       1.000 │           1.000 │    1.000 │        1.000 │      1.000 │  1.000 │
│ 5th   │ C2+C3+B1       │  0.832 │ 1.000 │       0.000 │           0.610 │    1.699 │        1.000 │      1.699 │  1.202 │
│ R1    │ C3+BR+F1+B1    │ -3.160 │ 1.000 │       0.000 │           0.610 │   -1.095 │        0.000 │     -1.095 │ -0.316 │
│ R2    │ C1+C3+BR       │ -1.928 │ 1.000 │       1.000 │           1.000 │   -1.794 │        0.000 │     -1.794 │ -0.519 │
│ N     │ C3+B1          │  0.000 │ 1.000 │       0.000 │           0.000 │    0.000 │        0.000 │      0.000 │  0.000 │
└───────┴────────────────┴────────┴───────┴─────────────┴─────────────────┴──────────┴──────────────┴────────────┴────────┘
```

```text
╭──────────────────── Allison 2K 6-Speed ────────────────────╮
│ input=input   output=output   speed=1.0   geometry=relaxed │
╰────────────────────────────────────────────────────────────╯
Tooth counts: PG1(Ns=67, Nr=109), PG2(Ns=49, Nr=91), PG3(Ns=39, Nr=97)
┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems ┃  Ratio ┃ Input ┃  ring1 ┃ node12 ┃  sun23 ┃ node23 ┃ Output ┃
┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 1st   │ C1+C5 │  3.487 │ 1.000 │ -1.484 │ -0.538 │  1.000 │  0.000 │  0.287 │
│ 2nd   │ C1+C4 │  1.864 │ 1.000 │ -0.615 │  0.000 │  1.000 │  0.350 │  0.536 │
│ 3rd   │ C1+C3 │  1.403 │ 1.000 │  0.000 │  0.381 │  1.000 │  0.597 │  0.713 │
│ 4th   │ C1+C2 │  1.000 │ 1.000 │  1.000 │  1.000 │  1.000 │  1.000 │  1.000 │
│ 5th   │ C2+C3 │  0.752 │ 1.000 │  0.000 │  0.381 │  2.150 │  1.000 │  1.330 │
│ 6th   │ C2+C4 │  0.653 │ 1.000 │ -0.615 │  0.000 │  2.857 │  1.000 │  1.533 │
│ Rev   │ C3+C5 │ -4.932 │ 1.000 │  0.000 │  0.381 │ -0.707 │  0.000 │ -0.203 │
└───────┴───────┴────────┴───────┴────────┴────────┴────────┴────────┴────────┘
```

```text
╭───────────── Mercedes-Benz W7A-700 7-Speed ─────────────╮
│ input=input   output=out   speed=1.0   geometry=relaxed │
╰─────────────────────────────────────────────────────────╯
Tooth counts: PG_A(Ns=52, Nr=106), PG_B(Ns=78, Nr=100), PG_R(Ns=66, Nr=164), PG_M(Ns=62, Nr=168)
┏━━━━━━━┳━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems    ┃  Ratio ┃ Input ┃     fa ┃    fb ┃    fc ┃     rs ┃    rc ┃     ms ┃ Output ┃
┡━━━━━━━╇━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 1st   │ C3+B2+B3 │  4.382 │ 1.000 │ -0.707 │ 0.000 │ 0.438 │  0.000 │ 0.312 │  0.000 │  0.228 │
│ 2nd   │ C3+B1+B2 │  2.862 │ 1.000 │  0.000 │ 0.414 │ 0.671 │  0.000 │ 0.478 │  0.000 │  0.349 │
│ 3rd   │ C1+C3+B2 │  1.920 │ 1.000 │  1.000 │ 1.000 │ 1.000 │  0.000 │ 0.713 │  0.000 │  0.521 │
│ 4th   │ C1+C2+B2 │  1.369 │ 1.000 │  1.000 │ 1.000 │ 1.000 │  1.000 │ 1.000 │  0.000 │  0.730 │
│ 5th   │ C1+C2+C3 │  1.000 │ 1.000 │  1.000 │ 1.000 │ 1.000 │  1.000 │ 1.000 │  1.000 │  1.000 │
│ 6th   │ C2+C3+B1 │  0.819 │ 1.000 │  0.000 │ 0.414 │ 0.671 │  1.818 │ 1.000 │  1.818 │  1.220 │
│ 7th   │ C2+C3+B3 │  0.727 │ 1.000 │ -0.707 │ 0.000 │ 0.438 │  2.396 │ 1.000 │  2.396 │  1.376 │
│ R1    │ C3+B3+BR │ -3.407 │ 1.000 │ -0.707 │ 0.000 │ 0.438 │ -1.089 │ 0.000 │ -1.089 │ -0.294 │
│ R2    │ C3+B1+BR │ -2.225 │ 1.000 │  0.000 │ 0.414 │ 0.671 │ -1.667 │ 0.000 │ -1.667 │ -0.449 │
│ N     │ C3+B3    │  0.000 │ 1.000 │  0.000 │ 0.000 │ 0.000 │  0.000 │ 0.000 │  0.000 │  0.000 │
└───────┴──────────┴────────┴───────┴────────┴───────┴───────┴────────┴───────┴────────┴────────┘
```

```text
╭────────────────── ZF 8HP 4th Generation ───────────────────╮
│ input=input   output=output   speed=1.0   geometry=relaxed │
╰────────────────────────────────────────────────────────────╯
Tooth counts: P1(Ns=48, Nr=96), P2(Ns=54, Nr=96), P3(Ns=60, Nr=108), P4(Ns=24, Nr=96)
┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems ┃  Ratio ┃ Input ┃ sun12 ┃   p1r ┃   p23 ┃  c_out ┃ p1c_p4r ┃    p3c ┃ Output ┃
┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━┩
│ 1st   │ A+B+C │  5.000 │ 1.000 │ 0.000 │ 0.000 │ 1.562 │  1.000 │   0.000 │  1.201 │  0.200 │
│ 2nd   │ A+B+E │  3.200 │ 1.000 │ 0.000 │ 0.000 │ 1.562 │  1.562 │   0.000 │  1.562 │  0.312 │
│ 3rd   │ B+C+E │  2.143 │ 1.000 │ 1.000 │ 0.000 │ 1.000 │  1.000 │   0.333 │  1.000 │  0.467 │
│ 4th   │ B+D+E │  1.720 │ 1.000 │ 1.744 │ 0.000 │ 0.581 │  0.581 │   0.581 │  0.581 │  0.581 │
│ 5th   │ B+C+D │  1.297 │ 1.000 │ 2.141 │ 0.000 │ 0.358 │  1.000 │   0.714 │  0.771 │  0.771 │
│ 6th   │ C+D+E │  1.000 │ 1.000 │ 1.000 │ 1.000 │ 1.000 │  1.000 │   1.000 │  1.000 │  1.000 │
│ 7th   │ A+C+D │  0.833 │ 1.000 │ 0.000 │ 1.877 │ 1.562 │  1.000 │   1.251 │  1.201 │  1.201 │
│ 8th   │ A+D+E │  0.640 │ 1.000 │ 0.000 │ 2.344 │ 1.562 │  1.562 │   1.562 │  1.562 │  1.562 │
│ Rev   │ A+B+D │ -3.968 │ 1.000 │ 0.000 │ 0.000 │ 1.562 │ -1.260 │   0.000 │ -0.252 │ -0.252 │
└───────┴───────┴────────┴───────┴───────┴───────┴───────┴────────┴─────────┴────────┴────────┘
```

```text
╭───────────── Mercedes-Benz 9G-TRONIC / NAG3 9-Speed ─────────────╮
│ input=input_s1   output=output_c3   speed=1.0   geometry=relaxed │
╰──────────────────────────────────────────────────────────────────╯
Tooth counts: P1(Ns=46, Nr=98), P2(Ns=44, Nr=100), P3(Ns=36, Nr=84), P4(Ns=34, Nr=86)
┏━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems ┃  Ratio ┃ Input ┃    c1 ┃  r1_c2 ┃     s2 ┃ r2_s3_s4 ┃    r3 ┃    r4 ┃ Output ┃
┡━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ 1st   │ A+B+E │  5.503 │ 1.000 │ 0.606 │  0.421 │  0.000 │    0.606 │ 0.000 │ 1.156 │  0.182 │
│ 2nd   │ F+E+B │  3.333 │ 1.000 │ 1.000 │  1.000 │  1.000 │    1.000 │ 0.000 │ 1.000 │  0.300 │
│ 3rd   │ F+A+B │  2.315 │ 1.000 │ 1.000 │  1.000 │  0.000 │    1.440 │ 0.000 │ 0.826 │  0.432 │
│ 4th   │ A+B+D │  1.661 │ 1.000 │ 1.268 │  1.394 │  0.000 │    2.007 │ 0.000 │ 0.602 │  0.602 │
│ 5th   │ F+A+D │  1.211 │ 1.000 │ 1.000 │  1.000 │  0.000 │    1.440 │ 0.563 │ 0.826 │  0.826 │
│ 6th   │ F+E+D │  1.000 │ 1.000 │ 1.000 │  1.000 │  1.000 │    1.000 │ 1.000 │ 1.000 │  1.000 │
│ 7th   │ E+A+D │  0.865 │ 1.000 │ 0.606 │  0.421 │  0.000 │    0.606 │ 1.392 │ 1.156 │  1.156 │
│ 8th   │ C+E+D │  0.717 │ 1.000 │ 0.000 │ -0.469 │ -1.536 │    0.000 │ 1.993 │ 1.395 │  1.395 │
│ 9th   │ C+A+D │  0.601 │ 1.000 │ 0.000 │ -0.469 │  0.000 │   -0.676 │ 2.665 │ 1.663 │  1.663 │
│ Rev   │ C+A+B │ -4.932 │ 1.000 │ 0.000 │ -0.469 │  0.000 │   -0.676 │ 0.000 │ 1.663 │ -0.203 │
└───────┴───────┴────────┴───────┴───────┴────────┴────────┴──────────┴───────┴───────┴────────┘
```

```text
╭──────────────── Ford 10R80 / 10R 10-Speed ─────────────────╮
│ input=input   output=output   speed=1.0   geometry=relaxed │
╰────────────────────────────────────────────────────────────╯
Tooth counts: P1(Ns=45, Nr=99), P2(Ns=51, Nr=89), P3(Ns=63, Nr=101), P4(Ns=23, Nr=85)
┏━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━┓
┃ State ┃ Elems   ┃  Ratio ┃ Input ┃    r1 ┃   s12 ┃  r4c1 ┃  r2s3 ┃   r3s4 ┃ interm ┃   p3c ┃ Output ┃
┡━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━┩
│ 1st   │ A+B+D+E │  4.696 │ 1.000 │ 0.000 │ 0.000 │ 0.000 │ 1.573 │  1.000 │  1.220 │ 1.220 │  0.213 │
│ 2nd   │ A+B+C+D │  2.985 │ 1.000 │ 0.000 │ 0.000 │ 0.000 │ 1.573 │  1.573 │  1.573 │ 1.573 │  0.335 │
│ 3rd   │ A+C+D+E │  2.179 │ 1.000 │ 0.000 │ 1.000 │ 0.312 │ 1.000 │  1.000 │  1.000 │ 1.000 │  0.459 │
│ 4th   │ A+C+D+F │  1.801 │ 1.000 │ 0.000 │ 1.776 │ 0.555 │ 0.555 │  0.555 │  0.555 │ 0.555 │  0.555 │
│ 5th   │ A+C+E+F │  1.539 │ 1.000 │ 0.000 │ 1.776 │ 0.555 │ 0.555 │  1.000 │  0.555 │ 0.829 │  0.650 │
│ 6th   │ A+D+E+F │  1.288 │ 1.000 │ 0.000 │ 2.291 │ 0.716 │ 0.260 │  1.000 │  0.716 │ 0.716 │  0.776 │
│ 7th   │ C+D+E+F │  1.000 │ 1.000 │ 1.000 │ 1.000 │ 1.000 │ 1.000 │  1.000 │  1.000 │ 1.000 │  1.000 │
│ 8th   │ B+D+E+F │  0.852 │ 1.000 │ 1.775 │ 0.000 │ 1.220 │ 1.573 │  1.000 │  1.220 │ 1.220 │  1.173 │
│ 9th   │ B+C+E+F │  0.689 │ 1.000 │ 2.288 │ 0.000 │ 1.573 │ 1.573 │  1.000 │  1.573 │ 1.220 │  1.451 │
│ 10th  │ B+C+D+F │  0.636 │ 1.000 │ 2.288 │ 0.000 │ 1.573 │ 1.573 │  1.573 │  1.573 │ 1.573 │  1.573 │
│ Rev   │ A+B+D+F │ -4.786 │ 1.000 │ 0.000 │ 0.000 │ 0.000 │ 1.573 │ -0.981 │  0.000 │ 0.000 │ -0.209 │
└───────┴─────────┴────────┴───────┴───────┴───────┴───────┴───────┴────────┴────────┴───────┴────────┘
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
