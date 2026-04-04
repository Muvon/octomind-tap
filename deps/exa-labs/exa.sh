#!/usr/bin/env bash
# dep: exa-labs/exa
# type: mcp
# description: Exa MCP Server — AI-powered web search, code search, and company research
# check: npx
# https://github.com/exa-labs/exa-mcp-server

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

info "Exa MCP Server requires Node.js — already available via npx"
