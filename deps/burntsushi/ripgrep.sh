#!/usr/bin/env bash
# dep: burntsushi/ripgrep
# type: dep
# description: ripgrep (rg) - fast recursive search tool
# check: rg
# https://github.com/BurntSushi/ripgrep

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check rg; then
  exit 0
fi

info "ripgrep not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install ripgrep
    else
      cargo install ripgrep
    fi
    ;;
  linux)
    pkg_install ripgrep
    ;;
  windows)
    # Download pre-built binary from GitHub.
    # Resolve the version via the releases/latest redirect instead of the REST API:
    # the unauthenticated API is rate-limited per IP and returns 403 on shared CI runners.
    VERSION=$(curl -fsSL -o /dev/null -w '%{url_effective}' "https://github.com/BurntSushi/ripgrep/releases/latest")
    VERSION="${VERSION##*/}"
    [[ -n "$VERSION" ]] || die "Failed to resolve latest ripgrep version"
    TMP_DIR=$(mktemp -d)
    trap "rm -rf '$TMP_DIR'" EXIT
    FILENAME="ripgrep-${VERSION}-x86_64-pc-windows-msvc.zip"
    curl -fsSL --retry 3 "https://github.com/BurntSushi/ripgrep/releases/download/${VERSION}/${FILENAME}" -o "$TMP_DIR/$FILENAME"
    unzip -qo "$TMP_DIR/$FILENAME" -d "$TMP_DIR"
    mkdir -p "${HOME}/.local/bin"
    cp "$TMP_DIR/ripgrep-${VERSION}-x86_64-pc-windows-msvc/rg.exe" "${HOME}/.local/bin/rg.exe"
    export PATH="${HOME}/.local/bin:$PATH"
    ;;
esac

if ! pkg_check rg; then
  die "ripgrep installed but 'rg' not in PATH. You may need to restart your shell."
fi

info "ripgrep installed successfully."
