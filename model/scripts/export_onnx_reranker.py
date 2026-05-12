"""Export a fine-tuned cross-encoder reranker to ONNX for fastembed.

Cross-encoders have a different output head than bi-encoders (a single
relevance score, not a sentence embedding), so they need their own export
script. Uses optimum's `ORTModelForSequenceClassification`.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="cross-encoder checkpoint dir")
    ap.add_argument("--out", type=Path, default=None, help="output dir (default: <run>/onnx)")
    ap.add_argument("--opset", type=int, default=14)
    args = ap.parse_args()

    out = args.out or (args.run / "onnx")
    out.mkdir(parents=True, exist_ok=True)

    print(f"exporting {args.run} → {out}")
    model = ORTModelForSequenceClassification.from_pretrained(args.run, export=True)
    model.save_pretrained(out)

    tok = AutoTokenizer.from_pretrained(args.run)
    tok.save_pretrained(out)

    # Cross-encoders sometimes ship a CECorrelationEvaluator config — copy
    # anything that exists so the HF repo is self-contained.
    for fname in ("config.json", "tokenizer_config.json", "special_tokens_map.json"):
        src = args.run / fname
        if src.exists() and not (out / fname).exists():
            shutil.copy2(src, out / fname)

    print("done. files:")
    for f in sorted(out.iterdir()):
        print(f"  {f.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
