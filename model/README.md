# octomind-tap embedding model

Fine-tune one small ONNX bi-encoder that octomind uses for three decisions:

- **Capability auto-activation**: which capability to switch on for a
  user message. `octomind/src/mcp/runtime/capability.rs` scores the
  message against each capability's trigger phrases (mean of the top 3
  cosines) and activates the best one when it clears a threshold and
  leads the runner-up by a margin.
- **Skill activation**: which skill to load for a user message.
  `octomind/src/mcp/runtime/skill.rs` scores the message against the
  `semantic(phrase, threshold)` rules of the skills offered to the running
  agent and loads the best one when it clears that rule's threshold and
  leads the runner-up by a margin.
- **Agent routing**: which agent should take a delegated task.
  `octomind/src/mcp/orchestration/tap_route.rs` scores the task brief
  against each reachable agent's "`<title>. <description>`" text and
  hands the task over under the same threshold-plus-margin rule, with
  its own constants. The tap has 34 base agents; the specialties inside a
  field are skills, so the model's second job after capability activation
  is to send a user message to the right skill's phrase.

The model:

- **`muvon/octomind-embed`** — granite-embedding-30m-english (30M
  params, 6 layers, 384-dim, CLS-pooled, prefix-free) given a short
  contrastive fine-tune. The runtime loads the ONNX graph with
  int8-stored weights (30 MB, fp32 arithmetic) and reads at most 512
  tokens of a text.
- Measured 2026-11 on that graph, identical on ARM, x86 and x86 with
  VNNI, against the weights published 2026-09 (scored on ARM; their
  graph scored differently per CPU):

  | | 2026-09 weights | 2026-11 weights |
  | --- | --- | --- |
  | Capability: right one activated (`eval_real`, 1,384 prompts) | 0.809 (0.796 on x86) | 0.837 |
  | Capability: activated on a prompt that needs none (90 prompts) | 0.033 (0.022 on x86) | 0.022 |
  | Routing: brief ranks its own agent first (2,184 briefs, own domain) | 0.682 | 0.824 |
  | Routing: brief handed to its agent | 0.304 | 0.456 |
  | Routing: brief handed to a wrong agent | 0.024 | 0.011 |

  Each column is at the constants octomind runs those weights with
  (threshold / margin): 0.65 / 0.06 for capabilities and 0.67 / 0.04 for
  routing in 2026-09, 0.68 / 0.05 and 0.66 / 0.05 in 2026-11.
- Before 2026-09 the same repo held a BGE-small-en-v1.5 fine-tune. The
  base bake-off (`scripts/compare_bases.py` on the raw trigger corpus,
  each model at its own best operating point) put granite at gate 0.846
  zero-shot vs 0.708 for bge-small and 0.690 for that fine-tune, at half
  the layers.
- New weights under the same name reach fresh installs only (hf_hub never
  re-checks a cached repo), and the runtime thresholds must ship with
  them — see calibration below.

The cross-encoder reranker is intentionally NOT trained / shipped here.
We tested it; with the current capability count it doesn't materially
improve the routing decision over a well-tuned bi-encoder. If the
catalog grows past ~150 capabilities and inter-cluster competition
gets harder, revisit.

## Why fine-tune

Off-the-shelf encoders score generic verbs ("run", "execute") high
across unrelated capabilities, so capabilities with shared vocabulary
(shell vs programming-rust) cluster too close to clear the runtime
margin gate.

With trigger-phrase supervision plus hard-negative mining, we sharpen
the embedding on the actual decision the runtime makes:

    intent (user phrase)  →  capability (one of N installed) or abstain

The fine-tune is a nudge in two phases: 105 steps over the four capability
and agent files in turn, then 105 steps over the agent files and the skill
pairs in turn. More capability batches cost accuracy on real prompts (210
mixed steps: capability top-1 0.931 against 0.940 for 105), while routing
batches keep improving routing.

A fine-tune can also *forget* some of the base's generalization.
Interpolating the fine-tuned weights with the base (WiSE-FT soup) wins it
back when that happens, so `bin/train` sweeps alpha 0.1-0.6 and ships the
best of the fine-tune and the blends by capability gate plus routing
handoff plus skill right-rate. In 2026-09 the blend at alpha 0.6 won; in 2026-11 the unblended
fine-tune did (every blend lost routing handoff, none gained capability
gate).

