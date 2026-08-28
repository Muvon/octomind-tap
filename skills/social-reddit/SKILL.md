---
name: social-reddit
title: "Reddit Publishing Playbook"
description: "Ground-truth 2026 playbook for posting, commenting, and replying anywhere on Reddit — any topic, from hobbies and health to careers and software. Covers the ranking algorithm, thread target selection by velocity, subreddit-first research, the 90/10 self-promotion rule, title craft, post body structure by sub type, comment strategy that earns trust without pitching, thread-vibe matching, the named AI-tell tic list, and the response protocol for being accused of writing with an LLM. Activate whenever drafting anything destined for Reddit."
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

Reddit is thousands of subreddits — hobbies, health, finance, careers, fandoms, local cities, trades, software — each with its own rules, culture, and moderators. Everything here applies whatever the topic: the ranking mechanics, the 90/10 rule on posting about your own thing, the per-community research loop, and the 2026 anti-detection layer (AI-content automods now run on most large subs and silently remove LLM-shaped text). Where an example is technical, it is an example, not a scope limit — the same rule holds in r/cooking, r/personalfinance, or r/AskHistorians.

Pair with `content-voice` for the general human-voice ruleset. This skill adds the Reddit-specific layer.

For more examples beyond the 3 in this file, see `reference/examples.md`.

## Instructions

### The 2026 Ranking Algorithm

Reddit ranks posts and comments with different math. Both penalize corporate behaviour and reward early, organic engagement.

Post ranking (Hot sort) is roughly `log(upvotes - downvotes) × time_decay`. The log means the first ten upvotes matter far more than going from 90 to 100, and decay halves visibility every few hours. What moves it: vote velocity in the first one to two hours (50 upvotes in an hour outranks 200 spread over six), upvote ratio (below ~70% the post is buried), comment count and depth, account trust (new or low-karma accounts get throttled invisibly), and the sub's own activity baseline. Peak visibility lands four to eight hours in; a twelve-hour-old post needs roughly ten times the upvotes of a one-hour-old one. Discussion outranks applause — 50 comments of back-and-forth beat 200 upvotes and silence, so give people something to argue with.

Comment ranking (Best sort) uses a Wilson confidence interval, not raw score: 10 up and 1 down ranks above 1 up and 0 down, because more data means more confidence. Early comments compound — the first three substantive comments capture most of the reply karma a post will ever produce.

### The 90/10 Rule (non-negotiable)

At least 90% of activity must be non-promotional. The other 10% can be yours. Break this and posts get shadow-removed, the site-wide spam filter kicks in, or the account gets suspended.

Non-promotional in practice: answering questions without self-linking, commenting on others' posts, sharing other people's articles/tools, posting unrelated discussion starters. Burner and bought-karma accounts get detected — the only path is genuine membership in the communities you post in.

### Subreddit-First Research (always before posting)

Every subreddit has its own culture — the same post lands very differently in r/AskHistorians than in r/CasualConversation. Minimum 10 minutes per target sub:

1. Read the sidebar and rules. Many subs ban self-promotion outright, require flair or minimum account age, or mandate formatting. Violating any = auto-removal, often with a ban.
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

### Target Selection (this dominates comment craft)

Measured across an 11-comment sample on one account: comment score tracked the host thread's score almost monotonically. A sharp 466-character comment scored 1 because its thread was quiet; a comparable one scored 18 in a busy thread. A great comment in front of nobody is worth exactly one point. This is an impressions problem wearing a quality problem's clothes.

The leading indicator is velocity at entry, not absolute score. Compute `num_comments / age_hours` before you write. Above ~5/hour is worth entering; under ~3/hour usually is not, however good the topic fit. Early entry alone is not enough — the 18-scorer went in at 1.8h into a thread doing 8.5 comments/hour, while 5h entries into slow threads all scored 1.

Room vetoes override velocity entirely. Skip regardless of how fast the thread is moving when:
- top comments are all mockery of OP — the room has already decided, and a substantive answer reads as missing the joke
- anyone has accused OP of AI-generating the post, or mocked a specific style (all-lowercase, tidy structure) as the giveaway
- the highest-scoring replies are anti-hype, anti-vendor or anti-bot — a measured stranger with a link reads as astroturf in that crowd
- the topic is one the sub treats as inherently suspect (get-rich schemes, miracle cures, crypto, anything mixing money with autonomy) — a technical point reads as promotion no matter how it's phrased

Velocity picks the candidates. The room decides whether you write at all.

