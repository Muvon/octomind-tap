#!/usr/bin/env bash
# dep: cybeleri/social-scheduler
# type: mcp
# description: Social Media Scheduler MCP — multi-platform content scheduling
# check: npx
# https://www.npmjs.com/package/@cybeleri/social-media-scheduler-mcp

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

info "Social Media Scheduler MCP requires Node.js — already available via npx"
