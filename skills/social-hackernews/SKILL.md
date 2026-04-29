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

# Hacker News Publishing Playbook

## Overview

Hacker News is unlike every other social platform. No feed personalization, no hashtags, no follower count, no algorithm-for-you. Every user sees the same front page. One post ships per slot and the ranking is pure: early upvotes, steep time decay, penalties for anything that reads as marketing. Of every platform covered in these skills, HN is the most allergic to promotional tone and the most rewarding when a post lands.

Pair with `content-voice` for human voice. HN readers — skilled engineers, researchers, founders — detect AI-generated and marketing text within the first line.

---

## Instructions

### The 2026 Ranking Algorithm (reverse-engineered from Arc source)

HN's front page ranking uses a simple formula derived from the open Arc source:

```
score = ((points - 1) ^ 0.8) / ((age_in_hours + 2) ^ gravity) × penalties
```

- **Gravity ≈ 1.8** — the time-decay exponent. Posts lose ranking steeply; after 24 hours almost nothing recovers.
- **Points exponent 0.8** — diminishing returns on raw upvotes. Going from 10 → 20 points matters more than going from 100 → 200.
- **Penalties** — applied opaquely by mods or heuristics; can halve or eighth a post's effective score. Triggers include: promotional language, domain flagging, flagged-by-users, too many comments-per-point ratio (signals controversy), voting rings.

**Practical implications:**
1. **The first 1–2 hours on `/newest` decide everything.** If you don't get ~5 upvotes in the first 30 minutes, you're buried under the next 500 submissions.
2. **"Rich get richer" dynamic.** A lucky early upvote cascade can push a mediocre post high; a great post posted at the wrong hour can die in `/newest` with zero visibility.
3. **You can't farm HN.** No hashtags to game, no follow-graph to hack, no engagement bait that works. The only lever is genuinely good content + good title + good timing + a non-zero amount of luck.

---

### The Five Post Types (and their exact conventions)

HN has strict naming conventions. Violating them results in the mods re-titling or killing your post.

| Type | Prefix | Use for | Title example |
|---|---|---|---|
| **Regular submission** | (none) | Linking to an article, blog post, paper, repo, video | *Observations on a 500-day project in Rust* |
| **Show HN** | `Show HN:` | Something you built that others can try | *Show HN: A terminal file manager written in Zig* |
| **Ask HN** | `Ask HN:` | Question for the community (self-post, no link) | *Ask HN: How do you evaluate long-context LLMs?* |
| **Tell HN** | `Tell HN:` | Short announcement or observation (self-post) | *Tell HN: HN front page is unreachable from EU today* |
| **Launch HN** | `Launch HN:` | YC-backed companies only (coordinated with YC) | *Launch HN: Acme (YC W25) – SDK for audio diffusion* |

Do not use `Launch HN:` unless you are actually a YC company with a launch scheduled. Mods will remove it.

---

### Tell HN — Expanded Rules

Tell HN is the most misused prefix. It's for short, factual announcements — not mini blog posts, not product pitches, not opinion pieces.

**What Tell HN IS for:**
- Service outages affecting HN or major tech infrastructure
- Security vulnerabilities with public disclosure
- Changes to HN itself (new features, policy updates)
- Short factual observations about the tech industry
- Corrections to previously submitted stories

**What Tell HN is NOT for:**
- "Tell HN: I built a thing" → that's Show HN
- "Tell HN: My thoughts on AI" → that's a blog post, submit the link
- "Tell HN: We're hiring" → use the monthly "Who is hiring?" thread
- "Tell HN: Please support our Kickstarter" → instant flag

**Tell HN title rules:**
- Lead with the fact, not the source. "Tell HN: GitHub Actions is down in us-east-1" not "Tell HN: GitHub says Actions is down"
- No editorializing. "Tell HN: AWS us-east-1 is down again" → "again" is editorializing. "Tell HN: AWS us-east-1 experiencing outages" is neutral.
- Include timeframe if known. "Tell HN: Cloudflare 522 errors since 14:00 UTC"

