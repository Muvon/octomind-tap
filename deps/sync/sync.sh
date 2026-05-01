#!/usr/bin/env bash
# dep: sync/sync
# type: mcp
# description: Sync.so MCP Server — drop-in lipsync postprocess for any video
# check: npx
# https://docs.sync.so/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Sync.so MCP Server requires Node.js — already available via npx"
