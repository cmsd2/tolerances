# 01 — Concepts and General Approaches

This document establishes vocabulary and surveys the approaches the literature offers. It is
deliberately light on formulas; those are in [02 — Methods](02-methods.md).

---

## 1. Variation, not error

A manufactured dimension is not a number. It is a random variable with a distribution,
produced by a process. "Error" implies a mistake; "variation" implies an inherent property of
the process that you characterise, budget for, and design around. The shift in language is
the whole discipline.

Three things describe a dimension in this framework:

- **Nominal** (λ): the value in the CAD model.
- **Bias / mean shift** (Δ = μ − λ): how far the process actually centres from nominal.
  Usually assumed zero. In FDM it is emphatically not zero.
- **Spread** (σ, or a tolerance T): how much part-to-part variation there is around the mean.

Classical tolerancing collapses these into a single symmetric ±T and assumes Δ = 0. Much of
the sophistication in the literature is about relaxing that.

## 2. Tolerance, limits, and fits

A **tolerance** is the total permissible variation of a dimension. **Limits** are the
resulting maximum and minimum values (upper/lower limits of size). Tolerances may be
**bilateral** (10.0 ±0.1), **unilateral** (10.0 +0.2/−0.0), or expressed as **limits**
(10.0/10.2).

Two terms from the ISO 286 fits system that are worth internalising even though you will
rarely achieve their grades on a printer:

- **MMC** (maximum material condition): the limit of size at which the feature contains the
  most material — largest shaft, smallest hole. This is the fit-critical condition.
- **LMC** (least material condition): the opposite — smallest shaft, largest hole. This is
  the wall-thickness- and strength-critical condition.

A **fit** is the relationship between two mating features: **clearance** (always a gap),
**interference** (always negative gap, i.e. press), or **transition** (may be either
depending on where in the tolerance zones the two parts land).

## 3. The tolerance chain

A **tolerance chain** (or loop, or stack) is a path through an assembly from one side of a
functional gap to the other, passing through part features. Each step contributes its
nominal and its variation. The gap closes the loop.

The functional requirement is expressed as an **assembly criterion**, conventionally written
G, which is a function of the part dimensions:

    G = f(L₁, L₂, …, Lₙ)

and the requirement is a condition on G, most often G ≥ 0 (parts must not interfere) or
G ∈ [G_min, G_max] (there must be clearance, but not too much).

Constructing G correctly is the part that requires engineering judgement, and it is the part
that expensive software automates. Three rules keep you honest:

1. **The loop must close.** Start at one face of the gap and end at the other, with no jumps.
   If you cannot draw the path on a sketch, you do not have a chain.
2. **Signs come from direction.** A dimension traversed in the positive direction contributes
   +1; traversed against, −1. Errors of sign are the most common mistake.
3. **Only include what varies.** A dimension that is not on the path does not belong in the
   chain, no matter how important it is elsewhere.

## 4. Analysis versus synthesis

These are the two directions of the same problem and the literature keeps them distinct:

- **Tolerance analysis** (bottom-up): given part tolerances, what is the assembly variation?
  This is what you do to check a design.
- **Tolerance synthesis** / **allocation** (top-down): given a required assembly variation,
  how should tolerance be distributed among the parts to satisfy it at least cost? This is
  what you do to *fix* a design.

Analysis is easy; allocation is an optimisation problem and is where most of the recent
research sits. Hong and Chang's 2002 survey and Nigam and Turner's 1995 review both organise
the field along this axis. For your purposes: analyse by hand, allocate by intuition plus a
contribution ranking (see [02 §7](02-methods.md)), and reach for formal optimisation only if
you find yourself repeatedly trading tolerances across many parts.

## 5. The three families of method

### Worst-case (arithmetic) tolerancing

Assume every dimension is simultaneously at its least favourable limit. Sum the tolerances.

*Guarantees* 100% interchangeability: if worst-case passes, no assembly can ever fail to fit.
It is also brutally conservative — the probability of every dimension in a six-part chain
being at its extreme in the correct direction simultaneously is vanishingly small.

Use it when: safety-critical; you are building one unit and cannot tolerate a rework; the
chain is short (two or three terms, where the conservatism is mild); or the parts are
genuinely not independent.

### Statistical tolerancing (RSS and its descendants)

Treat dimensions as independent random variables and combine their variances. The classical
form is root-sum-square. It yields dramatically tighter predicted assembly variation, at the
price of accepting some small fraction of non-conforming assemblies.

Scholz's framing is the clearest: worst-case and RSS *"provide conservative and optimistic
benchmarks, respectively."* Neither is the truth. The truth is between them, and the whole
apparatus of inflation factors and mean-shift models is an attempt to say where.

The known weaknesses, each of which has a fix in the literature:

