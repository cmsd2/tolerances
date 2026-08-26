# 08 — KiCad and the PCB Mechanical Interface

The PCB is where two variation regimes meet: a controlled industrial process with tolerances
in the 0.05–0.25 mm range, and a desktop printer with tolerances several times larger. Almost
every enclosure-fit failure lives at this boundary.

The mental model that makes this tractable: **treat the PCB as a purchased part with a
datasheet.** You do not control its variation; you look it up, you model it as a uniform
distribution over the stated limits, and you verify it on the first article.

*API specifics below are illustrative — KiCad's Python API changes between major versions.
Prefer `kicad-cli` and `kiutils`, which are more stable than `pcbnew` bindings.*

---

## 1. The mechanical interface list

The dimensions that cross from the electrical domain into the mechanical one. Every one
belongs in `parameters.yaml`.

| Quantity | Typically from | Feeds |
|---|---|---|
| Board outline X, Y | KiCad Edge.Cuts | cavity size |
| Board thickness | fab spec | lid/boss stack |
| Mounting hole positions | KiCad | boss positions |
| Mounting hole diameter | KiCad + fab tolerance | screw clearance |
| Connector position on board | KiCad footprint placement | aperture position |
| Connector body dimensions | component datasheet | aperture size |
| Connector height above board | datasheet | cavity height |
| Tallest component height | datasheet | cavity height |
| Keep-out zones | KiCad courtyards | internal ribs, bosses |

## 2. Getting numbers out of KiCad

Two routes. Prefer the second for scripting.

**`pcbnew` Python bindings** — full-featured, requires KiCad's own Python. Internal units are
nanometres; `pcbnew.ToMM()` converts.

```python
import pcbnew
board = pcbnew.LoadBoard("pcb/controller.kicad_pcb")

bbox = board.GetBoardEdgesBoundingBox()
outline_x = pcbnew.ToMM(bbox.GetWidth())
outline_y = pcbnew.ToMM(bbox.GetHeight())

for fp in board.GetFootprints():
    if fp.GetReference() == "J1":
        pos = fp.GetPosition()
        j1_x, j1_y = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
```

**`kiutils`** — a pure-Python parser for KiCad's s-expression files. No KiCad installation
needed, so it works in CI, and it does not break when KiCad changes its C++ bindings. Slower
and lower-level, but for extracting a handful of coordinates that does not matter. This is the
better choice for a build script.

**`kicad-cli`** — the supported command-line interface (KiCad 7+). Use it for exports:

```sh
kicad-cli pcb export step --output pcb/controller.step pcb/controller.kicad_pcb
kicad-cli pcb export drc  --output reports/drc.rpt      pcb/controller.kicad_pcb
```

## 3. Which direction should the sync go?

Genuinely a judgement call, and it depends on which constrains which.

- **Enclosure-led** (YAML → KiCad): the box has an existing size, so the board must fit. Push
  the outline and mounting holes into the board.
- **Board-led** (KiCad → YAML): the electronics determine the size, and the enclosure follows.
  Extract the outline and hole positions into the parameter file.

**Board-led is the usual and better default.** The board's size is driven by component
placement and routing, which are hard constraints; the enclosure is soft. Extract from KiCad,
and let the enclosure parameters be derived.

Whichever direction you choose, **also write a consistency check that runs the other way**
and fails loudly on disagreement. That check is the thing that catches the "PCB grew 2 mm
three weeks ago and nobody told the enclosure" failure, which is the single most common way
this goes wrong.

## 4. Fabrication tolerances

Working numbers for typical low-cost fab. **Confirm against your actual supplier's capability
page, and record the URL and read-date in the parameter file** — these change.

| Feature | Typical | Model as |
|---|---|---|
| Board thickness | ±10%, min ±0.127 mm | Normal (fabs control this well) |
| Routed outline | ±0.15 to ±0.25 mm | Uniform |
| V-scored outline | ±0.3 mm or worse | Uniform |
| Plated hole diameter | ±0.075 mm | Uniform |
| Non-plated hole diameter | ±0.05 mm | Uniform |
| Hole-to-outline registration | ±0.15 mm | Uniform |
| Layer-to-layer registration | ±0.075 mm | Uniform |
| Solder mask registration | ±0.075 mm | Uniform |
| Min annular ring, Class 2, after tolerances | 0.05 mm | IPC-2221 limit |

**The one people miss: hole-to-outline registration.** Drilling and routing may reference
different datums, so the error between a mounting hole and the board edge is *not* the
individual hole tolerance — it is the registration figure, and it is usually larger. Since
your printed bosses locate against the cavity walls (i.e. the board *edge*), this is the
tolerance that actually governs whether your screws line up. Get it right and you will avoid
the classic "the holes are perfect but nothing lines up" result.

Model as uniform, not normal — see [02 §8](02-methods.md). A supplier's ± is a limit they
undertake not to exceed, not a 3σ figure, and treating it as 3σ understates the tails by a
lot.

## 5. Worked chain: a USB-C aperture in a printed wall

The canonical failure. The plug must enter the aperture; a USB-C receptacle offers roughly
±0.4 mm of positional latitude before the plug fouls.

The chain, from the enclosure datum to the connector opening:

