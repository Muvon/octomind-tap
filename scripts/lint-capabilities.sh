#!/usr/bin/env bash
# Lint all capability definitions in capabilities/**/*.toml
#
# Two file kinds, two rule sets:
#
#   capabilities/<cap>/config.toml        — capability-level metadata, required
#     for every capability. Required: `triggers = [...]` (non-empty array of strings).
#     No Title/Description required (file holds only routing metadata).
#
#   capabilities/<cap>/<provider>.toml    — provider-specific MCP wiring.
#     Required: # Title and # Description comment headers, valid mcp wiring,
#     server_refs ↔ [[mcp.servers]] consistency, dep scripts present.
#     Registry-launched servers (npx/uvx, incl. inside sh -c) must pin an
#     exact package version (pkg@X.Y.Z / pkg==X.Y.Z) so a registry publish
#     can never change what users run. Pins are managed by
#     scripts/mcp-versions.sh (check drift / update / smoke-test); this
#     lint stays offline and only enforces that a pin is present.
#
# Plus structural rules: default.toml must exist and be a symlink (except
# for built-in caps: core, agent), and the symlink target must exist.
#
# Usage:
#   scripts/lint-capabilities.sh                  # lint all capabilities
#   scripts/lint-capabilities.sh <cap> [<cap>]    # lint specific capabilities (name or capabilities/<name>)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAP_ROOT="$REPO_ROOT/capabilities"
DEPS_ROOT="$REPO_ROOT/deps"
ERRORS=0
BUILTIN_CAPS=("core" "agent" "orchestration")

# Collect capability dirs to lint
if [[ $# -gt 0 ]]; then
  DIRS=("$@")
else
  while IFS= read -r found; do
    DIRS+=("$found")
  done < <(find "$CAP_ROOT" -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [[ ${#DIRS[@]} -eq 0 ]]; then
  echo "No capability directories found."
  exit 0
fi

is_builtin() {
  local cap="$1"
  for b in "${BUILTIN_CAPS[@]}"; do
    [[ $b == "$cap" ]] && return 0
  done
  return 1
}

lint_capability() {
  local dir="$1"
  local cap_name
  cap_name="$(basename "$dir")"
  local ok=1

  # Check default.toml exists
  local default_file="$dir/default.toml"
  if [[ ! -e $default_file ]]; then
    echo "  ✗ $cap_name: missing default.toml"
    return 1
  fi

  # For non-built-in: default.toml must be a symlink
  if ! is_builtin "$cap_name"; then
    if [[ ! -L $default_file ]]; then
      echo "  ✗ $cap_name: default.toml must be a symlink (not a plain file)"
      ok=0
    else
      # Symlink target must exist
      local target
      target="$(readlink "$default_file")"
      if [[ ! -f "$dir/$target" ]]; then
        echo "  ✗ $cap_name: default.toml -> $target (target does not exist)"
        ok=0
      fi
    fi
  fi

  # octomind refuses to resolve a capability without config.toml on every
  # runtime path (auto-activation, enable, skill-declared), so only a manifest
  # that lists it statically could ever load it.
  if [[ ! -f "$dir/config.toml" ]]; then
    echo "  ✗ $cap_name: MISSING_CONFIG: config.toml with 'triggers = [...]' is required"
    ok=0
  fi

  # Lint config.toml (capability-level metadata) and provider TOMLs with
  # different rule sets. Skip default.toml when it's a symlink (linted
  # already as the real provider file via its target).
  for toml in "$dir"/*.toml; do
    [[ -L $toml ]] && continue # skip symlinks (default.toml)
    local basename
    basename="$(basename "$toml")"

    local file_kind="provider"
    if [[ $basename == "config.toml" ]]; then
      file_kind="config"
    fi

    local py_err
    if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-capabilities.py" "$toml" "$DEPS_ROOT" "$file_kind" 2>&1); then
      echo "  ✗ $cap_name/$basename: $py_err"
      ok=0
    fi
  done

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $cap_name"
  fi
  [[ $ok -eq 1 ]]
}

echo "Linting ${#DIRS[@]} capability(ies)..."
echo ""

for dir in "${DIRS[@]}"; do
  # Accept a bare name (video-gen) or a repo-relative path (capabilities/video-gen/).
  [[ $dir == /* ]] || dir="$CAP_ROOT/${dir#capabilities/}"
  dir="${dir%/}"

  if ! lint_capability "$dir"; then
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS capability(ies) failed linting."
  exit 1
else
  echo "✅ All capabilities passed."
fi
