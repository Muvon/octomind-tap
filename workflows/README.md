# Workflows

Public, multi-step workflows fetched by name with `octomind workflow <name>`.

Each takes a single stdin input and drives it to a **validated** result — most
chain a gate, an evaluator-optimizer loop, or an independent verifier so the
output is checked against a machine-readable verdict, not just generated.

Each file here is one workflow: `workflows/<name>.toml`. The file stem is the
invocable name — `plan-and-build.toml` → `octomind workflow plan-and-build`.

## Available workflows

Build / repo (operate on the current directory):

| Name | What it does | Showcases |
|------|--------------|-----------|
| [`develop`](./develop.toml) | Spec-driven feature dev: context → developer/evaluator loop with a build/test gate (exit on `VERDICT: APPROVED`) → summary | `loop` |
| [`debug`](./debug.toml) | Reproduce + pin root cause → fix/verify loop until a test proves it fixed → summary | `loop` |
| [`review`](./review.toml) | Review changes → independently verify each finding → branch on a deterministic verdict to an approval note or a fix list | `conditional` |
| [`document`](./document.toml) | Classify the diff (SemVer + change buckets) → README/changelog/release-notes drafts in parallel → reconcile/validate loop | `parallel` + `loop` |
| [`plan-and-build`](./plan-and-build.toml) | Minimal starter: draft a spec, then implement it and verify with the project's own check | sequential |

Build / market / write / research (driven by a single stdin goal):

| Name | What it does | Showcases |
|------|--------------|-----------|
| [`launch`](./launch.toml) | Idea → market explore → honest validate behind a pre-committed kill-gate → (greenlight?) brand + pitch + ads + bootstrap, else pivots | `conditional` |
| [`content`](./content.toml) | Brief → researched draft → audit/edit loop until it passes (`AUDIT-PASS`) → promo posts | `loop` |
| [`research`](./research.toml) | Background + evidence + counter-views in parallel → synthesize → groundedness judge loop (claims checked vs sources) → cited report | `parallel` + `loop` |
| [`localize`](./localize.toml) | Transcreate every language requested in the input (no hardcoded list), then loop fix/audit until every language passes native-fluency review (`ALL-PASS`), then deliver — writes to disk in-place if a path was given | `loop` |
| [`seo`](./seo.toml) | Audit a site/page across technical/on-page/off-page/GEO lenses, then a tiered, finding-traceable strategy brief | sequential |

## How resolution works

`octomind workflow <arg>` resolves like `octomind run <tag>`:

- `octomind workflow plan-and-build` — **bare name** → fetched from taps
  (`<tap>/workflows/plan-and-build.toml`), first tap wins (user taps first,
  built-in `muvon/tap` last).
- `octomind workflow ./my.toml` — **existing path / `*.toml`** → loaded as a
  local file, no role restriction.
- `octomind workflow` — **no argument** → lists every workflow available across
  your taps.

Workflows read their driving input from stdin and stream per-step progress to
stderr:

```sh
echo "Add a --json flag to the export command" | octomind workflow plan-and-build
octomind workflow plan-and-build --dry-run   # validate + print the plan, run nothing
```

## Public roles only

Workflows fetched from a tap are validated to use **public tap roles only** —
every step's `role` must be a `category:variant` tag installed via taps
(e.g. `developer:general`, `developer:spec`). This keeps a public workflow
portable: anyone with the same taps can run it. Local workflow files may use
local config roles freely.

## Structure

```toml
# Title: My Workflow                 # optional comment — human title for web/SEO rendering
name = "my-workflow"                 # required, matches the file stem
description = "What it does."        # shown in `octomind workflow` listing and on the website

[[steps]]                            # one or more steps, run top to bottom
name = "plan"                        # unique step name (also a {{var}} for later steps)
role = "developer:spec"              # public tap role (category:variant)
prompt = "Plan this: {{input}}"      # {{input}} = stdin; {{step-name}} = a prior step's output
# session = "fresh" | "continue"     # optional; reuse one session across iterations
# timeout = 0                        # optional, seconds (0 = none)
# retries = 0                        # optional
# model = "openrouter:..."           # optional per-step model override
# workdir = "./sub/project"          # optional working directory
```

### Step kinds

A step is **sequential** by default. Set exactly one flag to change its kind:

- `parallel = true` — run its `[[steps.run]]` sub-steps concurrently (≥2 required).
- `loop = true` — repeat `run` sub-steps until `exit_when` matches (`max_iterations`, default 10).
- `conditional = true` — run `on_match` / `on_no_match` sub-steps based on a `condition`.

### Variable substitution

- `{{input}}` — the stdin passed to the workflow.
- `{{<step-name>}}` — the assistant output of an earlier step.
- Standard placeholders (`{{DATE}}`, `{{CWD}}`, `{{GIT_STATUS}}`, …) and
  `<context>path</context>` blocks are expanded per step, same as a chat session.

See [`plan-and-build.toml`](./plan-and-build.toml) for a complete example.
