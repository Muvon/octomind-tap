#!/usr/bin/env bash
# dep: google-maps/maps
# type: mcp
# description: Google Maps MCP Server - geocoding, directions and place search; distance matrix, elevation, timezone, weather and air quality via @cablate/mcp-google-map
# check: npx
# https://www.npmjs.com/package/@iflow-mcp/mcp-google-map

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

info "Google Maps MCP Server requires Node.js — already available via npx"
