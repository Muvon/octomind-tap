"""Run octomind's embedding-dependent test fixtures against an ONNX graph.

octomind has three tests that embed literal text with the real model and
assert on what the runtime gates decide. New weights move the scores, so
those tests can break the moment the weights are published. This script
runs the same fixtures on a graph BEFORE it is published.

Nothing is mirrored by hand: fixtures, floors and thresholds are read from
the octomind sources.

  src/mcp/runtime/capability_inline_tests.rs
      capability_routing_fixtures_match_expected_caps
      capability_routing_diversity_fixtures
  src/mcp/orchestration/tap_route_tests.rs
      developer_tasks_reach_their_specialist_and_foreign_tasks_reach_none

Besides pass/fail it lists the fixtures whose decision sits within
`--edge` of flipping. The int8 graph scores a few hundredths differently per
CPU kind, so run it on each kind (it needs only numpy, pyyaml, tokenizers
and onnxruntime; see dump_scores.py for the container recipe) and move or
replace fixtures that sit on the edge anywhere.

  uv run python scripts/eval_runtime_gate.py --model checkpoints/<run>/onnx
  # try thresholds before editing the Rust constants:
  uv run python scripts/eval_runtime_gate.py --model checkpoints/<run>/onnx \\
      --capability 0.60,0.05 --route 0.55,0.06
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import OnnxEncoder  # noqa: E402

_STRING = r'"((?:[^"\\]|\\.)*)"'


def strip_comments(source: str) -> str:
    """Drop `//` comments, leaving string literals intact."""
    out: list[str] = []
    for line in source.splitlines():
        in_string = False
        cut = len(line)
        i = 0
        while i < len(line):
            ch = line[i]
            if in_string:
                if ch == "\\":
                    i += 1
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif line.startswith("//", i):
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def unescape(literal: str) -> str:
    return literal.replace('\\"', '"').replace("\\\\", "\\")


def constant(source: str, name: str) -> float:
    found = re.search(rf"const {name}: \w+ = ([0-9.]+);", source)
    if not found:
        raise SystemExit(f"constant {name} not found")
    return float(found.group(1))


def test_body(source: str, name: str) -> str:
    start = source.index(f"fn {name}(")
    end = source.find("\n#[", start)
    return source[start : end if end != -1 else len(source)]


def block(body: str, declaration: str) -> str:
    """The `&[ ... ];` or `[ ... ];` initialiser that follows `declaration`."""
    start = body.index(declaration)
    return body[start : body.index("];", start)]


def capabilities(body: str) -> dict[str, list[str]]:
    caps: dict[str, list[str]] = {}
    for name, triggers in re.findall(rf"make_cap_with_triggers\(\s*{_STRING}\s*,\s*&\[(.*?)\]", body, re.S):
        caps[unescape(name)] = [unescape(t) for t in re.findall(_STRING, triggers)]
    return caps


class Gate:
    """One runtime gate over one candidate set: threshold + margin on ranked scores."""

    def __init__(self, encoder, threshold: float, margin: float):
        self.encoder = encoder
        self.threshold = threshold
        self.margin = margin

    def embed(self, texts: list[str]) -> np.ndarray:
        return self.encoder.encode(texts, normalize_embeddings=True, convert_to_numpy=True)

    def decide(self, scored: list[tuple[float, str]]) -> tuple[str | None, float, list[tuple[float, str]]]:
        """(picked, slack, ranked). `slack` is how far the decision is from
        flipping: for a pick, the smaller of its distances above the threshold
        and above the margin; for an abstain, the larger of the two shortfalls."""
        ranked = sorted(scored, reverse=True)
        top1 = ranked[0][0]
        gap = top1 - (ranked[1][0] if len(ranked) > 1 else 0.0)
        over_threshold, over_margin = top1 - self.threshold, gap - self.margin
        if over_threshold >= 0 and over_margin >= 0:
            return ranked[0][1], min(over_threshold, over_margin), ranked
        return None, max(-over_threshold, -over_margin), ranked


def describe(ranked: list[tuple[float, str]]) -> str:
    return ", ".join(f"{name}={score:.3f}" for score, name in ranked[:2])


def run_capability_tests(source: str, gate: Gate, top_k: int, min_chars: int, edge: float) -> bool:
    def scorer(caps: dict[str, list[str]]):
        vecs = {name: gate.embed(triggers) for name, triggers in caps.items()}

        def score(intent: str) -> list[tuple[float, str]]:
            intent_vec = gate.embed([intent])[0]
            return [(float(np.sort(v @ intent_vec)[-top_k:].mean()), name) for name, v in vecs.items()]

        return score

    ok = True

    # --- capability_routing_fixtures_match_expected_caps ---
    name = "capability_routing_fixtures_match_expected_caps"
    body = test_body(source, name)
    score = scorer(capabilities(body))
    positives = [(unescape(i), unescape(c)) for i, c in re.findall(rf"\(\s*{_STRING}\s*,\s*{_STRING}\s*\)", block(body, "let positives"))]
    negatives = [unescape(i) for i in re.findall(_STRING, block(body, "let negatives"))]
    pos_floor = float(re.search(r"pos_acc >= ([0-9.]+)", body).group(1))
    neg_floor = float(re.search(r"neg_acc >= ([0-9.]+)", body).group(1))
    notes: list[str] = []
    pos_ok = neg_ok = 0
    for intent, expected in positives:
        picked, slack, ranked = gate.decide(score(intent))
        pos_ok += picked == expected
        if picked != expected or slack < edge:
            notes.append(f"    {'MISS' if picked != expected else 'edge'} {intent!r}: expected {expected}, got {picked} (slack {slack:.3f}; {describe(ranked)})")
    for intent in negatives:
        picked, slack, ranked = gate.decide(score(intent))
        neg_ok += picked is None
        if picked is not None or slack < edge:
            notes.append(f"    {'MISS' if picked is not None else 'edge'} {intent!r}: expected None, got {picked} (slack {slack:.3f}; {describe(ranked)})")
    passed = pos_ok / len(positives) >= pos_floor and neg_ok / len(negatives) >= neg_floor
    ok &= passed
    print(f"{'PASS' if passed else 'FAIL'} {name}: positives {pos_ok}/{len(positives)} (floor {pos_floor}), "
          f"negatives {neg_ok}/{len(negatives)} (floor {neg_floor})")
    print("\n".join(notes))

    # --- capability_routing_diversity_fixtures ---
    name = "capability_routing_diversity_fixtures"
    body = test_body(source, name)
    score = scorer(capabilities(body))
    fixtures = re.findall(rf"\(\s*{_STRING}\s*,\s*{_STRING}\s*,\s*(?:Some\({_STRING}\)|None)\s*\)", block(body, "let fixtures"))
    floors = {c: float(f) for c, f in re.findall(rf"\(\s*{_STRING}\s*,\s*([0-9.]+)\s*\)", block(body, "let floors"))}
    totals: dict[str, list[int]] = {}
    notes = []
    for category, intent, expected in fixtures:
        intent, expected = unescape(intent), unescape(expected) or None
        entry = totals.setdefault(category, [0, 0])
        entry[1] += 1
        if sum(1 for ch in intent if not ch.isspace()) < min_chars:
            picked, slack, ranked = None, 1.0, []  # the runtime never embeds it
        else:
            picked, slack, ranked = gate.decide(score(intent))
        entry[0] += picked == expected
        if picked != expected or slack < edge:
            notes.append(f"    {'MISS' if picked != expected else 'edge'} [{category}] {intent!r}: expected {expected}, got {picked} (slack {slack:.3f}; {describe(ranked)})")
    passed = all(totals[c][0] / totals[c][1] >= floor for c, floor in floors.items())
    ok &= passed
    summary = ", ".join(f"{c} {totals[c][0]}/{totals[c][1]} (floor {floors.get(c, 0.0)})" for c in sorted(totals))
    print(f"{'PASS' if passed else 'FAIL'} {name}: {summary}")
    print("\n".join(notes))
    return ok


def run_route_test(source: str, gate: Gate, edge: float) -> bool:
    name = "developer_tasks_reach_their_specialist_and_foreign_tasks_reach_none"
    source = strip_comments(source)
    roster = re.findall(rf"\(\s*{_STRING}\s*,\s*{_STRING}\s*,\s*{_STRING}\s*\)", block(source, "const DEVELOPER_ROSTER"))
    tasks = re.findall(rf"\(\s*{_STRING}\s*,\s*(?:Some\({_STRING}\)|None)\s*\)", block(source, "const DEVELOPER_TASKS"))
    max_missed = int(re.search(r"const MAX_MISSED_DEVELOPER_TASKS: usize = (\d+);", source).group(1))

    tags = [unescape(tag) for tag, _, _ in roster]
    vecs = gate.embed([f"{unescape(title)}. {unescape(description)}" for _, title, description in roster])
    wrong = missed = 0
    notes: list[str] = []
    for task, expected in tasks:
        task, expected = unescape(task), unescape(expected) or None
        picked, slack, ranked = gate.decide(list(zip((vecs @ gate.embed([task])[0]).tolist(), tags)))
        if picked == expected:
            status = "edge" if slack < edge else None
        elif expected is not None and picked is None:
            missed += 1
            status = "missed"
        else:
            wrong += 1
            status = "WRONG"
        if status:
            notes.append(f"    {status} {task[:70]!r}: expected {expected}, got {picked} (slack {slack:.3f}; {describe(ranked)})")
    passed = wrong == 0 and missed <= max_missed
    print(f"{'PASS' if passed else 'FAIL'} {name}: wrong {wrong} (allowed 0), missed {missed} (allowed {max_missed}) of {len(tasks)}")
    print("\n".join(notes))
    return passed


def pair(value: str) -> tuple[float, float]:
    threshold, margin = value.split(",")
    return float(threshold), float(margin)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True, help="dir holding the ONNX graph, tokenizer.json and 1_Pooling/")
    ap.add_argument("--onnx-file", type=str, default="model_quantized.onnx")
    ap.add_argument("--octomind", type=Path, default=Path(__file__).resolve().parents[3] / "octomind",
                    help="octomind checkout to read fixtures and constants from")
    ap.add_argument("--capability", type=pair, default=None, metavar="THRESHOLD,MARGIN",
                    help="override AUTO_ACTIVATE_THRESHOLD / AUTO_ACTIVATE_MARGIN")
    ap.add_argument("--route", type=pair, default=None, metavar="THRESHOLD,MARGIN",
                    help="override ROUTE_THRESHOLD / ROUTE_MARGIN")
    ap.add_argument("--edge", type=float, default=0.03, help="list fixtures whose decision is closer than this to flipping")
    args = ap.parse_args()

    src = args.octomind / "src" / "mcp"
    capability_rs = (src / "runtime" / "capability.rs").read_text()
    skill_auto_rs = (src / "runtime" / "skill_auto.rs").read_text()
    route_rs = (src / "orchestration" / "tap_route.rs").read_text()
    capability = args.capability or (constant(capability_rs, "AUTO_ACTIVATE_THRESHOLD"), constant(capability_rs, "AUTO_ACTIVATE_MARGIN"))
    route = args.route or (constant(route_rs, "ROUTE_THRESHOLD"), constant(route_rs, "ROUTE_MARGIN"))
    print(f"capability gate {capability[0]}/{capability[1]}, route gate {route[0]}/{route[1]}, edge {args.edge}\n")

    encoder = OnnxEncoder(Path(args.model), args.onnx_file)
    ok = run_capability_tests(
        strip_comments((src / "runtime" / "capability_inline_tests.rs").read_text()),
        Gate(encoder, *capability),
        int(constant(capability_rs, "AUTO_ACTIVATE_TOP_K")),
        int(constant(skill_auto_rs, "MIN_INTENT_NON_WS_CHARS")),
        args.edge,
    )
    ok &= run_route_test((src / "orchestration" / "tap_route_tests.rs").read_text(), Gate(encoder, *route), args.edge)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
