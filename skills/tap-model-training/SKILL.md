---
name: tap-model-training
title: "Octomind-Tap Embed Model Training and Publishing"
description: "Operational playbook for training, evaluating, and publishing muvon/octomind-embed, the granite-embedding-30m WiSE-FT soup that powers octomind's capability auto-activation and skill semantic() rules. Covers when to retrain (any change to capabilities/*/config.toml triggers or skills/*/SKILL.md semantic phrases), the bin/train pipeline (LLM augmentation, dataset build, hard-negative re-mining, CachedMNRL + Matryoshka fine-tune, soup sweep, holdout and eval_real evaluation, int8 ONNX export and calibration), resuming an interrupted run, calibrating the runtime threshold and margin, publishing behind the regression gate, and recording the baseline. Use when triggers or semantic rules change, when retraining or republishing the tap model, or when auto-activation picks the wrong capability."
license: Apache-2.0
compatibility: "octomind-tap repo with the model/ subdirectory. Requires Python 3.11+, uv, ANTHROPIC_API_KEY for LLM augmentation, HF_TOKEN with write scope for publishing. GPU optional."
capabilities: core
domains: octomind
rules:
  - file(model/scripts/train.py)
  - file(model/bin/train)
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

`muvon/octomind-embed` is the bi-encoder octomind uses to score a user message against capability triggers and skill `semantic()` phrases. Since 2026-09 it is `ibm-granite/granite-embedding-30m-english` (6 layers, 384-dim, CLS-pooled) given a short contrastive fine-tune and blended back into the base as a WiSE-FT soup; the runtime loads its int8 ONNX graph. Whenever triggers or semantic phrases change, the model is stale. This skill walks through retraining, calibration, publishing, and recovery.

The cross-encoder reranker is intentionally not trained or shipped: at the current capability count it does not improve routing over a well-calibrated bi-encoder.

## Mental model

The runtime decision is: intent → one installed capability, or abstain. It scores each capability as the mean of its top-3 trigger cosines and accepts the winner only if it clears an absolute threshold and beats the runner-up by a margin. The model, the trigger corpus, and those two constants are one system: retraining moves the cosine scale, so the constants must be recalibrated on the int8 graph and shipped together with the weights.

The fine-tune is a nudge. A full fine-tune forgets the base's generalization; interpolating fine-tuned and base weights beats both parents, so `bin/train` sweeps the soup alpha and ships the best gate.

## Rules

### When to retrain

| Change | Retrain? |
|--------|----------|
| Added or removed a capability (`capabilities/<name>/config.toml`) | yes |
| Edited `triggers = [...]` | yes |
| Added or edited `semantic(...)` rules in any `SKILL.md` | yes |
| Edited the `_oos` curated phrases in `build_dataset.py` | yes |
| Agent, skill body, or docs change with no trigger touched | no |
| Threshold/margin change in octomind `capability.rs` / `skill.rs` | no — rebuild octomind |

### Standard retrain flow

Run from `model/`, inside `tmux` or `nohup` so a dropped connection doesn't kill it:

```bash
cd model && uv sync
tmux new -s train
ANTHROPIC_API_KEY=... bin/train --llm --resume --iterations 2
```

What runs (`bin/train`):

1. `build_eval_seed.py` once, if `data/eval_real.jsonl` is missing.
2. `augment_llm.py --resume` — LLM paraphrases for new `(label, trigger)` pairs only, appended to `data/intents.jsonl`.
3. `build_dataset.py` — `pairs.jsonl`, `triplets.jsonl`, `holdout.jsonl`, and `raw_triggers.jsonl` (the un-augmented corpus the runtime actually embeds), with the `_oos` sink label, multi-turn surfaces, and hard-negative mining.
4. `train.py` — CachedMNRL (scale 10) + Matryoshka, one epoch capped by `train.max_steps`; with `--iterations N`, triplets are re-mined from the previous round's mistakes between rounds.
5. `model_soup.py` + `compare_bases.py` — sweep `soup.alphas` against the base and keep the best gate on `raw_triggers.jsonl`.
6. `eval.py` (holdout) and `eval_gate.py` (`eval_real`, informational here).
7. `export_onnx.py` (fp32 + int8), then `eval_gate.py` and `calibrate_thresholds.py --target-fpr 0.03` on the int8 graph.

