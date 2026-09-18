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
| [`develop`](./develop.toml) | Gathers context for a feature spec, then iterates a developer/evaluator loop with a real build/test gate until the evaluator approves, then summarizes the change. | `loop` + `conditional` |
| [`debug`](./debug.toml) | Reproduces a bug and locates its root cause in the current repo, iterates a fix/verify loop until a test proves it fixed, then summarizes the change. | `loop` + `conditional` |
| [`upgrade`](./upgrade.toml) | Upgrades dependencies (named packages, or safe patch/minor by default), fixes breakages in a bump/verify loop until the project's checks pass, then writes upgrade notes. | `loop` + `conditional` |
| [`harden`](./harden.toml) | Security-audits the current repo across OWASP lenses, then fixes and independently re-audits in a loop until findings are resolved and checks stay green. | `loop` + `conditional` |
| [`learn`](./learn.toml) | Grounds project memory from the codebase, promotes durable knowledge into the .box/ knowledge base, then audits and fixes the notes until every claim verifies against the repo. | `loop` + `conditional` |
| [`review`](./review.toml) | Reviews the current unstaged changes against the request, independently verifies each finding, then branches on a deterministic verdict to an approval note or a prioritized fix list. | `conditional` |
| [`deep-review`](./deep-review.toml) | Reviews a change from five independent lenses in parallel, adversarially verifies every finding against the real code, then synthesizes one severity-ordered review with a verdict. | `parallel` |
| [`document`](./document.toml) | Classifies the current changes into a SemVer bump and change buckets, drafts README, changelog, and release notes in parallel, then reconciles them into one consistent plan via a validating gate. | `parallel` + `loop` |
| [`plan-and-build`](./plan-and-build.toml) | Drafts a concise implementation spec from the request, then implements it and verifies with the project's own check. | `conditional` |

Build / market / write / research (driven by a single stdin goal):

| Name | What it does | Showcases |
|------|--------------|-----------|
| [`scout`](./scout.toml) | Mines a field for evidenced pain via parallel community, review, and demand sweeps, vets candidates adversarially into ranked briefs or an honest no-signal verdict. Chain the winner into launch. | `parallel` + `loop` + `conditional` |
| [`launch`](./launch.toml) | Takes a product idea from market exploration to an honest go/no-go, then, only if viable, produces a GTM strategy, brand, pitch, ads, and a zero-budget launch plan. | `conditional` |
| [`content`](./content.toml) | Turns a brief into a researched, publish-ready article in the current directory, refined by an edit/audit loop until it passes. Chain the promote workflow for social adaptation. | `loop` |
| [`promote`](./promote.toml) | Turns an existing article into grounded, platform-native social drafts for each network requested, polished by a fix/audit loop until all pass, then delivered to files or inline. Chain after content. | `loop` |
| [`research`](./research.toml) | Investigates a question from background, evidence, and counter-argument angles in parallel, synthesizes a cited report, then loops a groundedness judge until every claim verifies against its sources. | `parallel` + `loop` |
| [`localize`](./localize.toml) | Transcreates content into every requested language, working each one in its destination file in-place (or inline when none is given), loops fix and audit until each passes native-fluency review, then ends with a per-language summary. | `loop` |
| [`apply`](./apply.toml) | Turns a master resume and a job posting into a tailored, ATS-optimized resume, a cover letter, and an honest match-gap report, refined by a screen/fix loop. Produces documents; never auto-submits. | `loop` |
| [`report`](./report.toml) | Turns a data source into a decision-ready report with every number computed from the data and inline-SVG charts, refined by an accuracy loop, delivered as self-contained HTML that prints to PDF. | `loop` |
| [`seo`](./seo.toml) | Audits a site or page across technical, on-page, off-page, and GEO lenses, then turns the evidence-bound findings into a tiered, finding-traceable, KPI-tagged SEO strategy brief. | sequential |

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

### Graph routing

Steps run top to bottom by default. For explicit control flow — conditional
branches and bounded cycles (e.g. a review→fix loop) — declare `entry`,
`max_transitions`, and top-level `[[edges]]`. Every step kind above becomes a
graph node; `$end` is the reserved terminal target.

- `entry` — name of the first node to run.
- `max_transitions` — hard cap on total node executions; bounds cycles.
- `[[edges]]` — `from`/`to` routes, tested in declaration order. Add
  `when = { contains = "..." }` or `when = { matches = "regex" }` for a
  conditional route; each node needs exactly one unconditional default edge,
  declared last.

### Variable substitution

- `{{input}}` — the stdin passed to the workflow.
- `{{<step-name>}}` — the assistant output of an earlier step.
- Standard placeholders (`{{DATE}}`, `{{CWD}}`, `{{GIT_STATUS}}`, …) and
  `<context>path</context>` blocks are expanded per step, same as a chat session.

See [`plan-and-build.toml`](./plan-and-build.toml) for a complete example.
