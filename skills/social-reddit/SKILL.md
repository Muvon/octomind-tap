---
name: social-reddit
title: "Reddit Publishing Playbook"
description: "Ground-truth 2026 playbook for posting, commenting, and replying on Reddit. Covers the ranking algorithm (Hot/Best sort, vote velocity, time decay, confidence score), subreddit-first research, the 90/10 self-promotion rule, title craft, post body structure per subreddit type, comment strategy, and what gets auto-removed. Activate whenever drafting anything destined for Reddit."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Reddit."
domains: content
rules:
  - content(reddit)
  - content(subreddit)
  - content(upvote)
  - content(upvotes)
  - content(karma)
  - match(\br/[a-zA-Z0-9_]+)
  - match(\bpost\s+(on|to|for)\s+(reddit|r/))
  - match(\bask\s?me\s?anything\b|\bAMA\b)
---

# Reddit Publishing Playbook

## Overview

Reddit is not one platform — it's thousands of communities each with their own rules, culture, and moderators. A post that hits the front page of one subreddit gets instantly removed from another. This skill encodes the ranking mechanics, the universal rules of thumb, and the per-community research loop that separates "contributing member" from "spam account."

Pair with `content-voice` for human voice. Reddit is the most allergic platform on the internet to corporate/AI-generated tone — if it reads like marketing, it's dead in minutes.

---

## Instructions

### The 2026 Ranking Algorithm

Reddit ranks posts and comments with different math. Both penalize corporate behaviour and reward early, organic engagement.

**Post ranking (Hot sort — the default feed)**

Score is roughly: `log(upvotes - downvotes) × time_decay_factor`. The log function means the first 10 upvotes matter far more than going from 90 to 100. Time decay halves visibility every few hours.

Inputs that actually move ranking:
- **Vote velocity in the first 1–2 hours.** A post with 50 upvotes in the first hour outranks one with 200 upvotes spread over 6 hours. The golden window is shorter than most platforms.
- **Upvote ratio.** If the ratio drops below ~70%, the post is effectively buried. Downvotes hurt far more than upvotes help once you're above a threshold.
- **Comment count and depth.** Posts with ongoing discussion stay in Hot longer. 1 comment with 5 replies beats 5 one-line comments.
- **Account trust score.** New accounts (< 30 days, low karma) are throttled invisibly. Their posts often land in a "new-queue jail" that mods have to manually approve.
- **Subreddit activity baseline.** A post needs more velocity in r/programming (huge) than in r/rust (niche) to trend.

**Comment ranking (Best sort — the default)**

Comments use a **Wilson confidence interval**: not just upvotes minus downvotes, but statistical confidence given the sample size. A comment with 10 upvotes and 1 downvote ranks above one with 1 upvote and 0 downvotes, even though raw ratio is worse — more data = more confidence.

Implication: **early comments compound.** First 3 substantive comments on a post capture most of the reply-karma that post will ever produce.

---

### The 90/10 Rule (non-negotiable)

At least **90% of your activity on Reddit must be non-promotional.** Comments, discussion, helping people, sharing things you didn't make. The other 10% can be yours.

Break this and:
- Mods shadow-remove your posts in their subreddit
- Reddit's site-wide spam filter kicks in (posts never appear to anyone)
- Accounts get permanently suspended

What "non-promotional" means in practice:
- Answering questions in your field without linking back to yourself
- Commenting on posts that aren't yours
- Sharing articles/tools from *other* people
- Posting memes, observations, discussion starters unrelated to your work

There is no way around this. Burner accounts get detected. Buying karma accounts gets detected. The only path is being a genuine member of the communities you want to post in.

---

### Subreddit-First Research (always before posting)

Every subreddit has a culture. Posting a "Show HN"-style project launch in r/programming gets you roasted; posting the same thing in r/SideProject gets upvoted. **Read before you post.** Minimum 10 minutes per target subreddit:

1. **Read the sidebar and rules.** Every subreddit has its own rules pinned. Many ban self-promotion outright, require flair, require minimum account age, or have specific formatting. Violating any of these = auto-removal, often with a ban.
2. **Check the last 20 posts.** What titles are getting upvotes? What's the vibe — technical, casual, sarcastic, earnest? Match the register.
3. **Check the pinned posts and weekly threads.** Many subs have a "Self-Promotion Saturday" or "Showcase Sunday" thread. Your post belongs there, not as a standalone submission.
4. **Check removed posts via reveddit.com or similar** to see what mods quietly take down. Often that's where self-promotion actually goes to die — it looks live to you, invisible to everyone else.
5. **Scan the top comments on similar posts.** What do they push back on? Pre-empt it in your post.

