#!/usr/bin/env bash
# dep: vercel/vercel
# type: mcp
# description: Vercel MCP Server — deployment and project management
# check: npx
# https://www.npmjs.com/package/vercel-mcp

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

info "Vercel MCP Server requires Node.js — already available via npx"
