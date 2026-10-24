---
name: video-thumbnails
title: "YouTube Thumbnail Maker: Shorts, Reels, and TikTok Covers"
description: "YouTube thumbnail maker workflow for marketing and creator videos: one clear promise per thumbnail, candidate frames pulled from the footage, cut-out faces and products, AI-generated backgrounds without baked-in text, 2-5 words of outlined text fitted and set by a libass renderer, feed-size previews with the duration badge, and three Test & Compare variants that change one variable. Covers 2026 specs for YouTube long-form and Shorts, TikTok and Reels covers with the 3:4 grid crop, and thumbnail policy. Use whenever a video needs a thumbnail, a cover image, or thumbnail A/B test variants."
license: Apache-2.0
compatibility: "Requires: python3 and an ffmpeg built with libass (macOS: Homebrew ffmpeg-full). Optional: uvx for rembg subject cut-outs. macOS/Linux."
capabilities: shell thumbnails
domains: video
rules:
  - session(thumbnail)
  - session(editor)
  - session(clips)
  - content(thumbnail)
  - content(thumbnails)
  - match(\b(cover|thumb)\s+(image|frame|art)\b)
  - match(\btest\s*(&|and)\s*compare\b)
  - semantic(make a youtube thumbnail for this video)
  - semantic(design three thumbnail variants to a/b test)
  - semantic(pick a cover frame for my reel)
---

## Overview

The thumbnail and the title are the whole pitch before anyone presses play. This skill is the video domain's thumbnail pipeline: decide the promise, get the best possible picture of it from the footage or a generated scene, put a real cut-out face or product on it, set two to five words of type with a renderer that measures and fits them, and check the result at the size people actually see it. It replaces drawing text onto frames with PIL or asking an image model to spell the headline, which give soft, misspelled, badly placed text.

## Mental model

A thumbnail does one job: make one promise the video keeps, readable in under a second at about 360 px wide on a phone or 168 px in a sidebar.

- The picture carries the emotion or the stakes: a face, a result, a before/after, the product in use.
- The text adds what the title doesn't say. It never repeats the title.
- Contrast, size, and placement decide whether it survives the feed; detail does not survive.

The renderer is the `video-thumbnail` command, installed on PATH with the `thumbnails` capability (the same file is the bundled `scripts/thumbnail.py`, listed under Skill Resources). It needs python3 and an ffmpeg with libass, which it finds on its own, including Homebrew's keg-only `ffmpeg-full`. Fonts come with the capability in `~/.local/share/octomind/fonts`. `video-thumbnail render --help` lists every option.

## Rules

### Specs (checked 2026-10)

| Surface | Size to render | Notes |
|---|---|---|
| YouTube long-form | `--format youtube` (1920x1080, under 2 MB) or `youtube-4k` (3840x2160) | 16:9, minimum 640 px wide, JPG or PNG. Desktop upload takes up to 50 MB, mobile 2 MB. Custom thumbnails need a verified channel |
| YouTube Shorts | `--format shorts` (1080x1920) | Custom Shorts thumbnails rolled out 2026-07-24 to Partner Program channels, desktop Studio only; elsewhere pick a frame |
| Vertical video with a 16:9 thumbnail | Keep the subject centered | YouTube auto-crops a 4:5 version for Home, Explore, Subscriptions |
| TikTok cover | `--format tiktok` (1080x1920) | Picked from a frame or uploaded in the app; the profile grid crops the center to about 3:4. Assume API posts can't set an uploaded cover |
| Instagram Reels cover | `--format reels` (1080x1920) | Frame or uploaded image; the profile grid crops the center to 3:4 (since January 2025) |
| LinkedIn video | `--format linkedin` (1920x1080) | Desktop upload option; ads take JPG/PNG up to 2 MB at the video's aspect |
| Square / portrait feed | `--format square` / `portrait` | 1080x1080, 1080x1350 |

### What drives the click (descriptive studies, not proof of cause)

- Faces appear in 69% of 500 breakout thumbnails (80% of the top 50), usually filling about a third of the frame (vidIQ, 2026). A larger dataset (1of10, 2025) finds faces and no-faces perform about the same overall, with big differences by niche. Use a face when the person is the draw or the emotion is the story; use the result or the object when that is the promise.
- Readable emotion beats theatre: shocked faces are a small minority (5–11%); neutral, focused, and happy faces dominate.
- Text: 72% carry text, median 5 words, and "no text" is the single most common bucket. Default to 0–4 words. The renderer warns above 5 (6 for vertical covers).
- High contrast shows up in more than half of breakout thumbnails. One focal subject, one accent color.
- YouTube's own guidance: an easy-to-read font, rule of thirds, a relatable emotion, title and thumbnail working together, and shooting dedicated thumbnail photos during the shoot.
- Keep text and faces out of the bottom-right corner (duration badge) and the bottom strip (progress bar). The renderer's layouts already do; it warns when text reaches there.

### Pipeline

1. Promise. Write the one-line promise and the title first. The thumbnail shows the payoff, stakes, or tension; the text adds one beat the title leaves out ("I quit" + title "Why I left Google after 8 years").
2. Background, in order of preference:
   - A real frame. `video-thumbnail frames master.mp4 -o thumbs/frames --count 12` writes 12 lossless candidates with timestamps and `sheet.jpg`. Pick the sharpest, most expressive frame; ask the user to choose when you can't view images.
   - A dedicated thumbnail photo from the shoot.
   - A generated scene: `generate_image` with `aspectRatio` 16:9 or 9:16, `imageSize` 2K or 4K, and "no text, no letters" in the prompt. Pass real product photos or the person's photo as `inputImagePaths` to keep identity and packaging true. Never generate a real person's face from scratch.
