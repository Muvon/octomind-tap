#!/usr/bin/env bash
# Lint all workflows in workflows/*.toml
# Checks:
#   1. Valid TOML; `name` matches the file stem; description 20–400 chars
#   2. Comment metadata: # Title: (5–60 chars)
#   3. Step names unique across steps and sub-steps; none named `input`
#   4. Every sequential step / sub-step has a prompt and a public role tag
#      (category:variant) that resolves to agents/<domain>/<spec>.toml
#   5. Every {{var}} is `input`, a step name, or an uppercase placeholder
#   6. exit_when / condition / edge `when` set exactly one of contains|matches,
#      and every `matches` regex compiles
#   7. Loops set exit_when and a max_iterations of 1–3
#   8. Graph mode (entry / [[edges]]) sets max_transitions
#   9. max_cost, when set, is a positive number
#  10. Listed in workflows/README.md; the root README workflow count is current
#  11. `octomind workflow <file> --dry-run` passes (skipped when octomind is not installed)
#
# Usage:
#   scripts/lint-workflows.sh                         # lint all workflows
#   scripts/lint-workflows.sh workflows/review.toml   # lint specific files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  mapfile -t FILES < <(find "$REPO_ROOT/workflows" -maxdepth 1 -name "*.toml" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No workflow files found."
  exit 0
fi

PYTHON_WORKFLOW_CHECK=$(
  cat <<'PYEOF'
import sys, pathlib, re

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

path = pathlib.Path(sys.argv[1])
repo_root = pathlib.Path(sys.argv[2])
max_loop_iterations = 3

raw = path.read_text()
try:
    data = tomllib.loads(raw)
except Exception as e:
    print(f"INVALID_TOML: {e}", file=sys.stderr)
    sys.exit(1)

errors = []

name = data.get("name")
if name != path.stem:
    errors.append(f"NAME_MISMATCH: name = {name!r} must equal the file stem {path.stem!r}")

desc = data.get("description", "")
if not isinstance(desc, str) or not 20 <= len(desc) <= 400:
    errors.append(f"DESCRIPTION_LENGTH: description must be 20–400 chars (got {len(str(desc))})")

m = re.search(r"^# Title:\s*(.+?)\s*$", raw, re.MULTILINE)
if not m:
    errors.append("MISSING_TITLE: add a '# Title: ...' header comment")
elif not 5 <= len(m.group(1)) <= 60:
    errors.append(f"TITLE_LENGTH: # Title: must be 5–60 chars (got {len(m.group(1))})")

max_cost = data.get("max_cost")
if max_cost is not None and not (isinstance(max_cost, (int, float)) and not isinstance(max_cost, bool) and max_cost > 0):
    errors.append(f"MAX_COST: max_cost must be a positive number (got {max_cost!r})")

steps = data.get("steps") or []
if not steps:
    errors.append("NO_STEPS: at least one [[steps]] entry is required")

# (kind, step) for every runnable node, plus the block steps themselves
leaves = []
all_names = []
blocks = []
node_of = {}  # step or sub-step name -> top-level graph node name


def collect(step):
    kinds = [k for k in ("parallel", "loop", "conditional") if step.get(k) is True]
    if len(kinds) > 1:
        errors.append(f"MIXED_KIND: step {step.get('name')!r} sets more than one of parallel/loop/conditional")
    all_names.append(step.get("name"))
    node_of[step.get("name")] = step.get("name")
    if kinds:
        blocks.append((kinds[0], step))
        for sub in step.get("run") or []:
            leaves.append(sub)
            all_names.append(sub.get("name"))
            node_of[sub.get("name")] = step.get("name")
    else:
        leaves.append(step)


for s in steps:
    collect(s)

seen = set()
for n in all_names:
    if not n:
        errors.append("EMPTY_STEP_NAME: every step and sub-step needs a name")
    elif n == "input":
        errors.append("RESERVED_NAME: no step may be named 'input'")
    elif n in seen:
        errors.append(f"DUPLICATE_STEP: {n!r} is used more than once")
    seen.add(n)

role_re = re.compile(r"^[a-z0-9-]+:[a-z0-9-]+$")
for s in leaves:
    sname = s.get("name")
    if not s.get("prompt"):
        errors.append(f"MISSING_PROMPT: step {sname!r}")
    # A dynamic-fanout template or sequential step must carry a role
    role = s.get("role")
    if not role:
        errors.append(f"MISSING_ROLE: step {sname!r}")
    elif not role_re.match(role):
        errors.append(f"ROLE_FORMAT: step {sname!r} role {role!r} must be a public category:variant tag")
    else:
        domain, spec = role.split(":")
        if not (repo_root / "agents" / domain / f"{spec}.toml").exists():
            errors.append(f"ROLE_NOT_FOUND: step {sname!r} role {role!r} has no agents/{domain}/{spec}.toml")

placeholder_re = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_-]*)(?::[^}]*)?\s*\}\}")
for s in leaves:
    for var in placeholder_re.findall(s.get("prompt", "")):
        if var != "input" and var not in seen and not var.isupper():
            errors.append(f"UNKNOWN_VAR: step {s.get('name')!r} references {{{{{var}}}}}")


