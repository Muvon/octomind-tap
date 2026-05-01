---
name: social-linkedin
title: "LinkedIn Publishing Playbook"
description: "Ground-truth 2026 playbook for writing posts, comments, and articles on LinkedIn. Covers the 2026 algorithm (dwell time as top signal, comments weighted 15× likes, golden hour, 63% impression drop, 60% off-platform link penalty), the 210-character 'see more' fold, format craft for the 1300–2000 char sweet spot, post types, and what gets suppressed as motivational slop. Activate whenever drafting anything destined for LinkedIn."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to LinkedIn."
domains: content
rules:
  - content(linkedin)
  - match(\blinkedin\s+post\b)
  - match(\bpost\s+(on|to|for)\s+linkedin\b)
  - match(\bprofessional\s+post\b)
  - match(\bcareer\s+post\b)
---

# LinkedIn Publishing Playbook

## Overview

LinkedIn in 2026 is not the LinkedIn of 2020. The algorithm rewards **dwell time** above everything else, comments weigh ~15× a like, and overall impressions have dropped ~63% platform-wide since 2024 — meaning the remaining audience is harder to earn and easier to lose. At the same time, the "motivational quote + emoji + humble brag" era is over; LinkedIn's 2026 LLM-powered ranking actively suppresses generic inspirational content.

Pair with `content-voice` for human voice. LinkedIn has its own dialect ("excited to announce," "humbled to share") that reads instantly as AI or PR. Kill it hard.

---

## Instructions

### The 2026 Algorithm — What Actually Matters

LinkedIn's LLM-powered ranking tracks two signals the rest of social media undervalues: **dwell time** (how long a user's eyeballs stay on your post as they scroll) and **substantive comments** (not reactions, not emoji replies).

| Signal | Weight / Effect |
|---|---|
| **Dwell time** | Top hidden signal. Measured as scroll pause + expansion + read time |
| **Comment (real reply, not emoji)** | ~15× a like |
| **Comment-on-your-comment (author re-engagement)** | Compounds — re-enters the feed for people who missed it |
| **Share with text (repost with commentary)** | Very high weight; pure reshare is worth less |
| **Like / reaction** | Low weight; mostly just a reach-base floor |
| **Click "see more" to expand post** | Dwell + intent signal |
| **External link in root post** | **~60% distribution penalty.** LinkedIn wants users on-platform |
| **Video (native, vertical, short)** | Boosted; outperforms text of same quality |
| **Document carousel (PDF upload)** | Still boosted as of 2026 but declining |
| **Polls** | Mostly gamed-out by 2026, moderate boost only |

**Critical structural facts:**
- **Golden hour**: first 60–90 minutes after publish decide if the post is amplified. Low engagement in this window caps the ceiling.
- **Impressions dropped 63%** platform-wide since 2024. What counted as a flop two years ago is now a good post.
- **The 210-character fold**: only the first ~210 chars show before "…see more" on mobile. If the user doesn't click "see more," you get close to zero dwell time. **The hook must earn the expand click.**

---

### What LinkedIn Kills in 2026 (dead patterns)

These used to work. They don't now. The 2026 LLM-based ranker actively downranks them:

- **Motivational platitudes**: "Success is a journey, not a destination" — instant suppression
- **Humble-brag clichés**: "I'm humbled/blessed/honored to announce…"
- **Emoji bullet lists**: 💡✨🚀 at the start of every line
- **"🚨 BREAKING:"** or "🚨 ATTENTION:" openers
- **"Who agrees?"** / "Thoughts?" endings — these are dead CTAs
- **"Agree / Disagree? Comment below."** — reads as engagement bait
- **Poll posts with fake options** designed only to farm votes
- **Text that reads like a press release**: "excited to announce," "delighted to share," "thrilled to partner with"
- **Screenshots of your own tweets**
- **AI vocabulary**: leverage, unlock, harness, delve, seamless, cutting-edge, transformative (full list in `content-voice`)
- **"As a leader…"** / "As a founder…" / "As an entrepreneur…" opens
- **Story-that-isn't-a-story**: "Yesterday a junior dev asked me…" followed by a generic lesson. The 2026 ranker detects fabricated parables