**Tell HN body rules:**
- Under 300 words. If it needs more, write an article and submit the link.
- Evidence first. Screenshots, status page links, specific error codes.
- No call to action. Don't end with "check out my monitoring tool that caught this."
- Update the body (not a new comment) as the situation evolves. HN supports editing.

---

### Launch HN — Expanded Rules (for YC companies only)

Launch HN is a coordinated program run by Y Combinator. You cannot self-declare a Launch HN.

**How it works:**
- YC schedules your launch with the HN mods. You don't pick the date unilaterally.
- The title format is strict: `Launch HN: CompanyName (YC W25) – one-line description`
- The batch code (W25, S24, etc.) is required. Mods add it if you forget.
- Launch HN posts get a special tag and often appear in the "Launches" section of HN.

**Launch HN first comment (different from Show HN):**
1. **What the company does** — 1 sentence, plain English
2. **The problem you're solving** — not "the market is huge" but "engineers waste 3 hours a week on X"
3. **How it works** — technical specifics, architecture, interesting implementation
4. **Traction so far** — users, revenue, growth rate. HN respects numbers.
5. **What you need help with** — hiring, beta testers, specific technical feedback
6. **How to try it** — demo link, signup, open-source repo

**Launch HN timing:**
- Usually scheduled for Tuesday or Wednesday mornings ET
- YC coordinates this; don't try to game it
- The launch window is your one shot — prepare the first comment in advance

**Launch HN pitfalls:**
- Don't use Launch HN if you're not YC-backed. Mods will retitle or kill it.
- Don't post a Launch HN without YC scheduling it. It won't get the special treatment and may be flagged.
- Don't treat it as a press release. HN readers want technical depth, not marketing.

---

### Title Craft (the most important part)

HN titles do 80% of the work. Rules, in priority order:

1. **If linking to an article, use the article's original title.** Paraphrasing or editorializing gets flagged by users and re-titled by mods.
2. **Drop the site name.** `"My post title - Dan's Blog"` → `"My post title"`. Always.
3. **No clickbait phrasing.** No "You won't believe," no "This one trick," no "10 things every engineer should know."
4. **No marketing adjectives.** Kill: revolutionary, game-changing, powerful, advanced, amazing, groundbreaking, cutting-edge, ultimate, best-in-class.
5. **No question marks unless it's an Ask HN** or the article literally asks a question.
6. **No exclamation marks. Ever.**
7. **No emoji.** Not even for icons.
8. **No ALL CAPS words** except proper acronyms (API, LLM, GPU).
9. **Neutral, factual, curious-hacker tone.** "How we cut our AWS bill 73% in one weekend" beats "We saved $$$: the secret to cloud cost optimization."
10. **Specificity wins.** Numbers, versions, exact tech, timeframes are all positive signals to HN readers.
11. **Under ~80 characters.** HN truncates beyond that.

---

### URL Submission Rules

HN moderators and users punish sloppy link hygiene. Get the URL right:

