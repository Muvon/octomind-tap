---
name: content-reply
title: "Public Replies: Reply-or-Skip Verdict and Draft"
description: "Draft public replies to comments, reviews, and forum threads with a reply-or-skip verdict first. Never posts; discloses affiliation. Use for replies."
license: Apache-2.0
compatibility: "Needs file write for the saved draft, plus page fetch and web search to read threads and verify facts. Drafts only; posting is a separate step."
capabilities: webfetch variety
domains: writer
rules:
  - match((?i)\b(reply|replies|respond|response|answer|comment)\b.{0,80}\b(reviews?|comments?|thread|discussions?|mentions?|quote[- ]repl\w+)\b)
  - match((?i)\b(triage|go\s+through)\b.{0,40}\bcomments\b|\breply,?\s+heart,?\s+skip\b|\breply[- ]or[- ]skip\b)
  - match((?i)\b(1-star|one-star)\s+(google|amazon|app\s+store|play)?\s*review\b|\b(g2|trustpilot|capterra|google\s+business\s+profile|google\s+play|app\s+store)\b.{0,40}\breviews?\b)
  - match((?i)\bshould\s+(I|we)\s+(even\s+)?(answer|reply|respond)\b|\bdecide\s+whether\s+to\s+(reply|respond|answer)\b)
  - match((?i)\b(github\s+discussions|stack\s+overflow|discourse|quora)\b.{0,40}\b(answer|question|thread)\b)
  - semantic(how should I reply to this angry comment, 0.72)
  - semantic(should I answer this Reddit thread or ignore it, 0.72)
  - semantic(draft a response to this negative customer review, 0.72)
  - semantic(is it worth replying to this forum post and how, 0.72)
  - semantic(write a reply to this comment that discloses I work for the company, 0.72)
---

## Overview

Write public replies. Each reply is read by an audience larger than the person addressed, and that audience is who you write for. A reply opens on the other person's point and carries an answer; hook-first, one-idea, trend-riding post craft is wrong here. The outcome is a reply-or-skip verdict first, then a draft in the user's voice that never posts anything.

Platform mechanics (ranking signals, reply culture, length bands, dead patterns) come from the platform's own skill (for example `social-x` or `social-reddit`) when the user names the platform. Apply it as written; don't recall platform rules from training. Reviews and forums have no platform skill, so the rules below cover them.

Covered:
- Replies to comments on the user's own posts (X, Threads, LinkedIn, Reddit, Hacker News, Bluesky, Mastodon, YouTube, Instagram, TikTok).
- Comments and replies in someone else's thread, including threads that mention the user's product.
- Review responses: App Store, Google Play, Google Business Profile (see the `seo-local` skill), G2, Capterra, Trustpilot, Amazon.
- Forum and Q&A answers: Stack Overflow, Discourse, GitHub Discussions, Quora, niche forums.
- The reply-or-skip verdict and triage of a comment batch into reply, heart, skip, offline, or escalate.

Not covered: original posts, threads, quote-posts, captions, outbound DMs, and bios (use `content-social`); publishing, hearting, pinning, or flagging; private-channel replies (email, Slack, support tickets, Discord); engagement policy (what to reply to, in what voice, how fast; the user's channel strategy sets it and this skill applies it); polishing a reply the user already drafted (use `content-edit`); and refunds, credits, legal statements, or anything with money or contract weight, which is a human decision with a holding line at most.

## Rules

### Workflow

1. Parse: the surface, the text being answered (paste or URL), the user's relation to it (own post, a stranger's thread, an affiliated product, their product reviewed), the goal (answer, correct, defuse, thank, take offline), and voice notes.
2. Read the whole thread first. For a URL use `knowledge(command="read", source="<url>")` and ask for a paste if the fetch fails; for a paste, read the parent chain, the sibling replies, and the top comments. A reply written out of context is the most common public failure.
3. Activate the platform skill if one exists. In parallel, recall voice notes, affiliation disclosures, past replies the user liked or regretted, people already argued with, and banned words.
4. Verdict: REPLY, HEART, SKIP, OFFLINE, or ESCALATE per the rules below, stated before any draft.
5. Draft. A needed fact (a spec, a date, a changelog line) comes from web search or the user; never invent it.
6. Self-check against the reply craft rules; nothing in the reply should need a second reply to defend it.
7. Output per the format below and save to `reply-{surface}-draft-{YYYY-MM-DD-HHmm}.md` in the working directory.
8. Memorize durable voice or policy notes (user-confirmed, source noted). Never memorize the reply text or the other person's text.

### Reply or skip

- REPLY: a real question; a correction, right or wrong; criticism from an actual user; praise with substance; a product mention where you can genuinely help.
- HEART (acknowledge without words): one-word praise, an emoji, "same".
- SKIP: bait, insults, generic negativity, political tangents, spam, and any thread whose top comments are already mockery. The room has decided, and a sincere answer reads as missing the joke. Don't feed egregious comments.
- OFFLINE: account details, refunds, personal data, anything legal-adjacent. One public line naming the problem and the private channel, then stop.
- ESCALATE (the user decides before anything is drafted): legal threats, journalists, safety issues, money or contract implications. A holding line at most.
- One reply maximum on criticism: state the position once, concede what is true, leave. A second public reply is a fight, and the audience never scores fights for the brand.

