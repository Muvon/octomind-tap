---
name: content-voice
title: "Human Writing Voice"
description: "Professional voice, clear prose, and context-aware editing for posts, replies, articles, and scripts. Preserve author facts and register without formulaic rhetoric or fabricated experience."
license: Apache-2.0
compatibility: "Text editing and source material; network access for current policy or factual checks."
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

## Overview

Write clear, useful content in the actual author's voice. Apply this to drafting and revision across posts, replies, articles, and scripts; platform skills provide local format and participation rules. These are editorial practices, not a test of whether a human or AI wrote something.

## Mental model

Professional voice comes from a definite point, credible detail, and respect for the reader. Natural writing can be formal, conversational, technical, or concise. It does not require slang, mistakes, dramatic rhythm, or a story about the speaker.

## Establish the brief

- Identify the speaker, intended reader, task, venue, and source material. Use approved samples to understand register, terminology, humor, and level of detail; don't copy another person's identity or invent a persona.
- With no voice samples, use clear, restrained prose and the supplied facts. Missing samples do not block an ordinary draft. Missing evidence blocks the unsupported claim.
- Preserve numbers, names, quotations, dates, technical terms, conditions, and uncertainty. A polished sentence must not make the claim stronger.
- First person is appropriate for experience or decisions the speaker supplied. Researching a product does not authorize “I tested it.” Don't invent customers, struggle, excitement, vulnerability, or quotations to create personality.

## Write for the reader

- Lead with the useful fact, observation, answer, or decision. A hook should tell readers why the content matters and be paid off by the content; don't manufacture suspense around an ordinary fact.
- Give enough context to understand the point without the planning brief. Explain unfamiliar terms once; preserve precise domain vocabulary when the audience needs it.
- Prefer concrete verbs and identifiable actors. Replace “a transformative solution” with what it actually does, if known. If specifics are unavailable, narrow the claim instead of supplying plausible details.
- Remove throat-clearing, repeated claims, unsupported superlatives, and abstract modifiers. Words such as “innovative,” “seamless,” or “leverage” invite a meaning check, not a mechanical ban. Literal or technical uses may be correct.
- Keep terminology consistent. Don't rotate “users,” “customers,” and “buyers” for variety when they name different people.
- State an evidenced position clearly; keep real qualifications. “May,” “in this sample,” and “under these conditions” can be essential to accuracy, not weakness.

## Rhythm and structure

- Read for comprehension and natural emphasis. Split an overloaded sentence or join choppy ones when it improves the logic. Don't enforce sentence-length alternation, contraction percentages, fragments, or punctuation quotas.
- Contractions, fragments, lowercase, and slang should fit the author's register and venue. Correct accidental errors; never add typos, fake edit notes, broken grammar, or invented dialect as camouflage.
- Use active voice when it clarifies responsibility; passive voice is useful when the actor is unknown or the process/result deserves focus.
- Treat repeated contrast slogans, padded adjective lists, staccato paragraph stacks, and compulsory morals as review prompts. Keep a real comparison, a meaningful list of three, or a useful summary.
- Use questions when their answers matter, not as automatic openers or “Agree?” endings. End after the point, a useful next action, or an unresolved question grounded in the subject; no mandatory twist or inspirational closer.
- Use headings, lists, and tables when they help readers navigate or compare. A technical reply may need steps or code; a brief conversational reply usually needs prose. Length and formatting follow the task, not an authorship stereotype.

## Platform adaptation and trust

- Adapt the same factual core to each venue's reader intent and medium. A narrated demo, a support reply, and a professional announcement need different context and pacing; changing a few synonyms is not adaptation.
- Read the parent post and relevant replies before answering. Add a specific answer or respectful correction; skip empty praise, imitation of the speaker, and unrelated promotion.
- Give a legitimate CTA only when useful. Asking a real question or inviting a relevant action is different from manufactured engagement, false urgency, or a promised reward that cannot be delivered.
- Keep commercial affiliation and required provenance disclosures visible. For US-facing endorsements, FTC guidance requires truthful experience and clear material-connection disclosures; platform controls alone may not communicate the relationship sufficiently. Check applicable local and platform rules.
- Keep alt text descriptive and faithful to visible information; retain material chart labels or provide equivalent explanation. Review captions for names, negation, numbers, and timing. Accessibility fields are not keyword dumps or extra sales copy.
- For another language, match local register and meaning rather than translating English catchphrases literally. Use contextual evidence or qualified review for uncertain idiom; low search frequency is not proof that a phrase is wrong.

## Examples

Illustrative source facts: a product exports CSV; importing CSV is not supported.

Before:
> This revolutionary update unlocks seamless data freedom.

After:
> You can export your data as CSV. CSV import isn't supported.

The rewrite adds only the stated capability and limitation. It does not invent a user result.

Illustrative source: the author's team tested one repository; runtime was not measured.

Avoid:
> We made every workflow dramatically faster.

Use:
> We tested this on one repository. We haven't measured runtime yet.

## Checklist

- [ ] The opening delivers a specific point for the intended reader.
- [ ] Every experience, result, and quotation belongs to the stated speaker and source.
- [ ] Edits preserve scope, uncertainty, and technical meaning.
- [ ] Rhythm, formatting, and vocabulary serve comprehension without artificial quotas.
- [ ] Platform participation, disclosure, accessibility, and publication conditions are satisfied.
- [ ] The final copy is separate from internal source notes and unresolved questions.

## References

Reviewed 2026-09-05. Apply source principles within their stated scope; they do not establish social-platform ranking factors. This is a review date, not a publication/update date for the sources below.

- [GOV.UK clear-language guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/) — a public-service style guide supporting audience-focused clarity, not a universal brand voice.
- [FTC endorsement disclosures](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers) — US-facing endorsements and truthful experience.
- [W3C image alternatives](https://www.w3.org/WAI/tutorials/images/decision-tree/) — communicate an image's purpose and relevant information.
- [Google's AI-content guidance](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) — accuracy and reader value, not guaranteed traffic from “human” style.
- [Fact grounding](../content-grounding/SKILL.md) and [structured revision](../content-humanize/SKILL.md).

Validated: 2026-09

Re-validate when disclosure or accessibility guidance changes, or house voice guidance is revised.
