#!/usr/bin/env python3
"""Replace the hand-typed worked examples with live Maxima cells.

Converting the guide to notebooks is only worth doing if the arithmetic becomes
executable. This rewrites the two worked-example sections so every number is
computed at build time:

    notebooks/guide/02-methods.macnb    section 10  (lid / boss / PCB stack)
    notebooks/guide/08-kicad-pcb.macnb  section 5   (USB-C aperture chain)

Run once after md2macnb.py. Idempotent: it matches on the section heading and
replaces whatever is there.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

CHAIN_TABLE = """\
## 10. Worked example: PCB retained between an enclosure boss and a lid rib

A printed enclosure, a PCB resting on printed bosses, and a printed lid whose ribs bear on
the top of the board. The functional gap $G$ is the residual clearance; $G < 0$ means the lid
will not close (or will bow the board), $G > 1$ mm means the board rattles.

| $i$ | Dimension | $a_i$ | $\\lambda_i$ (mm) | $T_i$ (mm) | Source |
|---|---|---|---|---|---|
| 1 | Enclosure internal height, floor to lid seat | $+1$ | 10.00 | 0.30 | printed, Z |
| 2 | Boss height above floor | $-1$ | 5.00 | 0.20 | printed, Z |
| 3 | PCB thickness | $-1$ | 1.60 | 0.16 | fab, ±10% |
| 4 | Lid rib height | $-1$ | 3.00 | 0.20 | printed, Z |

Everything below is computed, not transcribed. The chain is defined once in the next cell and
every figure in this section derives from it.
"""

SETUP = """\
/* The chain — the only place these numbers are written down. */
λs    : [10.00, 5.00, 1.60, 3.00]$          /* nominals            */
as    : [   +1,   -1,   -1,   -1]$          /* sign in the chain   */
Ts    : [ 0.30, 0.20, 0.16, 0.20]$          /* tolerance half-width */
names : ["enclosure height", "boss height", "PCB thickness", "lid rib height"]$

/* Standard normal CDF, for turning a z-score into a failure probability. */
Φ(z) := float( (1 + erf(z/sqrt(2)))/2 )$

aT : map("*", map(abs, as), Ts)$            /* |a_i| T_i */
γ  : apply("+", map("*", as, λs));          /* nominal gap */
"""

WC_MD = """\
### Worst case

Assume every dimension sits simultaneously at its least favourable limit."""

WC_CODE = """\
T_wc : apply("+", aT);
[γ - T_wc, γ + T_wc];      /* the guaranteed range of G */
"""

WC_TAIL = """\
**Fails** — worst-case interference of 0.46 mm. If this were a one-off safety part, stop here
and redesign."""

RSS_MD = """\
### RSS

Treat the four dimensions as independent and combine in quadrature."""

RSS_CODE = """\
T_rss  : float( sqrt( apply("+", map(lambda([u], u^2), aT)) ) );
σ_G    : T_rss/3$
P_fail : Φ(-γ/σ_G);
print("about 1 assembly in", round(1/P_fail), "fails")$
"""

RSS_TAIL = """\
For a hobby build, acceptable. Across twenty units you would almost certainly never see a
failure."""

CONTRIB_MD = """\
### Contribution ranking

**This is the deliverable**; the failure probability is only context for it. Because the
measure is squared it concentrates hard — a term with twice the tolerance of another
contributes four times the variance."""

CONTRIB_CODE = """\
tot : apply("+", map(lambda([u], u^2), aT))$
for i thru length(aT) do
    print( names[i], ":", float(100*aT[i]^2/tot), "percent of variance" )$

/* What halving the top contributor would buy, versus halving the smallest. */
retol(newT) := block([v : sqrt(apply("+", map(lambda([u], u^2), newT)))],
                     [float(v), Φ(-γ/(float(v)/3))])$
print("halve enclosure height:", retol([0.15, 0.20, 0.16, 0.20]))$
print("halve PCB thickness   :", retol([0.30, 0.20, 0.08, 0.20]))$
"""

CONTRIB_TAIL = """\
The enclosure height carries 46% of the variance. Halving it drops the failure rate about
eight-fold; halving the PCB tolerance instead barely moves it. Attack the top one or two terms
or nothing."""

BENDER_MD = """\
### Bender inflation

