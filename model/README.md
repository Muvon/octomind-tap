# octomind-tap embedding model

Fine-tune the BGE-small-en-v1.5 base into a tap-aware semantic embedder so
capability auto-activation picks the right capability from natural language.

## Why

Off-the-shelf BGE scores generic verbs ("run", "execute") high across
unrelated capabilities. With our trigger phrases as supervision, we sharpen
the model on the actual decision the runtime makes:

    intent (user phrase)  →  capability (one of N installed)

## Pipeline

    capabilities/*/config.toml
              │
              ▼
    scripts/build_dataset.py   →  data/pairs.jsonl
              │
              ▼
    scripts/train.py           →  checkpoints/<run>/
              │
              ▼
    scripts/eval.py            →  top-1 accuracy on holdout
              │
              ▼
    scripts/export_onnx.py     →  checkpoints/<run>/onnx/
              │
              ▼
    scripts/push_hf.py         →  hf.co/<org>/octomind-tap-embed

Then point `MODEL_NAME` in `octomind/src/embeddings/mod.rs` at the new
HuggingFace path and rebuild.

## Setup

    cd model
    uv sync                     # or: pip install -e .

## Run

    uv run python scripts/build_dataset.py
    uv run python scripts/train.py --config configs/default.yaml
    uv run python scripts/eval.py  --run checkpoints/<run>
    uv run python scripts/export_onnx.py --run checkpoints/<run>
    uv run python scripts/push_hf.py --run checkpoints/<run> --repo <org>/octomind-tap-embed

## Data shape

`data/pairs.jsonl` — one JSON object per line:

    {"anchor": "<trigger phrase>", "positive": "<other trigger from same capability>", "label": "<capability-name>"}

`MultipleNegativesRankingLoss` treats all other items in the same training
batch as implicit negatives, so we don't need to mine hard negatives in the
bootstrap.

## Holdout

20% of triggers per capability are reserved for `eval.py`. The eval measures
top-1 capability retrieval over the holdout intents against the full trigger
catalog.
