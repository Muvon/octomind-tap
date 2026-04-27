---
name: markup-landing-page
title: "Landing Page Craft — UI, Conversion, and System Patterns"
description: "Production playbook for building modern lightweight landing pages that sell. Covers automatic dark/light theming via CSS custom properties, system-font Apple-style typography, opinionated section anatomy (hero, features, comparison, pricing, FAQ, footer CTA), conversion-focused copy hierarchy, SEO/OG/JSON-LD baseline, and the structural patterns that move visitors to purchase. Activate whenever drafting, designing, or implementing a marketing or product landing page."
license: Apache-2.0
compatibility: "Stack-agnostic — examples use SvelteKit + plain CSS but rules apply to any HTML/CSS framework."
domains: design developer
rules:
  - content(landing page)
  - content(landing-page)
  - content(marketing site)
  - content(product page)
  - match(\blanding\s+page\b)
  - match(\bbuild.*landing\b)
  - match(\bdesign.*landing\b)
  - match(\bproduct\s+page\b)
  - match(\bmarketing\s+site\b)
  - match(\bhero\s+section\b)
  - match(\bpricing\s+page\b)
---

# Landing Page Craft

## Overview

A landing page has one job: turn a stranger into a buyer (or trial user). Everything else — logos, headers, badges, blog links — is decoration. This skill encodes the patterns that consistently convert: a tight design system that handles dark/light mode automatically, an opinionated section order that walks visitors through the buy decision, copy rules that avoid AI-generic language, and the SEO/structured-data baseline that gets the page found in the first place.

Pair with `content-voice` for copy. This skill handles *structure, design system, and conversion mechanics*. `content-voice` handles *how the words sound*.

---

## Tech Stack Baseline

Default to the lightest possible stack. Heavy frameworks slow time-to-interactive, hurt SEO, and add maintenance burden for what should be ~80% prerendered HTML.

**Recommended:**
- **SvelteKit + adapter-static** for prerendered SSR. Zero JS on most pages, full SEO, instant LCP.
- **Plain CSS with custom properties** — no Tailwind, no UI library. CSS custom properties + `prefers-color-scheme` give you theming for free.
- **System font stack** — `-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif`. Zero font load, native OS feel.
- **TypeScript** in `<script>` blocks.
- **Vite** for bundling.
- **Cloudflare Pages or Vercel** for hosting (static + edge functions).

**Avoid unless specifically needed:**
- React + Next.js for a marketing site (overkill, hydration cost)
- Tailwind for a single-domain landing (verbose class soup, design tokens scattered)
- Heavy animation libraries (GSAP, Framer Motion) for fade-ins (CSS does it in 4 lines)
- Web fonts (system fonts look better than 90% of imported fonts on Apple devices)
- Component libraries (Radix, shadcn) — landing pages need brand-specific UI, not generic primitives

---

## Design System (Single Source of Truth)

All design tokens live in one CSS file as custom properties on `:root`. Components read tokens via `var(--token)`. Hardcoded colors, spacing, or radii in components is a smell.

### Color tokens

```css
:root {
  /* Neutrals — Apple-style cold grays for premium feel */
  --gray-50: #fbfbfd;
  --gray-100: #f5f5f7;
  --gray-200: #e8e8ed;
  --gray-300: #d2d2d7;
  --gray-400: #aeaeb2;
  --gray-500: #86868b;
  --gray-600: #6e6e73;
  --gray-700: #48484a;
  --gray-800: #3a3a3c;
  --gray-900: #1d1d1f;

  /* Brand accent — pick ONE primary, use shades */
  --accent-50:  #eef2ff;
  --accent-100: #dbe4ff;
  --accent-200: #bfcfff;
  --accent-400: #6d8aff;
  --accent-500: #4a6cf7;  /* primary — buttons, links */
  --accent-600: #3451d1;  /* hover */

  /* Semantic — these are what components reference */
  --bg: var(--white);
  --bg-muted: var(--gray-100);
  --card-bg: var(--white);
  --text-primary: var(--gray-900);
  --text-secondary: var(--gray-600);
  --text-muted: var(--gray-500);
  --border: var(--gray-200);
  --border-light: var(--gray-100);
  --on-accent: #ffffff;  /* text on accent backgrounds — does NOT invert */
  --nav-bg: rgba(255, 255, 255, 0.72);

  /* Trust accent — green for privacy/security signals */
  --green-500: #30d158;
}
```

