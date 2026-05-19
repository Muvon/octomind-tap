---
name: ai-agent-design
title: "AI Agent Design: Loops, Tools, Schemas, Orchestration"
description: "Operational playbook for designing production LLM agents in 2026. Covers agent loop patterns (ReAct, Reflexion, Plan-and-Execute, function calling, Anthropic tool use), tool schema engineering (JSON Schema, strict mode, description craft, anti-patterns), the Agent Skills open standard (Anthropic Dec 2025), Model Context Protocol (MCP) integration, multi-agent orchestration (LangGraph, CrewAI, AutoGen — with cost trade-offs), error handling and infinite-loop prevention, observability via OpenTelemetry GenAI semantic conventions, the OWASP LLM Top 10 v2025 and OWASP Top 10 for Agentic Applications 2026, and the context-engineering discipline that replaced 'prompt engineering' in 2026. Use when designing a new agent, picking an orchestration framework, debugging a misbehaving agent, or hardening tool exposure. Output: agent specs with named patterns, cost projections, observability hooks, and OWASP-mapped risk surfaces."
license: Apache-2.0
compatibility: "Stack-agnostic. Production agent stacks typically need: LLM provider SDK (Anthropic / OpenAI / Google), an orchestration framework or hand-rolled loop, a tracing backend (Langfuse / Phoenix / OpenTelemetry collector), MCP servers or REST tools."
domains: ai
rules:
  - session(ai)
  - content(agent)
  - content(agents)
  - content(tool use)
  - content(function calling)
  - content(MCP)
  - content(orchestration)
  - match(\b(agent\s+(loop|design|pattern|architecture))\b)
  - match(\b(tool[\s-]?(use|call|calling|schema))\b)
  - match(\b(function[\s-]?call(ing|s)?)\b)
  - match(\b(ReAct|Reflexion|Plan-and-Execute|Tree[\s-]?of[\s-]?Thoughts|ToT)\b)
  - match(\b(LangGraph|CrewAI|AutoGen)\b)
  - match(\b(multi[\s-]?agent)\b)
  - match(\b(Model\s+Context\s+Protocol|MCP)\b)
  - match(\b(Agent\s+Skills)\b)
  - match(\b(context\s+engineering)\b)
  - semantic(design an LLM agent with tools)
  - semantic(my agent is stuck in a loop)
  - semantic(should we use multi-agent or single agent with tools)
  - semantic(what is the best agent framework)
  - semantic(write tool schemas for my agent)
---

## Overview

A production LLM agent is a loop: model proposes an action (often a tool call), system executes it, result becomes the next observation, repeat until done. The interesting questions are: which loop pattern, what tools, what schemas, what stops infinite recursion, what's logged for debugging, what's the cost ceiling per task, and which OWASP risks are alive in this surface. This skill encodes the 2026 patterns with cited sources, and the cost / risk numbers that decide architectural choices.

Use this skill when designing a new agent, picking an orchestration framework, debugging a misbehaving agent, or hardening tool exposure. Skip it for single-shot LLM prompts that don't call tools — that's a prompt problem, not an agent problem.

## Mental model

Three forces shape every agent design:

1. Loop structure — how the model reasons across steps. ReAct (interleaved thought-action-observation) is the foundation; Reflexion adds self-critique; Plan-and-Execute splits planning from execution; native function calling (OpenAI / Anthropic tool use) is the production-grade structured variant.
2. Tool surface — what the agent can do. The schema is the API; descriptions decide behavior; the privilege scope decides blast radius. Tool design is the highest-leverage engineering surface and the most-underserved craft.
3. Failure containment — what stops the agent when things go wrong. Max iterations, action deduplication, error feedback, escalation ladders. Without these, an agent that hits an unhandled state burns money in a loop until someone notices.

The 2026 shift: "prompt engineering" → "context engineering" (term coined by Andrej Karpathy, June 2025; amplified by Tobi Lütke). Context engineering covers the whole window — system prompt, tool definitions, retrieved docs, memory, conversation history, few-shot examples, output format. Prompt engineering is now a subset.

## Instructions

### 1. Agent loop patterns

