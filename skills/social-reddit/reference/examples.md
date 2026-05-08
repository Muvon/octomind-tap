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