### Typography scale

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
               'SF Pro Text', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono: 'SF Mono', SFMono-Regular, ui-monospace, 'Cascadia Code', Menlo, monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 2rem;
  --text-4xl: 2.5rem;
}
```

### Spacing scale (8px base)

```css
:root {
  --space-1: 0.25rem;   --space-5: 1.25rem;
  --space-2: 0.5rem;    --space-6: 1.5rem;
  --space-3: 0.75rem;   --space-8: 2rem;
  --space-4: 1rem;      --space-10: 2.5rem;
                        --space-12: 3rem;
                        --space-16: 4rem;
                        --space-20: 5rem;
                        --space-24: 6rem;
}
```

### Effects

```css
:root {
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.08);

  --transition: 0.2s ease;
  --nav-height: 56px;
  --max-width: 1100px;
}
```

---

## Automatic Dark/Light Mode

This is non-negotiable for modern landing pages. Implement once at the token level — components shouldn't know which mode they're in.

```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #000000;
    --bg-muted: #0a0a0a;
    --card-bg: #111113;
    --text-primary: #f5f5f7;
    --text-secondary: #a1a1a6;
    --text-muted: #6e6e73;
    --border: #2a2a2e;
    --border-light: #1c1c1f;
    --nav-bg: rgba(0, 0, 0, 0.72);

    /* Brighten accent slightly for dark mode contrast */
    --accent-500: #6d8aff;

    /* Adjust shadows — heavier on dark */
    --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
    --shadow-lg: 0 12px 32px rgba(0,0,0,0.6);
  }
}
```

**Rules:**
- **Never hardcode colors** in components. Use `var(--token)`.
- **`--on-accent` does NOT invert** — text on a colored button stays white in both modes.
- **Test both modes**. Dark mode reveals contrast bugs that pass in light.
- **Add the meta tag** so the OS chrome matches:
  ```html
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)" />
  <meta name="color-scheme" content="light dark" />
  ```
- Component-specific cases (like a `rgba(0,0,0,0.4)` overlay) need explicit dark-mode overrides inside the component.

---

## Section Anatomy (Top to Bottom)

Order matters. The page is a sales conversation. Each section answers the next objection.

### 1. Nav (sticky, blur backdrop)

- Fixed top, height ~56px
- Logo + 1–3 links + 1 primary CTA pill (accent fill)
- `backdrop-filter: blur(20px)` + translucent background
- Border-bottom appears on scroll (subtle shadow change)
- Mobile: same layout, smaller paddings — don't add a hamburger unless > 5 items

### 2. Hero

The single most important section. Conversion is decided here.

- **Badge** above headline — context tag (e.g., "macOS 14+ · Apple Silicon"). Tiny, uppercase, muted.
- **Headline** — `clamp(2.5rem, 6vw, 3.5rem)`, weight 700, letter-spacing -0.035em, line-height 1.08. Two lines max with `<br>`. State the outcome, not the feature. "Talk to your computer, don't type." beats "AI-powered voice recognition for macOS."
- **Subtitle** — single sentence, max ~30 words, `--text-lg`, `--text-secondary`. Includes 2–3 specific features ("smart cleanup, live translation, meeting summaries").
- **Primary CTA** — pill button, accent fill, `--text-lg`, generous padding. Use action verbs. "Download Free" beats "Get Started." Concrete > abstract.
- **Trust line** under CTA — free trial limits ("100 free dictations · No credit card") in `--text-sm` muted.
- **Alt install** — `brew install ...` block in monospace if relevant.
- **System requirements** — last line, muted small text.

Vertical centering: `min-height: calc(100vh - var(--nav-height))`. Background: subtle radial gradient to accent-50 at top.

### 3. How It Works (3 steps)

Three cards, numbered 01/02/03. Headline + 1–2 sentence description per step. Each card: card-bg, 1px border, radius-lg, padding-8. Hover: `translateY(-2px)` + shadow-md.

### 4. Three Modes / Use Cases overview (if multi-feature product)

If the product has 3+ distinct modes/jobs (dictation + meetings + notes, etc.), establish them early as cards. Sets expectations for the rest of the page.

### 5. Feature deep-dives (alternating two-column blocks)

Each major feature gets its own section: text on one side, visual on the other. Alternate sides for rhythm. Each block:
- Section heading (`--text-4xl`, weight 700, letter-spacing -0.03em)
- 2–4 sentence paragraph
- 3-bullet list of specifics (with accent dot before each)
- Visual: real screenshot, demo card, or stylized illustration

### 6. Privacy / Trust section

If your product has any privacy/local/data angle, give it a section. People scroll for trust signals.

### 7. Pricing (vs subscription comparison)

Two cards minimum: yours (highlighted) and the alternative (cloud subscription). Show:
- Price (`--text-4xl`)
- Period ("once" vs "/month")
- Year-2 cost line (the kicker)
- Feature list with checkmarks (you) or X marks (them)
- "Best Value" badge on yours

### 8. Competitor Comparison Table

Feature-by-feature against named competitors. Your column highlighted with `--accent-50` background. Strikethroughs for promo prices. Cost-after-2-years row at bottom in heavier border. **This is often the highest-converting section** — visitors scroll specifically to compare.

### 9. Performance / Stats (if applicable)

One big number ("150x realtime"). Bar chart or simple visual showing you vs competition.

### 10. Compatibility (where it works)

Pill grid of supported apps/integrations. Reassures buyers that the tool fits their existing workflow.

### 11. About / Made by

Brief: "Built by [team] in [city]. Selectively shipped." Link to company. Builds trust without taking up space.

### 12. FAQ

8–12 questions. Use `<details>` element — zero JS, accessible, animates with CSS. Cover:
- "What is it?" (echo the headline differently)
- Privacy / data handling
- Platform / requirements
- Free trial details
- Pricing details
- Each major feature ("How does X work?")
- Common objections ("What if X doesn't work?")
- Refund / cancellation

### 13. Footer CTA

A repeat CTA section before the footer. Different headline from hero — emotional or summarizing ("Local. Fast. Yours."). Same CTA. Same trust line.

### 14. Footer

Brand + tagline on left, columns on right (Product, Company, Legal, Connect). Copyright at bottom. Keep it minimal — 3–4 columns max.

---

## CTA Hierarchy

A landing page should have **one primary action** and zero or one secondary action. Multiple CTAs of equal weight = no CTA.

**Hierarchy:**
1. **Primary CTA** — accent-filled pill, white text. Use for the conversion goal (Download, Buy, Sign up). Placed in: Nav, Hero, FooterCTA. Same label, same color.
2. **Secondary CTA** — outline pill (accent border + accent text, transparent fill). Use for alternate paths (Learn more, Buy after free trial). Different label.
3. **Tertiary** — text links with underline-on-hover. Used in nav, footer, inline copy.

**Rules:**
- Never two filled accent CTAs in the same viewport.
- Never use red, orange, or yellow for primary CTAs unless brand-justified — they read as warnings.
- CTA text is a **verb + outcome**: "Download Free", "Start Trial", "Buy Vext" — not "Click here", "Learn more", "Submit".
- Pill radius (`border-radius: 9999px`) outperforms rounded rectangles in tests for software products.

---

## Conversion Patterns

### Show price prominently

Hide the price = lose the sale. Visitors who can't see the price assume "expensive" or "you have to talk to sales." Even if pricing is complex, show a starting number.

### Compare against the alternative

People don't evaluate prices in isolation — they evaluate them against alternatives. Always include a comparison: subscription vs one-time, your-tool vs status-quo, you vs named competitors. Make the math visible (e.g., "$49 vs $200 over 2 years").

### Specific over abstract

"150x realtime" beats "blazingly fast." "$24.50 with VEXT50" beats "Save big." Numbers, named features, named competitors, named integrations. Every abstract claim should be replaced with something checkable.

### Trust signals layered throughout

Don't bunch all trust at the bottom. Sprinkle:
- System requirements badge in hero
- "No credit card" in trial copy
- Privacy section mid-page
- Real screenshots (not stock illustrations)
- Specific company name + jurisdiction in footer

### Free trial with explicit limits

"Free trial — 100 dictations, 50 notes, 10 meeting recordings — no credit card" outperforms "Try free." Numbers make the offer concrete.

### Urgency without manipulation

If you have a real launch promo or deadline, show it: pulsing dot pill, deadline date, original price strikethrough. **Never use fake countdowns or invented deadlines** — buyers detect them, and trust dies fast.

### Multiple CTAs, one ask

The CTA should appear in nav, hero, mid-page (after pricing), and footer. All point to the same action. Don't split between "Buy" and "Sign up free" and "Watch demo" — pick one primary outcome and repeat.

---

## Copy Rules (apply on top of `content-voice`)

### Headlines

- **State the outcome, not the feature.** "Talk to your computer, don't type." > "AI-powered voice recognition."
- **Two lines max** — use `<br>` to control wrapping. Mobile gets the same break.
- **Verb-driven** when possible. "Capture a thought before it's gone." > "Voice notes feature."
- **No marketing dead words** in headlines: "revolutionary", "next-generation", "ultimate", "powerful". Use the words your customer would use describing it to a friend.

### Subtitles / lead paragraphs

- One sentence. Two if you must.
- Includes 2–3 concrete features by name.
- Ends with a trust signal ("No cloud. No subscription.") or differentiator.

### Section headings

- Short. 1–4 words ideally. End with a period for tonal calm: "Voice notes." "How it works." "What you earn."
- Avoid "Discover", "Unlock", "Experience", "Explore" — dead AI vocabulary.

### Body copy

- Apply `content-voice` rules: contractions, dramatic rhythm, no dead words.
- Concrete examples > abstract claims.
- One idea per paragraph.
- Bullet lists only when you have 3+ parallel items. Otherwise use prose.

### CTAs

- 1–3 words. "Download Free", "Buy for $24.50", "Get started".
- Action + outcome. Never "Click here" or "Submit".
- Match what happens next. "Buy" → checkout. "Download Free" → trial. "Start" → signup. Don't bait.

---

## SEO + Social Baseline

Every page (not just the landing) must set:

```html
<title>Page Name — Brand</title>
<meta name="description" content="..." />  <!-- under 160 chars, unique per page -->
<link rel="canonical" href="https://domain.com/path" />

