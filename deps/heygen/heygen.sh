#!/usr/bin/env bash
# dep: heygen/heygen
# type: mcp
# description: HeyGen MCP Server — AI avatar UGC video generation
# check: npx
# https://docs.heygen.com/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "HeyGen MCP Server requires Node.js — already available via npx"
