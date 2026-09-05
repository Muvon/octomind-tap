## Account setup and publishing checks

Use this reference before account setup or a publishing package involving optional formats. Record the actual server and client, retrieval date, observed controls, and source URLs. Treat an unavailable check as unverified; don't silently substitute a remembered limit (directional).

### Limits and optional formats

These are live verification procedures, not claims that every server exposes the same defaults (directional).

| Item | Check before marking ready |
|---|---|
| Post length | Inspect the connected server's instance response, starting with `/api/v1/instance`; look for `configuration.statuses.max_characters`. If unavailable, use its current documentation or composer counter. Validate final copy with URLs, tags, CW, and disclosure included. |
| Multi-image post | Read the accepted image count, formats, and per-file size limits. Confirm ordering and crops in preview; describe each image separately. |
| Video or audio | Read accepted formats and file-size limits before commissioning the asset. Check playback, supply captions or a transcript, and inspect attachment compatibility. |
| Alt text | Check the actual description-field character cap. Describe visible evidence and relevant embedded text; link an accessible table or transcript when the complete content won't fit. Check any client reminder independently from server enforcement. |
| Poll | Check option count, option length, expiry, selection mode, and media compatibility. Use non-overlapping choices for a defined decision; include an honest abstention option when needed. Preserve the question and limitations when reporting results. |
| Scheduled post | Check whether the chosen client or integration supports scheduling and inspect timezone and pending queue. Recheck time-sensitive claims before release; appoint a person to answer replies. |
| Edited post | Check what the current UI exposes in edit history and notifications. Preserve the original evidence, correct errors openly, and don't promise that previous text disappears. |
| Language | Set the post language to the language actually written. Inspect audience language preferences without claiming a delivery guarantee. |
| Custom emoji | Choose only available shortcodes that suit the author's existing usage. Preview rendering; don't imply identity verification through an emoji. |
| Followers or specific recipients | Read the audience explanation and recipient list. Don't describe a mentioned-only exchange as a secure customer-support channel. |

Exact character, media, poll, and description caps are intentionally runtime checks. A universal number without server evidence would give false precision. Obtain that evidence before sizing an asset or promising publication readiness.

### Profile as a useful destination

Write a display name and bio that identify the person or project, explain its scope, and disclose the relationship. Fill available profile fields with useful destinations instead of slogans. Introduce the account with its real purpose and a useful contribution; consider `#introduction` only after checking relevant live usage (directional).

An HTTPS profile field can verify through a matching `rel=me` backlink. A trusted owned domain is an identity option described in the docs, not a promised distribution advantage (official, Profile, 2026-04). Check the backlink from the actual linked page and view the resulting profile.

Pin current public material that helps a newcomer evaluate the account. The documented maximum is 5 public pinned posts; featured hashtags show use counts and last-use dates (official, Discoverability, 2024-10). Choose useful proof and an accurate introduction; don't fill every slot automatically (directional).

Featured hashtags became more prominent, with controls for Media and Featured tab visibility and inclusion of reply media. Profile pictures and headers gained descriptions and in-place cropping in Mastodon 4.6 (official, Release, 2026-06). Describe the avatar/header and preview the public profile; don't assume a hidden tab will support the campaign.

### Publication attribution and integrations

Add `fediverse:creator` to an article and authorize its publication domain in the linked account's settings to produce a creator byline (official, Profile, 2026-04). Open Graph supplies card data (official, PreviewCard, 2026-06). Preview the actual article link; don't promise a particular card from metadata alone (directional).

Mastodon 4.6 added `missing_attribution` for a card claiming current-user attribution from a domain missing from `attribution_domains` (official, Developer release, 2026-06). If it appears, check domain authorization before treating the byline as working.

For an integration, inspect `api_versions.mastodon` rather than assuming support. Mastodon 4.6 uses API version 10 and adds Collections endpoints plus GET/PATCH `/api/v1/profile`, including raw profile data, attribution domains, image descriptions, and tab preferences (official, Developer release, 2026-06). Read access is sufficient for preparation; writing the profile is a separate publishing action.

Activity Intents advertise templates for follow, reply, boost, and favourite actions so compatible tools can route users through their own server (official, Developer release, 2026-06). Test a compatible interaction path rather than assuming a visitor is signed in on the post's host (directional).

### Owned servers and community resources

Collections permit up to 25 opted-in discoverable profiles, notify additions, permit self-removal, and omit follow-all. Their shareable URLs appear under Featured; discovery is manual and primarily word of mouth (official, Release, 2026-06). Curate around a reader need and share the URL explicitly. Don't sell placement as guaranteed followers (directional).

Anonymous visitors can subscribe to public posts by email only when the server enables the feature and the account role has permission (official, Release, 2026-06). Inspect availability before offering this as a subscription CTA. The institutional landing-page option emphasizes the server description and recent local-profile updates rather than opening on Trending (official, Release, 2026-06). Review that public front door when planning an institutional account's output.

Brand a new owned server around the organization or community. Trademark guidance restricts Mastodon and confusingly similar terms such as masto or mstdn in top- or second-level domains; the exception for servers established before May 13, 2026 requires a non-affiliation disclaimer (official, Trademark guidance, 2026-08). Consult the full guidance for naming instead of inferring permission from existing server names.

The new operated-server terms took effect August 31, 2026 for mastodon.social and mastodon.online only (official, Server terms, 2026-07). Their standards require generative-AI disclosure and prohibit primarily or exclusively AI-generated accounts; they don't prescribe CWs as an AI label (official, Community Standards, 2026-02). Keep commercial permission and required disclosure in the publishing record. Independent servers require their own policy check.

### Changes to monitor

Quote display arrived in Mastodon 4.4; authoring and approval controls arrived in 4.5. Anyone is the documented default, with followers or Just me restrictions and later revocation available (official, Quote posts, 2025-11). Describe the supported permission, not an assumed community adoption rate.

Messages separation and changes to followed-hashtag navigation are part of the Mastodon 5.0 development preview. Enabled local and federated feeds are retained in that preview (official, Foundation preview, 2026-08). Don't treat it as a shipped UI contract. Recheck search aggregation and recommendation features when they ship; don't invent current FASP, Fediscovery, or For you behavior from announcements alone.

## References

- [Posting](https://docs.joinmastodon.org/user/posting/), 2026-07, verified media-description and Quiet public behavior; live-check guide for optional formats, no additional fixed caps asserted here.
- [Profile](https://docs.joinmastodon.org/user/profile/), 2026-04.
- [Discoverability](https://docs.joinmastodon.org/user/discoverability/), 2024-10.
- [Release](https://blog.joinmastodon.org/2026/06/mastodon-4.6/), 2026-06.
- [Developer release](https://blog.joinmastodon.org/2026/06/mastodon-4-6-for-devs/), 2026-06.
- [PreviewCard](https://docs.joinmastodon.org/entities/PreviewCard/), 2026-06.
- [Trademark guidance](https://blog.joinmastodon.org/2026/08/sharing-guidelines-about-mastodons-trade-mark-policy/), 2026-08.
- [Server terms](https://blog.joinmastodon.org/2026/07/announcing-new-terms-of-service-for-our-servers/), 2026-07.
- [Community Standards](https://help.joinmastodon.org/article/12-community-standards), 2026-02.
- [Quote posts](https://docs.joinmastodon.org/user/quote-posts/), 2025-11.
- [Foundation preview](https://blog.joinmastodon.org/2026/08/5.0-laying-the-foundation/), 2026-08.

Re-validate when the connected server upgrades, limits or policies change, profile/card behavior changes, or previewed discovery and messaging features ship.
Validated: 2026-09
