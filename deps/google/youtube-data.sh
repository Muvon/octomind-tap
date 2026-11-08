#!/usr/bin/env bash
# dep: google/youtube-data
# type: mcp
# description: YouTube Studio MCP Server - edit YouTube video metadata and SEO; channel analytics via the YouTube Data API v3 (no upload), runs via npx
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
