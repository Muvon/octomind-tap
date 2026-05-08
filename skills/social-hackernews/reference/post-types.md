# HN — extended post-type rules

Detail beyond the 5-post-types table in `SKILL.md`. Load this file when planning a Tell HN, Launch HN, or working through URL submission / duplicate edge cases.

## Tell HN — expanded rules

Tell HN is the most misused prefix. Short, factual announcements only — not mini blog posts, not product pitches, not opinion pieces.

What Tell HN IS for:
- Service outages affecting HN or major tech infrastructure
- Security vulnerabilities with public disclosure
- Changes to HN itself (new features, policy updates)
- Short factual observations about the tech industry
- Corrections to previously submitted stories

What Tell HN is NOT for:
- "Tell HN: I built a thing" → that's Show HN
- "Tell HN: My thoughts on AI" → that's a blog post, submit the link
- "Tell HN: We're hiring" → use the monthly "Who is hiring?" thread
- "Tell HN: Please support our Kickstarter" → instant flag

Title rules:
- Lead with the fact, not the source. "Tell HN: GitHub Actions is down in us-east-1" not "Tell HN: GitHub says Actions is down"
- No editorializing. "Tell HN: AWS us-east-1 is down again" → "again" is editorializing.
- Include timeframe if known. "Tell HN: Cloudflare 522 errors since 14:00 UTC"

Body rules:
- Under 300 words. If it needs more, write an article and submit the link.
- Evidence first. Screenshots, status page links, specific error codes.
- No call to action.
- Update the body (not a new comment) as the situation evolves.

## Launch HN — expanded rules (YC companies only)

Launch HN is a coordinated YC program. You cannot self-declare a Launch HN.

How it works:
- YC schedules your launch with the HN mods. You don't pick the date.
- Title format is strict: `Launch HN: CompanyName (YC W25) – one-line description`
- Batch code (W25, S24, etc.) is required. Mods add it if you forget.
- Launch HN posts get a special tag and often appear in the "Launches" section.

Launch HN first comment (different from Show HN — 6 sections):
1. What the company does — 1 sentence, plain English
2. The problem you're solving — not "the market is huge" but "engineers waste 3 hours a week on X"
3. How it works — technical specifics, architecture, interesting implementation
4. Traction so far — users, revenue, growth rate. HN respects numbers.
5. What you need help with — hiring, beta testers, specific technical feedback
6. How to try it — demo link, signup, open-source repo

Timing: usually Tuesday/Wednesday mornings ET, scheduled by YC.

Pitfalls:
- Don't use Launch HN if you're not YC-backed — mods retitle or kill.
- Don't post a Launch HN without YC scheduling — won't get special treatment, may be flagged.
- Don't treat it as a press release — HN readers want technical depth.

## URL submission rules

- Submit the canonical URL. No `?utm_source=`, no `ref=`, no tracking parameters.
- No AMP links. Submit the publisher's original URL, not Google AMP cache.
- No Medium / Substack tracking suffixes (`?sk=abc123`).
- No paywalled URL as the primary link. Submit the unpaywalled version (archive.today, Ghostreader, author's mirror) and mention paywall in the first comment.
- No link shorteners (`bit.ly`, `t.co`) — auto-flagged.
- No redirect chains — submit the final destination.
- GitHub: submit the repo root, not a specific file path, unless the file IS the story.
- YouTube: only if video is the primary content; explain why in the first comment.

## Duplicate detection and cross-posting etiquette

- Same URL = duplicate. Submitted in last ~6 months → redirects to old thread.
- Slightly different URLs (www., http vs https, trailing slash) bypass detection — mods later merge. Don't game; users flag.
- Cross-posting from Reddit / X / your blog: acceptable, but space by 48+ hours and rewrite the title for HN's audience. Never copy-paste the same first comment across platforms.
- If your post flopped: wait 3+ months before resubmitting, only if significantly improved.
- "Previously" etiquette: disclose if you posted it before — "I posted this last month; the update is X."

## Account warmup and karma

New accounts are heavily throttled. Brand-new account submitting its own project = voting-ring red flag.

First 30 days:
- Don't submit your own content. Comment substantively on others' posts for 2–3 weeks.
- Target 50+ karma before first self-promotion (informal threshold).
- Comment on posts in your domain — "We hit this exact issue at scale; the fix was X" builds recognition.
- Avoid early downvotes — they put the account in a low-trust bucket.

Karma mechanics:
- Karma = comment + post upvotes minus downvotes.
- Comment karma matters more than post karma for account trust.
- Downvotes on comments cost karma; downvotes on posts don't (but the post dies).
- No public leaderboard — karma is purely for trust and feature unlocks.

Karma unlocks:
- ~10: downvote comments
- ~30: flag posts
- ~500: vouch for dead posts
- Higher karma = more weight in voting (trust-weighted internally)

Red flags for new accounts:
- First action is a self-submission
- First comment on your own post
- Rapid-fire commenting (bot-like)
- All comments on posts you submitted
- Account created the same day as a Show HN
