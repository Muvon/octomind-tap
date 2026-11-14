"""Export the fine-tuned sentence-transformer to ONNX: an fp32 graph and a
quarter-size graph whose weights are stored as int8.

Octomind's runtime can load this checkpoint two ways:

  - `hf:muvon/octomind-embed`   → candle reads `model.safetensors` (fp32)
  - `onnx:muvon/octomind-embed` → ORT reads `onnx/*.onnx` (this script)

octolib's provider probes `onnx/model_quantized.onnx` BEFORE `onnx/model.onnx`,
so publishing both means every consumer downloads the small graph by default
while the fp32 graph stays available for anyone who pins it explicitly.

The small graph compresses STORAGE only. Each large weight matrix is kept as
int8 with one scale per channel, and two constant nodes (Cast, Mul) turn it
back into fp32; onnxruntime folds them when it loads the graph, so every
operator still computes in fp32. Measured 2026-11 on a granite soup:

  - the vectors match the fp32 graph (cosine 0.9996 on average);
  - a text gets the same vector alone or inside a batch;
  - ARM, x86 and x86 with VNNI give the same scores to four decimals;
  - 30 MB against 121 MB, at the fp32 graph's speed.

Until 2026-11 this script called onnxruntime's `quantize_dynamic`, which also
quantizes the activations, with a range taken from the whole batch. That graph
moved the vectors away from fp32 (cosine 0.973 on average), gave a text a
different vector depending on what else was in its batch (cosine 0.986), and
scored the same text up to 0.08 apart on ARM and x86, which is how a routing
test passed on a Mac and failed on CI. It was no faster on the short texts the
runtime embeds.

Output layout under `<run>/onnx/`:

    model.onnx              fp32 graph
    model_quantized.onnx    int8-stored weights, fp32 arithmetic (preferred by the runtime)
    tokenizer.json, config.json, special_tokens_map.json,
    tokenizer_config.json, 1_Pooling/ …

`1_Pooling/config.json` is copied deliberately: the ONNX provider reads it to
decide mean vs CLS pooling. Without it the provider assumes mean — correct for
this model today, but silently wrong for any future CLS-pooled checkpoint.

Verify the small graph before publishing:

    uv run python scripts/eval_gate.py --model <run>/onnx --onnx-file model_quantized.onnx
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

# Files the ONNX provider (and sentence-transformers) look for beside the graph.
SIDECAR_FILES = (
    "modules.json",
    "sentence_bert_config.json",
    "config_sentence_transformers.json",
    "1_Pooling",
)

# Weight matrices below this many elements stay fp32: together they are a few
# hundred kilobytes, and position embeddings and biases are among them.
MIN_QUANTIZED_ELEMENTS = 100_000

# Symmetric int8: the range is -127..127 so that zero stays exactly zero.
INT8_PEAK = 127

# Lowest cosine between a text's vector from the small graph and from the fp32
# graph that the export accepts. Per-channel int8 storage measured 0.9988 at
# worst over 450 texts; the batch-quantized graph it replaced fell to 0.92.
MIN_FP32_COSINE = 0.995


def quantize_weights(out: Path) -> Path:
    """Write `model_quantized.onnx` next to `model.onnx`: the same graph with
    its large weight matrices stored as int8.

    A matrix that a MatMul multiplies by gets one scale per output column; the
    token embedding table that a Gather reads gets one scale per row, so a rare
    token with small values keeps its precision.
    """
    model = onnx.load(str(out / "model.onnx"))
    graph = model.graph
    matmul_weights = {node.input[1] for node in graph.node if node.op_type == "MatMul"}
    gather_tables = {node.input[0] for node in graph.node if node.op_type == "Gather"}

    kept, stored, restore = [], [], []
    for init in graph.initializer:
        weight = numpy_helper.to_array(init)
        if (
            weight.dtype != np.float32
            or weight.ndim != 2
            or weight.size < MIN_QUANTIZED_ELEMENTS
            or init.name not in matmul_weights | gather_tables
        ):
            kept.append(init)
            continue
        across = 0 if init.name in matmul_weights else 1
        peak = np.abs(weight).max(axis=across, keepdims=True)
        scale = (np.where(peak == 0, 1.0, peak) / INT8_PEAK).astype(np.float32)
        quantized = np.clip(np.rint(weight / scale), -INT8_PEAK, INT8_PEAK).astype(np.int8)
        stored.append(numpy_helper.from_array(quantized, f"{init.name}_int8"))
        stored.append(numpy_helper.from_array(scale, f"{init.name}_scale"))
        # Constant inputs only, so onnxruntime computes these once at load.
        restore.append(helper.make_node("Cast", [f"{init.name}_int8"], [f"{init.name}_cast"], to=TensorProto.FLOAT))
        restore.append(helper.make_node("Mul", [f"{init.name}_cast", f"{init.name}_scale"], [init.name]))
    if not restore:
        raise SystemExit(f"no weight matrix to quantize in {out / 'model.onnx'}; the export layout changed")

    nodes = restore + list(graph.node)
    del graph.initializer[:]
    graph.initializer.extend(kept + stored)
    del graph.node[:]
    graph.node.extend(nodes)
    onnx.checker.check_model(model)
    dst = out / "model_quantized.onnx"
    onnx.save(model, str(dst))
    print(f"  stored {len(restore) // 2} weight matrices as int8 → {dst.name}")
    return dst


def check_against_fp32(out: Path) -> None:
    """Fail the export when the small graph does not reproduce the fp32 one."""
    import onnxruntime as ort

    tokenizer = AutoTokenizer.from_pretrained(out)
    batch = tokenizer(
        ["fix the failing unit test", "draft a contract for a freelance designer", "hi"],
        padding=True, return_tensors="np",
    )
    vectors = []
    for name in ("model.onnx", "model_quantized.onnx"):
        session = ort.InferenceSession(str(out / name), providers=["CPUExecutionProvider"])
        feed = {i.name: batch[i.name] for i in session.get_inputs()}
        cls = session.run(None, feed)[0][:, 0]
        vectors.append(cls / np.linalg.norm(cls, axis=1, keepdims=True))
    worst = float((vectors[0] * vectors[1]).sum(axis=1).min())
    print(f"  lowest cosine against the fp32 graph: {worst:.5f}")
    if worst < MIN_FP32_COSINE:
        raise SystemExit(f"model_quantized.onnx drifted from model.onnx: cosine {worst:.5f} < {MIN_FP32_COSINE}")


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
        "--no-quantize",
        action="store_true",
        help="export fp32 only (skip the small graph the runtime prefers)",
    )
    args = ap.parse_args()

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
        quantize_weights(out)
        check_against_fp32(out)

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
