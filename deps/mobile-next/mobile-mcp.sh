#!/usr/bin/env bash
# dep: mobile-next/mobile-mcp
# type: mcp
# description: Mobile MCP Server — iOS & Android device automation (real devices + simulators/emulators)
# check: npx
# https://github.com/mobile-next/mobile-mcp

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

info "Mobile MCP requires Node.js — already available via npx"
info "Note: iOS automation needs Xcode + Xcode CLT; Android needs platform-tools (adb)."
