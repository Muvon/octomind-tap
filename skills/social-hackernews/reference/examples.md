# HN — extended examples

Additional examples beyond the 3 in `SKILL.md`. Load this file when a more specific pattern is needed.

## Show HN title

Bad (marketing, adjectives, exclamation):
> Show HN: TurboForms - The Ultimate Form Builder for Modern SaaS 🚀!

Bad (too vague, no information):
> Show HN: My new side project

Good (specific, neutral, informative):
> Show HN: A form builder that outputs raw HTML and zero JavaScript

What works: says exactly what it does, has a specific technical angle (no JS) that HN readers will find interesting, no adjectives, no marketing.

## Title for a linked article

You're submitting: `"Why we moved from Kubernetes to Nomad: a 12-month retrospective - InternalDevBlog"`

Bad (kept site name, re-phrased):
> Why our team left Kubernetes for Nomad (awesome retrospective!)

Good (article's original title, site stripped, no editorializing):
> Why we moved from Kubernetes to Nomad: a 12-month retrospective

HN rule: use the original title unless misleading or clickbait. Strip site name. No commentary.

## Thread-vibe matching (technical deep-dive thread)

Show HN post about a SQLite-per-tenant architecture. Thread vibe: technical, 3–5 sentence comments, citing specific numbers and trade-offs.

Bad comment (ignores vibe — too casual for a technical thread):
> lol yeah sqlite is great, we use it too and its way easier than postgres tbh

Good comment (matches technical register, structural imperfection only):
> Ran into the same trade-off last year. Went with SQLite-per-tenant for a similar reason — write contention on a shared Postgres was killing p99 latency at ~2k concurrent tenants.
>
> One thing worth watching: WAL mode is essential, and you'll want to tune `PRAGMA journal_size_limit` or your WAL files balloon under write-heavy tenants. Caught us off guard in staging.

What works: matches technical depth, cites a specific production number (2k concurrent tenants), adds a concrete gotcha (WAL file size), informal opener (`Ran into`) is the only structural imperfection — no typos, no casual slang.

## Comment with calibrated imperfection (Ask HN thread)

Ask HN: "How do you evaluate long-context LLMs for retrieval tasks?"

Thread vibe: practitioners sharing real experience, 3–6 sentences, specific setups.

Bad comment (over-imperfected for HN):
> honestly idk lol we just kinda tried stuff and it worked out, ngl the whole eval thing is kinda a mess

Good comment (very low imperfection, matches practitioner register):
> Built a domain-specific eval for this last quarter. The key insight: synthetic evals (needle-in-haystack, LongBench) don't predict real retrieval quality on your data. They measure capability, not fit.
>
> What worked for us — take 200 real queries with known-good answers from your existing system, run them through the new model, and score with a cheap LLM judge. Imperfect but correlates with user satisfaction better than any benchmark we tried.

What works: `Built a` opener (dropped subject — structural imperfection), specific number (200 queries), honest about limitations ("Imperfect but"), adds a concrete method, no typos, no casual slang.
