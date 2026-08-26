# 02 — Methods: The Mathematics

Notation follows Scholz (1995), *Tolerance Stack Analysis Methods*, Boeing ISSTECH-95-030,
which is freely available and is the reference to reach for when this document is not enough.

> Every formula and every number below is derived symbolically and checked in
> [`notebooks/tolerance-mathematics.macnb`](../notebooks/tolerance-mathematics.macnb). If you
> would rather see where the constants come from than take them on trust, start there — its
> §0 is a self-contained primer that assumes no prior reading.

---

## 1. Notation

| Symbol | Meaning |
|---|---|
| Lᵢ | actual value of the i-th part dimension |
| λᵢ | nominal value of the i-th part dimension |
| μᵢ | actual process mean for the i-th dimension |
| Δᵢ | mean shift, Δᵢ = μᵢ − λᵢ |
| σᵢ | standard deviation of the i-th dimension |
| Tᵢ | tolerance (half-width) of the i-th dimension |
| G | assembly criterion (the gap of interest) |
| γ | nominal value of G |
| aᵢ | sensitivity coefficient of G to Lᵢ |
| T_assy | resulting assembly tolerance |
| cᵢ | distributional inflation factor |
| ηᵢ | mean shift as a fraction of tolerance, ηᵢ = \|Δᵢ\|/Tᵢ |

## 2. Linearising the chain

In general G = f(L₁, …, Lₙ). Expand about nominal:

    G ≈ a₀ + a₁L₁ + a₂L₂ + … + aₙLₙ

    aᵢ = ∂f/∂Lᵢ  evaluated at nominal

For a pure length stack — the common case — every aᵢ is +1 or −1, according to whether the
dimension adds to or subtracts from the gap. The general form matters when the chain involves
angles, projections, or trigonometric relationships; there, compute aᵢ by differentiation or
numerically:

    aᵢ ≈ [f(λ₁, …, λᵢ + h, …, λₙ) − f(λ₁, …, λᵢ − h, …, λₙ)] / 2h

Numerical differentiation is the pragmatic choice: it works on any function you can evaluate,
including one that calls into CAD.

**If the geometry is strongly non-linear over the tolerance range, do not linearise. Go
straight to Monte Carlo (§5).** Linearisation is an approximation that silently degrades; it
does not warn you.

## 3. Worst case (arithmetic)

    T_assy^arith = |a₁|T₁ + |a₂|T₂ + … + |aₙ|Tₙ

    G ∈ [γ − T_assy^arith, γ + T_assy^arith]     with absolute certainty

**Assumptions:** each Lᵢ lies within λᵢ ± Tᵢ. That is all. No distributional assumption
whatsoever, which is why it is the only method that gives a guarantee.

**Use when:** chains of two or three terms; safety-critical gaps; one-off builds where rework
is unacceptable; or when you have good reason to believe the dimensions are correlated (§6),
because correlated same-sign terms approach worst-case behaviour anyway.

## 4. Statistical (RSS)

    T_assy^stat = √(a₁²T₁² + a₂²T₂² + … + aₙ²Tₙ²)

and when all aᵢ = ±1 this reduces to the familiar √(T₁² + … + Tₙ²).

The geometric intuition Scholz offers: for three terms, worst-case is walking the three edges
of a box (T₁ + T₂ + T₃) while RSS is the diagonal (√(T₁²+T₂²+T₃²)). The diagonal is always
shorter, and increasingly so as terms are added.

**Assumptions — all four must hold, and they are load-bearing:**

1. **Independence** of the Lᵢ.
2. **Tᵢ = 3σᵢ** — the stated tolerance really is the ±3σ spread.
3. **Normality** of each Lᵢ.
4. **Centred** — μᵢ = λᵢ, the process sits on nominal.

**Interpretation:** γ ± T_assy^stat contains 99.73% of assemblies. Note the precision is
illusory in one direction: the 3 in 3σ is a round number and 0.9973 is what falls out of it,
not the other way round. You cannot have both round.

### Why RSS comes out optimistic in practice

