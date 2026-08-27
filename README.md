# Tolerance Management for a Desktop 3D-Printing + PCB Workflow

An open, self-hosted alternative to proprietary tolerance-analysis software (RD8, CETOL 6σ,
3DCS, VisVSA), targeted at FreeCAD + KiCad + FDM printing.

<p align="center">
  <a href="https://cmsd2.github.io/tolerances/">
    <img alt="Read the documentation at cmsd2.github.io/tolerances"
         src="https://img.shields.io/badge/%F0%9F%93%96%20Read%20the%20documentation-cmsd2.github.io%2Ftolerances-0969da?style=for-the-badge">
  </a>
  <br>
  <a href="https://github.com/cmsd2/tolerances/actions/workflows/pages.yml">
    <img alt="Pages build status"
         src="https://github.com/cmsd2/tolerances/actions/workflows/pages.yml/badge.svg">
  </a>
</p>

The premise: **the mathematics of tolerance analysis is easy and free. The hard parts are
knowing your actual process capability, and keeping one honest source of truth for every
dimension.** Commercial tools sell you automation and a managed record. They cannot sell you
capability data for your printer, and that is the input that dominates every result.

---

## The documents

Everything is a Maxima notebook (`.macnb`), executed and rendered to HTML by GitHub Actions on
every push. Worked examples are *computed at build time*, not transcribed — so the prose and
the arithmetic cannot drift apart.

### Guide — `notebooks/guide/`

| # | Notebook | What it is |
|---|---|---|
| 00 | Orientation | The problem, what you are actually replacing, what to ignore |
| 01 | Concepts | Variation, chains, analysis vs. synthesis, capability — with the literature |
| 02 | Methods | The mathematics: worst-case, RSS, inflation factors, mean shifts, Monte Carlo. **Live worked example** |
| 03 | Standards | ISO GPS, ASME Y14.5, ISO/ASTM AM, IPC. What to read, what to skip, what is free |
| 04 | Process capability | Characterising *your* printer and *your* fab house. The highest-value document here |
| 05 | Parameter model | The single-source-of-truth schema and why it is shaped that way |
| 06 | Workflow | The step-by-step procedure to follow |
| 07 | FreeCAD integration | Driving the model from the parameter file; worst-case configurations |
| 08 | KiCad and PCB | The board as a purchased part; **live USB-C aperture chain** |
| 09 | Bibliography | Annotated, marked by cost and access |
| 10 | Glossary | Terms, with the ISO/ASME distinctions that trip people up |

### Mathematics — `notebooks/mathematics/`

**Tolerance Stack Mathematics** — symbolic derivations behind everything in 02. Reproduces
Scholz's distribution inflation-factor table from first principles (all eight values exact),
derives the trapezoidal family in closed form, and verifies that Greenwood–Chase really does
interpolate between worst case and RSS. §0 is a self-contained primer.

Plus [`templates/parameters.example.yaml`](templates/parameters.example.yaml) — a complete,
commented worked example of the parameter file.

---

## Reading paths

**Understand the subject.** 00 → 01 → 02 → 03, then 09 to go deeper.

**Start doing something this week.** 00 → 06 → 04. Print coupons on day one; they take days of
wall-clock time and everything else depends on them.

**Look something up.** 02 for formulas, 03 for which standard says what, 05 for the schema,
10 for terms.

---

## Building the site locally

```sh
uv venv
uv pip install "maxima-nbconvert[plotly] @ git+https://github.com/cmsd2/maxima-nbconvert"
AXIMAR_MCP=path/to/aximar-mcp ./build.sh      # execute + export + index
make serve                                    # build, then serve on :8000
```

Requires [`aximar-mcp`](https://github.com/cmsd2/aximar) (executes the notebooks), a Maxima
install with gnuplot, and `uv`. `make docs/pages/02-methods.html` rebuilds one notebook.

`docs/pages/` is a build product and is not committed — CI renders it from the notebooks, so
the published site always matches the repository.

---

## Status

Documentation only. No analysis code has been written yet; notebook 06 gives the build order.