<meta property="og:type" content="website" />  <!-- or "article" for blog posts -->
<meta property="og:url" content="..." />
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://domain.com/og/page.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:site_name" content="Brand" />

<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="..." />
<meta name="twitter:description" content="..." />
<meta name="twitter:image" content="..." />
<meta name="twitter:site" content="@handle" />
```

### OG image generation

Generate per-page OG images at build time as 1200×630 SVG → PNG (use `@resvg/resvg-js` or similar).

- **PNG only** for `og:image` and `twitter:image` — Facebook, Slack, LinkedIn don't render SVG.
- **Brand-consistent**: dark background, accent gradient bar at top/bottom, logo top-left, headline center-left, domain footer.
- **Auto-wrap titles** with dynamic font sizing (drop from 80px → 64px → 52px as line count grows).
- **Generated files in .gitignore** — they're build artifacts, not source.

### JSON-LD structured data

For a software product landing page, include `SoftwareApplication`:

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "...",
  "description": "...",
  "url": "...",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "macOS 14+",
  "offers": {
    "@type": "Offer",
    "price": 49,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  },
  "publisher": { "@type": "Organization", "name": "...", "url": "..." }
}
```

Plus `Organization` and `FAQPage` (if you have a FAQ section).

**Never invent `aggregateRating`** with fake review counts — Google penalizes this. Only include if you have real reviews.

