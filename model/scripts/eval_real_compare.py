"""Compare several models on the broad real-user eval (data/eval_real.jsonl)
under the production runtime gate. Complements eval_runtime_gate.py: that one
is the 32 hand-picked diversity fixtures; this is all 904 real intents across
~77 caps + nulls, so it catches regressions a tiny fixture set can't.

  per_cap = mean of top-K cosine(intent, cap triggers)   (K=3)
  fire iff top1 >= TAU and (top1-top2) >= DELTA           (0.45, 0.08)

Triggers come from pairs.jsonl (the model's native augmented cap corpus),
matching eval_gate.py. Reports, per model:
  top1  = ranking accuracy (correct cap ranked #1, gate aside)
  gate  = fired AND correct / positives  (the real production hit rate)
  fpr   = fired on a null prompt / nulls (false activation; lower better)
  margin= mean top1-top2 on correct positives (separation; higher better)

Usage:
  python scripts/eval_real_compare.py base=ID name=path name2=path2 ...
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import cap_score, load_triggers_from_pairs, select_with_margin  # noqa: E402

TAU, DELTA, TOP_K = 0.45, 0.08, 3
ROOT = Path(__file__).resolve().parents[1]


def evaluate(model_id: str, rows, triggers_by_cap) -> dict:
    m = SentenceTransformer(model_id)
    labels = sorted(triggers_by_cap)
    tvs = {c: m.encode(sorted(triggers_by_cap[c]), normalize_embeddings=True,
                       convert_to_numpy=True, batch_size=128, show_progress_bar=False)
           for c in labels}
    intents = [r["intent"] for r in rows]
    ivs = m.encode(intents, normalize_embeddings=True, convert_to_numpy=True,
                   batch_size=128, show_progress_bar=False)

    pos = top1 = gate_ok = null = fp = 0
    margins = []
    for r, iv in zip(rows, ivs):
        scored = sorted(((cap_score(iv, tvs[c], TOP_K), c) for c in labels), reverse=True)
        fired = select_with_margin(scored, TAU, DELTA)
        gold = r.get("label")
        if gold is None:
            null += 1
            fp += fired is not None
        else:
            pos += 1
            if scored[0][1] == gold:
                top1 += 1
                margins.append(scored[0][0] - (scored[1][0] if len(scored) > 1 else 0.0))
            if fired is not None and fired[1] == gold:
                gate_ok += 1
    return {
        "top1": top1 / pos if pos else 0.0,
        "gate": gate_ok / pos if pos else 0.0,
        "fpr": fp / null if null else 0.0,
        "margin": float(np.mean(margins)) if margins else 0.0,
    }


def main() -> int:
    specs = [a.split("=", 1) for a in sys.argv[1:] if "=" in a]
    if not specs:
        print("usage: eval_real_compare.py name=model_id_or_path ...")
        return 2
    rows = [__import__("json").loads(l) for l in
            (ROOT / "data/eval_real.jsonl").read_text().splitlines() if l.strip()]
    triggers = load_triggers_from_pairs(ROOT / "data/pairs.jsonl")
    print(f"eval_real: {len(rows)} intents | gate tau={TAU} delta={DELTA} top_k={TOP_K}\n")
    print(f"{'model':<22}{'top1':>7}{'gate':>7}{'fpr':>7}{'margin':>8}")
    print("-" * 51)
    for name, mid in specs:
        r = evaluate(mid, rows, triggers)
        print(f"{name:<22}{r['top1']:>7.3f}{r['gate']:>7.3f}{r['fpr']:>7.3f}{r['margin']:>8.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
