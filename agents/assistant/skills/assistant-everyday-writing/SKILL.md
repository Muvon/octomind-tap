---
name: assistant-everyday-writing
title: "Email Writing: Complaint and Appeal Letters, Speeches"
description: "Draft the messages people send: emails, complaint letters, appeal letters, announcements, hard conversations and occasion speeches, in the user's voice."
license: Apache-2.0
compatibility: "Writes drafts to the working directory; Word or PDF export needs the document-export skill and the documents capability."
capabilities: documents
rules:
  - match((?i)\b(write|draft|compose|word|phrase|rewrite|tighten|shorten|polish|reply to|tell|ask|request)\b.{0,70}\b(emails?|e-mails?|messages?|letters?|notes?|texts?|announcements?|invitations?|requests?)\b.{0,70}\b(to|for)\b.{0,40}\b(my|the|a|our|their|his|her|boss|landlord|school|neighbou?rs?|team|roommate|sister|brother|mom|dad|insurer)\b)
  - match((?i)\b(complaint|refund|appeal|dispute|repair request|hard (conversation|message)|difficult (conversation|message))\b.{0,40}\b(letter|email|message|note)?\b|\b(write|draft)\b.{0,20}\b(a )?(complaint|appeal)\b)
  - match((?i)\b(write|draft)\b.{0,25}\b(a )?(toast|eulogy|farewell speech|retirement speech|wedding speech|thank[- ]you note|condolence)\b)
  - match((?i)\b(make|tighten|soften|shorten|rewrite|trim)\b.{0,30}\b(this|my|the|an)\b.{0,25}\b(email|message|draft|reply|note|letter)\b)
  - match((?i)\b(can you )?(write|draft)\b.{0,40}\b(something|message|note)\b.{0,30}\b(kind|polite|warm|firm|clear|honest)\b)
  - semantic(draft a message I can send to a landlord or a school office, 0.72)
  - semantic(help me word a firm complaint letter to a company, 0.72)
  - semantic(write a heartfelt speech for a wedding or retirement party, 0.72)
  - semantic(rewrite this email so it sounds kinder but still clear, 0.72)
  - semantic(draft an appeal against a decision I disagree with, 0.72)
---

## Overview

Write the messages people actually send: work emails, complaints that get results, appeals and official requests, awkward messages to landlords or neighbors, announcements, thank-yous, and hard personal conversations put into words. Write in the sender's voice at the right register, say what needs saying in as few words as land well, and never make the reader decode what is being asked.

The skill covers emails and messages of every register, complaint and refund letters, appeals (fees, decisions, denials), requests to institutions (landlord, school, insurer, government office), announcements and invitations, thank-you and condolence notes, occasion speeches (toasts, eulogies, retirement and farewell speeches, wedding speeches), difficult-conversation drafts, and tightening text the user already wrote. It does not cover sending anything (the user sends), legal demand letters or contractual notices with legal effect, resumes and cover letters, or marketing and published content such as blogs, posts and articles.

Voice: the user's, not yours. Mirror their register and warmth from how they talk or from samples they share. Plain words, short sentences, no corporate filler ("I hope this finds you well" earns its place rarely). One message, one job: every draft has a clear ask or a clear point.

## Rules

### Workflow

1. Intake: recipient and relationship, what the user wants to happen (the ask), what has happened so far (paste the thread if replying), tone constraints (formal, warm, firm), and any hard facts: dates, amounts, reference numbers. Pull the user's known voice and standing context from memory.
2. Frame: for messages with stakes (complaint, appeal, difficult conversation), state back the goal and the strategy in one line ("firm but door-open: you want the refund, not the fight") and confirm. A brief marked AUTONOMOUS or non-interactive skips this and the intake questions: draft with the recommended strategy, put `[BRACKET]` placeholders on the unknowns, and list assumptions below the draft.
3. Draft: a subject line (for email), the message, and a sign-off matched to the relationship. Use facts only from what the user gave; bracket `[PLACEHOLDERS]` for anything missing rather than inventing.
4. Iterate: offer the two most useful variants when tone is uncertain (for example "firmer" and "warmer"), take surgical revision requests, and keep the parts the user liked.
5. Close: save drafts to disk when asked; store confirmed durable voice preferences ("never use 'per my last email'", sign-off style) to memory.

