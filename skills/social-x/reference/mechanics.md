## Scope and snapshot

Open this reference when a draft, launch plan, or reach diagnosis depends on X ranking, labels, tiers, or format availability. Use the supplied evidence snapshot dated August 12–13, 2026, with the corrections validated in September 2026 (official, X algorithm sources below, 2026-08). The `main` URLs are mutable; a dated evidence snapshot isn't an archived deployment or proof of live serving behavior. The spam-flow source below has a commit pin. Recheck changed code before carrying forward parameters.

## Ranking and discovery

For You sources followed-account posts through Thunder and out-of-network candidates through Phoenix retrieval and SimClusters. Visibility filtering is separate from scoring and may allow, interstitial, or drop a candidate (official, X README, 2026-08). Describe these as the published pipeline, not a complete specification of all X feeds.

| Published default | Supported reading |
|---|---|
| Predicted reply and quote: 5.0; favorite: 0.5; profile click: 0.0 | These multiply predictions, not raw counts; a profile visit can still have business value (official, X parameters, 2026-08) |
| Copy-link share: 20.0; DM share: 5.0; follow: 4.0 | Forwardability is worth considering as craft; no post shape is proven best by these weights (official, X parameters, 2026-08) |
| Binary dwell: 0.05; continuous dwell: 0.004; not-dwelled: -0.02 | No supported second-based non-dwell threshold or audience-wide damage rule (official, X parameters, 2026-08) |
| Repeated-author decay: 0.5; floor: 0.25 | Applies within a feed request; no safe daily count or spacing interval follows (official, X parameters, 2026-08) |
| Video-quality-view duration floor: 10,000 ms; VQV weight: 0.0 | Don't lengthen a clip to buy a purported scoring advantage (official, X parameters, 2026-08) |
| Quoted VQV weight: 0.0; quoted duration check disabled | Don't promise a quoted-video bonus (official, X parameters, 2026-08) |

The bidirectional-follow change log documents a +15 predicted-reply boost above the 5.0 base for eligible originals, totaling 20.0, following the July 24 adjustment (official, X bidirectional change log, 2026-07). This is separate from mutual-follow Jaccard hydration and the following-replied-users facepile, which are disabled in the published defaults (official, X parameters, 2026-08). Don't infer a connected-reply distribution guarantee or organize mutual follows to manipulate metrics.

The cold-start path can lift eligible originals from authors with at most 1,000 followers and posts below 1,000 impressions toward slots 15–16. It also checks corpus, freshness, position ratio, and impression eligibility and excludes replies and reposts (official, X cold-start, 2026-08). It doesn't establish a launch-quality score, guaranteed reach, or a reply growth multiplier. Preserve time for original evidence even with a small account (directional).

The documented AgeFilter excludes posts older than 48 hours, and OONRetweetReplyFilter removes out-of-network replies and reposts from this candidate path (official, X README, 2026-08). Don't infer that replies have no audience anywhere, that every viewer sees a post only once, or that later follow-up is useless.

Bookmark weighting is unresolved in this evidence. Record available saves as reader behavior without assigning a ranking weight. Don't interpret source-list absence as proof of a production non-signal. Topic consistency remains reader-facing editorial advice (directional); no verified niche-lock duration, embedding reset, sequence-history count, or topic-name placement guarantee belongs in a writing plan.

## Classifiers and enforcement

The Banger schema contains `tweet_bool_metadata`, `slop_score`, and `has_minor_score`; the cited schema doesn't establish a numeric quality cutoff, automatic extra candidate pool, or direct slop penalty (official, X Banger schema, 2026-08). Don't diagnose suppression from prose style.

`SpamEapiLowFollowerClassifier` appears in the pinned spam-comment flow. The source doesn't establish universal small-account routing, large-account exemption, or an account-embedding reset (official, X spam flow, 2026-05).

PTOS enumerates 10 categories (official, X PTOS state, 2026-08):

- HateOrAbuse
- ViolentSpeech
- ChildSafety
- IllegalAndRegulatedBehaviors
- Spam
- SuicideOrSelfHarm
- AdultContent
- ViolentMedia
- TerrorismOrViolentExtremism
- CivicIntegrity

