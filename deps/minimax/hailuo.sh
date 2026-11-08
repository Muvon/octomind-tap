#!/usr/bin/env bash
# dep: minimax/hailuo
# type: mcp
# description: MiniMax Hailuo 02 MCP Server - text and image to video clips; uses the MiniMax Hailuo model, needs MINIMAX_API_KEY, launched through uvx
# check: uvx
# https://www.minimax.io/platform/document/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check uvx; then
  exit 0
fi

install_dep astral-sh/uv

info "MiniMax Hailuo MCP Server requires uv/uvx — already available"