Output before writing:
- Subreddit: r/_______
- Rule-compliant? (account age, karma, flair): _______
- Tone: (technical / casual / sarcastic / earnest): _______
- Recent upvoted titles — pattern noticed: _______
- Common criticism in comments on similar posts: _______
- Designated self-promo thread if any: _______

---

### Title Craft

Reddit titles are the entire package for most users — most scroll the feed without expanding. Rules:

- **State the thing.** "My experience migrating 200k LOC from Python to Go" beats "A journey of migration."
- **No clickbait.** "You won't believe what happened when..." = downvote reflex. Reddit trained itself off this years ago.
- **No "How to X in Y steps."** Reddit users have seen 10,000 of these. They read as SEO spam.
- **No emoji.** None. Not even a single rocket.
- **Specific over vague.** Numbers, names, tools, time windows. "6 months into building my own search engine: 3 things I got wrong" > "Lessons learned building a product."
- **No ALL CAPS words** except proper acronyms (API, LLM). Caps read as ad copy.
- **Keep it under ~80 characters.** Long titles truncate on mobile. The hook has to land early.
- **Don't name your product in the title** unless the subreddit explicitly allows it (e.g. r/SideProject). "I built a CLI for X" is fine; "[MyProduct]: The best CLI for X" gets removed.

---

### Post Body Structure (by subreddit type)

**Technical / discussion subs (r/programming, r/MachineLearning, r/devops)**
- Open with the specific thing. No preamble.
- Include code, logs, metrics, or diagrams inline. Text-only posts get less traction than posts with concrete artifacts.
- Name exact versions, tools, and dates. Credibility comes from specificity.
- End with a real question or a specific thing you want feedback on. Not "thoughts?" — something pointed.
- Markdown is mandatory: code fences, bullet lists, bold for key terms.

**Project-share subs (r/SideProject, r/IndieHackers, r/webdev "showcase")**
- Be upfront you made it. First line or first paragraph.
- Share what you learned, not what you sell. Revenue numbers, MRR, failures, tech stack — all good.
- Include screenshots. Text-only project posts flop.
- Don't link aggressively. One link, in-body, not repeated.

**Question subs (r/learnprogramming, r/AskReddit, domain subs)**
- Title is the question itself. Clear, specific, not "help pls."
- Body adds context: what you tried, what happened, what you expected. Minimal version.
- Never post a question answerable by 30 seconds of Googling. Mods remove these.

**Story/experience subs (r/cscareerquestions, industry subs)**
- First paragraph sets scene: role, years, stakes.
- Middle paragraphs are the specifics. What happened, what people said, what you did.
- End with the open question or the moral that isn't really a moral. Readers like to draw the lesson themselves.

---

### Comment Strategy

Comments are where most Reddit karma actually comes from, and where mods/moderators form their read on whether your account is a real member or a promo bot.

- **Answer the question asked.** Don't steer the conversation to your topic.
- **Top-comment early or don't bother.** After the first 3 substantive comments, you're buried unless your comment is exceptional.
- **Specific > general.** "In my experience with Postgres 16 the fsync cost actually went down after the commit-group changes" beats "Postgres is generally fast."
- **Don't link in comments unless asked** — and when asked, link once, no UTM parameters, no tracking.
- **Agree with the top comment? Don't just say 'this' — add the next layer.** Extension > echo.
- **Disagree? Cite the specific claim you disagree with.** "Disagree on point 2 — here's why" beats a general "no."
- **Never start with 'As someone who has worked in X…' unless you actually have.** Reddit detects credentialing theatre instantly.
- **Edit-to-add is fine and human.** "Edit: to clarify…" reads normal. Silent edits on controversial comments read sketchy.

---

### What Gets Auto-Removed (before anyone sees it)

Site-wide spam filter + subreddit automod catch these automatically:

- New account (< 1 week) or low total karma (< 50)
- Account with only 1 subreddit of activity
- Link to a domain flagged by the subreddit (often your own domain if posted before)
- Title or body containing banned words (varies per sub)
- Post during a rate-limited window (same user, too many posts)
- Link shorteners (bit.ly, t.co, etc.) — often auto-removed
- Affiliate links or UTM tracking parameters
- Text that matches known promotional patterns ("check out my new," "just launched," "I'd love your feedback on")

If your post disappears within minutes: check modmail, check your post on old.reddit.com logged out, or use reveddit.com.

---

### Cross-Posting and Reposting

- **Cross-posting to 5+ subreddits in one day triggers spam filter.** Space them out over days; customize the title and body per subreddit.
- **Never post the same image/link to multiple subs simultaneously** — Reddit's deduplication algo buries duplicates even if the first one did well.
- **Reposting your own content** after a month is fine in many subs if the original didn't land; different title, different opening line.

---

### Timing

