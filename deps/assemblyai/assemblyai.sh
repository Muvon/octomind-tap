#!/usr/bin/env bash
# dep: assemblyai/assemblyai
# type: mcp
# description: AssemblyAI MCP Server - speech-to-text with speaker diarization; auto-chapters, sentiment and SRT/VTT caption output, run via npx with an API key
# check: npx
# https://www.assemblyai.com/docs

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "AssemblyAI MCP Server requires Node.js — already available via npx"
