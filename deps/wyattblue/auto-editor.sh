#!/usr/bin/env bash
# dep: wyattblue/auto-editor
# type: dep
# description: auto-editor - cuts silence and dead air from video, exports trimmed media or NLE timelines
# check: auto-editor
# https://auto-editor.com

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Release binary pinned for non-Homebrew installs (PyPI stopped at 29.x).
VERSION="31.7.2"

# Fast path — already installed
if pkg_check auto-editor; then
  exit 0
fi

info "auto-editor not found — installing..."

install_release_binary() {
  local asset="$1" dest_dir="${HOME}/.local/bin" dest_name="${2:-auto-editor}"
  mkdir -p "$dest_dir"
  curl -fsSL --retry 3 \
    "https://github.com/WyattBlue/auto-editor/releases/download/${VERSION}/${asset}" \
    -o "${dest_dir}/${dest_name}"
  chmod +x "${dest_dir}/${dest_name}"
  export PATH="${dest_dir}:$PATH"
}

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install auto-editor
    elif [[ $IS_ARM64 == "1" ]]; then
      install_release_binary auto-editor-macos-arm64
    else
      install_release_binary auto-editor-macos-x86_64
    fi
    ;;

  linux)
    if [[ $IS_ARM64 == "1" ]]; then
      install_release_binary auto-editor-linux-aarch64
    elif [[ $IS_X86_64 == "1" ]]; then
      install_release_binary auto-editor-linux-x86_64
    else
      install_release_binary auto-editor-linux-armv7
    fi
    ;;

  windows)
    if [[ $IS_ARM64 == "1" ]]; then
      install_release_binary auto-editor-windows-aarch64.exe auto-editor.exe
    else
      install_release_binary auto-editor-windows-x86_64.exe auto-editor.exe
    fi
    ;;

  *)
    die "Unsupported OS. Install auto-editor manually: https://auto-editor.com/installing"
    ;;
esac

if ! pkg_check auto-editor; then
  die "auto-editor installed but not in PATH. Add ~/.local/bin to PATH."
fi

info "auto-editor installed successfully."
