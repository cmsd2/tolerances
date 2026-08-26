# 05 — The Parameter Model

One version-controlled file holds every dimension in the project, its variation, and where
that variation figure came from. FreeCAD reads from it. KiCad reads from it. The analysis
reads from it. Nothing keeps a private copy.

This document explains the schema and, more importantly, *why it is shaped that way*. The
complete worked example is [`templates/parameters.example.yaml`](../templates/parameters.example.yaml).

---

## 1. Why a file and not a spreadsheet

Spreadsheets are the industry default for tolerance work and they have real advantages: fast
to start, everyone can read one, trivial to do arithmetic in.

They lose on the things that matter over a project's life:

| | Spreadsheet | Version-controlled text |
|---|---|---|
| Diff two versions | effectively impossible | `git diff` |
| Why did this change? | lost | commit message |
| Comment on a value | a cell note nobody reads | inline, adjacent, permanent |
| Drive FreeCAD/KiCad from it | fragile export dance | direct parse |
| Review a change before accepting | no | yes |
| Merge two people's edits | no | yes |
| Formula errors | silent, invisible | visible in the diff |

The decisive one is the second row. Six months from now the question will be "why is this
clearance 0.4 and not 0.3?" A spreadsheet cannot answer it. A commit can.

**Use both.** YAML is the source of truth; generate a CSV or spreadsheet view for reading and
for sharing with anyone who wants to look at numbers in a grid. Generation is one-directional
— never edit the CSV.

## 2. Design principles

### 2.1 Every value carries its provenance

The most important field in the schema is `source`. A tolerance is one of:

- `measured` — from a characterisation campaign, with `n` and a date
- `supplier_spec` — from a datasheet or capability page, with a URL and read date
- `standard` — from ISO 2768, ISO 286, an IPC table
- `assumed` — you made it up

All four are legitimate. What is not legitimate is *not knowing which*. When a stack-up comes
out marginal, the first question is always "which of these inputs is real?" — and `assumed`
values are where you go looking. A report that lists its assumed inputs separately is worth
far more than one that doesn't.

### 2.2 Variation is (offset, spread), not ±T

Per [04 §1](04-process-capability.md), FDM error is mostly systematic. The schema's default
representation is therefore a distribution with an explicit `offset`, not a symmetric
tolerance. A plain `±T` is still allowed — it is what supplier datasheets give you — but it
is modelled as a *uniform* distribution over the interval unless you say otherwise, because a
supplier's ± is a limit, not a 3σ.

### 2.3 Process capability is referenced, not repeated

Twenty printed dimensions share one printer/material/profile combination. Their variation is
described once, in `processes:`, and each parameter names its process and feature class. Then
re-characterising the printer updates twenty parameters by editing one block.

This is also what makes the model portable: change `process: mk4_pla_04_02` to
`process: bambu_petg_04_02` on a part and its tolerances follow.

### 2.4 Correlation groups are first-class

Per [02 §6](02-methods.md), common-cause variation between features on the same printed part
is the dominant modelling error in 3D-printed assemblies, and it can push the answer either
way. The schema therefore has a `correlations:` section, and each parameter may name a group.

The model is the physical one: a shared latent cause, sampled once per virtual assembly,
affecting every member.

    L_i = nominal_i + offset_i + s_i · z_group + ε_i

where `z_group ~ N(0,1)` is drawn once per assembly and `share` sets what fraction of the
variance is common-mode. `share: 0` recovers independence; `share: 1` makes the group move
rigidly together.

Guessing `share` is fine and far better than the alternative, which is silently assuming 0.
Start at 0.5 for features on one part, 0.3 for parts printed in one session, and run the
analysis at 0, 0.5 and 1.0 to see whether it even matters — often it doesn't, and then you can
stop worrying about it.

### 2.5 Consumers are declared

Each parameter lists what reads it — the FreeCAD document and spreadsheet alias, the KiCad
reference. This gives you two things: a script can push values out automatically, and you can
answer "what breaks if I change this?" by grep.

### 2.6 Stacks live in the same file

A stack-up is not a separate artefact; it is a statement about parameters. Keeping it beside
them means the expression cannot drift out of sync with the dimensions it references, and a
diff shows both together.

## 3. Schema reference

### Top level

```yaml
schema_version: 1
project: <name>
units: mm            # everything is mm; angles in degrees where used
processes:    { … }  # capability library
correlations: { … }  # common-cause groups
parameters:   { … }  # the dimensions
stacks:       { … }  # the assembly criteria
```

### `processes:`

A named process, its identifying configuration, and its measured capability by feature class.

