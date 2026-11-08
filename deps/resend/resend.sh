#!/usr/bin/env bash
# dep: resend/resend
# type: mcp
# description: Resend MCP Server - send transactional email via Resend; manage contacts, broadcasts, domains and webhooks, runs via npx, needs RESEND_API_KEY
# check: npx
# https://github.com/resend/mcp-send-email

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

info "Resend MCP Server requires Node.js — already available via npx"