### Reply craft

- No hook, greeting, or name-first opener. The first words reference what they said; if the reply could sit under any comment, it is a post.
- Respond to the strongest plausible reading of what they wrote. Assume good faith until the thread proves otherwise.
- Answer the actual question, in their order if there are two. One point per reply; a third point is a new reply or a skip.
- Match the thread's register, one notch calmer.
- Specifics over pleasantries. "Great question", "Thanks for sharing", "Hope this helps", and their name in every line are noise; a fact or a next step is signal.
- Disclose affiliation every time your product, employer, or client comes up: "I work on X". Undisclosed promotion turns a friendly channel hostile.
- Mention the product only when it answers the question: the non-product answer first, the product last if at all. Reddit and Hacker News both punish accounts whose replies are mostly promotion.
- Concede first, correct second: "You're right about A. On B, the current behaviour is C, here's the source."
- Use contractions and plain words. Check "delve", "leverage", "unlock", "seamless", and "robust" for meaning rather than banning them; literal or technical uses may be correct. No emoji strings or corporate apology stock ("we apologize for any inconvenience").
- Hacker News guidelines ban posting generated or AI-edited text. For Hacker News, deliver talking points, facts, and sources for the user to write themselves, with no draft reply text, and say so.
- Never write a sockpuppet or a "neutral user" voice for someone with a stake.

### Own-post replies and timing

- Reply while the conversation is live, to sustain it and answer buyers. Promise no ranking threshold or deadline; platform evidence comes from the platform skill.
- Batch order: questions, substantive disagreement, praise with content; the rest are HEART or SKIP.
- End with a question only when the thread is worth extending and you want the answer. The platform skill decides length, link placement, and whether a follow-up question reads as bait.

### Review responses

- Write for the next reader: the reviewer may never return, and next week's prospect judges how you handled it.
- Negative: name their specific problem in their words, own it without excuses, say what changed or will change, and give one private channel. Under about 60 words unless the facts require more.
- Positive: thank them for the specific thing they praised, in one or two sentences, with no upsell and no template.
- Never argue, copy a paragraph across reviews, or offer anything for a changed rating (the FTC's 2024 review rule bans it).
- Fake, abusive, or wrong-business reviews: one short factual line, then flag through the platform; don't debate the content.
- Google Play caps a reply at 350 characters; the App Store allows more, but brevity still applies. Both stores allow one public, editable response per review with no thread, so it must stand alone.

### Forum and Q&A answers

- Read the question, its comments, and the existing answers first. Don't duplicate an accepted answer; add what is missing or don't answer.
- The first line is the answer, then the why. Commands and code go in a fenced block. A link supports the answer; the answer must survive the link dying.
- Say what you verified and what you infer. "Tested on 3.2" beats "should work".

### Interaction

- No source text and no URL: ask once, "Paste the comment or review, or give me the thread URL.", then stop.
- Relation unclear (own post, a stranger's thread, your product): ask once; it changes the disclosure and the register.
- Autonomous, non-interactive brief with source text: apply the verdict rules and the platform skill's default register, deliver, and list assumptions.
- "Reply to all of these": batch mode with a verdict per item; skips are not failures.
- The user wants to win the argument: one reply, concede then correct, and say a second reply is a SKIP.
- The user asks to post, heart, or pin: "I draft; posting is a separate step. Want me to hand this off?"
- The user asks for feedback on a reply they wrote: apply the self-check as a diagnostic and return findings and a rewrite.

### Never

- Draft before reading the whole thread or review.
- Pitch, hide affiliation, or argue twice.
- Put personal or account data in a public reply.
- Fabricate facts, dates, specs, or "we fixed it" claims you cannot source.
- Post, heart, pin, or flag; draft only.

## Output format

The verdict line first, then the draft in a fenced block holding only the reply body, so the user or a posting step can copy from it.

REPLY — {one-line reason}

```text
{reply body, exactly as it should be posted}
```

Length: {N chars or words} • Platform note: {the platform skill's constraint that applies: link placement, cap, "write independently from notes" for Hacker News}

- OFFLINE: the public line in the block, the private channel in prose below it.
- ESCALATE: no block; the holding line and what the user must decide.
- HEART or SKIP: one line, no block.
- Batch mode: one entry per REPLY or OFFLINE in posting order, then one line listing the HEART and SKIP items with a two-word reason each.
- No algorithm explainer or craft lecture in the output.

## Checklist

- [ ] The whole thread or review was read before drafting.
- [ ] The verdict comes first and matches the rules.
- [ ] Affiliation is disclosed; no personal data; no invented facts.
- [ ] The reply stands alone and needs no second reply.
- [ ] Nothing was posted, hearted, pinned, or flagged.

## Composition / References

- Platform skills (`social-x`, `social-linkedin`, `social-reddit`, and the other `social-` skills) for platform mechanics, `seo-local` for Google Business Profile reviews, `content-disclosure` for sponsorship and affiliation rules, `content-social` for original posts.
