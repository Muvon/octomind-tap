#!/usr/bin/env bash
# dep: raydeck/handle-checker
# description: Social Media Handle Checker — username availability
# check: npx
# https://www.npmjs.com/package/@raydeck/social-media-handle-checker-mcp

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

info "Social Media Handle Checker MCP requires Node.js — already available via npx"
