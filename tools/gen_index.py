#!/usr/bin/env python3
"""Generate docs/pages/index.html from the built notebooks.

Titles come from the H1 of each notebook's first markdown cell rather than from
the filename, so "02-methods.macnb" is listed as its real heading. Ordering is by
filename, which is why the guide documents are numbered.
"""

from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "docs/pages"))
NOTEBOOK_DIR = Path("notebooks")

SECTION_BLURB = {
    "guide": "The documentation set, in reading order. Start at Orientation; if you "
             "want to begin doing something this week, jump to the Workflow.",
    "mathematics": "Symbolic derivations behind the methods, with every constant "
                   "computed rather than quoted.",
}

STYLE = """\
:root { color-scheme: light dark; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
       max-width: 46rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.55;
       color: #24292f; background: #fff; }
h1 { font-size: 1.6rem; border-bottom: 1px solid #d0d7de; padding-bottom: .4rem; }
h2 { font-size: 1.05rem; margin-top: 2rem; color: #57606a; text-transform: uppercase;
     letter-spacing: .04em; }
p.blurb { color: #57606a; font-size: .93rem; margin-top: .3rem; }
ol { padding-left: 1.4rem; }
li { margin: .35rem 0; }
li span { color: #57606a; font-size: .9rem; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }
footer { margin-top: 2.5rem; border-top: 1px solid #d0d7de; padding-top: .6rem;
         font-size: .85rem; color: #6e7781; }
@media (prefers-color-scheme: dark) {
  body { color: #e6edf3; background: #0d1117; }
  h1, footer { border-color: #30363d; }
  h2, p.blurb, li span, footer { color: #8b949e; }
  a { color: #4493f8; }
}
"""


def title_of(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        m = re.search(r"^#\s+(.+)$", source, re.M)
        if m:
            return m.group(1).strip()
    return nb_path.stem


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    sections: dict[str, list[tuple[str, str]]] = {}

    for nb in sorted(NOTEBOOK_DIR.glob("*/*.macnb")):
        target = OUTPUT_DIR / f"{nb.stem}.html"
        if not target.exists():
            continue
        sections.setdefault(nb.parent.name, []).append((nb.stem, title_of(nb)))

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Tolerance Management for 3D Printing</title>",
        f"<style>{STYLE}</style></head><body>",
        "<h1>Tolerance Management for a Desktop 3D-Printing + PCB Workflow</h1>",
        "<p>An open alternative to proprietary tolerance-analysis software, for "
        "FreeCAD, KiCad and FDM printing. The mathematics of tolerance analysis is "
        "easy and free; the hard parts are knowing your actual process capability "
        "and keeping one honest source of truth for every dimension.</p>",
    ]

    for section in sorted(sections):
        parts.append(f"<h2>{html.escape(section.replace('-', ' '))}</h2>")
        if blurb := SECTION_BLURB.get(section):
            parts.append(f'<p class="blurb">{html.escape(blurb)}</p>')
        parts.append("<ol>")
        for stem, title in sections[section]:
            # "02 — Methods: The Mathematics" -> number and title shown separately
            m = re.match(r"^(\d+)\s*[—–-]\s*(.*)$", title)
            label = html.escape(m.group(2) if m else title)
            parts.append(f'  <li><a href="{html.escape(stem)}.html">{label}</a></li>')
        parts.append("</ol>")

    parts += [
        "<footer>Built from Maxima notebooks with "
        '<a href="https://github.com/cmsd2/aximar">Aximar</a> and '
        '<a href="https://github.com/cmsd2/maxima-nbconvert">maxima-nbconvert</a>. '
        'Source: <a href="https://github.com/cmsd2/tolerances">cmsd2/tolerances</a>.'
        "</footer>",
        "</body></html>",
    ]

    (OUTPUT_DIR / "index.html").write_text("\n".join(parts) + "\n", encoding="utf-8")
    total = sum(len(v) for v in sections.values())
    print(f"index.html: {total} notebooks in {len(sections)} sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
