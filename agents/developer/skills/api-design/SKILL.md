---
name: api-design
title: "API Design for REST, GraphQL and Webhooks"
description: "API contract design: RFC 9457 errors, idempotency keys, cursor pagination, versioning, deprecation, webhook signing, OpenAPI. Use to design an API."
license: Apache-2.0
compatibility: "Optional: an OpenAPI linter (Spectral) and a breaking-change checker (oasdiff) on PATH."
rules:
  - content(openapi)
  - content(graphql)
  - content(webhook)
  - content(webhooks)
  - content(idempotency)
  - match((?i)\b(rest(ful)?\s+apis?|api\s+(design|contract|errors?|versions?|versioning|deprecation)|design\s+(an?\s+|the\s+|our\s+)?(api|endpoints?))\b)
  - match((?i)\b(paginat\w*|idempoten\w*|swagger|problem\s+details|rfc\s*9457)\b)
  - match((?i)\bversion(ing)?\b.{0,20}\bapi\b)
---

## Overview

An API is a contract that outlives the code behind it. Use this skill when a request designs endpoints or a schema, reviews an existing API, adds pagination, errors, versioning or webhooks, or writes an OpenAPI document. The deliverable is a contract (an OpenAPI or GraphQL schema plus the rules behind it) that a client can implement without asking questions, with changes classified as breaking or not. Read the project's existing API conventions first and follow them; only propose a different convention for new surface.

## Mental model

Clients cannot be upgraded on your schedule, so every released field, status code and error shape is a promise. Design for retries (networks fail after the server acted), for growth (lists get large, fields get added), and for removal (every endpoint eventually retires). A change is breaking if a correct existing client can fail because of it.

## Rules

### Resources and methods

- Name resources with nouns and plural collections (`/orders/{id}`); model actions that are not CRUD as a sub-resource or a verb endpoint with `POST`, and say so in the contract.
- `GET` is safe and cacheable; `PUT` and `DELETE` are idempotent; `POST` and `PATCH` are not unless made so. State the idempotency of every operation in the contract.
- Return `201` with a `Location` header on creation, `204` for success without a body, `409` for state conflicts, `422` for well-formed but invalid input, `429` with `Retry-After` when throttling.
- Accept unknown request fields only if you document it; otherwise reject them. Clients must ignore unknown response fields, and the contract says so.

### Errors: RFC 9457

Use Problem Details (RFC 9457, July 2023, obsoletes RFC 7807) with media type `application/problem+json`.

| Member | Rule |
|---|---|
| `type` | URI that identifies the problem kind; clients branch on it. Use an absolute URI; defaults to `about:blank` when omitted |
| `status` | The HTTP status of this response; must equal the real status |
| `title` | Short, stable across occurrences |
| `detail` | Explains this occurrence so the client can fix it; no stack traces or internals |
| `instance` | URI identifying this occurrence (a request or trace id) |

Add extension members for machine-readable detail (for example an `errors` array with a JSON pointer per field). Clients ignore extensions they do not know. Use one error shape for the whole API, including 401, 403, 404 and 5xx.

### Idempotency keys

For `POST` operations that create or charge, accept an `Idempotency-Key` request header. The IETF draft (`draft-ietf-httpapi-idempotency-key-header-08`, 2026-10-22) is still an Internet-Draft, not an RFC, so document the behavior in your own contract:

- Key missing where required: `400`. Same key with a different payload: `422`. Same key while the first request is still running: `409`. Same key after completion: replay the original response.
- Store the key, a fingerprint of the request, and the response for a fixed retention window (state it, for example 24 hours), scoped per client. Make the check and the write atomic (a unique constraint), not read-then-write.

### Pagination

- Use cursor (keyset) pagination for any collection that can grow: an opaque `cursor` or `page_token`, a `limit` with a documented default and maximum, and `next_cursor` (absent or null on the last page). Offsets get slower with depth and skip or repeat rows when data changes between requests.
- Order by a unique, stable key (created time plus id). Document the order; never change it later.
- GraphQL: use the Relay connection shape (`edges { node cursor }`, `pageInfo { hasNextPage endCursor }`) with opaque cursors; bound every list field.
- Return a total count only when it is cheap or optional; counting a large table on every page is a hidden cost.

### Versioning and deprecation

