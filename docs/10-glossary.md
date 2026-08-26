# 10 — Glossary

Where ISO and ASME differ, both are given. Symbols follow Scholz (1995), as used in
[02 — Methods](02-methods.md).

---

## Symbols

| Symbol | Meaning |
|---|---|
| Lᵢ | actual value of the i-th part dimension (a random variable) |
| λᵢ | nominal value of the i-th part dimension |
| μᵢ | actual process mean for the i-th dimension |
| Δᵢ | mean shift, Δᵢ = μᵢ − λᵢ |
| σᵢ | standard deviation of the i-th dimension |
| Tᵢ | tolerance (half-width) of the i-th dimension |
| G | assembly criterion — the gap of interest |
| γ | nominal value of G |
| aᵢ | sensitivity coefficient, ∂G/∂Lᵢ; ±1 for a pure length stack |
| cᵢ | distributional inflation factor, c = 3σ/T |
| ηᵢ | mean shift as a fraction of tolerance, \|Δᵢ\|/Tᵢ |
| ρᵢⱼ | correlation coefficient between dimensions i and j |

---

## Terms

**Additive manufacturing (AM)** — the ISO/ASTM term for what everyone else calls 3D printing.
Standards use it exclusively; ISO/ASTM 52900 defines the vocabulary.

**Allocation** — see *synthesis*.

**Annular ring** — the copper remaining around a drilled hole in a PCB. IPC-2221 requires a
minimum of 0.05 mm for Class 2 *after all tolerances*, which is the operative phrase.

**Assembly criterion (G)** — the quantity a tolerance chain computes: a clearance, an
interference, an alignment error. The functional requirement is a condition on it.

**Basic dimension** — a theoretically exact dimension carrying no tolerance of its own;
variation is controlled by an associated geometric tolerance. Boxed on a drawing. ISO calls
it a *theoretically exact dimension* (TED).

**Bias** — the systematic component of error: Δ = μ − λ. The dominant term in FDM and the one
classical tolerancing usually assumes away. See [04 §1](04-process-capability.md).

**Bilateral / unilateral** — a tolerance applied in both directions (10.0 ±0.1) or one
(10.0 +0.2/−0).

**Capability (Cp, Cpk)** — how process spread compares to tolerance width. Cp ignores
centring; Cpk penalises it. Cpk ≥ 1.33 is conventionally "capable". Both assume normality;
ISO 22514-4 gives percentile-based alternatives.

**Chain** — see *tolerance chain*.

**Datum** — a theoretically exact reference (point, axis, plane) from which geometric
relationships are established. A *datum feature* is the real, imperfect surface used to
establish it. Confusing the two is the most common GD&T error.

**Design for fit** — working backwards from the required fit to the tolerance specification,
rather than forwards from a tolerance to whatever fit results.

**DRF (datum reference frame)** — the coordinate system established by a set of datums,
constraining all six degrees of freedom. ISO and ASME construct these differently in detail.

**Elephant's foot** — the outward bulge in the first few layers of an FDM print, caused by the
nozzle squashing hot material against the bed. Makes the base oversize. Measure above it.

**Envelope requirement (Ⓔ)** — the rule that a feature of size must fit within a
perfect-form boundary at MMC. **ASME Rule #1 applies this by default; ISO does not** — under
ISO 8015's independency principle you must invoke it explicitly. The single most important
ISO/ASME difference. See [03 §2](03-standards.md).

**Feature of size** — a feature with opposed elements defining a size: a cylinder, a slot, a
pair of parallel faces. The things ± tolerances legitimately apply to.

**Fit** — the relationship between mating features: *clearance* (always a gap), *interference*
(always a press), or *transition* (either, depending where in the zones the parts land).

**GD&T** — geometric dimensioning and tolerancing. The symbolic language for specifying form,
orientation, location and run-out. ASME Y14.5 or ISO 1101.

**GPS (Geometrical Product Specification)** — the ISO system of ~150 interlocking standards
covering specification and verification of geometry. ISO 8015 states its fundamental rules.

