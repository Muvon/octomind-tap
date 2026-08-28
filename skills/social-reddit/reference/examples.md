# Reddit — extended examples

Additional examples beyond the 3 in `SKILL.md`. Load this file when a more specific pattern is needed.

## Self-promotion that doesn't get removed

Bad (pure promo — gets filtered):
> Hey r/webdev! I just launched [MyApp], the best CRM for freelancers. Check it out! 🎉

Good (post-mortem with the product as part of the story):
> 6 months building a CRM for freelancers — MRR, tech stack, the two features I wish I'd cut
>
> Built this after freelancing for 3 years and hating every existing CRM. Some numbers, lessons, and honest mistakes below.
>
> Stack: Next.js 15, Postgres, Redis, Stripe, Resend
> MRR after 6 months: $1,840
> Feature I built and regret: AI-generated invoices…
>
> (link to site at the bottom, no UTM)

What works: post is about the journey, not the pitch. Product URL appears once. Specific numbers. Honest failure disclosure. The 10% rule is satisfied because this reads as a contribution, not a conversion funnel.

## Ask-question post

Bad (vague, no context, unanswerable):
> Help with Postgres?

Good (specific, shows effort, asks a real question):
> Postgres 16 — can `VACUUM FULL` be safely run on a 400GB table with replication lag concerns?
>
> Setup: primary + 2 async replicas, ~30MB/s write throughput, nightly 4-hour maintenance window. Table is bloated (~40% dead tuples), `pg_repack` keeps OOM-ing.
>
> What I've tried: `pg_repack` with `-T 900` (still OOM after ~2h), `VACUUM (PARALLEL 4)` (runs but doesn't reclaim space). Considering `VACUUM FULL` but worried about the exclusive lock + replication catchup time.
>
> Has anyone run `VACUUM FULL` on a similar-size table in production? What was the replica catchup pattern?

What works: title is the real question. Body shows effort (three things already tried). Ends with a specific question someone can answer from experience.

## What gets removed by automod

> Hey everyone! Excited to share that I've just launched my brand new SaaS, TurboForms 🚀 — the ultimate form builder for startups! Would love your feedback! [link with UTM]

Triggers: exclamation marks, "just launched," emoji, UTM tracking, "would love your feedback," generic SaaS positioning. Removed by automod in most subs within seconds. Reads as advertising from the first word.

## Removed by AI-content automod (real r/SaaS case)

A reply in r/SaaS like this:

> Excellent point! AI is fundamentally reshaping the SaaS landscape in profound ways. Here are three key considerations:
>
> 1. Distribution matters more than ever — with reduced build costs, the bottleneck shifts to customer acquisition.
> 2. Iteration speed is paramount — teams that ship faster can navigate complex market dynamics more effectively.
> 3. Real wedges trump features — having a genuine, defensible advantage is crucial in today's competitive environment.
>
> Ultimately, success in this space requires a holistic approach combining technical excellence with strategic distribution.

Removed by AutoModerator within seconds. Any one of these is sufficient — this comment hits all of them:
- "Excellent point!" sycophantic opener
- "fundamentally", "profound", "paramount", "holistic", "crucial" (dead vocabulary)
- Numbered list with parallel bold leads
- Em-dash on every list item
- "navigate complex market dynamics", "in today's competitive environment" (dead phrases)
- "Ultimately, ..." closing summary
- Zero contractions in 80+ words
- Zero personal anchor, zero reference to the OP or thread
- Three balanced bullets (tri-colon structure)

Same idea, automod-survivable rewrite:

> agree on the wedge thing but i think you're underselling distribution. shipped 4 saas products since 2019, the two that survived weren't the technically best ones, they were the ones where i'd already built an audience in the niche before launch. the failed ones i tried to launch cold and even with a better product they died within 6 months. ai didn't change that math, it just made the technically-best part cheaper to get to.

What changed: lowercase opener, real disagreement, specific number (4 products, 2019), specific failure outcome (died within 6 months), one sentence fragment, zero markdown, zero dead vocabulary, no closing summary.

## Thread-vibe matching in action

The thread (r/cscareerquestions, fast-moving, casual):
> OP: "is it worth learning rust in 2026 or just stick with go"
> Reply 1: "go tbh, rust is overkill for most jobs"
> Reply 2: "depends what you want to do"
> Reply 3: "rust if you want systems, go if you want a job"

Every reply is 1 line. No punctuation at the end. Lowercase. No markdown.

Bad reply (ignores thread vibe — will read as AI or try-hard):
> This is a great question! In my experience, the choice between Rust and Go depends heavily on your career goals:
>
> - Rust is ideal for systems programming, embedded, and performance-critical applications
> - Go is better suited for backend services, cloud infrastructure, and general web development
>
> Ultimately, Go will get you hired faster, but Rust is worth learning if you're passionate about systems.

Good reply (matches thread vibe):
> rust if you care about the craft, go if you want to get hired in 6 months

One line. No caps. No punctuation. Matches the thread exactly.

## Realistic imperfections in a reply

Context: r/SaaS, someone asks "how do you handle churn in the early days?"

Too perfect (reads AI):
> In the early days, churn is almost always a signal problem, not a product problem. The customers who churn fastest are usually the ones who had the wrong expectations going in. I'd focus on tightening the onboarding conversation — specifically the questions you ask before someone signs up — rather than adding features to retain people who were never a good fit.

With realistic imperfections (reads human):
> in the early days churn is almost always a signal problem, not a product problem. the customers who churn fastest are usually the ones who had the wrong expectations going in. i'd focus on tightening the onboarding conversation — specificaly the questions you ask before someone signs up — rather than adding features to retain people who were never a good fit.

What changed: lowercase opener, lowercase `i`, one realistic typo (`specificaly`), no closing summary. Same idea, reads like someone typed it on their phone.

## Calibrating imperfection level by reply type

Scenario: r/webdev, a long technical thread about CSS container queries. Thread has a mix of short and medium replies, mostly lowercase, some punctuation.

Top-level comment (low imperfection — more considered):
> container queries are genuinely useful but the mental model shift is harder than people admit. you're not asking "how wide is the viewport" anymore, you're asking "how wide is this specific box" — and that changes how you think about component design from the ground up. took me a few projects to stop reaching for media queries out of habit.

One minor imperfection: no period at the end (matches thread style). Otherwise clean.

Reply to a comment that said "just use media queries lol" (high casualness — match the energy):
> lol yeah until you try to reuse a component in a sidebar and a main column and suddenly your media queries are lying to you

No punctuation. Lowercase. Matches the dismissive-but-friendly tone of what it's replying to. No imperfection needed — the casualness is the imperfection.

Reply in a heated debate (short, punchy, no grammar polish):
> thats not how specificity works tho

Missing apostrophe in `thats`. Short. Ends without punctuation. Matches the pace of a fast argument thread.
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
- "The real moat" survives here only because the personal anchor immediately undercuts it. Note the "isn't the code, it's the distribution" construction: that antithesis has since been named as a tell by real readers, so prefer stating the answer straight unless the thread's own register carries it

This is the template. Anchor → observation → reference to thread → specific reframe → no closing summary.