## Pipeline

    capabilities/*/config.toml  +  skills/*/SKILL.md  +  agents/<name>/skills/*/SKILL.md
    +  agents/<name>/default.toml
                       │
                       ▼
    scripts/augment_llm.py     (optional) →  data/intents.jsonl
    scripts/augment_agents.py  (optional) →  data/agent_briefs.jsonl
                       │
                       ▼
    scripts/build_dataset.py   →  data/pairs.jsonl, triplets.jsonl, holdout.jsonl
                       │          raw_triggers.jsonl (what the runtime embeds)
                       │          agent_pairs.jsonl, agent_triplets.jsonl,
                       │          raw_agents.jsonl (the agent texts the runtime embeds)
                       │          skill_brief_pairs.jsonl (brief → phrase of its skill)
                       │       (+ _oos sink label, multi-turn surfaces,
                       │          positive-aware hard-negative mining)
                       ▼
    scripts/train.py           →  checkpoints/embed-<run>-<ts>/
                       │       (CachedMNRL + Matryoshka: 105 steps on the
                       │        capability and agent files, then 105 on the
                       │        agent files and skill_brief_pairs.jsonl)
                       ▼
    scripts/model_soup.py      →  checkpoints/embed-<run>-<ts>-soup-a<α>/
    scripts/compare_bases.py      (best capability gate + routing handoff
                       │           + skill right-rate wins)
                       ▼
    scripts/eval.py            →  holdout-distribution metrics
    scripts/eval_gate.py       →  real-user-distribution metrics  ← publish gate
    scripts/eval_route.py      →  does a task brief reach its agent
    scripts/eval_skills.py     →  does the right skill load for a task brief
                       │
                       ▼
    scripts/export_onnx.py     →  onnx/  (fp32 graph + int8-stored graph)
    scripts/dump_scores.py     →  scores/<cpu>.json, once per CPU kind
    scripts/calibrate_cpus.py  →  runtime thresholds, checked on every CPU kind
    scripts/eval_runtime_gate.py  →  octomind's Rust test fixtures, scored in Python
                       │
                       ▼
    scripts/push_hf.py         →  hf.co/muvon/octomind-embed

The HF repo holds BOTH formats:
- `onnx/model_quantized.onnx` (+ `model.onnx`) → what octomind loads via
  octolib's ONNX provider; it honours `1_Pooling/config.json` (CLS).
- `model.safetensors` + config + tokenizer → sentence-transformers layout
  for eval scripts and the candle fallback (`EMBED_BACKEND`), which always
  mean-pools and is therefore not the production path for this model.

`bin/train` runs the full pipeline. Use `--skip-export` to skip ONNX,
`--ft checkpoints/<dir>` to redo soup + eval + export on an existing run.

## Setup

    cd model
    uv sync

## Quick start

    # 1) Bootstrap a real-user eval set (one-time, then hand-edit as needed).
    uv run python scripts/build_eval_seed.py

    # 2) Record the baseline from the currently-shipped model (raw trigger
    #    corpus — the same thing the runtime scores).
    uv run python scripts/eval_gate.py \
        --model muvon/octomind-embed \
        --write-baseline eval_baselines.json

    # 3) Full training run (build + train + soup + eval + export + calibrate).
    ANTHROPIC_API_KEY=... bin/train --llm

    # 4) Calibrate the runtime thresholds, check them on every CPU kind and copy them
    #    into configs/default.yaml and octomind (see "Runtime threshold
    #    calibration" below). bin/train prints the numbers for this
    #    machine only.

    # 5) Publish (the gate runs automatically on both graphs).
    HF_TOKEN=hf_... bin/publish

    # 6) After production rollout, record the new baseline.
    uv run python scripts/eval_gate.py --model muvon/octomind-embed \
        --write-baseline eval_baselines.json

## What's in the loss stack

Configured in `configs/default.yaml::loss`. Defaults match the
production recipe.

1. **CachedMultipleNegativesRankingLoss** — MNRL with GradCache, lets
   us push the effective batch to 256-2048 on a single GPU. More
   in-batch negatives = harder contrast = wider runtime margins.
   ([sbert docs](https://huggingface.co/blog/train-sentence-transformers))
   Its `scale` (the inverse temperature of the in-batch softmax) is set
   per file: 10 for the capability files (`loss.scale`), 50 for the agent
   files (`loss.agent_scale`) and 10 for the skill pairs (`loss.skill_scale`). An agent is one title and description
   rather than a cluster of triggers, and at 10 routing stayed
   under-fitted: handoff 0.418, against 0.456 at 50 with the capability
   gate at 0.837 instead of 0.823 (2026-11).

2. **GISTEmbedLoss** *(optional, off by default)* — A frozen guide model
   (BGE-small-en-v1.5) decides which in-batch candidates are *true*
   negatives. Anything the guide rates above the anchor/positive
   similarity is excluded from the contrastive loss. Off because without
   an explicit `scale` it trains at temperature 0.01, which collapses the
   runtime margin, and it costs ~5x per step on CPU.
   ([arxiv 2402.16829](https://arxiv.org/abs/2402.16829))

3. **MatryoshkaLoss** *(optional, wraps either of the above)* —
   Applies the inner loss at `[384, 256, 192, 128, 96]` truncation
   dims simultaneously. The same trained model is then usable at any
   of those dims without retraining — useful when the on-disk embed
   cache size becomes a concern.
   ([sbert docs](https://sbert.net/examples/sentence_transformer/training/matryoshka/README.html))

## What's in the dataset

`build_dataset.py` builds its artifacts from `capabilities/`, the shared
`skills/`, the skills each agent owns (`agents/<name>/skills/`) and the 34 base
agents (`agents/<name>/default.toml`); `scripts/tap_paths.py` at the repository
root lists them:

- **pairs.jsonl** `{anchor, positive, label}` — in-capability pairs
  from authored triggers + rule-template expansions + LLM paraphrases.
  MNRL training signal.
- **triplets.jsonl** `{anchor, positive, negative, label, neg_label}` —
  hard-negative triplets. Round 1 uses base-BGE centroid similarity;
  rounds 2+ use the previous FT bi-encoder's actual retrieval mistakes
  (NV-Retriever recipe, with positive-aware false-negative filtering).
  ([arxiv 2407.15831](https://arxiv.org/pdf/2407.15831))
- **holdout.jsonl** `{intent, label}` — held-out trigger paraphrases
  per capability for in-distribution eval.
- **raw_triggers.jsonl** `{anchor, positive, label}` — the un-augmented
  `config.toml` triggers + skill `semantic()` phrases (the phrase without its
  threshold: `semantic(write a researched article, 0.76)` contributes
  "write a researched article"). Each row has a `kind`, `capability` or
  `skill`. Training draws on both kinds in one pool; the capability gate
  (`eval_gate.py`, `calibrate_thresholds.py`, `dump_scores.py`,
  `compare_bases.py`) offers only the `capability` rows as candidates, as
  `capability.rs` does, and leaves out the `eval_real.jsonl` rows whose gold
  label is a skill (it prints how many, per row kind). This is what the
  runtime embeds, so `eval_gate.py`, `compare_bases.py` and
  `calibrate_thresholds.py` score against it (`eval.triggers_path`).
- **agent_pairs.jsonl** `{anchor, positive, label}` — a train-split task
  brief and the text of the agent that should take it (33 agent labels).
- **agent_triplets.jsonl** — the same pairs with a hard negative: per
  brief, the 6 closest other agents (`--agent-neg-per-brief`). An agent that
  scores within 0.95 of the brief's own agent is skipped, since it may fit the
  brief as well.
- **raw_agents.jsonl** `{tag, text}` — one row per base agent that has
  briefs (33 of the 34; `plain` is a baseline nobody routes to and has none);
  `text` is "`<title>. <description>`", the string the runtime embeds.
- **skill_brief_pairs.jsonl** `{anchor, positive, label}` — a train-split
  task brief that carries skills, and one `semantic()` phrase of each of its
  skills (label = skill name). The phrase rotates over the skill's phrases
  from brief to brief, so every phrase is trained on. Eval-split briefs never
  enter training.

The agent and skill files train under `NO_DUPLICATES` batches, which admit a
text once: a batch of agent pairs holds one brief per agent, and a batch of
triplets about half as many (each row uses two agent texts). `train.agent_batch_size`
is therefore 33, the number of routable agents, so each agent step contrasts every
agent against every other. A skill batch holds each phrase once; two different
phrases of one skill in a batch count as negatives of each other, as two
different triggers of one capability do in the capability pairs.

### Task briefs for agent routing

Agent manifests carry no example tasks, so the briefs are written by an
LLM: `scripts/augment_agents.py` reads each agent's manifest, shows the writer
the roster of all agents to tell apart, and writes briefs in five styles to
`data/agent_briefs.jsonl`. A row is `{agent, split, style, brief, model,
skills, source}`: `agent` is the base agent that takes the brief, `skills` the
skills that hold the procedure the brief asks for (empty when the agent's own
prompt covers it), and `source` the tag the brief was written for (it keeps the train/eval split
traceable; for briefs written by the script it is the agent).

| Style | What it imitates |
| ----- | ---------------- |
| `lead` | a lead delegating: the kind of work, then a few sentences of context (30-90 words) |
| `short` | one sentence, the task and nothing else |
| `user` | how an end user asks for it in a chat |
| `full` | a brief in four labelled parts: objective, context, source material, output shape (80-160 words) |
| `long` | the same four parts with the raw material written out (500-900 words), longer than the 512 tokens the runtime reads |

Training briefs and eval briefs come from different models
(`SPLIT_MODELS` in the script), so the eval set is not an echo of the
training phrasing. The file is append-only: a run adds only the
(agent, split, style) groups that are missing, and eval briefs written
once stay, so routing and skill scores remain comparable across retrains. To
replace an agent's briefs after its description changed, delete its
lines and run the script again. A brief written by the script has no
`skills`, so it trains agent routing only.

### `_oos` sink label

The training set includes a synthetic `_oos` label with curated
chitchat / vague / paste-dump / off-topic phrases. The runtime never
registers `_oos` as a capability — it exists only at training time so
the encoder learns a dedicated cluster for "no real intent" phrases,
which lowers real-cap cosines for those inputs and lets the runtime's
absolute-threshold gate filter them.
Disable with `--no-oos-label` on `build_dataset.py`.

### Multi-turn-shaped surfaces

A fraction of training surfaces (default 15%, configurable via
`--multi-turn-ratio`) get a context-laden prefix attached
("earlier we set up X; now ...", "following up: ...", etc.). Trains
the embedding to attend to the actionable tail when the latest user
message presumes prior conversation context.
([arxiv 2411.14252](https://arxiv.org/html/2411.14252v1))

### Cross-domain shell synthesis

The `shell` label gets synthetic surfaces like `"run cargo build"`,
`"execute swift build"` so the model learns the verb dominates the
tool name for routing — same as before, just kept for completeness.

## What's in the eval set

`data/eval_real.jsonl` is the **frozen** real-user eval set. It's a
*different distribution* from `holdout.jsonl`:

- `holdout.jsonl` uses the same rule-template expansion as training,
  just with held-out triggers. Good for in-distribution regression
  testing.
- `eval_real.jsonl` reflects how real users phrase prompts in
  coding-assistant chats (WildChat / LMSYS-Chat distribution): short
  utterances, follow-ups, typos, casual register, paste-dumps,
  chitchat, vague asks, sarcastic feedback, ambiguous edge cases.
  ~15-20% of real chat traffic is "Other/Unknown" and should abstain —
  those rows have `label: null` in the eval set.

Each row carries a `kind` tag (positive / follow_up / typo_casual /
multi_turn / cross_domain_shell / chitchat / vague /
sarcastic_feedback / paste_dump / off_topic / ambiguous / compound) so
`eval_gate.py` can break down accuracy by failure-mode category.

Bootstrap with `scripts/build_eval_seed.py`, then **hand-edit the
JSONL** to add production-observed failure modes. The file is the
publish gate; whatever is in it becomes part of the regression test.

### Routing eval

`scripts/eval_route.py` ranks every eval-split brief against the texts of all
33 routable agents, as a caller that reaches every agent sees them, and reports three
numbers at the configured `eval.route_threshold` / `route_margin`:

- `top1_acc` — the brief's own agent ranks first.
- `handoff` — the gate fires and picks the brief's agent.
- `wrong` — the gate fires and picks another agent.

It also prints the point with the best handoff whose `wrong` stays under
0.02, and the numbers per brief style.

### Skill eval

`scripts/eval_skills.py` replays the runtime's skill rule engine (keyword
rules, `semantic()` thresholds and the margin between the two best
candidates) on the briefs. For each brief the pool is the skills offered to
its agent: the ones the agent owns and the shared ones whose `domains:` has
it. `--model` takes a checkpoint directory, an `onnx/` directory or a hub id
with a revision (`muvon/octomind-embed@<sha>`). Three summary lines, for
the keyword rules alone (`kw`), the full engine (`full`) and the full engine
without the margin rule (`reach`), each give `own` (briefs that carry the
skill and load it, the right-skill rate) and `other` (briefs of other work
that load it, the wrong-skill rate). `--misses <skill>` lists the briefs a
skill missed and the ones that loaded it by mistake; `--json <path>` writes
the three lines as numbers. The skills counted in the summary are those that
head a brief's `skills` list.

## Publish gate

`bin/publish` runs `eval_gate.py` against `eval_baselines.json` before
upload. Fails if:

- `top1_acc` drops more than `--top1-tol` (default 0.01)
- `null_fpr` rises more than `--fpr-tol` (default 0.01)
- any per-capability recall drops more than `--per-label-tol` (default 0.05)

Override with `bin/publish --force` only for emergencies (and record
why in the commit message).

## Runtime threshold calibration

The runtime compares cosines against constants that only fit one set of
weights:

| Decision | octomind constants | Mirror in `configs/default.yaml` |
| -------- | ------------------ | -------------------------------- |
| capability activation | `capability.rs` `AUTO_ACTIVATE_THRESHOLD` / `AUTO_ACTIVATE_MARGIN`, `skill.rs` `SEMANTIC_DEFAULT_THRESHOLD` / `SEMANTIC_MARGIN` | `eval.runtime_threshold` / `runtime_margin` |
| agent routing | `tap_route.rs` `ROUTE_THRESHOLD` / `ROUTE_MARGIN` | `eval.route_threshold` / `route_margin` |

Every base has its own cosine scale, so the operating point moves with
each retrain. Calibrate against `onnx/model_quantized.onnx`, because
that is the graph the runtime loads, and confirm the result on every
CPU kind. The graph `export_onnx.py` writes today computes in fp32 and
scored identically on ARM, x86 and x86 with VNNI (2026-11). The graph
shipped 2026-09 quantized its activations per batch and did not: the
same text scored 0.620 on an ARM Mac and 0.664 on an x86 CI runner, and
a test that passed on the Mac failed on CI. The dumps below are the
check that this has not come back.

1. Dump the scores once per CPU kind (ARM and x86 at least):

       uv run python scripts/dump_scores.py --model checkpoints/<run>/onnx \
           --out checkpoints/<run>/scores/arm64.json

   The script needs only numpy, pyyaml, tokenizers and onnxruntime, so
   it runs in a bare container; its docstring has the Docker command
   that emulates x86 on an ARM Mac.

2. Pick the thresholds that hold on all of them:

       uv run python scripts/calibrate_cpus.py checkpoints/<run>/scores/*.json

   For each decision it prints the point with the best accuracy on the
   worst machine, among the points that keep false activations under
   the cap on every machine (capability `null_fpr` 0.03; routing wrong
   handoffs 0.02).

3. Copy the constants into octomind and `configs/default.yaml`, then
   check octomind's test fixtures against the new graph without a Rust
   build, on each CPU kind:

       uv run python scripts/eval_runtime_gate.py --model checkpoints/<run>/onnx

   It reads the fixtures and constants from the octomind source tree
   (`--octomind`, default: a sibling checkout) and prints PASS or FAIL
   per test, plus every fixture that sits within `--edge` of a
   threshold.

`scripts/calibrate_thresholds.py` still prints the full Pareto front of
(gate_acc, null_fpr) for the capability decision on one machine.

## When to retrain

You MUST retrain (and republish) whenever the supervision set changes:

| Change                                                       | Retrain? |
| ------------------------------------------------------------ | -------- |
| Added a new capability (`capabilities/<new>/config.toml`)    | yes      |
| Removed a capability                                         | yes      |
| Edited `triggers = [...]` in any `config.toml`               | yes      |
| Added or edited `semantic(...)` rules in any `SKILL.md` (owned or shared) | yes |
| Edited the `_oos` curated phrases in `build_dataset.py`      | yes      |
| Added or removed an agent, or edited its `# Title:` / `# Description:` | yes |
| Added briefs, or changed the `skills` of a brief                | yes      |
| Agent prompt, playbook or docs change, title and description untouched | no |
| Code change in `octomind/` runtime only                      | no       |
| Threshold/margin tweak in `capability.rs` / `skill.rs` / `tap_route.rs` | no (just rebuild octomind) |

Run from `model/`:

    ANTHROPIC_API_KEY=... bin/train --llm --resume

`--resume` is passed to `augment_llm.py`: it skips `(label, trigger)`
pairs already paraphrased in `data/intents.jsonl`, so you only pay for
the NEW triggers and phrases. Without `--resume` you re-augment everything
(same result, costs ~$1-2 extra). Paraphrases whose label or source trigger
is not in the catalog stay in `intents.jsonl` but `build_dataset.py` drops them.
`augment_agents.py` always adds only what is missing.

Training runs on the CPU when there is no CUDA device. On a machine
that other jobs share, set `OMP_NUM_THREADS` to a measured thread count
before `bin/train`: with every core claimed, a loaded 12-core box ran a
mini-batch in 12.8 s, against 2-4 s with 4 threads.

After it finishes:

    HF_TOKEN=hf_... bin/publish        # gate-protected, blocks on regression

Then update the runtime baseline:

    uv run python scripts/eval_gate.py --model muvon/octomind-embed \
        --write-baseline eval_baselines.json

## Resuming an interrupted training

The trainer auto-checkpoints at the end of each epoch
(`save_strategy="epoch"`, `save_total_limit=2`). If you lose the SSH
session, get OOM'd, or the box reboots mid-run:

    # check what got saved
    ls checkpoints/embed-*/checkpoint-*

