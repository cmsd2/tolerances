#!/usr/bin/env bash
# Execute every notebook, export to HTML, and regenerate the index.
#
# Usage: ./build.sh [--pdf] [notebook.macnb ...]
#
# With no arguments, builds every notebook under notebooks/.
#
# Requires:
#   - aximar-mcp   (set AXIMAR_MCP, or have it on PATH)
#   - uv           (runs nbconvert from the project venv)
#   - maxima       (the kernel aximar-mcp drives)

set -euo pipefail

AXIMAR_MCP="${AXIMAR_MCP:-aximar-mcp}"
OUTPUT_DIR="${OUTPUT_DIR:-docs/pages}"
FORMAT="maxima_html"

args=()
for arg in "$@"; do
  if [[ "$arg" == "--pdf" ]]; then FORMAT="maxima_pdf"; else args+=("$arg"); fi
done

shopt -s globstar nullglob
if [[ ${#args[@]} -gt 0 ]]; then
  notebooks=("${args[@]}")
else
  notebooks=(notebooks/**/*.macnb)
fi
[[ ${#notebooks[@]} -gt 0 ]] || { echo "No .macnb files found" >&2; exit 1; }

mkdir -p "$OUTPUT_DIR"

echo "==> Executing ${#notebooks[@]} notebook(s)"
for nb in "${notebooks[@]}"; do
  echo "    $nb"
  "$AXIMAR_MCP" run --allow-dangerous "$nb"
done

echo "==> Exporting to $FORMAT"
for nb in "${notebooks[@]}"; do
  name="$(basename "$nb" .macnb)"
  uv run jupyter nbconvert --to "$FORMAT" \
      --output-dir "$OUTPUT_DIR" --output "$name" "$nb" 2>&1 \
    | grep -Ev 'MissingIDFieldWarning|_validate|^\s*$' || true
done

echo "==> Generating index"
python3 tools/gen_index.py

echo "==> Done. Output in $OUTPUT_DIR/"
