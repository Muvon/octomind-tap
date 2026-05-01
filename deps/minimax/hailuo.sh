#!/usr/bin/env bash
# dep: minimax/hailuo
# type: mcp
# description: MiniMax Hailuo 02 MCP Server — cheapest viable text-to-video and image-to-video for volume tests
# check: npx
# https://www.minimax.io/platform/document/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "MiniMax Hailuo MCP Server requires Node.js — already available via npx"
