#!/usr/bin/env bash
# dep: muvon/doc-export
# type: dep
# description: doc-export - convert Markdown to Word and PDF; sets fonts, sizes and margins, plus PDF page, font and text-layer checks, needs python3 3.9+
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

# `ln` and `mv` would create the link inside a directory at the link path instead of replacing it.
if [[ -d $LINK ]]; then
  die "$LINK is a directory, not a link — remove it or rename it, then run again"
fi

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
mkdir_err="$(mkdir -p "$BIN_DIR" 2>&1)" || die "cannot create $BIN_DIR: $mkdir_err"

# Each session of an agent with the documents capability runs this installer, so several start at
# once. `ln -sf` checks for the old link before creating the new one; a writer that loses that race
# dies with "File exists" (BSD ln does not retry). Build the link under a name only this process
# uses, then rename it into place: rename(2) replaces the old link atomically.
TMP_LINK="$LINK.$$"
if ! link_err="$({ ln -sf "$SCRIPT" "$TMP_LINK" && mv -f "$TMP_LINK" "$LINK"; } 2>&1)"; then
  rm -f "$TMP_LINK"
  die "cannot link $LINK -> $SCRIPT: $link_err"
fi
export PATH="${BIN_DIR}:$PATH"

if ! pkg_check doc-export; then
  die "doc-export linked but not in PATH. Add ~/.local/bin to PATH."
fi

info "doc-export installed: $LINK -> $SCRIPT"
