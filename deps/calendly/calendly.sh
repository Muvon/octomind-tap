#!/usr/bin/env bash
# dep: calendly/calendly
# type: mcp
# description: Calendly MCP Server - manage Calendly events and event types; invitees and availability, authenticates with a Personal Access Token or OAuth 2.0
# check: npx
# https://github.com/meAmitPatil/calendly-mcp-server

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

info "Calendly MCP Server requires Node.js — already available via npx"
