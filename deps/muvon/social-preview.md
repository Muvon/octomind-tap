# muvon/social-preview

social-preview — the tap's GitHub social preview renderer. It lays out a 1280x640 card from the repository's own brand: the project name as a wordmark, an open-source badge, a tagline fitted to two lines, an optional subline, install command in a terminal pane, footer URL, and the logo on the right. Colors not given are derived from the accent and background. Typst renders it with system fonts ignored, so the same inputs give the same PNG on every machine; fonts come from `~/.local/share/octomind/fonts` (Inter and JetBrains Mono via `muvon/ui-fonts`) plus any `--font-path` you add, such as the repository's bundled brand fonts. Warnings flag low contrast, long text, and stars, versions, or percentages that go stale. It fails on an unknown font family, a wrong output size, or a file over GitHub's 1 MB limit. The installer links the `repo-social-preview` skill's bundled `scripts/social_preview.py` onto PATH. Python 3.9+, standard library only; needs typst.

## Key Commands

| Command | Description |
|---------|-------------|
| `social-preview -o card.png --name acme --tagline "..." --accent "#0969da"` | Minimal card: wordmark, tagline, brand accent on near-black |
| `social-preview ... --logo assets/logo.svg --badge "Open source · Go · MIT"` | Logo on the right, open-source badge under the wordmark |
| `social-preview ... --install "brew install acme/tap/acme" --url github.com/acme/acme` | Install pane and footer URL |
| `social-preview ... --bg "#ffffff" --fg "#1f2328"` | Light card; the terminal pane stays dark |
| `social-preview ... --font "Brand Sans" --font-path ./fonts` | Brand fonts from the repository |
| `social-preview ... --preview card-preview.png` | Also write a 480 px feed-size copy to judge legibility |
| `social-preview --help` | All options |

## Common Usage

```bash
social-preview -o .github/social-preview.png --preview /tmp/card-preview.png \
  --name acme --tagline "Two-way sync between Postgres and spreadsheets" \
  --subline "One binary · Any database · No glue code" --badge "Open source · Go · MIT" \
  --install "go install github.com/acme/acme@latest" --url github.com/acme/acme \
  --logo assets/logo.svg --accent "#0969da"
```

## Links

- [Homepage](https://github.com/muvon/octomind-tap)
- [GitHub: customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [Typst](https://typst.app)
