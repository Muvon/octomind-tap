#!/usr/bin/env bash
# Manage exact version pins for registry-launched MCP servers.
#
# Every [[mcp.servers]] entry launched via npx (npm) or uvx (PyPI) must pin
# an exact package version so a registry publish can never change what users
# run. lint-capabilities.sh enforces pin presence offline; this script does
# the network side:
#
#   scripts/mcp-versions.sh check [--strict]
#       Compare every pinned version against the registry's latest and print
#       a drift report. Always exits 0 unless --strict is given, in which
#       case any outdated/unpinned/error row exits 1 (for scheduled CI).
#
#   scripts/mcp-versions.sh update [--all | <capability> ...]
#       Rewrite pins to the current registry latest (also pins anything
#       unpinned or tagged @latest). Leaves changes uncommitted for review.
#       Run `test` afterwards to smoke-test the updated servers.
#
#   scripts/mcp-versions.sh test [<capability> ...]
#       Spawn each stdio server, perform the MCP initialize handshake and
#       tools/list, and report per server. Tools advertised by the server
#       are matched against the file's roles.mcp allowed_tools globs to
#       catch upstream tool-set changes. Servers needing credentials may
#       fail with a missing-key error — that shows in the report; judge by
#       whether the process starts and speaks MCP at all.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export OCTOTAP_ROOT="$REPO_ROOT"

exec python3 - "$@" <<'PYEOF'
import concurrent.futures
import fnmatch
import json
import os
import pathlib
import re
import shlex
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

ROOT = pathlib.Path(os.environ["OCTOTAP_ROOT"])
CAP_ROOT = ROOT / "capabilities"

# Flags whose next token is a value, not the package (uvx/npx).
FLAG_WITH_VALUE = {"--with", "--from", "--python", "-p", "--package", "--node-options", "-c", "--constraints"}


def first_package(tokens):
    skip = False
    for t in tokens:
        if skip:
            skip = False
            continue
        if t in FLAG_WITH_VALUE:
            skip = True
            continue
        if t.startswith("-") or "{{" in t or t.startswith("$") or t == "exec":
            continue
        return t
    return None


def embedded_launches(shell_str):
    """Find `npx …`/`uvx …` invocations inside an sh -c string."""
    try:
        toks = shlex.split(shell_str)
    except ValueError:
        toks = shell_str.split()
    out = []
    for i, t in enumerate(toks):
        if t in ("npx", "uvx"):
            pkg = first_package(toks[i + 1:])
            if pkg:
                out.append((t, pkg))
    return out


def parse_spec(token, runner):
    """Return (name, version_or_None) for a package spec token."""
    if runner == "npx":
        if token.startswith("@"):
            m = re.match(r"^(@[^/]+/[^@]+?)(?:@(.+))?$", token)
        else:
            m = re.match(r"^([^@]+?)(?:@(.+))?$", token)
        return (m.group(1), m.group(2)) if m else (token, None)
    if "==" in token:
        name, ver = token.split("==", 1)
        return name, ver
    return token, None


def is_exact(version, runner):
    if not version or not version[0].isdigit():
        return False
    if runner == "npx":
        return re.fullmatch(r"\d+\.\d+\.\d+([-+][0-9A-Za-z.-]+)?", version) is not None
    return not any(c in version for c in "*<>=!,")


def make_spec(name, version, runner):
    return f"{name}@{version}" if runner == "npx" else f"{name}=={version}"


def iter_servers():
    """Yield (path, data, server, runner, token, embedded) for registry-launched stdio servers."""
    for path in sorted(CAP_ROOT.rglob("*.toml")):
        if path.is_symlink():
            continue
        try:
            data = tomllib.loads(path.read_text())
        except Exception as e:
            print(f"WARN: skipping unparseable {path}: {e}", file=sys.stderr)
            continue
        for srv in (data.get("mcp") or {}).get("servers") or []:
            if srv.get("type") != "stdio":
                continue
            cmd = srv.get("command", "")
            args = srv.get("args") or []
            if cmd in ("npx", "uvx"):
                tok = first_package(args)
                if tok:
                    yield path, data, srv, cmd, tok, False
            elif cmd in ("sh", "bash"):
                for a in args:
                    if isinstance(a, str):
                        for runner, tok in embedded_launches(a):
                            yield path, data, srv, runner, tok, True