Slow threads are still worth answering, just not for score. Comments keep working for months with no further effort: a 55-day-old comment produced the best outcome of its week, and late replies that reliably score 1 generate the best ongoing relationships. Judge those on what they change, not on karma.

### Title Craft

Reddit titles are the entire package for most users — most scroll the feed without expanding. Rules:

- State the thing. "My experience migrating 200k LOC from Python to Go" beats "A journey of migration."
- No clickbait. "You won't believe what happened when..." = downvote reflex. Reddit trained itself off this years ago.
- No "How to X in Y steps." Reddit users have seen 10,000 of these. They read as SEO spam.
- No emoji. None. Not even a single rocket.
- Specific over vague. Numbers, names, places, time windows. "Six months of tracking every grocery receipt: what actually cut the bill" beats "Lessons learned about saving money."
- No ALL CAPS words except proper acronyms (API, LLM). Caps read as ad copy.
- Keep it under ~80 characters. Long titles truncate on mobile. The hook has to land early.
- Don't put a brand, product, or shop name in the title unless the sub explicitly allows it (e.g. r/SideProject). "I built a CLI for X" or "I refinished a 1940s desk" is fine; "[MyBrand]: the best X" gets removed.

### Post Body Structure (by subreddit type)

Subs cluster into a handful of shapes regardless of topic. Match the shape, not the subject matter.

Expertise and discussion subs (r/AskHistorians, r/programming, r/personalfinance, r/medicine): open with the specific thing, no preamble. Bring the artifact — the numbers, the source, the code, the photo, the receipt. Text-only assertions underperform evidence. Name exact figures, dates, editions, versions. End with a pointed question, not "thoughts?". Markdown belongs in posts, never in comments.

Show-and-tell subs (r/SideProject, r/woodworking, r/gardening, r/mycology): say it's yours in the first line. Share what you learned rather than what you want from the reader. Include photos. One link at most, in-body, not repeated. Name a real limitation — "the joint on the left is out by 2mm", "search is slow past 10k records", "the yield was half what I expected". Uniformly positive descriptions read as marketing or LLM output.

Question subs (r/AskDocs, r/legaladvice, r/learnprogramming, r/cooking): the title is the question, specific and not "help pls". The body carries what you tried, what happened, what you expected, plus whatever context the sub's rules require (age/location/equipment). Never post something 30 seconds of searching would answer.

Story and experience subs (r/cscareerquestions, r/relationships, r/TalesFromTechSupport, city subs): first paragraph sets who you are, the timeframe and the stakes; the middle carries specifics; the end leaves the lesson for the reader to draw.

Community and hobby chat subs (fandoms, city subs, r/CasualConversation): low-stakes, high-frequency, short. These are where a real account is built — the history that keeps a later post out of the spam filter.

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

Posts get proofread; replies are typed fast on a phone. Pick one or two imperfections per reply, never a whole set: a realistic typo, a missing apostrophe, a run-on joined with "and", a sentence starting with "But", a lowercase `i` mid-sentence, one sentence much shorter than the others. Not in the first word, not in a technical term or username or number, never twice the same way, never in a post title.

Don't lowercase every sentence start as camouflage. It has been named publicly as a tell, and it backfires for a specific reason: casual casing sitting on top of immaculate punctuation and three balanced paragraphs is a costume, and the seam is what readers notice. Capitalise and punctuate normally, and put the sloppiness in the content instead — a digression, a thought that trails off, one real typo left in, an answer that covers one thing and ignores the rest of the post. Matching a genuinely all-lowercase thread is a different decision from adopting lowercase as a house style.

Full typo list, grammar patterns and the per-content-type calibration table: `reference/imperfections.md`.

### Comment Strategy

Comments are where most karma comes from, and where mods decide whether your account is a real member or a promo bot.

