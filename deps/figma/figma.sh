#!/usr/bin/env bash
# dep: figma/figma
# type: mcp
# description: Figma MCP Server - read Figma files, components and variables; design tokens for design-to-code work, needs a Figma Personal Access Token
# check: npx
# https://www.npmjs.com/package/figma-developer-mcp

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

info "Figma MCP Server requires Node.js — already available via npx"
