#!/usr/bin/env bash
# dep: mem0ai/mem0
# type: mcp
# description: Mem0 MCP Server - store and search persistent memories on Mem0; update and delete them, graph support, runs through uvx, needs MEM0_API_KEY
# check: uvx
# https://github.com/mem0ai/mem0-mcp

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — uvx is available (uv is installed)
if pkg_check uvx; then
  exit 0
fi

# Ensure uv is available
install_dep astral-sh/uv

info "Mem0 MCP Server requires Python/uv — already available via uvx"
