#!/usr/bin/env bash
# dep: pika/pika
# type: mcp
# description: Pika Labs MCP Server — text-to-video, image-to-video, Pikaffects
# check: npx
# https://pika.art/docs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Pika MCP Server requires Node.js — already available via npx"
