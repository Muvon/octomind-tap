---
name: octomind-tap-training
title: "octomind-tap: train and publish the embed model"
description: "Operational playbook for training, evaluating, and publishing `muvon/octomind-embed` — the BGE-small-en-v1.5 fine-tune that powers octomind's capability auto-activation. Covers when to retrain (after any change to `capabilities/*/config.toml` triggers or `skills/*/SKILL.md` semantic phrases), the full pipeline (LLM augmentation, dataset build, iterative hard-negative mining, CachedMNRL + GISTEmbed + Matryoshka loss stack, holdout + eval_real evaluation, ONNX export, HuggingFace publish), how to resume an interrupted training, how to calibrate the runtime threshold/margin from eval_real, and how to update the publish baseline. Use whenever the user adds/removes/edits capability triggers or skill semantic rules, asks about retraining the tap model, or reports false-positive/false-negative auto-activation issues."
license: Apache-2.0
compatibility: "octomind-tap repo with `model/` subdirectory. Requires Python 3.11+ (for onnxruntime wheels), `uv` for dependency management, ANTHROPIC_API_KEY for LLM augmentation, HF_TOKEN with read+write scope for publish, and ~30min-6h compute (GPU vs CPU) per training run."
capabilities: core
domains: developer
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
  - match(\b(eval_gate|eval_real|build_dataset|build_eval_seed|calibrate_thresholds)\b)
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

## What this skill is for

`muvon/octomind-embed` is the bi-encoder that decides which capability
auto-activates from a user's prompt. It is fine-tuned from
BGE-small-en-v1.5 on the triggers authored in `capabilities/*/config.toml`
and the `semantic(phrase)` rules in `skills/*/SKILL.md`.

Whenever those source files change, the model is stale. This skill walks
through the retrain-and-publish loop and the recovery paths.

The cross-encoder reranker (`muvon/octomind-rerank`) is **intentionally
not maintained**. Production validation showed it doesn't help at the
current capability count (~75 labels); the bi-encoder + a well-tuned
runtime gate is the production path.

## When to retrain

You MUST retrain (and republish) when the supervision set changes:

| Change                                                       | Retrain? |
| ------------------------------------------------------------ | -------- |
| Added `capabilities/<new>/config.toml`                       | yes      |
| Removed a capability                                         | yes      |
| Edited `triggers = [...]` in any `config.toml`               | yes      |
| Added or edited `semantic(...)` rules in any `SKILL.md`      | yes      |
| Edited `_oos` curated phrases in `build_dataset.py`          | yes      |
| Agent/playbook/docs change with no trigger touched           | no       |
| Code change in `octomind/` runtime only                      | no       |
| Threshold/margin tweak in `capability.rs` / `skill.rs`       | no (just rebuild octomind) |

## Standard retrain flow

ALWAYS run inside `tmux` or `nohup` — sessions get disconnected.

```bash
cd model
uv sync  # if env not warm

tmux new -s train
ANTHROPIC_API_KEY=sk-ant-... bin/train --llm --resume --iterations 2
# Ctrl+B then D to detach. Reattach with: tmux attach -t train
```

What runs:

1. `augment_llm.py --resume` — paraphrases ONLY the new `(label, trigger)`
   pairs against `data/intents.jsonl`. Skips already-augmented ones.
   Cost: ~$0.10–$2 depending on how many new triggers. Time: 3–5 min.
2. `build_dataset.py` — rebuilds `pairs.jsonl`, `triplets.jsonl`,
   `holdout.jsonl` from `capabilities/` + `skills/` + LLM intents + OOS
   sink + multi-turn surfaces + realistic typo augmentation.
3. Train iter 1 with CachedMNRL + GISTEmbed + Matryoshka. ~3-6h on
   GPU, 6-12h on CPU.
4. Re-mine triplets with iter-1 model (retrieval-aligned + NV-Retriever
   positive-aware filter).
5. Train iter 2. Same time as iter 1.
6. `eval.py` against holdout (in-distribution).
7. `eval_gate.py` against `data/eval_real.jsonl` (real-user
   distribution — informational at this step, blocks at publish).
8. `export_onnx.py` — produces `checkpoints/embed-<ts>/onnx/` for
   ORT-based consumers.

When it finishes, publish:

```bash
HF_TOKEN=hf_... bin/publish
```

`bin/publish` runs `eval_gate.py` against `eval_baselines.json` first
and aborts on regression (top1_acc drops >1pt, null_fpr rises >1pt, any
per-cap recall drops >5pts). Use `--force` only for documented
emergencies.

After production rollout, record the new baseline so the NEXT publish
gates against it:

```bash
uv run python scripts/eval_gate.py --model muvon/octomind-embed \
    --write-baseline eval_baselines.json
```

## Resuming an interrupted training

SentenceTransformerTrainer auto-checkpoints at the end of each epoch
(`save_strategy="epoch"`, `save_total_limit=2`). Recovery:

```bash
# 1. check what got saved
ls checkpoints/embed-*/checkpoint-*
```

If you see `checkpoint-N/` dirs, there's state. Resume:

```bash
uv run python scripts/train.py --resume
```

