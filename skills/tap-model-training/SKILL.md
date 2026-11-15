---
name: tap-model-training
title: "Fine-Tune Embedding Model: Octomind Embed"
description: "Fine-tune, evaluate and publish the octomind-embed model that routes requests to capabilities and agents. Use when triggers or agent descriptions change."
license: Apache-2.0
compatibility: "octomind-tap repo with the model/ subdirectory. Requires Python 3.11+, uv, ANTHROPIC_API_KEY for LLM augmentation, HF_TOKEN with write scope for publishing. GPU optional."
capabilities: core
domains: octomind
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

`muvon/octomind-embed` is the bi-encoder octomind uses for two decisions: scoring a user message against capability triggers and skill `semantic()` phrases, and scoring a delegated task brief against each reachable agent's "`<title>. <description>`". Since 2026-09 it is `ibm-granite/granite-embedding-30m-english` (6 layers, 384-dim, CLS-pooled) given a short contrastive fine-tune; the runtime loads `onnx/model_quantized.onnx`, a 30 MB graph with int8-stored weights and fp32 arithmetic. Whenever triggers, semantic phrases, or agent titles and descriptions change, the model is stale. This skill walks through retraining, calibration, publishing, and recovery.

The cross-encoder reranker is intentionally not trained or shipped: at the current capability count it does not improve routing over a well-calibrated bi-encoder.

## Mental model

Both decisions have the same shape: rank the candidates by cosine, accept the winner only if it clears an absolute threshold and beats the runner-up by a margin, otherwise abstain. For capabilities the score is the mean of the top-3 trigger cosines; for agents it is the cosine to the agent text. The model, the corpus, and the two pairs of constants are one system: retraining moves the cosine scale, so the constants must be recalibrated on the graph the runtime loads and shipped together with the weights.

The fine-tune is a nudge with two phases. First 105 steps over all four training files in turn (capability pairs and triplets, agent pairs and triplets), then 105 steps over the agent files alone: capability batches past about 50 start to cost accuracy on real prompts, while agent batches keep improving routing. `bin/train` then sweeps a blend of the fine-tuned and base weights (WiSE-FT soup) and keeps whichever of the fine-tune and the blends scores best on the capability gate plus routing handoff; in 2026-11 that was the unblended fine-tune.

## Rules

### When to retrain

| Change | Retrain? |
|--------|----------|
| Added or removed a capability (`capabilities/<name>/config.toml`) | yes |
| Edited `triggers = [...]` | yes |
| Added or edited `semantic(...)` rules in any `SKILL.md` | yes |
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
3. `augment_agents.py` — LLM-written task briefs per agent in five styles, train and eval split written by different models, appended to `data/agent_briefs.jsonl` for whatever is missing. To replace an agent's briefs after its description changed, delete its lines first.
4. `build_dataset.py` — `pairs.jsonl`, `triplets.jsonl`, `holdout.jsonl`, `raw_triggers.jsonl` (the un-augmented corpus the runtime embeds), `agent_pairs.jsonl`, `agent_triplets.jsonl`, `raw_agents.jsonl` (the agent texts the runtime embeds), with the `_oos` sink label, multi-turn surfaces, and hard-negative mining.
5. `train.py` — CachedMNRL + Matryoshka: `train.max_steps` over all four files (`round_robin`), then `train.agent_steps` over the agent files alone. Capability files train at `loss.scale` (10), agent files at `loss.agent_scale` (50).
6. `model_soup.py` + `compare_bases.py` — sweep `soup.alphas` against the base and keep the best of the fine-tune and the blends by capability gate plus routing handoff.
7. `eval.py` (holdout), `eval_gate.py` (`eval_real`, informational here) and `eval_route.py` (does a brief reach its agent).
8. `export_onnx.py` (fp32 graph + int8-stored graph, checked against each other), then `eval_gate.py`, `eval_route.py`, `dump_scores.py` and `calibrate_cpus.py` on the graph the runtime loads.

