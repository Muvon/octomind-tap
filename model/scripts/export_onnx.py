"""Export the fine-tuned sentence-transformer to ONNX (fp32 + static int8).

Octomind's runtime can load this checkpoint two ways:

  - `hf:muvon/octomind-embed`   → candle reads `model.safetensors` (fp32)
  - `onnx:muvon/octomind-embed` → ORT reads `onnx/*.onnx` (this script)

The ONNX path is the fast one: ORT's fused int8 kernels are typically 2-4x
quicker on CPU than candle fp32, at roughly a quarter of the on-disk size.
octolib's provider probes `onnx/model_quantized.onnx` BEFORE `onnx/model.onnx`,
so publishing both means every consumer gets int8 by default while the fp32
graph stays available for anyone who pins it explicitly.

Quantization is WEIGHT-ONLY int8, never activation-dynamic. Dynamic activation
quantization recalculates ranges per batch, which makes a vector depend on what
else was in its batch; fastembed refuses to batch such graphs at all. Weight-only
quantization keeps activations fp32, so embeddings stay batch-invariant.

Output layout under `<run>/onnx/`:

    model.onnx              fp32 graph
    model_quantized.onnx    int8 graph (preferred by the runtime)
    tokenizer.json, config.json, special_tokens_map.json,
    tokenizer_config.json, 1_Pooling/ …

`1_Pooling/config.json` is copied deliberately: the ONNX provider reads it to
decide mean vs CLS pooling. Without it the provider assumes mean — correct for
this model today, but silently wrong for any future CLS-pooled checkpoint.

Verify a quantized export before publishing:

    uv run python scripts/eval_gate.py --model <run>/onnx --onnx-file model_quantized.onnx
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import yaml

from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

# Files the ONNX provider (and sentence-transformers) look for beside the graph.
SIDECAR_FILES = (
    "modules.json",
    "sentence_bert_config.json",
    "config_sentence_transformers.json",
    "1_Pooling",
)


def quantize_int8(out: Path, src_name: str = "model.onnx", reduce_range: bool = False) -> Path | None:
    """Produce `model_quantized.onnx` next to the fp32 graph.

    Returns the path on success, or None if the quantization extras aren't
    installed — the fp32 export stays valid either way.
    """
    try:
        from onnxruntime.quantization import QuantType, quantize_dynamic
    except ImportError as exc:  # pragma: no cover - environment dependent
        print(f"  int8 skipped — onnxruntime.quantization unavailable ({exc})")
        print("  install with: uv add 'optimum[onnxruntime]'")
        return None

    src = out / src_name
    if not src.exists():
        print(f"  int8 skipped — {src_name} not found")
        return None

    dst = out / "model_quantized.onnx"
    print("  quantizing → int8 weights (per-channel, activations left fp32)")

    # Despite the name, `quantize_dynamic` with weight_type=QInt8 and
    # per_channel=True quantizes WEIGHTS only; activations are computed in fp32
    # and re-quantized per operator, so the output does not depend on batch
    # composition. That is what keeps this graph safe to batch.
    quantize_dynamic(
        model_input=str(src),
        model_output=str(dst),
        weight_type=QuantType.QInt8,
        per_channel=True,
        reduce_range=reduce_range,
        extra_options={"MatMulConstBOnly": True},
    )
    return dst


def copy_sidecars(run: Path, out: Path) -> None:
    for fname in SIDECAR_FILES:
        src = run / fname
        if not src.exists():
            continue
        dst = out / fname
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)


def warn_if_pooling_missing(out: Path) -> None:
    """The provider's pooling default is mean; make a mismatch loud, not silent."""
    pooling_cfg = out / "1_Pooling" / "config.json"
    if not pooling_cfg.exists():
        print("  WARNING: no 1_Pooling/config.json — ONNX consumers will assume MEAN pooling")
        return
    try:
        cfg = json.loads(pooling_cfg.read_text())
        mode = cfg.get("pooling_mode") or ("cls" if cfg.get("pooling_mode_cls_token") else None)
    except (OSError, json.JSONDecodeError):
        return
    if mode and mode.lower() != "mean":
        print(f"  NOTE: checkpoint pools with '{mode}' — octolib reads this from 1_Pooling")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="sentence-transformer checkpoint dir")
    ap.add_argument("--out", type=Path, default=None, help="output dir (default: <run>/onnx)")
    ap.add_argument("--opset", type=int, default=14)
    ap.add_argument(
        "--config", type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml",
        help="read export.reduce_range from here unless --reduce-range is given",
    )
    ap.add_argument(
        "--reduce-range",
        action="store_true",
        help="int8 with 7-bit weight range. Artifact-specific: on the 2026-09 raw-corpus "
             "gate it rescued the untrained granite base (0.747 → 0.837) but hurt the "
             "shipped granite soup (0.848 → 0.785) and bge-small (0.717 → 0.651) — "
             "always re-score the int8 graph before publishing.",
    )
    ap.add_argument(
        "--no-quantize",
        action="store_true",
        help="export fp32 only (skip the int8 graph the runtime prefers)",
    )
    args = ap.parse_args()
    reduce_range = args.reduce_range
    if not reduce_range and args.config.exists():
        reduce_range = bool(yaml.safe_load(args.config.read_text()).get("export", {}).get("reduce_range", False))
    print(f"int8 reduce_range={reduce_range}")

    out = args.out or (args.run / "onnx")
    out.mkdir(parents=True, exist_ok=True)

    print(f"exporting {args.run} → {out}")
    model = ORTModelForFeatureExtraction.from_pretrained(args.run, export=True)
    model.save_pretrained(out)

    tok = AutoTokenizer.from_pretrained(args.run)
    tok.save_pretrained(out)

    copy_sidecars(args.run, out)
    warn_if_pooling_missing(out)

    if not args.no_quantize:
        quantize_int8(out, reduce_range=reduce_range)

    print("done. files:")
    for f in sorted(out.iterdir()):
        if f.is_file():
            print(f"  {f.name}  ({f.stat().st_size / (1024 * 1024):.1f} MB)")
        else:
            print(f"  {f.name}/")

    print()
    print("Runtime picks onnx/model_quantized.onnx first. Verify before publishing:")
    print(f"  uv run python scripts/eval_gate.py --model {out} --onnx-file model_quantized.onnx")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
