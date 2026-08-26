# 04 — Process Capability: Characterising Your Own Equipment

**This is the most valuable document in the set.** Everything in
[02 — Methods](02-methods.md) is a function whose inputs come from here. A stack-up computed
over guessed tolerances is a guess rendered to three decimal places.

It is also the part no commercial tool can do for you. RD8 will happily accept ±0.2 mm and
produce a confident answer. Only you can find out what your printer actually does.

Budget: two or three evenings of printing and an afternoon of measuring, for a result that
stays valid for months.

---

## 1. The central insight

Classical tolerancing models a dimension as **symmetric random variation about nominal**.

FDM is not like that. FDM error is dominated by **systematic, directional, repeatable bias**,
with comparatively small random spread on top. Concretely, on a typical desktop machine:

- external dimensions come out **oversize**
- internal dimensions (holes, slots, pockets) come out **undersize**
- both effects are consistent run to run
- the random part-to-part spread is often *smaller* than the bias

So a printed hole nominally Ø8.00 might measure 7.84, 7.86, 7.85, 7.83, 7.86 — bias −0.15 mm,
spread σ ≈ 0.013 mm. Describing that as "±0.2 mm" is wrong twice over: it overstates the
randomness by an order of magnitude and completely hides the offset that is actually going to
break your assembly.

**Therefore: characterise every feature class as a pair (δ, σ) — bias and spread — never as a
single ±T.** This single change in representation is worth more than any analysis method.

And note the happy consequence: **bias is correctable.** Once measured, you can design it out
(compensate the model or the slicer) and be left with only the small σ. That is how you get
usable precision out of a cheap machine.

## 2. Where the variation comes from

Understanding the mechanisms tells you what to hold constant and what to measure.

### Systematic (bias) — correctable

| Mechanism | Effect | Character |
|---|---|---|
| Extrusion width / flow calibration | External features grow, internal features shrink, by ~½ the error on each wall | **Constant offset**, independent of feature size |
| Thermal shrinkage on cooling | Everything shrinks. PLA ~0.2–0.3%, PETG ~0.2–0.4%, ABS/ASA ~0.7–0.8% | **Proportional to size** |
| Elephant's foot | First few layers squashed outward; base is oversize | Localised, first ~0.5 mm of Z |
| Polygonal approximation of circles | Mesh facets inscribe the true circle, so holes are undersize | Depends on mesh resolution |
| Z quantisation | A height is built from an integer number of layers | **Deterministic**, see below |
| Corner bulge from acceleration | Outside corners overshoot | Localised |

### Random (spread) — irreducible, must be budgeted

| Mechanism | Typical magnitude |
|---|---|
| Filament diameter variation (batch and along-spool) | flow ±1–2% |
| Bed levelling / first-layer height variation | 0.02–0.05 mm on Z datum |
| Ambient temperature and draughts | small on PLA, significant on ABS |
| Spool-to-spool and colour-to-colour differences | can be larger than everything else combined |
| Position on the bed | measurable on poorly trammed machines |
| Belt tension drift, mechanical wear | slow drift, shows as between-session variation |

**Filament colour is not cosmetic.** Pigments and additives change melt rheology and
shrinkage. A change of colour within one brand can shift dimensions measurably. Treat
(brand, material, colour) as the unit of characterisation, not just material.

### The Z quantisation effect

This one is specific to layer-based processes and is routinely missed.

A part's Z height is built from an integer number of layers. At 0.2 mm layer height, a
nominal 5.03 mm feature becomes 25 layers = 5.00 mm, or 5.20 mm — never 5.03. The error is
not random; it is **fully determined** by the nominal, the layer height, and the first-layer
height.

Two consequences:

1. **Z dimensions have near-zero random spread but a potentially large deterministic error.**
   Modelling Z as normal with σ = T/3 is the wrong model entirely.