def filter_paths(entries, selectors):
    if not selectors:
        return entries
    keep = []
    for sel in selectors:
        p = pathlib.Path(sel)
        if not p.is_absolute():
            p = CAP_ROOT / sel if not sel.startswith("capabilities/") else ROOT / sel
        keep.append(p.resolve())
    out = []
    for entry in entries:
        rp = entry[0].resolve()
        if any(str(rp).startswith(str(k) + "/") or rp == k or rp.parent == k for k in keep):
            out.append(entry)
    return out


def registry_latest(runner, name):
    if runner == "npx":
        url = "https://registry.npmjs.org/" + urllib.parse.quote(name, safe="")
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.npm.install-v1+json"})
        with urllib.request.urlopen(req, timeout=20) as r:
            tags = json.load(r).get("dist-tags") or {}
        if "latest" not in tags:
            raise RuntimeError("no published versions (unpublished from npm?)")
        return tags["latest"]
    with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=20) as r:
        return json.load(r)["info"]["version"]


def resolve_latest(pkgs):
    """pkgs: set of (runner, name) -> dict[(runner, name)] = version or Exception."""
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(registry_latest, r, n): (r, n) for r, n in pkgs}
        for fut in concurrent.futures.as_completed(futs):
            key = futs[fut]
            try:
                results[key] = fut.result()
            except Exception as e:
                if isinstance(e, urllib.error.HTTPError):
                    e.close()
                results[key] = e
    return results


def collect(selectors=None):
    entries = filter_paths(list(iter_servers()), selectors)
    rows = []
    for path, data, srv, runner, token, embedded in entries:
        name, ver = parse_spec(token, runner)
        rows.append({
            "path": path, "data": data, "srv": srv, "runner": runner,
            "token": token, "embedded": embedded, "name": name, "version": ver,
        })
    return rows


def rel(path):
    return str(path.relative_to(ROOT))


# ---------------------------------------------------------------- check

def cmd_check(argv):
    strict = "--strict" in argv
    rows = collect([a for a in argv if not a.startswith("--")])
    latest = resolve_latest({(r["runner"], r["name"]) for r in rows})

    seen = set()
    counts = {"ok": 0, "outdated": 0, "unpinned": 0, "error": 0}
    width = max((len(r["name"]) for r in rows), default=20) + 2
    print(f"{'package':<{width}} {'type':<5} {'pinned':<14} {'latest':<14} status")
    for r in sorted(rows, key=lambda r: r["name"]):
        key = (r["runner"], r["name"], r["version"])
        if key in seen:
            continue
        seen.add(key)
        kind = "npm" if r["runner"] == "npx" else "pypi"
        got = latest[(r["runner"], r["name"])]
        if isinstance(got, Exception):
            status, latest_s = "error: " + str(got), "?"
        elif not is_exact(r["version"], r["runner"]):
            status, latest_s = "unpinned", got
        elif r["version"] == got:
            status, latest_s = "ok", got
        else:
            status, latest_s = "outdated", got
        counts[status.split(":")[0]] += 1
        print(f"{r['name']:<{width}} {kind:<5} {r['version'] or '-':<14} {latest_s:<14} {status}")

    print(f"\n{counts['ok']} ok, {counts['outdated']} outdated, "
          f"{counts['unpinned']} unpinned, {counts['error']} lookup errors")
    if counts["outdated"] or counts["unpinned"]:
        print("Run: scripts/mcp-versions.sh update --all   (then: scripts/mcp-versions.sh test)")
    if strict and (counts["outdated"] or counts["unpinned"] or counts["error"]):
        sys.exit(1)


