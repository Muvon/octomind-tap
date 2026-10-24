#!/usr/bin/env bash
# dep: softcatala/whisper-ctranslate2
# type: dep
# description: whisper-ctranslate2 - local faster-whisper transcription CLI with word-level timestamps
# check: whisper-ctranslate2
# https://github.com/Softcatala/whisper-ctranslate2

set -euo pipefail

DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

VERSION="0.5.8"

# Fast path — already installed
if pkg_check whisper-ctranslate2; then
  exit 0
fi

info "whisper-ctranslate2 not found — installing ${VERSION} with uv..."

install_dep astral-sh/uv

# Python 3.12: CTranslate2 publishes wheels for it on macOS arm64/x86_64 and
# Linux x86_64/aarch64; uv downloads a managed interpreter when none is present.
uv tool install --python 3.12 "whisper-ctranslate2==${VERSION}"

export PATH="$HOME/.local/bin:$PATH"

if ! pkg_check whisper-ctranslate2; then
  die "whisper-ctranslate2 installed but not in PATH. Add ~/.local/bin to PATH."
fi

info "whisper-ctranslate2 installed successfully. Models download on first use."
