# 03 — The Standards Landscape

Standards do three jobs here: they give you a **precise vocabulary** so that "flat" and
"round" mean something; they give you **default rules** so a drawing without a callout is
still unambiguous; and they give you **decision rules** for judging conformity when your
measurement is itself uncertain.

Buying all of them would cost well over £2,000. Almost none of that is necessary. This
document says which matter, in what order, and what is free.

---

## 1. The two systems

There are two competing dimensioning-and-tolerancing systems in world use:

- **ISO GPS** (Geometrical Product Specification) — a *system* of ~150 interlocking
  standards. Dominant in Europe, the UK, and much of Asia. Rigorous, modular, and hard to
  learn piecemeal because each standard assumes the others.
- **ASME Y14.5** — a single, largely self-contained document. Dominant in the United States.
  Much easier to learn, because you can read one book and be functional.

They agree on most concepts and disagree on important details — most notably the default
relationship between size and form (see §2), datum reference frame construction, and the
treatment of "±" size tolerances.

**Practical recommendation.** You are in the UK, so ISO GPS is the system to *specify* in
when you send anything to a supplier. But ASME Y14.5 is the system to *learn from*, because a
single purchase gets you a complete, coherent treatment and the free teaching material for it
is far better. Learn Y14.5, then read the ISO deltas.

## 2. The one rule that matters most

**ISO 8015 — the Principle of Independency.** Under ISO, unless otherwise stated, a size
tolerance and a form tolerance are *independent*: a shaft specified Ø10 ±0.1 may be Ø9.95
everywhere and simultaneously bent 0.3 mm out of straight, and it conforms. Size says nothing
about form.

**ASME Y14.5 uses the opposite default** — Rule #1, the envelope requirement: a feature of
size at MMC must fit within a perfect-form boundary. Size *does* constrain form.

If you internalise one thing from any standard, make it this, because it is the difference
between a part that measures correct on calipers and a part that assembles. A printed boss
that measures 5.00 mm across its diameter at three heights can still be a banana. In ISO
terms, if you need the envelope requirement you must ask for it explicitly (the Ⓔ modifier).

## 3. ISO GPS: what is what

Grouped by what you would use it for.

### Fundamentals

| Standard | Covers | Priority |
|---|---|---|
| **ISO 8015:2011** | Fundamental concepts, principles and rules of GPS. The independency principle | **Read first** |
| ISO 14638:2015 | The GPS "matrix model" — how the ~150 standards relate | Useful map, low priority |
| ISO 17450-1:2011 | General concepts: the model for geometrical specification and verification | Theory |

### Size

| Standard | Covers | Priority |
|---|---|---|
| **ISO 286-1 / -2:2010** | The IT-grade code system for limits and fits (H7, h6, g6 …). Part 1 is the basis, Part 2 the tables | **High** |
| ISO 14405-1:2016 | Dimensional tolerancing of linear sizes — the modifiers that say *which* size you mean | Medium |

ISO 286 is worth understanding even though FDM lives at the coarse end of it. It gives you a
vocabulary for fits (clearance / transition / interference) and a scale to place your
process on. Published research on FDM PLA places well-calibrated desktop machines in roughly
the **IT9–IT14** band depending on nominal size and axis — see Processes 11(10):2810 (2023),
open access. Conventional machining sits at IT6–IT9; that gap is the honest measure of what
you are working with.

### Geometry

| Standard | Covers | Priority |
|---|---|---|
| **ISO 1101:2017** | The core geometrical tolerancing language: form, orientation, location, run-out. The symbols | **High** |
| ISO 5459:2011 | Datums and datum systems | High if you use GD&T seriously |
| ISO 5458:2018 | Pattern and combined specification (e.g. a bolt circle) | Medium |
| ISO 1660:2017 | Profile tolerancing | Medium |
| ISO 2692:2021 | Maximum/least material requirement (Ⓜ, Ⓛ) and reciprocity | Medium |

