#!/usr/bin/env bash
# dep: codefuturist/email
# type: mcp
# description: Email MCP Server — SMTP/IMAP email via standard protocols
# check: npx
# https://github.com/codefuturist/email-mcp

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check npx; then
  exit 0
fi

install_dep nodejs/node

info "Email MCP Server requires Node.js — already available via npx"
