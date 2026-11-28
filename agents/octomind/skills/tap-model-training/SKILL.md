---
name: tap-model-training
title: "Fine-Tune Embedding Model: Octomind Embed"
description: "Fine-tune, evaluate and publish the octomind-embed model that routes requests to capabilities and agents. Use when triggers or agent descriptions change."
license: Apache-2.0
compatibility: "octomind-tap repo with the model/ subdirectory. Requires Python 3.11+, uv, ANTHROPIC_API_KEY for LLM augmentation, HF_TOKEN with write scope for publishing. GPU optional."
capabilities: core
rules:
  - content(retrain)
  - content(octomind-tap)
  - content(octomind-embed)
  - content(auto-activation)
  - content(auto_activate)
  - match(\b(re)?train\s+(the\s+)?(tap|embedding|embed)\b)
  - match(\b(publish|ship)\s+(the\s+)?(tap|embedding|embed|model)\b)
  - match(\b(add|edit|update)\s+(a\s+)?(new\s+)?(capability|capabilities|trigger|triggers)\b)
  - match(\b(eval_gate|eval_real|build_dataset|build_eval_seed|calibrate_thresholds|model_soup|compare_bases)\b)
  - match(\bbin/(train|publish)\b)
  - match(\b(auto[\s-]?activation|capability\s+routing)\b)
  - semantic(retrain the tap embedding model)
  - semantic(I added a new capability — what do I need to do)
  - semantic(how do I republish octomind-embed)
  - semantic(my new triggers aren't being picked up by auto-activation)
  - semantic(training got disconnected, how do I resume)
  - semantic(how do I update the runtime threshold for capability auto-activation)
  - semantic(the model is missing intents for one of my capabilities)
---

## Overview

`muvon/octomind-embed` is the bi-encoder octomind uses for three decisions: scoring a user message against capability triggers, scoring it against the `semantic()` phrases of the skills offered to the running agent (the specialties inside a field are skills, in `skills/` and in `agents/<name>/skills/`), and scoring a delegated task brief against the "`<title>. <description>`" of each of the 33 routable base agents. Since 2026-09 it is `ibm-granite/granite-embedding-30m-english` (6 layers, 384-dim, CLS-pooled) given a short contrastive fine-tune; the runtime loads `onnx/model_quantized.onnx`, a 30 MB graph with int8-stored weights and fp32 arithmetic. Whenever triggers, semantic phrases, or agent titles and descriptions change, the model is stale. This skill walks through retraining, calibration, publishing, and recovery.

The cross-encoder reranker is intentionally not trained or shipped: at the current capability count it does not improve routing over a well-calibrated bi-encoder.

## Mental model

The three decisions have the same shape: rank the candidates by cosine, accept the winner only if it clears an absolute threshold and beats the runner-up by a margin, otherwise abstain. For capabilities the score is the mean of the top-3 trigger cosines; for skills it is the best cosine to a `semantic(phrase, threshold)` phrase, with the threshold of that rule; for agents it is the cosine to the agent text. The model, the corpus, and the constants are one system: retraining moves the cosine scale, so the constants must be recalibrated on the graph the runtime loads and shipped together with the weights.

The fine-tune is a nudge with two phases. First 105 steps over the four capability and agent files in turn (capability pairs and triplets, agent pairs and triplets), then 105 steps over the agent files and the skill pairs (`skill_brief_pairs.jsonl`: a task brief against one `semantic()` phrase of the skill that holds its procedure): capability batches past about 50 start to cost accuracy on real prompts, while routing batches keep improving routing. The agent files use batches of 33, one text per agent, because each batch admits an agent text once. `bin/train` then sweeps a blend of the fine-tuned and base weights (WiSE-FT soup) and keeps the fine-tune or blend with the highest sum of capability gate accuracy, routing handoff rate and skill right-rate.

## Rules

### When to retrain

| Change | Retrain? |
|--------|----------|
| Added or removed a capability (`capabilities/<name>/config.toml`) | yes |
| Edited `triggers = [...]` | yes |
| Added or edited `semantic(...)` rules in any `SKILL.md`, shared or agent-owned | yes |
| Added briefs, or changed which skills a brief carries (`data/agent_briefs.jsonl`) | yes |
| Edited the `_oos` curated phrases in `build_dataset.py` | yes |
| Added or removed an agent, or edited its `# Title:` / `# Description:` | yes |
| Agent prompt, skill body, or docs change with none of the above touched | no |
| Threshold/margin change in octomind `capability.rs` / `skill.rs` / `tap_route.rs` | no — rebuild octomind |

### Standard retrain flow

Run from `model/`, inside `tmux` or `nohup` so a dropped connection doesn't kill it. Without a GPU the trainer uses the CPU; on a machine other jobs share, set `OMP_NUM_THREADS` to a measured count (4 beat 12 by 3-6x on a loaded 12-core box):

```bash
cd model && uv sync
tmux new -s train
ANTHROPIC_API_KEY=... bin/train --llm --resume
```

What runs (`bin/train`):

1. `build_eval_seed.py` once, if `data/eval_real.jsonl` is missing.
2. `augment_llm.py --resume` — LLM paraphrases for new `(label, trigger)` pairs only, appended to `data/intents.jsonl`.
3. `augment_agents.py` — LLM-written task briefs per base agent in five styles, train and eval split written by different models, appended to `data/agent_briefs.jsonl` for whatever is missing. Each row carries the agent, the `skills` that hold the brief's procedure (empty for new briefs) and its `source` tag. To replace an agent's briefs after its description changed, delete its lines first.
4. `build_dataset.py` — `pairs.jsonl`, `triplets.jsonl`, `holdout.jsonl`, `raw_triggers.jsonl` (the un-augmented corpus the runtime embeds: trigger phrases and skill `semantic()` phrases without their thresholds, each row marked `capability` or `skill`; the capability gate scores against the capability rows only and skips `eval_real` rows labelled with a skill), `agent_pairs.jsonl`, `agent_triplets.jsonl`, `raw_agents.jsonl` (the 34 agent texts the runtime embeds) and `skill_brief_pairs.jsonl` (train briefs against a phrase of each skill they carry), with the `_oos` sink label, multi-turn surfaces, and hard-negative mining. Paraphrases in `intents.jsonl` whose label or source trigger is not in the catalog are dropped.
5. `train.py` — CachedMNRL + Matryoshka: `train.max_steps` over the capability and agent files (`round_robin`), then `train.agent_steps` over the agent files and the skill pairs. Capability files train at `loss.scale` (10), agent files at `loss.agent_scale` (50) with batches of `train.agent_batch_size` (33), skill pairs at `loss.skill_scale` (10).
6. `model_soup.py` + `compare_bases.py --skill-eval` — sweep `soup.alphas` against the base and keep the fine-tune or blend with the highest sum of capability gate accuracy, routing handoff rate and skill right-rate.
7. `eval.py` (holdout), `eval_gate.py` (`eval_real`, informational here), `eval_route.py` (does a brief reach its agent among all 34: top-1, handoff, wrong) and `eval_skills.py` (replays the runtime's skill rule engine on the eval briefs: right skill loaded, wrong skill loaded).
8. `export_onnx.py` (fp32 graph + int8-stored graph, checked against each other), then `eval_gate.py`, `eval_route.py`, `eval_skills.py`, `dump_scores.py` and `calibrate_cpus.py` on the graph the runtime loads.

Other flags: `--skip-build` (reuse `data/`), `--skip-export`, `--ft checkpoints/<dir>` (redo soup, eval, export, and calibration on an existing run), `--iterations N` (re-mine capability triplets from the previous round's mistakes), `--legacy` (diagnostic `model.fit` path).

### Calibrating the runtime gates

`bin/train` prints the operating points for the machine it ran on. Confirm them on every CPU kind before rollout: dump the scores once per kind, then calibrate over all dumps.

```bash
uv run python scripts/dump_scores.py --model checkpoints/<run>/onnx --out checkpoints/<run>/scores/arm64.json
uv run python scripts/calibrate_cpus.py checkpoints/<run>/scores/*.json
uv run python scripts/eval_runtime_gate.py --model checkpoints/<run>/onnx   # octomind's test fixtures, no Rust build
```

`dump_scores.py` needs only numpy, pyyaml, tokenizers and onnxruntime, so it runs in a bare container (its docstring has the Docker command for x86 on an ARM Mac). `calibrate_cpus.py` picks, per decision, the point with the best accuracy on the worst machine among those that keep false activations under the cap on every machine (capability null false-positive rate 0.03; routing wrong handoffs 0.02). Copy the values into:

- `octomind/src/mcp/runtime/capability.rs` — `AUTO_ACTIVATE_THRESHOLD`, `AUTO_ACTIVATE_MARGIN`
- `octomind/src/mcp/runtime/skill.rs` — `SEMANTIC_DEFAULT_THRESHOLD`, `SEMANTIC_MARGIN`
- `octomind/src/mcp/orchestration/tap_route.rs` — `ROUTE_THRESHOLD`, `ROUTE_MARGIN`
- `model/configs/default.yaml` — `eval.runtime_threshold`, `eval.runtime_margin`, `eval.route_threshold`, `eval.route_margin` (the publish gate and `eval_route.py` score at these)

The 2026-11 model runs at 0.68 / 0.05 for capabilities and 0.66 / 0.05 for routing, and scores identically on ARM, x86 and x86 with VNNI. The graph shipped 2026-09 quantized activations per batch and scored the same text up to 0.08 apart between ARM and x86; the per-CPU dumps are the check that this has not come back.

### Publishing

```bash
HF_TOKEN=hf_... bin/publish --run checkpoints/<dir> --baseline eval_baselines.shipped-<sha>.json
```

`bin/publish` gates twice, the fp32 safetensors and then `onnx/model_quantized.onnx`, and aborts on regression (top-1 drop > 0.01, null FPR rise > 0.01, per-label recall drop > 0.05). Per-label recall only gates labels with at least `--per-label-min-n` positives (default 20): a 10-row label moves in 0.1 steps, so its one flipped prompt prints as a note instead of blocking. It warns when the int8 graph is missing — export it first, since the runtime prefers it. `--force`/`--skip-gate` are for documented emergencies; `--dry-run` prints without uploading.

### Gate the candidate against the incumbent, not a stale baseline

`eval_baselines.json` describes the graph that was current when it was written. It goes stale the moment the corpus is rebuilt, and then it measures the dataset change, not the model: the incumbent fails it too. Rescore the shipped graph on today's `data/eval_real.jsonl` first, then gate the candidate against that file:

```bash
INC=<checkpoint of HF main>    # confirm by sha256, not by name
uv run python scripts/eval_gate.py --model $INC --write-baseline eval_baselines.shipped-<sha>.json
uv run python scripts/eval_gate.py --model <candidate> --baseline eval_baselines.shipped-<sha>.json
uv run python scripts/eval_gate.py --model <candidate>/onnx --onnx-file model_quantized.onnx \
    --baseline eval_baselines.shipped-<sha>.json
```

Build the incumbent from a local copy whose hashes match the hub, not from a fresh download: `sha256sum` on `model.safetensors` and `onnx/model_quantized.onnx` against the LFS oids from `https://huggingface.co/api/models/<repo>/tree/main?expand=true`. Commit the resulting baseline file — it is what every publish compares against until the rollout lands.

### Ship the pin with the weights

Octolib serves a repo already in its cache without asking the hub whether it changed, and octomind asserts the loaded revision equals its pin. So a published graph reaches nobody until `MODEL_REVISION` in `octomind/src/embeddings/mod.rs` names the new commit, and an old build on a fresh machine must not pick up new weights under old thresholds. After the upload, one octomind commit carries:

1. `MODEL_REVISION` → the full 40-character sha of the new hub main (`curl -s https://huggingface.co/api/models/muvon/octomind-embed/revision/main`).
2. The recalibrated constants from `calibrate_cpus.py` — capability, skill, and `ROUTE_*`, mirrored in `model/configs/default.yaml`.
3. Nothing else, so the release notes say what changed.

Then verify the artifact that landed is the one that was gated: the `onnx/model_quantized.onnx` LFS oid on the hub must equal `sha256sum` of the checkpoint file. A mismatch means the upload pushed a different export.

After the rollout is confirmed, rewrite the rolling baseline from what users now run and commit it:

```bash
uv run python scripts/eval_gate.py --model muvon/octomind-embed --write-baseline eval_baselines.json
```

### Resuming an interrupted run

The trainer checkpoints every epoch (`save_total_limit=2`). If `checkpoints/embed-*/checkpoint-N/` exists:

```bash
uv run python scripts/train.py --resume                 # latest run dir
uv run python scripts/train.py --resume-from <run-dir>  # explicit
```

If iteration 1 was interrupted: finish it with `--resume`, re-mine with `build_dataset.py --neg-embed-model <iter1-dir>`, train iteration 2 with `train.py`, then `bin/train --ft <iter2-dir>` for soup, eval, export, and calibration. `--resume` covers the modern `train.py` path only, not `--legacy`.

## Examples

### Example 1: new triggers not picked up

❌ `bin/train --skip-build` after editing triggers — the build is what turns triggers into training surfaces, so the new run inherits the old weaknesses.

✅ `bin/train --llm --resume` — rebuild, augment only the new triggers, retrain.

### Example 2: wrong capability wins but triggers look right

Retraining rarely fixes this. First run `calibrate_cpus.py` on fresh dumps to see whether the shipped thresholds still fit the model; add the failing prompt to `data/eval_real.jsonl` with its correct label and rerun `eval_gate.py`; then compare the competing capabilities' triggers — shared generic vocabulary is fixed by differentiating triggers, not by more training.

### Example 3: publishing without a baseline update

Publishing and forgetting `--write-baseline` leaves the next publish gating against the previous model, so a later regression can slip through. Record the baseline once the rollout is confirmed.

### Example 4: pushed the weights, users still run the old graph

`bin/publish` succeeded and the hub main moved, yet every install keeps routing on the previous weights: `MODEL_REVISION` still names the old sha, and octolib never re-checks a cached repo. Bump the pin in the same commit as the constants — publishing alone reaches only fresh installs of a build that has no pin.

## Checklist

- [ ] Trigger, semantic-phrase or agent-description change → full rebuild with `--llm --resume`, not `--skip-build`?
- [ ] Training run inside tmux or nohup?
- [ ] Winner evaluated on holdout, `eval_real`, `eval_route.py` and `eval_skills.py`; ONNX graphs exported and the small one scored?
- [ ] Thresholds calibrated over dumps from every CPU kind and copied into `capability.rs`, `skill.rs`, `tap_route.rs`, and `configs/default.yaml`?
- [ ] `eval_runtime_gate.py` reports PASS for octomind's fixtures?
- [ ] Gate run against the incumbent rescored on the current corpus, with the baseline file committed — not against a stale `eval_baselines.json`?
- [ ] `bin/publish` passed the gate without `--force` on both the fp32 and the int8 graph?
- [ ] `MODEL_REVISION` in `octomind/src/embeddings/mod.rs` bumped to the new hub sha in the same commit as the constants?
- [ ] Published `onnx/model_quantized.onnx` hash equals the gated checkpoint's?
- [ ] Baseline rewritten from `muvon/octomind-embed` after the rollout was confirmed?

## Composition / References

- `model/README.md` — pipeline, dataset, loss stack, eval set, routing and skill evals
- `model/configs/default.yaml` — base model, training, soup alphas, runtime-mirror constants
- `model/bin/train`, `model/bin/publish` — entry points
- `tap-capability-authoring` skill — writing triggers