# ---------------------------------------------------------------- update

def rewrite_file(path, changes):
    """changes: list of (runner, name, old_token, new_spec, embedded). Line-scoped
    to `args = [...]` lines so package names in comments are never touched."""
    lines = path.read_text().splitlines(keepends=True)
    applied = 0
    for i, line in enumerate(lines):
        if not re.match(r"\s*args\s*=", line):
            continue
        new_line = line
        for runner, name, old_token, new_spec, embedded in changes:
            if embedded:
                pat = rf"(?<![\w.-]){re.escape(name)}(==[^\s\"'\\]+)?(?![\w.-])"
                new_line = re.sub(pat, new_spec, new_line)
            else:
                new_line = new_line.replace(f'"{old_token}"', f'"{new_spec}"')
        if new_line != line:
            lines[i] = new_line
            applied += 1
    if applied:
        path.write_text("".join(lines))
    return applied


def cmd_update(argv):
    selectors = [a for a in argv if not a.startswith("--")]
    if "--all" not in argv and not selectors:
        print("usage: scripts/mcp-versions.sh update [--all | <capability> ...]", file=sys.stderr)
        sys.exit(2)
    rows = collect(selectors)
    latest = resolve_latest({(r["runner"], r["name"]) for r in rows})

    by_file = {}
    errors = 0
    for r in rows:
        got = latest[(r["runner"], r["name"])]
        if isinstance(got, Exception):
            print(f"  ✗ {r['name']}: registry lookup failed: {got}", file=sys.stderr)
            errors += 1
            continue
        if r["version"] == got:
            continue
        new_spec = make_spec(r["name"], got, r["runner"])
        by_file.setdefault(r["path"], []).append(
            (r["runner"], r["name"], r["token"], new_spec, r["embedded"]))
        print(f"  {rel(r['path'])}: {r['token']} -> {new_spec}")

    for path, changes in by_file.items():
        if not rewrite_file(path, changes):
            print(f"  ✗ {rel(path)}: no args line matched — pin NOT applied", file=sys.stderr)
            errors += 1

    # Re-scan and verify every touched package now parses as exactly pinned.
    for r in collect(selectors):
        got = latest.get((r["runner"], r["name"]))
        if isinstance(got, str) and not is_exact(r["version"], r["runner"]):
            print(f"  ✗ {rel(r['path'])}: {r['name']} still unpinned after rewrite", file=sys.stderr)
            errors += 1

    changed = sum(len(c) for c in by_file.values())
    print(f"\n{changed} pin(s) updated across {len(by_file)} file(s), {errors} error(s).")
    if changed:
        print("Review with git diff, then smoke-test: scripts/mcp-versions.sh test")
    sys.exit(1 if errors else 0)


# ---------------------------------------------------------------- test

ENV_PLACEHOLDER = re.compile(r"\{\{ENV:([A-Za-z0-9_]+)\}\}")


def substitute_env(value):
    return ENV_PLACEHOLDER.sub(lambda m: os.environ.get(m.group(1), ""), value)


