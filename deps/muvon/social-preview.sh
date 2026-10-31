#!/usr/bin/env bash
# dep: muvon/social-preview
# type: dep
# description: social-preview - GitHub social preview card renderer CLI (1280x640 PNG in the repo's brand, via Typst)
# check: social-preview
# https://github.com/muvon/octomind-tap

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The renderer is the repo-social-preview skill's bundled script; linking it onto
# PATH makes it callable whether or not the skill is active in the session. The
# script finds its Typst template through the link, so the skill dir stays the source.
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../skills/repo-social-preview/scripts" && pwd)/social_preview.py"
BIN_DIR="${HOME}/.local/bin"
LINK="${BIN_DIR}/social-preview"

# Fast path — already linked to this tap's script
if pkg_check social-preview && [[ "$(readlink "$LINK" 2>/dev/null)" == "$SCRIPT" ]]; then
  exit 0
fi

[[ -f $SCRIPT ]] || die "Social preview script not found: $SCRIPT"

if ! pkg_check python3; then
  info "python3 not found — installing..."
  case "$OS" in
    macos)
      if pkg_check brew; then
        brew install python
      else
        die "brew not found. Install Homebrew first: https://brew.sh"
      fi
      ;;
    linux)
      pkg_install python3
      ;;
    *)
      die "Install Python 3.9+ manually: https://www.python.org/downloads/"
      ;;
  esac
fi

# The script ships executable; chmod only if a checkout lost the bit (read-only mounts fail on chmod).
[[ -x $SCRIPT ]] || chmod +x "$SCRIPT"
mkdir -p "$BIN_DIR"
ln -sf "$SCRIPT" "$LINK"
export PATH="${BIN_DIR}:$PATH"

if ! pkg_check social-preview; then
  die "social-preview linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "social-preview installed: $LINK -> $SCRIPT"
