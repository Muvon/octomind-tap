"""WiSE-FT / model-soup weight averaging between the BASE embedder and a
fine-tuned checkpoint.

Why: fine-tuning a very general base (all-MiniLM-L6-v2, pretrained on 1B+
diverse pairs) on our narrow templated augmentation narrows it — better on
the synthetic holdout, worse on real diverse phrasings (eval_real). That's
catastrophic forgetting of the base's generalization. The documented fix is
to interpolate the weights:

    theta_soup = (1 - alpha) * theta_base + alpha * theta_ft

which keeps the base's broad generalization (high top1/gate on real prompts)
AND grafts in the fine-tune's capability-cluster sharpening (wider margin).
Costs nothing at train or inference time.
  - WiSE-FT: https://arxiv.org/abs/2109.01903
  - Model soups: https://arxiv.org/abs/2203.05482

Usage:
  uv run python scripts/model_soup.py \
      --base sentence-transformers/all-MiniLM-L6-v2 \
      --ft checkpoints/embed-minilm-lowtemp-<ts> \
      --alphas 0.2,0.4,0.5,0.6,0.8 \
      --out-dir checkpoints/soup
  # → writes checkpoints/soup/soup-a0.2 ... ready to eval with compare_bases.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from sentence_transformers import SentenceTransformer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="base model id or dir")
    ap.add_argument("--ft", required=True, help="fine-tuned checkpoint dir")
    ap.add_argument("--alphas", default="0.2,0.4,0.5,0.6,0.8",
                    help="comma list; weight on the FT model (0=base, 1=ft)")
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()

    alphas = [float(x) for x in args.alphas.split(",")]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    print(f"loading base: {args.base}")
    base = SentenceTransformer(args.base)
    print(f"loading ft:   {args.ft}")
    ft = SentenceTransformer(args.ft)

    # The underlying HF transformer is module 0; pooling/normalize modules
    # follow and are identical between base and ft (same architecture), so
    # we only average the transformer weights and keep ft's module config.
    sd_base = {k: v.clone() for k, v in base[0].auto_model.state_dict().items()}
    sd_ft = {k: v.clone() for k, v in ft[0].auto_model.state_dict().items()}

    missing = set(sd_base) ^ set(sd_ft)
    if missing:
        raise SystemExit(f"state-dict key mismatch (different architectures?): {list(missing)[:5]}")

    for alpha in alphas:
        souped = {k: (1.0 - alpha) * sd_base[k] + alpha * sd_ft[k] for k in sd_base}
        ft[0].auto_model.load_state_dict(souped)
        out = args.out_dir / f"soup-a{alpha}"
        ft.save(str(out))
        print(f"wrote {out}  (alpha={alpha})")

    print("done. eval with: compare_bases.py --models <these dirs>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
