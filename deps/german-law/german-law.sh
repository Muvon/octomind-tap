#!/usr/bin/env bash
# dep: german-law/german-law
# type: mcp
# description: German Law MCP Server — federal statutes live from gesetze-im-internet.de
# check: npx
# https://www.npmjs.com/package/german-law-mcp

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

info "German Law MCP Server requires Node.js — already available via npx"
