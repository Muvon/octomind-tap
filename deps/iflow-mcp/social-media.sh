#!/usr/bin/env bash
# dep: iflow-mcp/social-media
# description: Social Media MCP — multi-platform posting, scheduling
# check: npx
# https://www.npmjs.com/package/@iflow-mcp/2389-research-mcp-socialmedia

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

info "Social Media MCP requires Node.js — already available via npx"
