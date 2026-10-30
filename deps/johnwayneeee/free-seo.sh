#!/usr/bin/env bash
# dep: johnwayneeee/free-seo
# type: mcp
# description: Ensures uvx is available for the experimental free-seo-mcp keyword discovery server
# check: uvx
# https://github.com/JohnWayneeee/free-seo-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check uvx; then exit 0; fi
install_dep astral-sh/uv
pkg_check uvx || die "uvx not found after install"
