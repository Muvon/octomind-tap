#!/usr/bin/env bash
# dep: upload-post/upload-post
# type: mcp
# description: Upload-Post MCP Server - publish and schedule videos to YouTube, TikTok and more through one hosted posting API
# check: npx
# https://github.com/Upload-Post/upload-post-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — npx is available (node is installed); the capability pins the package version
if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

if ! pkg_check npx; then
  die "npx not found after installing Node.js"
fi

info "Upload-Post MCP Server runs via npx"