The correction applied when a quoted $T$ is really a $2\\sigma$ figure rather than the
$3\\sigma$ that RSS assumes (see §5.1)."""

BENDER_CODE = """\
T_bender : 1.5 * T_rss;
P_bender : Φ(-γ/(T_bender/3));
print("about 1 assembly in", round(1/P_bender), "fails")$
"""

BENDER_TAIL = """\
Now marginal. The whole difference between "fine" and "you will hit this" is whether those
printed tolerances were 3σ or 2σ figures — which is a question about your measurement
process, not your design."""

CORR_MD = """\
### Correlation

Dimensions 1, 2 and 4 are all printed Z-heights sharing a common bias. RSS assumed they were
independent; they are not. The full variance is

$$Var(G) = \\sum_i a_i^2 \\sigma_i^2 + 2 \\sum_{i<j} a_i a_j \\rho_{ij} \\sigma_i \\sigma_j$$

and the sign of each cross term is the sign of $a_i a_j$."""

CORR_CODE = """\
varG(avec, Tvec, corr) := block([m : length(avec), σv, s],
    σv : map(lambda([t], t/3), Tvec),
    s  : 0,
    for i thru m do
      for j thru m do
        s : s + avec[i]*avec[j]*corr(i,j)*σv[i]*σv[j],
    float(s))$

indep(i,j) := if i = j then 1 else 0$

/* CASE A — this chain. Printed Z dims are 1, 2, 4; the PCB (3) is independent. */
caseA(i,j) := if i = j then 1 elseif i = 3 or j = 3 then 0 else 0.6$

print("independent : σ_G =", float(sqrt(varG(as, Ts, indep))),
      " P(G<0) =", Φ(-γ/sqrt(varG(as, Ts, indep))))$
print("correlated  : σ_G =", float(sqrt(varG(as, Ts, caseA))),
      " P(G<0) =", Φ(-γ/sqrt(varG(as, Ts, caseA))))$
"""

CORR_TAIL = """\
**Correlation makes this chain better**, by a factor of about 45 in failure rate. The reason
is physical: the cavity enters with $+1$ while the boss and rib enter with $-1$, so if the
printer runs everything tall the errors largely cancel. RSS could not see this, having already
assumed the dimensions were unrelated.

Now the opposite case — four printed spacers in series, where every term has the same sign."""

CASEB_CODE = """\
asB : [   +1,   -1,   -1,   -1,   -1]$
TsB : [ 0.30, 0.20, 0.20, 0.20, 0.20]$
γB  : 21.00 - 4*5.00$

caseB(i,j) := if i = j then 1 elseif i = 1 or j = 1 then 0 else 0.6$

pB_indep : Φ(-γB/sqrt(varG(asB, TsB, indep)))$
pB_corr  : Φ(-γB/sqrt(varG(asB, TsB, caseB)))$

print("independent : 3σ =", float(3*sqrt(varG(asB, TsB, indep))), " P(G<0) =", pB_indep)$
print("correlated  : 3σ =", float(3*sqrt(varG(asB, TsB, caseB))), " P(G<0) =", pB_corr)$
print("worst case bound =", apply("+", map(abs, map("*", asB, TsB))))$
print("failure rate ratio =", float(pB_corr/pB_indep))$
"""

CASEB_TAIL = """\
**The failure rate rose by a factor of about 22,000**, and the effective assembly tolerance
moved from 0.50 (RSS) most of the way to 1.10 (worst case). Nothing about the parts changed —
only the assumption.

### What the example is for

1. **The method choice changes the answer by orders of magnitude** — from $7\\times10^{-5}$ to
   3.5% across the treatments above, on identical inputs. Always report which method you used
   and why.
2. **Correlation can go either way and RSS cannot tell you which.** For 3D-printed assemblies,
   where common-cause variation is the norm, this is the argument for Monte Carlo with
   explicit correlation groups over any closed-form method."""

USBC = """\
## 5. Worked chain: a USB-C aperture in a printed wall

The canonical failure. The plug must enter the aperture; a USB-C receptacle offers roughly
±0.4 mm of positional latitude before the plug fouls.

