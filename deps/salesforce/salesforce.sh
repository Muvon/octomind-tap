#!/usr/bin/env bash
# dep: salesforce/salesforce
# type: mcp
# description: Salesforce MCP Server - query CRM objects and manage records; runs Apex code, handles triggers and debug logs, via npx, auth by CLI, password or OAuth
# check: npx
# https://www.npmjs.com/package/@tsmztech/mcp-server-salesforce

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed)
if pkg_check npx; then
  exit 0
fi

# Ensure node is available
install_dep nodejs/node

info "Salesforce MCP Server requires Node.js — already available via npx"
