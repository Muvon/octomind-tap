#!/usr/bin/env bash
# dep: google/youtube-data
# type: mcp
# description: YouTube Data API v3 MCP Server — Shorts and long-form upload, metadata edit, analytics
# check: npx
# https://developers.google.com/youtube/v3

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "YouTube Data API MCP Server requires Node.js — already available via npx"