Don't claim these were all newly added or that each category hit removes a post. Enforcement outcomes come from the separate README visibility description (official, X README, 2026-08). For review, identify the actual policy concern, inspect the source material, and retain enough context to distinguish reporting or criticism from endorsement. If policy compliance remains unresolved, withhold the affected material.

The cited brand-safety file establishes verdict mappings, including `MediumRisk`, without proving organic reach loss (official, X brand safety, 2026-08). Don't equate ad adjacency with feed eligibility. Check visible notices and, if available, the Under the Hood aggregate-label pilot at `https://x.com/i/under_the_hood` (official, X README, 2026-08). No notification doesn't prove absence of a label.

X describes expanded EU “Made with AI” indicators separately from restricted-reach labels (official, X Media Literacy, 2026-07). Authenticity policy allows non-deceptive manipulated media but includes reach restrictions among possible responses to violations (official, X Authenticity, 2025-04). Keep provenance; don't promise either blanket suppression or immunity for labeled synthetic media.

## Format and monetization boundaries

The ordinary text limit is 280 characters. App help permits mixed photos, GIFs, and video up to 4 total media items; inspect the target client's combination and layout (official, X posting help, reviewed 2026-09-05). Premium help supports longer posts up to 25,000 characters, while posting-help mobile instructions still mention 4,000 (official, X Premium and X posting help, reviewed 2026-09-05). Verify the actual composer rather than assuming parity. A cap isn't a target length.

The evidence supplied for this playbook doesn't settle the following. Resolve them in the intended account before making a publishing promise:

| Unsettled detail | Action |
|---|---|
| Video duration and upload size by tier/client | Inspect the actual upload control and matching help; record the accepted asset specifications |
| Article tier, length, and publishing controls | Check the live editor; prepare an external-document fallback if unavailable |
| Spaces hosting, recording, and access | Confirm host permissions and availability before announcing a live session |
| Communities, polls, Lists, and DMs | Inspect the current surface and permission controls; follow the visible participation rules |
| Target-client mixed-media support and rendering | App help documents mixed media; preview the selected combination and don't assume a swipe carousel |
| Organic hashtags versus ad restrictions | Use a relevant tag only as an editorial choice; no universal organic ban is established |
| Video-tab placement or Community Notes reach effect | Don't promise distribution or infer enforcement; review actual notices and evidence |
| Premium reply-priority magnitude | Don't quote a lift or infer subscription from appearance alone |

Creator Revenue Sharing closed enrollment on August 7, 2026; its retirement is scheduled for September 7, with Original Content Rewards applications beginning rollout for existing members on September 8 (official, X creator monetization help, 2026-08). As of September 5, those latter events are upcoming. Direct eligible creators to check Creator Studio after rollout; don't budget revenue from old Premium-engagement rules.

## References

- [X README](https://github.com/xai-org/x-algorithm/blob/main/README.md), August 13, 2026.
- [Production parameters](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs), August 12, 2026; corrected values validated September 2026.
- [Cold-start scorer](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/author_cold_start.rs), August 13, 2026.
- [Bidirectional boost change](https://github.com/xai-org/x-algorithm/blob/main/docs/BIDIRECTIONAL_BOOST_CHANGE.md), July 24, 2026.
- [Banger schema](https://github.com/xai-org/x-algorithm/blob/main/grox/flows/upa/state_initial_banger.py), [PTOS state](https://github.com/xai-org/x-algorithm/blob/main/grox/flows/ptos/state.py), [brand safety](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/models/brand_safety.rs), August 13, 2026.
- [Spam flow, pinned commit](https://github.com/xai-org/x-algorithm/blob/e414c171ed68266341193330bc4864bf3f3534e3/grox/tasks/task_spam_detection.py), May 15, 2026.
- [X posting help](https://help.x.com/en/using-x/how-to-post), [Premium](https://help.x.com/en/using-x/x-premium), undated, reviewed September 2026.
- [Media Literacy](https://help.x.com/en/rules-and-policies/media-literacy-plan), July 2026; [Authenticity](https://help.x.com/en/rules-and-policies/authenticity), April 2025.
- [Creator monetization transition](https://help.x.com/en/using-x/creator-revenue-sharing), August 7, 2026.

Re-validate when:
- Algorithm commits or runtime defaults change.
- Feature names, subscription tiers, policies, or monetization programs change.
- New vendor reports motivate a different distribution claim.

Validated: 2026-09