| # | Contributor | Typical | Source |
|---|---|---|---|
| 1 | Board edge to connector centre, as designed | nominal | KiCad, exact |
| 2 | Board outline routing tolerance | ±0.20 | fab spec, uniform |
| 3 | Connector placement on board | ±0.10 reflow / ±0.30 hand-solder | assembly |
| 4 | Connector body to its own footprint centre | ±0.15 | datasheet |
| 5 | Board seating clearance in the cavity | ±0.25 | design + printed cavity |
| 6 | Printed wall position relative to cavity datum | ±0.20 | printer, external XY |
| 7 | Printed aperture position within the wall | ±0.15 | printer, external XY |

    Worst case: 0.20 + 0.10 + 0.15 + 0.25 + 0.20 + 0.15 = 1.05 mm  ✗  (budget ±0.4)

    RSS: √(0.04 + 0.01 + 0.0225 + 0.0625 + 0.04 + 0.0225) = √0.1975 = 0.44 mm  ✗ (marginal)

**Both fail.** And this is with reflow assembly; hand-soldered, contributor 3 triples and it
gets worse.

Contribution ranking: board seating clearance (31.6%), board routing (20.3%), wall position
(20.3%), connector body (11.4%), aperture position (11.4%), placement (5.1%).

The instructive part is that **no tolerance tightening fixes this.** Even eliminating the top
contributor entirely leaves RSS at 0.37 mm against a 0.4 mm budget. The answer has to be a
design change, and the options are exactly the moves from
[06](06-workflow.md#design-moves-that-beat-tolerance-analysis):

- **Oversize the aperture and add a generous internal chamfer.** Removes contributors 6 and 7
  from mattering and guides the plug. Nearly free.
- **Locate the board off the connector, not the board edge.** Make the aperture the locating
  feature: a close-fitting pocket around the connector body, with the board floating on
  slotted mounting holes. This deletes contributors 2 and 5 — the two largest — from the
  chain entirely. This is the right answer and it is the one a stack-up tool will never
  suggest.
- **Use a panel-mount connector on a pigtail.** Decouples the domains completely at the cost
  of a cable.
- **Recess the receptacle** behind a larger opening so the plug's own moulding does the
  guiding.

That third bullet is the general principle worth extracting: **choose your datum to be the
feature that matters.** Locating the board by its edge when what you care about is the
connector position is a self-inflicted wound.

## 6. Encoding fab limits as design rules

KiCad supports custom design rules in a `.kicad_dru` file alongside the board, in
s-expression syntax:

```
(version 1)

(rule "min annular ring"
    (constraint annular_width (min 0.13mm))
    (condition "A.Type == 'Via'"))

(rule "edge clearance"
    (constraint edge_clearance (min 0.3mm))
    (condition "A.Type != 'Zone'"))
```

Two ready-made rule sets for common fabs, worth starting from rather than writing your own:

- [`labtroll/KiCad-DesignRules`](https://github.com/labtroll/KiCad-DesignRules) — JLCPCB
- [`Cimos/KiCad-CustomDesignRules`](https://github.com/Cimos/KiCad-CustomDesignRules) —
  JLCPCB and PCBWay, validated against a test board

Note that custom rules are evaluated *after* the board's own constraints, and the more
restrictive value wins — so a global setting looser than your custom rule is harmless, but one
that is tighter will silently dominate.

DRC does not check mechanical fit. Encoding fab limits here protects the board; the enclosure
chain is still yours to analyse.

## 7. Checking fit in 3D

`kicad-cli pcb export step` produces a STEP model of the board and its components, which you
can import into FreeCAD and check against the enclosure.

**What this catches:** gross interference, a component you forgot about, a connector fouling a
rib, insufficient headroom.

**What it does not catch, and this is the important caveat:** the STEP model is *nominal*.
Component 3D models are idealised and frequently wrong — many are community-contributed,
some are approximate, some are simply the wrong part. A visual clearance check in FreeCAD
tells you nothing about variation, and it can tell you nothing reliable about a component
whose model nobody verified.

So: use the STEP import for gross checks and visualisation. Take critical component
dimensions — connector heights, body sizes, keep-outs — **from the datasheet**, into
`parameters.yaml`, with the datasheet as the `reference`. Never from a 3D model you did not
author.

## 8. Component placement accuracy

Fabrication tolerance covers the bare board. Where the assembler *put* the part is separate:

| Method | Typical placement accuracy |
|---|---|
| Machine pick-and-place, reflow | ±0.05 mm machine, improved by self-alignment on small passives |
| Machine placement, large connectors | ±0.10 mm — self-alignment is weak on heavy parts |
| Hand soldering, through-hole | ±0.3 mm or worse, and often tilted |
| Hand soldering, SMD connector | highly variable; measure your own |

Get real numbers from your assembly house if you use one. If you hand-solder, **measure your
own placement on a scrap board** — this is a five-minute characterisation that most people
skip, and for a hand-built prototype it is frequently the largest single contributor in the
chain.

---

## Reading

- **IPC-2615**, *Printed Board Dimensions and Tolerances* — the definitive document, derived
  from ASME Y14.5M-1994. Superseded IPC-D-300G. Dated but unreplaced.
- **IPC-2221**, generic printed board design — clearances, annular ring, conductor widths.
- **IPC-7351B**, surface mount land patterns.
- **IPC-A-600** / **IPC-6012** — what a fab house is permitted to ship you.

---

Previous: [07 — FreeCAD](07-freecad.md) · Next: [09 — Bibliography](09-bibliography.md)
