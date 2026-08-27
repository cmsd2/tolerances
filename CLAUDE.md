# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

An open alternative to proprietary tolerance-analysis software (RD8, CETOL 6σ, 3DCS) for a
one-person FreeCAD + KiCad + FDM-printing workflow.

**There is no analysis code yet — no tests, no application build.** The twelve Maxima
notebooks are the design; notebook `06-workflow` §"What to build, in order" is the
implementation plan. When tooling gets written, add its commands to this file.

## The documents are notebooks

Every document is a Maxima notebook under `notebooks/{guide,mathematics}/*.macnb` (Jupyter
`.ipynb` JSON with a maxima kernel). There are no Markdown sources — the notebooks are the
source of truth. `docs/pages/` is a gitignored build product.

```sh
uv venv && uv pip install "maxima-nbconvert[plotly] @ git+https://github.com/cmsd2/maxima-nbconvert"
AXIMAR_MCP=path/to/aximar-mcp ./build.sh   # execute all, export HTML, regenerate index
make docs/pages/02-methods.html            # rebuild one notebook
make serve                                 # build + serve on :8000
make import-md FILE=draft.md               # convert a new Markdown draft into a notebook
```

`.github/workflows/pages.yml` does the same thing in CI and publishes to GitHub Pages. Note
this differs from `maxima-demos` and the journey repos, which render locally and commit
`docs/pages`; here CI renders, so the site always matches the notebooks.

Editing notebooks: use the `aximar` MCP tools, and run each cell after changing it.
`maxima-nbconvert` is **not on PyPI** — install it from git, as above.

## The domain decisions that pervade everything

These are the non-obvious choices the whole design rests on. Violating one silently produces
plausible, wrong answers.

**Dimensions are `(offset, spread)`, never `±T`.** FDM error is dominated by *systematic,
directional* bias — external features run oversize, holes run undersize, repeatably — with
comparatively small random spread. A symmetric ± both overstates the randomness and hides the
offset. See `04-process-capability` §1.

**Correlation is first-class, and it cuts both ways.** Features on one printed part share a
first-layer offset, flow calibration and thermal history, so RSS's independence assumption
fails routinely. The sign structure of the chain decides the direction: same-sign terms
accumulate common-mode error, opposite-sign terms cancel it. Worked both ways in `02-methods`
§10 and notebook §7 — a ~22,000× swing in failure rate. Never assume RSS is the conservative
choice.

**A supplier's `±` is a spec limit, not a 3σ.** Model datasheet and fab-house tolerances as
**uniform**, not normal. Reaching for the normal distribution by default is the single most
common way to understate tails here. See `02-methods` §8.

**`source:` is the trust boundary.** Every parameter is `measured` / `supplier_spec` /
`standard` / `assumed`. All four are legitimate; not knowing which is not. Any analysis output
must list its `assumed` inputs separately.

**Compensate in exactly one place.** Process bias is corrected in the slicer profile *or* in
the CAD model, never both, and the location is recorded in the parameter file. `04-process-capability` §9.

**Sync is one-directional: YAML → FreeCAD/KiCad.** Values edited in a FreeCAD spreadsheet are
expected to be overwritten. Board geometry is normally extracted *from* KiCad into the YAML
(board-led), with a consistency check running the other way. `07-freecad` §3, `08-kicad-pcb` §3.

## Cross-file invariants

**Worked examples are computed, never transcribed.** `02-methods` §10 and `08-kicad-pcb` §5
define their chains in a Maxima cell and derive every figure from it; the maths notebook §6–7
recomputes the first one independently as a cross-check. Two computed results agreeing is a
feature — two *typed* results are drift waiting to happen. If you add a numeric claim to any
notebook, compute it. (Converting these to live cells immediately caught an arithmetic error
in the original hand-written prose.)

**Prose still holds interpretations, and those have numbers in them** — "about 1 in 300",
"roughly eight-fold". Re-run the notebook and check the narrative still matches before
committing.

