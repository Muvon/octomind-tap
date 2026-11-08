#!/usr/bin/env bash
# dep: stripe/stripe
# type: mcp
# description: Stripe MCP Server - manage payments, customers and subscriptions; includes invoices through auto-discovered tools, runs via npx, needs STRIPE_SECRET_KEY
# check: npx
# https://www.npmjs.com/package/@stripe/mcp

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

info "Stripe MCP Server requires Node.js — already available via npx"
