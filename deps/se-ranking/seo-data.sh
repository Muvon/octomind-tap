#!/usr/bin/env bash
# dep: se-ranking/seo-data
# description: SE Ranking MCP — SEO data, keyword research, site audits
# check: docker
# https://github.com/seranking/seo-data-api-mcp-server

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — docker is available
if pkg_check docker; then
  exit 0
fi

# Ensure docker is available
install_dep containers/docker

info "SE Ranking MCP Server requires Docker — already available"