- **Submit the canonical URL.** No `?utm_source=`, no `ref=`, no tracking parameters. Strip them all.
- **No AMP links.** Submit the publisher's original URL, not the Google AMP cache version.
- **No Medium / Substack tracking suffixes.** `?sk=abc123` and similar — strip them.
- **No paywalled URL as the primary link.** If the article is paywalled, submit the unpaywalled version (archive.today, Ghostreader, or the author's own non-paywalled mirror) and mention the paywall in the first comment. HN readers flag paywalls hard.
- **No link shorteners.** `bit.ly`, `t.co`, etc. are auto-flagged. Use the final destination URL.
- **No redirect chains.** If the URL redirects to a different domain, submit the final destination.
- **GitHub links:** submit the repo root, not a specific file path, unless the file itself is the story (e.g., a single-file project).
- **YouTube:** only if the video is the primary content and you explain why in the first comment. HN is text-first.

---

### Duplicate Detection & Cross-posting Etiquette

HN has built-in duplicate detection, but it's not perfect. Know the rules:

- **Same URL = duplicate.** If the URL was submitted in the last ~6 months, HN redirects to the old thread. You cannot force a new discussion.
- **Slightly different URLs bypass detection.** Adding or removing `www.`, `http` vs `https`, or a trailing slash can create a duplicate that mods later merge. Don't game this intentionally — users will flag it.
- **Cross-posting from Reddit / X / your blog:** acceptable, but space them out by at least 48 hours and rewrite the title for HN's audience. Never copy-paste the same first comment across platforms.
- **If your post flopped:** wait at least 3 months before resubmitting, and only if you have significantly improved the content or found a better angle. Resubmitting the same thing weekly is a fast path to a domain flag.
- **"Previously" etiquette:** if you're commenting on a thread about something you posted before, disclose it with a neutral "I posted this last month; the update is X."

---

### Body Craft (for Ask HN, Tell HN, and self-posts)

HN self-posts live or die by the body text. Unlike link submissions where the article carries the weight, here your writing is the entire experience.

**Structure for Ask HN:**
1. **Restate the core question in one sentence** — many readers skim titles; the body should make the question unmissable.
2. **Context, not autobiography.** "We have 5M support tickets in Postgres" is context. "I started coding at 12 and have always been passionate about..." is autobiography. HN hates the latter.
3. **What you've already tried.** This is mandatory. "I looked at X and Y but they don't handle Z" shows effort and prevents low-effort "have you tried Google?" responses.
4. **Specific constraints.** Performance budgets, compliance requirements, team size — these shape useful answers.
5. **What a good answer looks like.** "I'm looking for war stories from production, not theoretical comparisons" sets the frame.

**Structure for Tell HN:**
1. **Lead with the news.** "HN front page is unreachable from EU today due to a Cloudflare routing issue."
2. **Evidence, not outrage.** Screenshots, traceroutes, specific error codes. HN is a technical audience — they want data.
3. **No call to action.** Tell HN is not Show HN. Don't end with "check out my project" or "sign up for updates."
4. **Keep it under 300 words.** Tell HN is for short announcements. If it needs more, it's an article — submit the article instead.

**Formatting:**
- Use blank lines between paragraphs. Wall-of-text posts get ignored.
- Use `code` formatting for commands, error messages, or short snippets.
- Use bullet points for lists of 3+ items.
- No bold or italic abuse. One or two emphasized phrases per post maximum.
- No images in self-posts. HN doesn't support inline images; link to them if essential.

---

### Show HN — Specific Rules (and the mandatory first comment)

Show HN is for things you built and want feedback on. Follow the official format or mods kill the post.

**Title**: `Show HN: [what it is]`
- Not `Show HN: MyProduct – the revolutionary X`
- Yes: `Show HN: A static site generator written in OCaml`
- Yes: `Show HN: I built a CLI to search AWS resources by tag`

**The first comment (posted by you, within ~1 minute of submission) is mandatory for Show HN.** It's not optional — the community expects it and you will get roasted if you don't. It should include:

1. **What it is** — 1–2 sentences, plain English
2. **Why you built it** — the itch, the missing tool, the problem
3. **Tech stack / interesting implementation detail** — HN audience reads this
4. **What's not working yet / where you want feedback** — honest about limits
5. **How to try it** — install command, hosted demo link, whatever is lowest-friction

Do NOT in the first comment:
- Ask for upvotes (instant voting-ring flag)
- Use marketing language
- Include promotional links beyond the core project
- Shill affiliated services

**First-comment template (adapt, don't copy):**
```
Hey HN — built this because [specific personal itch / missing tool].

It's a [one-line description] written in [language]. The interesting part of the implementation is [specific technical detail that HN readers will find interesting — a datastructure, an optimization, an unusual architecture].

Currently it handles [X] but [Y] is not yet implemented and I'd especially love feedback on [specific thing]. Happy to answer questions about [technical area].

Repo: [link]
```

---

### Ask HN — Specific Rules

Ask HN is for genuine questions, no link in the URL field. It's a self-post.

- **Title IS the question.** Not "Ask HN: I have a question about X" — just ask it. "Ask HN: How do you structure config files in a polyglot monorepo?"
- **Body is context.** What you've tried, what you've ruled out, what specifically you want help with.
- **Don't use Ask HN as disguised promotion** — "Ask HN: How can we improve [MyProduct]?" gets flagged instantly.

---

### Moderation You Need to Know

- **Flagged posts** disappear from `/newest` and the front page. Usually triggered by multiple users hitting the flag link — often for marketing tone, duplicate submissions, political content, or being off-topic for HN.
- **Dead posts** (shown as `[dead]` to logged-in users, invisible otherwise) were removed by the software or a mod. Can sometimes be resurrected by mods if you email **hn@ycombinator.com** politely.
- **Hellban / shadowban** — your account posts but no one sees them. Usually triggered by voting-ring behavior or repeated rule violations. Hard to recover from.
- **Vouches** — users with enough karma can vouch for a flagged/dead post to revive it. You can't vouch for your own posts.
- **Emailing mods** — `hn@ycombinator.com`, polite, short, with the post URL. Works more often than you'd think if the post was clean and got caught by a heuristic. Do NOT email for "boost my post."

---

### Voting Rings and Account Trust

HN's single biggest anti-gaming focus. Never do any of these:

- Ask friends, teammates, or Twitter/Slack groups to upvote
- Post a link to your submission with "please upvote" anywhere, ever
- Have multiple accounts (detected by IP, browser fingerprint, posting patterns)
- Coordinate simultaneous posting/upvoting with others
- Create an account solely to submit your own link

All of these trigger voting-ring detection, which typically hellbans every involved account permanently. HN is serious about this and good at detecting it.

**The only legitimate pre-submission move:** post the URL in your own newsletter/network, mention "it's on HN" *without* asking for upvotes or linking the HN submission directly. Let people find it organically.

---

### Account Warmup & Karma Building

New accounts on HN are heavily throttled. A brand-new account submitting its own project is a voting-ring red flag. Build trust first:

**The first 30 days:**
- **Don't submit your own content.** Comment substantively on others' posts for at least 2–3 weeks.
- **Target 50+ karma before first self-promotion.** This is an informal threshold; below it, your submissions get less visibility and more scrutiny.
- **Comment on posts in your domain.** If you're launching a database tool, comment on database-related posts with genuine expertise. "We hit this exact issue at scale; the fix was X" builds recognition.
- **Avoid early downvotes.** One or two early downvotes can put your account in a low-trust bucket that's hard to escape. Be conservative in your first comments.

**Karma mechanics:**
- Karma = upvotes on your comments and posts, minus downvotes.
- Comment karma matters more than post karma for account trust.
- Downvotes on comments cost you karma. Downvotes on posts don't (but the post dies).
- There's no public karma leaderboard. It's purely for account trust and unlocks (vouching, flagging, downvoting).

**What unlocks with karma:**
- ~10 karma: ability to downvote comments
- ~30 karma: ability to flag posts
- ~500 karma: ability to vouch for dead posts
- Higher karma = more weight in voting (HN uses a trust-weighted system internally)

**Red flags for new accounts:**
- First action is a self-submission
- First comment is on your own post
- Rapid-fire commenting (looks like a bot)
- All comments are on posts you submitted
- Account created the same day as a Show HN

---

### Timing

- **Best windows** for English-speaking tech audience: weekday mornings **8–11 AM ET** (US east coast awake, Europe late afternoon).
- **Tuesday–Thursday** tend to be best days; weekends are quieter but less competitive.
- **Late-night ET / early morning European time** is a decent second-chance window.
- Timing is contested — Ken Shirriff's ranking analyses show variance, and a truly good post can break through most times. But bad timing + mediocre hook = invisible.

---

### What Gets a Post Flagged — by Severity

HN penalties are not binary. Understanding the tiers helps you calibrate risk.

**Instant death (software or mods kill within minutes, often with hellban risk):**
- Voting-ring detection (coordinated upvotes, multiple accounts, same IP)
- First comment asking for upvotes — automatic flag + account review
- Duplicate URL submitted within ~6 months — redirects to old thread
- `Launch HN:` by a non-YC company — retitled or removed by mods
- Political / culture-war content — HN is aggressively moderated here
- Job postings outside the monthly "Who is hiring?" threads

**Heavy algorithmic penalty (score halved or worse; usually dies on `/newest`):**
- Marketing adjectives in title ("revolutionary," "game-changing," "ultimate")
- Exclamation marks, emoji, or ALL CAPS words in title
- Clickbait or editorialized title (paraphrasing instead of original)
- Newsletter signup wall or hard paywall as the linked URL
- Landing page with only a product pitch and no technical substance
- Low-quality AI-generated content — HN readers detect this within lines

**Community flagging (users hit "flag," post drops from front page):**
- Self-promotion without substance (5 blog posts in 2 weeks all linking your product)
- Off-topic for HN — lifestyle, general business advice, personal journeys without technical angle
- Surveys and polls — read as low-effort data collection unless academically rigorous
- Previously flopped content resubmitted too soon (< 6 months)
- "I quit my job to build X" — overplayed narrative, flagged as self-promotion

---

### When NOT to Post

Some topics are effectively banned by community norms even if not in the written guidelines. Save yourself the flag:

- **Crypto / NFT / Web3 speculation** — unless it's a technical deep-dive on consensus algorithms or cryptography, it gets flagged.
- **Political culture war** — even tangential mentions get flagged. HN moderates this harder than almost any topic.
- **Job postings** — use the monthly "Who is hiring?" thread. Standalone job posts get killed.
- **Surveys and polls** — unless academically rigorous with methodology disclosed.
- **"I quit my job to build X"** — overplayed narrative, usually flagged as self-promotion.
- **Listicles** — "10 things every developer should know" is universally hated on HN.
- **AI-generated content without human curation** — HN readers detect this instantly and flag hard.
- **Personal blog posts with no technical substance** — "My journey learning Rust" rarely does well unless it contains genuinely novel technical observations.
- **YouTube Shorts / TikTok-style content** — HN is text-first. Short-form video gets flagged.

---

### Comment Strategy

On other people's posts:
- **Substantive first.** HN's comment ranking values thoughtfulness; one-liners get downvoted fast.
- **Cite specifics.** "Having run this in production at X scale, we found Y" is gold.
- **Disagree politely with reasons.** "I don't think this holds because…" beats "This is wrong."
- **Assume good faith.** HN's comment culture explicitly requires it — mods enforce.
- **Don't name-call, don't dunk, don't rage-post.** You'll be banned faster than anywhere else.
- **Cite sources for factual claims.** Engineers on HN check.

On your own posts (especially Show HN):
- Respond to every substantive comment for the first 2–3 hours.
- Treat critical feedback as the point. Most useful comments are negative.
- Correct your own mistakes openly. "You're right, I was wrong about X" earns karma.

---

### Responding to Criticism on Your Own Posts

HN's culture is direct, technical, and allergic to defensiveness. Negative comments are often the most valuable.

- **Never get defensive.** "You don't understand" or "You clearly didn't read it" kills your karma and the thread.
- **Assume the critic is right until proven otherwise.** "You're right that X is a problem. We tried Y and it failed because Z. Open to better ideas."
- **Don't argue with every comment.** Pick the substantive ones. Ignore drive-by negativity.
- **If someone finds a real bug or error:** thank them publicly, fix it, and comment back with the fix. This is karma gold on HN.
- **If the criticism is about your business model:** engage honestly about trade-offs. HN respects "we chose X over Y because Z, knowing the downside is W."
- **Never delete comments.** HN has no delete. Editing is limited to a short window. What you post stays.

---

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

---

## Examples

### Example 1: Show HN title

**Bad (marketing, adjectives, exclamation):**
> Show HN: TurboForms - The Ultimate Form Builder for Modern SaaS 🚀!

**Bad (too vague, no information):**
> Show HN: My new side project

**Good (specific, neutral, informative):**
> Show HN: A form builder that outputs raw HTML and zero JavaScript

What works: says exactly what it does, has a specific technical angle (no JS) that HN readers will find interesting, no adjectives, no marketing.

---

### Example 2: Show HN first comment

**Bad (marketing, asks for upvotes, no substance):**
> Hey HN! 🎉 Super excited to share TurboForms! We've been working SO hard on this. Would love your support and upvotes!! Check it out at turboforms.io — it's a game-changer for form building!

**Good (substantive, technical, asks for real feedback):**
> Hey HN — built this because every form builder I tried (Typeform, Tally, custom in-app ones) either forced a JS runtime on my users' sites or had vendor lock-in I couldn't stomach.
>
> It outputs raw HTML + a tiny amount of progressive-enhancement JS (optional, adds inline validation). Server-side it's Elixir + a SQLite-per-tenant architecture — happy to talk about why I went with that over Postgres, it was a real trade-off.
>
> Currently handles single-step forms well. Multi-step and conditional logic are half-done and I'd love feedback on whether the DSL I'm prototyping (shown on the /experimental page) is reasonable or cursed.
>
> Demo: https://example.com
> Repo: https://github.com/me/project

What works: personal itch, technical specifics HN cares about (SQLite-per-tenant is interesting), honest about what's not done, asks for specific feedback, no marketing language, no upvote ask.

---

### Example 3: Ask HN

**Bad (vague, unanswerable):**
> Ask HN: Any advice for a startup founder?

**Bad (disguised promotion):**
> Ask HN: What would you want in a CRM built for freelancers? (I'm building one)

**Good (specific, shows effort, has context):**
> Ask HN: How do you evaluate long-context LLMs for retrieval tasks?
>
> Context: we have ~5M support tickets in Postgres, and I've been testing Claude 3.7 (200k), GPT-4.1 (128k), and Gemini 2.0 (1M) for "find similar tickets" workflows.
>
> Benchmarks I've tried: needle-in-haystack (shows little about real retrieval), RAG-bench (synthetic), LongBench (helpful but old). What I'm struggling with: building an eval that reflects our actual query distribution without hand-labeling thousands of ticket pairs.
>
> Has anyone built domain-specific LC-LLM evals they can talk about? Especially interested in how you decided when the eval was "good enough" to trust.

What works: real question, specific setup, shows prior work, asks something experts can actually answer from their own experience. Will attract the right kind of comment thread.

---

### Example 4: Title for a linked article

You're submitting: `"Why we moved from Kubernetes to Nomad: a 12-month retrospective - InternalDevBlog"`

**Bad (kept site name, re-phrased):**
> Why our team left Kubernetes for Nomad (awesome retrospective!)

**Good (article's original title, site stripped, no editorializing):**
> Why we moved from Kubernetes to Nomad: a 12-month retrospective

HN rule: use the original title unless it's misleading or clickbait. Strip the site name. No commentary.

---

### Example 5: Post that flops and why

Submission:
> Show HN: Revolutionary AI-Powered SaaS Analytics Platform That Will Transform Your Business 🚀🔥

First comment:
> Hi everyone! We built this to help businesses leverage AI! Please check out our landing page and let us know what you think! Upvotes appreciated 🙏

**Why this dies in under 10 minutes**: title has `Revolutionary`, `AI-Powered`, `Transform Your Business`, two emoji, no specifics. First comment asks for upvotes, has no substance, no tech stack, no real problem description. Flagged within the first 5 users; hellban risk for "Upvotes appreciated." Mods remove, account reputation damaged.

---

## References

- AgentSkills spec: https://agentskills.io/specification
- HN guidelines: https://news.ycombinator.com/newsguidelines.html
- HN FAQ: https://news.ycombinator.com/newsfaq.html
- Ranking source (Arc): https://github.com/wting/hackernews/blob/master/news.arc
- Contact mods: hn@ycombinator.com
- Companion skill: `content-voice` — HN is the hardest platform for sounding human; voice rules are essential
