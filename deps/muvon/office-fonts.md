# muvon/office-fonts

office-fonts installs open fonts with the same character widths as the Microsoft Office defaults: Carlito (Calibri), Caladea (Cambria), and Liberation Sans, Serif, and Mono (Arial, Times New Roman, Courier New). A document written for Calibri 11 pt keeps its line breaks and page count when it is rendered on a machine without Office, so `doc-export pdf` and LibreOffice page counts match what the recipient sees in Word. Linux gets the distribution packages, macOS gets Carlito and Caladea from Homebrew (it already ships Arial, Times New Roman, and Courier New), and Windows is skipped because it has the originals.

## Key Commands

| Command | Description |
|---------|-------------|
| `fc-list \| grep -i -e carlito -e liberation` | Confirm the fonts are installed (Linux) |
| `typst fonts \| grep -i -e carlito -e liberation` | Confirm Typst sees them |
| `doc-export pdf letter.md -o letter.pdf --font Calibri` | Uses Carlito automatically when Calibri itself is missing |

## Common Usage

```bash
bash deps/muvon/office-fonts.sh
doc-export pdf proposal.md -o proposal.pdf --font "Times New Roman" --size 12 --max-pages 20
```

| Original | Clone |
|----------|-------|
| Calibri | Carlito |
| Cambria | Caladea |
| Arial, Helvetica | Liberation Sans |
| Times New Roman | Liberation Serif |
| Courier New | Liberation Mono |

## Links

- [Liberation fonts](https://github.com/liberationfonts/liberation-fonts)
- [Carlito](https://fonts.google.com/specimen/Carlito)
- [Caladea](https://fonts.google.com/specimen/Caladea)