### Canonical and sitemap

- Every page sets `<link rel="canonical">`.
- Static `sitemap.xml` listing all routes with `lastmod` and reasonable `priority` (1.0 for home, 0.7 for content, 0.3 for legal).
- `robots.txt` allowing everything except `/api/*` and `/_*`.

---

## Error Pages (404, 5xx)

A non-existent route is a conversion opportunity, not a dead end. Most sites ship the framework's default 404 — generic, brand-broken, no recovery path. Don't.

### One component, all errors

Build a single `+error.svelte` (SvelteKit) / `error.tsx` (Next) / equivalent that handles every status code. Branch the headline and copy on `status`:

- **404** — "Lost in transcription." / "Page not found." Light, on-brand, slight humor if it fits the voice.
- **5xx** — "Something glitched on our end." Acknowledge the problem honestly. Don't blame the user.
- **Other (403, 401, etc.)** — fall back to the actual error message in a plain frame.

### Required elements

1. **Status badge** — small monospace pill ("Error 404"). Tells the user what category of problem it is without the page looking like a debug screen.
2. **Headline** — `clamp(2rem, 5vw, 2.75rem)`, on-brand, friendly. Avoid all-caps "OOPS!" or "PAGE NOT FOUND!".
3. **Blurb** — single sentence explaining what happened in human language. Never expose stack traces or server-side error messages to users.
4. **Two CTAs** — "Back home" (primary, accent-filled) + a secondary path ("Read the blog", "See pricing"). Same hierarchy as the rest of the site.
5. **Suggestions list** — 3–5 inline links to common destinations (Pricing, FAQ, Contact, etc.). Catches the "I was looking for X" case where Home isn't the right answer.
6. **Visual** — optional but recommended: a subtle brand element (animated icon, illustration). Reuses brand tokens so it doesn't break in dark mode.

