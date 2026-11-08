#!/usr/bin/env bash
# dep: uk-legislation/uk-legislation
# type: mcp
# description: UK Legislation MCP Server - search and read UK law; Acts and statutory instruments via the official legislation.gov.uk API, runs via npx, no API key needed
# check: npx
# https://www.npmjs.com/package/legislation-gov-uk-mcp

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

info "UK Legislation MCP Server requires Node.js — already available via npx"
