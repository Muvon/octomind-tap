#!/usr/bin/env bash
# dep: replicate/replicate
# type: mcp
# description: Replicate MCP Server — AI image generation, Flux, SDXL
# check: npx
# https://www.npmjs.com/package/replicate-flux-mcp

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

info "Replicate MCP Server requires Node.js — already available via npx"
