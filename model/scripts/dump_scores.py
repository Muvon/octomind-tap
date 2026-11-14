"""Score both eval sets with an ONNX graph on THIS machine and save the scores.

A graph can give different cosines on different CPUs: with the graph
shipped 2026-09, which quantized activations, the same brief scored 0.620
against an agent on ARM and 0.664 on an x86 CI runner, and a threshold
calibrated on one machine misfired on the other. The graph export_onnx.py
writes now computes in fp32 and scored identically on three CPU kinds
(2026-11); this dump is how that stays checked. Run it once per CPU kind,
then hand all the dumps to `calibrate_cpus.py`, which picks operating
points that hold on every one.

It needs only numpy, pyyaml, tokenizers and onnxruntime, so it runs in a
bare container:

  # this machine
  uv run python scripts/dump_scores.py --model checkpoints/<run>/onnx --out scores/arm64.json

  # x86 without VNNI, emulated on an ARM Mac (run from the repository root)
  docker run --rm --platform linux/amd64 -v "$PWD/model:/m" -w /m python:3.12-slim sh -c \\
    'pip install -q numpy pyyaml tokenizers onnxruntime && \\
     python scripts/dump_scores.py --model checkpoints/<run>/onnx --out scores/x86-sse.json'
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calibrate_thresholds import precompute_scored  # noqa: E402
from eval_gate import OnnxEncoder, load_triggers_from_pairs  # noqa: E402
from eval_route import load_agents, load_eval_briefs, score_rows  # noqa: E402


def cpu_description() -> str:
    """Architecture plus the SIMD flags that select onnxruntime's int8 kernels."""
    cpuinfo = Path("/proc/cpuinfo")
    if not cpuinfo.exists():
        return platform.machine()
    flags = sorted(set(re.findall(r"\b(avx2|avx512f|avx512_vnni|avx_vnni|sse4_1)\b", cpuinfo.read_text())))
    return f"{platform.machine()} {' '.join(flags)}".strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True, help="dir holding the ONNX graph, tokenizer.json and 1_Pooling/")
    ap.add_argument("--onnx-file", type=str, default="model_quantized.onnx")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    args = ap.parse_args()

    eval_cfg = yaml.safe_load(args.config.read_text())["eval"]
    root = Path(__file__).resolve().parents[1]

    eval_rows = [json.loads(line) for line in (root / eval_cfg["real_set_path"]).read_text().splitlines() if line.strip()]
    triggers_by_cap = load_triggers_from_pairs(root / eval_cfg["triggers_path"])
    scored = precompute_scored(args.model, eval_rows, triggers_by_cap, int(eval_cfg["runtime_top_k"]), args.onnx_file)
    capability = [
        {
            "gold": row.get("label"),
            "kind": row.get("kind", ""),
            "top1": ranked[0][1],
            "s1": ranked[0][0],
            "s2": ranked[1][0] if len(ranked) > 1 else 0.0,
        }
        for row, ranked in zip(eval_rows, scored)
    ]

    encoder = OnnxEncoder(Path(args.model), args.onnx_file)
    route = score_rows(encoder, load_agents(root / eval_cfg["agents_path"]), load_eval_briefs(root / eval_cfg["agent_briefs_path"]))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "cpu": cpu_description(),
        "model": f"{args.model}/{args.onnx_file}",
        "capability": capability,
        "route": route,
    }))
    print(f"wrote {len(capability)} capability rows and {len(route)} route rows to {args.out} ({cpu_description()})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
