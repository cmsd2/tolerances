AXIMAR_MCP ?= aximar-mcp
OUTPUT_DIR ?= docs/pages
FORMAT     ?= maxima_html

NOTEBOOKS  := $(wildcard notebooks/*/*.macnb)
HTML_FILES := $(addprefix $(OUTPUT_DIR)/,$(addsuffix .html,$(basename $(notdir $(NOTEBOOKS)))))

.PHONY: all site index clean import-md serve

all: site

# Full build: execute every notebook, export, regenerate the index.
site:
	./build.sh

# Per-notebook incremental rule, so `make $(OUTPUT_DIR)/02-methods.html` works.
define nb_rule
$(OUTPUT_DIR)/$(basename $(notdir $(1))).html: $(1) | $(OUTPUT_DIR)
	$$(AXIMAR_MCP) run --allow-dangerous $$<
	uv run jupyter nbconvert --to $$(FORMAT) --output-dir $$(OUTPUT_DIR) \
	    --output $$(basename $$(notdir $$<) .macnb) $$<
endef
$(foreach nb,$(NOTEBOOKS),$(eval $(call nb_rule,$(nb))))

$(OUTPUT_DIR):
	mkdir -p $@

index: | $(OUTPUT_DIR)
	python3 tools/gen_index.py

# One-shot importer for a new Markdown draft:
#     make import-md FILE=draft.md SECTION=guide
# The notebooks are the source of truth; this is only for bringing in new prose.
import-md:
	@test -n "$(FILE)" || { echo "usage: make import-md FILE=draft.md [SECTION=guide]"; exit 2; }
	python3 tools/md2macnb.py "$(FILE)" \
	    "notebooks/$(or $(SECTION),guide)/$(basename $(notdir $(FILE))).macnb"

serve: site
	python3 -m http.server -d $(OUTPUT_DIR) 8000

clean:
	rm -rf $(OUTPUT_DIR)
