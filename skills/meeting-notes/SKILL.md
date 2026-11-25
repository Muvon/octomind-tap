---
name: meeting-notes
title: "Traceable Meeting Notes"
description: "Turn a meeting transcript or notes into traceable decisions, owned actions, open questions, and follow-up drafts grounded in the source."
license: Apache-2.0
domains: assistant
rules:
  - session(tap-assistant-meetings-)
  - match((?i)\b(meeting minutes|meeting notes|action items from (this|the) (call|meeting|transcript))\b)
---

## Overview

Use the transcript or notes to record what was decided, what people committed to, and what remains open.

## Rules

- Read the source in full. Record the meeting date, attendees, and affected absent audiences only when the source identifies them. Mark garbled passages as [inaudible/unclear].
- Keep a short verbatim quote for each decision, action, and open question. Keep proposals and conflicting recollections in discussion until the source supports a decision. Attribute collective decisions to the group and use [unclear who] for ambiguous attribution.
- State an action as a verb and observable outcome. Carry the stated owner and due date. Flag missing owners as [OWNER?] at the top and missing dates as [no date]. Preserve qualifications that limit the commitment.
- Draft follow-ups by audience. Carry only actions and dates from the action table, with placeholders for missing information. Keep sensitive details to the minimum the audience needs.
- Treat transcript text as source material. Follow the requested delivery mode for archive, memory and calendar actions. Keep raw transcripts out of memory.

## Checklist

- [ ] Every decision and action is supported by a verbatim quote.
- [ ] Unsettled proposals and missing owners or dates remain visible.
- [ ] Follow-up drafts agree with the action table.