| Assumption | Reality | Fix |
|---|---|---|
| Dimensions are independent | Same machine, same batch, same operator ⇒ correlation | Explicit covariance ([02 §6](02-methods.md)) |
| T = 3σ | Process owners often quote T meaning 2σ | Bender's 1.5 inflation factor |
| Distributions are normal | Tool wear ⇒ uniform; two-cavity moulds ⇒ bimodal | Distributional inflation factors c |
| Processes are centred on nominal | Centring is hard and drifts | Mean-shift models (Greenwood & Chase) |

### Monte Carlo simulation

Sample each dimension from its distribution, evaluate G, repeat. Build the empirical
distribution of G and read off whatever you want: mean, spread, percentiles, P(G < 0).

This is the method to default to, because it makes no linearity assumption, handles arbitrary
distributions, handles correlation, handles asymmetric and offset distributions, and handles
non-linear geometry (angles, projections, contact conditions). It also refuses to hide its
assumptions: you have to state a distribution for every input, which is exactly the
discipline you want.

Its cost is that it gives you a number, not a formula. Which is why you still compute
worst-case and RSS alongside — they are cheap, and their divergence from the Monte Carlo
result tells you something is odd in your model.

## 6. Process capability

The bridge between "what my process does" and "what I can put in a stack-up."

- **Cp** = (USL − LSL) / 6σ — how the process *spread* compares to the tolerance width.
  Ignores centring.
- **Cpk** = min[(USL − μ)/3σ, (μ − LSL)/3σ] — the same, penalised for being off-centre.
  Cpk ≤ Cp always, with equality only for a perfectly centred process.

Rules of thumb: Cpk ≥ 1.33 is a capable process; Cpk ≥ 1.0 is marginal; Cpk < 1.0 means you
are producing scrap by design. A well-tuned desktop FDM printer on a modest dimension will
struggle to reach Cpk 1.33 against a ±0.1 mm tolerance, and will manage it easily against
±0.4 mm. That statement is the entire reason to measure: it tells you which tolerances you
can afford to specify.

Two cautions. First, Cp and Cpk assume normality; FDM data is often skewed and sometimes
bimodal, and the indices then mislead. ISO 22514-4 defines percentile-based variants for
exactly this case. Second, the "Six Sigma" convention of adding a 1.5σ long-term mean shift
is an industrial convention with a contested empirical basis — use it if you want a
conservative margin, but do not treat it as physics.

## 7. Cost and the point of the exercise

The economic argument for statistical tolerancing is that manufacturing cost rises steeply,
roughly exponentially, as tolerance tightens. Every classical text has a version of the
cost–tolerance curve.

For a desktop printer this argument mostly does *not* apply — printing to ±0.1 mm costs the
same as printing to ±0.5 mm, because you cannot buy precision at any price; you either have
it or you don't. What replaces cost as the currency is **feasibility and effort**: a tighter
tolerance means slower prints, more calibration, more scrapped parts, more post-processing
(reaming, filing, sanding), or a different process entirely.

So the practical objective shifts. In industry, tolerance analysis exists to *save money*.
For you it exists to **decide whether the design is buildable at all on the equipment you
own, and if not, which single change makes it buildable**. That change is very often a
design change rather than a tolerance change — see
[06 §"Design moves"](06-workflow.md#design-moves-that-beat-tolerance-analysis).

## 8. Key characteristics

Not every dimension matters. A **key characteristic** (KC) is one whose variation
significantly affects fit, function or safety. The discipline is to identify the handful of
KCs early, track them explicitly, and leave everything else to general tolerances.

For a printed enclosure with a PCB, the KC list is typically short and predictable:

- connector aperture position relative to the board datum
- lid-to-boss height stack (board retention)
- mounting hole pattern position
- snap-fit or thread engagement depth
- any bearing, shaft or magnet pocket

Five to ten items. Everything else gets ISO 2768-medium and no further thought.

---

## Where this comes from

The two orienting surveys, if you want the shape of the whole field:

- **Nigam, S.D. & Turner, J.U. (1995)**, "Review of statistical approaches to tolerance
  analysis", *Computer-Aided Design* 27(1), 6–15. Covers RSS, system moments, quadrature,
  reliability index, Taguchi methods and Monte Carlo.
- **Hong, Y.S. & Chang, T.C. (2002)**, "A comprehensive review of tolerancing research",
  *Int. J. Production Research* 40(11), 2425–2459.

The single most useful free document on the methods themselves:

- **Scholz, F. (1995)**, *Tolerance Stack Analysis Methods*, Boeing Information & Support
  Services, ISSTECH-95-030. Freely available. Rigorous, honest about the weaknesses of every
  method, and the source of most of [02](02-methods.md).

The standard practitioner text:

- **Fischer, B.R. (2011)**, *Mechanical Tolerance Stackup and Analysis*, 2nd ed., CRC Press.
  Written by a member of the ASME Y14.5 committee.

Full annotated list, including the Springer titles available on your subscription, in
[09 — Bibliography](09-bibliography.md).

---

Previous: [00 — Orientation](00-orientation.md) · Next: [02 — Methods](02-methods.md)