Reddit is heavily US-skewed. For English subs:
- **Best windows**: weekdays 8–11 AM ET and 6–9 PM ET
- **Sunday evening ET** is often the single strongest window for weekly discussion posts
- **Avoid Friday afternoon / Saturday** for anything you want real engagement on — the active demographic drops off
- **Niche subs (r/rust, r/emacs, etc.)** don't follow this — check their own activity patterns

---

### Pre-Publish Checklist

- [ ] Subreddit rules read in full, not skimmed
- [ ] Account meets karma/age requirements for the sub
- [ ] Title is specific, no clickbait, no emoji, under ~80 chars
- [ ] Not using a designated self-promo thread? Make sure standalone posting is allowed
- [ ] If promotional at all: confirmed it's within the 10% budget, and the post adds real value
- [ ] Markdown formatted: code fences, bullets, bold
- [ ] No tracking parameters or link shorteners
- [ ] Posted in a peak window for the sub
- [ ] Ready to respond to the first comment within 30 minutes
- [ ] Post doesn't sound like marketing if read aloud

---

## Examples

### Example 1: Title craft

**Bad (marketing, vague, clickbait):**
> 🚀 You won't believe how we scaled our platform to 10M users — a success story!

**Bad (SEO-spam listicle):**
> Top 10 Ways to Scale Your Backend in 2026

**Good (specific, neutral, a story someone wants to read):**
> Scaling Postgres from 40GB to 4TB: what broke, what we changed, what we'd do differently

What works: real numbers, neutral tone, implicit stakes, offers a story and lessons without selling them.

---

### Example 2: Self-promotion that doesn't get removed

**Bad (pure promo — gets filtered):**
> Hey r/webdev! I just launched [MyApp], the best CRM for freelancers. Check it out! 🎉

**Good (post-mortem with the product as part of the story):**
> 6 months building a CRM for freelancers — MRR, tech stack, the two features I wish I'd cut
>
> Built this after freelancing for 3 years and hating every existing CRM. Some numbers, lessons, and honest mistakes below.
>
> **Stack**: Next.js 15, Postgres, Redis, Stripe, Resend
> **MRR after 6 months**: $1,840
> **Feature I built and regret**: AI-generated invoices…
>
> *(link to site at the bottom, no UTM)*

What works: post is about the journey, not the pitch. Product URL appears once. Specific numbers. Honest failure disclosure. The 10% rule is satisfied because this reads as a contribution, not a conversion funnel.

---

### Example 3: Comment that earns karma (and trust)

Someone posts in r/rust: *"Is tokio really necessary or can I just use threads?"*

**Bad (generic, authority-theatre, no specifics):**
> As someone who has worked extensively with Rust, tokio is essential for any serious async workload. Threads don't scale.

**Good (specific, domain-aware, honest about trade-offs):**
> Depends on your workload. If you're I/O bound and handling >~10k concurrent connections, tokio is hard to beat — the overhead per task is tiny compared to a thread's ~2MB stack.
>
> If you're CPU-bound or running <1k concurrent tasks, `std::thread` + a channel is simpler and often faster. Threads also debug way better — stack traces, backtraces, no `.await` gymnastics.
>
> Short answer: pick tokio for network services, threads for background processing.

What works: opens on the answer, gives concrete numbers, acknowledges the alternative is sometimes better, ends with a poster-able summary.

---

### Example 4: Ask-question post

**Bad (vague, no context, unanswerable):**
> Help with Postgres?

**Good (specific, shows effort, asks a real question):**
> Postgres 16 — can `VACUUM FULL` be safely run on a 400GB table with replication lag concerns?
>
> Setup: primary + 2 async replicas, ~30MB/s write throughput, nightly 4-hour maintenance window. Table is bloated (~40% dead tuples), `pg_repack` keeps OOM-ing.
>
> What I've tried: `pg_repack` with `-T 900` (still OOM after ~2h), `VACUUM (PARALLEL 4)` (runs but doesn't reclaim space). Considering `VACUUM FULL` but worried about the exclusive lock + replication catchup time.
>
> Has anyone run `VACUUM FULL` on a similar-size table in production? What was the replica catchup pattern?

What works: title is the real question. Body shows effort (three things already tried). Ends with a specific question someone can answer from experience.

---

### Example 5: What gets removed by automod

> Hey everyone! Excited to share that I've just launched my brand new SaaS, TurboForms 🚀 — the ultimate form builder for startups! Would love your feedback! [link with UTM]

Triggers: exclamation marks, "just launched," emoji, UTM tracking, "would love your feedback," generic SaaS positioning. Removed by automod in most subs within seconds. Reads as advertising from the first word.

---

## References

- AgentSkills spec: https://agentskills.io/specification
- Reddit content policy: https://www.redditinc.com/policies/content-policy
- Reveddit (see removed posts): https://reveddit.com
- Companion skill: `content-voice` — especially critical for Reddit, which detects corporate tone instantly