```yaml
processes:
  <process_id>:
    kind: fdm | pcb_fab | pcb_assembly | purchased | machined
    # identifying configuration — enough to reproduce
    printer: <str>
    material: <str>
    brand_colour: <str>          # colour matters; see 04 §2
    nozzle: <float>
    layer_height: <float>
    profile: <path>              # committed slicer profile
    profile_sha256: <str>
    characterised: <YYYY-MM-DD>
    compensation:                # where bias is corrected; see 04 §9
      location: slicer | cad | none
      <setting>: <value>
      note: <str>
    classes:
      <external_xy|internal_xy|external_z|internal_z>:
        offset: <float>          # constant bias 'a'  (mm)
        scale:  <float>          # proportional bias 'b' (dimensionless)
        sigma:  <float>          # random spread (mm)
        sigma_upper95: <float>   # upper 95% CB — use this in stacks
        n: <int>
        dist: normal | uniform | triangular | empirical
        samples: <path>          # if dist: empirical
```

A parameter's total variation is then derived:

    offset_total = offset + scale × nominal
    spread       = sigma_upper95   (by default)

### `correlations:`

```yaml
correlations:
  <group_id>:
    description: <str>
    share: <0.0–1.0>     # fraction of member variance that is common-mode
```

### `parameters:`

```yaml
parameters:
  <param_id>:
    nominal: <float>
    description: <str>
    # EITHER reference a process:
    process: <process_id>
    feature_class: <class>
    # OR state the tolerance explicitly:
    tolerance:
      type: symmetric | asymmetric | limits
      value: <float>              # for symmetric
      plus: <float>               # for asymmetric
      minus: <float>
      dist: uniform | normal | triangular | empirical
      offset: <float>             # optional explicit bias
    source: measured | supplier_spec | standard | assumed
    reference: <str>              # URL, standard clause, campaign id
    correlation_group: <group_id>
    fixed: true|false             # true = a constant, contributes no variation
    consumers:
      freecad:
        document: <str>
        spreadsheet: <str>
        alias: <str>
      kicad:
        board: <str>
        item: <str>
    notes: <str>
```

### `stacks:`

```yaml
stacks:
  <stack_id>:
    description: <str>
    criticality: key | normal      # key characteristic? see 01 §8
    expression: "<arithmetic over param ids>"
    requirement:
      min: <float>                 # null for unbounded
      max: <float>
      target: <float>
    acceptance:
      method: worst_case | rss | monte_carlo
      max_failure_rate: <float>    # for monte_carlo
      samples: <int>
    path:                          # documentation of the physical route
      - {param: <id>, sign: +1, note: <str>}
    notes: <str>
```

`expression` is authoritative — signs come from the arithmetic. `path` exists so a human can
check the loop closes, which is the error that formulas hide. Keep them consistent; a
validator should check that `path` and `expression` reference the same parameters with the
same signs.

## 4. A note for whoever implements the evaluator

`expression` is a string from a configuration file that gets evaluated as arithmetic. **Do not
use Python's `eval()`.** Even in a personal project this is the wrong habit, and the file may
later come from a shared repository or a generated source.

Use one of:

- `ast.parse(expr, mode="eval")` followed by a walk that rejects any node type outside
  `Expression, BinOp, UnaryOp, Name, Constant, Call(whitelisted)`, `Add, Sub, Mult, Div, Pow,
  USub, UAdd` — about thirty lines, no dependency, and it fails closed.
- the `simpleeval` or `asteval` package, which do the same thing maintained.

Also validate on load: every name in `expression` resolves to a defined parameter, every
`process`/`correlation_group` reference exists, no parameter is defined twice, and units are
consistent. Failing loudly on a malformed parameter file is much better than silently
producing a stack-up over a typo'd name.

## 5. Suggested repository layout

```
tolerances/
├── README.md
├── docs/                       these documents
├── params/
│   ├── parameters.yaml         the source of truth
│   └── capability/
│       ├── mk4_pla_04_02.yaml  per-process capability, if it grows too big to inline
│       └── campaigns/          raw measurement data, CSV, never edited
├── profiles/                   committed slicer profiles + hashes
├── cad/                        FreeCAD documents
├── pcb/                        KiCad project
├── tools/                      the scripts (see 06)
├── reports/                    generated stack-up reports — committed, so they diff
└── templates/
    └── parameters.example.yaml
```

Two conventions worth adopting:

- **Commit generated reports.** A stack-up report in git means a code review shows "this
  change moved the lid clearance failure rate from 0.1% to 3%". That is the single most
  useful review signal you can have.
- **Never edit raw measurement CSVs.** They are evidence. Corrections go in a separate file
  with a reason.

---

Previous: [04 — Process capability](04-process-capability.md) · Next: [06 — Workflow](06-workflow.md)
