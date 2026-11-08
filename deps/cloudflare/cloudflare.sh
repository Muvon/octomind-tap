#!/usr/bin/env bash
# dep: cloudflare/cloudflare
# type: mcp
# description: Cloudflare MCP Server - manage Cloudflare Workers and storage; KV namespaces, R2 buckets, D1 databases and DNS records, run via npx with an API token
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
