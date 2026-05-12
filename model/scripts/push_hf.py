"""Upload an ONNX-exported model (embedding or reranker) to HuggingFace Hub.

Reads HF_TOKEN from the environment. Creates the repo if it doesn't exist.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


EMBED_CARD = """---
license: apache-2.0
base_model: BAAI/bge-small-en-v1.5
library_name: sentence-transformers
tags:
- sentence-transformers
- onnx
- fastembed
- octomind
- embeddings
---

# {repo}

Fine-tuned BGE-small-en-v1.5 (33M params, 384-dim) for octomind capability
auto-activation.

Trained on trigger phrases from the octomind-tap capabilities catalog with
rule-based + LLM paraphrase augmentation, using `MultipleNegativesRankingLoss`
on both in-capability pairs and hard-negative triplets mined from
confusable neighboring capabilities.

## Use with fastembed

Point `MODEL_NAME` in `octomind/src/embeddings/mod.rs` at `{repo}` and rebuild.

## Paired reranker

For higher precision use the matching reranker `muvon/octomind-rerank`
as a second stage after this model's retrieval.
"""

RERANK_CARD = """---
license: apache-2.0
base_model: jinaai/jina-reranker-v1-turbo-en
library_name: sentence-transformers
tags:
- cross-encoder
- onnx
- fastembed
- octomind
- reranker
---

# {repo}

Fine-tuned Jina reranker v1 turbo (33M params, English) for octomind
capability auto-activation. Designed as the second stage after the
`muvon/octomind-embed` bi-encoder retrieves the top-N candidates.

Trained with `BinaryCrossEntropyLoss` over (anchor, positive) and
(anchor, hard_negative) pairs derived from the octomind-tap capabilities
catalog. The hard negatives target the specific confusable neighbors the
bi-encoder cannot reliably separate alone (e.g. shell vs programming-rust).

## Use with fastembed

Wired in via `octolib::reranker` with `RerankProviderType::FastEmbed`.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="checkpoint dir from train.py or train_reranker.py")
    ap.add_argument("--repo", type=str, required=True, help="<namespace>/<repo>")
    ap.add_argument("--subdir", type=str, default="onnx", help="subdir under --run to upload")
    ap.add_argument("--type", choices=["embed", "rerank"], default="embed",
                    help="model type (selects model card template)")
    ap.add_argument("--private", action="store_true")
    args = ap.parse_args()

    src = args.run / args.subdir
    if not src.is_dir():
        raise SystemExit(f"missing {src}; run export_onnx{'_reranker' if args.type == 'rerank' else ''}.py first")

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("set HF_TOKEN env var (read+write scope)")

    api = HfApi(token=token)
    api.create_repo(args.repo, exist_ok=True, private=args.private)

    readme = src / "README.md"
    if not readme.exists():
        template = RERANK_CARD if args.type == "rerank" else EMBED_CARD
        readme.write_text(template.format(repo=args.repo))

    print(f"uploading {src} → {args.repo}")
    api.upload_folder(folder_path=str(src), repo_id=args.repo, repo_type="model")
    print(f"done: https://huggingface.co/{args.repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
