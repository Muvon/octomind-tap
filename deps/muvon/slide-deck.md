# muvon/slide-deck

slide-deck — the tap's presentation renderer. It writes starter decks, lints Marp Markdown (assertion titles, words and bullets per slide, alt text, speaker notes), and exports PDF, HTML, PowerPoint, speaker notes, and PNG previews through a pinned Marp CLI with the bundled `octo` theme. After export it renders small PNGs and flags slides whose content runs into the bottom margin, where Marp silently clips overflowing text. The installer links the `slide-decks` skill's `scripts/deck.py` onto PATH and, when no Chrome, Edge, Chromium, or Firefox is installed, installs Playwright's Chromium for rendering (with its system libraries on Linux when it runs as root or with passwordless sudo). Python 3.9+ standard library plus Node.js.

## Key Commands

| Command | Description |
|---------|-------------|
| `slide-deck new deck-q3.md --title "Churn concentrates in month two"` | Starter deck: title, claim, stat, divider, and ask slides |
| `slide-deck lint deck-q3.md` | Per-slide issues; `--mode read` for send-ahead decks with more text |
| `slide-deck render deck-q3.md` | PDF with outlines, plus the overflow check |
| `slide-deck render deck-q3.md --html --pptx --notes --png` | Also HTML, PPTX (each slide an image), notes text, PNG per slide |
| `slide-deck render deck-q3.md --pptx-editable` | Experimental editable PPTX (needs LibreOffice; lower fidelity, no notes) |

## Common Usage

```bash
slide-deck new deck-board.md --title "Approve the EU launch for March"
# edit the Markdown: one claim per slide, notes in <!-- --> comments
slide-deck lint deck-board.md
slide-deck render deck-board.md --png --notes
```

Theme classes, per slide with `<!-- _class: name -->`: `lead` (title), `divider` (section break), `stat` (`##` is the big number, `#` the claim), `quote`, `cols` (title + two blocks; for two lists use `-` then `*`), `dark`. Brand color: `style: section { --octo-accent: #E11D48; }` in the front matter.

## Links

- [Homepage](https://github.com/muvon/octomind-tap)
- [Marp CLI](https://github.com/marp-team/marp-cli)
- [Marpit directives](https://marpit.marp.app/directives)