---

### Post Length — 3 Modes

LinkedIn allows up to **3000 characters**. Three viable modes:

| Mode | Chars | Use When |
|---|---|---|
| **Virality** | 150–300 | Sharp take, one idea, no "see more" needed |
| **Depth** | 1300–2000 | Story, framework, breakdown — most engagement per post |
| **Authority article** | 2000–3000 | Long-form thinking, white paper bait |

The 1300–2000 band is the sweet spot for dwell time + comment generation. Shorter posts can go viral but rarely generate the conversation LinkedIn rewards.

---

### The Post Anatomy (1300–2000 char mode)

```
[LINE 1 — HOOK]               ← fits above the 210-char fold; must pull the expand click
[BLANK LINE]
[LINE 2–3 — SETUP]            ← still above the fold ideally
[BLANK LINE]                  ← "...see more" appears around here
[LINE 4–N — BODY]             ← one idea per paragraph, blank line between each
[BLANK LINE]
[CLOSING LINE OR QUESTION]    ← earns the comment, not an "Agree?" beg
```

Rules:

- **First line is the whole gamble.** If it doesn't earn the "see more" click, the post is done. Treat it like an email subject line.
- **Line breaks are structural.** Dense paragraphs flop. One idea per short paragraph, blank line between. This triples scan-readability and dwell time.
- **No emoji bullets.** Use them sparingly inline for tone, never as list markers.
- **Body in the expanded section is where specifics go** — numbers, names, concrete artifacts, your actual experience.
- **Closing question must be answerable.** "What's your take?" is dead. "Has anyone tried X in production? Did it behave the way I'm describing?" works.

---

### Hook Patterns That Earn the Expand Click

LinkedIn's 210-char fold is brutal. These hook shapes survive it:

1. **The counter-intuitive claim** — "I just fired our top-performing SDR." → reader has to click to find out why
2. **The specific artifact** — "Day 47 of running our ops with zero meetings. Here's the cost sheet:"
3. **The rejection of a common belief** — "Stop writing job descriptions. They're the reason your funnel is broken."
4. **The moment of realization** — "I lost a $40k deal last week. The post-mortem is ugly."
5. **The pattern callout** — "Every Series A founder I meet has the same broken hiring loop."
6. **The asymmetric result** — "We cut our AWS bill by 73%. One config change."
7. **The confession** — "I've been running performance reviews wrong for 8 years. Here's what I changed."

**Never** open with: "Excited to," "Thrilled to," "Humbled to," "Happy to," "I'm proud to," a generic quote, or a motivational aphorism.

---

### Post Types That Work in 2026

| Type | Structure | Why It Works |
|---|---|---|
| **Personal story with lesson** | Scene → turn → lesson (not a moral) | Highest dwell time; feels human |
| **Framework / how-we-did-it** | Problem → approach → numbers → trade-offs | Bookmark-bait; reshared with commentary |
| **Contrarian take** | Claim → evidence → implication | Drives comments both supporting and disagreeing |
| **Data reveal** | Here's what we found → what surprised us | Quoted by others; builds authority |
| **Document carousel** | 6–10 slide PDF uploaded as native doc | Still gets a boost; works for step-by-step teaching |
| **Short-form vertical video (< 90s)** | Face-to-camera or screen recording | The single most boosted format in 2026 |

What doesn't work as its own post type: pure product announcement, pure inspirational quote, pure request-for-network-help without value offered in return.

---

### Comment Strategy

Comments are worth ~15× a like on your own posts AND the biggest growth lever if you comment on others' posts.

**On your own post:**
- Respond to the first 5 comments within 60 minutes. This is the single biggest thing you control for amplification.
- Author-reply with substance. Don't just "Thanks!" — add a follow-up thought, a related story, or a question back.
- Never like your own post. The signal is noise.
- Pin the best comment if it adds real value; it anchors the conversation.

