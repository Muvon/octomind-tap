"""Export the fine-tuned cross-encoder reranker to ONNX.

Optional second artifact. Output goes under `<run>/onnx/`. Octomind uses
safetensors via candle today; ONNX is for ORT-based consumers.

Cross-encoders have a sequence-classification head (single relevance
score), so we use `ORTModelForSequenceClassification` instead of the
feature-extraction class used for bi-encoders.
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
