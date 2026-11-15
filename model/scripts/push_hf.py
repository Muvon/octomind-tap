"""Upload a trained checkpoint (embedding or reranker) to HuggingFace Hub.

Pushes the checkpoint root as-is, which contains:
  - `model.safetensors` + `config.json` + tokenizer  (consumed by octomind
    today via octolib's candle-based HuggingFace provider)
  - `onnx/`                                          (optional, present if
    export_onnx.py / export_onnx_reranker.py was run; available for any
    ORT-based consumer — fastembed user-defined, edge runtimes, etc.)

Both formats live in the same HF repo so consumers can pick.

Reads HF_TOKEN from the environment. Creates the repo if missing.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


EMBED_CARD = """---
license: apache-2.0
base_model: ibm-granite/granite-embedding-30m-english
library_name: sentence-transformers
tags:
- sentence-transformers
- octomind
- embeddings
- roberta
- onnx
---

# {repo}

Embedding model for two octomind decisions: which capability or skill to
activate for a user message, and which agent takes a delegated task.
`ibm-granite/granite-embedding-30m-english` (30M params, 6 layers, 384-dim,
CLS-pooled, prefix-free, English) fine-tuned on the octomind-tap catalog
(capability and skill trigger phrases, agent titles and descriptions).

Training: rule-based + LLM paraphrase augmentation for triggers, LLM-written
task briefs for agents, `CachedMultipleNegativesRankingLoss` (scale 10 for
triggers, 50 for agents) on pairs and positive-aware hard-negative triplets,
`MatryoshkaLoss` over [384, 256, 192, 128, 96]. Two phases: 105 steps over
all files, then 105 steps over the agent files alone.

## Files

- `model.safetensors` + `1_Pooling/` — sentence-transformers layout (fp32).
- `onnx/model.onnx` — fp32 graph.
- `onnx/model_quantized.onnx` — the same graph with its weight matrices stored
  as int8 (one scale per channel) and restored to fp32 by constant nodes, so
  the arithmetic is fp32; this is what the octomind runtime loads. Pool with
  CLS as declared in `1_Pooling/config.json`.

## Use

octomind loads `onnx:{repo}` via octolib's ONNX provider (`MODEL_NAME` in
`octomind/src/embeddings/mod.rs`). Runtime thresholds are model-specific and
calibrated against `onnx/model_quantized.onnx` (`AUTO_ACTIVATE_THRESHOLD` /
`_MARGIN` in `capability.rs`, `SEMANTIC_*` in `skill.rs`, `ROUTE_*` in
`tap_route.rs`).
"""

RERANK_CARD = """---
license: apache-2.0
base_model: cross-encoder/ms-marco-MiniLM-L-6-v2
library_name: sentence-transformers
tags:
- cross-encoder
- octomind
- reranker
- bert
---

# {repo}

Fine-tuned MS-MARCO MiniLM-L-6 cross-encoder (22M params, English) for
octomind capability auto-activation. Designed as the second stage after
the `muvon/octomind-embed` bi-encoder retrieves the top-N candidates.

Trained with `BinaryCrossEntropyLoss` over (anchor, positive) and
(anchor, hard_negative) pairs from the octomind-tap catalog. The hard
negatives target the confusable neighbors the bi-encoder alone cannot
reliably separate.

## Use

Wired into octomind via octolib's HuggingFace reranker provider (candle
backend).
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="checkpoint dir from train.py or train_reranker.py")
    ap.add_argument("--repo", type=str, required=True, help="<namespace>/<repo>")
    ap.add_argument("--type", choices=["embed", "rerank"], required=True,
                    help="model type — selects the model-card template")
    ap.add_argument("--private", action="store_true")
    args = ap.parse_args()

    if not args.run.is_dir():
        raise SystemExit(f"checkpoint dir not found: {args.run}")
    if not (args.run / "model.safetensors").exists():
        raise SystemExit(f"missing model.safetensors in {args.run} — is this a trained checkpoint?")

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("set HF_TOKEN env var (read+write scope)")

    api = HfApi(token=token)
    api.create_repo(args.repo, exist_ok=True, private=args.private)

    readme = args.run / "README.md"
    template = RERANK_CARD if args.type == "rerank" else EMBED_CARD
    readme.write_text(template.format(repo=args.repo))

    print(f"uploading {args.run} → {args.repo}")
    api.upload_folder(
        folder_path=str(args.run),
        repo_id=args.repo,
        repo_type="model",
        # soup/ and scores/ are what bin/train leaves inside the run dir: the
        # blends it compared (one full model each) and the per-CPU score dumps.
        # training_args.bin is a pickle holding the training machine's paths.
        ignore_patterns=[
            "train_config.yaml", "training_args.bin", "checkpoint-*", "runs/", "*.log", "soup/", "scores/",
        ],
    )
    print(f"done: https://huggingface.co/{args.repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
