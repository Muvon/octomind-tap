# muvon/ui-fonts

Interface fonts for rendered cards and previews: Inter (sans, variable weight 100–900) and JetBrains Mono (mono, variable weight 100–800), both SIL Open Font License. The installer downloads them from a pinned [google/fonts](https://github.com/google/fonts) commit, checks each file's SHA-256, and puts them in `~/.local/share/octomind/fonts` as `Inter.ttf` and `JetBrainsMono.ttf` (override the directory with `OCTOMIND_FONTS_DIR`). The `social-preview` renderer always searches that directory and ignores system fonts, so a card renders the same on every machine.

## Key Commands

| Command | Description |
|---------|-------------|
| `typst fonts --ignore-system-fonts --font-path ~/.local/share/octomind/fonts` | List the families a renderer will see |
| `social-preview ... --font "Inter" --mono "JetBrains Mono"` | The defaults the card renderer uses |

## Common Usage

```bash
social-preview -o card.png --name acme --tagline "Two-way sync for Postgres and spreadsheets" --accent "#0969da"
```

## Links

- [Inter](https://rsms.me/inter/)
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
- [google/fonts](https://github.com/google/fonts)
