#!/usr/bin/env bash
# dep: ansvar/australian-law-mcp
# type: mcp
# description: Australian Law MCP Server
# check: npx
# https://github.com/muvon/ansvar
set -euo pipefail
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"
if pkg_check npx; then exit 0; fi
install_dep nodejs/node
info "Australian Law MCP requires Node.js — already available via npx"
