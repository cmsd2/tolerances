# Tolerance Management for a Desktop 3D-Printing + PCB Workflow

An open, self-hosted alternative to proprietary tolerance-analysis software (RD8, CETOL 6σ,
3DCS, VisVSA), targeted at FreeCAD + KiCad + FDM printing.

The premise of this document set: **the mathematics of tolerance analysis is easy and free.
The hard parts are knowing your actual process capability, and keeping one honest source of
truth for every dimension.** Commercial tools sell you automation and a managed record. They
cannot sell you capability data for your printer, and that is the input that dominates every
result you will compute.

---

## Reading paths

**"I want to understand the subject."**
Read in order: [00](docs/00-orientation.md) → [01](docs/01-concepts.md) →
[02](docs/02-methods.md) → [03](docs/03-standards.md). Then
[09](docs/09-bibliography.md) to go deeper.

**"I want to start doing something this week."**
[00](docs/00-orientation.md) → [06](docs/06-workflow.md) → [04](docs/04-process-capability.md).
Start printing coupons on day one; they take days of wall-clock time and everything else
depends on them.

**"I need to look something up."**
[02](docs/02-methods.md) for formulas, [03](docs/03-standards.md) for which standard says
what, [05](docs/05-parameter-model.md) for the schema, [10](docs/10-glossary.md) for terms.

---

## The documents

| # | Document | What it is |
|---|---|---|
| 00 | [Orientation](docs/00-orientation.md) | The problem, what you are actually replacing, what to ignore |
| 01 | [Concepts](docs/01-concepts.md) | Variation, chains, analysis vs. synthesis, capability — with the literature |
| 02 | [Methods](docs/02-methods.md) | The mathematics: worst-case, RSS, inflation factors, mean shifts, Monte Carlo. Worked example |
| 03 | [Standards](docs/03-standards.md) | ISO GPS, ASME Y14.5, ISO/ASTM AM standards, IPC. Which to read, which to skip, what is free |
| 04 | [Process capability](docs/04-process-capability.md) | Characterising *your* printer and *your* fab house. The highest-value document here |
| 05 | [Parameter model](docs/05-parameter-model.md) | The single-source-of-truth schema and why it is shaped that way |
| 06 | [Workflow](docs/06-workflow.md) | The step-by-step procedure to follow, and where I can help |
| 07 | [FreeCAD integration](docs/07-freecad.md) | Driving the model from the parameter file; worst-case configurations |
| 08 | [KiCad and PCB](docs/08-kicad-pcb.md) | The board as a purchased part; the mechanical interface; fab tolerances |
| 09 | [Bibliography](docs/09-bibliography.md) | Annotated, marked by cost and access |
| 10 | [Glossary](docs/10-glossary.md) | Terms, with the ISO/ASME distinctions that trip people up |

Plus:

- [`notebooks/tolerance-mathematics.macnb`](notebooks/tolerance-mathematics.macnb) — a Maxima
  notebook deriving the formulas in [02](docs/02-methods.md) symbolically. It reproduces
  Scholz's distribution inflation-factor table from first principles (every value exact),
  derives the trapezoidal family in closed form, verifies that the Greenwood–Chase mean-shift
  model really does interpolate between worst case and RSS, and re-computes the worked example
  so the prose and the maths cannot drift apart. Opens in Jupyter or any `.ipynb` tool.
  Section 0 is a self-contained primer — no prior reading required.
- [`templates/parameters.example.yaml`](templates/parameters.example.yaml) — a complete,
  commented worked example of the parameter file.

---

## Status

Documentation only at this point. No code has been written yet. See
[06 — Workflow](docs/06-workflow.md) for what gets built and in what order.
