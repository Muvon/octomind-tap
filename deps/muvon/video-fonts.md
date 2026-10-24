# muvon/video-fonts

Heavy display fonts for burned-in captions and video thumbnails: Poppins Black, Poppins ExtraBold, Anton, Bebas Neue, and Archivo Black, all SIL Open Font License. The installer downloads them from a pinned [google/fonts](https://github.com/google/fonts) commit, checks each file's SHA-256, and puts them in `~/.local/share/octomind/fonts` (override with `OCTOMIND_FONTS_DIR`). The `video-captions` and `video-thumbnail` renderers use that directory as libass `fontsdir` by default, so their styles render with the intended typeface instead of a fallback.

## Key Commands

| Command | Description |
|---------|-------------|
| `ls ~/.local/share/octomind/fonts` | List the installed font files |
| `video-thumbnail render bg.jpg -o thumb.jpg --text "..." --font "Anton"` | Use another installed family by name |
| `video-captions vo.json --video cut.mp4 -o c.ass --font "Archivo Black" --burn out.mp4` | Captions in another family |
| `ffmpeg -i in.mp4 -vf "ass=c.ass:fontsdir=$HOME/.local/share/octomind/fonts" out.mp4` | Point a manual libass burn at the same fonts |

## Common Usage

```bash
# Families available by name: "Poppins Black", "Poppins ExtraBold", "Anton", "Bebas Neue", "Archivo Black"
video-thumbnail render frame.png -o thumb.jpg --text "I quit my job" --font "Anton" --highlight quit
```

Add a brand font by copying its `.ttf`/`.otf` into the same directory and passing its family name with `--font`.

## Links

- [Google Fonts repository](https://github.com/google/fonts)
- [SIL Open Font License](https://openfontlicense.org)
