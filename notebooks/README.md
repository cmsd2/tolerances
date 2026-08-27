# Notebooks

Every document in this project is a Maxima notebook. `build.sh` executes them all and exports
to `docs/pages/`; `.github/workflows/pages.yml` does the same in CI and publishes to GitHub
Pages.

- `guide/` — the eleven documentation notebooks, numbered in reading order.
- `mathematics/` — symbolic derivations.

## `mathematics/tolerance-mathematics.macnb`

Maxima notebook deriving the formulas used in `guide/02-methods.macnb`.
Saved in Jupyter `.ipynb` format, so it opens in Jupyter, VS Code, or any `.ipynb` tool, and
runs against a Maxima kernel.

**§0 is a self-contained primer** — tolerance chains, what `T` means, the `T = 3σ` convention
and the four ways it fails. You do not need to have read Scholz first.

### What it establishes

| § | Content |
|---|---|
| 0 | Primer: the setup, notation, and why each later section exists |
| 1 | `Var(G) = aᵀ Σ a`, expanded; setting ρ = 0 recovers RSS |
| 2 | Worst case ÷ RSS = √n for n equal terms |
| 3 | **Scholz's Figure 6 derived from scratch.** `c = 3σ/T`; all eight densities integrated, every value matching to three decimals |
| 4 | Trapezoidal family: `σ² = T²(1+k²)/6`, `c = √(3(1+k²)/2)`, with uniform and triangular as its endpoints |
| 5 | Greenwood–Chase verified to collapse to RSS at η=0 and worst case at η=1 |
| 6 | The worked example from `guide/02-methods` §10, recomputed independently |
| 7 | Correlated variance for both the sign-alternating and same-sign cases |

### Why it exists

Three reasons.

**The inflation factors should not be magic numbers.** Scholz's table circulates as a list of
decimals — 1.732, 1.225, 1.369 — with no visible origin, and gets copied between documents
until nobody knows what they mean. They are all just `3σ/T` for a given density. §3 integrates
each one and checks it. Once you have seen that, you can derive a factor for a distribution
that is not in the table, which is what you will actually need for a real printer.

**The prose and the arithmetic must not drift.** §6 recomputes the worked example from
`guide/02-methods` §10 independently. Both are now computed rather than typed, so two agreeing
results are a genuine cross-check.

**It proved its worth immediately.** Converting the guide's worked examples from typed tables
to live cells surfaced an arithmetic error in the original hand-written prose — a retolerancing
figure quoted as 0.368 mm / 0.00056 that is actually 0.358 mm / 0.0004.

### Running it

Needs a Maxima kernel. Section 3 uses `minfactorial(makefact(makegamma(...)))` to collapse a
gamma-function ratio via the recurrence Γ(z+1) = zΓ(z); other CAS backends will need their own
equivalent.

Two Maxima gotchas the notebook works around, in case you extend it:

- A bare `%` inside a string is parsed as an output-line reference. Write "percent".
- Binding a name to a matrix makes `name[i]` return a *row*, not a scalar. `kill()` it first
  if you then want indexed symbols.