**On others' posts (the actual growth play):**
- Reply early. Top 3 comments get seen; later comments are buried.
- Minimum 2 lines of substance. One-liners don't earn profile clicks.
- Add, don't echo. "Great post!" is invisible. Extending the idea with a specific example is read and clicked.
- Disagree respectfully with specifics. "I had the opposite experience at [scale / domain]" beats "Disagree."
- No links in comments unless asked. LinkedIn throttles them.
- Tag people sparingly and only when genuinely relevant.

---

### Documents (PDF Carousels)

Still a boosted format as of 2026 but declining — use selectively.

- **6–10 slides max.** Longer fatigues the swipe.
- **Slide 1 = hook slide.** Same rule as a post first line.
- **One idea per slide.** Massive font, minimal text, one visual anchor per slide.
- **Last slide = soft CTA** — "Save this if it was useful" or "Follow for more on [niche]"
- **Design matters.** Canva-default templates are obvious; bespoke or minimalist wins.

---

### Videos (the 2026 growth edge)

- **Vertical (9:16), native upload.** Re-uploads from TikTok/IG get suppressed.
- **< 90 seconds** for best watch-through rate.
- **First 3 seconds = hook.** Same principle as text — break the expected.
- **Captions burned in.** Most LinkedIn users watch muted.
- **Face-to-camera outperforms voiceover** for personal accounts.
- **No intro logos, no "hey guys welcome back."** Straight to the point.

---

### Timing

- **Best windows**: Tue–Thu, 8–10 AM local and 12–1 PM local (lunch scroll).
- **Avoid**: Friday afternoon, all weekend for B2B audiences; Sunday evening can work for career/personal-development content.
- **One post per day max** for personal accounts; more dilutes each post's reach budget.
- **Company pages are separate** and generally have 5–10× less organic reach — don't mix strategies.

---

### Thread-Vibe Matching (Comments)

Before writing a comment on someone else's post, scan the existing comment section. LinkedIn comments develop a tone quickly — formal vs. casual, long vs. short, personal vs. analytical.

**What to scan:**
- **Length** — are comments 1 line or 4–5 lines? Match the median. A 4-line comment in a 1-line thread reads like a lecture.
- **Formality** — are people writing in full sentences with punctuation, or is it casual and clipped?
- **Personal vs. analytical** — is the thread sharing personal stories, or debating a claim? Match the mode.
- **First-name culture** — if people are addressing the author by first name, you can too. If not, don't.

**Vibe calibration by post type:**

| Post type | Comment vibe |
|---|---|
| Personal story / vulnerability post | Warmer, shorter, first-person, no data |
| Framework / how-we-did-it | Analytical, can be 3–4 lines, add your own data |
| Contrarian take | Engage the claim directly; disagree or extend with specifics |
| Announcement / milestone | Brief acknowledgment + a real question (not "congrats!") |
| Data reveal | Add a counter-data point or a "we saw the same/opposite" |

---

### Human Imperfection Protocol

LinkedIn is the most polished of all social platforms — posts are professional, people proofread. But **comments** are typed casually, often from a phone between meetings. Calibrate accordingly.

**Imperfection level by content type:**

| Content type | Level | What that means |
|---|---|---|
| Original post | Very low | 0 imperfections for posts; one subtle slip max if it's a personal/casual post |
| Document carousel | Zero | Slides are designed artifacts — no imperfections |
| Comment on others' post | Low-medium | 1 natural imperfection is fine; reads human, not careless |
| Reply to a comment on your own post | Low | 1 subtle imperfection acceptable; you're in a conversation |

**Imperfection menu for LinkedIn (pick 0–1 per comment, never in posts):**

- **Missing comma** — `I saw the same thing at our last company and it surprised me` — natural in fast typing
- **Lowercase opener** — only if the comment thread is already casual/lowercase
- **Casual contraction** — `gonna`, `kinda`, `tbh` — only in clearly informal threads, never in professional/formal ones
- **Dropped article** — `We ran [the] same experiment` — one small omission
- **Run-on with "and"** — two thoughts joined without a period — common in typed-fast comments
- **No closing period** — end a comment without a period — very common in LinkedIn comments

