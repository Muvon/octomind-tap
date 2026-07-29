#!/usr/bin/env bash
# dep: heygen/heygen
# type: mcp
# description: HeyGen MCP Server — AI avatar UGC video generation
# check: uvx
# https://docs.heygen.com/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check uvx; then
  exit 0
fi

install_dep astral-sh/uv

info "HeyGen MCP Server requires uv/uvx — already available"
