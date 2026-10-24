#!/usr/bin/env bash
# dep: muvon/doc-export
# type: dep
# description: doc-export - Markdown to Word and PDF with set fonts, sizes, and margins, plus PDF page, font, and text-layer checks
# check: doc-export
# https://github.com/muvon/octomind-tap

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# The CLI is the document-export skill's bundled script; linking it onto PATH makes
# it callable whether or not the skill is active in the session.
SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../skills/document-export/scripts" && pwd)/doc_export.py"
BIN_DIR="${HOME}/.local/bin"
LINK="${BIN_DIR}/doc-export"

# Fast path — already linked to this tap's script
if pkg_check doc-export && [[ "$(readlink "$LINK" 2>/dev/null)" == "$SCRIPT" ]]; then
  exit 0
fi

[[ -f $SCRIPT ]] || die "doc-export script not found: $SCRIPT"

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

if ! pkg_check doc-export; then
  die "doc-export linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "doc-export installed: $LINK -> $SCRIPT"
