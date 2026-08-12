# HN — extended examples

Additional examples beyond the 3 in `SKILL.md`. Load this file when a more specific pattern is needed.

## Real winners, mid-2026 (measured, not invented)

Show HN titles that broke 900 points in one quarter, annotated by pattern:

| Points | Title | Pattern |
|---|---|---|
| 2,935 | I replaced a $120k bowling center system with $1,600 in ESP32s | Origin story + cost contrast |
| 1,679 | Elevators | Bare intrigue (self-evident link) |
| 1,481 | Homebrew 6.0.0 | Known name + version, nothing else |
| 1,181 | Performative-UI – A react component library of design tropes | Name – capability, with a wink |
| 1,033 | Bento - An entire PowerPoint in one HTML file (edit+view+data+collab) | Name – impossible-sounding capability |
| 919 | Open-source engine running Gemma 4 26B in 2 GB RAM on any M-series Mac | Constraint numbers as hook |

## Real Show HN submission text (the winning shape)

The 2,935-point bowling post opens its submission text field like this (abridged):

> I might be the only SRE on Earth with his own bowling center. It's a more in-depth gig than you'd think. My family and I bought an abandoned 8-lane bowling center in the rural mid-west. [...] The system that keeps your score is particularly interesting to me. [...] Turns out these things are really cool, but absurdly expensive. Ours was installed in 2008 and cost six figures.

Why it works: one improbable-but-true sentence up front, personal stakes, zero product language, and every claim concrete (8 lanes, 2008, six figures). The 1,033-point Bento post uses the same shape for a dev tool: real workflow pain ("to make even small edits we need to edit the code"), what it is ("a single HTML file with everything you need in a slide tool"), then verifiable specifics ("the default deck is around 560 KB", "no cloud login, everything works offline").

The author's first comment then goes one level deeper technically (Bento: how the base64 blob decompresses via DecompressionStream, File System Access API writeback) or asks voters a direct question (18 Words: "Two questions: 1. … 2. …"). Depth in the comment, story in the text field.

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