### Tone rules

- **Be human, not corporate.** "We can't find that page" beats "The requested resource was not found."
- **Don't apologize excessively.** One sentence acknowledging is enough.
- **No "Click here to" instructions.** The CTAs are obvious.
- **No marketing copy.** Don't try to sell. Just help them find what they wanted.
- **Never blame the user.** "You typed the wrong URL" is hostile. "This page doesn't exist anymore" is neutral.

### Technical requirements

- **Title**: `<title>404 — Brand</title>` (use the actual status code).
- **Meta**: `<meta name="robots" content="noindex">` — error pages should never be indexed.
- **Same layout**: nav + footer present, identical to the rest of the site. Visitors should see continuity, not a stripped-down system page.
- **Dark/light mode**: error page uses the same CSS custom properties — zero special-case styling.
- **Reduced motion**: any animations gate on `@media (prefers-reduced-motion: reduce)`.
- **No third-party calls**: error pages must work even when APIs are down. No analytics that block render, no social embeds.

### Static fallback

For static sites (`adapter-static`, Next export, etc.), configure the adapter to emit `404.html` from your error component. Cloudflare Pages, Netlify, Vercel, and S3 will serve it automatically for unknown routes:

```js
// SvelteKit svelte.config.js
adapter: adapter({ fallback: '404.html' })
```

The `+error.svelte` component is what gets prerendered into `404.html` at build time.

### Don't do

- ❌ Render a stack trace or framework default error page in production
- ❌ Auto-redirect after a delay ("Redirecting in 5 seconds...") — disorienting and feels broken
- ❌ Show a search bar without a real search backend
- ❌ Use stock "lost robot" / "broken cable" illustrations — generic and dated
- ❌ Skip the nav and footer — the page should feel like part of the site
- ❌ Index error pages (missing `noindex` is a common SEO bug)

---

## Animation (Restrained)

Default to no animation. Add only when it serves communication.

### `.animate-on-scroll` pattern

```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  },
  { threshold: 0.1 }
);
document.querySelectorAll('.animate-on-scroll').forEach((el) => observer.observe(el));
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.animate-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}
```

**Rules:**
- Use sparingly — every section animating is annoying.
- Never animate content above the fold (hero is visible at load).
- Disable on `prefers-reduced-motion: reduce`:
  ```css
  @media (prefers-reduced-motion: reduce) {
    .animate-on-scroll { opacity: 1; transform: none; transition: none; }
  }
  ```

### Hover micro-interactions

- Buttons: `transform: translateY(-1px)` on hover, accent color shift.
- Cards: `translateY(-2px)` + shadow upgrade.
- Links: color shift only, no underline-fade gimmicks.

### Pulsing dots

For "live" indicators (recording, launch promo):
```css
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.4); }
}
.dot { animation: pulse 1.6s ease-in-out infinite; }
```

---

## Responsive Rules

Two breakpoints cover ~95% of cases:

```css
@media (max-width: 768px) { /* tablet */ }
@media (max-width: 640px) { /* mobile */ }
```

**Patterns:**
- 3-column grids → 1 column on mobile, max-width 480px centered
- 2-column feature blocks → stack on tablet, both full-width
- Hero clamp() handles headline sizing automatically — no manual mobile override needed
- Tap targets ≥ 44×44px on mobile
- Tables: `overflow-x: auto` wrapper with `min-width` on the table itself

