## Verified mechanics and publishing checks

Use these checks when the draft depends on a feature. Keep a recorded composer preview with the publishing package; a client check establishes what that client accepts, not an undocumented platform-wide rule (directional).

### Media and thread preparation

| Feature | Verified boundary | Preparation (directional) |
|---|---|---|
| Text | 300 grapheme clusters (official, Post lexicon, 2026-09) | Check the final composer counter after handles and URLs are inserted. The reviewed claim doesn't establish URL shortening or destination-URI counting behavior. |
| Photos | Up to 10; carousel from 5 photos (official, Photos release, 2026-06) | Put the identifying image first; confirm crop, sequence, and mobile legibility. Don't extrapolate a different layout below the carousel threshold. |
| Video | Up to 10 minutes and 300 MB (official, Video release, 2026-08) | Record the real workflow, retain necessary setup conditions, and supply accurate captions. Don't lengthen a demonstration to fill the limit. |
| Alt text | No current numeric cap established by the reviewed evidence | Describe visible evidence and relevant image text. Don't put overflow prose, unrelated jokes, keywords, or sensitive metadata here. Inspect the field and preview. |
| GIF and mixed embeds | No exhaustive combination matrix established by the reviewed evidence | Use a GIF only when a silent loop communicates the task. Preview quote/media/link combinations; don't promise simultaneous embeds or universal exclusivity. |
| Thread numbering | Introduced as beta; the later release removes its gate (official, Thread numbering, 2026-08; App releases, 2026-09) | Inspect the native thread composer, numbering, and published order. Don't infer that numbering is enabled by default or repeat it manually. |
| Scheduled thread | Buffer documents scheduling complete Bluesky threads in order and platform-specific customization (official, Buffer scheduling, 2026-07) | If using that tool, review the full thread and arrange human reply coverage. Scheduling doesn't supply the author's experience. |

For long evidence, use a destination the reader can inspect. Bluesky's partnership names community-built Offprint, Leaflet, and pckt.blog (official, Summer of Standard.site, 2026-06). Don't describe them as a built-in Bluesky editor or promise enhanced-card behavior without a preview.

### Account and conversation checks

Bluesky introduced group chats and subsequently added replies to specific messages in both group chats and DMs (official, Group chats and Message replies, 2026-06). Use the relevant message as context for requested support. Obtain an invitation before taking a public exchange into chat; don't assume every recipient accepts unsolicited DMs or expose private conversation in public proof (directional).

Check regional eligibility when addressing younger audiences: Bluesky restricted certain content and features for Texas users under 18 (official, Age assurance update, 2026-07). The reviewed statement doesn't identify every affected feature. Provide a destination that the intended audience can access (directional).

An account can request exclusion from algorithmic recommendations through `app.bsky.actor.contentVisibilityDeclaration`; strangers' Discover respects it, while topic- or list-based feeds needn't do so (official, Visibility declaration, 2026-09). Record the account owner's discovery preference; don't silently change it for a campaign.

Followers can hide an individual followed account's reposts in feeds (official, Repost controls, 2026-08). Don't equate a repost with delivery to every follower. Starter-pack reference-list opt-out UI is included in the release (official, App releases, 2026-09). Respect exclusion choices rather than promising pack placement.

The reviewed evidence doesn't establish current options or scopes for the controls below. Inspect the current UI before making the publishing package depend on them. These are operational checks, not feature guarantees (directional).

| Check | Decision to document (directional) |
|---|---|
| Reply settings or threadgates | Intended reply audience; actual available setting; accessible route for excluded readers needing support |
| Quote disable, detach, and hide-reply controls | Whether each control is available and what the UI says it affects; don't infer deletion of other people's content |
| Lists and mute lists | Whether a list is for reading, moderation, or public curation; don't treat moderation choices as acquisition tactics |
| Verification badge, trusted verifier, custom-domain handle | Inspect the displayed identity information and linked official site; don't promise a badge, infer paid endorsement, or claim a ranking advantage |
| Live-status link | Availability, supported destination, and actual live session; prepare an ordinary post with the working link if status linking isn't available |
| Profile and pinned post | Clear identity, useful current destination, and accurate product availability; don't claim pinning causes starter-pack inclusion |
| Post self-label picker | Applicable warning and actual available values; never invent an AI option or claim inline wording prevents labeling |

