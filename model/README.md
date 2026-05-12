# octomind-tap embedding + reranker

Fine-tune two small ONNX models that power octomind's capability auto-activation:

- **`muvon/octomind-embed`** — BGE-small-en-v1.5 fine-tune (33M, 384-dim). First-stage bi-encoder retrieval.
- **`muvon/octomind-rerank`** — Jina-reranker-v1-turbo-en fine-tune (33M, English). Second-stage cross-encoder reranker.

## Why

Off-the-shelf BGE scores generic verbs ("run", "execute") high across
unrelated capabilities, so capabilities with shared vocabulary (shell vs
programming-rust) cluster too close to clear the runtime margin gate.

With trigger-phrase supervision plus hard-negative mining, we sharpen the
embedding on the actual decision the runtime makes:

    intent (user phrase)  →  capability (one of N installed)

The reranker is a second, more precise pass on the bi-encoder's top-5 that
typically widens top1/top2 by 2-5x.

## Pipeline

    capabilities/*/config.toml  +  skills/*/SKILL.md
                       │
                       ▼
    scripts/augment_llm.py     (optional) →  data/intents.jsonl
                       │
                       ▼
    scripts/build_dataset.py   →  data/pairs.jsonl, triplets.jsonl, holdout.jsonl
                       │
       ┌───────────────┴───────────────┐
       ▼                               ▼
    scripts/train.py            scripts/train_reranker.py
       │                               │
       ▼                               ▼
    scripts/eval.py             scripts/eval_reranker.py
       │                               │
       ▼                               ▼
    scripts/export_onnx.py      scripts/export_onnx_reranker.py
       │                               │
       ▼                               ▼
    scripts/push_hf.py          scripts/push_hf.py --type rerank
       │                               │
       ▼                               ▼
    hf.co/muvon/octomind-embed  hf.co/muvon/octomind-rerank

Each HF repo holds BOTH formats:
- `model.safetensors` + config + tokenizer at the root → consumed by octomind today via octolib's candle-based HuggingFace provider.
- `onnx/` subdir → available for ORT-based consumers (fastembed user-defined, edge runtimes, browser onnxruntime-web).

`bin/train` runs both training and export by default. Use `--skip-export`
to skip ONNX export if you don't need it.

## Setup

    cd model
    uv sync

## One-shot pipelines

    bin/train                       # bi-encoder only
    bin/train --reranker            # reranker only (reuses existing dataset)
    bin/train --all                 # both
    bin/train --llm --all           # deep: LLM-augment + train both
    bin/train --llm --resume        # resume an interrupted LLM augmentation run

Each pipeline prints a base-vs-fine-tuned comparison so you can verify the
fine-tune actually improved precision before exporting.

## Manual steps

    uv run python scripts/build_dataset.py
    uv run python scripts/train.py
    uv run python scripts/train_reranker.py
    uv run python scripts/eval.py          --run checkpoints/embed-<ts>
    uv run python scripts/eval_reranker.py --run checkpoints/rerank-<ts>
    uv run python scripts/export_onnx.py           --run checkpoints/embed-<ts>
    uv run python scripts/export_onnx_reranker.py  --run checkpoints/rerank-<ts>
    HF_TOKEN=... uv run python scripts/push_hf.py --run checkpoints/embed-<ts>  --repo muvon/octomind-embed
    HF_TOKEN=... uv run python scripts/push_hf.py --run checkpoints/rerank-<ts> --repo muvon/octomind-rerank --type rerank

## Data shape

- `pairs.jsonl`    — `{anchor, positive, label}` from same-capability triggers (with paraphrase expansion).
- `triplets.jsonl` — `{anchor, positive, negative, label, neg_label}` with hard negatives mined from base-model centroid neighbors.
- `holdout.jsonl`  — held-out trigger paraphrases per capability for eval.
- `intents.jsonl`  — (optional) LLM-generated natural user paraphrases. Produced by `augment_llm.py`; auto-loaded by `build_dataset.py` if present.

## Runtime integration

Embedding model path: `octomind/src/embeddings/mod.rs` → `MODEL_NAME`.
Reranker is wired through `octolib::reranker` with the FastEmbed provider.
The two-stage activation lives in `src/mcp/core/capability.rs::auto_activate_capabilities_for_intent`.
