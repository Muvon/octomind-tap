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
# Also the workflow page's search snippet on octomind.run.
if not isinstance(desc, str) or not 120 <= len(desc) <= 155:
    errors.append(f"DESCRIPTION_LENGTH: description must be 120–155 chars (got {len(str(desc))})")

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
        agent_file = repo_root / "agents" / domain / f"{spec}.toml"
        # A symlink is an alias for a renamed agent; workflows must name the real one.
        if not agent_file.is_file() or agent_file.is_symlink():
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
