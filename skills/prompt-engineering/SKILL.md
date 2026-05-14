---
name: prompt-engineering
title: "Prompt Engineering — SOTA 2026 Toolkit"
description: "Generate, improve, analyze, and debug LLM prompts. Activate only when the user explicitly asks to write, rewrite, optimize, diagnose, or design a prompt/system prompt, or names a prompt-engineering technique."
license: Apache-2.0
compatibility: "Works with any LLM. Anthropic-specific notes flagged inline (Claude 4.7 behavior, XML tags, effort levels, structured outputs)."
domains: assistant
rules:
  - match(\bprompt\s+engineer(?:ing|ed|er)?\b)
  - match(\b(write|rewrite|design|build|craft|improve|fix|debug|analy[sz]e|optimi[sz]e|structure)\b.{0,80}\b(a\s+|the\s+|my\s+|this\s+|an\s+)?(system\s+prompt|agent\s+prompt|prompt|prompts|prompting)\b)
  - match(\b(system\s+prompt|agent\s+prompt|prompt|prompts|prompting)\b.{0,80}\b(write|rewrite|design|build|craft|improve|fix|debug|analy[sz]e|optimi[sz]e|structure)\b)
  - match(\b(few|one|zero|multi|N)[-\s]?shot\b)
  - match(\bchain[-\s]of[-\s]thought\b|\bcot\b)
  - match(\btree[-\s]of[-\s]thought\b|\btot\b)
  - match(\breact\s+(prompt|agent|pattern)\b)
  - match(\bself[-\s]consistency\b)
  - match(\bstep[-\s]back\s+prompt\w*)
  - match(\bdspy\b)
  - match(\bprompt\s+(template|framework|pattern)\b)
---

## Overview

This skill helps the user generate, improve, analyze, and debug LLM prompts using state-of-the-art 2026 techniques. Use it when the user wants help writing a prompt, fixing one that misbehaves, picking a technique for their goal, or designing an agent's system prompt. The skill encodes Anthropic's published priority order, the major reasoning and agentic patterns, the most-used frameworks, token-efficiency rules, and the documented failure modes with fixes.

Default framing: the prompt is a contract. Specify what the model should know, do, output, and avoid — in that order — using structure the model can parse unambiguously.

## Mental model

Three layers compose every effective prompt:

1. Spec — what the goal is, what success looks like, what counts as failure. Vague specs are the single largest source of bad output (the documented "underspecification" failure mode).
2. Context — who the model is, what facts it has, what examples bound the task. Context goes first when long; query goes last (30% accuracy lift on multi-document inputs).
3. Reasoning shape — whether to ask for direct answer, step-by-step, multi-path, or plan-then-execute. Pick by problem type, not by habit.

Iteration is the work. Expert prompts hit requirements first try only 40–60% of the time; the same prompt after 3 iterations hits 85%. Treat prompts as code: specify, test, iterate.

The five-step authoring loop:
1. Write the success criteria first (what does "right" look like, measurably).
2. Draft a prompt that names the goal, the role, the format, and the constraints.
3. Run against 3–10 representative inputs.
4. Diagnose failures by category (see Checklist).
5. Apply the smallest fix that resolves the category, re-run, repeat.

## Rules

### Anthropic's priority order (official, 2026 docs)

Apply in this order — earlier items have higher impact per minute spent.

1. Be clear and direct. Tell the model exactly what you want, not what you want it to avoid. Golden rule: would a smart colleague with no context understand this prompt? If no, neither will the model.
2. Add context and motivation. Saying "your response will be read aloud" is more effective than "no ellipses" — Claude generalises from the why.
3. Use examples (3–5, wrapped in `<example>` tags inside `<examples>`). Make them relevant, diverse, and cover edge cases. Few-shot is the single most reliable steerer of format and tone.
4. Structure with XML tags. `<instructions>`, `<context>`, `<input>`, `<output_format>` — Claude was trained to treat these as semantic separators, not decoration.
5. Assign a role in the system prompt. One sentence focuses tone and behaviour ("You are a senior code reviewer specialising in Rust").
6. Long context: data at the top, query at the bottom. Wrap each document in `<document index="n">` with `<source>` and `<document_content>`. For 20k+ token inputs, ask the model to extract relevant quotes first into `<quotes>` before answering.

### Reasoning techniques (pick by problem type)

