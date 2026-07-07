#!/usr/bin/env bash
# dep: swiftlang/swift
# type: dep
# description: Ensures the Swift toolchain (swift, swiftc) is available — Xcode CLT on macOS, swiftly on Linux
# check: swift
# https://www.swift.org

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check swift; then
  exit 0
fi

info "swift not found — installing..."

case "$OS" in
  macos)
    # Swift ships with the Xcode Command Line Tools. xcode-select opens the
    # Apple GUI installer; we trigger it and tell the user to complete it.
    if xcode-select --install >/dev/null 2>&1; then
      die "Xcode Command Line Tools installer launched. Complete it, then re-run — swift comes with the CLT."
    else
      die "Xcode CLT appears present but swift is missing. Run 'xcode-select --install' or install Xcode from the App Store, then re-run."
    fi
    ;;
  linux)
    # swiftly is the official swift.org toolchain installer for Linux
    if pkg_check curl; then
      curl -fsSL https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz -o /tmp/swiftly.tar.gz
      tar -xzf /tmp/swiftly.tar.gz -C /tmp
      /tmp/swiftly init --quiet-shell-followup --assume-yes --skip-install
      # shellcheck disable=SC1091
      [ -f "$HOME/.local/share/swiftly/env.sh" ] && source "$HOME/.local/share/swiftly/env.sh"
      swiftly install latest
    else
      die "curl is required to install the Swift toolchain on Linux. Install curl, then re-run."
    fi
    ;;
esac

# Verify the toolchain is reachable
if ! pkg_check swift; then
  if [[ -d "$HOME/.local/share/swiftly/bin" ]]; then
    export PATH="$HOME/.local/share/swiftly/bin:$PATH"
  fi
  if ! pkg_check swift; then
    info "swift still not in PATH. You may need to restart your shell."
    exit 1
  fi
fi
