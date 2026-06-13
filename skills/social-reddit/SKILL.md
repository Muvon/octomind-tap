---
name: social-reddit
title: "Reddit Publishing Playbook"
description: "Ground-truth 2026 playbook for posting, commenting, and replying on Reddit. Covers the ranking algorithm, subreddit-first research, the 90/10 self-promotion rule, title craft, post body structure, comment strategy, thread-vibe matching, and surviving AI-content automods. Replies and comments must read as a real human typed them — imperfect, thread-aware, naturally flawed. Activate whenever drafting anything destined for Reddit."
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

## Overview

Reddit is thousands of subreddits, each with its own rules, culture, and moderators. This skill encodes ranking mechanics, the 90/10 self-promo rule, per-community research loop, and the 2026 anti-detection layer (AI-content automods now run on most large subs and silently remove LLM-shaped text).

Pair with `content-voice` for the general human-voice ruleset. This skill adds the Reddit-specific layer.

For more examples beyond the 3 in this file, see `reference/examples.md`.

## Instructions

### The 2026 Ranking Algorithm

Reddit ranks posts and comments with different math. Both penalize corporate behaviour and reward early, organic engagement.

Post ranking (Hot sort — the default feed)

Score is roughly: `log(upvotes - downvotes) × time_decay_factor`. The log function means the first 10 upvotes matter far more than going from 90 to 100. Time decay halves visibility every few hours.

Inputs that actually move ranking:
- Vote velocity in the first 1–2 hours. A post with 50 upvotes in the first hour outranks one with 200 upvotes spread over 6 hours. The golden window is shorter than most platforms.
- Upvote ratio. If the ratio drops below ~70%, the post is effectively buried. Downvotes hurt far more than upvotes help once you're above a threshold.
- Comment count and depth. Posts with ongoing discussion stay in Hot longer. 1 comment with 5 replies beats 5 one-line comments.
- Account trust score. New accounts (< 30 days, low karma) are throttled invisibly. Their posts often land in a "new-queue jail" that mods have to manually approve.
- Subreddit activity baseline. A post needs more velocity in r/programming (huge) than in r/rust (niche) to trend.

Comment ranking (Best sort — the default)

Comments use a Wilson confidence interval: not just upvotes minus downvotes, but statistical confidence given the sample size. A comment with 10 upvotes and 1 downvote ranks above one with 1 upvote and 0 downvotes, even though raw ratio is worse — more data = more confidence.

Implication: early comments compound. First 3 substantive comments on a post capture most of the reply-karma that post will ever produce.

### The 90/10 Rule (non-negotiable)

At least 90% of activity must be non-promotional. The other 10% can be yours. Break this and posts get shadow-removed, the site-wide spam filter kicks in, or the account gets suspended.

Non-promotional in practice: answering questions in your field without self-linking, commenting on others' posts, sharing articles/tools from other people, posting unrelated discussion starters. Burner and bought-karma accounts get detected — the only path is genuine membership in the communities you want to post in.

### Subreddit-First Research (always before posting)

Every subreddit has its own culture — same post lands wildly different in r/programming vs r/SideProject. Minimum 10 minutes per target sub:

1. Read the sidebar and rules. Every subreddit has its own rules pinned. Many ban self-promotion outright, require flair, require minimum account age, or have specific formatting. Violating any of these = auto-removal, often with a ban.
2. Check the last 20 posts. What titles are getting upvotes? What's the vibe — technical, casual, sarcastic, earnest? Match the register.
3. Check the pinned posts and weekly threads. Many subs have a "Self-Promotion Saturday" or "Showcase Sunday" thread. Your post belongs there, not as a standalone submission.
4. Scan the top comments on similar posts. What do they push back on? Pre-empt it in your post.

Output before writing:
- Subreddit: r/_______
- Rule-compliant? (account age, karma, flair): _______
- Tone: (technical / casual / sarcastic / earnest): _______
- Recent upvoted titles — pattern noticed: _______
- Common criticism in comments on similar posts: _______
- Designated self-promo thread if any: _______

### Title Craft

Reddit titles are the entire package for most users — most scroll the feed without expanding. Rules:

- State the thing. "My experience migrating 200k LOC from Python to Go" beats "A journey of migration."
- No clickbait. "You won't believe what happened when..." = downvote reflex. Reddit trained itself off this years ago.
- No "How to X in Y steps." Reddit users have seen 10,000 of these. They read as SEO spam.
- No emoji. None. Not even a single rocket.
- Specific over vague. Numbers, names, tools, time windows. "6 months into building my own search engine: 3 things I got wrong" > "Lessons learned building a product."
- No ALL CAPS words except proper acronyms (API, LLM). Caps read as ad copy.
- Keep it under ~80 characters. Long titles truncate on mobile. The hook has to land early.
- Don't name your product in the title unless the subreddit explicitly allows it (e.g. r/SideProject). "I built a CLI for X" is fine; "[MyProduct]: The best CLI for X" gets removed.

### Post Body Structure (by subreddit type)

Technical / discussion subs (r/programming, r/MachineLearning, r/devops)
- Open with the specific thing. No preamble.
- Include code, logs, metrics, or diagrams inline. Text-only posts get less traction than posts with concrete artifacts.
- Name exact versions, tools, and dates. Credibility comes from specificity.
- End with a real question or a specific thing you want feedback on. Not "thoughts?" — something pointed.
- Markdown is mandatory: code fences, bullet lists, bold for key terms.

Project-share subs (r/SideProject, r/IndieHackers, r/webdev "showcase")
- Be upfront you made it. First line or first paragraph.
- Share what you learned, not what you sell. Revenue numbers, MRR, failures, tech stack — all good.
- Include screenshots. Text-only project posts flop.
- Don't link aggressively. One link, in-body, not repeated.
- Name a real limitation of the thing you built. Uniformly positive descriptions read as marketing or LLM output. A specific con — "the search is slow on >10k records", "auth still doesn't have SSO" — does more for trust than any amount of polish.

Question subs (r/learnprogramming, r/AskReddit, domain subs)
- Title is the question itself. Clear, specific, not "help pls."
- Body adds context: what you tried, what happened, what you expected. Minimal version.
- Never post a question answerable by 30 seconds of Googling. Mods remove these.

Story/experience subs (r/cscareerquestions, industry subs)
- First paragraph sets scene: role, years, stakes.
- Middle paragraphs are the specifics. What happened, what people said, what you did.
- End with the open question or the moral that isn't really a moral. Readers like to draw the lesson themselves.

### Thread-Vibe Matching (read before you write)

Scanning the thread before replying is the single most effective anti-detection move — it makes output structurally match community behaviour in that moment.

What to read:
- Top 5–8 comments (or all if small)
- OP's writing style — length, punctuation, caps, casualness
- Dominant reply length — 2-line zingers or 6-paragraph essays?
- Emotional register — sarcastic, earnest, technical, venting?
- Recurring phrases, in-jokes, sub-specific slang

What to extract before writing:

| Signal | What to match |
|--------|--------------|
| Median comment length | Stay within ±30% of it |
| Punctuation style | If nobody uses periods at end of short comments, don't |
| Capitalization | If thread is mostly lowercase, go lowercase |
| Emoji usage | If zero emoji in thread, use zero |
| Markdown | If nobody uses bold/bullets, don't |
| Tone | Match the dominant register (sarcastic, earnest, technical, casual) |

Hard rule: if the thread is full of 1–3 line replies, your 8-line structured comment will stand out as AI-generated even if every word is perfect. Short thread = short reply. Long thread = you have room to breathe.

### Human Imperfection Protocol (replies and comments)

Posts get proofread; replies are typed fast on a phone. The goal is to read like a real person typing quickly, not like a bad writer.

#### Imperfections to inject (pick 1–2 per reply, not all at once)

Typos (realistic ones — adjacent keys, missed letters, transpositions):
- `teh` → `the`, `hte` → `the`, `taht` → `that`, `jsut` → `just`
- `becuase` → `because`, `recieve` → `receive`, `definately` → `definitely`
- `youre` → `you're` (missing apostrophe), `dont` → `don't`, `cant` → `can't`
- Doubled letters: `thiss`, `iss`, `andd`
- Missing space: `alot` instead of `a lot`, `infact` instead of `in fact`

