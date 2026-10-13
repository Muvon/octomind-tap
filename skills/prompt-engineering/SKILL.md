---
name: prompt-engineering
title: "Prompt Engineering: SOTA 2026 Toolkit"
description: "Generate, improve, analyze, and debug LLM prompts. Activate only when the user explicitly asks to write, rewrite, optimize, diagnose, or design a prompt/system prompt, or names a prompt-engineering technique."
license: Apache-2.0
compatibility: "Works with any LLM. Anthropic-specific notes flagged inline (Claude 4.6+ and Claude 5 family behavior, XML tags, effort levels, structured outputs)."
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
2. Context — who the model is, what facts it has, what examples bound the task. Long data goes first; the query goes last (Anthropic: up to 30% better on complex multi-document inputs).
3. Reasoning shape — whether to ask for direct answer, step-by-step, multi-path, or plan-then-execute. Pick by problem type, not by habit.

Iteration is the work. Treat prompts as code: specify, test against representative inputs, iterate.

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
7. Prefer general instructions over prescriptive steps. On current models "think thoroughly" often beats a hand-written step-by-step plan, and prompts written for older models are often too prescriptive for the Claude 5 family; state the goal, constraints, and done-criteria, then let the model plan.

### Reasoning techniques (pick by problem type)

| Problem type | Technique | When to reach for it |
|---|---|---|
| Simple lookup, classification | Zero-shot direct | Default; no scaffolding |
| Format-sensitive output | Few-shot (3–5 examples) | Style, tone, structure |
| Multi-step math/logic | Chain-of-Thought ("think step by step") | Zero-shot CoT took MultiArith 17.7% → 78.7% (Kojima et al. 2022); on reasoning models it's a fallback for thinking-off routes |
| Open-ended planning, multiple valid paths | Tree-of-Thought (explore branches) | Game-of-24: GPT-4 went 4% → 74% |
| High-stakes correctness, single answer | Self-Consistency (sample N, majority vote) | +11–18 points over CoT on arithmetic benchmarks (Wang et al. 2022) |
| Abstract problem hard to attack | Step-Back (ask the general principle first) | Physics, law, framework-application |
| Long task with distinct stages | Plan-and-Solve (write plan, stop, then execute) | Reduces drift on multi-section outputs |
| Wrong first try, can be self-judged | Reflexion / Self-Refine (draft → critique → revise) | Gains depend on a reliable critic; verify on your eval set |
| Tool-use agent | ReAct (thought → action → observation loop) | The standard agentic pattern |

Reasoning models change this table. Current frontier models think internally (Claude adaptive thinking, OpenAI reasoning effort, Gemini thinking level): control depth with the effort parameter, not prompt scaffolding. On Claude Fable 5.1, Opus 5.5, and Sonnet 5.5, a prompt that asks for reasoning written into the response may be declined (`reasoning_extraction`); ask for a short explanation instead and read summarized thinking if you need the trace.

### Agentic prompts (Claude 5 family, 2026)

Agent prompts are runbooks: goal, tools, decision criteria, error handling, stopping conditions. For current Claude models (verify on the model-specific prompting pages):

- Put the full task spec in the first turn; progressive disclosure across turns costs quality and tokens.
- Effort is the main dial. Defaults differ (Opus 5.5 and Haiku 5.5: `medium`; Fable 5.1 and Sonnet 5.5: `high`) and level names don't map across models, so sweep per model against evals. Lowering effort cuts thinking more reliably than prompt instructions.
- Thinking is always on for Fable 5.1 and Opus 5.5: remove "don't think" rules. `budget_tokens` returns 400 on Claude 4.7+, prefill on 4.6+, forced `tool_choice` on Opus 5.5 / Sonnet 5.5 / Fable 5.1 — use structured outputs, or `auto` + an instruction + `strict: true`.
- State scope explicitly ("apply to every section"); current models follow instructions literally.
- Ask for progress updates when you want them (Opus 5.5 returns them as thinking blocks, visible with `display: "updates"`). In unattended runs a text-only turn is a report, not completion.
- State when subagents are and aren't warranted; current models delegate readily.
- Wrap user-pasted content in tags with a random ID; keep histories append-only and add reminders as new messages.

### Tone calibration (the over-emphasis anti-pattern on 4.6+)

Claude 4.5 and later are far more responsive to the system prompt than 3.x; aggressive language written to defeat under-triggering now over-triggers. Substance stays, theatre goes: `CRITICAL: YOU MUST use this tool when...` → `Use this tool when...`; stacked `NEVER`/`ALWAYS` bullets → plain `Don't …` / `Do …`; `DEFAULT TO X` → `Use X when it helps`. Reserve all-caps for one or two genuine safety hard-stops. Substance test: delete the `NEVER`/`MUST` and lowercase the line — if it still makes sense, soften it; if it reads as filler, cut it.