| # | Contributor | Typical | Source |
|---|---|---|---|
| 1 | Board outline routing tolerance | ±0.20 | fab spec, uniform |
| 2 | Connector placement on board | ±0.10 reflow | assembly |
| 3 | Connector body to its own footprint centre | ±0.15 | datasheet |
| 4 | Board seating clearance in the cavity | ±0.25 | design + printed cavity |
| 5 | Printed wall position relative to cavity datum | ±0.20 | printer, external XY |
| 6 | Printed aperture position within the wall | ±0.15 | printer, external XY |

Board edge to connector centre as *designed* is exact by construction in KiCad, so it
contributes nominal but no variation."""

USBC_CODE = """\
cnames : ["board routing", "connector placement", "connector body",
          "board seating", "wall position", "aperture position"]$
cT     : [0.20, 0.10, 0.15, 0.25, 0.20, 0.15]$
budget : 0.40$                     /* USB-C positional latitude */

wc  : apply("+", cT);
rss : float( sqrt( apply("+", map(lambda([u], u^2), cT)) ) );

print("worst case", wc, if wc  <= budget then "PASS" else "FAIL")$
print("RSS       ", rss, if rss <= budget then "PASS" else "FAIL")$

tot : apply("+", map(lambda([u], u^2), cT))$
for i thru length(cT) do
    print( cnames[i], ":", float(100*cT[i]^2/tot), "percent of variance" )$

/* What if the top contributor were eliminated entirely? */
print("RSS without board seating:",
      float( sqrt( tot - 0.25^2 ) ))$
"""

USBC_TAIL = """\
**Both fail**, and this is with machine placement — hand-soldered, contributor 2 triples and
it gets worse.

The instructive part is the last line: **no tolerance tightening fixes this.** Even
eliminating the largest contributor outright leaves RSS at 0.37 mm against a 0.40 mm budget.
The answer has to be a design change:

- **Oversize the aperture and add a generous internal chamfer.** Removes contributors 5 and 6
  from mattering and guides the plug. Nearly free.
- **Locate the board off the connector, not the board edge.** Make the aperture a close-fitting
  pocket around the connector body, with the board floating on slotted mounting holes. This
  deletes contributors 1 and 4 — the two largest — from the chain entirely. This is the right
  answer, and it is the one a stack-up tool will never suggest.
- **Use a panel-mount connector on a pigtail.** Decouples the domains completely, at the cost
  of a cable.
- **Recess the receptacle** behind a larger opening so the plug's own moulding does the
  guiding.

The general principle: **choose your datum to be the feature that matters.** Locating the board
by its edge when what you care about is the connector position is a self-inflicted wound."""


def cell(kind: str, source: str) -> dict:
    return {
        "cell_type": kind,
        "id": uuid.uuid4().hex[:8],
        "source": source if source.endswith("\n") else source + "\n",
        "metadata": {},
        **({"outputs": [], "execution_count": None} if kind == "code" else {}),
    }


def replace_section(path: Path, heading: str, blocks: list[tuple[str, str]]) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    idx = next(
        i for i, c in enumerate(nb["cells"]) if c["source"].startswith(heading)
    )
    nb["cells"][idx : idx + 1] = [cell(k, s) for k, s in blocks]
    path.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{path}: replaced {heading.strip()!r} with {len(blocks)} cells")


def main() -> int:
    replace_section(
        Path("notebooks/guide/02-methods.macnb"),
        "## 10. Worked example",
        [
            ("markdown", CHAIN_TABLE),
            ("code", SETUP),
            ("markdown", WC_MD),
            ("code", WC_CODE),
            ("markdown", WC_TAIL),
            ("markdown", RSS_MD),
            ("code", RSS_CODE),
            ("markdown", RSS_TAIL),
            ("markdown", CONTRIB_MD),
            ("code", CONTRIB_CODE),
            ("markdown", CONTRIB_TAIL),
            ("markdown", BENDER_MD),
            ("code", BENDER_CODE),
            ("markdown", BENDER_TAIL),
            ("markdown", CORR_MD),
            ("code", CORR_CODE),
            ("markdown", CORR_TAIL),
            ("code", CASEB_CODE),
            ("markdown", CASEB_TAIL),
        ],
    )
    replace_section(
        Path("notebooks/guide/08-kicad-pcb.macnb"),
        "## 5. Worked chain",
        [
            ("markdown", USBC),
            ("code", USBC_CODE),
            ("markdown", USBC_TAIL),
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