| Problem type | Technique | When to reach for it |
|---|---|---|
| Simple lookup, classification | Zero-shot direct | Default; no scaffolding |
| Format-sensitive output | Few-shot (3–5 examples) | Style, tone, structure |
| Multi-step math/logic | Chain-of-Thought ("think step by step") | GSM8K-style 17.7% → 78.7% jump on PaLM |
| Open-ended planning, multiple valid paths | Tree-of-Thought (explore branches) | Game-of-24: GPT-4 went 4% → 74% |
| High-stakes correctness, single answer | Self-Consistency (sample N, majority vote) | +12–18% over CoT, no training |
| Abstract problem hard to attack | Step-Back (ask the general principle first) | Physics, law, framework-application |
| Long task with distinct stages | Plan-and-Solve (write plan, stop, then execute) | Reduces drift on multi-section outputs |
| Wrong first try, can be self-judged | Reflexion / Self-Refine (draft → critique → revise) | +10–25% quality on creative tasks |
| Tool-use agent | ReAct (thought → action → observation loop) | The standard agentic pattern |

### Agentic prompts (Claude 4.7-specific, 2026)

Agent prompts are runbooks: goal, tools, decision criteria, error handling, stopping conditions. For Claude Opus 4.7 specifically:

- Put everything the model needs in the first user turn. Ambiguous progressive disclosure across multiple turns reduces both intelligence and token efficiency.
- Set effort to xhigh for coding and agentic work; minimum high for any intelligence-sensitive task. Effort is a more important lever in 4.7 than in any prior Opus.
- Trust adaptive thinking. Don't manually steer the thinking budget; raise effort if you see under-thinking.
- 4.7 follows instructions literally. State scope explicitly ("apply to every section, not just the first"). It will not silently generalise.
- For tool-light behaviour: describe when and why to use each tool. For tool-heavy behaviour: raise effort to high or xhigh.
- Subagent control: "do not spawn a subagent for work you can complete in a single response; spawn multiple in the same turn for fan-out across files".
- Prefilled assistant turns are deprecated in 4.6+. Use Structured Outputs for JSON/schema, and direct system instructions for "no preamble".

### Tone calibration (the over-emphasis anti-pattern on 4.6+)

Claude 4.5+ is far more responsive to the system prompt than 3.x. Aggressive language written to defeat under-triggering on older models now causes over-triggering. The fix is tonal, not structural — substance stays, theatre goes.

- `CRITICAL: YOU MUST use this tool when...` → `Use this tool when...`
- `🚨 HARD RULES` + stacked `NEVER`/`ALWAYS` bullets → plain `Don't …` / `Do …` bullets in a `<critical>` block
- `MANDATORY: Run validation` → `Run validation after edits.`
- `DEFAULT TO using web search` → `Use web search when it would enhance your understanding of the problem.`
- `After every 3 tool calls, summarize` → drop entirely on 4.7 (internalised)

Reserve all-caps and "must" for one or two genuine safety hard-stops (e.g. `Never force-push to main`). Stacking ten dilutes attention and the model treats them as flavour.

Substance test: delete the `NEVER`/`ALWAYS`/`MUST` and lowercase the line. Does the rule still make sense? Soften it. Does it now read as filler? Cut it.

Full recipe with verbatim Anthropic quotes, parallel-tool-calls block, message-history rules, and authoring checklist: `reference/claude-4-emphasis-and-tools.md`.

### Frameworks (when you need a quick template)

| Framework | Slots | Best for |
|---|---|---|
| RTF | Role · Task · Format | Fast one-offs, draft quality |
| RACE | Role · Action · Context · Expectation | Everyday structured tasks (default beginner pick) |
| CRAFT | Context · Role · Action · Format · Tone | Most general-purpose work |
| RISEN | Role · Input · Steps · Expectation · Narrowing | Multi-step procedures |
| CRISPE | Context · Response format · Input · System role · Persona · Execution | Creative, multi-variant generation |

These are scaffolding for thinking, not magic. Output quality comes from spec clarity, not letter-counting.

### Token efficiency (cost-effective by default)

- Minimise instructions: every line should do work; if removing it doesn't change behaviour, cut it.
- Compress context: summarise large documents before injecting; prefer extractive summaries over re-paraphrasing.
- Cache aggressively: put static content (system prompt, tool definitions, examples) at the top of the message; put variable content (user query, runtime data) at the bottom. With Anthropic prompt caching this can cut cost by up to 90% and latency by 85%.
- Don't pad. "Let's think step by step in great detail with maximum thoroughness" wastes tokens; "think step by step" works the same.
- Watch for context rot: even on a 1M-token window, recall degrades visibly past ~50k. Padding actively hurts; irrelevant context is noise.

### Output control