**Never do on LinkedIn:**
- Typos in a post — credibility damage is real; LinkedIn audiences notice and judge
- Typos in a document/carousel — these are designed artifacts, zero tolerance
- Casual slang (`lol`, `ngl`, `tbh`) in a formal or B2B thread
- More than 1 imperfection per comment — stacking reads as careless, not human
- Imperfections when citing data, numbers, or making a technical claim

**Calibration check before posting:**
1. Is this a post or a comment? Posts = zero imperfections (or one subtle slip in a personal post only).
2. Read the existing comment thread — what's the formality level?
3. Does your comment have 0–1 natural imperfections appropriate to the register?
4. Would a professional typing this between meetings plausibly have written exactly this?

---

### Pre-Publish Checklist

- [ ] First 210 characters stand alone and pull the expand click
- [ ] No motivational aphorisms, no "excited to," no "humbled to"
- [ ] No emoji bullets
- [ ] Length in the 1300–2000 sweet spot (unless virality mode or article mode, intentional)
- [ ] One idea per paragraph, blank line between paragraphs
- [ ] No external link in the root post (put links in first comment)
- [ ] Closing question is answerable, not engagement-bait
- [ ] Scheduled for Tue–Thu morning or lunch window
- [ ] Ready to respond to first 5 comments within 60 minutes
- [ ] Reads like a person talking, not a press release
- [ ] **Strip-test (announcement / win / company-mention posts):** if the announcement, milestone, or company name is removed, is the post still useful or interesting to a reader? If no, it's a humble-brag wearing a story's clothes — rewrite around the actual lesson, or skip the post
- [ ] **Post:** zero imperfections (or one subtle slip in a personal/casual post only)
- [ ] **Comment only:** scanned existing comments for length/formality before writing; 0–1 natural imperfection calibrated to register

---

## Examples

### Example 1: Hook that earns the expand click

**Bad (press-release opener):**
> I'm absolutely thrilled and humbled to announce that after many months of hard work, our team has successfully launched our brand-new initiative focused on driving impactful outcomes for our customers 🚀🎉

**Bad (generic motivational):**
> Success isn't about being the smartest in the room. It's about showing up every day and putting in the work 💪

**Good (counter-intuitive + specific):**
> I just fired our top-performing SDR.
>
> He hit 140% of quota three quarters running. Here's why letting him go was the single best hiring decision I made this year.
>
> [body below the fold…]

What works: line 1 creates a gap the reader must close. Specific number. Promise of a counter-intuitive lesson. No LinkedIn-speak.

---

### Example 2: 1300–1800 char story post

```
I lost a $40k deal last week because of a single sentence in my email.

Not the pricing. Not the features. One sentence.

Here's what happened.

We were two weeks into procurement with a mid-market SaaS company. Demo went well, technical eval passed, legal was reviewing the MSA. On Thursday, their VP asks for a "final summary of why we should pick you."

I wrote back a nine-point email. Point four was: "Our platform is built to scale to enterprise, so you won't need to replatform when you grow."

Monday morning, they went with our competitor.

In the debrief, their VP was honest: "That line made us feel like you saw us as a stepping stone, not a customer."

Three things I learned, hard:

1. The "future-proof" pitch reads as condescending when someone hasn't asked for it. They know they'll need to scale. They don't need me telling them.

2. Enterprise-readiness is a hygiene factor — useful if asked, insulting if volunteered. It signals "you're small now."

3. The worst sales mistakes aren't in the demo. They're in the tone of one line in one email after the close.

I've rewritten our follow-up templates. Every "built to scale" claim is gone. I now ask, at the start, what tier of growth they're planning for — and match the pitch to that tier, not the biggest customer we have.

Has anyone else had a deal die on a specific line they wrote? Curious which phrases have cost you money.
```

