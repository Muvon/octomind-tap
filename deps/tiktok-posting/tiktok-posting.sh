#!/usr/bin/env bash
# dep: tiktok-posting/tiktok-posting
# type: mcp
# description: TikTok Content Posting API MCP Server — direct upload of videos and photos
# check: npx
# https://developers.tiktok.com/doc/content-posting-api-get-started/

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "TikTok Posting MCP Server requires Node.js — already available via npx"