- Tell, don't forbid. "Write smoothly flowing prose" beats "do not use markdown".
- Plain directives outperform theatrical ones on 4.6+. `Use tool X when ...` lands harder than `CRITICAL: YOU MUST use X`. See the "Tone calibration" section above and `reference/claude-4-emphasis-and-tools.md`.
- For structured output, use Structured Outputs (JSON Schema) for typed responses. For classification, use a tool with an enum field.
- For format constraints, wrap in tags: `Write the answer inside <answer> tags`.
- Match prompt style to desired output style — if you want minimal markdown out, use minimal markdown in.

### Failure modes and their fixes

The 12 documented LLM failure modes (Masood 2026, Galileo 2026):

| Mode | Symptom | Fix |
|---|---|---|
| Hallucination | Confident wrong facts | Ground in cited context; allow "I don't know"; add quotes-first step |
| Sycophancy | Agrees with user's wrong premise | "Disagree with confidence when the evidence supports it" |
| Context rot | Quality drops as context grows | Trim context; RAG instead of dumping full docs |
| Instruction attenuation | Ignores rules later in long prompt | Move binding rules to the tail (recency); use XML anchors; restate the constraint |
| Underspecification | Vague output | Add success criteria + format spec + 1 example |
| Task drift (agentic) | Model wanders off goal | Explicit stopping conditions; goal restated each turn |
| Incorrect tool invocation | Wrong tool, wrong args | Describe each tool's purpose and pre/post-conditions |
| Reward hacking | Gaming the metric | Multi-criteria evaluation; adversarial test cases |
| Positional bias | First option over-selected | Randomise option order; test counter-balanced sets |
| Mode collapse | Repetitive output | Increase temperature; add diversity instruction |
| Degeneration loops | Stuck repeating | Max-iteration cap; explicit exit pattern |
| Version drift | Same prompt, new model, worse | Re-evaluate on every model upgrade; pin version in prod |

### Improving an existing prompt (analysis workflow)

When the user shows you a prompt that misbehaves:

1. Read the prompt aloud as if you were the model. Where would you guess what was meant?
2. Ask for 3 example inputs that fail and the desired output for each.
3. Categorise the failure (use the table above). Most failures are underspecification, instruction attenuation, or context rot.
4. Apply the smallest fix:
   - Underspecification → add success criteria + 1 worked example.
   - Instruction attenuation → move the violated rule to the end of the system prompt; add to a `<critical>` block if the harness uses XML structure.
   - Context rot → trim irrelevant context; for long docs, switch to quote-first.
   - Wrong technique → re-pick from the reasoning table.
5. Re-test on the same 3 examples plus 2 new ones to check for regression.

### Evaluation

Don't change prompts without tests. Build a 5–20 input eval set with known-good outputs. Score on accuracy, relevance, coherence, completeness, conciseness. Tools: PromptFoo (open-source), LangSmith, Braintrust. Iteration target: 55% → 85% after 3 rounds is the documented expert baseline — if you're not improving, your eval set is missing the actual failure mode.

### Meta-techniques

- DSPy / MIPROv2 / GEPA: programmatic prompt optimisation. Write input/output signatures, let the optimiser compile prompts. Useful for production pipelines with stable specs.
- Meta-prompting: ask the model to critique and rewrite its own prompt. 10–25% quality lift, near-zero engineering cost. Pattern: "Here is my prompt. Here are 3 inputs and the bad outputs it produced. Suggest 3 specific changes that would fix the failures."
- Constitutional AI: give the model principles, ask it to self-check and revise against them. Works well for safety/tone consistency.

## Examples

### Example 1: Underspecification fix

Bad:
```
Summarise this article.
```

Good:
```
<task>Summarise the article below in 3 bullet points for a technical audience.</task>

<output_format>
- Each bullet: 1 sentence, max 25 words.
- Lead with the most surprising fact, not the topic.
- No "the article discusses..." preamble.
</output_format>

<article>
{{ARTICLE}}
</article>
```

What changed: explicit format, audience, length cap, opening rule. The model now knows what "right" looks like.

### Example 2: Reasoning technique selection

User: "I'm asking the model to solve a logic puzzle and it gets the answer wrong half the time."

Diagnosis: multi-step reasoning, single answer, high-stakes. → Self-Consistency.

Fix: sample 5 CoT runs at temperature 0.7, take the majority answer. Ship the most-frequent answer, not the first.

### Example 3: Agent prompt skeleton (Claude 4.7-tuned)