Grammar that reads human, not broken:
- Run-on sentences joined with "and" or "but" where a period would be "correct"
- Starting a sentence with "And" or "But" or "So" — very common in casual writing
- Ending a thought mid-sentence and starting fresh: "the thing is. its just not worth it"
- Lowercase `i` mid-sentence (not at the start of a sentence — that reads like a style choice, not a typo)
- Missing comma in a compound sentence: "I tried that once and it didnt work at all"
- Casual abbreviation without consistency: "you" in one sentence, "u" in the next (only in very casual threads)

Rhythm and structure:
- One sentence that's noticeably shorter than the others. Like this.
- A thought that trails off with "..." when you're not sure how to finish it
- "edit: typo" or "edit: meant to say X" at the end (use sparingly — once per session max)
- Repeating a word accidentally: "the the" or "is is" — only if the comment is long enough that it reads like a scanning miss

#### Calibration by content type

| Type | Imperfection level | Notes |
|------|-------------------|-------|
| Standalone post / thread | Low — 0–1 minor imperfection | People proofread posts more; too many errors reads as low-effort |
| Top-level comment | Low-medium — 1 imperfection | Still somewhat considered |
| Reply to a comment | Medium — 1–2 imperfections | This is where humans are most casual |
| Reply in a fast-moving thread | Medium-high — 1–2 imperfections + short length | Match the pace of the thread |
| Reply to a hostile/sarcastic comment | High casualness — short, punchy, possibly no punctuation | Matching the energy is more important than grammar |

#### What NOT to do

- Don't inject a typo in the first word — it reads like a deliberate trick
- Don't put a typo in a technical term, a username, or a number — those get corrected by humans too
- Don't use more than 2 imperfections in a single comment — it tips from "human" to "illiterate"
- Don't use the same imperfection twice in the same comment
- Don't add imperfections to a post title — titles get proofread

### Comment Strategy

Comments are where most Reddit karma actually comes from, and where mods form their read on whether your account is a real member or a promo bot.

- Answer the question asked. Don't steer the conversation to your topic.
- Top-comment early or don't bother. After the first 3 substantive comments, you're buried unless your comment is exceptional.
- Specific > general. "In my experience with Postgres 16 the fsync cost actually went down after the commit-group changes" beats "Postgres is generally fast."
- Don't link in comments unless asked — and when asked, link once, no UTM parameters, no tracking.
- Agree with the top comment? Don't just say 'this' — add the next layer. Extension > echo.
- Disagree? Cite the specific claim you disagree with. "Disagree on point 2 — here's why" beats a general "no."
- Never start with 'As someone who has worked in X…' unless you actually have. Reddit detects credentialing theatre instantly. Fabricated specifics are worse than vague comments — a fake-precise claim ("ran this in production at a 10k-employee bank") attracts replies asking which bank, and the silence that follows is what mods and classifier bots escalate on. If you don't have the experience, write from the angle of what you've actually read or seen, and say so.
- Include a real con when recommending something you have a stake in. Bots and marketing copy are uniformly positive. Real recommendations name a specific trade-off — "the mobile app is weak", "scaling past ~50k rows the planner gives up", "onboarding took me a week to figure out". Vague hedges ("not for everyone") don't count; the con has to be concrete enough that someone could verify or push back on it.
- Edit-to-add is fine and human. "Edit: to clarify…" reads normal. Silent edits on controversial comments read sketchy.

### Surviving AI Detection on Reddit (the 2026 reality)

Most large subs run two filters: automod regex/keyword rules and classifier bots trained on LLM samples. The signature that gets caught is the cumulative shape, not one phrase.

Structural tells detectors look for:

