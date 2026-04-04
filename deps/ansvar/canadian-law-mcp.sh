#!/usr/bin/env bash
# dep: ansvar/canadian-law-mcp
# type: mcp
# description: Canadian Law MCP Server
# check: npx
# https://github.com/muvon/ansvar
set -euo pipefail
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"
if pkg_check npx; then exit 0; fi
install_dep nodejs/node
info "Canadian Law MCP requires Node.js — already available via npx"
