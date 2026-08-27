#!/usr/bin/env python3
"""Convert a Markdown document into a Maxima notebook (.macnb).

The guide documents are prose, so they become all-markdown notebooks. Splitting
happens on level-2 headings, which gives cell granularity that matches how the
documents are actually structured. Code fences are respected, so a `##` inside a
fenced block does not split a cell.

Links are rewritten for the flat rendered site (docs/pages/*.html):

    NN-name.md                              -> NN-name.html
    ../notebooks/tolerance-mathematics.macnb -> tolerance-mathematics.html
    ../README.md                             -> index.html
    ../templates/*.yaml                      -> GitHub blob URL

Usage:
    python3 tools/md2macnb.py <input.md> <output.macnb>
"""

from __future__ import annotations

import json
import re
import sys
import uuid
from pathlib import Path

REPO_BLOB = "https://github.com/cmsd2/tolerances/blob/main"

# (pattern, replacement) applied to the target of every markdown link.
LINK_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^(?:\.\./)?(?:docs/)?(\d{2}-[a-z0-9-]+)\.md(#.*)?$"), r"\1.html\2"),
    (re.compile(r"^\.\./notebooks/([a-z0-9-]+)\.macnb(#.*)?$"), r"\1.html\2"),
    (re.compile(r"^(?:\.\./)?README\.md(#.*)?$"), r"index.html\1"),
    (re.compile(r"^\.\./(templates/.*)$"), rf"{REPO_BLOB}/\1"),
    (re.compile(r"^(?:\.\./)?(notebooks/.*\.macnb)$"), rf"{REPO_BLOB}/\1"),
]

LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")

# nbconvert derives heading ids from the heading text with spaces hyphenated and
# punctuation kept -- "## 6. Measurement and its uncertainty" becomes
# "6.-Measurement-and-its-uncertainty", NOT GitHub's "6-measurement-and-its-uncertainty".
# Any cross-document anchor must be written in nbconvert's form; check a rendered
# page with `grep -o 'id="[^"]*"'` when adding one.
FENCE_RE = re.compile(r"^\s*(```|~~~)")
H2_RE = re.compile(r"^## ")


def rewrite_target(target: str) -> str:
    if target.startswith(("http://", "https://", "#", "mailto:")):
        return target
    for pattern, replacement in LINK_RULES:
        if pattern.match(target):
            return pattern.sub(replacement, target)
    return target


def rewrite_links(text: str) -> str:
    return LINK_RE.sub(
        lambda m: f"[{m.group(1)}]({rewrite_target(m.group(2))})", text
    )


def split_cells(text: str) -> list[str]:
    """Split on level-2 headings, ignoring headings inside fenced code blocks."""
    chunks: list[list[str]] = [[]]
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence and H2_RE.match(line) and any(
            ln.strip() for ln in chunks[-1]
        ):
            chunks.append([])
        chunks[-1].append(line)
    return ["\n".join(c).strip() + "\n" for c in chunks if any(ln.strip() for ln in c)]


def make_notebook(cells: list[str]) -> dict:
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "name": "maxima",
                "display_name": "Maxima",
                "language": "maxima",
            },
            "aximar": {},
        },
        "cells": [
            {
                "cell_type": "markdown",
                "id": uuid.uuid4().hex[:8],
                "source": source,
                "metadata": {},
            }
            for source in cells
        ],
    }


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    src, dst = Path(argv[1]), Path(argv[2])
    text = rewrite_links(src.read_text(encoding="utf-8"))

    # Drop the trailing prev/next navigation rule: the generated index and the
    # notebook ordering carry navigation on the rendered site.
    text = re.sub(r"\n---\n+(?:Previous|Next|\[Back).*$", "\n", text, flags=re.S)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps(make_notebook(split_cells(text)), indent=1, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(f"{src} -> {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