That picks the latest `checkpoints/embed-*/` dir and continues from the
highest-numbered `checkpoint-N`. Use `--resume-from <path>` for an
explicit run dir.

Mid-iter-1 interruption — finish iter 1, then continue iter 2 manually:

```bash
# 1. finish iter 1
uv run python scripts/train.py --resume

# 2. re-mine triplets with iter-1 model
ITER1=$(ls -td checkpoints/embed-*/ | head -1 | sed 's:/$::')
uv run python scripts/build_dataset.py --neg-embed-model "$ITER1"

# 3. train iter 2 fresh
uv run python scripts/train.py

# 4. eval + export
ITER2=$(ls -td checkpoints/embed-*/ | head -1 | sed 's:/$::')
uv run python scripts/eval.py        --run "$ITER2"
uv run python scripts/eval_gate.py   --model "$ITER2"
uv run python scripts/export_onnx.py --run "$ITER2"
```

`--resume` works only for the modern `train.py` path (CachedMNRL +
GIST + Matryoshka). `--legacy` has no checkpoint-resume.

## Calibrating the runtime gate

After every retrain, recalibrate the runtime threshold/margin against
eval_real:

```bash
RUN=$(ls -td model/checkpoints/embed-*/ | head -1 | sed 's:/$::')
uv run python model/scripts/calibrate_thresholds.py --model "$RUN" --target-fpr 0.05
```

It sweeps τ × δ over `data/eval_real.jsonl`, prints the Pareto front,
and recommends the operating point with highest gate_acc whose
null_fpr ≤ target. Copy-paste the recommended constants into:

- `octomind/src/mcp/core/capability.rs:772` → `AUTO_ACTIVATE_THRESHOLD`
- `octomind/src/mcp/core/capability.rs:781` → `AUTO_ACTIVATE_MARGIN`
- `octomind/src/mcp/core/skill.rs:66`       → `SEMANTIC_DEFAULT_THRESHOLD`
- `octomind/src/mcp/core/skill.rs:78`       → `SEMANTIC_MARGIN`

The threshold often drops after fine-tuning (0.55 → ~0.45) because the
FT model puts every matched positive well above the floor; the margin
becomes the binding constraint, not the floor.

## Common mistakes

1. Using `--skip-build` when triggers changed. The build is what
   converts new triggers into training surfaces. `--skip-build` reuses
   the previous `pairs.jsonl`, so new triggers don't show up in the
   training set, and the resulting checkpoint inherits the old
   weaknesses. The new run is wasted compute. Always rebuild after a
   catalog change.

2. Forgetting `--llm` after adding triggers. `--llm` is what kicks off
   `augment_llm.py` to generate user-style paraphrases of the new
   triggers. Without it, the new triggers only get rule-template
   expansion, which is much narrower. Use `--llm --resume` to skip
   already-paraphrased triggers.

3. Running outside tmux/nohup. Long training (5h+) over SSH dies when
   the connection drops. Always wrap in tmux or nohup.

4. Skipping the publish gate. `bin/publish --force` exists for
   emergencies. Don't use it as habit — silent regressions ship.

5. Not recording the new baseline after promotion. If you don't run
   `eval_gate.py --write-baseline` after a successful publish, the
   next publish has nothing to gate against and any future regression
   slips through.

6. Editing trigger lists without thinking about overlap. When two
   capabilities share vocabulary (e.g. all `messaging-*`, all
   `legal-*`, `webfetch` vs `scraping`), the model gets confused. Use
   PLATFORM-specific or JURISDICTION-specific vocabulary in each cap's
   triggers — not the same generic verbs across the family.

## Key files

- `model/bin/train` — full pipeline entrypoint.
- `model/bin/publish` — gate-protected HF upload.
- `model/configs/default.yaml` — loss stack, batch sizes, eval paths.
- `model/scripts/build_dataset.py` — surface generation, OOS sink,
  multi-turn, typo aug, hard-negative mining.
- `model/scripts/train.py` — modern trainer (CachedMNRL + GIST +
  Matryoshka) + `--resume` flag.
- `model/scripts/eval_gate.py` — publish-time regression gate.
- `model/scripts/calibrate_thresholds.py` — runtime τ/δ sweep.
- `model/scripts/build_eval_seed.py` — frozen real-user eval set
  generator. Hand-edit `data/eval_real.jsonl` to add production-observed
  failure modes.
- `model/eval_baselines.json` — recorded baseline; the publish gate
  reads this.
- `model/data/intents.jsonl` — LLM paraphrases. `augment_llm.py
  --resume` skips entries already here.

## When NOT to retrain

If the symptom is "auto-activation picks the wrong capability for X but
the triggers are correct", retraining usually won't fix it. Three other
levers first:

1. Run `calibrate_thresholds.py` to see if the current τ/δ in the
   Rust constants matches the FT model's distribution.
2. Add the failing prompt to `data/eval_real.jsonl` with the correct
   label, then re-run `eval_gate.py` to confirm it's an actual model
   problem and not an eval-distribution gap.
3. Check the trigger lists for the competing capabilities — if two
   neighbors share generic vocabulary, the fix is differentiating
   triggers, not retraining alone.

Retrain when the triggers themselves change, not when production
behavior is unexpected.
