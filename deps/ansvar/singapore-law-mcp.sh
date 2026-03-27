#!/usr/bin/env bash
# dep: ansvar/singapore-law-mcp
# description: Singapore Law MCP Server
# check: npx
set -euo pipefail
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"
if pkg_check npx; then exit 0; fi
install_dep nodejs/node
info "Singapore Law MCP requires Node.js — already available via npx"
