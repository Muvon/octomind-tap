#!/usr/bin/env bash
# dep: huggingface/huggingface
# type: mcp
# description: Hugging Face MCP Server — ML models, datasets, Spaces discovery
# check: npx
# https://github.com/huggingface/hf-mcp-server

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed)
if pkg_check npx; then
  exit 0
fi

# Ensure node is available
install_dep nodejs/node

info "Hugging Face MCP Server requires Node.js — already available via npx"
