#!/usr/bin/env bash
# dep: swiftlang/swift
# type: dep
# description: Ensures the Swift toolchain (swift, swiftc) is available — Xcode CLT on macOS, swiftly on Linux, winget on Windows
# check: swift
# https://www.swift.org

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Pick up a prior swiftly install (its bin is not on a fresh shell's PATH) so
# the fast path and idempotent re-runs short-circuit cleanly.
# shellcheck disable=SC1091
[ -f "$HOME/.local/share/swiftly/env.sh" ] && source "$HOME/.local/share/swiftly/env.sh"
[ -d "$HOME/.local/share/swiftly/bin" ] && export PATH="$HOME/.local/share/swiftly/bin:$PATH"

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
    if ! pkg_check curl; then
      die "curl is required to install the Swift toolchain on Linux. Install curl, then re-run."
    fi
    curl -fsSL "https://download.swift.org/swiftly/linux/swiftly-$(uname -m).tar.gz" -o /tmp/swiftly.tar.gz
    tar -xzf /tmp/swiftly.tar.gz -C /tmp
    /tmp/swiftly init --quiet-shell-followup --assume-yes --skip-install
    # shellcheck disable=SC1091
    [ -f "$HOME/.local/share/swiftly/env.sh" ] && source "$HOME/.local/share/swiftly/env.sh"
    # --no-verify skips GPG signature checks (gpg is often absent on minimal
    # images); the download stays HTTPS-authenticated, matching the TLS-only
    # trust model used by the rust/cargo dep. --assume-yes keeps re-runs
    # non-interactive. --post-install-file captures the system-dependency
    # install commands swiftly generates instead of erroring out.
    post_install="$(mktemp)"
    swiftly install latest --no-verify --assume-yes --post-install-file "$post_install"
    # The Swift Linux toolchain needs system libraries; swiftly writes the
    # commands to install them into the post-install file. Run them (needs
    # root/sudo — present in CI and expected for a system install).
    if [ -s "$post_install" ]; then
      info "Installing Swift's system dependencies..."
      bash "$post_install" || warn "Swift system-dependency step failed — swift may need those libraries installed manually."
    fi
    rm -f "$post_install"
    swiftly use latest || true
    ;;
  windows)
    # Official Swift toolchain via Windows Package Manager (winget).
    if ! pkg_check winget; then
      die "winget not found. Install the Swift toolchain manually: https://www.swift.org/install/windows/"
    fi
    # Idempotent: winget's exit code is unreliable (it returns non-zero when the
    # package is already installed and an upgrade is "available"), so match on
    # the list output text instead of trusting the exit code.
    if winget list --id Swift.Toolchain -e 2>/dev/null | grep -qi "Swift.Toolchain"; then
      info "Swift toolchain already installed (winget)."
      exit 0
    fi
    # Exit code 0 means a successful fresh install. winget does a machine-level
    # install; swift lands on the machine PATH that a fresh shell picks up, so
    # exit 0 here rather than fall through to the same-session PATH check below.
    # Don't re-verify via 'winget list': its installed-package correlation is
    # heuristic and can miss a just-installed toolchain.
    if winget install --id Swift.Toolchain -e --source winget \
      --accept-package-agreements --accept-source-agreements; then
      info "Swift toolchain installed via winget. Open a new shell for swift to be on PATH."
      exit 0
    fi
    # Non-zero exit is unreliable (winget returns non-zero when the package is
    # already installed and an upgrade is "available") — re-check by list output.
    if winget list --id Swift.Toolchain -e 2>/dev/null | grep -qi "Swift.Toolchain"; then
      info "Swift toolchain installed via winget. Open a new shell for swift to be on PATH."
      exit 0
    fi
    die "winget could not install the Swift toolchain. Install manually: https://www.swift.org/install/windows/"
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
