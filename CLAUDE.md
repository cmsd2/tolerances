# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

An open alternative to proprietary tolerance-analysis software (RD8, CETOL 6σ, 3DCS) for a
one-person FreeCAD + KiCad + FDM-printing workflow.

**It is currently documentation only — there is no code, no build, no tests.** The eleven
documents in `docs/` are the design; `docs/06-workflow.md` §"What to build, in order" is the
implementation plan. When tooling gets written, add its commands to this file.

Working commands today: `git`, and a Maxima kernel for the notebook.

## The domain decisions that pervade everything

These are the non-obvious choices the whole design rests on. Violating one silently produces
plausible, wrong answers.

**Dimensions are `(offset, spread)`, never `±T`.** FDM error is dominated by *systematic,
directional* bias — external features run oversize, holes run undersize, repeatably — with
comparatively small random spread. A symmetric ± both overstates the randomness and hides the
offset. See `docs/04` §1.

**Correlation is first-class, and it cuts both ways.** Features on one printed part share a
first-layer offset, flow calibration and thermal history, so RSS's independence assumption
fails routinely. The sign structure of the chain decides the direction: same-sign terms
accumulate common-mode error, opposite-sign terms cancel it. Worked both ways in `docs/02`
§10 and notebook §7 — a ~22,000× swing in failure rate. Never assume RSS is the conservative
choice.

**A supplier's `±` is a spec limit, not a 3σ.** Model datasheet and fab-house tolerances as
**uniform**, not normal. Reaching for the normal distribution by default is the single most
common way to understate tails here. See `docs/02` §8.

**`source:` is the trust boundary.** Every parameter is `measured` / `supplier_spec` /
`standard` / `assumed`. All four are legitimate; not knowing which is not. Any analysis output
must list its `assumed` inputs separately.

**Compensate in exactly one place.** Process bias is corrected in the slicer profile *or* in
the CAD model, never both, and the location is recorded in the parameter file. `docs/04` §9.

**Sync is one-directional: YAML → FreeCAD/KiCad.** Values edited in a FreeCAD spreadsheet are
expected to be overwritten. Board geometry is normally extracted *from* KiCad into the YAML
(board-led), with a consistency check running the other way. `docs/07` §3, `docs/08` §3.

## Cross-file invariants

**Numbers appear in three places and must agree.** The worked example lives in `docs/02` §10
(prose), `templates/parameters.example.yaml` (as a stack definition), and
`notebooks/tolerance-mathematics.macnb` §6–7 (recomputed). The second worked example is
`docs/08` §5. If you change a tolerance or a nominal in any of them, re-run the notebook and
update the others.

**Docs are a numbered, cross-linked sequence.** Each file ends with prev/next links and is
listed in the `README.md` table. Adding or renumbering a document means updating both.

**Reports are committed on purpose; raw measurement data is never edited.** `reports/` is
version-controlled so a diff shows "this change moved the lid clearance failure rate from
0.1% to 3%". Raw CSVs under `params/capability/campaigns/` are evidence — corrections go in a
separate file with a reason. `docs/05` §5.

## When writing the tooling

Build order and dependencies are in `docs/06`; the schema is `docs/05` with a complete worked
instance in `templates/parameters.example.yaml`. The minimum viable system is the loader, the
analysis engine and the report generator.

**Expression evaluation must not use `eval()`.** Stack definitions carry arithmetic as strings
from a config file. Use `ast.parse(mode="eval")` with a node whitelist, or `simpleeval` /
`asteval`. `docs/05` §4 specifies this.

**Report all four methods every time** — worst case, RSS, Monte Carlo, and the contribution
ranking — even when one drives the decision. Their divergence is diagnostic: Monte Carlo
outside the worst-case bounds means a bug; Monte Carlo sitting exactly on RSS means the
correlation groups were dropped.

**The contribution ranking is the deliverable**, not the failure probability. It is a squared
measure, so it concentrates hard — two or three terms usually carry 70–90% of a stack.

Snyk scanning applies to first-party code in supported languages (see the global instructions);
it has not been relevant so far because nothing here is code.

## The Maxima notebook

`notebooks/tolerance-mathematics.macnb` is saved as Jupyter `.ipynb` with a Maxima kernel, and
is edited through the `aximar` MCP tools. Run each cell after creating or updating it.

Two gotchas encountered while writing it:

- A bare `%` inside a Maxima string is parsed as an output-line reference. Write "percent".
- Binding a name to a matrix makes `name[i]` return a *row*, not a scalar. `kill()` it before
  reusing the name for indexed symbols.

Markdown cells must stay on a conservative LaTeX subset — the renderer chokes on multi-line
`$$…$$`, `\text{}`, `\boxed`, `\operatorname` and bare `|` pipes. Use single-line display
maths and `\lvert … \rvert`.

## Conventions

Prose is British English. Parameter and FreeCAD alias IDs are `snake_case`, prefixed by part
(`encl_cavity_height`), and must match exactly between the YAML and the CAD spreadsheet —
FreeCAD also rejects aliases starting with a digit.

Standards, figures and claims are cited to a source. `docs/09` is the annotated bibliography
and marks each entry `[free]` / `[springer]` / `[open]` / `[buy]`; the user has Springer
institutional access. Fritz Scholz, *Tolerance Stack Analysis Methods* (Boeing ISSTECH-95-030,
1995) is the free primary source for the mathematics and supplies the notation used
throughout.

---

Other agent configs were found at `~/.codex/config.toml` and `~/.gemini/settings.json`. To
bring over MCP servers, slash commands, subagents, skills or instructions from them, reply
`/import` to scan and list what's importable, then `/import --yes=<digest>` to apply. If
`/import` isn't available on this surface, run `claude import` from a terminal.
