# SEO registry metadata review

Reviewed 2026-10-30. Scope: the SEO/GEO agent and skill metadata, SEO-data provider additions, and their supporting documentation. This is a source-level editorial SEO pass, not a deployment, indexing, ranking, or authenticated-provider test.

## Search intent and comparison evidence

Web-search queries used for qualitative intent discovery:

- `SEO MCP servers keyword research Search Console` — connection/setup and provider-selection intent. Results distinguish keyword/backlink databases, first-party Search Console analytics, and site inspection. The registry should name the actual job and authentication boundary, not imply that every provider supplies every kind of SEO data.
- `long tail keyword research SERP analysis content gap low competition` — research-method and prioritized-content-opportunity intent, not automatic publishing or guaranteed rankings. Competing results include [a content-gap methodology](https://github.com/rampstackco/claude-skills/blob/main/skills/seo-competitor/references/content-gap-method.md) and [Query Hunter](https://chromewebstore.google.com/detail/query-hunter/odgolnndpdjdoelhnokhgcdlfdachfhc), which mines existing Search Console opportunities.
- `AI search visibility audit buyer questions citations GEO` — observed brand recommendations/citations and readiness audits are distinct deliverables. Results include [a captured-answer audit skill](https://github.com/mikefutia/ai-visibility-audit/blob/main/SKILL.md) and [a page-readiness audit](https://apify.com/jumpy_invoice/geo-visibility-audit-intelligence). Our descriptions retain the captured-answer evidence requirement rather than promising a live engine measurement from public-page inspection.

Inspected comparison-page passages from [Themeisle](https://themeisle.com/blog/best-seo-mcp-servers/) and [squirrelscan](https://squirrelscan.com/learn/seo-mcp-server): both organize providers by data job, access, and setup. These are editorial/vendor comparisons, not ranking rules or independent product verification. Provider claims were checked against the primary documentation linked in the [provider guide](README.md), including Ahrefs tool categories, Semrush MCP, SE Ranking MCP, Serpstat's repository, DataForSEO's repository, and free-seo's repository. The npm Search Console page returned HTTP 403 during this pass; wrapper behavior rests on the previously inspected pinned package and registry configuration, not on a different Search Console package appearing in search results.

Search results are tool-returned discovery evidence, not a captured Google SERP or AI-answer run. No monthly volume, keyword difficulty, attainable position, or traffic estimate was measured.

## Item-by-item decisions

Provider descriptions were checked against exposed tools, not the full upstream product catalog. Authentication requirements remain in descriptions or adjacent setup guidance.

| Item | Intent and decision |
|---|---|
| `public.toml` | Revised title/description to keyless SEO research and public-page inspection; explicitly excludes metrics and AI-answer tracking. |
| `dataforseo.toml` | Revised title to name MCP and keyword/SERP/backlink data; retained the accurate credential-specific description. |
| `ahrefs.toml` | Revised title/description to name keywords, backlinks, and Domain Rating; hosted MCP and access requirements remain explicit. |
| `semrush.toml` | Revised title to keyword/domain/backlink research via MCP; retained accurate hosted-provider description and API-access condition. |
| `seranking.toml` | Revised title to keyword/SERP/backlink data via MCP; retained description and entitlement condition. No blanket AI-visibility promise. |
| `serpstat.toml` | Revised title to keyword/competitor research via MCP; retained description consistent with restricted research categories. |
| `search-console.toml` | Revised title/description to read-only, first-party search performance and authorized URL inspection, not competitor or market-wide keyword metrics. |
| `free-seo.toml` | Revised title/description to autocomplete and relative Google Trends; removed the implication that this restricted profile exposes Bing metrics. Experimental status and no-volume limit are explicit. |
| `../../agents/seo/audit.toml` | Retained `SEO and GEO Auditor` and its description: diagnostic findings, technical/content/link checks, and captured-answer visibility gaps match the role. |
| `../../agents/seo/strategist.toml` | Retained `SEO and GEO Strategist` and its description: keyword/content plans and buyer-question-led experiment briefs, not implementation. |
| `../../skills/geo-visibility-audit/SKILL.md` | Retained `AI Search Visibility Audit` and its concise evidence-led description; no implied engine access or citation guarantee. |
| `../../skills/seo-keyword-research/SKILL.md` | Retained the specific long-tail research title; replaced the long description's ranking/citation promises with the actual intent-analysis, expansion, competitor-review, and keyword-brief deliverable. Corrected the contradictory mandatory-DR gate and Search Console metric attribution in the related guidance. |
| `../../skills/geo-visibility-audit/reference/audit-contract.md` | Retained `GEO Audit Report Templates` title/description: reusable records and before/after checks, not an observed audit result. |
| `../../skills/seo-keyword-research/references/brief-template.md` | Retained the reference heading `Keyword Brief Template`; an output template, not another keyword-research landing page. |
| `../../skills/seo-keyword-research/references/modifier-library.md` | Retained `Long-Tail Modifier Library` reference heading; supports query expansion rather than duplicating the skill's title. |
| `README.md` | Revised heading to identify SEO MCP provider selection, keyword data, public research, and Search Console; linked this review and replaced the failed Ahrefs introduction link with its tool-category reference. |
| `../../deps/johnwayneeee/free-seo.md` | Retained required dep-ID heading and accurate experimental setup summary; restricted tools and relative-interest limits remain explicit. |
| `../../deps/google/search-console.md` | Retained required dep-ID heading and community-wrapper summary; authorized first-party access and excluded submission tools are clear. |
| `../../deps/serpstat/serpstat.md` | Retained required dep-ID heading and research summary; correct token name, credits, and restricted categories match configuration. |
| `../../deps/dataforseo/mcp-server.md` | Retained required dep-ID heading and setup summary; Node.js requirement, API credentials, and billable-request boundary match the provider. |
| `../../deps/ahrefs/ahrefs.md` | Added a legacy-package warning and directed new connections to hosted `seo-data:ahrefs`; this document is not evidence that the old npm package was tested. |

## Acceptance and limits

- Titles/descriptions are distinct, readable, aligned with the actual deliverable, and free of guaranteed rankings, citations, or traffic. Registry character limits are contribution constraints, not Google display limits.
- No trigger or semantic-rule changes; no retraining is required. No provider wiring, version pins, or authentication mechanism changed in this metadata pass.
- No deployed catalogue URL or source-to-HTML mapping was supplied or established. Served `<title>`, meta description, canonical, robots/snippet directives, crawler eligibility, and indexing remain Unverified. Registry comments/frontmatter are not proof of published HTML metadata.
- Once a deployed URL is available, verify rendered metadata against these source fields, inspect canonical and indexing/snippet controls, and check owner indexing data before calling deployment or indexing verified. No sitemap submission or publishing is authorized by this review.

Editorial criteria: Google's [title-link guidance](https://developers.google.com/search/docs/appearance/title-link) and [snippet guidance](https://developers.google.com/search/docs/appearance/snippet): descriptive, concise, distinct titles and accurate page-specific summaries; neither has a fixed Google character limit.
