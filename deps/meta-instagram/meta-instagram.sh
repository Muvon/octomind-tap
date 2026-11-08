#!/usr/bin/env bash
# dep: meta-instagram/meta-instagram
# type: mcp
# description: Meta Instagram Graph API MCP Server - publish Reels and Stories; also feed video and carousels from a Business or Creator account, needs META_ACCESS_TOKEN
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
