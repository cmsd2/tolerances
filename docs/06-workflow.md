# 06 — The Workflow

The procedure to follow, phase by phase. Each phase states its inputs, actions, outputs, and
**where I can help** — marked 🤖 — so you can hand off the parts that are mechanical and keep
the parts that need your judgement.

Two things run on very different clocks, so start them together:

- **Phase 2 (characterisation)** costs days of wall-clock printing time and almost no
  attention.
- **Phases 1, 3–5** cost attention and almost no wall-clock time.

Start the printer on day one. Do the thinking while it runs.

---

## Phase 0 — Set up the repository

**Output:** the layout in [05 §5](05-parameter-model.md), under version control.

- `git init`, and commit these documents.
- Create `params/`, `profiles/`, `cad/`, `pcb/`, `tools/`, `reports/`.
- Export your current slicer profile into `profiles/` and commit it. Do this *before* you
  change anything, so you have a baseline.

🤖 *I can scaffold the directory structure, the `.gitignore` (FreeCAD and KiCad both generate
a lot of noise), and a `Makefile`/`justfile` for the common commands.*

---

## Phase 1 — Write down the requirements before you model anything

This is the phase people skip, and skipping it is why tolerance analysis usually happens too
late to change anything.

**Input:** your idea of the assembly.
**Output:** a list of functional requirements, each expressed as a condition on a gap.

For each way the assembly could fail to work, write one line:

> "The lid must close without bowing the PCB" → `cavity − boss − pcb − rib ≥ 0`
>
> "The USB-C plug must enter the aperture" → `|aperture_centre − connector_centre| ≤ 0.35`
>
> "The board must not rattle" → `cavity − boss − pcb − rib ≤ 1.0`

Rules that make this phase pay off:

- **Express every requirement as an inequality on a computable quantity.** "The lid should fit
  nicely" is not a requirement. If you cannot write it as an inequality, you do not yet know
  what you want.
- **Both bounds, where both exist.** Most clearances have a maximum as well as a minimum, and
  the maximum is the one people forget until the thing rattles.
- **Mark the key characteristics** ([01 §8](01-concepts.md)). Expect five to ten. If you have
  thirty, you have not thought hard enough about which ones matter.
- **Note what is adjustable.** A requirement you can satisfy with a shim, a screw adjustment,
  or a bit of foam is a different kind of problem from one fixed at print time. Record it.

🤖 *Give me a description or sketch of the assembly and I'll draft the requirement list and
the candidate chains for you to correct. Getting the loop closure and signs right is exactly
the sort of thing worth a second pair of eyes.*

---

## Phase 2 — Characterise the process (start this on day one)

**Input:** a printer and some filament.
**Output:** a capability table, per [04 §8](04-process-capability.md).

Follow [04 — Process capability](04-process-capability.md) in full. In brief:

1. Model the six coupons (A–F).
2. Print them across three sessions, recording configuration exactly.
3. Measure, with a repeatability study first (§6) so you know what your measurements are
   worth.
4. Regress error on nominal to separate offset from scale (§7).
5. Decide and apply compensation, in one place (§9).
6. Re-measure to confirm.

If you do nothing else in this phase, do **coupon C (the fit ladder)**. It answers the single
most common practical question — what clearance do I need — with no measurement and no
statistics.

🤖 *I can generate the coupon geometry as FreeCAD macros or OpenSCAD/STL, write the
measurement log template, and do the regression and distribution fitting once you have
numbers. Send me a CSV of measurements and I'll return the capability table.*

---

## Phase 3 — Build the parameter file

**Input:** Phase 1 requirements, Phase 2 capability (or placeholders).
**Output:** `params/parameters.yaml`.

- Enter every dimension that appears in any chain, plus every dimension you expect to tune.
- Fill in `source:` honestly on every one. Use `assumed` freely at this stage — the point is
  that it is *visible*.
- Define correlation groups for features that share a cause.
- Define the stacks from Phase 1.

Do not wait for Phase 2 to finish. Populate with `assumed` values now, and let the
characterisation results replace them. The diff when that happens is instructive.

🤖 *I can write the initial parameter file from your requirement list, and write the loader
and validator (see the security note in [05 §4](05-parameter-model.md) — expression
evaluation must not use `eval()`).*

---

## Phase 4 — Wire CAD and PCB to the parameter file

**Input:** `parameters.yaml`.
**Output:** a FreeCAD model and a KiCad board that cannot silently disagree with it.

See [07 — FreeCAD](07-freecad.md) and [08 — KiCad and PCB](08-kicad-pcb.md).

The test of success: change one number in the YAML, run one command, and both the model and
the board update. Until that works, you do not have a single source of truth — you have a
document that describes one.

🤖 *This is the most script-heavy phase and the one I'm most useful for: the YAML→FreeCAD
spreadsheet sync, the KiCad geometry extraction, and the consistency checker that fails if
CAD and YAML have drifted.*

---

## Phase 5 — Analyse

**Input:** parameters and stacks.
**Output:** a report in `reports/`, committed.

For each stack, compute and report **all** of:

- worst case — the guaranteed bound
- RSS — the optimistic bound
- Monte Carlo with your actual distributions, offsets and correlations — the estimate
- the **contribution ranking** ([02 §7](02-methods.md))
- which inputs were `assumed` rather than measured

Report all four methods every time, even when only one drives the decision. Their divergence
is diagnostic: if Monte Carlo lands outside the worst-case bounds you have a bug; if it sits
almost exactly on RSS you have probably forgotten your correlations.

