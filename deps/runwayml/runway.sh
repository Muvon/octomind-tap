#!/usr/bin/env bash
# dep: runwayml/runway
# type: mcp
# description: RunwayML MCP Server — Gen-4 video/image generation
# check: npx
# https://github.com/runwayml/runway-api-mcp-server

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

info "RunwayML MCP Server requires Node.js — already available via npx"