def check_condition(label, cond, step_names):
    if not isinstance(cond, dict):
        errors.append(f"CONDITION_MISSING: {label}")
        return
    has_c, has_m = "contains" in cond, "matches" in cond
    if has_c == has_m:
        errors.append(f"CONDITION_SHAPE: {label} must set exactly one of contains|matches")
    if has_m:
        try:
            re.compile(cond["matches"])
        except re.error as e:
            errors.append(f"REGEX: {label} does not compile: {e}")
    out = cond.get("output")
    if out is not None and out not in step_names:
        errors.append(f"CONDITION_OUTPUT: {label} references unknown step {out!r}")


for kind, b in blocks:
    bname = b.get("name")
    if kind == "parallel" and len(b.get("run") or []) < 2 and not b.get("source"):
        errors.append(f"PARALLEL_SIZE: {bname!r} needs at least 2 sub-steps")
    if kind == "loop":
        check_condition(f"{bname!r} exit_when", b.get("exit_when"), seen)
        mi = b.get("max_iterations")
        if not isinstance(mi, int) or not 1 <= mi <= max_loop_iterations:
            errors.append(f"MAX_ITERATIONS: loop {bname!r} must set max_iterations 1–{max_loop_iterations} (got {mi!r})")
    if kind == "conditional":
        check_condition(f"{bname!r} condition", b.get("condition"), seen)
        subs = {x.get("name") for x in b.get("run") or []}
        for branch in ("on_match", "on_no_match"):
            for ref in b.get(branch) or []:
                if ref not in subs:
                    errors.append(f"BRANCH_REF: {bname!r} {branch} names unknown sub-step {ref!r}")

edges = data.get("edges") or []
if data.get("entry") or edges:
    if not isinstance(data.get("max_transitions"), int) or data["max_transitions"] < 1:
        errors.append("MAX_TRANSITIONS: graph mode requires max_transitions >= 1")
    for i, e in enumerate(edges):
        if "when" in e:
            check_condition(f"edge {i} ({e.get('from')} -> {e.get('to')}) when", e["when"], seen)

    # octomind bails at runtime when a prompt reads an output whose producer did
    # not run on the chosen route, and pre-flight does not catch it. A producer is
    # safe only if it lies on every path from entry to the consumer (dominates it).
    nodes = {s.get("name") for s in steps}
    preds = {n: set() for n in nodes}
    for e in edges:
        if e.get("to") in nodes and e.get("from") in nodes:
            preds[e["to"]].add(e["from"])
    entry = data.get("entry")
    if entry in nodes:
        dom = {n: set(nodes) for n in nodes}
        dom[entry] = {entry}
        changed = True
        while changed:
            changed = False
            for n in nodes - {entry}:
                new = {n} | (set.intersection(*(dom[p] for p in preds[n])) if preds[n] else set())
                if new != dom[n]:
                    dom[n], changed = new, True
        for s in leaves:
            consumer = node_of[s.get("name")]
            for var in set(placeholder_re.findall(s.get("prompt", ""))):
                producer = node_of.get(var)
                if producer and producer not in dom.get(consumer, set()):
                    errors.append(
                        f"ROUTE_VAR: step {s.get('name')!r} reads {{{{{var}}}}} but {producer!r} "
                        f"does not run on every route to {consumer!r} (runtime failure in graph mode)"
                    )

if errors:
    print("\n".join(f"  ✗ {e}" for e in errors), file=sys.stderr)
    sys.exit(1)
PYEOF
)

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  local py_err
  if ! py_err=$(python3 -c "$PYTHON_WORKFLOW_CHECK" "$file" "$REPO_ROOT" 2>&1); then
    echo "$py_err"
    ok=0
  fi

  local stem
  stem="$(basename "$file" .toml)"
  if ! grep -qF "](./$stem.toml)" "$REPO_ROOT/workflows/README.md"; then
    echo "  ✗ NOT_LISTED: add $stem to the table in workflows/README.md"
    ok=0
  fi

  if command -v octomind >/dev/null 2>&1; then
    local dry_err
    if ! dry_err=$(octomind workflow "$file" --dry-run 2>&1 >/dev/null); then
      echo "  ✗ DRY_RUN: ${dry_err##*$'\n'}"
      ok=0
    fi
  fi

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $rel"
  else
    echo "    file: $rel"
    return 1
  fi
}

echo "Linting ${#FILES[@]} workflow(s)..."
echo ""

for file in "${FILES[@]}"; do
  [[ $file == /* ]] || file="$REPO_ROOT/$file"

  if ! lint_file "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

# Repo-wide: the root README count must match what ships
if [[ $# -eq 0 ]]; then
  actual=${#FILES[@]}
  claimed=$(grep -oE '[0-9]+ ready-made workflows' "$REPO_ROOT/README.md" | grep -oE '^[0-9]+' || true)
  table=$(grep -E '^\| `workflows/<name>\.toml`' "$REPO_ROOT/README.md" | grep -oE '[0-9]+ \|$' | grep -oE '^[0-9]+' || true)
  for n in $claimed $table; do
    if [[ $n -ne $actual ]]; then
      echo "  ✗ README.md claims $n workflows but workflows/ has $actual"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS workflow check(s) failed."
  exit 1
else
  echo "✅ All workflows passed."
fi