1. Tri-colon listing — "X, Y, and Z" three-item parallels stacked across paragraphs. Humans write uneven lists: pairs, fours, single items, run-ons. Three balanced clauses in a row reads LLM.
2. Symmetrical paragraph length. AI writes paragraphs of similar size. Real Redditors write one-line zingers next to four-line rants next to a single sentence-fragment.
3. The "It's not X, it's Y" reframe — when used cleanly. (The donk8r-style "the question isn't X — it's Y" works because it's colloquial and contains a personal anchor; the corporate version "It's not just about features, it's about experience" is dead on arrival.)
4. Bullet-list-heavy posts. Comments with 3+ bullets read as ChatGPT output unless the question explicitly asked for a list. Most native Reddit comments are prose, even when listing things.
5. Headers in comments. Almost no human uses `## Headers` in a Reddit comment. Mods flag them on sight.
6. Bold mid-sentence. `Building cheaper and faster with AI tools just compresses the timeline` — the random bold inside flowing text is an LLM tic.
7. Closing summary line. AI loves to end with a one-line tl;dr restating the post. Most Redditors just stop, or trail off mid-thought, or end on a question.
8. No typos, no contractions, no slang. Humans on Reddit type fast. "gonna", "ngl", "tbh", "imo", "pretty much", "kinda", missed apostrophes, occasional run-on sentences — these are camouflage.
9. Em-dashes everywhere. A single em-dash is fine and human. Three em-dashes in one paragraph is GPT signature. Mix in parentheses, commas, and full stops.
10. Hedge phrases on every claim. "It's worth noting", "that said", "with that in mind", "ultimately", "at the end of the day". One per comment is fine. Three is a tell.

The lexical tells detectors look for:

Beyond the `content-voice` dead-vocabulary list — these are extra-flagged on Reddit:

- Anything reading as ad copy: "game-changer", "powerful", "robust", "seamless", "effortless", "next-level"
- Vague stakes language: "the stakes have never been higher", "in today's competitive landscape"
- Empty contrast: "while X is great, Y matters more"
- Author-as-narrator: "Let's dive in", "Let me explain", "Here's the thing"
- Conclusion telegraphs: "In conclusion", "To wrap up", "The bottom line"
- The phrase "real moat" / "real question" / "real X" used cleanly — only works with a personal anchor (see Example 6)

Tactics that pass detectors:

1. Anchor with a specific lived detail in the first 1–2 sentences. "I've been building software for 20 years and the pattern I keep seeing…" / "Ran into this last week on a Postgres 14 cluster…" / "Spent six months on this exact problem in 2023." Detectors weight comments lower when there's a verifiable, specific autobiographical claim.
2. Reference another commenter by username. "jonathancheckwise is right that…" / "Disagree with what u/foo said about X." Real Reddit threading. Bots almost never do this.
3. Quote a fragment of someone else's comment. "if you can clone it in 3 hours, so can everyone else" — using their words inside your reply signals you read the thread.
4. Use one casual reduction per comment. "imo", "ngl", "tbh", "fwiw", "ymmv", "iirc", lowercase "i" mid-sentence, contraction without apostrophe ("its" for "it's" once), or a sentence fragment. One. Multiple tics in one comment = trying too hard, also flagged.
5. Vary sentence length aggressively. Three words. Then one that runs much longer because you're explaining a thing. Short.
6. Drop the closing summary. End on the example, the question, or a half-thought. Not "In short, X" or "The takeaway is Y."
7. Skip the headers and bullets unless the question structurally calls for them. Prose wins on Reddit.
8. Write the comment, then delete the first sentence. AI-trained openers ("Great question!", "This is an interesting point", "I think there are a few things to consider") almost always live in sentence #1.
9. Disagree with part of what you're replying to. Pure agreement reads sycophantic and AI-shaped. A small, specific pushback ("agree on most of this but the part about X is overstated because…") reads as a thinking human.
10. Run the draft through a 'would I actually type this on my phone at 11pm' filter. If no, cut it down.
11. Pre-empt the sub's known controversy directly. If the topic, tool, or stance you're writing about is divisive in this community — and you can usually tell from a 5-minute scroll of recent threads — name that disagreement up front instead of pretending consensus. "I know [X] gets mixed reviews here, here's my honest read after [specific time/context]" reads like a member of the community talking to other members. Bots paper over disagreement; humans acknowledge it. Bonus effect: it pre-empts downvote brigading from the camp that disagrees, because they recognise you've already heard their argument.

Per-sub calibration: the level of AI suspicion varies. r/SaaS, r/startups, r/Entrepreneur, r/MachineLearning, r/programming, r/cscareerquestions are high-suspicion. r/SideProject, r/IndieHackers, niche hobby subs are mid. Default to high-suspicion behaviour everywhere; relax only after you've read recent successful posts.

Account-level signals. Detectors don't just look at the text — they look at the account. New account + first-comment-is-on-r/SaaS-with-marketing-language = removed regardless of how human the text reads. Build comment history in low-stakes subs first (r/AskReddit, hobby subs, your home country sub) before commenting in high-suspicion business subs.

### What Gets Auto-Removed (before anyone sees it)

Site-wide spam filter + subreddit automod catch these automatically:

Account-level signals:
- New account (< 1 week) or low total karma (< 50)
- Account with only 1 subreddit of activity
- Account with comment-only history that suddenly posts a self-link
- Recently posted the same domain in another sub

Content-level signals:
- Link to a domain flagged by the subreddit (often your own domain if posted before)
- Title or body containing banned words (varies per sub)
- Link shorteners (bit.ly, t.co, etc.) — often auto-removed
- Affiliate links or UTM tracking parameters
- Text that matches known promotional patterns ("check out my new," "just launched," "I'd love your feedback on", "I'm excited to share")

AI-content signals (2026 — the new automod layer):
- Em-dash density above ~1 per 100 words
- Tri-colon parallel structure ("X, Y, and Z" three times in close range)
- Markdown headers (`##`) in a comment
- Bold inside flowing prose
- Phrases from the dead-vocabulary list (see `content-voice`) — especially "delve", "leverage", "robust", "seamless", "in today's", "ever-evolving", "navigate the complexities"
- "It's important to note", "It's worth noting", "That said,", "In conclusion" as paragraph openers
- Symmetrical paragraph lengths (3 paragraphs all 4–5 lines)
- Zero contractions in a comment longer than 100 words
- Closing tl;dr-style summary line

If your post disappears within minutes: check modmail, and open the post URL in a logged-out browser session — if it shows as removed there, mods took it down.

### Cross-Posting and Reposting

- Cross-posting to 5+ subreddits in one day triggers spam filter. Space them out over days; customize the title and body per subreddit.
- Never post the same image/link to multiple subs simultaneously — Reddit's deduplication algo buries duplicates even if the first one did well.
- Reposting your own content after a month is fine in many subs if the original didn't land; different title, different opening line.

### After Posting (the behavioural detection layer)

The first hour is part of the post — silent OPs on commented threads are a known classifier signal.

- Answer the first 2–3 comments within an hour, even briefly ("good point, I'd missed that" / "no I tried that and it didn't work because…").
- Edit with corrections when commenters catch something. "edit: u/foo pointed out X, fixed" reads as a real person updating their thinking.
- Concede where you're wrong. "Yeah you're right, that part was sloppy" outperforms defending every point.
- If you can't engage live for an hour after posting, don't post yet.

### Timing

Reddit is heavily US-skewed. For English subs:
- Best windows: weekdays 8–11 AM ET and 6–9 PM ET
- Sunday evening ET is often the single strongest window for weekly discussion posts
- Avoid Friday afternoon / Saturday for anything you want real engagement on — the active demographic drops off
- Niche subs (r/rust, r/emacs, etc.) don't follow this — check their own activity patterns

### Pre-Publish Checklist

- [ ] Subreddit rules read in full, not skimmed
- [ ] Account meets karma/age requirements for the sub
- [ ] Title is specific, no clickbait, no emoji, under ~80 chars
- [ ] Not using a designated self-promo thread? Make sure standalone posting is allowed
- [ ] If promotional at all: confirmed it's within the 10% budget, and the post adds real value
- [ ] Markdown formatted: code fences, bullets, bold (posts only — strip from comments)
- [ ] No tracking parameters or link shorteners
- [ ] Posted in a peak window for the sub
- [ ] Ready to respond to the first comment within 30 minutes
- [ ] Post doesn't sound like marketing if read aloud
- [ ] Strip-test (project/recommendation posts): if the product/project mention is removed, is the post still useful to a reader? If no, it's marketing wearing humble clothes — rewrite around the actual lesson, or don't post
- [ ] Honest-con check (project/recommendation posts): at least one specific, concrete trade-off named — not a vague hedge
- [ ] Engagement window: can be at the keyboard for the next hour to reply to first 2–3 comments — if not, postpone
- [ ] Thread-vibe check (replies/comments): scanned the thread, matched dominant length and tone, no markdown if nobody else uses it
- [ ] Imperfection check (replies/comments): 1–2 realistic imperfections present — typo, missing apostrophe, run-on, or casual grammar — not in the first word, not in a technical term
- [ ] AI-detection pass: opens with a specific lived detail, no headers in comments, no bold in prose, < 1 em-dash per 100 words, at least one contraction, no closing summary, no dead vocabulary, no tri-colon parallel structure, no "It's worth noting" / "That said" openers
- [ ] Sub is high-suspicion (r/SaaS, r/startups, r/Entrepreneur, r/programming, r/MachineLearning)? Comment quotes another commenter or references a username, includes one casual reduction (imo/ngl/tbh/fwiw), and varies sentence length deliberately

## Examples

### Example 1: Title craft

Bad (marketing, vague, clickbait):
> 🚀 You won't believe how we scaled our platform to 10M users — a success story!

Bad (SEO-spam listicle):
> Top 10 Ways to Scale Your Backend in 2026

Good (specific, neutral, a story someone wants to read):
> Scaling Postgres from 40GB to 4TB: what broke, what we changed, what we'd do differently

What works: real numbers, neutral tone, implicit stakes, offers a story and lessons without selling them.

### Example 2: Comment that earns karma (and trust)

Someone posts in r/rust: "Is tokio really necessary or can I just use threads?"

Bad (generic, authority-theatre, no specifics):
> As someone who has worked extensively with Rust, tokio is essential for any serious async workload. Threads don't scale.

Good (specific, domain-aware, honest about trade-offs):
> Depends on your workload. If you're I/O bound and handling >~10k concurrent connections, tokio is hard to beat — the overhead per task is tiny compared to a thread's ~2MB stack.
>
> If you're CPU-bound or running <1k concurrent tasks, `std::thread` + a channel is simpler and often faster. Threads also debug way better — stack traces, backtraces, no `.await` gymnastics.
>
> Short answer: pick tokio for network services, threads for background processing.

What works: opens on the answer, gives concrete numbers, acknowledges the alternative is sometimes better, ends with a poster-able summary.

### Example 3: Rewriting a comment to pass AI detection

Original draft (will be auto-removed in r/SaaS, r/startups, r/Entrepreneur — every detector tell present):

> The real moat is distribution and iteration speed. Building software has fundamentally changed in recent years, and the patterns we're seeing are clear:
>
> - The first mover figures out the market exists
> - The second mover figures out what people actually want
> - The third mover with the best distribution wins
>
> Building cheaper and faster with AI tools simply compresses the timeline. It's important to note that the question is no longer "can I build it?" — it's "can I out-distribute and out-iterate?" Ultimately, in today's competitive landscape, distribution is everything.

What's wrong: bold opener, three balanced bullets, header-style emphasis, "It's important to note", "Ultimately", "in today's competitive landscape", closing summary, zero personal anchor, zero contractions where they'd naturally appear, three em-dashes, no reference to the post or other commenters.

Rewritten (this is roughly the surviving `donk8r` comment from the actual r/SaaS thread):

> The real moat isn't the code, it's the distribution and the iteration speed. I've been building software for 20 years and the pattern I keep seeing: the first mover figures out the market exists, the second mover figures out what people actually want, and the third mover with the best distribution wins. Building cheaper and faster with AI tools just compresses the timeline. But jonathancheckwise is right that if you can clone it in 3 hours, so can everyone else. The question isn't "can I build it?" anymore — it's "can I out-distribute and out-iterate the other 50 people who also built it this weekend?"

What works:
- Opens with a personal anchor: "I've been building software for 20 years" (verifiable, specific, autobiographical)
- Quotes another commenter by username (`jonathancheckwise`) and uses their exact phrase (`if you can clone it in 3 hours`)
- Prose, not bullets, even though the structure is tri-partite
- No headers, no bold, only one em-dash
- Contractions throughout (`isn't`, `can't`, `aren't`)
- Ends on a quoted question, not a summary
- "The real moat" works here because it's immediately undercut with the personal anchor — without that anchor, the same phrase reads AI

This is the template. Anchor → observation → reference to thread → specific reframe → no closing summary.

For more examples (self-promotion, ask posts, automod removals, thread-vibe matching, calibrated imperfections), see `reference/examples.md`.

## References

- AgentSkills spec: https://agentskills.io/specification
- Reddit content policy: https://www.redditinc.com/policies/content-policy
- Companion skill: `content-voice` — especially critical for Reddit, which detects corporate tone instantly
