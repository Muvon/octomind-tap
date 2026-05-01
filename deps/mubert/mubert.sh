#!/usr/bin/env bash
# dep: mubert/mubert
# type: mcp
# description: Mubert MCP Server — royalty-safe AI music generation for ad soundtracks
# check: npx
# https://docs.mubert.com/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Mubert MCP Server requires Node.js — already available via npx"
