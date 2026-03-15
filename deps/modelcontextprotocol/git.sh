#!/usr/bin/env bash
# dep: modelcontextprotocol/git
# description: MCP Git Server — read, search, and manipulate local Git repositories
# check: uvx
# https://github.com/modelcontextprotocol/servers/tree/main/src/git

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — uvx is available (uv is installed)
if pkg_check uvx; then
  exit 0
fi

# Ensure uv is available (provides uvx)
install_dep astral-sh/uv

info "Git MCP Server requires uv/uvx — already available"