**Notebooks are a numbered, cross-linked sequence.** Links between them point at the *rendered*
flat site (`05-parameter-model.html`, `tolerance-mathematics.html`), not at file paths.
`tools/md2macnb.py` holds the link-rewriting rules. Adding or renumbering a notebook means
updating the `README.md` table too.

**KaTeX, not MathJax, renders the maths** (loaded from CDN by the exporter, with auto-render
for `$…$`). Keep markdown-cell LaTeX to a conservative subset — see the notebook section
below — and keep `$` balanced within a cell.

**Reports are committed on purpose; raw measurement data is never edited.** `reports/` is
version-controlled so a diff shows "this change moved the lid clearance failure rate from
0.1% to 3%". Raw CSVs under `params/capability/campaigns/` are evidence — corrections go in a
separate file with a reason. `05-parameter-model` §5.

## When writing the tooling

Build order and dependencies are in `06-workflow`; the schema is `05-parameter-model` with a complete worked
instance in `templates/parameters.example.yaml`. The minimum viable system is the loader, the
analysis engine and the report generator.

**Expression evaluation must not use `eval()`.** Stack definitions carry arithmetic as strings
from a config file. Use `ast.parse(mode="eval")` with a node whitelist, or `simpleeval` /
`asteval`. `05-parameter-model` §4 specifies this.

**Report all four methods every time** — worst case, RSS, Monte Carlo, and the contribution
ranking — even when one drives the decision. Their divergence is diagnostic: Monte Carlo
outside the worst-case bounds means a bug; Monte Carlo sitting exactly on RSS means the
correlation groups were dropped.

**The contribution ranking is the deliverable**, not the failure probability. It is a squared
measure, so it concentrates hard — two or three terms usually carry 70–90% of a stack.

The only code today is the build tooling in `tools/` (notebook conversion, index generation)
and `build.sh`. Per the global instructions, run a Snyk scan on new first-party code in a
supported language; no Snyk MCP tool was available in the session that wrote these, so they
were reviewed by hand instead — no `eval`, no shell interpolation, no network access.

## Maxima gotchas

Encountered while writing these; all of them cost time:

- A bare `%` inside a Maxima string is parsed as an output-line reference. Write "percent".
- Binding a name to a matrix makes `name[i]` return a *row*, not a scalar. `kill()` it before
  reusing the name for indexed symbols.
- A markdown-cell `$$…$$` block must be **single-line**; multi-line display maths, `\text{}`,
  `\boxed`, `\operatorname` and bare `|` pipes all render badly. Use `\lvert … \rvert`.
- `aximar-mcp run --allow-dangerous <nb>` executes a notebook in place. Guide notebooks are
  mostly markdown, so this is fast; only 02, 08 and the maths notebook do real work.

## Conventions

Prose is British English. Notebook filenames are `NN-kebab-case.macnb`; the index generator
takes each title from the H1 of the first markdown cell and orders by filename, which is why
the guide is numbered. Parameter and FreeCAD alias IDs are `snake_case`, prefixed by part
(`encl_cavity_height`), and must match exactly between the YAML and the CAD spreadsheet —
FreeCAD also rejects aliases starting with a digit.

Standards, figures and claims are cited to a source. `09-bibliography` is the annotated bibliography
and marks each entry `[free]` / `[springer]` / `[open]` / `[buy]`; the user has Springer
institutional access. Fritz Scholz, *Tolerance Stack Analysis Methods* (Boeing ISSTECH-95-030,
1995) is the free primary source for the mathematics and supplies the notation used
throughout.

---

Other agent configs were found at `~/.codex/config.toml` and `~/.gemini/settings.json`. To
bring over MCP servers, slash commands, subagents, skills or instructions from them, reply
`/import` to scan and list what's importable, then `/import --yes=<digest>` to apply. If
`/import` isn't available on this surface, run `claude import` from a terminal.
