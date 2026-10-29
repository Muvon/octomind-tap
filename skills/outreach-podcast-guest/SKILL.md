---
name: outreach-podcast-guest
title: "Podcast Guest Pitch Templates and Speaker Outreach"
description: "Podcast guest pitch templates, show research, speaker pitches, one-sheets, and follow-up guidance. Use when pitching yourself or a founder for podcast interviews, webinars, or conference talks."
license: Apache-2.0
compatibility: "Needs web search and page fetch for show research. Any OS."
domains: marketing launch
rules:
  - content(podcast) content(guest)
  - content(speaking) content(pitch)
  - content(one-sheet)
  - content(conference) content(submission)
---

## Overview

Guest and speaking outreach earns an audience through someone else's show. Hosts need good episodes, not promotion, so the pitch sells the listener's outcome: a specific story, argument, or lesson the audience cannot get elsewhere. This skill covers finding fitting shows, the pitch, the one-sheet, and follow-up.

## Mental model

A host is choosing an episode, not a guest. The pitch has to make the episode visible: the title, the three things the listener walks away with, and proof you speak well. A guest who has listened to the show and fits its format gets booked over a bigger name who did not.

## Rules

### Finding shows and slots

Research from live sources:

| Check | Evidence |
|-------|----------|
| Topic and format | Last 10 episode titles; interview, solo, panel, or narrative |
| Guest policy | Booking page, "be a guest" form, or host note |
| Audience | Stated size or ranking, listener profile, how recent episodes perform |
| Activity | An episode in the last 60 days |
| Contact route | Booking form, host email, or producer on the show page |

For conferences and webinars, check the call-for-proposals dates, track themes, talk formats, and past speakers. Drop shows that are inactive, closed to guests, or off-topic.

### The pitch

Under 150 words. Subject: the episode idea, not "Guest request". Line one names a specific recent episode and what you took from it. Then: your proposed episode title, three takeaways for the listener, one credibility fact, a link to the one-sheet, and one ask. Use the booking form when the show asks for it, instead of emailing the host.

### The one-sheet

One page, saved as `onesheet-<name>.md`:

- Name, role, photo link, short bio in third person (60 words).
- Three episode topics, each with a title and three takeaways.
- Three sample questions a host can ask.
- Proof: past appearances, audience, results, with links.
- Contact and booking route.
- Technical setup: microphone, location, availability.

### Conference and webinar submissions

Follow the CFP format exactly. Lead with the audience problem, state the learning outcomes, and write a title that works as a search query. Include a short speaker bio and a link to a recording if one exists.

### Follow-up

One follow-up after 7 to 10 days. A booking request on a busy show may take weeks. After two touches, stop and recommend a different show.

### Before and after the recording

Send a short prep note with links the host may want. Afterwards, send a thank-you, the assets promised, and an offer to share the episode. Track appearances and which pitch worked.

### Shared rules

Use the `outreach-cold-copy` skill for subject and cadence craft, and the `outreach-compliance` skill for consent and opt-out rules.

## Examples

Bad: "Hi, I'd love to be on your podcast. I'm the CEO of Acme and I talk about many things."

Good: "Your episode with Dana Lee on pricing page tests changed how I think about anchoring. I'd pitch 'Three pricing mistakes we made at $5k MRR': the free tier trap, the annual discount, and the tier we deleted. One-sheet attached."

## Checklist

- [ ] Show active, open to guests, and listened to before pitching?
- [ ] Pitch names one recent episode, one episode idea, three takeaways?
- [ ] One-sheet complete with proof and technical setup?
- [ ] Booking form used when the show requires it?
- [ ] Follow-up capped at one, then stop?
- [ ] Appearances and outcomes tracked?

## Composition / References

- Pair with `outreach-cold-copy` and `outreach-compliance` for craft and legal rules.
- Pair with press and clip specialists once an episode is recorded.
