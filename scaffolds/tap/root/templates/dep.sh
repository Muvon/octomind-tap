#!/usr/bin/env bash
# dep: <org>/<tool>
# type: mcp|dep
# description: <What this installs>
# check: <command>
# https://example.com/tool

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check "<command>"; then
  exit 0
fi

info "Installing <tool>..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install "<package>"
    else
      die "Homebrew is required. Install it from https://brew.sh and retry."
    fi
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt) apt_install "<package>" ;;
      dnf) dnf_install "<package>" ;;
      pacman) as_root pacman -S --noconfirm "<package>" ;;
      zypper) as_root zypper install -y "<package>" ;;
      apk) as_root apk add "<package>" ;;
      *)
        # Replace with the tool's official universal installer when available.
        die "No supported package manager found. Install <tool> manually."
        ;;
    esac
    ;;
esac

if ! pkg_check "<command>"; then
  [[ -d "$HOME/.local/bin" ]] && export PATH="$HOME/.local/bin:$PATH"
  [[ -d "$HOME/.cargo/bin" ]] && export PATH="$HOME/.cargo/bin:$PATH"
fi

pkg_check "<command>" || die "<tool> was installed but <command> is not in PATH."
info "<tool> installed successfully."