### Search and feed inspection

Shareable search filters cover keywords, people, date range, and language (official, Search rollout, 2026-07). The app's search migration completed in the release (official, Search migration, 2026-07). Copy the share URL from the actual filtered result. Those announcements don't establish a replacement API endpoint or sort-mode contract.

Official Search Tips document phrase matches in image alt text. Treat it as public searchable content; keep it useful for understanding the image, without inserting keywords for distribution or information absent from the redacted asset (official, Search Tips, 2024-05; editorial application).

Find custom feeds through the navigation available in the current app and record their URLs and descriptions. Inspect whether a feed uses a topic, list, or another stated criterion; observed inclusion doesn't prove a causal ranking factor (directional). Don't hardcode a Discover generator route from an unsupported citation. Check whether Trending topics or Explore is present; record availability and the destination reached, without asserting a default roster (directional).

### Disclosure and moderation

Bluesky documents automated sensitive-media labels and hide/warn/show controls (official, Transparency report, 2026-01). This doesn't establish an AI-writing detector or a universal AI-content self-label. Keep an inline media-origin disclosure distinct from a selected content-warning control; neither is a visibility guarantee (directional).

Disclose commercial relationships and avoid disruptive repetition or manipulated social signals (official, Community Guidelines, 2025-09). Don't transfer another network's synthetic-media policy to Bluesky. Check the current applicable policy if the work depends on a specific disclosure requirement.

## References

- [Search Tips](https://bsky.social/about/blog/05-31-2024-search), 2024-05-31; reviewed 2026-09-05.

- [Post lexicon](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/post.json), undated; reviewed 2026-09.
- [Photos release](https://bsky.app/profile/bsky.app/post/3mnslrkd6ok2g), 2026-06-08.
- [Video release](https://bsky.app/profile/bsky.app/post/3mtwf7gxkwc2r), 2026-08-25.
- [Thread numbering](https://bsky.app/profile/bsky.app/post/3msqpusnigc2t), 2026-08-10; [App releases](https://github.com/bluesky-social/social-app/releases), 2026-09-03.
- [Buffer scheduling](https://buffer.com/resources/schedule-to-bluesky/), 2026-07-24.
- [Summer of Standard.site](https://bsky.social/about/blog/06-22-2026-summer-of-standard-site), 2026-06-22.
- [Group chats](https://bsky.app/profile/bsky.app/post/3mnzmprxpe22y), 2026-06-11; [Message replies](https://bsky.app/profile/bsky.app/post/3mojb23vtt22c), 2026-06-17.
- [Age assurance update](https://bsky.social/about/blog/09-10-2025-age-assurance-approach), updated 2026-07-08.
- [Visibility declaration](https://bsky.network/blog/content-visibility-declaration/), 2026-09-01.
- [Repost controls](https://bsky.app/profile/bsky.app/post/3msqpuobiwk2t), 2026-08-10.
- [Search rollout](https://bsky.app/profile/bsky.app/post/3mqafridzgk2e), 2026-07-09; [Search migration](https://github.com/bluesky-social/social-app/releases/tag/1.128.0), 2026-07-16.
- [Transparency report](https://bsky.social/about/blog/01-29-2026-transparency-report-2025), 2026-01-29.
- [Community Guidelines](https://bsky.social/about/support/community-guidelines), 2025-09-19.

Re-validate when: media lexicons change; composer or conversation controls change; search navigation changes; eligibility or labeling policies change.

Validated: 2026-09