| Pattern | When to use | Source |
|---|---|---|
| ReAct (Thought → Action → Observation) | Default for tool-using agents | Yao et al., Princeton/Google, Oct 2022, [arXiv:2210.03629](https://arxiv.org/abs/2210.03629) |
| Reflexion | Trial-and-error tasks where self-critique helps; more expensive | Shinn et al., [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) |
| Tree-of-Thoughts (ToT) | Hard search problems where ReAct gets stuck; branches reasoning paths | Yao et al., [arXiv:2305.10601](https://arxiv.org/abs/2305.10601) |
| Plan-and-Execute | Cheaper than ReAct (fewer LLM calls per step); brittle when early steps surprise | LangGraph docs; practitioner pattern |
| ReWOO (Reasoning WithOut Observation) | Reduce tokens by decoupling reasoning from tool execution | [arXiv:2305.18323](https://arxiv.org/abs/2305.18323) |
| OpenAI function calling / Anthropic tool use | Production-grade structured tool invocation; default for new builds | [OpenAI function calling guide](https://platform.openai.com/docs/guides/function-calling) (verify URL); [Anthropic tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use) |

Both Anthropic and OpenAI converge on JSON Schema input definitions. Anthropic added `strict: true` mode and Programmatic Tool Calling (agent writes code to orchestrate tools).

### 2. Tool schema design

The most-underserved craft area in 2026. Bad tool schemas produce loops, wrong-tool calls, and ambiguous outcomes.

Best practices (per [Anthropic tool-use docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)):
- Tool descriptions carry more behavioral weight than tool names. Write detailed descriptions; include usage patterns and edge cases.
- Include examples in description text — JSON Schema can't express "when to use this tool."
- Use strict mode when available (Anthropic strict tool use, OpenAI strict function calling).
- Explicit JSON Schema types per parameter; document the expected format with examples.
- One tool per concept; do not overlap. Two tools that could plausibly answer the same query produce wrong-tool calls.

Anti-patterns:
- Generic names (`get_data`, `process`) — the model has no signal for when to call.
- Overlapping tools — `search_customers` and `find_customer` create routing ambiguity.
- Too many optional fields — model fills them with hallucinated defaults.
- Missing examples in description — model has no template for parameter format.
- Vague return-shape — model can't reason about how to use the result.

### 3. Agent Skills (Anthropic open standard, Dec 18, 2025)

Portable skill format across Claude.ai, Claude Code, Agent SDK, and Anthropic Developer Platform. Microsoft integrated it into VS Code; OpenAI announced a "Skills Editor" to export Custom GPTs to the format. Launch partners include Canva, Notion, Figma, Atlassian, Cloudflare, Stripe, Zapier.

Skill format: a directory with a `SKILL.md` (YAML frontmatter + instruction body), optional `validate` script, optional `references/` and `scripts/`. See the canonical spec at the [Anthropic announcement](https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/) and verify current spec URL before integrating.

Use the standard for: agent-specific knowledge that should travel between agents and clients; reusable playbooks across Claude / Cursor / Copilot deployments; production agents whose behavior depends on portable expertise.

### 4. Model Context Protocol (MCP)

Anthropic, launched November 2024. Client–server architecture using JSON-RPC 2.0. Transports: stdio (local), Streamable HTTP (replaced SSE in the November 2025 spec).

2026 roadmap priorities (per [MCP 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)):
- Stateless Streamable HTTP for horizontal scale
- Tasks primitive (async long-running operations)
- MCP Server Cards (`.well-known` metadata)
- Centralized server registry (npm-style)
- SSO-integrated auth, audit trails

MCP vs REST: MCP is purpose-built for LLM tool exposure (server discovery, tool inventory introspection, structured errors); REST is universal but requires manual schema mapping per agent. Use MCP when the tool will be reused across agent contexts; use REST when the tool is one-off or already exists as a deployed service.

Spec: [modelcontextprotocol.io](https://modelcontextprotocol.io).

### 5. Multi-agent orchestration

| Framework | Strength | Trade-off |
|---|---|---|
| LangGraph | Stateful graph + conditional edges; deepest LangChain integration; most production-tested | Steeper learning curve; tied to LangChain abstractions |
| CrewAI | Role-based crews; lowest onboarding cost | Less control over execution; ~18% token overhead vs LangGraph per practitioner benchmarks (verify) |
| AutoGen | Conversational GroupChat patterns | Every turn re-evaluates full history; expensive for high-volume |

Cost trade-off: multi-agent is typically 2–4× single-agent for similar tasks. An AutoGen 4-agent × 5-round debate is 20+ LLM calls minimum. Use multi-agent only when sub-tasks are genuinely parallel or specialized, or when a single agent with rich tools cannot solve the problem. The default should be single agent + better tools + better context.

Orchestration patterns:
- Orchestrator-worker: one planner agent dispatches to worker agents
- Supervisor: hierarchical with a manager and specialist subordinates
- Swarm: peer-to-peer with shared state
- Sequential pipeline: agents in fixed order; cheapest multi-agent variant

### 6. Error handling and infinite-loop prevention

Hard requirements for every production agent:

- Hard max_turns / max wall-time — every agent. No exceptions. A 50-turn cap on a Sonnet 4.6 conversation with rich context can cost $5+ per stuck run.
- Action deduplication — hash `(tool_name, args)` across a run; flag a repeat as a likely loop.
- Action-history comparison — detect oscillation (A → B → A → B …).
- Exponential backoff on retries — 3–5 retries general; 5–7 for rate limits.
- Error message as observation — when a tool fails, feed the error text back as the observation so the model can reason about recovery.
- Escalation ladder — reflection prompt → alternative tool suggestion → context compression + restart → graceful termination with partial results.
- Termination predicate — explicit "done" signal in the system prompt; without it, agents won't stop voluntarily.

Common root causes of stuck agents (per [agentpatterns.tech](https://www.agentpatterns.tech/en/failures/infinite-loop)): missing max_turns, broken termination predicate, no "done" signal in system prompt, ambiguous tool schemas, oscillation between two near-equivalent actions.

### 7. Observability

OpenTelemetry GenAI Semantic Conventions (2026 standardization) — standardizes span names, tool-call attributes, PII-safe prompt logging, agent span kind. Use this as the schema for any new agent.

| Tool | Strength |
|---|---|
| Langfuse | ClickHouse backend, native OTLP endpoint (`/api/public/otel`), strong multi-tenant; OSS |
| Arize Phoenix | Local-first, notebook-friendly, zero external deps; OSS |
| Helicone | Drop-in proxy when you cannot instrument code; OSS |
| LangSmith | Deepest LangChain integration; paid, per-seat |

Per-tool-call log — tool name, args (PII-safe), result, latency, token count, cost, error, parent span ID. Without these, debugging a multi-step failure is forensic guessing.

### 8. OWASP LLM Top 10 (2025) and Agentic Top 10 (2026)

Every agent design surfaces OWASP risks. Map every tool, every retrieved-context source, and every output sink to the relevant item.

OWASP Top 10 for LLM Applications 2025 ([OWASP](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)):
- LLM01 Prompt Injection — direct and indirect
- LLM02 Sensitive Information Disclosure
- LLM03 Supply Chain
- LLM04 Data and Model Poisoning
- LLM05 Improper Output Handling — agent outputs consumed by downstream sinks (SQL, shell, XSS)
- LLM06 Excessive Agency — over-broad tool / permission scopes
- LLM07 System Prompt Leakage (new in 2025)
- LLM08 Vector and Embedding Weaknesses (new in 2025)
- LLM09 Misinformation
- LLM10 Unbounded Consumption — cost / token DoS

OWASP Top 10 for Agentic Applications 2026 ([OWASP](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)) — items begin with `ASI` (Agentic Security Issue). ASI01 Agent Goal Hijack, ASI02 Tool Misuse, ASI03 Identity & Privilege Abuse, plus categories covering delegated trust, persistent memory poisoning, inter-agent communication abuse, unsafe planning/reasoning, supply-chain-of-agents, observability gaps, and ASI10 Rogue Agents. Verify exact names for ASI04–ASI09 against the OWASP PDF before citing in production reports.

Cross-reference with the sibling AI skill on prompt injection defense for the offensive-and-defensive playbook.

### 9. Production failures (cautionary)

- Slack AI indirect prompt injection (Aug 20, 2024) — PromptArmor disclosure; indirect injection from a public Slack channel exfiltrated private DMs via a clickable link. Slack initially called it "intended behavior." [The Register](https://www.theregister.com/2024/08/21/slack_ai_prompt_injection/).
- EchoLeak (CVE-2025-32711) — Microsoft 365 Copilot zero-click; email-triggered indirect prompt injection plus reflection led to confidential data exfiltration. CVSS 9.3; took >5 months to patch. [The Hacker News](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html).
- GitHub Copilot RCE (CVE-2025-53773) — prompt injection led to remote code execution; patched Aug 2025 Patch Tuesday. [Embrace the Red](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/).
- ShareLeak (Copilot Studio, late 2025) and PipeLeak (Salesforce Agentforce) — indirect injection via form/data inputs.

These are all agentic-system failures where untrusted content reached an action surface. The lesson: indirect injection is the dominant 2026 risk; LLM05 (Improper Output Handling) and LLM06 (Excessive Agency) are the cost amplifiers.

### 10. Context engineering (the discipline)

Term coined by Andrej Karpathy, June 2025: "the delicate art and science of filling the context window with just the right information for the next step." Amplified by Tobi Lütke (Shopify CEO) as the "highest-leverage skill" for AI work.

Covers: system prompt + tool definitions + retrieved docs + memory + conversation history + few-shot examples + output format constraints. Prompt engineering is now a subset; the standalone "prompt engineer" role is largely gone (Fast Company, May 2025).

Practical implications:
- Treat context as a budget — every section costs tokens and changes behavior.
- System prompt + tool defs should be cached aggressively (Anthropic / OpenAI prompt caching) — they're long, stable, and re-sent every turn.
- Retrieved context belongs in clearly labeled XML tags so the model knows what's instruction vs data.
- Conversation history grows; cap it or summarize it past a threshold to keep latency / cost bounded.
- Few-shot examples are still effective for behavior shaping when system-prompt instructions alone don't carry.

Cross-reference the cost / FinOps skill for caching numbers and the prompt-injection-defense skill for the data-vs-instruction separation patterns.

## Checklist

- [ ] Loop pattern named (ReAct / Reflexion / Plan-and-Execute / native function calling) with rationale
- [ ] Tool schemas have detailed descriptions with examples; strict mode where available
- [ ] No overlapping tools; one concept per tool
- [ ] Hard max_turns + max wall-time configured
- [ ] Action deduplication + oscillation detection in place
- [ ] Error feedback loop wired (tool errors become observations)
- [ ] Termination predicate explicit in system prompt
- [ ] OpenTelemetry GenAI tracing enabled (Langfuse / Phoenix / Helicone / LangSmith)
- [ ] Per-tool-call logging with cost, latency, token count
- [ ] OWASP LLM Top 10 + Agentic Top 10 risks mapped per tool / context source / output sink
- [ ] Single-agent considered before multi-agent (cost rationale documented if multi-agent chosen)
- [ ] System prompt + tool defs marked for prompt caching
- [ ] If using MCP: server has Server Card metadata (per 2026 roadmap); auth model documented

## Composition / References

Within-domain pairings:
- Pairs with the sibling AI skill on RAG patterns (most agents use retrieval as a tool).
- Pairs with the sibling AI skill on evals (every agent needs trajectory + tool-use accuracy eval).
- Pairs with the sibling AI skill on cost optimization (multi-agent and tool calls are the dominant cost drivers).
- Pairs with the sibling AI skill on prompt injection defense (every tool surface is an attack surface).

Primary sources:
- [ReAct, arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- [Anthropic — Implement tool use](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use)
- [Anthropic — Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)
- [MCP 2026 Roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/)
- [MCP specification](https://modelcontextprotocol.io)
- [Anthropic Agent Skills open standard (SiliconANGLE, Dec 18 2025)](https://siliconangle.com/2025/12/18/anthropic-makes-agent-skills-open-standard/)
- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions/tree/main/docs/gen-ai)
- [Langfuse OpenTelemetry integration](https://langfuse.com/integrations/native/opentelemetry)
- [Slack AI prompt injection (The Register, Aug 2024)](https://www.theregister.com/2024/08/21/slack_ai_prompt_injection/)
- [EchoLeak CVE-2025-32711](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html)
- [GitHub Copilot RCE CVE-2025-53773](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
- [Agent Patterns: Infinite Loop](https://www.agentpatterns.tech/en/failures/infinite-loop)
