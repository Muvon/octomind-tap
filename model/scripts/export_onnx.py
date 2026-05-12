"""Export the fine-tuned sentence-transformer to ONNX for fastembed.

fastembed expects an ONNX bundle with model.onnx + tokenizer files. Optimum's
ORTModelForFeatureExtraction handles the export end-to-end. The resulting
directory can be uploaded to HuggingFace as-is and loaded by fastembed.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="sentence-transformer checkpoint dir")
    ap.add_argument("--out", type=Path, default=None, help="output dir (default: <run>/onnx)")
    ap.add_argument("--opset", type=int, default=14)
    args = ap.parse_args()

    out = args.out or (args.run / "onnx")
    out.mkdir(parents=True, exist_ok=True)

    print(f"exporting {args.run} → {out}")
    model = ORTModelForFeatureExtraction.from_pretrained(args.run, export=True)
    model.save_pretrained(out)

    tok = AutoTokenizer.from_pretrained(args.run)
    tok.save_pretrained(out)

    for fname in ("modules.json", "sentence_bert_config.json", "config_sentence_transformers.json", "1_Pooling"):
        src = args.run / fname
        if src.exists():
            dst = out / fname
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

    print("done. files:")
    for f in sorted(out.iterdir()):
        print(f"  {f.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
