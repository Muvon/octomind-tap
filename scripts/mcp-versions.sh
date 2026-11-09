#!/usr/bin/env bash
# Manage exact version pins for registry-launched MCP servers.
#
# Every [[mcp.servers]] entry launched via npx (npm) or uvx (PyPI) must pin
# an exact package version so a registry publish can never change what users
# run. lint-capabilities.sh enforces pin presence offline; this script does
# the network side:
#
#   scripts/mcp-versions.sh check [--strict]
#       Compare every pinned version against the registry's latest and print
#       a drift report. Always exits 0 unless --strict is given, in which
#       case any outdated/unpinned/error row exits 1 (for scheduled CI).
#
#   scripts/mcp-versions.sh update [--all | <capability> ...]
#       Rewrite pins to the current registry latest (also pins anything
#       unpinned or tagged @latest). Leaves changes uncommitted for review.
#       Run `test` afterwards to smoke-test the updated servers.
#       A capability file line `# mcp-versions: hold <package>` keeps that
#       pin as is (check reports it as held); state the reason next to it.
#
#   scripts/mcp-versions.sh test [<capability> ...]
#       Spawn each stdio server, perform the MCP initialize handshake and
#       tools/list, and report per server. Tools advertised by the server
#       are matched against the file's roles.mcp allowed_tools globs to
#       catch upstream tool-set changes. Servers needing credentials may
#       fail with a missing-key error — that shows in the report; judge by
#       whether the process starts and speaks MCP at all.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export OCTOTAP_ROOT="$REPO_ROOT"

exec python3 "$REPO_ROOT/scripts/mcp-versions.py" "$@"