Full recipe with verbatim Anthropic quotes, parallel-tool-calls block, and message-history rules: `reference/claude-4-emphasis-and-tools.md`.

### Frameworks

Acronym templates (RTF, RACE, CRAFT, RISEN, CRISPE) are scaffolding for beginners, not magic: output quality comes from spec clarity, not letter-counting.

### Token efficiency (cost-effective by default)

- Minimise instructions: every line should do work; if removing it doesn't change behaviour, cut it.
- Compress context: summarise large documents before injecting; prefer extractive summaries over re-paraphrasing.
- Cache by design: static content (tools, system prompt, examples) first and byte-stable; variable content (query, runtime data, timestamps) last. Anthropic cache reads cost ~0.1× input or less, writes 1.25× (5-min) or 2× (1-hour); OpenAI and Gemini cache prefixes automatically.
- Don't pad. "Think step by step in great detail with maximum thoroughness" wastes tokens; on reasoning models, raise effort instead.
- Watch for context rot: reliability drops as input grows even on simple tasks (Chroma, Jul 2025). Irrelevant context is noise.

### Output control

- Tell, don't forbid. "Write smoothly flowing prose" beats "do not use markdown".
- Plain directives outperform theatrical ones on 4.6+. `Use tool X when ...` lands harder than `CRITICAL: YOU MUST use X`. See the "Tone calibration" section above and `reference/claude-4-emphasis-and-tools.md`.
- For structured output, use Structured Outputs (Anthropic `output_config.format`, OpenAI Structured Outputs) for typed responses; prefill is not an option on Claude 4.6 and later. For classification, use a tool with an enum field.
- For format constraints, wrap in tags: `Write the answer inside <answer> tags`.
- Match prompt style to desired output style — if you want minimal markdown out, use minimal markdown in.

### Failure modes and their fixes

Common failure modes:

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

Don't change prompts without tests. Build a 5–20 input eval set with known-good outputs, scored on the criteria that matter (accuracy, completeness, format, conciseness). Tools: Promptfoo (open source), LangSmith, Braintrust. If three rounds of fixes don't move the score, the eval set is missing the actual failure mode.

### Meta-techniques

- DSPy / MIPROv2 / GEPA: programmatic prompt optimisation. Write input/output signatures, let the optimiser compile prompts. Useful for production pipelines with stable specs.
- Meta-prompting: ask the model to critique and rewrite its own prompt from concrete failures. Pattern: "Here is my prompt. Here are 3 inputs and the bad outputs it produced. Suggest 3 specific changes that would fix the failures." Verify the rewrite on the eval set.
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

Diagnosis: multi-step reasoning, single answer, high-stakes.

Fix: on a reasoning model, raise effort one level first and re-measure. If errors persist, use Self-Consistency: sample 5 independent runs and ship the majority answer, not the first. (Several current Claude models reject non-default `temperature`, so rely on run-to-run variance there.)

### Example 3: Agent prompt skeleton (Claude 5 family)

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

Effort: start at the model's default and sweep against an eval; adaptive thinking is on. Current models follow instructions literally, so "report every issue including low-severity" is load-bearing — without it, recall drops.

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

Why: data first and query last improves quality by up to 30% on complex multi-document inputs (Anthropic); quote-first cuts through document noise.

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
- [ ] Effort chosen deliberately and swept per model (level names don't map across models); no "don't think" rules on always-thinking models; no prefill or forced tool choice where the model rejects them.
- [ ] Re-tested after every change against the eval set.

## Composition / References

Within-domain skills that pair naturally with this one:
- A prompt being designed for content authoring: see voice/humanisation skills in the content domain.
- A prompt being designed for an agent system prompt: structural rules live in `tap-agent-authoring` (XML block order, U-shape attention, caching rules).

In-skill references:
- `reference/claude-4-emphasis-and-tools.md` — Claude 4.6+ and Claude 5 family tone calibration, parallel-tool-calls block, message-history rules, dial-back recipes.

External authoritative sources:
- [Anthropic — Prompt engineering best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Anthropic — Use XML tags to structure prompts](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [Anthropic — Adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) and [effort](https://platform.claude.com/docs/en/build-with-claude/effort)
- [Anthropic — Prompting Claude Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5) and [Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)
- [Anthropic — Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
- [Prompting Guide — CoT](https://www.promptingguide.ai/techniques/cot), [ToT](https://www.promptingguide.ai/techniques/tot), [ReAct](https://www.promptingguide.ai/techniques/react), [Self-Consistency](https://www.promptingguide.ai/techniques/consistency)
- [Lost in the Middle (Liu et al., TACL 2024)](https://aclanthology.org/2024.tacl-1.9/) — U-shape attention foundation
- [DSPy — Stanford NLP](https://dspy.ai/) — programmatic prompt optimisation
- [Lakera — 2026 prompt-engineering guide](https://www.lakera.ai/blog/prompt-engineering-guide)
- [Anthropic Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