def handshake(command, args, extra_env, timeout):
    env = dict(os.environ)
    for k, v in (extra_env or {}).items():
        env[k] = substitute_env(str(v))
    proc = subprocess.Popen(
        [command, *args], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, env=env, cwd=ROOT)
    out_lines, err_parts = [], []
    threading.Thread(target=lambda: [out_lines.append(l) for l in proc.stdout], daemon=True).start()
    threading.Thread(target=lambda: err_parts.append(proc.stderr.read()), daemon=True).start()

    def send(obj):
        try:
            proc.stdin.write((json.dumps(obj) + "\n").encode())
            proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass

    def stderr_tail():
        text = b"".join(err_parts).decode(errors="replace")
        tail = [l for l in text.strip().splitlines() if l.strip()][-3:]
        return " | ".join(tail)[:300]

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2024-11-05", "capabilities": {},
        "clientInfo": {"name": "octomind-tap-smoke", "version": "0"}}})
    deadline = time.time() + timeout
    initialized = False
    try:
        while time.time() < deadline:
            while out_lines:
                try:
                    msg = json.loads(out_lines.pop(0))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
                if msg.get("id") == 1 and not initialized:
                    if "error" in msg:
                        return "FAIL", f"initialize error: {msg['error']}"
                    initialized = True
                    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
                    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
                elif msg.get("id") == 2:
                    if "error" in msg:
                        return "FAIL", f"tools/list error: {msg['error']}"
                    return "OK", [t["name"] for t in msg["result"].get("tools", [])]
            if proc.poll() is not None:
                time.sleep(0.3)  # let reader threads drain the pipes
                return "FAIL", f"exited rc={proc.returncode}: {stderr_tail()}"
            time.sleep(0.2)
        return "FAIL", f"timeout after {timeout}s ({'initialized, no tools/list' if initialized else 'no initialize response'}): {stderr_tail()}"
    finally:
        proc.kill()


def cmd_test(argv):
    rows = collect([a for a in argv if not a.startswith("--")])
    # One test per unique server declaration (default.toml symlinks already skipped).
    jobs = []
    seen = set()
    for r in rows:
        key = (r["path"], r["srv"].get("name"))
        if key in seen:
            continue
        seen.add(key)
        jobs.append(r)

    def run(r):
        srv = r["srv"]
        args = [substitute_env(str(a)) for a in srv.get("args") or []]
        timeout = srv.get("timeout_seconds", 60) + 30  # headroom for cold npx/uvx download
        status, detail = handshake(srv["command"], args, srv.get("env"), timeout)
        note = ""
        if status == "OK":
            tools = detail
            globs = (r["data"].get("roles", {}).get("mcp", {}) or {}).get("allowed_tools", [])
            # allowed_tools may use raw tool names (git_*) or the runtime's
            # server-namespaced form (playwright:*) — accept either.
            sname = srv.get("name", "")
            candidates = tools + [f"{sname}:{t}" for t in tools]
            unmatched = [g for g in globs if not any(fnmatch.fnmatch(t, g) for t in candidates)]
            note = f"{len(tools)} tools"
            if unmatched:
                status = "WARN"
                note += f"; allowed_tools with no match: {', '.join(unmatched)}"
        else:
            note = detail
        return r, status, note

    counts = {"OK": 0, "WARN": 0, "FAIL": 0}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for r, status, note in pool.map(run, jobs):
            counts[status] += 1
            mark = {"OK": "✓", "WARN": "⚠", "FAIL": "✗"}[status]
            print(f"  {mark} {rel(r['path'])} [{r['srv'].get('name')}] {r['token']}: {status} — {note}", flush=True)

    print(f"\n{counts['OK']} ok, {counts['WARN']} warnings, {counts['FAIL']} failed "
          f"(failures may be missing credentials — check the message, not just the status)")
    sys.exit(1 if counts["FAIL"] else 0)


# ---------------------------------------------------------------- main

USAGE = """usage: scripts/mcp-versions.sh <command> [args]
  check  [--strict]                 drift report: pinned vs registry latest
  update [--all | <capability> ...] rewrite pins to registry latest
  test   [<capability> ...]         smoke-test servers (initialize + tools/list)"""

args = sys.argv[1:]
if not args or args[0] in ("-h", "--help", "help"):
    print(USAGE)
    sys.exit(0 if args else 2)
cmd, rest = args[0], args[1:]
if cmd == "check":
    cmd_check(rest)
elif cmd == "update":
    cmd_update(rest)
elif cmd == "test":
    cmd_test(rest)
else:
    print(USAGE, file=sys.stderr)
    sys.exit(2)
PYEOF
