---
name: content-voice
title: "Human Writing Voice"
description: "AI pattern avoidance, dead vocabulary, voice rules, and rhythm guidance for writing that reads as genuinely human. Apply to any content writing or rewriting task."
license: Apache-2.0
compatibility: "Octomind content agents."
domains: content
rules:
  - content(humanize)
  - content(voice)
  - content(article)
  - content(blog)
  - match(\brewrite\s+(this|the|my)\s+(article|blog|post|copy|content|draft|piece|writing)\b)
  - match(\b(write|writing|draft|drafting)\s+(an|a|the|this)\s+(article|blog|post|copy|piece|essay|newsletter)\b)
  - match(\b(make|sounds?)\b.*\b(human|natural|authentic|less\s+ai|less\s+robotic)\b)
  - match(\b(ai|gpt|llm)[-\s]?(generated|sounding|tone|copy|writing|text|prose)\b)
  - match(\bdead\s+vocabulary\b)
  - match(\b(content|copy|article|blog|writing)\s+voice\b)
  - match(\b(tone\s+of\s+voice|brand\s+voice|writing\s+voice)\b)
  - semantic(write this in a more human voice)
  - semantic(make this copy sound natural and authentic)
  - semantic(fix the tone of this writing)
  - semantic(rewrite this article so it does not sound robotic)
  - semantic(remove AI patterns from this draft)
  - semantic(polish this content to read like a real person wrote it)
---

# Human Writing Voice

## Overview

AI-generated text has measurable signatures that readers and search engines detect. This skill encodes the complete ruleset for eliminating those signatures — dead vocabulary, uniform rhythm, missing contractions, structural uniformity — and replacing them with patterns that characterise skilled human writing.

Apply this skill whenever writing, rewriting, or editing content intended to read as human.

---

## Instructions

### Dead Vocabulary — Never Use

These words appear 5–10× more in AI text than human text. Replace every instance.

**Dead verbs**: delve, embark, elevate, unleash, harness, unlock, unveil, foster, navigate, streamline, leverage, underscore, garner, revolutionize

**Dead adjectives**: profound, innovative, transformative, seamless, meticulous, vibrant, robust, cutting-edge, pivotal, intricate, comprehensive, groundbreaking, crucial, vital, essential, poignant, renowned

**Dead nouns**: landscape, tapestry, realm, journey, testament, synergy, underpinnings, dynamic (as noun), aspect (overused), complexity (overused)

**Dead adverbs**: seamlessly, significantly, notably, relentlessly, tirelessly, profoundly

**Dead transitions**: furthermore, moreover, additionally, consequently, importantly, notably, indeed, essentially, alternatively, ultimately

**Dead phrases**:
- "it's important to note"
- "in today's [anything] world"
- "in the realm of"
- "designed to enhance"
- "diverse array"
- "rich tapestry"
- "ever-evolving"
- "game changer"
- "it's worth noting"
- "delving into the intricacies"
- "navigating the complexities"
- "a testament to"
- "not just X, but also Y" — rewrite this construction every time

**Formal overreach** — always use the simpler word:
- "utilize" → "use"
- "facilitate" → "help"
- "demonstrate" → "show"
- "commence" → "start"
- "regarding" → "about"
- "leverage" → "use"
- "implement" → "do" / "build" / "run"

**Trailing participles** — never end sentences with these:
- "...highlighting the importance of"
- "...ensuring that"
- "...contributing to"
- "...underscoring the need for"
- "...demonstrating that"

Rewrite as a separate sentence instead.

---

### Voice Rules

**Contractions — always**
"don't" not "do not", "it's" not "it is", "won't" not "will not", "can't" not "cannot". Uncontracted forms read as AI or legal text. More than 2 uncontracted forms per 500 words is a detectable signal.

**Sentence rhythm — dramatic variation**
Never write 3 consecutive sentences of similar length. Follow a 30-word analytical sentence with a 5-word one. Use fragments for emphasis. One-sentence paragraphs between dense ones. This is burstiness — humans write it naturally, AI doesn't.

Good rhythm:
> The algorithm processes every request through three validation layers before committing to state. That's by design. A single bad write corrupts the entire chain, and recovery is expensive.

Bad rhythm (AI):
> The algorithm processes every request through three validation layers. This ensures data integrity throughout the system. The design prevents corruption and reduces recovery costs.

**Don't rotate synonyms**
If "users" is the right word, keep saying "users." Artificial variation ("users/customers/clients/patrons") across paragraphs reads as AI. Pick the right word and stay with it.

**Personal stake**
Occasional first-person: "I've seen this pattern in...", "What surprised me was...". Acknowledge genuine uncertainty: "The data is mixed here." Show emotional range: enthusiasm, skepticism, curiosity. These are human signals.

**Natural grammar breaks**
Start sentences with "And" or "But" when it flows. Use parenthetical commentary. Occasional fragments for emphasis. These are human patterns — don't avoid them.

**Active voice**
"Studies show X" not "X has been shown by studies." Flag passive constructions and rewrite to active unless passive is intentional for emphasis.

---

### Transitions

Don't use a transition when the logic is clear — just start the next idea. When you need one:

✅ "But." / "The problem is —" / "Here's what that looks like." / "Which raises the question:" / "And this matters because —" / "So what does this mean?" / "The catch?" / "Plus,"

❌ Never: "Furthermore," "Moreover," "Additionally," "Consequently," "It's worth noting"

---

### Conclusions

Never open a conclusion with:
- "In conclusion,"
- "Overall,"
- "In summary,"
- "To summarize,"
- "To wrap up,"

End by circling back to the opening, posing a question, making a prediction, or just stopping. A conclusion that recaps all main points is an AI pattern.

---

## Examples

### Dead vocabulary replacement

❌ `This innovative solution leverages cutting-edge technology to seamlessly facilitate collaboration.`

✅ `This tool uses a shared workspace so teams can work on the same document without stepping on each other.`

### Rhythm fix

❌ `The system processes requests in parallel. This improves throughput significantly. Users experience faster response times as a result.`

✅ `The system processes requests in parallel, which improves throughput. Users notice it immediately. Pages that used to take 800ms now load in under 200.`

### Trailing participle fix

❌ `The update ships next week, highlighting the importance of backward compatibility.`

✅ `The update ships next week. Backward compatibility matters here — anything that breaks existing integrations will be reverted.`