- Prefer additive evolution inside one version: add optional fields, new endpoints, new enum values only if clients are told to tolerate unknown ones. Anything else is a new version.
- Breaking: removing or renaming a field, changing a type, making an optional input required, tightening validation, changing a default, changing an error `type`, adding an enum value for clients that switch exhaustively.
- Put the version in the URL path (`/v2/`) or a header; pick one for the whole API.
- Announce retirement with the `Deprecation` header (RFC 9745, March 2025: a structured-field date such as `Deprecation: @1688169599`) and the `Sunset` header (RFC 8594: an HTTP-date; it must not be earlier than the deprecation date), plus a `Link` header with `rel="deprecation"` pointing at the migration guide. These headers are hints; also tell consumers directly and measure remaining traffic by client before removal.

### Webhooks

Follow the Standard Webhooks specification unless the project has its own scheme.

- Headers: `webhook-id` (stable per event, so receivers can deduplicate), `webhook-timestamp`, `webhook-signature`.
- Sign the string `msg_id.timestamp.payload` with HMAC-SHA256 (signature prefix `v1,` plus base64) or ed25519 (`v1a,`). The signature header may carry several space-separated signatures, which allows rotating a secret without downtime. Secrets are random, 24 to 64 bytes, base64, prefixed `whsec_`.
- Receivers verify the signature over the raw body, compare in constant time, and reject timestamps outside a tolerance window (the spec sets no value; choose and document one, such as five minutes). Receivers answer fast with `2xx` and process asynchronously.
- Senders count only `2xx` as success (a redirect is a failure), retry with exponential backoff and jitter over days (the spec's example schedule: immediately, 5 s, 5 min, 30 min, 2 h, 5 h, 10 h, 14 h, 20 h, 24 h), disable an endpoint that returns `410 Gone`, and tell the owner when delivery fails for a long time. Delivery is at least once and unordered; say so and include an event id and a version or timestamp.

### GraphQL operations

Bound cost, since one request can ask for a lot: depth limits, breadth and alias limits, query complexity weights, rate limits based on cost rather than request count, timeouts, and trusted (persisted) documents for first-party clients. Mask resolver error details in production. Disabling introspection outside development is a supplement, not protection.

### OpenAPI as the contract

- OpenAPI 3.2.1 is the latest published version (as of 2026-11; read spec.openapis.org/oas for the current one). Write the document first or generate it from code, but commit it and treat it as source of truth.
- Every operation has an `operationId`, request and response schemas, the shared `application/problem+json` error responses, and examples. Reuse schemas through `components`.
- Lint with Spectral (`spectral lint openapi.yaml`, ruleset `spectral:oas` plus project rules). Compare the new document with the released one using oasdiff (`oasdiff breaking old.yaml new.yaml`) in CI, and fail the build on an unapproved breaking change.

## Examples

Bad: generic error, offset paging, unsafe retry.

```http
POST /charges            -> 500 {"error": "failed"}
GET  /orders?page=40&size=100
```

Good: typed error, cursor paging, retry-safe create.

```http
POST /charges
Idempotency-Key: 8f0c2c5e-...
-> 422 Content-Type: application/problem+json
{"type":"https://api.example.com/problems/card-declined","title":"Card declined",
 "status":422,"detail":"The card was declined by the issuer.","instance":"/requests/req_91"}

GET /orders?limit=100&cursor=eyJpZCI6MTIzfQ
-> 200 {"data":[...],"next_cursor":"eyJpZCI6MjIzfQ"}
```

## Checklist

- Every operation states its idempotency, its error responses, and its auth requirement.
- Errors use one problem+json shape; `status` matches the HTTP status.
- Every list is paginated with an opaque cursor, a default and a maximum limit, and a fixed order.
- Each change is classified breaking or non-breaking; breaking changes get a new version or a deprecation window with `Deprecation` and `Sunset` headers.
- Webhooks are signed, timestamped, deduplicable, and retried; the receiver contract states the tolerance window.
- The OpenAPI file lints clean and the breaking-change check passes; commands were run or the report says they were not.

## References

- [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html)
- [Idempotency-Key header draft](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
- [RFC 9745 Deprecation header](https://www.rfc-editor.org/rfc/rfc9745.html) and [RFC 8594 Sunset header](https://www.rfc-editor.org/rfc/rfc8594.html)
- [Standard Webhooks](https://www.standardwebhooks.com/) and [its specification](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md)
- [OpenAPI Specification](https://spec.openapis.org/oas/), [Spectral](https://github.com/stoplightio/spectral), [oasdiff](https://github.com/oasdiff/oasdiff)
- [GraphQL pagination](https://graphql.org/learn/pagination/) and [GraphQL security](https://graphql.org/learn/security/)