Assembly variation observed in the field is routinely wider than RSS predicts. Each of the
four assumptions is a suspect, and each has a repair.

## 5. Repairs to RSS

### 5.1 Bender's inflation factor

    T_assy^stat(Bender) = 1.5 × √(a₁²T₁² + … + aₙ²Tₙ²)

The rationale matters, because the folklore version is wrong. Scholz's account: process
owners asked what tolerance they can hold often answer with a ±Tᵢ that actually corresponds
to their ±2σ range, not ±3σ — values outside ±2σ are rarely seen and get rationalised away.
Since ±2σ covers ~95%, correcting a 2σ-meaning-T to a 3σ-meaning-T requires a factor of 1.5.
Bender called this "benderising".

So the 1.5 is **a fix for a communication failure about what T means**, not a universal
physical correction. Scholz is blunt that *"the rationale for the inflation factor is not
altogether satisfactory, since it is based on ignorance and suppositions about meanings of
Tᵢ."* If you measured your own process and know what your Tᵢ means, you do not need it.

Note also that for n = 2, 1.5 × RSS is *more conservative than worst-case*. Which tells you
it is a blunt instrument.

*(Attribution: Scholz cites Bender (1962); the widely cited publication is Bender, A., "Statistical
Tolerancing as it Relates to Quality Control and the Designer", SAE paper 680490, 1968.)*

### 5.2 Distributional inflation factors

If a dimension is not normally distributed, inflate its contribution by a factor cᵢ:

    T_assy^stat(c) = √((c₁a₁T₁)² + (c₂a₂T₂)² + … + (cₙaₙTₙ)²)

Values from Scholz, Figure 6 — these are the numbers to use when you know the shape:

| Distribution over the tolerance interval | c |
|---|---|
| Normal (T = 3σ) | 1.000 |
| Beta, α = β = 3 | 1.134 |
| Triangular | 1.225 |
| Half cosine wave | 1.306 |
| Beta, α = β = 2 (parabolic) | 1.342 |
| Trapezoidal, k = 0.5 | 1.369 |
| Elliptical (semicircular) | 1.500 |
| DIN histogram, p = 0.7, g = 0.4 | 1.512 |
| **Uniform** | **1.732** |
| Beta, α = β = 0.6 (bimodal) | 2.023 |
| Student t (df = 4 or 10), scaled so T = 3σ | 1.000 |

The uniform value 1.732 = √3 is the one to remember: uniform is the most-spread symmetric
unimodal distribution over a fixed interval, and it inflates the contribution by 73%. A
tool-wear process, or a printer whose parameter drifts monotonically across a build, produces
something close to uniform.

Scholz's caveat is worth repeating: apply cᵢ where you have a **validated** reason to think
the distribution differs, leaving the rest at 1. Using them as blanket protection factors is
fine too — but then admit that is what you are doing rather than pretending to model a shape.

### 5.3 Mean shifts

If processes are not centred, the general model (Greenwood & Chase, 1987) stacks the mean
shifts arithmetically and the residual random variation statistically:

    ηᵢ = |Δᵢ| / Tᵢ                  (shift as a fraction of tolerance)

    T_assy^Δ(η) = Σ ηᵢ|aᵢ|Tᵢ  +  √( Σ [(1 − ηᵢ)aᵢTᵢ]² )

At η = 0 this collapses to RSS; at η = 1 it collapses to worst-case. Worst-case and RSS are
the two endpoints of one family, which is the sense in which Greenwood and Chase "unify"
matters.

**This is the single most important formula for FDM work**, because FDM mean shifts are large,
systematic, and knowable. If you measure that your holes come out 0.15 mm undersize with a
0.05 mm spread, you have Δ = −0.15 and σ = 0.05 — do not average that into a symmetric ±0.2.

But note: if you have *measured* the shift, the better move is to **put it in the nominal**.
Correct the model or the slicer, re-measure to confirm, and then work with a genuinely
centred, smaller tolerance. Mean-shift models are for variation you know exists but cannot
remove — e.g. spool-to-spool differences you will not re-characterise each time.

## 6. Correlation — the one that bites 3D printing

RSS assumes independence. When it does not hold, use the full variance:

    Var(G) = Σᵢ aᵢ²σᵢ²  +  2 Σᵢ<ⱼ aᵢaⱼ Cov(Lᵢ, Lⱼ)

    Cov(Lᵢ, Lⱼ) = ρᵢⱼ σᵢ σⱼ

The sign of the cross term is `aᵢaⱼρᵢⱼ`. So, for positively correlated dimensions:

- **same sign in the chain (aᵢaⱼ > 0) → variance increases.** Correlation hurts.
- **opposite sign (aᵢaⱼ < 0) → variance decreases.** Correlation helps; the common-mode error
  partially cancels.

RSS gets *both* cases wrong. It is not universally optimistic — it is simply blind.

**When to expect correlation in this workflow:**

- Multiple features on the same printed part (share first-layer squish, flow calibration,
  thermal history, Z-step error).
- Different parts printed in the same session on the same machine with the same spool.
- A shared datum feature — if two dimensions are both measured from a face that is itself
  displaced, they move together.
- Thermal expansion across an assembly.
- Multiple pads on the same PCB (share etch compensation and layer registration).

**How to handle it:** define correlation groups in the parameter file
([05](05-parameter-model.md)) and sample the common component once per virtual assembly in
Monte Carlo. That is far easier than assembling a covariance matrix, and it is exactly what
the physical situation is: one shared cause, several affected dimensions.

    L_i = λ_i + Δ_i + s_i · z_common + ε_i        z_common ~ N(0,1) drawn once per assembly
                                                   ε_i ~ independent residual

## 7. Sensitivity and contribution ranking

For an RSS stack, each term's share of the total variance is

    contribution_i = (aᵢTᵢ)² / Σⱼ (aⱼTⱼ)²

This is the most actionable output of the whole exercise. Because it is a *squared* measure,
it concentrates hard: a term with twice the tolerance of another contributes four times the
variance. In practice, two or three terms usually account for 70–90% of a stack, and the rest
are noise. Tighten the top contributor or nothing.

For Monte Carlo with correlations or non-linearity, compute contributions by
variance-decomposition instead: re-run with input *i* frozen at its mean and observe the drop
in Var(G).

## 8. Monte Carlo

The default method. Algorithm:

```
for k in 1..N:
    for each correlation group g:
        z_g ← sample N(0,1)                    # shared cause, once per assembly
    for each dimension i:
        L_i ← λ_i + Δ_i + s_i·z_g(i) + sample(dist_i)
    G_k ← f(L_1, …, L_n)                       # the real function, not the linearisation
report: mean(G), sd(G), percentiles, P(G < 0), histogram
```

**Sample size.** The standard error of an estimated failure probability p is √(p(1−p)/N). To
resolve p ≈ 0.001 to within a relative 10%, you need N ≈ 10⁵. For the decisions you are
making, N = 10⁵ is plenty and runs in well under a second in NumPy; N = 10⁶ if you are
chasing a tail. Do not report more significant figures than √(p/N) supports.

**Choosing input distributions.** For this workflow:

| Input | Sensible default |
|---|---|
| FDM dimension, characterised | Normal with measured (Δ, σ); or the empirical sample itself |
| FDM dimension, uncharacterised | Uniform over your believed range — honest about ignorance, and conservative |
| Bought part with a datasheet ± | Uniform, unless the datasheet states a distribution. A supplier's ± is a spec limit, not a 3σ |
| PCB thickness | Normal, ±10% as roughly 3σ (fab houses do control this) |
| Screw/fastener dimensions | Uniform over the ISO tolerance class |
| Anything you guessed | Uniform, and flag it in the parameter file |

The instinct to reach for the normal distribution everywhere is wrong. A supplier's stated
tolerance is a *limit* they undertake not to exceed; assuming it is 3σ of a normal is an
assumption you have not earned. Uniform is the defensible default for spec-limit inputs.

**Reading a Monte Carlo result honestly.** If the empirical distribution of G is visibly
non-normal — skewed, or with a shoulder — say so, and report percentiles rather than mean ±
3σ. The whole reason to run Monte Carlo is that you did not have to assume normality; do not
throw that away in the reporting.

## 9. Acceptance criteria

Decide *before* you compute what result would be acceptable. Options, roughly in order of
increasing sophistication:

- **Worst-case passes** (G_min ≥ 0). The strongest statement. Aim for this on anything
  safety-relevant or unreworkable.
- **P(G < 0) below a threshold.** For a one-off, 1% is fine. For twenty units, you want ~0.1%
  or you will be filing parts. Express it as "1 in N assemblies will need rework" — it makes
  the decision concrete.
- **Cpk of the gap** ≥ 1.33 against its requirement limits. Useful if you want a single number
  comparable across chains.
- **Margin ratio** γ / T_assy. Quick to eyeball; > 1 means RSS passes at 3σ.

Also decide what happens when a criterion fails — that is [06 §6](06-workflow.md).

---

## 10. Worked example: PCB retained between an enclosure boss and a lid rib

### The chain

A printed enclosure, a PCB resting on printed bosses, and a printed lid whose ribs bear on
the top of the board. The functional gap G is the residual clearance; G < 0 means the lid
will not close (or will bow the board), G > ~1 mm means the board rattles.

| i | Dimension | a | λ (mm) | T (mm) | Source |
|---|---|---|---|---|---|
| 1 | Enclosure internal height, floor to lid seat | +1 | 10.00 | 0.30 | printed, Z |
| 2 | Boss height above floor | −1 | 5.00 | 0.20 | printed, Z |
| 3 | PCB thickness | −1 | 1.60 | 0.16 | fab, ±10% |
| 4 | Lid rib height | −1 | 3.00 | 0.20 | printed, Z |

    γ = 10.00 − 5.00 − 1.60 − 3.00 = 0.40 mm

### Worst case

    T^arith = 0.30 + 0.20 + 0.16 + 0.20 = 0.86 mm
    G ∈ [−0.46, +1.26] mm

**Fails.** Worst-case interference of 0.46 mm. If this were a one-off safety part, stop here
and redesign.

### RSS

    T^stat = √(0.30² + 0.20² + 0.16² + 0.20²) = √0.1956 = 0.442 mm
    G ∈ [−0.042, +0.842] mm at ±3σ

    σ_G = 0.442/3 = 0.1474 mm
    P(G < 0) = Φ(−0.40/0.1474) = Φ(−2.713) ≈ 0.0033

**≈ 3300 ppm, about 1 assembly in 300.** For a hobby build, acceptable. For twenty units,
you will almost certainly never see a failure.

### Contribution ranking

| Dimension | (aT)² | Share of variance |
|---|---|---|
| Enclosure internal height | 0.0900 | **46.0%** |
| Boss height | 0.0400 | 20.4% |
| Lid rib height | 0.0400 | 20.4% |
| PCB thickness | 0.0256 | 13.1% |

The enclosure height dominates. Halving its tolerance to 0.15 would drop T^stat to
√(0.0225+0.04+0.0256+0.04) = 0.368 mm and P(G<0) to Φ(−3.26) ≈ 0.00056. Halving the PCB
tolerance instead would achieve almost nothing. **This ranking is the deliverable**; the
failure probability is just context for it.

### Bender inflation

    T^stat(Bender) = 1.5 × 0.442 = 0.663 mm
    σ_G = 0.221,  P(G < 0) = Φ(−1.809) ≈ 0.035

**3.5%, about 1 in 28.** Now marginal. This is the value of knowing what your T actually
means: the difference between "fine" and "you will hit this" is entirely down to whether
those printed tolerances are 3σ or 2σ figures.

### Correlation, case A: this chain (correlation helps)

Dimensions 1, 2 and 4 are all printed Z-heights sharing a common bias. Take ρ = 0.6 between
each pair, σᵢ = Tᵢ/3, and PCB thickness independent.

    σ₁ = 0.1000,  σ₂ = 0.0667,  σ₃ = 0.0533,  σ₄ = 0.0667
    Σ aᵢ²σᵢ² = 0.021733                          (this is just RSS, σ_G = 0.1474)

    Cov(1,2) = Cov(1,4) = 0.6 × 0.1000 × 0.0667 = 0.00400
    Cov(2,4)             = 0.6 × 0.0667 × 0.0667 = 0.00267

    signs:  a₁a₂ = −1,  a₁a₄ = −1,  a₂a₄ = +1

    2 × [(−1)(0.00400) + (−1)(0.00400) + (+1)(0.00267)] = −0.01067

    Var(G) = 0.021733 − 0.010667 = 0.011066
    σ_G = 0.1052,  P(G < 0) = Φ(−3.80) ≈ 7×10⁻⁵

**Correlation makes this chain better, by a factor of ~45 in failure rate.** The reason is
physical and obvious once seen: if the printer runs everything tall, the cavity grows *and*
the boss and rib grow, and the errors substantially cancel. RSS missed this by assuming
independence.

### Correlation, case B: a same-sign chain (correlation hurts)

Change the design to four printed spacers in series inside a 21.00 mm cavity:

    G = L_cavity − (s₁ + s₂ + s₃ + s₄),   λ: 21.00 − 4×5.00,  γ = 1.00 mm
    T_cavity = 0.30, T_spacer = 0.20 each

    Independent RSS: √(0.09 + 4×0.04) = 0.500,  σ_G = 0.1667
                     P(G < 0) = Φ(−6.0) ≈ 1×10⁻⁹

Now the four spacers are printed together and correlated at ρ = 0.6. All four have a = −1, so
all six pairs have aᵢaⱼ = +1:

    Cov(sᵢ,sⱼ) = 0.6 × 0.0667² = 0.002667,  6 pairs
    2 × 6 × 0.002667 = +0.032

    Var(G) = 0.027778 + 0.032 = 0.059778
    σ_G = 0.2445,  3σ = 0.733
    P(G < 0) = Φ(−4.09) ≈ 2.2×10⁻⁵

**The failure rate rose by a factor of ~20,000**, and the effective assembly tolerance moved
from 0.50 (RSS) most of the way to 1.10 (worst case). Nothing about the parts changed — only
the assumption.

### What the example is for

Two lessons, and they are the reason this document set exists:

1. **The method choice changes the answer by orders of magnitude** — 7×10⁻⁵ to 3.5% across
   the treatments above, on identical inputs. Report which method you used and why, always.
2. **Correlation can go either way and RSS cannot tell you which.** For 3D-printed
   assemblies, where common-cause variation is the norm rather than the exception, this is
   the argument for Monte Carlo with explicit correlation groups over any closed-form method.

## 11. Beyond 1D

When the chain involves rotations, contact conditions, or floating fasteners, the linear
model runs out. The literature offers three approaches:

- **Vector loop / direct linearisation** (Chase and co-workers, Brigham Young ADCATS).
  Kinematic loop equations with small-displacement assumptions; solved for sensitivities.
  Well documented and implementable.
- **Small displacement torsors (SDT)** and **T-Maps**. Represent the allowed variation of a
  feature as a set in a six-dimensional displacement space; propagate by Minkowski sums and
  intersections. Rigorous, mathematically heavy, and the mainstream of European academic
  work.
- **Monte Carlo over a parametric CAD model.** Perturb parameters, rebuild, measure. Slow
  (seconds per sample) but conceptually trivial and exact for whatever the model captures.
  Viable for a few thousand samples of a small FreeCAD assembly overnight.

For the assemblies in scope here, the third is almost always the right call when 1D is
insufficient, because you already have the parametric model.

For a survey of the underlying mathematical models, see the Springer review "A comprehensive
review of tolerance analysis models", *Int. J. Adv. Manuf. Technol.* (2018),
[doi:10.1007/s00170-018-1920-2](https://doi.org/10.1007/s00170-018-1920-2).

---

Previous: [01 — Concepts](01-concepts.md) · Next: [03 — Standards](03-standards.md)