2. **Design rule: make critical Z dimensions integer multiples of your layer height** (after
   accounting for the first layer, which is usually a different thickness). Do this and the
   error disappears. It costs nothing and it is the single cheapest precision win available
   to you.

## 3. Coupon design

Six coupons. Print them as one plate if your bed allows, or as a small set.

### A — External size ladder
Stepped rectangular prism with nominal features at **5, 10, 20, 40, 80 mm** measured in each
of X, Y and Z. Purpose: separate constant offset from proportional shrinkage (§7), and
compare axes.

### B — Bore ladder
Flat plate with through-holes at **Ø3, 5, 8, 12, 20 mm**, axes vertical (the common case).
Purpose: internal-feature bias and its size dependence.

### C — Fit ladder
A reference pin (Ø10 nominal) plus a row of holes at Ø10.0 through Ø10.6 in 0.05 mm steps.
Purpose: a direct, no-measurement-needed answer to "what clearance do I need for a sliding
fit / press fit". The smallest hole that accepts the pin with the intended feel *is* your
answer. Print this even if you print nothing else.

### D — Wall thickness
Upright walls at **0.4, 0.8, 1.2, 1.6, 2.0 mm**. Purpose: minimum feature size and
extrusion-width quantisation.

### E — First-layer / elephant's-foot
A 20 mm prism with the same nominal width measured at **0.4, 1.0, 2.0, 5.0 and 10.0 mm**
above the bed. Purpose: how far up the elephant's foot extends and how large it is. Determines
whether you need a base chamfer and where it is safe to measure everything else.

### F — Repeatability array
**Ten identical 20 mm cubes**, distributed across the whole bed. Purpose: the actual σ, plus
any spatial dependence. This is the coupon that gives you the number you will put in every
stack-up.

## 4. Print protocol

The discipline here is what separates data from anecdote.

- **Record the configuration completely and immutably.** Export the slicer profile to a file
  and commit it. Note: printer, firmware version, slicer and version, nozzle diameter and
  age, layer height, filament brand/material/colour/spool ID, bed and nozzle temperatures,
  print speed, cooling, ambient temperature. If you cannot reproduce the print, the data has
  no shelf life.
- **Print across sessions, not all at once.** Between-session variation (re-levelling,
  ambient change, spool position) is real and is what you will actually experience. Three
  sessions of ~4 coupons beats one session of 12.
- **Randomise bed position** between sessions.
- **Number every part as it comes off the bed.** Emboss an index on coupon F.
- **Do not adjust anything mid-campaign.** If you re-level or change a setting, that starts a
  new characterisation.
- **Deburr consistently, or not at all** — and record which.

## 5. What to measure, and where

- Measure **above the elephant's foot** — use coupon E to find out where that is, typically
  1–2 mm.
- Measure **away from the layer seam**, and record the orientation you used. The seam is a
  local bump; hitting it or not is a 0.05 mm coin flip.
- Take **three measurements per feature** at different heights/positions and record all
  three, not the average. The spread within a part tells you about form error; the spread
  between parts tells you about process σ. Averaging destroys that distinction.
- For holes, **pin gauges beat calipers** by a wide margin. A cheap pin gauge set is the best
  measurement purchase you can make for this work. Failing that, coupon C is a functional
  gauge.
- For external dimensions, **a micrometer with a friction thimble beats a caliper**, because
  it applies consistent force.

## 6. Measurement and its uncertainty

**Plastic is compliant.** A digital caliper reads to 0.01 mm and, squeezed hard on a printed
PLA part, will happily read 0.08 mm small. Your measurement uncertainty is not the
instrument's resolution — it is dominated by technique.

**Do a repeatability study before trusting any data.** Take one part. Measure the same feature
twenty times, putting the instrument down between measurements. The standard deviation of
those twenty readings is your measurement σ_meas. Expect:

| Instrument, on printed plastic | Realistic σ_meas |
|---|---|
| Digital caliper, casual technique | 0.03–0.05 mm |
| Digital caliper, careful consistent technique | 0.015–0.025 mm |
| Micrometer with friction thimble | 0.005–0.010 mm |
| Pin gauges (holes) | ~half the gauge step |

