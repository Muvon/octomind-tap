# typst/typst

Typst is a modern typesetting engine: Markdown-like markup in, precise PDF out, in milliseconds and without a LaTeX distribution. In this tap it is pandoc's PDF engine (`--pdf-engine=typst`) for proposals, reports, and cover letters, and it compiles `.typ` templates directly. RenderCV bundles its own Typst binding, so resumes don't depend on this binary. The installer uses Homebrew on macOS and a pinned, checksummed static release on Linux.

## Key Commands

| Command | Description |
|---------|-------------|
| `typst compile doc.typ doc.pdf` | Compile a Typst document |
| `typst fonts` | List the fonts Typst can see (system fonts plus `--font-path`) |
| `typst compile --font-path ./fonts doc.typ` | Use fonts from a folder |
| `typst watch doc.typ` | Recompile on every save |

## Common Usage

```bash
pandoc proposal.md -o proposal.pdf --pdf-engine=typst -V mainfont="Source Serif 4" -V fontsize=11pt
typst fonts | grep -i "source serif"   # confirm the font exists before relying on it
```

## Links

- [Typst documentation](https://typst.app/docs/)
- [Typst releases](https://github.com/typst/typst/releases)