**Guard band** — the reduction of a tolerance zone by the measurement uncertainty, so that a
measurement inside the reduced zone *proves* conformity. ISO 14253-1.

**Independency principle** — the ISO default (ISO 8015): size and form tolerances are
independent unless linked explicitly. Opposite of ASME Rule #1.

**Inflation factor (c)** — a multiplier applied to a term in an RSS stack to account for a
non-normal distribution. Defined as c = 3σ/T. Uniform gives √3 ≈ 1.732. See
[02 §5.2](02-methods.md) and the [Maxima notebook](../notebooks/tolerance-mathematics.macnb).

**IT grade** — the ISO 286 tolerance grade, IT01 to IT18. Lower is tighter; the tolerance for
a given grade widens with nominal size. Machining sits at IT6–IT9, FDM at roughly IT9–IT14.

**Key characteristic (KC)** — a dimension whose variation materially affects fit, function or
safety. Expect five to ten per assembly. Everything else gets general tolerances.

**LMC (least material condition)** — the limit of size leaving the least material: smallest
shaft, largest hole. Governs wall thickness and strength.

**MMC (maximum material condition)** — the limit of size leaving the most material: largest
shaft, smallest hole. Governs fit.

**MBD (model-based definition)** — tolerancing carried on the 3D model rather than a drawing.
ISO 16792 / ASME Y14.41.

**Mean shift** — see *bias*.

**Monte Carlo** — sampling each input from its distribution, evaluating the criterion, and
building the empirical distribution of the result. The default method here, because it makes
no linearity or normality assumption and handles correlation directly.

**Nominal (λ)** — the value in the CAD model. What you asked for.

**Process capability** — what a process can actually hold, measured rather than assumed.
[04](04-process-capability.md).

**RSS (root sum square)** — combining tolerances in quadrature: √(Σaᵢ²Tᵢ²). Assumes
independence, normality, centring, and T = 3σ. Optimistic when those fail.

**Sensitivity coefficient (aᵢ)** — how much the assembly criterion changes per unit change in
a part dimension. ±1 for a pure length stack; computed by differentiation otherwise.

**Statistical tolerancing** — treating dimensions as random variables and accepting a small
non-conformance rate in exchange for looser part tolerances. ASME Y14.5 §2.16 provides a
drawing symbol for it but does not specify the statistics.

**Synthesis (allocation)** — the inverse of analysis: given a required assembly variation,
distribute tolerance among parts at least cost. An optimisation problem.

**Tolerance** — the total permissible variation of a dimension. Note that in most of this
document set T denotes the *half*-width, following Scholz.

**Tolerance chain (stack, loop)** — the path through an assembly from one side of a functional
gap to the other. Must close; signs come from direction of travel. Constructing it correctly
is the part that needs judgement.

**Tolerance zone** — the region within which a toleranced feature must lie. For geometric
tolerances this is a shape (two parallel planes, a cylinder, a region between profile
boundaries), not just a pair of numbers.

**Topological naming problem** — FreeCAD's tendency to lose track of which face or edge a
feature references when parameters change enough to alter topology. Mitigated in 1.0, not
eliminated. Relevant to CAD-driven parameter sweeps. See [07 §6](07-freecad.md).

**True position** — a location tolerance defining a circular (or cylindrical) zone about a
theoretically exact position, rather than a square zone from ± dimensions. Gives 57% more
area for the same worst-case error, which is why it exists.

**Worst case (arithmetic tolerancing)** — assuming every dimension is simultaneously at its
least favourable limit. The only method that guarantees interchangeability; very conservative
for long chains.

**Z quantisation** — the discretisation of printed heights into an integer number of layers.
Makes Z error deterministic rather than random. Design critical Z dimensions as integer
multiples of layer height. See [04 §2](04-process-capability.md).

---

Previous: [09 — Bibliography](09-bibliography.md) · [Back to README](../README.md)