What works: specific dollar amount, concrete scene, three numbered lessons that are actually lessons (not platitudes), honest failure, closing question is answerable from real experience not a forced prompt.

---

### Example 3: Short virality-mode post

```
Stop writing job descriptions.

They're the reason your funnel is broken.

Every JD I've read in 2026 asks for the same 14 skills, the same "fast-paced environment," the same "drive for results."

Candidates skim them, pattern-match to 100 identical postings, and apply to all of them equally. Your JD isn't doing the filtering you think it is.

Write a 3-line "what this role actually does on Monday morning" instead. Watch your inbound quality double.
```

What works: under 300 characters would be tighter, but this reads as a sharp single-idea post. No fold problem because it's short enough to read whole. Contrarian claim, evidence, actionable alternative, specific prediction.

---

### Example 4: Closing question comparison

**Dead (engagement bait):**
> What do you think? Agree? Disagree? Let me know in the comments! 👇

**Dead (too generic):**
> Thoughts?

**Alive (answerable from experience):**
> Has anyone seen the opposite — where "built to scale" language actually helped close a mid-market deal? Curious if there's a segment where it still lands.

What works: specific, bounded, invites someone who has a counter-example to contribute something the OP hasn't thought of. These replies drive the dwell time and comment chains that amplify reach.

---

### Example 5: Comment that earns a profile visit

Someone posts: *"We cut our engineering hiring in half this year and shipped more features than the year before."*

**Bad (echo, no substance):**
> This is so true! Quality over quantity, always.

**Good (extending with specifics):**
> Seeing the same in our org. We went from 38 engineers to 24 over 18 months and throughput went up, not down.
>
> The thing that surprised me: it wasn't the layoffs that helped, it was the meetings we stopped holding because there weren't enough people to staff them. We accidentally killed 12 recurring syncs.
>
> Has the meeting load gone down on your side too, or did you consciously cut it?

What works: specific numbers from own experience, extends the idea with an unexpected angle (meetings disappeared), closes with a real question that invites a reply. High chance of profile visit, very high chance of a reply-to-your-reply (the compounding signal).

---

### Example 6: Thread-vibe matching in a casual comment thread

Post: *"We cut our engineering hiring in half this year and shipped more features than the year before."*

Comment thread vibe: casual, 1–3 lines, conversational, no formal punctuation.

**Bad comment (ignores vibe — reads like a formal reply):**
> This is a fascinating observation that aligns with research on team efficiency. Smaller, more focused teams often outperform larger ones due to reduced coordination overhead and clearer ownership boundaries.

**Good comment (matches casual vibe, 1 natural imperfection):**
> Same here — went from 22 to 14 and honestly the velocity went up
>
> I think we just stopped having meetings to coordinate the coordination

What works: matches the short/casual register of the thread, missing period at the end of line 1 reads natural, adds a specific angle (meta-meetings) without lecturing.

---

### Example 7: Comment with calibrated imperfection (professional thread)

Post: *"I lost a $40k deal last week because of a single sentence in my email."*

Comment thread vibe: professional, 3–5 lines, full sentences, sharing real experiences.

**Bad comment (over-imperfected for a professional thread):**
> omg yeah this happens all the time lol, we had the same thing happen and it was kinda embarrassing tbh

**Good comment (low imperfection, matches professional register):**
> Had the exact same thing happen with "future-proof architecture" in a proposal.
>
> The client read it as "you're not ready for us yet." We meant it as a selling point.
>
> Now we only mention scale if they bring it up first.

What works: one missing article (`[the] exact same thing` → `the exact same thing` — actually clean here, which is right for a professional thread), specific parallel experience, concrete lesson, no imperfections because the register doesn't call for them.

---

## References

- AgentSkills spec: https://agentskills.io/specification
- Companion skill: `content-voice` — essential for stripping LinkedIn-dialect cliché
- Companion skill: `content-humanize` — use when rewriting AI-generated LinkedIn drafts
