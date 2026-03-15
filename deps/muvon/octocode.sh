#!/usr/bin/env bash
# dep: muvon/octocode
# description: Installs the octocode CLI (code indexing and search tool by Muvon)
# check: octocode
# https://github.com/muvon/octocode

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check octocode; then
	exit 0
fi

# Ensure cargo is available
install_dep rust/cargo

info "octocode not found — installing..."

case "$OS" in
	macos)
		# Ensure Xcode command line tools are available (required for cargo install)
		# GitHub Actions macOS runners have Xcode but may need developer directory set
		if ! pkg_check cc && command -v xcode-select &>/dev/null; then
			info "Setting up Xcode developer tools..."
			# Try to accept license and set developer directory
			sudo xcodebuild -license accept 2>/dev/null || true
			sudo xcode-select -s /Applications/Xcode.app 2>/dev/null || true
			# If still no cc, install command line tools
			if ! pkg_check cc; then
				xcode-select --install 2>/dev/null || true
				# Wait for installation (can take a while)
				for i in {1..60}; do
					if pkg_check cc; then break; fi
					sleep 5
				done
			fi
		fi
		if pkg_check brew; then
			brew install muvon/tap/octocode
		else
			cargo install octocode
		fi
		;;
	linux)
		cargo install octocode
		;;
esac