**The decision rule.** Measured variance is the sum of real and measurement variance:

    σ²_observed = σ²_process + σ²_meas    ⟹    σ_process = √(σ²_observed − σ²_meas)

If σ_meas is more than about a third of σ_observed, you are largely measuring yourself. Fix
the technique or buy a better instrument before collecting more data.

This is the practical form of **ISO 14253-1**: uncertainty narrows what you are entitled to
conclude. Do not report a 0.03 mm bias from an instrument with 0.05 mm uncertainty. Either
increase n until the standard error of the *mean* (σ_meas/√n) is small enough, or stop
claiming the effect.

## 7. Analysis

### Fit the size-dependent model

Do not compute one average error. The two dominant mechanisms have different size dependence,
so regress error on nominal:

    error = measured − nominal = a + b × nominal + ε

- **a** (intercept) is the constant offset from extrusion width and flow. Typically a few
  hundredths of a mm, positive for external features and negative for internal.
- **b** (slope) is the proportional shrinkage. Typically −0.002 to −0.003 for PLA.
- **ε** is what is left over: your genuine random spread, σ.

This is the single most informative analysis in the whole campaign, and it is a two-line
linear regression. It tells you *why* your parts are wrong, which tells you *how* to fix
them: `a` is corrected by an XY compensation setting, `b` by a scale factor.

Fit it separately for **external-XY, internal-XY, external-Z**. Those three classes behave
differently enough that pooling them destroys the signal.

### Check the distribution

Plot a histogram and a normal QQ plot of the residuals from coupon F. Run Shapiro–Wilk if you
like, but at n = 20 it has weak power — the QQ plot is more informative. If the data is
clearly skewed or bimodal, say so in the parameter file and use the empirical distribution in
Monte Carlo rather than fitting a normal.

### Use an upper confidence bound on σ, not the point estimate

Small samples estimate σ badly, and always in the dangerous direction — you are more likely
to get a comfortingly small estimate than an alarming one. The 95% confidence interval for σ:

| n | 95% CI for σ, as a multiple of the estimate σ̂ |
|---|---|
| 5 | [0.60 σ̂, 2.87 σ̂] |
| 10 | [0.69 σ̂, 1.83 σ̂] |
| 20 | [0.76 σ̂, 1.46 σ̂] |
| 30 | [0.80 σ̂, 1.34 σ̂] |

At n = 5, your σ could be nearly three times what you measured. **Use the upper bound in
stack-ups.** Scholz recommends exactly this: upper confidence bounds on 3σ from limited data
are conservative, and conservative is what you want when the data is thin.

**Minimum useful n is 20. Thirty is comfortable. Five tells you almost nothing about spread**
(though it does give a usable estimate of *bias*, since the standard error of the mean is
only σ/√5 — which is why bias is cheap to measure and spread is expensive).

## 8. The capability table

The output of all this is a table, committed to the repository, keyed by the conditions that
matter:

| Key field | Example |
|---|---|
| printer | `prusa_mk4` |
| material | `pla` |
| brand + colour | `prusament_galaxy_black` |
| nozzle | `0.4` |
| layer height | `0.2` |
| profile hash | `sha256:ab3f…` |
| feature class | `external_xy` / `internal_xy` / `external_z` / `internal_z` |

with, for each row: `a` (offset), `b` (scale), `sigma`, `sigma_upper_95`, `n`,
`distribution`, `date`, `notes`.

Every tolerance in [05 — the parameter model](05-parameter-model.md) then either references a
row of this table or is explicitly marked as a guess. That distinction — measured versus
assumed — is what makes the whole system trustworthy, and it is why the schema carries a
`source` field on every parameter.

## 9. Compensation strategy

Once you know `a` and `b`, you can correct them. The options:

