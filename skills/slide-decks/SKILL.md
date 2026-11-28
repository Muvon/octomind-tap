---
name: slide-decks
title: "Markdown Slides with Marp: Decks to PDF and PowerPoint"
description: "Marp markdown slide decks with a bundled theme, linter and overflow check, exported to PDF, HTML or PowerPoint. Use when a deck must ship as a file."
license: Apache-2.0
compatibility: "Requires: python3, Node.js (npx), and Chrome, Edge, Chromium, or Firefox (the installer adds Playwright's Chromium when none is present). Editable PPTX also needs LibreOffice. macOS/Linux."
capabilities: shell slides image-gen image-view
domains: writer founder
rules:
  - content(deck)
  - content(slides)
  - content(marp)
  - match(\b(slide\s*deck|pitch\s*deck|presentation|keynote|pptx|powerpoint)\b)
  - semantic(turn this document into slides, 0.72)
  - semantic(make a pitch deck I can send as a PDF, 0.72)
  - semantic(export my marp deck to powerpoint, 0.72)
  - semantic(build a slide deck from this outline and export it, 0.72)
---

## Overview

A deck is finished when it renders, reads well at the back of the room, and nothing is cut off. This skill takes Marp Markdown (slides as plain text, versionable and easy for an agent to write) all the way to files people open: PDF, PowerPoint, HTML, and PNG previews. The `slide-deck` command lints the Markdown, renders through a pinned Marp CLI with the bundled `octo` theme, and flags slides whose content overflows. Handing over raw Markdown with "render it yourself" is not a deliverable.

## Mental model

- Story first: titles read top to bottom are the argument. Each content slide's title is a full-sentence claim; the body is the evidence.
- The slide shows, the speaker tells: talk decks keep slides sparse and put the narration in speaker notes. Read decks (sent ahead, read alone) carry complete sentences and roughly double the text.
- The theme carries the design: layout classes for title, section break, big number, quote, and two columns, one accent color. Don't hand-style slides with inline HTML.
- Rendering is verification: the PNGs and the overflow check show what the audience will see.

`slide-deck` is installed on PATH with the `slides` capability (the same file is the bundled `scripts/deck.py`, listed under Skill Resources with the `octo.css` theme). `slide-deck <new|lint|render> --help` lists options.

## Rules

### Pipeline

1. Outline: write the assertion titles as a list and read them as a paragraph. If the titles don't carry the story, fix the outline before any slide.
2. `slide-deck new deck-<topic>.md --title "<the deck's one-line claim>"` writes front matter and example layouts.
3. Write the slides (syntax below), notes in `<!-- -->` comments.
4. `slide-deck lint deck-<topic>.md` (`--mode read` for send-ahead decks). Fix every issue or keep it deliberately.
5. `slide-deck render deck-<topic>.md --png --notes` (add `--pptx` and `--html` when asked). Fix every slide the overflow warning names.
6. Open the PNGs in `deck-<topic>-png/` and look at them: hierarchy, crowding, image crops. If an image can't be read, rely on lint and the overflow check and tell the user which files to review.

### Marp essentials

| Need | Markdown |
|---|---|
| New slide | A line with `---` |
| Layout for one slide | `<!-- _class: lead -->` (also `divider`, `stat`, `quote`, `cols`, `dark`) |
| Layout for all following slides | `<!-- class: dark -->` |
| Speaker notes | Any other HTML comment: `<!-- Say the churn number slowly. -->` |
| Hide the page number | `<!-- _paginate: skip -->` |
| Footer on every slide | `footer: Acme · Q3 review` in front matter |
| Brand color | `style: section { --octo-accent: #E11D48; }` in front matter |
| Image with size and alt text | `![w:900 Revenue by month, 2026](chart.png)`: size keywords first, alt text after |
| Half-slide image | `![bg right:40%](photo.jpg)`; text flows on the left |
| Full-bleed background | `![bg](photo.jpg)`; add `![bg brightness:0.5](...)` under white text |
| Big number | `<!-- _class: stat -->` with `## 47%` then `# of churn happens in month two` |
| Two columns | `<!-- _class: cols -->`, a `#` title, then exactly two blocks; for two lists use `-` for the left one and `*` for the right one |
| Heading that shrinks to fit | `# <!-- fit --> Ship it` |

Local images need paths relative to the deck; `slide-deck` passes `--allow-local-files`. Charts are images: render them first (PNG or SVG) at the slide's aspect, one message per chart, the message in the title.

### Slide craft defaults

- Talk decks: ≤ 40 words and ≤ 6 bullets per slide; 1–2 minutes per content slide; 20 minutes ≈ 10–15 slides plus backups.
- Read decks: ≤ 90 words per slide, complete sentences, an executive-summary slide second.
- Open with the stakes, not an agenda; close on the ask, not "Thank you" (the last slide stays up during Q&A).
- Accessibility: alt text on every meaningful image, body text ≥ 24 px (the theme uses 30), contrast ≥ 4.5:1 (keep text off busy photos or darken them), color never the only signal.
- Backup slides after a `<!-- _class: divider -->` slide titled "Appendix".

### Frame the room and the storyline

