# muvon/video-thumbnail

video-thumbnail — the tap's thumbnail and cover renderer. It composes a background (an image, or one frame of a video), an optional cut-out subject with a sticker outline and soft shadow, a contrast gradient behind the text, and 2–5 words of overlay text. The text is set with libass: each candidate line is measured by rendering it, the line split that allows the largest type is chosen, and lines are placed on a cap/descender grid. Output is JPEG or PNG at the platform size, plus an optional preview at feed sizes on dark and light UI. Warnings flag too many words, text that repeats the title, the YouTube duration-badge corner, the 3:4 grid crop of vertical covers, low contrast, missing fonts, and oversized files. The installer links the `video-thumbnails` skill's bundled `scripts/thumbnail.py` onto PATH. Python 3.9+, standard library only; needs an ffmpeg with libass (it finds Homebrew's keg-only `ffmpeg-full` on its own).

## Key Commands

| Command | Description |
|---------|-------------|
| `video-thumbnail frames talk.mp4 -o thumbs/frames --count 12` | Export 12 candidate stills (PNG, with timestamps) and a contact sheet |
| `video-thumbnail render thumbs/frames/frame-04.png -o thumb.jpg --text "I quit my job" --highlight quit` | Bold YouTube thumbnail (1920x1080), text left |
| `video-thumbnail render bg.png -o thumb.jpg --text "..." --subject me-cutout.png --stroke 12 --layout left` | Cut-out subject on the right with a white outline |
| `video-thumbnail render bg.png -o thumb.jpg --style box --layout right --text "..."` | Text on rounded boxes (news / explainer look) |
| `video-thumbnail render frame.png -o cover.jpg --format reels --layout top --text "..."` | 1080x1920 cover, text inside the 3:4 grid crop |
| `video-thumbnail render ... --title "Video title" --preview thumb-preview.png` | Flag title repetition and write a feed-size preview |
| `video-thumbnail render --help` | All options: formats, layouts, styles, colors, fonts |

## Common Usage

```bash
video-thumbnail frames work/master.mp4 -o thumbs/frames --count 12
video-thumbnail render thumbs/frames/frame-07.png -o thumbs/a.jpg \
  --text "We fired our agency" --highlight fired --layout left \
  --title "How we doubled leads without an agency" --preview thumbs/a-preview.png
```

Formats: `youtube` (1920x1080, ≤ 2 MB), `youtube-4k` (3840x2160), `hd`/`linkedin`/`x` (1920x1080), `vertical`/`shorts`/`reels`/`tiktok` (1080x1920), `portrait` (1080x1350), `square` (1080x1080). Styles: `bold` (caps, black outline, accent highlight), `box` (rounded text boxes), `clean` (sentence case on a darkened side).

## Links

- [Homepage](https://github.com/muvon/octomind-tap)
- [YouTube custom thumbnails](https://support.google.com/youtube/answer/72431)
- [ffmpeg ass filter](https://ffmpeg.org/ffmpeg-filters.html#ass)
