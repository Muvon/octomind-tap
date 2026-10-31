# SEO MCP Providers: Keyword Data, Public Research and Search Console

The default is `public.toml`: existing keyless DuckDuckGo search plus public-page inspection. It does not supply monthly volume, keyword difficulty, backlink metrics, DR, or observed AI answers. Both SEO agents and the GEO/keyword-research skills use this baseline without credentials. Shared websearch/webfetch servers are deduplicated during manifest resolution.

## Choose a provider

Users select one provider with `[capabilities] seo-data = "<provider>"` in their own Octomind configuration; manifests only name `seo-data`, and this registry does not edit that file. No provider is automatically chosen merely because a credential exists. Missing required variables withhold the authenticated provider at runtime; separately declared websearch/webfetch remain available.

| Provider | Evidence | Required environment | Access |
|---|---|---|---|
| `public` (default) | Public pages and search discovery | None | Keyless; upstream search may rate-limit |
| `dataforseo` | Keyword, SERP, competitor, backlink API data | `DATAFORSEO_LOGIN`, `DATAFORSEO_PASSWORD` | API credentials, Node.js 22+, pay-per-use |
| `ahrefs` | Ahrefs keywords, backlinks and actual Ahrefs DR | `AHREFS_MCP_TOKEN` | Hosted MCP, MCP-scoped key, eligible paid plan/units; check client eligibility |
| `semrush` | Keyword, domain and backlink reports | `SEMRUSH_API_KEY` | Hosted MCP, eligible subscription and API units |
| `seranking` | Keywords, SERPs, backlinks and domain data | `SERANKING_API_KEY` | Hosted MCP, SE Ranking/SE Visible API Dashboard key and entitlement |
| `serpstat` | Keyword, domain and backlink research | `SERPSTAT_API_TOKEN` | Official npm MCP, API-enabled plan (documented Team+); research categories only |
| `search-console` | Authorized first-party performance and URL inspection | `GOOGLE_APPLICATION_CREDENTIALS` | Absolute path to private service-account JSON; enable API and grant property access |
| `free-seo` (experimental) | Autocomplete suggestions and relative Trends | None for exposed tools | Third-party Git-pinned server, Python 3.11 via uv; unofficial endpoints, no volume guarantee |

Search Console is a community MCP wrapper around Google's API, not a Google-published MCP server. Its credential file must remain outside version control. The registry exposes only read tools and excludes `submit_sitemap`; Google's `webmasters.readonly` OAuth scope is used upstream. It is complementary to competitor data, not an equivalent replacement. Search Console's Generative AI performance report shows impressions, not clicks, for AI Overviews and AI Mode, and Web totals also include these features; don't infer AI-specific clicks from either.

The experimental free-seo profile exposes `suggest`, `trends_compare`, and `trends_related`, not Bing tools, volume estimates, storage helpers, or crawl expansion. Upstream Bing support requires `FREE_SEO_BING_API_KEY` but is not enabled here. Trends is relative interest, not monthly demand. Autocomplete/Trends can fail or rate-limit; do not solve CAPTCHAs or treat unavailable data as zero. The full Git commit is pinned; transitive dependencies follow upstream constraints.

## Authentication and safety

Remote providers use native HTTP MCP with documented header authentication, not an interactive OAuth bridge or obsolete local packages:

- Ahrefs: `Authorization: Bearer <MCP token>` at `https://api.ahrefs.com/mcp/mcp`. Generate an MCP-scoped key in Ahrefs account settings; its external endpoint is for permitted AI clients, not custom API scripts/bridges. Confirm Octomind client eligibility with Ahrefs before use.
- Semrush: `Authorization: Apikey <API key>` at `https://mcp.semrush.com/v2/mcp`.
- SE Ranking: `X-Api-Key: <API key>` at `https://api.seranking.com/mcp`.
- Serpstat (local npm server) reads `SERPSTAT_API_TOKEN`, not `SERPSTAT_API_KEY`.

Secrets are injected through `env`/`headers`, never arguments. Offline resolution preserves placeholders; it does not authenticate. Hosted providers need no local dep scripts.

Inspect the connected tool schemas and endpoint docs, confirm report scope/budget before billable calls, and record provider, endpoint, locale, retrieval time, and returned cost. No publishing, project mutations, sitemap submission, profile claims, or paid scan starts without separate explicit authorization. Serpstat excludes non-research categories. Only Ahrefs supplies Ahrefs DR; other authority/difficulty scores are provider-specific. Provider data is not an observed ChatGPT/AI Overview/UI answer unless the exact surface and capture method establish it.

## Validation

Run `bash scripts/setup-symlinks.sh`, `bash scripts/lint-capabilities.sh capabilities/seo-data`, `python3 scripts/test-seo-providers.py`, `bash scripts/validate-capabilities.sh`, and `scripts/mcp-versions.sh test seo-data`.

MCP initialization and tools/list do not prove authenticated data access, current API entitlements, endpoint reliability, or successful paid calls. Hosted endpoints require an authorized native client smoke test with the user's credentials; do not issue billable requests just to validate wiring.

## Sources

- Ahrefs: https://docs.ahrefs.com/mcp/docs/tool-categories.md and https://docs.ahrefs.com/mcp/docs/manus.md
- Semrush: https://developer.semrush.com/api/introduction/semrush-mcp/
- SE Ranking: https://seranking.com/api/integrations/mcp
- Serpstat: https://github.com/SerpstatGlobal/serpstat-mcp-server-js
- Search Console wrapper: https://www.npmjs.com/package/mcp-server-gsc
- Search Console authorization: https://developers.google.com/webmaster-tools/v1/how-tos/authorizing
- Experimental source: https://github.com/JohnWayneeee/free-seo-mcp
