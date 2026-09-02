#!/usr/bin/env bash
# dep: xdevplatform/xurl
# type: mcp
# description: xurl MCP bridge — official X API MCP (api.x.com/mcp) with OAuth handled locally
# check: npx
# https://github.com/xdevplatform/xurl

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "xurl MCP bridge requires Node.js — already available via npx"