| Where | Corrects | Notes |
|---|---|---|
| Slicer XY size compensation | constant offset `a`, external | Applies to all XY contours |
| Slicer hole/horizontal expansion | constant offset `a`, internal | Separate setting in PrusaSlicer / OrcaSlicer — this is what lets you fix holes and externals independently |
| Slicer scale factor / filament shrinkage compensation | proportional error `b` | Material property; set once per material |
| Model-level parameter offsets | anything | Full control, but pollutes the CAD with process artefacts |

**Recommendation:** correct `b` (shrinkage) as a material setting in the slicer, and `a` via
the slicer's XY-compensation and hole-expansion settings. Keep the CAD model at true nominal.
The model then represents the *design*, and the slicer profile represents the *process* — a
clean separation that survives changing printers.

**The one rule that matters: compensate in exactly one place, and record where.** The classic
failure is applying a hole-expansion setting in the slicer, forgetting, then also enlarging
holes in the model six months later — and getting double the correction. Put the compensation
location in the parameter file as a comment.

**Always re-measure after compensating**, on a fresh coupon set. Compensation changes the
process; the old σ may not survive it.

## 10. When to re-characterise

Re-run at least coupon C (fit ladder) and coupon F (repeatability array) when:

- new filament **brand, material, or colour** — colour genuinely matters
- new spool of the same product, if the fit is critical
- nozzle replaced, or after significant wear (brass nozzles wear measurably with filled
  filaments)
- firmware or slicer major version change
- any profile change to flow, temperature, speed or layer height
- seasonal ambient change, if the printer is unenclosed
- belt tension, extruder or hotend maintenance
- anything unexpected in a print

Date-stamp every characterisation. A capability figure with no date is not evidence.

## 11. Characterising the PCB side

Much less work, because a fab house is a controlled industrial process and publishes its
capability. The procedure:

1. **Take the supplier's published tolerances as your starting values.** Record the URL and
   the date you read it in the parameter file — these pages change.
2. **Model them as uniform distributions**, not normal. A supplier's ± is a limit they
   undertake not to exceed, not a 3σ figure. See [02 §8](02-methods.md).
3. **Verify on the first article.** When the first boards arrive, measure: board thickness
   (micrometer, five places), outline dimensions (calipers), mounting-hole positions relative
   to a board edge, and the position of any connector whose aperture you have to hit. Ten
   minutes of work that catches the mistakes that matter.
4. **Watch for the things suppliers do not publish**: hole-to-outline registration is often
   worse than either individual tolerance, and it is exactly what determines whether your
   mounting holes line up with your printed bosses. If the datum for routing differs from the
   datum for drilling, the errors add.
5. **Component placement is a separate contributor.** Board fabrication tolerance does not
   include where the assembler put the connector. Get that from your assembly house; if you
   are hand-soldering, it is your own hand, and it is worse than you think — measure it.

See [08 — KiCad and PCB](08-kicad-pcb.md) for how these feed into the enclosure chain.

---

## Reading

- **ISO/ASTM 52902:2023** — *Additive manufacturing — Test artefacts — Geometric capability
  assessment of AM systems*. The formal version of this document.
- **ISO 22514-4** — process capability estimates, including the percentile-based indices to
  use when your data is not normal.
- **ISO 14253-1:2017** — decision rules under measurement uncertainty.
- Vidakis et al. / Kechagias et al., *Accuracy of FDM PLA Polymer 3D Printing Technology
  Based on Tolerance Fields*, **Processes** 11(10):2810 (2023). Open access. Places FDM PLA
  in the ISO 286 IT-grade system and demonstrates the size dependence discussed in §7.
- *The Impact of Elevated Printing Speeds and Filament Color on the Dimensional Precision and
  Tensile Properties of FDM-Printed PLA Specimens* (2025), PMC12349424. Evidence for the
  colour effect in §2.

---

Previous: [03 — Standards](03-standards.md) · Next: [05 — Parameter model](05-parameter-model.md)