3. Subject cut-out (optional, strong for faces and products): `uvx --python 3.12 --from "rembg[cpu,cli]==2.0.86" rembg i -m birefnet-portrait frame.png thumbs/subject.png` for people, `-m isnet-general-use` for products. The first run downloads the model, up to about 1 GB for BiRefNet. Check the edge on hair and fingers in the preview.
4. Render:

```bash
video-thumbnail render thumbs/frames/frame-07.png -o thumbs/a.jpg \
  --text "I quit my job" --highlight quit --subject thumbs/subject.png --stroke 12 \
  --layout left --title "Why I left Google after 8 years" --preview thumbs/a-preview.png
```

5. Check the preview (`--preview`): the image at 360 px and 168 px on dark and light UI with the duration badge drawn in. The text must read at 168 px. If your tools can't display images, rely on the warnings and tell the user which preview to check and that legibility is unverified.
6. Variants. Make three for YouTube Test & Compare, each changing one variable: face vs object, text vs no text, or framing. Name them `a.jpg`, `b.jpg`, `c.jpg`.

### Renderer choices

| Choice | Options | Use |
|---|---|---|
| `--style` | `bold` (caps, black outline, accent word), `box` (rounded text boxes), `clean` (sentence case on a darkened side) | Creator and entertainment / explainers and news / B2B and premium |
| `--layout` | `left`, `right`, `top`, `bottom`, `center` | Text side; a `--subject` goes opposite (bottom-center for top/vertical) |
| `--highlight WORD` | Repeatable | One accent word, usually the verb or the number |
| `--font` | Poppins Black, Poppins ExtraBold, Anton, Archivo Black, Bebas Neue, or a brand font via `--fontsdir` | Keep one family per channel |
| `--darken`, `--grade` | Gradient strength 0–1; `pop` or `none` | Raise `--darken` if the contrast warning fires |
| `--crop-x`, `--crop-y` | 0–1 | Shift the crop when the source aspect differs |

The renderer measures each candidate line with libass, picks the split that allows the largest type, avoids lines ending on "I", "the", or "my", and stacks lines on a cap/descender grid. Pass the text plainly; don't add line breaks.

### Policy

- YouTube removes thumbnails that mislead viewers about the content, are sexual, shock with violence or gore, use vulgar text, or impersonate. Borderline ones get age-restricted or removed; repeat violations can cost custom thumbnails for 30 days.
- Egregious clickbait (a promise the video doesn't keep, especially news and current events) is enforced with removals.
- AI-generated or AI-edited thumbnails need no synthetic-content label, but the misleading and impersonation rules still apply.
- Thumbnails on ads also fall under Google Ads clickbait rules: no "you won't believe", no fake shock, no fear of negative life events.
- Sponsored content: when the image itself endorses a product, the disclosure must be visual and on the image (FTC).

## Examples

### Example 1: text by the image model

❌ `generate_image` with the prompt "YouTube thumbnail, man shocked, big yellow text I QUIT MY JOB". The letters come out soft at feed size, the line split is arbitrary, and a variant with different text means a new image.

✅ Generate or pick the scene without text, cut out the face, and set "I quit" with `video-thumbnail render ... --highlight quit`. A text variant is one more command.

### Example 2: title repeated

❌ Title "How we cut churn in half", overlay "HOW WE CUT CHURN IN HALF". The renderer warns; the thumbnail adds nothing.

✅ Overlay "One email" over the dashboard showing the drop: the title says what, the thumbnail shows the surprising how.

### Example 3: Reels cover outside the grid crop

❌ Text placed at the very top of a 1080x1920 cover: the 3:4 profile grid cuts it off.

✅ `--format reels --layout top` keeps the text inside the centered 3:4 area; the preview shows both the full frame and the grid crop.

## Checklist

- [ ] One promise; overlay text adds to the title instead of repeating it; 0–5 words.
- [ ] Background from a real frame, a shoot photo, or a text-free generated scene; real faces and products not invented.
- [ ] Rendered with `video-thumbnail` at the platform format; no font, contrast, badge, or grid-crop warnings left unexplained.
- [ ] Preview checked at 168 px, or reported to the user as unchecked.
- [ ] Three single-variable variants for YouTube Test & Compare when the channel can use it.
- [ ] Nothing misleading, sexual, gory, or impersonating; sponsored images carry a visual disclosure.
- [ ] Files saved under `./video-out/<slug>/thumbs/` (variants, previews, the chosen frame, the cut-out).

## Composition / References

- `video-hooks` — the promise the thumbnail and the first three seconds share.
- `video-spec-sheet` — platform specs and safe zones for the video itself.
- `video-editing` — finding the strongest moments; the thumbnail frame often comes from the hook.
- [YouTube: add video thumbnails](https://support.google.com/youtube/answer/72431)
- [YouTube: Test & Compare](https://support.google.com/youtube/answer/13861714)
- [YouTube: thumbnail best practices](https://support.google.com/youtube/answer/12340300)
- [YouTube thumbnail policy](https://support.google.com/youtube/answer/9229980)
- [YouTube Studio custom thumbnail updates, 2026-07-24](https://blog.youtube/news-and-events/youtube-studio-custom-thumbnail-updates/)
- [vidIQ thumbnail study, 2026](https://vidiq.com/research/youtube-thumbnail-study/)
- [rembg](https://github.com/danielgatis/rembg)