If you see `checkpoint-N/` directories — there's state to resume:

    uv run python scripts/train.py --resume

That picks up the LATEST `checkpoints/embed-*/` run dir, finds the
highest-numbered `checkpoint-N`, and continues from there. Use
`--resume-from <path>` to target a specific run dir.

`--resume` works only for the modern `train.py` path (CachedMNRL +
GIST + Matryoshka). The `--legacy` path has no checkpoint-resume.

If the interruption hit AT iter 1, run `--resume` once to finish iter 1,
then manually continue iter 2:

    # 1. finish iter 1
    uv run python scripts/train.py --resume

    # 2. re-mine triplets with iter-1 model
    ITER1=$(ls -td checkpoints/embed-*/ | head -1 | sed 's:/$::')
    uv run python scripts/build_dataset.py --neg-embed-model "$ITER1"

    # 3. train iter 2 fresh
    uv run python scripts/train.py

    # 4. eval + export
    ITER2=$(ls -td checkpoints/embed-*/ | head -1 | sed 's:/$::')
    bin/train --ft "$ITER2"            # soup + eval + export + calibrate

**Always run training in tmux/nohup** so disconnects don't kill the
foreground process:

    tmux new -s train
    bin/train --llm --resume
    # Ctrl+B then D to detach.  Reattach: tmux attach -t train