Other flags: `--skip-build` (reuse `data/`), `--skip-export`, `--ft checkpoints/<dir>` (redo soup, eval, export, and calibration on an existing run), `--iterations N` (re-mine capability triplets from the previous round's mistakes), `--legacy` (diagnostic `model.fit` path).

### Calibrating the runtime gates

`bin/train` prints the operating points for the machine it ran on. Confirm them on every CPU kind before rollout: dump the scores once per kind, then calibrate over all dumps.

```bash
uv run python scripts/dump_scores.py --model checkpoints/<run>/onnx --out checkpoints/<run>/scores/arm64.json
uv run python scripts/calibrate_cpus.py checkpoints/<run>/scores/*.json
uv run python scripts/eval_runtime_gate.py --model checkpoints/<run>/onnx   # octomind's test fixtures, no Rust build
```

`dump_scores.py` needs only numpy, pyyaml, tokenizers and onnxruntime, so it runs in a bare container (its docstring has the Docker command for x86 on an ARM Mac). `calibrate_cpus.py` picks, per decision, the point with the best accuracy on the worst machine among those that keep false activations under the cap on every machine (capability null false-positive rate 0.03; routing wrong handoffs 0.02, foreign handoffs 0.03). Copy the values into:

- `octomind/src/mcp/runtime/capability.rs` — `AUTO_ACTIVATE_THRESHOLD`, `AUTO_ACTIVATE_MARGIN`
- `octomind/src/mcp/runtime/skill.rs` — `SEMANTIC_DEFAULT_THRESHOLD`, `SEMANTIC_MARGIN`
- `octomind/src/mcp/orchestration/tap_route.rs` — `ROUTE_THRESHOLD`, `ROUTE_MARGIN`
- `model/configs/default.yaml` — `eval.runtime_threshold`, `eval.runtime_margin`, `eval.route_threshold`, `eval.route_margin` (the publish gate and `eval_route.py` score at these)

The 2026-11 model runs at 0.68 / 0.05 for capabilities and 0.65 / 0.05 for routing, and scores identically on ARM, x86 and x86 with VNNI. The graph shipped 2026-09 quantized activations per batch and scored the same text up to 0.08 apart between ARM and x86; the per-CPU dumps are the check that this has not come back.

### Publishing

```bash
HF_TOKEN=hf_... bin/publish            # latest checkpoint; --run <dir> to choose
```

`bin/publish` runs `eval_gate.py` against `eval_baselines.json` on the fp32 weights and again on `onnx/model_quantized.onnx`, and aborts on regression (top-1 accuracy drop > 0.01, null FPR rise > 0.01, any per-capability recall drop > 0.05). It warns if `onnx/model_quantized.onnx` is missing, since the runtime prefers it. `--force`/`--skip-gate` bypass the gate for documented emergencies only; `--dry-run` prints without uploading.

Octomind's CI and every fresh install download the current weights, while an existing install keeps its cached copy (a cached HF repo is not re-checked). So publish and the octomind commit that carries the recalibrated constants go out together. After the rollout is confirmed, record the baseline the next publish gates against:

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

## Checklist

- [ ] Trigger, semantic-phrase or agent-description change → full rebuild with `--llm --resume`, not `--skip-build`?
- [ ] Training run inside tmux or nohup?
- [ ] Winner evaluated on holdout, `eval_real` and the agent briefs; ONNX graphs exported and the small one scored?
- [ ] Thresholds calibrated over dumps from every CPU kind and copied into `capability.rs`, `skill.rs`, `tap_route.rs`, and `configs/default.yaml`?
- [ ] `eval_runtime_gate.py` reports PASS for octomind's fixtures?
- [ ] `bin/publish` passed the gate without `--force`, and the octomind commit with the new constants goes out with it?
- [ ] Baseline rewritten after the rollout was confirmed?

## Composition / References

- `model/README.md` — pipeline, dataset, loss stack, eval set
- `model/configs/default.yaml` — base model, training, soup alphas, runtime-mirror constants
- `model/bin/train`, `model/bin/publish` — entry points
- `tap-capability-authoring` skill — writing triggers
