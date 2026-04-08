 The Review Card: What It Is, Why It's Viral, How to Prompt It──────────────────────────────────────────────┤
  │ Real-time impact visualization        │ "What does this change affect at runtime?" — nobody answers this │
  The Gap Is Real and Nobody's In It──────┼──────────────────────────────────────────────────────────────────┤
  │ Spec ↔ Code ↔ Runtime unified         │ One view from intent through generated code to observed behavior │
  Every AI code review tool ($180M+ invested across CodeRabbit, Qodo, Greptile, etc.) does the same thing: adds comments to diffs. Nobody has replaced the diff as the primary
  surface. Devin Review comes closest (groups changes by intent) but still shows diffs underneath.───────────┤
  │ Cognitive-load-aware review           │ Apply beacon/chunking research to review UX (no tool does this)  │
  The opportunity: the card IS the review. The diff is the footnote.─────────────────────────────────────────┤
  │ Specification debugging               │ Debug ambiguous intent, not incorrect code                       │
  ---─────────────────────────────────────┴──────────────────────────────────────────────────────────────────┘
  What a Review Card Looks Like

  ┌──────────────────────────────────────────────┐
  │ 🟡 MEDIUM RISK          PR #847 · 3 cards    │
  ├──────────────────────────────────────────────┤
  │                                              │
  │  Card 1 of 3: Rate Limiting Added to API     │
  │                                              │
  │  WHY: Upstream service outage on March 12    │
  │  cascaded because we had no request limits.  │
  │                                              │
  │  WHAT CHANGED:                               │
  │  · New middleware: 100 req/s per tenant      │
  │  · 429 response with Retry-After header      │
  │  · Redis counter with sliding window         │
  │                                              │
  │  WHAT'S AFFECTED:                            │
  │  · Payment flow — will reject during spikes  │
  │  · Mobile app v2.3 — no retry logic yet (⚠️) │
  │  · Load tests need update                    │
  │                                              │ onto editors. Developers feel faster but aren't. The old tool with a new trick.
  │  RISK:                                       │
  │  · Clients with no backoff get hard failures │ure tools emerge. Developers work at intent and architecture level. Code generated but inspectable. Like early parametric CAD
  │  · Redis unavailability = open or closed?    │
  │    (currently: open — no limiting if Redis   │
  │     is down. Is this intentional?)           │a living model of the system. Code as compiled artifact. New kinds of software become possible that couldn't be designed by
  │                                              │wn by hand.
  │  ┌──────────┐ ┌──────────┐ ┌─────────────┐  │
  │  │ Approve  │ │ Comment  │ │ View Source ↓│  │came after CAD — someone who understands structures, materials, forces, and human needs. Not someone who draws lines. The ones
  │  └──────────┘ └──────────┘ └─────────────┘  │ribed: "A person that understands how to leverage software to solve problems" — not someone who writes code in an "arcane
  │                                              │
  │  [collapsed: 4 files, 127 lines changed]     │
  └──────────────────────────────────────────────┘ll make coding irrelevant as the primary activity — the way BIM made drafting irrelevant. The developer's job becomes:
  understand the problem, design the solution, verify it works, evolve it over time. The code is a byproduct.
  Progressive disclosure — three layers:

  ┌────────┬────────────────────────────────────────┬─────────────────┐
  │ Layer  │           What reviewer sees           │ Time to process │
  ├────────┼────────────────────────────────────────┼─────────────────┤
  │ Triage │ Risk badge + one-line summary per card │ 5 seconds       │
  ├────────┼────────────────────────────────────────┼─────────────────┤
  │ Card   │ Intent, impact, risks, questions       │ 30-60 seconds   │
  ├────────┼────────────────────────────────────────┼─────────────────┤
  │ Source │ Actual diff, file-by-file (expandable) │ As needed       │
  └────────┴────────────────────────────────────────┴─────────────────┘

  Most reviews stop at Layer 2. You open Layer 3 only when something smells off. This is the key insight: 80% of review decisions don't require reading code, they require
  understanding intent and impact.

  ---
  Will It Speed Up AI-Generated Code Review?

  Yes, specifically because it attacks the actual bottleneck.

  The Faros data: AI adoption → +91% review time, +154% PR size. Cisco research: reviewer effectiveness drops past 200-400 lines and collapses after 90 minutes. AI generates
  bigger PRs that take longer to review through the same 40-year-old diff interface.

  Cards fix this by:

  1. Chunking — cognitive science shows humans process information in chunks of 4-7 items. One 800-line PR becomes 3-5 cards of one concept each. Matches the brain's
  architecture.
  2. Top-down entry — research shows expert programmers use hypothesis-driven comprehension ("I think this adds rate limiting, let me verify"). Cards hand them the hypothesis
  directly instead of forcing them to build it from line-level diffs.
  3. Risk-first triage — reviewer spends 80% of attention on the 20% that's risky. Current diffs give equal weight to every line.
  4. Eliminating re-derivation — today, every reviewer independently derives the same understanding from the same diff. The card derives it once. Five reviewers × 15 minutes
  understanding = 75 minutes. Card = 5 × 1 minute.

  Estimate: 3-5x faster for the 80% of reviews that are approve/minor-comment. The remaining 20% (deep architectural issues) still needs source inspection, but the card tells
  you WHICH 20% to look at.

  ---
  Can It Go Viral?

  It has the strongest structural advantage of any dev tool category:

  Every PR is a product demo. Unlike Cursor (requires download) or Linear (requires migration), the card appears inside the GitHub PR where developers already work. Dev A
  installs the GitHub App → every PR on the repo now has cards → every reviewer on the team sees them → they install it on their repos. The Calendly pattern: usage IS
  distribution.

  The viral mechanics that apply:

  ┌────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │        Mechanic        │                                           How it works here                                            │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Single-player value    │ Works for ONE person reviewing their own PR before team buys in                                        │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Ambient demonstration  │ Every PR reviewer sees the card without installing anything                                            │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Visual "wow" artifact  │ Cards are screenshotable. Inline comments are not. Devs will tweet "look what this caught"             │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Enemy positioning      │ "Kill the diff" — clear, emotional, relatable enemy                                                    │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Bottom-up infiltration │ Individual → team → org → enterprise. GitHub App model enables this                                    │
  ├────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ Low adoption friction  │ One-click GitHub App install. No migration. No workflow change. Cards appear alongside existing review │
  └────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Critical requirement: signal-to-noise ratio. The #1 killer of AI review tools is false positives and verbose noise (CodeRabbit's main complaint on G2). The card must be
  opinionated and sparse — better to miss a minor issue than cry wolf. If the LLM isn't confident, the card should say nothing, not hedge with caveats.

  ---
  The LLM Prompt Framework

  This is the core IP. The prompt needs to produce Endsley Level 1+2+3 (perception + comprehension + projection) from a diff. Here's the framework:

  ## System Prompt: Review Card Generator

  You are a senior staff engineer generating review cards for code changes.
  Your audience is a reviewer who has NOT seen this code before.

  ### CARD STRUCTURE (strict, every card must have all sections)

  **INTENT** (one sentence):
  Why does this change exist? Not what it does — why it was needed.
  Link to ticket/issue if available.

  **CHANGE SUMMARY** (bullet points, max 5):
  What happened, described as BEHAVIORS not code.
  Bad:  "Added timeout parameter to fetch call in api.ts line 47"
  Good: "External API calls now timeout after 5 seconds instead of hanging indefinitely"

  **IMPACT RADIUS** (bullet points):
  What else in the system is affected by this change?
  For each: name the component + describe the effect + flag if breaking.
  If nothing is affected, say "Isolated change — no downstream impact detected."

  **RISK ASSESSMENT** (only if non-trivial):
  What could go wrong? Be specific:
  - Edge cases the author may not have considered
  - Behavioral changes that existing consumers depend on
  - Missing error handling for new failure modes
  - Security implications
  Flag as: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW
  If risk is LOW and obvious, omit this section entirely.

  **QUESTIONS FOR AUTHOR** (only if genuinely unclear):
  Decisions that look intentional but could be accidental.
  "Redis failure mode is set to open (fail-open). Was this intentional,
  or should this fail-closed to maintain rate limits?"
  Never ask questions you could answer by reading the code more carefully.

  ### GROUPING RULES

  Do NOT create one card per file. Create one card per LOGICAL CHANGE.
  A logical change = one intent/motivation, even if it spans 10 files.

  Examples:
  - Renaming a function across 15 files = 1 card
  - Adding a feature + updating tests + fixing a typo = 2 cards
    (feature+tests = one intent, typo = separate intent)
  - Refactoring auth + adding rate limiting = 2 cards
    (different motivations even if same files touched)

  ### WHAT TO OMIT

  - Do not describe formatting changes, import reordering, or whitespace
  - Do not describe test changes unless the test reveals non-obvious behavior
  - Do not flag style/convention issues (linters handle this)
  - Do not praise the code. Do not say "great work" or "nice refactor"
  - Do not hedge. If you're not confident about a risk, say nothing
  - Do not generate more than 5 cards. If the PR is that large,
    the top-level summary should say "This PR should be split"

  ### TONE

  Write like a busy staff engineer reviewing a PR at 9am with coffee.
  Direct, specific, no filler. Every word must earn its place.

  The key design choices in the prompt:

  1. "Behaviors not code" — forces the LLM to describe what changed for users/system, not what changed in files
  2. "One card per logical change" — maps to cognitive chunking research
  3. "Omit if LOW risk" — prevents noise, the #1 killer
  4. "Questions only if genuinely unclear" — prevents sycophantic "have you considered..." padding
  5. "Never ask questions you could answer" — forces the LLM to do the work, not punt to reviewer
  6. Strict section structure — reviewers learn the card format once, then scan by position (like how you read a familiar dashboard)

  What the LLM Actually Needs as Input

  The prompt above is the output format. The input matters just as much:

  1. The diff (obviously)
  2. The PR description / commit messages
  3. The linked ticket/issue (if available)
  4. File-level context: surrounding code for each changed file
     (not just the diff — the LLM needs to see what the change
     sits inside to assess impact)
  5. Repository structure / dependency graph
  6. Recent related PRs (optional — for "part 2 of 5" narratives)

  Items 4 and 5 are what separates a good card from a useless one. Every AI review tool that just feeds the diff produces surface-level comments. The context window is the moat
   — the more of the codebase the LLM sees, the better the impact analysis.

  ---
  The Minimum Viable Product

  1. GitHub App — installs in one click
  2. On PR open/update → LLM generates cards → posts as a single formatted comment (not inline comments scattered across files)
  3. Cards in the comment body with collapsible sections
  4. "View Source" links jump to the relevant diff lines
  5. Reviewer reacts with 👍 (useful) or 👎 (noise) → feedback loop

  That's it. No separate UI. No migration. Lives in GitHub where reviewers already are. The card IS the comment, just structured differently than what any tool does today.

  The moment it becomes viral: when a reviewer opens a 600-line PR, sees 3 clean cards, understands the entire change in 90 seconds, approves in 2 minutes, and thinks "I need
  this on every repo."

✻ Cogitated for 6m 51s
