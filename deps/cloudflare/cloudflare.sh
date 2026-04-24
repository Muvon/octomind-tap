#!/usr/bin/env bash
# dep: cloudflare/cloudflare
# type: mcp
# description: Cloudflare MCP Server — Workers, KV, R2, D1, DNS management
# check: npx
# https://github.com/cloudflare/mcp-server-cloudflare

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Cloudflare MCP Server requires Node.js — already available via npx"
