#!/usr/bin/env bash
# dep: rust/cargo
# description: Installs Rust toolchain via rustup (provides cargo, rustc)
# check: cargo
# https://rustup.rs

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Always source cargo env first — ensures PATH is set for the calling script
# whether cargo was just installed or was already present.
# shellcheck source=/dev/null
[[ -f "$HOME/.cargo/env" ]] && source "$HOME/.cargo/env"

# Fast path — already installed
if pkg_check cargo; then
	exit 0
fi

info "Rust not found — installing via rustup..."

if pkg_check curl; then
	curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path
elif pkg_check wget; then
	wget -qO- https://sh.rustup.rs | sh -s -- -y --no-modify-path
else
	die "Neither curl nor wget found. Install one of them first, then re-run."
fi

# rustup installs to ~/.cargo/bin — source the env so cargo is reachable immediately
# shellcheck source=/dev/null
source "$HOME/.cargo/env"

if ! pkg_check cargo; then
	die "Rust installed but cargo not in PATH. Add ~/.cargo/bin to your PATH, then re-run."
fi