Other flags: `--skip-build` (reuse `data/`), `--skip-export`, `--ft checkpoints/<dir>` (redo soup, eval, export, and calibration on an existing run), `--legacy` (diagnostic `model.fit` path).

### Calibrating the runtime gate

`bin/train` prints the recommended operating point. To rerun by hand:

```bash
uv run python scripts/calibrate_thresholds.py \
  --model checkpoints/<run>/onnx --onnx-file model_quantized.onnx --target-fpr 0.03
```

It sweeps τ × δ over `data/eval_real.jsonl` and recommends the highest gate accuracy with null false-positive rate under the target. Copy the values into:

- `octomind/src/mcp/runtime/capability.rs` — `AUTO_ACTIVATE_THRESHOLD`, `AUTO_ACTIVATE_MARGIN`
- `octomind/src/mcp/runtime/skill.rs` — `SEMANTIC_DEFAULT_THRESHOLD`, `SEMANTIC_MARGIN`
- `model/configs/default.yaml` — `eval.runtime_threshold`, `eval.runtime_margin` (the publish gate scores at these)

The shipped soup runs at 0.65 / 0.06. Calibrate on the int8 graph: quantization shifts cosines, and that graph is what users load.

### Publishing

```bash
HF_TOKEN=hf_... bin/publish            # latest checkpoint; --run <dir> to choose
```

`bin/publish` runs `eval_gate.py` against `eval_baselines.json` on the fp32 weights and again on the int8 graph, and aborts on regression (top-1 accuracy drop > 0.01, null FPR rise > 0.01, any per-capability recall drop > 0.05). It warns if `onnx/model_quantized.onnx` is missing, since the runtime prefers it. `--force`/`--skip-gate` bypass the gate for documented emergencies only; `--dry-run` prints without uploading.

New weights reach fresh installs only — a cached HF repo is not re-checked — so ship the recalibrated octomind constants in the same release. After the rollout is confirmed, record the baseline the next publish gates against:

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

✅ `bin/train --llm --resume --iterations 2` — rebuild, augment only the new triggers, retrain.

### Example 2: wrong capability wins but triggers look right

Retraining rarely fixes this. First run `calibrate_thresholds.py` to see whether the shipped τ/δ still fit the model; add the failing prompt to `data/eval_real.jsonl` with its correct label and rerun `eval_gate.py`; then compare the competing capabilities' triggers — shared generic vocabulary is fixed by differentiating triggers, not by more training.

### Example 3: publishing without a baseline update

Publishing and forgetting `--write-baseline` leaves the next publish gating against the previous model, so a later regression can slip through. Record the baseline once the rollout is confirmed.

## Checklist

- [ ] Trigger or semantic-phrase change → full rebuild with `--llm --resume`, not `--skip-build`?
- [ ] Training run inside tmux or nohup?
- [ ] Soup winner evaluated on holdout and `eval_real`, int8 graph exported and scored?
- [ ] τ/δ calibrated on the int8 graph and copied into `capability.rs`, `skill.rs`, and `configs/default.yaml`?
- [ ] `bin/publish` passed the gate without `--force`, and the octomind release carries the new constants?
- [ ] Baseline rewritten after the rollout was confirmed?

## Composition / References

- `model/README.md` — pipeline, dataset, loss stack, eval set
- `model/configs/default.yaml` — base model, training, soup alphas, export, runtime-mirror constants
- `model/bin/train`, `model/bin/publish` — entry points
- `tap-capability-authoring` skill — writing triggers