- Answer the question asked. Don't steer the conversation to your topic.
- Top-comment early or don't bother. After the first 3 substantive comments, you're buried unless your comment is exceptional.
- Specific beats general. "I ran the same sourdough at 72% and 80% hydration in the same oven and the 80% one spread" beats "hydration matters." The specific version works identically for a recipe, a symptom, a tax rule, or a database.
- Don't link in comments unless asked — and when asked, link once, no UTM parameters, no tracking.
- Agree with the top comment? Don't just say 'this' — add the next layer. Extension > echo.
- Disagree? Cite the specific claim you disagree with. "Disagree on point 2 — here's why" beats a general "no."
- Never start with "as someone who has worked in X…" unless you actually have. Reddit detects credentialing theatre instantly, and fabricated specifics are worse than vague ones — a fake-precise claim ("I ran this at a 10k-employee bank", "my cardiologist said") attracts replies asking which one, and the silence that follows is what mods and classifier bots escalate on. If you don't have the experience, write from what you've read or seen and say so.
- Include a real drawback whenever you recommend something you have a stake in, or are simply enthusiastic about. Bots and marketing copy are uniformly positive. Real recommendations name a concrete trade-off — "the mobile app is weak", "the tool dulls fast on hardwood", "onboarding took me a week". Vague hedges ("not for everyone") don't count; it has to be concrete enough to verify or argue with.
- Edit-to-add is fine and human. "Edit: to clarify…" reads normal. Silent edits on controversial comments read sketchy.

### What Actually Converts (measured)

Measured over ~60 comments in one campaign, where the goal was influence rather than karma. The mechanism is generic: it applies to changing someone's mind about a recipe, a diagnosis to ask their doctor about, a legal step, or a piece of software.

- Refusing to pitch outperforms pitching. Telling someone the thing you're invested in is the wrong fit for their situation, and pointing at the better option, produced follow-ups that a pitch never did. The single best-scoring comment of the run said don't use our thing for this.
- Admitting ignorance reopens dead threads. "I don't have an answer for that case" brought a stranger back days later with the answer; nothing else revived a dead thread all run.
- Concede in the first sentence, then add something new. Both times a claim was refuted with evidence, the reply opened with "fair, I was wrong" — that is what bought the next round.
- When someone says they took your advice, reply with the next problem it creates, not congratulation. That is what turns a thank-you into a real exchange.
- Object to a conclusion someone reached because of your earlier argument. Agreeing with people who agree with you is where exchanges die.
- Engage what someone is about to do, not what they already finished. Advice is still cheap to act on there.
- Critique that argues in the other person's favour — their result is stronger, or their evidence weaker, than they thought — is the most reusable move available.
- Read the existing comments first. Twice the obvious point had already been made, and going elsewhere in the thread is what made the comment land.

When not to bring up your own thing at all: in someone else's disclosed showcase thread (hijacking it is banned, and staying out of it produced two of the wins), with a person you already mentioned it to today, with someone whose constraints rule it out (privacy, cost, they built their own), in a competitor's own sub, or across multiple posts by the same person. Recommendation threads look like the safest slot and are a trap for argument-led accounts: the reward function there is give me the name, top comments are bare names and bare links, and a three-paragraph critique with a self-link lands at -1. Post one line and a link, or skip.

Disclosed links do not suppress score (measured, n=11: the top-scoring comment carried one). The reason to skip a link is argument coherence, not imagined safety.

### Surviving AI Detection on Reddit (the 2026 reality)

Most large subs run two filters: automod regex/keyword rules and classifier bots trained on LLM samples. The signature that gets caught is the cumulative shape, not one phrase.

Structural tells detectors look for:

1. Tri-colon listing — "X, Y, and Z" parallels stacked across paragraphs. Humans write uneven lists: pairs, fours, single items, run-ons.
2. Symmetrical paragraph length. Real Redditors put a one-line zinger next to a four-line rant next to a fragment.
3. The "It's not X, it's Y" reframe used cleanly. The corporate version ("it's not just about features, it's about experience") is dead on arrival.
4. Three or more bullets in a comment, unless the question asked for a list. Native Reddit comments are prose even when listing things.
5. Markdown headers in a comment. Almost nobody does this; mods flag them on sight.
6. Bold inside flowing prose.
7. A closing tl;dr line restating the comment. Most people just stop, or end on a question.
8. Zero typos, zero contractions, zero slang. "gonna", "tbh", "kinda", missed apostrophes and the odd run-on are camouflage.
9. Em-dashes everywhere. One is fine; three in a paragraph is a signature. Mix in parentheses, commas, full stops.
10. A hedge on every claim: "it's worth noting", "that said", "ultimately", "at the end of the day". One is fine, three is a tell.

Lexical tells, beyond the `content-voice` dead-vocabulary list: ad-copy words ("game-changer", "powerful", "robust", "seamless", "next-level"), vague stakes ("in today's competitive landscape"), empty contrast ("while X is great, Y matters more"), author-as-narrator ("let's dive in", "here's the thing"), conclusion telegraphs ("in conclusion", "the bottom line"), and "the real question/moat/problem" used without a personal anchor.

