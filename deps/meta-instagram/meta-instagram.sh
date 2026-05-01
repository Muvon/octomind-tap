#!/usr/bin/env bash
# dep: meta-instagram/meta-instagram
# type: mcp
# description: Meta Instagram Graph API MCP Server — Reels and feed video publishing
# check: npx
# https://developers.facebook.com/docs/instagram-api/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Meta Instagram MCP Server requires Node.js — already available via npx"
