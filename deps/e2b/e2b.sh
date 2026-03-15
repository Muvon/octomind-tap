#!/usr/bin/env bash
# dep: e2b/e2b
# description: E2B MCP Server — secure code execution sandbox for Python/JS
# check: npx
# https://www.npmjs.com/package/@e2b/mcp-server

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

info "E2B MCP Server requires Node.js — already available via npx"
