#!/usr/bin/env bash
# dep: openai/sora
# type: mcp
# description: OpenAI Sora 2 video generation — long coherent shots via the OpenAI Video API
# check: npx
# https://platform.openai.com/docs/guides/video

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "OpenAI Sora MCP Server requires Node.js — already available via npx"