- Before any slide, fix the audience (who exactly, what they know, what they care about), the occasion and time slot, and the one-sentence outcome: "after this, the room will ___". No outcome, no deck. Ask at most three questions; in an autonomous, non-interactive run, derive the three from the request, state them, and build the outline and deck in one pass with the assumptions listed.
- Find the throughline: one controlling idea in one sentence. Cut what does not serve it or park it in backup slides.
- Structure persuasion by SCQA (situation, complication, question, answer). Structure a pitch that is not a fundraise as problem, stakes, resolution, proof, ask. Structure teaching decks as need, concept, example, practice.
- Outline before slides: the storyline as a list of assertion titles. Read them aloud as a paragraph; if the titles alone do not carry the story, the deck will not either. Get outline approval before drafting the full deck when the user asks for it.
- Turning a document into slides: extract the throughline, state it back in one sentence, then compress by assertion. Never paste paragraphs onto slides.
- Reviewing an existing deck: give a verdict against the titles-as-argument test, the 10-second test, and the outcome, then per-slide fixes ranked by impact.
- Investor fundraising decks, pricing narratives, delivery coaching, rehearsal, and brand identity systems are outside this skill; the storyline method carries over.

### Slide content

- One idea per slide. The title is a full-sentence assertion ("Churn concentrates in month two", never "Churn Overview"). If you cannot write the assertion, the slide has no point yet.
- The 10-second test: the message lands in 10 seconds or the slide is doing the speaker's job. The speaker notes hold the rest.
- Slides are free: split a crowded slide into three. The 10/20/30 rule is a pitch sanity check, not law.
- Prefer progressive disclosure over walls: build a complex diagram across slides or step the visual emphasis. Never put six bullets of eight words on a slide to be read aloud.
- Use sentence case and consistent terminology. Round numbers to meaning ("increase of 47.3%" becomes "nearly half again").
- Generate images with `generate_image` only where they carry meaning (a diagram, a mood-setter for a section break), never as filler and never with text baked in. Save them beside the deck and reference them relatively.
- Verify unfamiliar figures destined for evidence slides by web search, or flag them. Never fabricate data, quotes, or citations.

### Data slides

One chart, one message, the message in the title. Simplify the visual until that message is the first thing seen. Use bar for comparison, line for trend, scatter for relationship, table for lookup; pie only for two or three parts of an obvious whole. Drop 3D, dual axes (they imply causation that is not shown), and rainbow palettes. Highlight the one series that matters and grey the rest. Put a source line on every data slide.

### Deck genres

Say which genre you are building.

- Talk deck: sparse slides, rich notes.
- Send-ahead deck: complete sentences, readable alone, roughly double the text; used for executive pre-reads and async review.
- Hybrid (a talk deck someone will forward) is the most common request: talk-deck slides plus an executive-summary slide and an appendix that survive forwarding.
- Executive and board audiences: answer first (the ask or verdict on slide 2), evidence after.

### Openings, closings, timing

Open with the stakes or the surprise; agenda and team bios go later or in the appendix. Close on the specific ask or action, restated. Plan about 1 to 2 minutes per content slide; a 20-minute slot fits 10 to 15 slides plus backups. Mark the cut-line in the notes: which sections drop if the time halves.

### Exports

| Format | Command | Use |
|---|---|---|
| PDF | default | Sending, printing, investor and board pre-reads (with outlines) |
| PPTX | `--pptx` | The recipient needs PowerPoint; each slide is an image, so it looks exact but text isn't editable |
| Editable PPTX | `--pptx-editable` | Experimental: needs LibreOffice, lower fidelity, no speaker notes; check every slide |
| HTML | `--html` | Presenting from a browser (presenter view with `p`) |
| Notes | `--notes` | Speaker notes as text for rehearsal |
| PNG | `--png` | Review and thumbnails |

## Examples

### Example 1: raw Markdown handed over

❌ "Here is `deck.md`; render it with Marp." The user installs tools and finds slide 7 cut off.

✅ `slide-deck render deck.md --png --notes`, overflow warning on slide 7 fixed by splitting it, and the PDF, notes, and previews delivered.

### Example 2: topic-label titles

❌ `# Churn Overview`, `# Q3 Results`, `# Next Steps`. Lint flags them; the titles don't argue anything.

✅ `# Churn concentrates in month two`, `# Q3 revenue beat plan by 12% on two enterprise deals`, `# Approve the pilot budget by Friday`.

### Example 3: hand-styled slides

❌ Inline `<div style="font-size:18px">` blocks to fit more text. HTML is disabled by default and small text fails the back row.

✅ Split the slide, move detail to notes, or use the `cols` layout.

## Checklist

- [ ] Titles read as an argument; every content slide states a claim.
- [ ] `slide-deck lint` clean or each remaining issue intentional.
- [ ] Rendered with `slide-deck render`; no overflow warning left.
- [ ] Speaker notes on content slides (talk decks).
- [ ] Alt text on meaningful images; brand color set once in front matter.
- [ ] Files delivered: the `.md` source plus PDF (and PPTX/HTML/notes when asked), PNG previews reviewed or flagged as unreviewed.
- [ ] Text contrast is at least 4.5:1 (WCAG 2.2 criterion 1.4.3) and body text is at least 24 px on the 1280x720 slide; smaller text fails the back row.
- [ ] Content slides number between slot minutes divided by 2 and slot minutes divided by 1, plus backups.
- [ ] Notes mark the cut-line for a halved slot.
- [ ] Outlines are delivered as the assertion-title list with the throughline on top.

## Composition / References

- [Marp CLI](https://github.com/marp-team/marp-cli)
- [Marpit directives](https://marpit.marp.app/directives) and [image syntax](https://marpit.marp.app/image-syntax)
- [Marp Core features (fitting header, size)](https://github.com/marp-team/marp-core)
