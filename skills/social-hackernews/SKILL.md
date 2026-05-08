---
name: social-hackernews
title: "Hacker News Publishing Playbook"
description: "Ground-truth 2026 playbook for submitting and commenting on Hacker News. Covers the reverse-engineered ranking formula, the five post types (Show HN, Ask HN, Launch HN, Tell HN, regular submission) with their exact title conventions, the mandatory first-comment pattern for Show HN, moderation (flags, vouches, mailing the mods), voting-ring detection, and how to write titles that don't read as marketing. Activate when drafting anything for Hacker News."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Hacker News (news.ycombinator.com)."
domains: content
rules:
  - content(hackernews)
  - match(\bhacker\s+news\b)
  - match(\bshow\s+HN\b)
  - match(\bask\s+HN\b)
  - match(\blaunch\s+HN\b)
  - match(\btell\s+HN\b)
  - match(\bpost\s+(on|to|for)\s+HN\b)
  - match(\by\s*combinator\b)
  - match(\bycombinator\b)
---

## Overview

Hacker News is unlike every other social platform. No feed personalization, no hashtags, no follower count, no algorithm-for-you. Every user sees the same front page. One post ships per slot and the ranking is pure: early upvotes, steep time decay, penalties for anything that reads as marketing. Of every platform covered in these skills, HN is the most allergic to promotional tone and the most rewarding when a post lands.

Pair with `content-voice` for human voice. HN readers — skilled engineers, researchers, founders — detect AI-generated and marketing text within the first line.

## Instructions

### The 2026 Ranking Algorithm (reverse-engineered from Arc source)

HN's front page ranking uses a simple formula derived from the open Arc source:

```
score = ((points - 1) ^ 0.8) / ((age_in_hours + 2) ^ gravity) × penalties
```

- Gravity ≈ 1.8 — the time-decay exponent. Posts lose ranking steeply; after 24 hours almost nothing recovers.
- Points exponent 0.8 — diminishing returns on raw upvotes. Going from 10 → 20 points matters more than going from 100 → 200.
- Penalties — applied opaquely by mods or heuristics; can halve or eighth a post's effective score. Triggers include: promotional language, domain flagging, flagged-by-users, too many comments-per-point ratio (signals controversy), voting rings.

Practical implications:
1. The first 1–2 hours on `/newest` decide everything. If you don't get ~5 upvotes in the first 30 minutes, you're buried under the next 500 submissions.
2. "Rich get richer" dynamic. A lucky early upvote cascade can push a mediocre post high; a great post posted at the wrong hour can die in `/newest` with zero visibility.
3. You can't farm HN. No hashtags to game, no follow-graph to hack, no engagement bait that works. The only lever is genuinely good content + good title + good timing + a non-zero amount of luck.

### The Five Post Types (and their exact conventions)

HN has strict naming conventions. Violating them results in the mods re-titling or killing your post.

| Type | Prefix | Use for | Title example |
|---|---|---|---|
| Regular submission | (none) | Linking to an article, blog post, paper, repo, video | Observations on a 500-day project in Rust |
| Show HN | `Show HN:` | Something you built that others can try | Show HN: A terminal file manager written in Zig |
| Ask HN | `Ask HN:` | Question for the community (self-post, no link) | Ask HN: How do you evaluate long-context LLMs? |
| Tell HN | `Tell HN:` | Short announcement or observation (self-post) | Tell HN: HN front page is unreachable from EU today |
| Launch HN | `Launch HN:` | YC-backed companies only (coordinated with YC) | Launch HN: Acme (YC W25) – SDK for audio diffusion |

Do not use `Launch HN:` unless you are actually a YC company with a launch scheduled. Mods will remove it.

### Tell HN and Launch HN

Both have specific rules — see `reference/post-types.md` for full detail. Quick guidance:

- Tell HN is for short factual announcements only (outages, vulnerabilities, HN changes). Under 300 words. NOT for "I built a thing" (use Show HN), "thoughts on X" (submit a blog), or hiring (use the monthly thread).
- Launch HN is YC-only and YC-scheduled. Don't self-declare. First comment has a 6-section structure (what / problem / how / traction / help-needed / try-it).

### Title Craft (the most important part)

HN titles do 80% of the work. Rules, in priority order:

1. If linking to an article, use the article's original title. Paraphrasing or editorializing gets flagged by users and re-titled by mods.
2. Drop the site name. `"My post title - Dan's Blog"` → `"My post title"`. Always.
3. No clickbait phrasing. No "You won't believe," no "This one trick," no "10 things every engineer should know."
4. No marketing adjectives. Kill: revolutionary, game-changing, powerful, advanced, amazing, groundbreaking, cutting-edge, ultimate, best-in-class.
5. No question marks unless it's an Ask HN or the article literally asks a question.
6. No exclamation marks. Ever.
7. No emoji. Not even for icons.
8. No ALL CAPS words except proper acronyms (API, LLM, GPU).
9. Neutral, factual, curious-hacker tone. "How we cut our AWS bill 73% in one weekend" beats "We saved $$$: the secret to cloud cost optimization."
10. Specificity wins. Numbers, versions, exact tech, timeframes are all positive signals to HN readers.
11. Under ~80 characters. HN truncates beyond that.

### URL submission and duplicates

Quick rules: canonical URLs only (strip UTM/ref/AMP/Medium-sk tracking), no link shorteners, no redirect chains, no paywalled URLs (use archive.today instead and mention in first comment), GitHub repo root not a file path, YouTube only if explained in first comment. Same URL within ~6 months = duplicate, redirects to old thread. Cross-posting acceptable but rewrite titles per platform; never copy-paste first comments.

Full URL hygiene + duplicate-detection edge cases: see `reference/post-types.md`.

### Body Craft (for Ask HN, Tell HN, and self-posts)

HN self-posts live or die by the body text. Unlike link submissions where the article carries the weight, here your writing is the entire experience.

Structure for Ask HN:
1. Restate the core question in one sentence — many readers skim titles; the body should make the question unmissable.
2. Context, not autobiography. "We have 5M support tickets in Postgres" is context. "I started coding at 12 and have always been passionate about..." is autobiography. HN hates the latter.
3. What you've already tried. This is mandatory. "I looked at X and Y but they don't handle Z" shows effort and prevents low-effort "have you tried Google?" responses.
4. Specific constraints. Performance budgets, compliance requirements, team size — these shape useful answers.
5. What a good answer looks like. "I'm looking for war stories from production, not theoretical comparisons" sets the frame.

Structure for Tell HN:
1. Lead with the news. "HN front page is unreachable from EU today due to a Cloudflare routing issue."
2. Evidence, not outrage. Screenshots, traceroutes, specific error codes. HN is a technical audience — they want data.
3. No call to action. Tell HN is not Show HN. Don't end with "check out my project" or "sign up for updates."
4. Keep it under 300 words. Tell HN is for short announcements. If it needs more, it's an article — submit the article instead.

Formatting:
- Use blank lines between paragraphs. Wall-of-text posts get ignored.
- Use `code` formatting for commands, error messages, or short snippets.
- Use bullet points for lists of 3+ items.
- No bold or italic abuse. One or two emphasized phrases per post maximum.
- No images in self-posts. HN doesn't support inline images; link to them if essential.

### Show HN — Specific Rules (and the mandatory first comment)

Show HN is for things you built and want feedback on. Follow the official format or mods kill the post.

Title: `Show HN: [what it is]`
- Not `Show HN: MyProduct – the revolutionary X`
- Yes: `Show HN: A static site generator written in OCaml`
- Yes: `Show HN: I built a CLI to search AWS resources by tag`

The first comment (posted by you, within ~1 minute of submission) is mandatory for Show HN. It's not optional — the community expects it and you will get roasted if you don't. It should include:

1. What it is — 1–2 sentences, plain English
2. Why you built it — the itch, the missing tool, the problem
3. Tech stack / interesting implementation detail — HN audience reads this
4. What's not working yet / where you want feedback — honest about limits
5. How to try it — install command, hosted demo link, whatever is lowest-friction

Do NOT in the first comment:
- Ask for upvotes (instant voting-ring flag)
- Use marketing language
- Include promotional links beyond the core project
- Shill affiliated services

First-comment template (adapt, don't copy):
```
Hey HN — built this because [specific personal itch / missing tool].

It's a [one-line description] written in [language]. The interesting part of the implementation is [specific technical detail that HN readers will find interesting — a datastructure, an optimization, an unusual architecture].

Currently it handles [X] but [Y] is not yet implemented and I'd especially love feedback on [specific thing]. Happy to answer questions about [technical area].

Repo: [link]
```

### Ask HN — Specific Rules

Ask HN is for genuine questions, no link in the URL field. It's a self-post.

- Title IS the question. Not "Ask HN: I have a question about X" — just ask it. "Ask HN: How do you structure config files in a polyglot monorepo?"
- Body is context. What you've tried, what you've ruled out, what specifically you want help with.
- Don't use Ask HN as disguised promotion — "Ask HN: How can we improve [MyProduct]?" gets flagged instantly.

### Moderation You Need to Know

- Flagged posts disappear from `/newest` and the front page. Usually triggered by multiple users hitting the flag link — often for marketing tone, duplicate submissions, political content, or being off-topic for HN.
- Dead posts (shown as `[dead]` to logged-in users, invisible otherwise) were removed by the software or a mod. Can sometimes be resurrected by mods if you email hn@ycombinator.com politely.
- Hellban / shadowban — your account posts but no one sees them. Usually triggered by voting-ring behavior or repeated rule violations. Hard to recover from.
- Vouches — users with enough karma can vouch for a flagged/dead post to revive it. You can't vouch for your own posts.
- Emailing mods — `hn@ycombinator.com`, polite, short, with the post URL. Works more often than you'd think if the post was clean and got caught by a heuristic. Do NOT email for "boost my post."

### Voting Rings and Account Trust

HN's single biggest anti-gaming focus. Never do any of these:

- Ask friends, teammates, or Twitter/Slack groups to upvote
- Post a link to your submission with "please upvote" anywhere, ever
- Have multiple accounts (detected by IP, browser fingerprint, posting patterns)
- Coordinate simultaneous posting/upvoting with others
- Create an account solely to submit your own link

All of these trigger voting-ring detection, which typically hellbans every involved account permanently. HN is serious about this and good at detecting it.

The only legitimate pre-submission move: post the URL in your own newsletter/network, mention "it's on HN" without asking for upvotes or linking the HN submission directly. Let people find it organically.

### Account warmup and karma

New accounts are heavily throttled — a brand-new account submitting its own project is a voting-ring red flag. First 30 days: don't submit your own content, comment substantively on others' posts in your domain, target 50+ karma before first self-promotion, avoid early downvotes (low-trust bucket is hard to escape).

Full karma mechanics, unlock thresholds, and new-account red flags: see `reference/post-types.md`.

### Timing

- Best windows for English-speaking tech audience: weekday mornings 8–11 AM ET (US east coast awake, Europe late afternoon).
- Tuesday–Thursday tend to be best days; weekends are quieter but less competitive.
- Late-night ET / early morning European time is a decent second-chance window.
- Timing is contested — Ken Shirriff's ranking analyses show variance, and a truly good post can break through most times. But bad timing + mediocre hook = invisible.

### What Gets a Post Flagged — by Severity

HN penalties are not binary. Understanding the tiers helps you calibrate risk.

Instant death (software or mods kill within minutes, often with hellban risk):
- Voting-ring detection (coordinated upvotes, multiple accounts, same IP)
- First comment asking for upvotes — automatic flag + account review
- Duplicate URL submitted within ~6 months — redirects to old thread
- `Launch HN:` by a non-YC company — retitled or removed by mods
- Political / culture-war content — HN is aggressively moderated here
- Job postings outside the monthly "Who is hiring?" threads

Heavy algorithmic penalty (score halved or worse; usually dies on `/newest`):
- Marketing adjectives in title ("revolutionary," "game-changing," "ultimate")
- Exclamation marks, emoji, or ALL CAPS words in title
- Clickbait or editorialized title (paraphrasing instead of original)
- Newsletter signup wall or hard paywall as the linked URL
- Landing page with only a product pitch and no technical substance
- Low-quality AI-generated content — HN readers detect this within lines

Community flagging (users hit "flag," post drops from front page):
- Self-promotion without substance (5 blog posts in 2 weeks all linking your product)
- Off-topic for HN — lifestyle, general business advice, personal journeys without technical angle
- Surveys and polls — read as low-effort data collection unless academically rigorous
- Previously flopped content resubmitted too soon (< 6 months)
- "I quit my job to build X" — overplayed narrative, flagged as self-promotion

### When NOT to Post

Some topics are effectively banned by community norms even if not in the written guidelines. Save yourself the flag:

- Crypto / NFT / Web3 speculation — unless it's a technical deep-dive on consensus algorithms or cryptography, it gets flagged.
- Political culture war — even tangential mentions get flagged. HN moderates this harder than almost any topic.
- Job postings — use the monthly "Who is hiring?" thread. Standalone job posts get killed.
- Surveys and polls — unless academically rigorous with methodology disclosed.
- "I quit my job to build X" — overplayed narrative, usually flagged as self-promotion.
- Listicles — "10 things every developer should know" is universally hated on HN.
- AI-generated content without human curation — HN readers detect this instantly and flag hard.
- Personal blog posts with no technical substance — "My journey learning Rust" rarely does well unless it contains genuinely novel technical observations.
- YouTube Shorts / TikTok-style content — HN is text-first. Short-form video gets flagged.

### Comment Strategy

On other people's posts:
- Substantive first. HN's comment ranking values thoughtfulness; one-liners get downvoted fast.
- Cite specifics. "Having run this in production at X scale, we found Y" is gold.
- Disagree politely with reasons. "I don't think this holds because…" beats "This is wrong."
- Assume good faith. HN's comment culture explicitly requires it — mods enforce.
- Don't name-call, don't dunk, don't rage-post. You'll be banned faster than anywhere else.
- Cite sources for factual claims. Engineers on HN check.
- Don't fabricate specifics to sound credible. A fake-precise claim ("ran this in production at a 10k-employee bank", "we hit 99.999% uptime") attracts replies asking which bank or which SLO calculation, and the silence that follows is what damages your account. A vague-but-honest comment ("from what I've read on this") survives. A fake-specific one gets dunked on, and the dunk is what classifier bots and mods escalate on.

On your own posts (especially Show HN):
- Respond to every substantive comment for the first 2–3 hours.
- Treat critical feedback as the point. Most useful comments are negative.
- Correct your own mistakes openly. "You're right, I was wrong about X" earns karma.

### Responding to Criticism on Your Own Posts

HN's culture is direct, technical, and allergic to defensiveness. Negative comments are often the most valuable.

- Never get defensive. "You don't understand" or "You clearly didn't read it" kills your karma and the thread.
- Assume the critic is right until proven otherwise. "You're right that X is a problem. We tried Y and it failed because Z. Open to better ideas."
- Don't argue with every comment. Pick the substantive ones. Ignore drive-by negativity.
- If someone finds a real bug or error: thank them publicly, fix it, and comment back with the fix. This is karma gold on HN.
- If the criticism is about your business model: engage honestly about trade-offs. HN respects "we chose X over Y because Z, knowing the downside is W."
- Never delete comments. HN has no delete. Editing is limited to a short window. What you post stays.

### Pre-Publish Checklist

- [ ] Title follows the type convention (Show HN / Ask HN / plain / Tell HN / Launch HN)
- [ ] Title is neutral, specific, no marketing adjectives, no exclamation marks, no emoji
- [ ] If linking an article: using the original title, site name stripped
- [ ] Posted the URL not the AMP/tracking version
- [ ] No "please upvote" anywhere, including other channels
- [ ] For Show HN: first comment drafted and ready to post within 1 minute of submission
- [ ] For Ask HN: real question in the title, real context in the body
- [ ] Timing: weekday 8–11 AM ET or best-available slot
- [ ] Account is established (30+ days, non-zero karma) — new accounts get throttled
- [ ] Ready to engage with comments for 2–3 hours after posting
- [ ] If the post dies: know the hn@ycombinator.com email and when it's legitimate to use it
- [ ] Comment only: scanned the existing comment tree for depth and tone before writing
- [ ] Comment only: 0–1 structural imperfection only (informal phrasing, casual aside) — no typos

### Thread-Vibe Matching (Comments)

Before commenting, read the existing comment tree — not just the top-level comments but the depth. HN threads develop a specific intellectual register within the first 10–20 comments, and deviating from it reads as out-of-place.

What to scan:
- Depth of technical detail — are people citing papers, benchmarks, production numbers? Match that depth.
- Comment length — 2-sentence quips or 5-paragraph mini-essays? Match the median.
- Tone — skeptical/analytical, warm/collaborative, or heated/contested? Adjust accordingly.
- Whether the thread is already contested — if there's a flame war forming, either add something genuinely de-escalating or stay out.
- Existing answers — don't repeat what's already been said well. Add or extend.

Vibe calibration by thread type:

| Thread type | Comment vibe |
|---|---|
| Technical deep-dive (Show HN, paper) | Match the depth; cite specifics, production numbers, versions |
| Ask HN (genuine question) | Answer directly; show your work; "we did X and found Y" |
| Contested claim / debate | Measured, specific disagreement; cite sources; no contempt |
| Personal story / retrospective | Warmer; share a parallel experience; shorter |
| News / announcement | Factual extension or question; no hype either direction |

### Human Imperfection Protocol

HN is the most formal platform in this set. Comments are essentially mini-essays — readers are engineers, researchers, and founders who notice both AI-polished prose and careless typos. The goal is structural informality, not visible sloppiness.

Key HN nuance: typos read as careless, not human. On HN, a typo in a technical term signals you don't know the domain. Imperfections should be structural — informal phrasing, a sentence fragment, a casual aside in parentheses — not spelling errors.

Imperfection level by content type:

| Content type | Level | What that means |
|---|---|---|
| Submission title | Zero | Titles are edited artifacts; zero imperfections |
| Show HN first comment | Zero | This is your pitch; zero imperfections |
| Ask HN body | Very low | 0–1 structural imperfection max |
| Comment on others' posts | Very low | 1 structural imperfection; no typos |
| Reply in a casual/warm thread | Low | 1 structural imperfection; slightly more informal phrasing |

Imperfection menu for HN (pick 0–1 per comment, structural only):

- Casual aside in parentheses — `(worth checking if yours went dark)` — very HN-native; engineers write like this
- Sentence fragment as emphasis — `Not a typo. The whole thing.` — used for emphasis, reads as deliberate
- "though" / "honestly" / "actually" — casual qualifiers that read as human hedging
- Informal opener — `Ran into this exact thing last year.` instead of `I encountered this issue last year.`
- Dropped subject — `Tried X, didn't work.` instead of `I tried X and it didn't work.` — common in technical writing
- Em-dash used informally — `The fix was one line — and it was embarrassing.` — reads as thinking-while-typing

Never do on HN:
- Typos in technical terms, library names, language names, or proper nouns — credibility damage is severe
- `lol`, `lmao`, `tbh`, `ngl` — too casual for HN register in almost all threads
- Emoji in comments — HN culture treats this as low-effort
- Stack 2+ imperfections in one comment — reads as careless
- Imperfections in a Show HN first comment or submission title — these are edited artifacts

Calibration check before posting:
1. Is this a title, first comment, or a reply? Titles and first comments = zero imperfections.
2. Read the existing thread — what's the depth and formality level?
3. Does your comment have 0–1 structural imperfections (informal phrasing, not typos)?
4. Would a senior engineer typing this between tasks plausibly have written exactly this?

## Examples

### Example 1: Show HN first comment

Bad (marketing, asks for upvotes, no substance):
> Hey HN! 🎉 Super excited to share TurboForms! We've been working SO hard on this. Would love your support and upvotes!! Check it out at turboforms.io — it's a game-changer for form building!

Good (substantive, technical, asks for real feedback):
> Hey HN — built this because every form builder I tried (Typeform, Tally, custom in-app ones) either forced a JS runtime on my users' sites or had vendor lock-in I couldn't stomach.
>
> It outputs raw HTML + a tiny amount of progressive-enhancement JS (optional, adds inline validation). Server-side it's Elixir + a SQLite-per-tenant architecture — happy to talk about why I went with that over Postgres, it was a real trade-off.
>
> Currently handles single-step forms well. Multi-step and conditional logic are half-done and I'd love feedback on whether the DSL I'm prototyping (shown on the /experimental page) is reasonable or cursed.
>
> Demo: https://example.com
> Repo: https://github.com/me/project

What works: personal itch, technical specifics HN cares about (SQLite-per-tenant is interesting), honest about what's not done, asks for specific feedback, no marketing language, no upvote ask.

### Example 2: Ask HN

Bad (vague, unanswerable):
> Ask HN: Any advice for a startup founder?

Bad (disguised promotion):
> Ask HN: What would you want in a CRM built for freelancers? (I'm building one)

Good (specific, shows effort, has context):
> Ask HN: How do you evaluate long-context LLMs for retrieval tasks?
>
> Context: we have ~5M support tickets in Postgres, and I've been testing Claude 3.7 (200k), GPT-4.1 (128k), and Gemini 2.0 (1M) for "find similar tickets" workflows.
>
> Benchmarks I've tried: needle-in-haystack (shows little about real retrieval), RAG-bench (synthetic), LongBench (helpful but old). What I'm struggling with: building an eval that reflects our actual query distribution without hand-labeling thousands of ticket pairs.
>
> Has anyone built domain-specific LC-LLM evals they can talk about? Especially interested in how you decided when the eval was "good enough" to trust.

What works: real question, specific setup, shows prior work, asks something experts can actually answer from their own experience. Will attract the right kind of comment thread.

### Example 3: Post that flops and why

Submission:
> Show HN: Revolutionary AI-Powered SaaS Analytics Platform That Will Transform Your Business 🚀🔥

First comment:
> Hi everyone! We built this to help businesses leverage AI! Please check out our landing page and let us know what you think! Upvotes appreciated 🙏

Why this dies in under 10 minutes: title has `Revolutionary`, `AI-Powered`, `Transform Your Business`, two emoji, no specifics. First comment asks for upvotes, has no substance, no tech stack, no real problem description. Flagged within the first 5 users; hellban risk for "Upvotes appreciated." Mods remove, account reputation damaged.

For more examples (Show HN title patterns, linked-article titles, thread-vibe matching, calibrated imperfection in Ask HN), see `reference/examples.md`.

## References

- AgentSkills spec: https://agentskills.io/specification
- HN guidelines: https://news.ycombinator.com/newsguidelines.html
- HN FAQ: https://news.ycombinator.com/newsfaq.html
- Ranking source (Arc): https://github.com/wting/hackernews/blob/master/news.arc
- Contact mods: hn@ycombinator.com
- Companion skill: `content-voice` — HN is the hardest platform for sounding human; voice rules are essential