---

## Performance Targets

A landing page that takes >1s to render loses customers regardless of copy quality.

- **LCP < 1.5s** — system fonts, prerendered HTML, images optimized
- **CLS < 0.1** — explicit width/height on images, no layout-shifting embeds
- **Total JS shipped** — under 50KB gzipped for a marketing-only landing
- **Image format** — WebP for photos, SVG for illustrations, PNG only for screenshots that need pixel accuracy
- **Hero image** — preload it: `<link rel="preload" as="image" href="...">`
- **Above-the-fold CSS** — inline critical CSS if your stack supports it

---

## Anti-Patterns (Don't)

- **Don't autoplay video** — it ships +500KB, distracts, and breaks on mobile
- **Don't use full-bleed background videos** — performance disaster
- **Don't gate the price** behind "Contact us" unless you genuinely sell enterprise
- **Don't add a "newsletter signup" modal** that interrupts reading
- **Don't use generic stock photos** of laptops/teams/handshakes — kills credibility
- **Don't put "Award winning" or trust-badge soup** in hero — empty signals
- **Don't bury the CTA** below 4 sections of content
- **Don't write copy that sounds like AI** — see `content-voice`
- **Don't scroll-jack** with libraries that hijack the wheel event
- **Don't hide nav on scroll** — visitors lose orientation
- **Don't ship cookie banners** unless you actually need them (most marketing sites don't if no third-party cookies)
- **Don't write "trusted by X companies"** without showing real logos and numbers — adds nothing

---

## Pre-Ship Checklist

Before declaring a landing page ready:

- [ ] Hero passes the 3-second test: someone landing here understands what it is and what to do
- [ ] Primary CTA visible without scrolling on a 13" laptop
- [ ] Dark mode tested — no contrast bugs
- [ ] Mobile tested at 375px and 414px
- [ ] All copy passes `content-voice` rules (no dead vocabulary)
- [ ] Every external link has `rel="noopener"` and `target="_blank"` if appropriate
- [ ] Every image has descriptive `alt`
- [ ] OG image renders in https://www.opengraph.xyz preview
- [ ] Lighthouse: Performance ≥ 95, SEO 100, Accessibility ≥ 95
- [ ] Tested on actual mobile device (not just DevTools)
- [ ] No console errors in production build
- [ ] Form submissions / CTAs actually work end-to-end
- [ ] 404 page exists and matches brand
- [ ] Sitemap.xml lists every page
- [ ] Canonical URL is set on every page
- [ ] At least one trust signal in hero, one mid-page, one footer

---

## Examples

### Hero — what works

❌ AI-generic:
> "Revolutionary AI-Powered Voice Recognition Software for Modern Professionals"

✅ Outcome-driven:
> "Talk to your computer, don't type."
> Subtitle: Voice to text with smart cleanup, live translation, meeting summaries. No cloud. No subscription. Your voice never leaves your Mac.

### Pricing — what works

❌ Hidden / vague:
> "Get a quote" or "Starting at $—"

✅ Concrete + comparison:
> Vext: **$49** once · $0 in year 2
> Cloud voice tools: **$10–30** /month · $120–360/year

### CTA — what works

❌ "Click here", "Submit", "Get started"

✅ "Download Free" (verb + outcome)
✅ "Buy for $24.50" (verb + price clarity)
✅ "Apply to join" (verb + commitment level)

### Comparison row — what works

❌ Generic feature names:
> "Cloud-dependent · Account required"

✅ Specific friction points:
> "Audio sent to third-party servers · Requires monthly subscription · Account + login required"

---

## When to Break the Rules

- **Premium price points (>$500)** — add more credibility (case studies, named customers, ROI calculator). Single-page may not be enough.
- **Enterprise B2B** — gate pricing behind a demo if your sales motion needs qualification.
- **High-emotion products** (luxury, lifestyle) — typography and imagery matter more than spec lists.
- **Developer tools** — code samples in hero, GitHub stars badge, technical spec sheet upfront.

The patterns above are calibrated for $20–200 indie/SaaS products sold to individuals or small teams. Adjust upward (more depth, more proof) for higher prices.