## Manual steps (per-stage, if you want fine control)

    uv run python scripts/build_eval_seed.py
    uv run python scripts/augment_llm.py --resume
    uv run python scripts/build_dataset.py
    uv run python scripts/build_dataset.py --neg-embed-model checkpoints/embed-<ts>  # iter 2
    uv run python scripts/train.py
    uv run python scripts/model_soup.py --base ibm-granite/granite-embedding-30m-english \
        --ft checkpoints/embed-<ts> --alphas 0.4,0.5,0.6 --out-dir checkpoints/embed-<ts>/soup
    uv run python scripts/compare_bases.py --skill-eval --models checkpoints/embed-<ts>,checkpoints/embed-<ts>/soup/soup-a0.6
    uv run python scripts/eval.py        --run <winner>
    uv run python scripts/eval_gate.py   --model <winner>
    uv run python scripts/eval_route.py  --model <winner>
    uv run python scripts/eval_skills.py --model <winner>
    uv run python scripts/export_onnx.py --run <winner>
    uv run python scripts/calibrate_thresholds.py --model <winner>/onnx --onnx-file model_quantized.onnx
    HF_TOKEN=... uv run python scripts/push_hf.py --run <winner> \
        --repo muvon/octomind-embed --type embed

## Runtime integration

Embedding model path: `octomind/src/embeddings/mod.rs` → `MODEL_NAME`.
Capability activation lives in
`octomind/src/mcp/runtime/capability.rs::auto_activate_capabilities_for_intent`,
skill `semantic()` checks in `octomind/src/mcp/runtime/skill.rs`, agent
routing in `octomind/src/mcp/orchestration/tap_route.rs::route_task`.