```
<role>
You are a code-review agent. Find correctness bugs in the diff provided.
</role>

<task>
For each finding, output: file:line, severity (low/med/high), confidence (0–1), one-paragraph explanation.
</task>

<rules>
- Report every issue you find, including low-severity. A separate filter ranks them downstream.
- A "bug" is anything that could cause incorrect behaviour, a test failure, or a misleading result.
- Style and naming preferences are not bugs.
- If the diff has no bugs, return an empty findings list. Do not invent issues.
</rules>

<output_format>
JSON array of {file, line, severity, confidence, explanation}.
</output_format>

<diff>
{{DIFF}}
</diff>
```

Effort: xhigh. Adaptive thinking: on. The literal-instruction-follower behaviour of 4.7 means stating "report every issue including low-severity" is load-bearing — without it, recall drops.

### Example 4: Token-efficient long-context query

Bad (query first, dump everything):
```
What does this contract say about termination clauses?

[50,000 tokens of legal documents]
```

Good (data first, quote-first, query last):
```
<documents>
  <document index="1">
    <source>contract_2026.pdf</source>
    <document_content>{{CONTRACT}}</document_content>
  </document>
</documents>

Find quotes from the contract that govern termination. Place them in <quotes> tags. Then answer: under what conditions can either party terminate, with what notice period? Place the answer in <answer> tags.
```

Why: data-at-top is the documented +30% accuracy pattern; quote-first cuts through document noise; trailing query gets recency attention.

### Example 5: Meta-prompt for self-improvement

```
Here is my system prompt:
<prompt>{{CURRENT_PROMPT}}</prompt>

Here are 3 user inputs and the unwanted outputs the prompt produced:
<failure index="1">
  <input>{{INPUT_1}}</input>
  <bad_output>{{OUTPUT_1}}</bad_output>
  <desired>{{DESIRED_1}}</desired>
</failure>
<!-- repeat for 2, 3 -->

Diagnose which of these failure modes is at play (hallucination, underspecification, instruction attenuation, context rot, sycophancy, task drift, format error, other). For each diagnosed mode, propose ONE specific change to the prompt that would fix it. Output a revised prompt that applies the highest-impact fix only.
```

This pattern delivers 10–25% quality lift on first iteration with no model fine-tuning.

## Checklist

Before shipping a prompt, verify:

- [ ] Success criteria defined: what does "right" measurably look like?
- [ ] A 5+ input eval set exists; current prompt scored against it.
- [ ] Goal stated in one sentence the model could repeat back.
- [ ] Role assigned (one sentence in system).
- [ ] Output format explicit (schema, tags, length, tone).
- [ ] 3–5 examples included if format/tone matters.
- [ ] Long inputs (20k+ tokens) placed at top, query at bottom.
- [ ] XML tags wrapping each content type (`<context>`, `<input>`, `<output_format>`).
- [ ] Instructions phrased as "do this" rather than "don't do that" where possible.
- [ ] Reasoning technique matches problem type (see table — not picked by habit).
- [ ] Constraints that must hold appear near the end of the prompt (recency).
- [ ] No `{{CWD}}` / `{{DATE}}` / dynamic placeholders in the static portion (they break caching).
- [ ] Static content first, variable content last (cache hit ratio).
- [ ] For agents: stopping condition stated; tool descriptions explicit.
- [ ] For Claude 4.7: effort level chosen deliberately (xhigh for coding/agentic, high minimum for intelligence-sensitive).
- [ ] Re-tested after every change against the eval set.

## Composition / References

Within-domain skills that pair naturally with this one:
- A prompt being designed for content authoring: see voice/humanisation skills in the content domain.
- A prompt being designed for an agent system prompt: structural rules live in `tap-agent-authoring` (XML block order, U-shape attention, caching rules).

In-skill references:
- `reference/claude-4-emphasis-and-tools.md` — Claude 4.6+ tone calibration, parallel-tool-calls block, message-history rules, dial-back recipes.

External authoritative sources:
- [Anthropic — Prompt engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Anthropic — Use XML tags to structure prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Anthropic — Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)
- [Anthropic — Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Prompting Guide — CoT](https://www.promptingguide.ai/techniques/cot), [ToT](https://www.promptingguide.ai/techniques/tot), [ReAct](https://www.promptingguide.ai/techniques/react), [Self-Consistency](https://www.promptingguide.ai/techniques/consistency)
- [Lost in the Middle (Liu et al., TACL 2024)](https://aclanthology.org/2024.tacl-1.9/) — U-shape attention foundation
- [DSPy — Stanford NLP](https://dspy.ai/) — programmatic prompt optimisation
- [Lakera — 2026 prompt-engineering guide](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Anthropic Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
