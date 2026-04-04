#!/usr/bin/env bash
# dep: aws/s3
# type: mcp
# description: AWS S3 MCP Server — object storage, upload, download, list buckets
# check: npx
# https://www.npmjs.com/package/@geunoh/s3-mcp-server

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

info "AWS S3 MCP Server requires Node.js — already available via npx"
