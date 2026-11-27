#!/usr/bin/env bash
# Regression test for deps/muvon/doc-export.sh: the link must survive installers that start at once.
#
# Every session of an agent with the `documents` capability runs the installer, so several writers
# can race for ~/.local/bin/doc-export. `ln -sf` checks whether the link exists before it creates the
# new one, and BSD ln (macOS) does not retry when another writer creates the link in between: the
# loser exits 1 with "ln: .../doc-export: File exists" and the session fails to start. The test
# injects that interleaving through the ln stand-in in scripts/fixtures/ln-racy/, then runs the real
# tools concurrently, repeats the install, and checks the failure paths. It runs in a temporary HOME
# and never touches ~/.local/bin. Needs python3; POSIX symlinks (Linux, macOS).
#
# Usage: bash scripts/test-doc-export.sh        # WRITERS and ROUNDS override the defaults

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALLER="$REPO_ROOT/deps/muvon/doc-export.sh"
TARGET="$REPO_ROOT/skills/document-export/scripts/doc_export.py"
LN_STAND_IN="$REPO_ROOT/scripts/fixtures/ln-racy"
REAL_LN="$(command -v ln)"
WRITERS="${WRITERS:-12}"
ROUNDS="${ROUNDS:-5}"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

# PATH without ~/.local/bin, so the user's own link neither satisfies nor shadows anything.
TEST_PATH="$(printf '%s' "$PATH" | tr ':' '\n' | grep -vx "$HOME/.local/bin" | paste -sd: -)"
export LN_RACE_DIR="$TMP" LN_RACE_REAL="$REAL_LN"

# Start $2 installers in $1 with PATH $3, wait for them, and echo how many exited non-zero.
# With the ln stand-in on PATH, every installer parks at the existence check until all have
# arrived, so the race is deterministic instead of a matter of timing.
concurrent_installs() {
  local home="$1" writers="$2" search_path="$3" logs="$4" failed=0 i pid arrived=0 barrier=0
  local pids=()
  [[ :$search_path: == *":$LN_STAND_IN:"* ]] && barrier=1
  rm -f "$TMP/release" "$TMP"/arrived.*
  mkdir -p "$logs"
  for ((i = 0; i < writers; i++)); do
    HOME="$home" PATH="$search_path" bash "$INSTALLER" >"$logs/$i.log" 2>&1 &
    pids+=("$!")
  done
  if ((barrier)); then
    for ((i = 0; i < 300 && arrived < writers; i++)); do
      arrived=$(find "$TMP" -maxdepth 1 -name 'arrived.*' | wc -l)
      ((arrived < writers)) && sleep 0.1
    done
    if ((arrived < writers)); then
      # Barrier failed: release the parked stand-ins and wait until each has left the barrier
      # (they poll every 50 ms), then stop and reap the writers before the EXIT trap removes $TMP —
      # a stand-in still waiting on it would spin forever.
      touch "$TMP/release"
      for ((i = 0; i < 300 && $(find "$TMP" -maxdepth 1 -name 'arrived.*' | wc -l) > 0; i++)); do
        sleep 0.1
      done
      kill "${pids[@]}" 2>/dev/null || true
      for pid in "${pids[@]}"; do wait "$pid" 2>/dev/null || true; done
      fail "only $arrived of $writers installers reached ln"
    fi
    touch "$TMP/release"
  fi
  for pid in "${pids[@]}"; do
    wait "$pid" || failed=$((failed + 1))
  done
  echo "$failed"
}

assert_link() {
  local link="$1/.local/bin/doc-export"
  [[ -L $link ]] || fail "no link at $link"
  [[ $(readlink "$link") == "$TARGET" ]] || fail "$link -> $(readlink "$link"), expected $TARGET"
  HOME="$1" PATH="$1/.local/bin:$TEST_PATH" doc-export --help >/dev/null || fail "$link is not runnable"
}

first_error() {
  grep -h -m1 'File exists\|ERROR' "$1"/*.log | head -1
}

echo "== concurrent installers, macOS ln interleaving, fresh HOME ($WRITERS writers)"
HOME_DIR="$TMP/racy-fresh"
failed="$(concurrent_installs "$HOME_DIR" "$WRITERS" "$LN_STAND_IN:$TEST_PATH" "$TMP/logs-racy-fresh")"
((failed == 0)) || fail "$failed of $WRITERS installers failed: $(first_error "$TMP/logs-racy-fresh")"
assert_link "$HOME_DIR"

echo "== concurrent installers, macOS ln interleaving, stale link"
HOME_DIR="$TMP/racy-stale"
mkdir -p "$HOME_DIR/.local/bin"
ln -s "$TMP/old-tap/doc_export.py" "$HOME_DIR/.local/bin/doc-export"
failed="$(concurrent_installs "$HOME_DIR" "$WRITERS" "$LN_STAND_IN:$TEST_PATH" "$TMP/logs-racy-stale")"
((failed == 0)) || fail "$failed of $WRITERS installers failed: $(first_error "$TMP/logs-racy-stale")"
assert_link "$HOME_DIR"

echo "== concurrent installers, real ln ($WRITERS writers x $ROUNDS rounds, fresh and stale HOME)"
for ((round = 0; round < ROUNDS; round++)); do
  HOME_DIR="$TMP/real-$round"
  if ((round % 2)); then
    mkdir -p "$HOME_DIR/.local/bin"
    ln -s "$TMP/old-tap/doc_export.py" "$HOME_DIR/.local/bin/doc-export"
  fi
  failed="$(concurrent_installs "$HOME_DIR" "$WRITERS" "$TEST_PATH" "$TMP/logs-real-$round")"
  ((failed == 0)) || fail "round $round: $failed of $WRITERS installers failed: $(first_error "$TMP/logs-real-$round")"
  assert_link "$HOME_DIR"
done

echo "== repeat install takes the fast path"
HOME_DIR="$TMP/repeat"
HOME="$HOME_DIR" PATH="$TEST_PATH" bash "$INSTALLER" 2>/dev/null
output="$(HOME="$HOME_DIR" PATH="$HOME_DIR/.local/bin:$TEST_PATH" bash "$INSTALLER" 2>&1)"
[[ -z $output ]] || fail "repeat install did not exit through the fast path: $output"
assert_link "$HOME_DIR"

echo "== failures name the path and leave nothing behind"
HOME_DIR="$TMP/dir-at-link"
mkdir -p "$HOME_DIR/.local/bin/doc-export"
if HOME="$HOME_DIR" PATH="$TEST_PATH" bash "$INSTALLER" 2>"$TMP/dir.err"; then
  fail "installer accepted a directory at the link path"
fi
grep -qF "$HOME_DIR/.local/bin/doc-export" "$TMP/dir.err" || fail "directory at link path: $(cat "$TMP/dir.err")"
[[ -z $(ls -A "$HOME_DIR/.local/bin/doc-export") ]] || fail "installer wrote inside the directory at the link path"

HOME_DIR="$TMP/file-home"
mkdir -p "$HOME_DIR" && touch "$HOME_DIR/.local"
if HOME="$HOME_DIR" PATH="$TEST_PATH" bash "$INSTALLER" 2>"$TMP/file.err"; then
  fail "installer accepted a file at $HOME_DIR/.local"
fi
grep -qF "$HOME_DIR/.local/bin" "$TMP/file.err" || fail "file at .local: $(cat "$TMP/file.err")"

echo "PASS: doc-export link is correct after concurrent, stale-link and repeat installs"
