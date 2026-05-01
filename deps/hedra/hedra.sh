#!/usr/bin/env bash
# dep: hedra/hedra
# type: mcp
# description: Hedra Character-3 MCP Server — image-to-talking-character video
# check: npx
# https://www.hedra.com/docs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Hedra MCP Server requires Node.js — already available via npx"