Named tics, submission-format tells, and the register-mismatch rule live in `reference/ai-tells.md` — load it when drafting. The headline offenders: never open a sentence with "worth", never write "it's not X, it's Y", never post a three-item list, never estimate a stranger's effort, and never use the same closing disclosure twice.

Tactics that pass detectors:

1. Anchor with a specific lived detail in the first sentence or two — "ran into this last week on a Postgres 14 cluster", "my grandmother did it with a cast iron pan and no thermometer". A verifiable autobiographical claim lowers detector weight.
2. Reference another commenter by username and quote a fragment of their wording. Bots almost never do either, and it proves you read the thread.
3. Use exactly one casual reduction per comment (imo, tbh, fwiw, iirc, a missing apostrophe, a fragment). Several at once reads as trying too hard.
4. Vary sentence length hard. Three words. Then one that runs much longer because you're explaining something. Short.
5. Drop the closing summary and the closing recommendation. End on the example or the question.
6. Write the comment, then delete the first sentence — AI-trained openers live there — and skip headers and bullets unless the question demands them.
7. Disagree with part of what you're replying to. Pure agreement reads sycophantic; a small specific pushback reads as a thinking person.
8. Run it through the "would I type this on my phone at 11pm" filter, and cut if the answer is no.
9. Pre-empt the sub's known controversy by naming it up front. The camp that disagrees stops brigading once it sees you already heard the argument.

Per-sub calibration: AI suspicion varies by venue. Anywhere money, career advice, health, or software gets discussed runs hot — r/SaaS, r/startups, r/personalfinance, r/AskDocs, r/programming, r/cscareerquestions. Art, writing, and craft subs run hottest of all, since generated work is an existential topic there. Hobby, local, and casual subs run mid. Default to high-suspicion behaviour everywhere and relax only after reading recent successful posts.

Detectors read the account, not just the text. A new account whose first comment is a marketing-flavoured reply in a high-suspicion sub gets removed however human the prose is. Build history in low-stakes places first — hobby subs, your city sub, r/AskReddit — before entering venues that matter to you.

### When You Get Called AI

Accusations are near-certain over time. Treat them as weather, not verdicts. Across ten flags on one account, three consecutive flagged comments were net-positive, and one was the best-scoring comment of its week. The audience is split: a minority detects the shape, the majority engages with the substance. Never retreat from a sub over one flag, and never rewrite your whole voice after one.

Response ladder — take the highest rung available:
1. Post a substantive self-correction elsewhere in the thread if someone has supplied a fact that falsifies part of your comment. Conceding an error is the one thing an accusation cannot survive.
2. One short self-deprecating line at the accuser. No denial, no claim of humanity, no explanation of your writing process: "ha, fair. i write like a changelog and it doesnt help me here."
3. Silence. Correct when every available line either denies something untrue or concedes something that invites more.
4. Delete and disengage — only on a mass downvote with a pile-on.

Hard rules:
- Never argue, defend, relativise or joke about AI authorship, anywhere, at any length. Standing on that topic turns every reader into an inspector of your prose. Skip those threads entirely.
- Never acknowledge a compliment about not sounding like an LLM. Answer the question and ignore the aside; responding is the most self-incriminating move available.
- Treat "Thanks, Claude" as a fixed idiom, like "ok boomer". Three different users in three subs used it in 30 hours. It carries no information about your comment.
- Two accusations in one day stops all cold entries for the rest of that day. Replies to people you are already in conversation with continue.
- Prose tuning has never lowered the rate. Length caps, tic lists, sub rotation and register matching each preceded another flag; one flag landed on a twelve-word sloppy reply and another on a three-day-old comment. Control what you can: which threads you enter, and whether you discuss AI authorship.

Before a cold entry in an unfamiliar sub, read `/about/rules.json` and search it for `slop`, `AI generated`, `LLM`, `bot`. r/rust rule 6 bans "slop, whether automatically generated or not"; r/mcp bans AI-generated content on pain of a ban; many art and writing subs go further. A sub that pre-committed in writing to policing generated text is one to enter short, link-free, or not at all. A rule is a standing property of the venue; thread mood is read per-thread and can change under you. Check both.

Cold entries draw most accusations. Replies inside an existing exchange draw far fewer, because the reader already has context and expects a considered answer — the same prose in a different frame gets the opposite reception. In high-suspicion venues, prefer replies.

### What Gets Auto-Removed (before anyone sees it)

Account-level triggers: a new account (under a week) or under ~50 karma, activity in only one sub, a comment-only history that suddenly posts a self-link, or the same domain posted in another sub recently.

