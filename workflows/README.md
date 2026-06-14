# Workflows

Public, multi-step workflows fetched by name with `octomind workflow <name>`.

Each file here is one workflow: `workflows/<name>.toml`. The file stem is the
invocable name — `plan-and-build.toml` → `octomind workflow plan-and-build`.

## Available workflows

Build / repo (operate on the current directory):

| Name | What it does | Showcases |
|------|--------------|-----------|
| [`develop`](./develop.toml) | Spec-driven feature dev: context → developer/evaluator loop (exit on `ALL GOOD`) → summary | `loop` |
| [`debug`](./debug.toml) | Locate root cause → fix/verify loop until confirmed → summary | `loop` |
| [`review`](./review.toml) | Review the current changes, then branch to an approval note or a fix list | `conditional` |
| [`document`](./document.toml) | README + changelog + release-notes drafts in parallel, then a combined doc plan | `parallel` |
| [`plan-and-build`](./plan-and-build.toml) | Minimal starter: draft a spec, then implement it | sequential |

Build / market / write / research (driven by a single stdin goal):

| Name | What it does | Showcases |
|------|--------------|-----------|
| [`launch`](./launch.toml) | Idea → market explore → honest validate → (greenlight?) brand + pitch + ads + bootstrap, else pivots | `conditional` |
| [`content`](./content.toml) | Brief → researched draft → audit/edit loop until it passes → promo posts | `loop` |
| [`research`](./research.toml) | Investigate background + evidence + counter-views in parallel → synthesize a cited report | `parallel` |
| [`localize`](./localize.toml) | Translate one input into several locales in parallel (locale-aware) | `parallel` |
| [`seo`](./seo.toml) | Audit a site/page, then produce a prioritized strategy brief | sequential |

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
