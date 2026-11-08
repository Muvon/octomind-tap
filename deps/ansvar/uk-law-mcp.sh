#!/usr/bin/env bash
# dep: ansvar/uk-law-mcp
# type: mcp
# description: UK Law MCP Server - look up UK laws and statutes; includes legal references, uses the Ansvar @ansvar/uk-law-mcp package, run via npx, no authentication
# check: npx
# https://github.com/muvon/ansvar
set -euo pipefail
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"
if pkg_check npx; then exit 0; fi
install_dep nodejs/node
info "UK Law MCP requires Node.js — already available via npx"
