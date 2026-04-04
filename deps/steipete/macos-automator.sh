#!/usr/bin/env bash
# dep: steipete/macos-automator
# type: mcp
# description: macOS Automator MCP — AppleScript, JXA execution
# check: npx
# https://www.npmjs.com/package/@steipete/macos-automator-mcp

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

info "macOS Automator MCP requires Node.js — already available via npx"
