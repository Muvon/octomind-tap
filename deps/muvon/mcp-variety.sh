#!/usr/bin/env bash
# dep: muvon/mcp-variety
# type: mcp
# description: Variety MCP Server - vary openings, lengths and endings; picks them per item in a repeated job, avoids recent combinations and flags AI writing tells
# check: uvx
# https://github.com/muvon/mcp-variety

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

info "Variety MCP Server requires uv/uvx — already available"
