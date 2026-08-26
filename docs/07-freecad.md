# 07 — FreeCAD Integration

Goal: the FreeCAD model contains **no typed dimensions**. Every number that matters comes from
`parameters.yaml`, via a spreadsheet.

*API specifics below are illustrative — FreeCAD's Python API shifts between major versions.
Verify against your installed version before building on them.*

---

## 1. The mechanism

FreeCAD's **Spreadsheet workbench** provides named cells. Give a cell an alias (right-click →
Alias, or `sheet.setAlias('B2', 'boss_height')`), and any numeric field anywhere in the
document can reference it through the expression engine:

    Spreadsheet.boss_height

The same syntax works in a sketch constraint, a Pad length, a placement, a pattern count —
the expression engine is uniform across FreeCAD. Labels containing awkward characters are
escaped as `<<My Label>>`.

That is the whole mechanism. The spreadsheet becomes the model's control panel, and our job is
to generate it from the YAML rather than typing into it.

## 2. Naming conventions

Aliases must match parameter IDs in `parameters.yaml` exactly. Adopt:

- `snake_case`, no leading digits (FreeCAD rejects aliases starting with a digit)
- prefix by part: `encl_cavity_height`, `lid_rib_height`, `pcb_thickness`
- suffix derived values: `encl_wall_thickness_x2`
- never abbreviate inconsistently — `ht` in one place and `height` in another will cost you an
  hour eventually

Reserve one spreadsheet named `Params` per document, holding *only* generated values, and a
second named `Derived` for spreadsheet-internal formulas you write by hand. Never mix
generated and hand-written cells in one sheet: the sync script overwrites, and it will eat
your formulas.

## 3. Generating the spreadsheet from YAML

Headless, via `FreeCADCmd` (macOS:
`/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd`):

```python
import FreeCAD, yaml

params = yaml.safe_load(open("params/parameters.yaml"))
doc = FreeCAD.openDocument("cad/enclosure.FCStd")
sheet = doc.getObject("Params") or doc.addObject("Spreadsheet::Sheet", "Params")

row = 1
sheet.set(f"A{row}", "parameter"); sheet.set(f"B{row}", "value")
sheet.set(f"C{row}", "source");    sheet.set(f"D{row}", "note")

for name, p in params["parameters"].items():
    row += 1
    sheet.set(f"A{row}", name)
    sheet.set(f"B{row}", str(p["nominal"]))
    sheet.setAlias(f"B{row}", name)
    sheet.set(f"C{row}", p.get("source", "?"))
    sheet.set(f"D{row}", p.get("description", ""))

doc.recompute()
doc.save()
```

Carrying `source` and `description` into columns C and D costs nothing and means the
provenance is visible while you are modelling — which is when you most need to know whether a
number is real.

Run it as: `FreeCADCmd tools/sync_freecad.py`

**Sync is one-directional: YAML → FreeCAD.** If you change a value in the spreadsheet it will
be silently reverted on the next sync. This is the correct behaviour and should be documented
at the top of the sheet, in a cell, in capitals.

## 4. Modelling at nominal

Model everything at nominal. Do **not** model at MMC/LMC or build tolerance offsets into the
geometry — that conflates design intent with process compensation and makes the model
unusable when you change printers. Process compensation lives in the slicer
([04 §9](04-process-capability.md)).

The one exception worth making: where a *functional* clearance is a design decision rather
than a process artefact — a 0.3 mm gap you have deliberately chosen for a sliding fit — model
it, and make it a named parameter so it appears in stacks.

## 5. Worst-case and extreme-condition checks

The parametric model gives you something a spreadsheet stack-up cannot: an actual geometric
check at the tolerance extremes.

Procedure:

1. Generate a variant parameter set at the worst-case combination for the chain of interest —
   the analysis tool knows the signs, so it knows which direction each parameter goes.
2. Sync it into the spreadsheet, recompute.
3. Check for interference: Part workbench → Boolean → **Intersection** of the two solids. A
   non-empty, non-zero-volume result is an interference, and `shape.Volume` gives you the
   magnitude.
4. Restore nominal.

This catches an entire class of error that 1D stack-ups miss: interference somewhere other
than where you drew your chain. It is slow and manual, so reserve it for key characteristics.

The same loop, driven by sampled rather than extreme values, is the Monte-Carlo-over-CAD
approach in [02 §11](02-methods.md). At a second or two per recompute, a few thousand samples
is an overnight job — viable, occasionally necessary, rarely worth it.

## 6. Practical cautions

**Topological naming.** FreeCAD's long-standing weakness: sketches and features reference
faces and edges by generated names, and changing a parameter enough to alter the topology can
re-map those names and break downstream features. FreeCAD 1.0 introduced substantial
mitigation but it is not wholly solved.

Consequences for this workflow, and they are real:

- **Sketch on datum planes**, not on model faces, wherever a downstream feature depends on it.
- **Keep parameter sweeps modest.** A worst-case check moving a dimension by 0.3 mm is fine.
  A Monte Carlo that occasionally makes a wall thickness negative will produce broken
  recomputes, and — worse — recomputes that *appear* to succeed.
- **Always check the recompute succeeded** before trusting a measurement:
  `doc.recompute()` then inspect `obj.State` / `doc.RecomputesFrozen`, and treat any object
  in error as a failed sample rather than a valid one. Silently averaging over broken
  geometry is the failure mode to guard against.

**Spreadsheet recompute order.** Deep chains of spreadsheet formulas referencing each other
can require two recomputes to settle. If a synced value doesn't propagate, recompute twice
before debugging anything else.

**Units.** Cells set as bare numbers are unitless; FreeCAD interprets them per the field they
feed. Setting `'5.0'` into a length field gives 5 mm under default preferences, but this is
preference-dependent. Setting `'5.0 mm'` explicitly is unambiguous and worth the extra
characters.

## 7. What FreeCAD does not give you

- **No tolerance analysis.** There is no stack-up capability, native or in any mature addon.
  That is what this project builds.
- **GD&T annotation is limited.** TechDraw carries geometric-tolerance symbols, but it is a
  drafting aid, not a semantic model — nothing validates your datum scheme or propagates
  tolerance information into geometry. It is fine for producing a drawing a supplier will
  read; it is not model-based definition in the ISO 16792 sense.
- **No variational geometry.** The model is a single nominal configuration. Perturbation
  means recompute, which is why CAD-based Monte Carlo is slow.

None of this is a problem, because the analysis lives outside the CAD tool by design. The CAD
tool's job is to be driven by the parameter file and to render nominal geometry faithfully.

---

Previous: [06 — Workflow](06-workflow.md) · Next: [08 — KiCad and PCB](08-kicad-pcb.md)
