# octomind-tap embedding model

Fine-tune one small ONNX bi-encoder that powers octomind's capability
auto-activation:

- **`muvon/octomind-embed`** — granite-embedding-30m-english (30M
  params, 6 layers, 384-dim, CLS-pooled, prefix-free) fine-tuned and
  blended back into the base as a WiSE-FT soup. The runtime in
  `octomind/src/mcp/runtime/capability.rs` uses it to decide which
  capability to auto-activate from a single user message via a
  mean-of-top-3 cosine score + threshold + margin gate, loading the int8
  ONNX graph (~2 ms per intent on CPU).
- Before 2026-09 the same repo held a BGE-small-en-v1.5 fine-tune. The
  base bake-off (`scripts/compare_bases.py` on the raw trigger corpus,
  each model at its own best operating point) put granite at gate 0.846
  zero-shot vs 0.708 for bge-small and 0.690 for that fine-tune, at half
  the layers. At the shipped operating point (0.65 / 0.06) the published
  soup scores gate 0.848 / fpr 0.022 on the int8 graph vs 0.778 / 0.033
  for the old fine-tune — that old-model score is what
  `eval_baselines.json` holds until the post-rollout baseline is recorded.
  New weights under the same name reach fresh installs only (hf_hub never
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

A raw fine-tune also *forgets* some of the base's generalization (top-1
and gate drop on real prompts while the margin rises). Interpolating the
fine-tuned weights with the base (WiSE-FT soup; `bin/train` sweeps
alpha 0.1-0.6 and keeps the best gate) beats both parents, so that is
what ships.

## Pipeline

    capabilities/*/config.toml  +  skills/*/SKILL.md
                       │
                       ▼
    scripts/augment_llm.py     (optional) →  data/intents.jsonl
                       │
                       ▼
    scripts/build_dataset.py   →  data/pairs.jsonl, triplets.jsonl, holdout.jsonl
                       │          raw_triggers.jsonl (what the runtime embeds)
                       │       (+ _oos sink label, multi-turn surfaces,
                       │          positive-aware hard-negative mining)
                       ▼
    scripts/train.py           →  checkpoints/embed-<run>-<ts>/
                       │       (CachedMNRL scale=10 + Matryoshka, 1 epoch)
                       ▼
    scripts/model_soup.py      →  checkpoints/embed-<run>-<ts>-soup-a<α>/
    scripts/compare_bases.py      (best gate on raw_triggers.jsonl wins)
                       ▼
    scripts/eval.py            →  holdout-distribution metrics
    scripts/eval_gate.py       →  real-user-distribution metrics  ← publish gate
                       │
                       ▼
    scripts/export_onnx.py     →  onnx/  (fp32 + int8, reduce_range from config)
    scripts/calibrate_thresholds.py --onnx-file  →  runtime τ, δ for the int8 graph
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

    # 4) Copy the calibrated τ/δ printed at the end into
    #    configs/default.yaml eval.runtime_* and octomind capability.rs /
    #    skill.rs. To re-run calibration by hand:
    uv run python scripts/calibrate_thresholds.py \
        --model checkpoints/embed-<ts>-soup-a<α>/onnx --onnx-file model_quantized.onnx

    # 5) Publish (the gate runs automatically on fp32 and int8).
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

`build_dataset.py` builds three artifacts from `capabilities/` +
`skills/`:

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
  `config.toml` triggers + skill `semantic()` phrases. This is what the
  runtime embeds, so `eval_gate.py`, `compare_bases.py` and
  `calibrate_thresholds.py` score against it (`eval.triggers_path`).

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

## Publish gate

`bin/publish` runs `eval_gate.py` against `eval_baselines.json` before
upload. Fails if:

- `top1_acc` drops more than `--top1-tol` (default 0.01)
- `null_fpr` rises more than `--fpr-tol` (default 0.01)
- any per-capability recall drops more than `--per-label-tol` (default 0.05)

Override with `bin/publish --force` only for emergencies (and record
why in the commit message).

## Runtime threshold calibration

The runtime uses two constants in
`octomind/src/mcp/runtime/capability.rs` (mirrored by
`SEMANTIC_DEFAULT_THRESHOLD` / `SEMANTIC_MARGIN` in `skill.rs`):

    const AUTO_ACTIVATE_THRESHOLD: f32 = ...;
    const AUTO_ACTIVATE_MARGIN: f32    = ...;

Every base has its own cosine scale, so the operating point moves with
each retrain. Calibrate against the int8 graph — that is what the
runtime loads, and quantization shifts cosines:

    uv run python scripts/calibrate_thresholds.py \
        --model checkpoints/<run>/onnx --onnx-file model_quantized.onnx \
        --target-fpr 0.03

Prints the Pareto front of (gate_acc, null_fpr) over a τ × δ grid and
suggests the operating point with highest gate_acc whose
`null_fpr ≤ target`. Copy the recommended constants into
`capability.rs` / `skill.rs` and into `configs/default.yaml`
`eval.runtime_threshold` / `runtime_margin` (the publish gate scores at
those values). `bin/train` runs this step automatically.

## When to retrain

You MUST retrain (and republish) whenever the supervision set changes:

| Change                                                       | Retrain? |
| ------------------------------------------------------------ | -------- |
| Added a new capability (`capabilities/<new>/config.toml`)    | yes      |
| Removed a capability                                         | yes      |
| Edited `triggers = [...]` in any `config.toml`               | yes      |
| Added or edited `semantic(...)` rules in any `SKILL.md`      | yes      |
| Edited the `_oos` curated phrases in `build_dataset.py`      | yes      |
| Pure agent / playbook / docs change, no triggers touched     | no       |
| Code change in `octomind/` runtime only                      | no       |
| Threshold/margin tweak in `capability.rs` / `skill.rs`       | no (just rebuild octomind) |

Run from `model/`:

    ANTHROPIC_API_KEY=... bin/train --llm --resume --iterations 2

`--resume` is passed to `augment_llm.py`: it skips `(label, trigger)`
pairs already paraphrased in `data/intents.jsonl`, so you only pay for
the NEW triggers. Without `--resume` you re-augment everything (same
result, costs ~$1-2 extra).

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
    bin/train --llm --resume --iterations 2
    # Ctrl+B then D to detach.  Reattach: tmux attach -t train

## Manual steps (per-stage, if you want fine control)

    uv run python scripts/build_eval_seed.py
    uv run python scripts/augment_llm.py --resume
    uv run python scripts/build_dataset.py
    uv run python scripts/build_dataset.py --neg-embed-model checkpoints/embed-<ts>  # iter 2
    uv run python scripts/train.py
    uv run python scripts/model_soup.py --base ibm-granite/granite-embedding-30m-english \
        --ft checkpoints/embed-<ts> --alphas 0.4,0.5,0.6 --out-dir checkpoints/embed-<ts>/soup
    uv run python scripts/compare_bases.py --models checkpoints/embed-<ts>,checkpoints/embed-<ts>/soup/soup-a0.6
    uv run python scripts/eval.py        --run <winner>
    uv run python scripts/eval_gate.py   --model <winner>
    uv run python scripts/export_onnx.py --run <winner>
    uv run python scripts/calibrate_thresholds.py --model <winner>/onnx --onnx-file model_quantized.onnx
    HF_TOKEN=... uv run python scripts/push_hf.py --run <winner> \
        --repo muvon/octomind-embed --type embed

## Runtime integration

Embedding model path: `octomind/src/embeddings/mod.rs` → `MODEL_NAME`.
The two-stage activation lives in
`octomind/src/mcp/runtime/capability.rs::auto_activate_capabilities_for_intent`.
