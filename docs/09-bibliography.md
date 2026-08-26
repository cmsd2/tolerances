# 09 — Annotated Bibliography

Access markers: **[free]** · **[springer]** available on a Springer institutional subscription
· **[open]** open-access journal · **[buy]** paid.

---

## Start here

**Scholz, F. (1995).** *Tolerance Stack Analysis Methods.* Boeing Information & Support
Services, ISSTECH-95-030, December 1995. **[free]** —
[faculty.washington.edu/fscholz/Reports/isstech-95-030.pdf](https://faculty.washington.edu/fscholz/Reports/isstech-95-030.pdf)

> The best free document on the subject, and the primary source for
> [02 — Methods](02-methods.md). Covers worst-case, RSS, RSS with inflation factors for
> non-normal distributions, and several treatments of mean shifts. Gives the assumptions
> before each formula and is candid about which are unlikely to hold. The distribution
> inflation-factor table (Figure 6) is reproduced in [02 §5.2](02-methods.md) and derived
> from first principles in the [Maxima notebook](../notebooks/tolerance-mathematics.macnb).
> Its companion, Scholz (1995) *"A Critical Look at Tolerance Stacking Methods"*, carries the
> derivations.

**Fischer, B.R. (2011).** *Mechanical Tolerance Stackup and Analysis*, 2nd ed. CRC Press /
Taylor & Francis. ISBN 978-1439815724. **[buy]**

> The practitioner's standard text, by a member of the ASME Y14.5 committee. Covers form
> tolerances in stackups, 3D tolerance analysis, and Six Sigma concepts. If you buy one book
> on this subject, buy this one.

## Surveys — the shape of the field

**Nigam, S.D. & Turner, J.U. (1995).** "Review of statistical approaches to tolerance
analysis." *Computer-Aided Design* 27(1), 6–15. **[buy]**

> The canonical survey. Covers RSS, system moments, quadrature, the reliability index,
> Taguchi methods and Monte Carlo. Still the clearest map of the statistical methods.

**Hong, Y.S. & Chang, T.C. (2002).** "A comprehensive review of tolerancing research."
*Int. J. Production Research* 40(11), 2425–2459.
[doi:10.1080/00207540210128242](https://doi.org/10.1080/00207540210128242) **[buy]**

> Broader than Nigam & Turner: representation, specification, analysis, allocation and
> transfer. The reference for placing any particular technique in context.

**"A comprehensive review of tolerance analysis models."** *Int. J. Adv. Manuf. Technol.*
(2018). [doi:10.1007/s00170-018-1920-2](https://doi.org/10.1007/s00170-018-1920-2)
**[springer]**

> Modern survey of the mathematical models — vector loop, small displacement torsors,
> T-Maps, matrix and Jacobian methods. The place to start if you need to go beyond 1D.

## Springer books on your subscription

**Geometric Tolerancing Standard to Machine Design: A Design-for-Fit Approach** (2024).
[doi:10.1007/978-3-031-47585-6](https://link.springer.com/book/10.1007/978-3-031-47585-6)
**[springer]**

> **The most directly useful of the Springer titles for your purposes.** Works from "what fit
> do I need" back to the geometric tolerance statements required to achieve it — which is
> precisely the question a designer actually has, and the reverse of how most GD&T books are
> organised.

**Colosimo, B.M. & Senin, N. (eds.) (2011).** *Geometric Tolerances: Impact on Product
Design, Quality Inspection and Statistical Process Monitoring.* Springer.
[doi:10.1007/978-1-84996-311-4](https://link.springer.com/book/10.1007/978-1-84996-311-4)
**[springer]**

> Tolerance selection, how tolerances stack in assemblies, inspection of geometrically
> toleranced parts, and SPC. Strong on the measurement and monitoring half, which is the part
> [04 — Process capability](04-process-capability.md) is about.

**Wartzack, S. (ed.) (2024).** *Research in Tolerancing.* Springer.
[doi:10.1007/978-3-031-64225-8](https://link.springer.com/book/10.1007/978-3-031-64225-8)
**[springer]**

> Current research. Notable chapters: "Tolerances in Mechanisms" (Husch & Walter), and
> "Sampling-Based Tolerance-Cost Optimization", which is the modern treatment of tolerance
> allocation via metaheuristics over Monte Carlo analysis.

**ElMaraghy, H.A. (ed.) (1998).** *Geometric Design Tolerancing: Theories, Standards and
Applications.* Springer.
[doi:10.1007/978-1-4615-5797-5](https://link.springer.com/book/10.1007/978-1-4615-5797-5)
**[springer]**

> The classic collected volume. Dated in its computational assumptions, foundational in its
> theory.

## Statistical tolerancing — primary sources

**Greenwood, W.H. & Chase, K.W. (1987).** "A new tolerance analysis method for designers and
manufacturers." *J. Engineering for Industry* 109(2), 112–116. **[buy]**

> The mean-shift model that unifies worst-case and RSS as endpoints of one family. The
> formula in [02 §5.3](02-methods.md).

**Bender, A. (1968).** "Statistical Tolerancing as it Relates to Quality Control and the
Designer." SAE Technical Paper 680490. **[buy]**

> The origin of the 1.5 inflation factor ("benderising"). Scholz cites a 1962 date; the
> widely available publication is the 1968 SAE paper. Read Scholz's §3.3 first — his account
> of *why* 1.5 is a fix for a communication failure about the meaning of T, rather than an
> empirical universal, corrects the common folklore.

**Chase, K.W. & Parkinson, A.R. (1991).** "A survey of research in the application of
tolerance analysis to the design of mechanical assemblies." *Research in Engineering Design*
3, 23–37. **[springer]**

> Chase's group at Brigham Young (ADCATS) produced the vector-loop / direct-linearisation
> method, which remains the most implementable approach to 2D and 3D chains.

**Grohmann, P. & Walter, M.S.J. (2021).** "Speeding up Statistical Tolerance Analysis to Real
Time." *Applied Sciences* 11(9), 4207.
[doi:10.3390/app11094207](https://doi.org/10.3390/app11094207) **[open]**

> Open access, with working code at
> [github.com/EinmalmitProfis/Statistical-Tolerance-Analysis-and-Synthesis-with-Python](https://github.com/EinmalmitProfis/Statistical-Tolerance-Analysis-and-Synthesis-with-Python).
> Covers analysis *and* synthesis with GPU acceleration. The most rigorous open codebase in
> this space and the best model to copy from.

## Additive manufacturing accuracy

**Accuracy of FDM PLA Polymer 3D Printing Technology Based on Tolerance Fields.** *Processes*
11(10), 2810 (2023). [doi:10.3390/pr11102810](https://doi.org/10.3390/pr11102810) **[open]**

> Places FDM PLA within the ISO 286 IT-grade system — roughly IT9 to IT14 depending on
> nominal size and axis — and presents a calibration procedure. The empirical anchor for the
> claims in [03 §3](03-standards.md) and the size-dependence model in
> [04 §7](04-process-capability.md).

**The Impact of Elevated Printing Speeds and Filament Color on the Dimensional Precision and
Tensile Properties of FDM-Printed PLA Specimens** (2025). PMC12349424. **[open]**

> Evidence that filament colour affects dimensional outcomes — the basis for treating
> (brand, material, colour) as the unit of characterisation in
> [04 §2](04-process-capability.md).

**Evaluation of the surface roughness and dimensional accuracy of low-cost 3D-printed parts
made of PLA–aluminum** (2024). PMC10878859. **[open]**

## Standards

Full treatment in [03 — Standards](03-standards.md). The essential list:

| Standard | Title | Access |
|---|---|---|
| ISO 8015:2011 | GPS — Fundamentals: concepts, principles and rules | [buy] |
| ISO 286-1/-2:2010 | ISO code system for tolerances on linear sizes | [buy] |
| ISO 1101:2017 | Geometrical tolerancing — form, orientation, location, run-out | [buy] |
| ISO 2768-1:1989 | General tolerances — linear and angular dimensions | [buy] |
| ISO 22081:2021 | General geometrical and size specifications (replaces ISO 2768-2) | [free preview](https://cdn.standards.iteh.ai/samples/72514/78d2a06f1b7a42ddb87e7180c790cc9c/ISO-22081-2021.pdf) |
| ISO 14253-1:2017 | Decision rules for verifying conformity under measurement uncertainty | [buy] |
| ISO 22514-4 | Process capability estimates | [buy] |
| **ISO/ASTM 52902:2023** | **AM — Test artefacts — geometric capability assessment** | [buy] |
| ISO/ASTM 52900:2021 | AM — fundamentals and vocabulary | [buy] |
| ISO/ASTM 52903-2:2020 | Material extrusion of plastics — process equipment | [buy] |
| ASME Y14.5-2018 | Dimensioning and Tolerancing | [buy] |
| ASME Y14.5.1-2019 | Mathematical definition of Y14.5 principles | [buy] |
| IPC-2615 | Printed Board Dimensions and Tolerances | [buy] |
| IPC-2221 | Generic standard on printed board design | [buy] |

**The ISO Online Browsing Platform** ([iso.org/obp](https://www.iso.org/obp)) publishes the
*Terms and definitions* clauses of most ISO standards free of charge. Enough to settle a
vocabulary question without buying the document.

## Software

| Project | Language | License | Status | Notes |
|---|---|---|---|---|
| [stackcore](https://pypi.org/project/stackcore/) | Python | MIT | v0.3.3, Jul 2025, one maintainer | Plane/point-based stacks, Monte Carlo, numba-parallel. Best-maintained option |
| [tol-stack](https://github.com/slightlynybbled/tol-stack) | Python | — | unmaintained, ~13 stars | Simple 1D and true-position; supports skew-normal, which matters for FDM. Worth reading |
| [tolstack](https://github.com/aevyrie/tolstack) | Rust | — | archived-ish | 1D visual editor, MC and RSS. Standalone GUI |
| [Grohmann & Walter](https://github.com/EinmalmitProfis/Statistical-Tolerance-Analysis-and-Synthesis-with-Python) | Python | — | paper companion | Analysis *and* synthesis, CuPy GPU support. The most rigorous |
| [kiutils](https://kiutils.readthedocs.io/) | Python | MIT | active | Pure-Python KiCad file parsing; no KiCad install needed |

Commercial, for reference: RD8 (cloud, 14-day trial, no public pricing), CETOL 6σ (Sigmetrix),
3DCS (DCS), VisVSA (Siemens), Ansys VRXPERIENCE / Tolerance Analysis.

## Related, occasionally useful

**Creveling, C.M. (1997).** *Tolerance Design: A Handbook for Developing Optimal
Specifications.* Addison-Wesley. **[buy]** — the Taguchi-influenced treatment of tolerance
design and quality loss.

**Bjørke, Ø. (1989).** *Computer-Aided Tolerancing*, 2nd ed. ASME Press. **[buy]** — an early
systematic treatment, cited throughout Scholz.

**Henzold, G. (2020).** *Geometrical Dimensioning and Tolerancing for Design, Manufacturing
and Inspection*, 3rd ed. Butterworth-Heinemann. **[buy]** — the best single reference for
**ISO** GD&T specifically, as opposed to ASME. If you work to ISO, this is the book that
Fischer is for ASME.

---

Previous: [08 — KiCad and PCB](08-kicad-pcb.md) · Next: [10 — Glossary](10-glossary.md)