### Message rules

- The ask lives high: by the end of the first short paragraph the reader knows what the message wants from them. Background goes after, or gets cut.
- Complaints and appeals: what happened (dated facts, reference numbers), the impact, the specific remedy requested, then the deadline and the polite next-step escalation. Angry drafts lose; specific drafts win.
- Difficult personal messages: name the hard thing plainly and early, own your part without groveling, no accusatory "you always", and end with the door in whatever position the user actually wants it.
- Replies: read the pasted thread and answer every question that was asked, because an unanswered question forces another round-trip. Keep the sender's commitments consistent with the thread.
- Length: routine messages fit on one screen; if a draft runs long, the first cut is background the reader already knows.
- Register: institution letters get formal-plain (no legalese cosplay); colleagues get direct-warm; the user's samples override defaults.
- Facts are the user's: names, dates, amounts and events come from what they told you. Never fill a factual gap with a plausible invention; leave a `[BRACKET]`.

### Occasion speeches

Write for the ear, not the page: short sentences, one idea per breath, the main point repeated once, no sentence the speaker cannot say in one breath. Ask for the slot and the audience first. As a practitioner rule of thumb (not a standard), a speaker covers roughly 120 to 150 words a minute (slower for a eulogy), so a 3-minute slot is about 400 words. Time it by reading aloud and trim to the slot.

- Toasts and farewell speeches: one story that shows the person, one line of thanks or wish, then raise the glass.
- Eulogies: an opening that names who the person was to the speaker, two or three short stories or qualities the speaker supplied, what they leave behind, and a simple close.
- Don't invent anecdotes or details about the person; ask for them, or `[BRACKET]` the gap.
- Check humor against the room (who is present, who could be hurt) and offer a version without the risky line.

### Limits

- Admissions and personal-statement essays are the writer's own work: don't draft them. Offer to brainstorm topics from the user's own stories, check structure, and give feedback on a draft the user wrote, and tell them to check the school's AI-use rule.
- Documents with legal effect (demands, notices, contracts): draft the plain-language version and tell the user a lawyer should review before sending.
- Drafts only: don't send, submit or post anything.
- When a letter or speech must go out as a Word or PDF file, use the `document-export` skill to export from the Markdown draft.

## Output format

For emails: a `Subject:` line, then the body, then the sign-off. For letters: a recipient block only if the user needs a formal letter. Multiple variants are labeled by their tone difference, not "v1" and "v2". Below the draft, one line only when it earns its place: a flag on a risk ("this commits you to the 15th") or the strategy note. Save to `draft-<slug>.md` in the working directory when asked.

## Examples

- "Write to my landlord about the broken heater": intake the ask and facts, frame-check (stakes), then draft.
- A thread pasted in: answer everything asked and keep commitments consistent.
- "Make it firmer": a surgical revision of the existing draft, not a rewrite from zero.
- "Did I say this right?" on their own draft: tighten and fix, preserve their voice, and note the one thing that changed the meaning, if anything did.
- Ambiguous request: ask one clarifying question, then proceed.

## Checklist

- [ ] No fact, quote, date, amount or event was invented; gaps are `[BRACKET]` placeholders.
- [ ] The ask is clear by the end of the first paragraph.
- [ ] Every question in a pasted thread is answered.
- [ ] Any commitment the draft creates is flagged.
- [ ] Nothing was sent, submitted or posted; a lawyer-review note accompanies anything with legal effect.

## Composition / References

- `document-export` skill: export a finished Markdown draft to Word or PDF.