### General tolerances (the ones that apply when you say nothing)

| Standard | Covers | Priority |
|---|---|---|
| **ISO 2768-1:1989** | General *linear and angular* tolerances: classes f/m/c/v (fine, medium, coarse, very coarse) | **High** |
| **ISO 22081:2021** | General *geometrical* specifications. **Cancels and replaces the geometrical part of ISO 2768-2** and brings it into the ISO 8015 framework | **High** |

ISO 2768-2:1989 is superseded. If you have seen a title block saying "ISO 2768-mK", the "K"
part is the withdrawn half. Current practice is `ISO 2768-m` for sizes plus an ISO 22081
general geometrical specification referencing a datum system.

This pair is where most of your practical value is: putting `ISO 2768-m` in a title block
means every unstated dimension has a defined tolerance, and you stop having to think about
the 95% of dimensions that don't matter.

**ISO 22081 has a free preview PDF** at
[standards.iteh.ai](https://cdn.standards.iteh.ai/samples/72514/78d2a06f1b7a42ddb87e7180c790cc9c/ISO-22081-2021.pdf).

### Verification and measurement — the underrated section

| Standard | Covers | Priority |
|---|---|---|
| **ISO 14253-1:2017** | **Decision rules** for proving conformity or non-conformity when measurement uncertainty is non-negligible | **High for you** |
| ISO/IEC Guide 98-3 (GUM) | Evaluating measurement uncertainty | Reference |
| ISO 22514 series | Statistical methods: process capability and performance. Part 4 covers capability estimates; Part 2 time-dependent models | Medium |
| ISO 5725 series | Accuracy (trueness and precision) of measurement methods | Reference |

**ISO 14253-1 deserves special attention** because you will be measuring 0.1 mm effects with
a £30 caliper. Its core idea: measurement uncertainty is subtracted from the tolerance zone to
form a **guard band**. To *prove* conformity you must measure inside the reduced zone; to
*prove* non-conformity you must measure outside the expanded zone; in between, you have not
proved anything. Applied to your coupons, this stops you concluding that a 0.03 mm shift is
real when your measurement uncertainty is 0.05 mm. See
[04 §6](04-process-capability.md#6-measurement-and-its-uncertainty).

### Model-based definition

| Standard | Covers |
|---|---|
| ISO 16792:2021 | Digital product definition data practices — tolerancing on the 3D model rather than a drawing |
| ASME Y14.41-2019 | The ASME equivalent |

Relevant because your workflow has no drawings — it is CAD to slicer. Worth knowing these
exist; low priority to buy.

## 4. ASME, if you go that route

| Standard | Covers |
|---|---|
| **ASME Y14.5-2018** | Dimensioning and Tolerancing. The one book |
| ASME Y14.5.1-2019 | Mathematical definition of the Y14.5 principles. Rigorous; the reference for anyone implementing tolerance software |
| ASME Y14.41-2019 | Digital product definition |

Y14.5 §2.16 (in the 1994 edition; retained since) introduced the statistical tolerance symbol
— a tolerance so marked is to be maintained by statistical process control rather than
100% inspection. It is the standards' formal acknowledgement that statistical tolerancing
exists, and it is notably brief; the standards have never specified *how* to do the
statistics. That is why documents like Scholz (1995) exist.

**If you buy one paper standard, this is the one.** It is cheaper than the ISO set, it is
self-contained, and the surrounding ecosystem of textbooks and training material is far
richer.

## 5. Additive manufacturing standards

This is the family most 3D-printing practitioners have never heard of, and it contains the
single most directly useful document for your workflow.

| Standard | Covers | Priority |
|---|---|---|
| **ISO/ASTM 52902:2023** | **Test artefacts — geometric capability assessment of AM systems** | **Highest** |
| ISO/ASTM 52900:2021 | General principles, fundamentals and vocabulary | Reference |
| ISO/ASTM 52910:2018 | Design — requirements, guidelines and recommendations | Medium |
| ISO/ASTM 52901:2017 | Requirements for purchased AM parts | Useful if you outsource printing |
| ISO/ASTM 52903-1:2021 | Material extrusion of plastics — feedstock materials | Low |
| ISO/ASTM 52903-2:2020 | Material extrusion of plastics — process equipment. Defines process classes I–III by quality and traceability | Medium |

**ISO/ASTM 52902 is the standard that answers "how do I benchmark my printer".** It defines a
suite of test geometries — each targeting a specific performance metric — and prescribes what
to measure on them, deliberately without dictating the measurement method. It exists precisely
to let you make quantitative, comparable statements about geometric capability. It is the
formal version of what [04](04-process-capability.md) describes doing.

Note the 2019 edition was withdrawn and replaced by the 2023 edition; cite the current one.

## 6. PCB standards (IPC)

For the mechanical interface between board and enclosure, these are the relevant documents.

| Standard | Covers | Priority |
|---|---|---|
| **IPC-2615** | **Printed Board Dimensions and Tolerances.** Exactly what it says — dimensioning and tolerancing of boards and board assemblies, derived from ASME Y14.5M-1994 | **Highest for mechanical fit** |
| IPC-2221 (B/C) | Generic standard on printed board design — clearances, conductor widths, annular ring | High |
| IPC-7351B | Surface mount land patterns | Medium (electrical, but drives component position) |
| IPC-A-600 | Acceptability of printed boards — what a fab house is allowed to ship | Medium |
| IPC-6012 | Qualification and performance specification for rigid boards | Medium |
| IPC-A-610 | Acceptability of electronic assemblies | Low for fit |

IPC-2615 replaced IPC-D-300G and is *the* document for board dimensional tolerancing. It is
old (2000) and pegged to the 1994 Y14.5, but nothing has superseded it.

Working numbers for a typical low-cost fab house, to use until you have your supplier's own
specification — treat these as **spec limits, so model them as uniform**, per
[02 §8](02-methods.md):

| Feature | Typical tolerance |
|---|---|
| Board thickness | ±10%, minimum ±0.127 mm |
| Routed outline | ±0.15 to ±0.25 mm |
| Scored/V-cut outline | ±0.3 mm or worse |
| Plated hole diameter | ±0.075 mm |
| Non-plated hole diameter | ±0.05 mm |
| Hole-to-outline registration | ±0.15 mm |
| Solder mask registration | ±0.075 mm |
| Minimum annular ring, Class 2, after all tolerances | 0.05 mm (IPC-2221) |

**Always confirm against your actual supplier's published capability page** — they differ, and
the cheap options differ most. Record the source in the parameter file.

## 7. What to actually acquire

In priority order, with honest cost:

1. **Free, do it today.** ISO 22081 preview PDF (linked above). The ISO **Online Browsing
   Platform** ([iso.org/obp](https://www.iso.org/obp)) publishes the *Terms and definitions*
   section of most standards at no charge — enough to settle vocabulary questions without
   buying anything. Scholz (1995) for the methods.
2. **~£30–60.** A good GD&T textbook. This gets you 90% of the practical value of ISO 1101 +
   ISO 5459 + ASME Y14.5 without buying any of them.
3. **~£100–200.** ASME Y14.5-2018, if you want the primary source.
4. **~£100 each.** ISO 2768-1 and ISO 22081, if you start sending work to suppliers and want
   your title blocks to be defensible.
5. **~£100.** ISO/ASTM 52902:2023, if you want to run a formal capability assessment rather
   than the pragmatic version in [04](04-process-capability.md).
6. **Probably never.** The full ISO GPS set, IPC-2615, ISO 14253-1. Understand the *concepts*
   from secondary sources; buy the documents only if a customer or a certification requires
   you to cite them.

The concepts are free. The documents are what cost money, and for a one-person workshop the
concepts are what you need.

---

Previous: [02 — Methods](02-methods.md) · Next: [04 — Process capability](04-process-capability.md)
