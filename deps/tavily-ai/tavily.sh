#!/usr/bin/env bash
# dep: tavily-ai/tavily
# type: mcp
# description: Tavily MCP Server — AI search API for real-time web information and extraction
# check: npx
# https://github.com/tavily-ai/tavily-mcp

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

info "Tavily MCP Server requires Node.js — already available via npx"