**Sensitivity to your guesses.** Re-run with `share: 0`, `0.5`, `1.0` on the correlation
groups, and with `assumed` tolerances at half and double. If the decision does not change, you
can stop worrying about those inputs — which is a much stronger result than a single precise
number.

🤖 *I can write the analysis tool — worst case, RSS, Monte Carlo with correlation groups,
contribution ranking, and a markdown/HTML report generator. The maths is settled in
[02](02-methods.md) and verified symbolically in the
[Maxima notebook](../notebooks/tolerance-mathematics.macnb); the code is straightforward.*

---

## Phase 6 — Decide

**Input:** the report. **Output:** a decision, recorded.

If every stack passes with margin, build it.

If one does not, you have five options, in the order you should consider them:

1. **Change the design so the stack does not exist.** The best tolerance analysis is one you
   deleted. See below.
2. **Change the nominal.** Very often the gap is simply too small and there is no reason for
   it. Free.
3. **Reduce the top contributor's variation.** Print that feature in a different orientation,
   in a different material, or make it the one machined/reamed feature. Only ever attack the
   top one or two — the ranking is squared, so the rest do not matter.
4. **Accept the failure rate.** For a one-off with a 2% chance of needing a file, this is
   correct and you should not feel bad about it. Record the decision.
5. **Add adjustment.** A shim, a slot instead of a hole, a set screw. Converts a tolerance
   problem into an assembly step.

Record which you chose and why, in the commit message. Six months on, the reasoning is the
part you will have lost.

### Design moves that beat tolerance analysis

Worth their own section, because for 3D printing these are usually the *right* answer, and
they are what a tolerance-analysis tool will never suggest:

- **Compliance.** A snap arm, a spring finger, a foam pad, an O-ring. Absorbs the entire stack
  and turns a ±0.5 mm problem into a non-problem. The most powerful move available.
- **Lead-ins and chamfers.** A 45° chamfer on a hole entry converts a positional error into a
  guided insertion. Costs nothing, works every time.
- **Kinematic (exact) constraint.** Constrain each degree of freedom exactly once. Three
  points define a plane; four points define a rocking part. Over-constraint is what turns
  small errors into large stresses.
- **Self-alignment.** Cones, vees, tapered pins, magnets. Let the parts find their own
  position rather than specifying it.
- **Slots instead of holes.** A slotted mounting hole removes one direction from the chain
  entirely.
- **Deliberate slop plus a datum.** Locate on *one* feature precisely and let everything else
  float. Trying to locate on two features precisely is how you get an over-constrained
  assembly that never fits.
- **Print it as one part.** Every joint you remove removes a whole chain. Printing is the one
  process where part-count reduction is nearly free.
- **Move the precision to a bought part.** A printed bearing pocket holding a steel bearing
  needs one accurate diameter; a printed bearing needs everything accurate.

🤖 *Given a failing stack and the contribution ranking, I can propose specific design changes
and re-run the analysis for each so you can compare them numerically.*

---

## Phase 7 — Verify on real parts

**Input:** the first physical assembly. **Output:** confirmation, or a corrected model.

- Measure the actual gaps on the first article and compare to the predicted distribution.
- One sample cannot validate a distribution, but it *can* falsify one: if the measured gap
  falls outside the predicted worst-case range, your chain is wrong. That is a real and
  common finding, and it is worth going back for.
- Feed the measurement back into the parameter file as evidence.

🤖 *I can write the first-article check: predicted vs. measured, with the percentile the
observation landed at.*

---

## Phase 8 — Maintain

The system pays for itself here.

- Re-run the analysis on every design change. Because the reports are committed, the diff
  shows you the effect immediately.
- Re-characterise on the triggers in [04 §10](04-process-capability.md).
- Move `assumed` values to `measured` opportunistically — every time you measure anything, put
  it in the file.

🤖 *I can set up a pre-commit hook or CI check that re-runs the analysis and fails if any key
characteristic's failure rate has regressed past its threshold.*

---

## Suggested order of work

| Week | Do |
|---|---|
| 1 | Phase 0. Phase 1 requirements. Start Phase 2 printing — coupons C and F first |
| 1–2 | Phase 3 with `assumed` values. Measure coupons |
| 2 | Phase 2 analysis and compensation. Re-print, re-measure |
| 2–3 | Phase 4 wiring. Phase 5 first real analysis |
| 3 | Phase 6 decisions, iterate |
| 4 | Phase 7 first article |

The first project takes about a month of evenings. Subsequent projects reuse the capability
data and the tooling, and take a day.

---

## What to build, in order

If you want the tooling built, this is the dependency order:

1. **Parameter file loader + validator.** Everything depends on it. Safe expression
   evaluation, reference checking, clear errors.
2. **Analysis engine.** Worst case, RSS, Monte Carlo with correlation groups, contribution
   ranking.
3. **Report generator.** Markdown to `reports/`, committed.
4. **Coupon generator.** Parametric coupons A–F.
5. **Capability fitter.** Measurement CSV → regression → capability table entry.
6. **FreeCAD sync.** YAML → spreadsheet aliases.
7. **KiCad extractor.** Board geometry → parameters, and the consistency check.
8. **CI check.** Regression gate on key characteristics.

Items 1–3 are the minimum viable system and are perhaps 400 lines of Python. Item 5 is where
the real value is unlocked. Items 6–8 are conveniences that matter once the project is alive.

---

Previous: [05 — Parameter model](05-parameter-model.md) · Next: [07 — FreeCAD](07-freecad.md)
