"""Upload the ONNX-exported model to HuggingFace Hub.

Reads HF_TOKEN from the environment. Creates the repo if it doesn't exist.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi


CARD_TEMPLATE = """---
license: apache-2.0
base_model: BAAI/bge-small-en-v1.5
library_name: sentence-transformers
tags:
- sentence-transformers
- onnx
- fastembed
- octomind
---

# {repo}

Fine-tuned BGE-small-en-v1.5 for octomind-tap capability auto-activation.

Trained on trigger phrases from the octomind-tap capabilities catalog using
`MultipleNegativesRankingLoss`. The model sharpens semantic separation
between capability domains so the runtime can deterministically pick the
right capability for a user's intent.

## Use with fastembed

Point `MODEL_NAME` in `octomind/src/embeddings/mod.rs` at `{repo}` and
rebuild.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="checkpoint dir from train.py")
    ap.add_argument("--repo", type=str, required=True, help="<namespace>/<repo>")
    ap.add_argument("--subdir", type=str, default="onnx", help="subdir under --run to upload")
    ap.add_argument("--private", action="store_true")
    args = ap.parse_args()

    src = args.run / args.subdir
    if not src.is_dir():
        raise SystemExit(f"missing {src}; run export_onnx.py first")

    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("set HF_TOKEN env var (read+write scope)")

    api = HfApi(token=token)
    api.create_repo(args.repo, exist_ok=True, private=args.private)

    readme = src / "README.md"
    if not readme.exists():
        readme.write_text(CARD_TEMPLATE.format(repo=args.repo))

    print(f"uploading {src} → {args.repo}")
    api.upload_folder(folder_path=str(src), repo_id=args.repo, repo_type="model")
    print(f"done: https://huggingface.co/{args.repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
