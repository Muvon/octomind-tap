# Claude 4.6+ and Claude 5 Tone Calibration & Tool-Use Patterns

Reference card distilled from Anthropic's published prompting guidance (Claude 4.5 through the Claude 5 family). Source-linked at the bottom. Use this when authoring or auditing a system prompt that will run on Claude 4.5 or later.

## The over-emphasis anti-pattern (the "YOU MUST" problem)

Claude Opus 4.5 and later are far more responsive to the system prompt than 3.x. Aggressive language that was needed to overcome under-triggering on older models now causes over-triggering. The fix is tonal, not structural — the rule stays, the theater goes. The Claude 5 family goes further: prompts written for earlier models are often too prescriptive, so prefer stating the goal and constraints over scripting every step.

Anthropic's verbatim guidance:

> Claude Opus 4.5 and Claude Opus 4.6 are also more responsive to the system prompt than previous models. If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said "CRITICAL: You MUST use this tool when...", you can use more normal prompting like "Use this tool when...".

On tool selection:

> Replace blanket defaults with more targeted instructions. Instead of "Default to using [tool]," add guidance like "Use [tool] when it would enhance your understanding of the problem."

On scaffolding 4.7 has internalised:

> Claude Opus 4.7 provides more regular, higher-quality updates to the user throughout long agentic traces. If you've added scaffolding to force interim status messages ("After every 3 tool calls, summarize progress"), try removing it.

## Dial-back recipe

The shift is from theatrical emphasis to plain directive language. Substance stays; tone softens.

| Don't write | Do write |
|---|---|
| `CRITICAL: YOU MUST X` | `X.` (one line, no all-caps prefix) |
| `🚨 HARD RULES` + 10 stacked `NEVER` bullets | `<critical>` block with `Don't … / Do …` bullets in plain language |
| `MANDATORY: Run validation` | `Run validation after edits.` |
| `NEVER assert X you haven't verified` | `Don't assert X you haven't verified.` |
| `ALWAYS use tool Y` | `Use tool Y when …` |
| `DEFAULT TO using web search` | `Use web search when it would enhance your understanding.` |
| `IMPORTANT: After every 3 tool calls, summarize` | (drop on 4.7+; Claude Fable 5.1 writes fewer updates, so ask for them in plain terms there) |

Reserve all-caps and "must" for one or two single load-bearing safety hard-stops the model genuinely needs to refuse against (e.g. `Never force-push to main`). Stacking ten of them dilutes the signal and the model starts treating all of them as flavour.

The substance test: would the rule still make sense if I deleted the `NEVER`/`ALWAYS`/`MUST` and lowered the case? If yes → soften. If the rule reads as flavour or filler once softened → cut it.

## The parallel-tool-calls block (verbatim, Anthropic-recommended)

For agent prompts that benefit from concurrent tool use, append this block. Keep the tag name verbatim — Anthropic's training data uses it as a structural anchor.

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

Anthropic's claim: takes parallel-call success rate from "high by default" to ~100%. Claude Fable 5.1 usually parallelizes explicit multi-fetch requests but may issue implied independent calls one per turn in coding and computer-use loops; a one-sentence batching nudge at the end of the request fixes it ([Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)).

### Message-history formatting (the silent killer)

Bigger cause of regression to sequential tool calls than any prompt change:

- All tool results from one assistant turn go in a single user message (one content array of `tool_result` blocks).
- Splitting tool results into separate user messages teaches the model to avoid parallel calls.
- No text before tool results inside the content array.
- Return a failed tool as `tool_result` with `is_error: true`; don't drop it.
- On models that check thinking-block bindings (Claude Fable 5.1, Opus 5.5, Sonnet 5.5), keep the history append-only: add reminders as new messages instead of editing earlier turns.

## Reflection between tool batches

When you want the model to plan rather than reflexively chain another call:

```text
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, and then take the best next action.
```

## Tool-use triggering and effort

> Claude Opus 4.7 has a tendency to use tools less often than Claude Opus 4.6 and to use reasoning more. This produces better results in most cases. However, increasing the effort setting is a useful lever to increase the level of tool usage, especially in knowledge work. `high` or `xhigh` effort settings show substantially more tool usage in agentic search and coding.

The same lever holds on the Claude 5 family, with one caveat: effort level names don't map to the same amount of thinking across models, and defaults differ (Opus 5.5 defaults to `medium`). Re-run the effort sweep per model.

Levers, in priority order:
1. Raise `effort` (more impact than prompt changes).
2. Describe each tool's purpose, when it helps, and post-conditions.
3. Drop blanket "default to X" instructions — they over-trigger.

## Empirical results worth knowing

- LLMCompiler (ICML 2024) — planner emits a DAG of tasks → parallel dispatch: up to 3.7× latency speedup, 6.7× cost savings, ~9% accuracy gain vs ReAct.
- W&D (Feb 2026) — scaling the number of parallel tool calls per turn reduces turns needed and raised BrowseComp accuracy in deep-research agents; see the paper for the per-turn instruction design.
- M1-Parallel (2025) — "devise a different plan" diversity prompts offered no advantage over plain resampling; diversity prompting introduced unnecessary steps.

## Authoring checklist

- [ ] No stacked `CRITICAL:` / `🚨 HARD RULES` / theatrical headers — use plain `<critical>` block.
- [ ] All-caps emphasis reserved for one or two genuine safety hard-stops; stacked all-caps softened to plain language.
- [ ] `Use X when …` rather than `Default to X` / `Always use X`.
- [ ] `Don't X` rather than `NEVER X` (capitals reserved for one or two genuine safety hard-stops).
- [ ] Tool descriptions describe purpose + when it helps, not "MUST USE THIS TOOL".
- [ ] No "after every N calls, summarize" scaffolding on 4.7+; ask for progress updates in plain terms only where the model writes too few.
- [ ] `<use_parallel_tool_calls>` block present if the agent benefits from concurrent tool calls.
- [ ] Tool-result messages: all results in one user message per assistant turn.

## Sources

- [Anthropic — Prompting best practices (current models)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [Anthropic — Parallel tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/parallel-tool-use)
- [LLMCompiler (ICML 2024)](https://arxiv.org/abs/2312.04511)
- [W&D — Scaling Parallel Tool Calling for Efficient Deep Research Agents (arXiv 2026)](https://arxiv.org/html/2602.07359v1)
- [M1-Parallel (arXiv 2025)](https://arxiv.org/html/2507.08944v1)