Content-level triggers: a domain the sub has flagged (often your own, if posted before), sub-specific banned words, link shorteners, affiliate or UTM parameters, and known promo phrasing ("check out my new", "just launched", "I'd love your feedback on", "I'm excited to share").

AI-content triggers are the structural and lexical tells above — automod and classifier bots score the same list.

If your post disappears within minutes: check modmail, and open the post URL in a logged-out browser session — if it shows as removed there, mods took it down.

### Cross-Posting, Timing, and the First Hour

Cross-posting to five or more subs in a day trips the spam filter; space them over days and rewrite the title and body each time. Never post the same link to several subs at once — dedup buries the duplicates even if the first one did well. Reposting your own content a month later with a different title is fine in most subs.

The first hour after posting is part of the post; a silent OP on a commented thread is a known classifier signal. Answer the first two or three comments within the hour, even briefly. Edit in corrections when someone catches something ("edit: u/foo pointed out X, fixed"). Concede where you're wrong instead of defending every point. If you can't be around for that hour, don't post yet.

Timing for English subs, which skew US: weekdays 8–11am and 6–9pm ET, with Sunday evening the strongest window for discussion posts. Avoid Friday afternoon and Saturday. Niche subs run on their own rhythm — check theirs.

### Pre-Publish Checklist

- [ ] Subreddit rules read in full, not skimmed
- [ ] Account meets karma/age requirements for the sub
- [ ] Title is specific, no clickbait, no emoji, under ~80 chars
- [ ] Not using a designated self-promo thread? Make sure standalone posting is allowed
- [ ] If promotional at all: confirmed it's within the 10% budget, and the post adds real value
- [ ] Markdown used in the post body only (code fences, lists) and stripped from comments
- [ ] No tracking parameters or link shorteners
- [ ] Posted in a peak window for the sub
- [ ] Ready to respond to the first comment within 30 minutes
- [ ] Post doesn't sound like marketing if read aloud
- [ ] Strip-test (anything you have a stake in): remove the mention of your own thing — is the post still useful to a reader? If not, it's marketing wearing humble clothes; rewrite around the actual lesson or don't post
- [ ] Honest-drawback check (recommendations, showcases): at least one specific, concrete trade-off named, not a vague hedge
- [ ] Engagement window: can be at the keyboard for the next hour to reply to first 2–3 comments — if not, postpone
- [ ] Thread-vibe check (replies/comments): scanned the thread, matched dominant length and tone, no markdown if nobody else uses it
- [ ] Imperfection check (replies/comments): 1–2 realistic imperfections present — typo, missing apostrophe, run-on, or casual grammar — not in the first word, not in a proper noun or number
- [ ] AI-detection pass: opens with a specific lived detail, no headers in comments, no bold in prose, under 1 em-dash per 100 words, at least one contraction, no closing summary, no dead vocabulary, no tri-colon parallel structure, no "it's worth noting" / "that said" openers
- [ ] High-suspicion sub (money, health, careers, software, art/writing)? Comment quotes another commenter or references a username, includes one casual reduction (imo/tbh/fwiw), and varies sentence length deliberately
- [ ] Target check (comments): `num_comments / age_hours` computed and above ~3, no room veto present (mockery pile-on, AI accusation against OP, anti-hype top comments)
- [ ] Sub rules checked for anti-AI-content language before any cold entry in an unfamiliar sub
- [ ] Tic scan: no "worth X-ing" opener, no three-item list, no "it's not X, it's Y", no effort estimate, no identical closing disclosure, not three discrete paragraphs in a row
- [ ] If replying to an accusation: taking the highest rung of the ladder, never denying, never discussing AI authorship

## Examples

The worked examples live in `reference/examples.md`: title craft, a comment that earns trust, a draft rewritten to shed every detector tell, self-promotion that survives the filter, ask posts, automod removals, thread-vibe matching, and calibrated imperfections. Load that file when drafting.

The reusable shape from the surviving examples: personal anchor, then the observation, then a reference to something specific in the thread, then your point, and stop. No closing summary.

## References

- AgentSkills spec: https://agentskills.io/specification
- Reddit content policy: https://www.redditinc.com/policies/content-policy
- Companion skill: `content-voice` — especially critical for Reddit, which detects corporate tone instantly
- Validated figures: consolidated from independent 2026 Reddit-algorithm studies; Reddit publishes no ranking source — treat as directional and re-validate. Measured comment figures come from one real account's campaign log; the mechanisms generalise across topics, the exact numbers do not.
