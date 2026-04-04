#!/usr/bin/env bash
# dep: joshrutkowski/applescript
# type: mcp
# description: AppleScript MCP — 45 tools for macOS control
# check: npx
# https://github.com/joshrutkowski/applescript-mcp

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

info "AppleScript MCP requires Node.js — already available via npx"
