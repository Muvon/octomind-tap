#!/usr/bin/env bash
# dep: us-legal-tools/courtlistener
# description: CourtListener MCP Server — US court cases, legal research, opinions
# check: npx
# https://www.npmjs.com/package/@us-legal-tools/courtlistener-sdk

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

info "CourtListener MCP Server requires Node.js — already available via npx"
