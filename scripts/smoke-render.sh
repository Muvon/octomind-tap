#!/usr/bin/env bash
# scripts/smoke-render.sh
# End-to-end check of the artifact CLIs the tap ships. Installs their deps with
# the dep scripts, then renders a slide deck, a PDF and DOCX, an ATS resume, a
# thumbnail, burned-in captions, and a GitHub social preview. Fails on any missing output or failed check.
#
# Usage: bash scripts/smoke-render.sh [workdir]   # default: a fresh temp dir

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPS=(muvon/slide-deck muvon/doc-export jgm/pandoc typst/typst freedesktop/poppler muvon/office-fonts
  rendercv/rendercv ffmpeg/ffmpeg muvon/video-fonts muvon/video-thumbnail muvon/video-captions
  muvon/ui-fonts muvon/social-preview)

# Dep scripts link CLIs into ~/.local/bin; later steps need it on PATH too.
export PATH="$HOME/.local/bin:$PATH"

for dep in "${DEPS[@]}"; do
  echo "== dep $dep"
  bash "$REPO_ROOT/deps/$dep.sh"
done

WORK="${1:-$(mktemp -d)}"
mkdir -p "$WORK"
cd "$WORK"
echo "== working in $WORK"

need_file() {
  [[ -s $1 ]] || {
    echo "FAIL: $1 missing or empty" >&2
    exit 1
  }
}

echo "== slide-deck"
slide-deck new deck.md --title "Churn concentrates in month two"
slide-deck render deck.md --png --pptx
need_file deck.pdf
need_file deck.pptx
compgen -G "deck-png/*.png" >/dev/null || {
  echo "FAIL: no PNG previews" >&2
  exit 1
}

echo "== doc-export"
cat >proposal.md <<'EOF'
---
title: "Smoke test proposal"
---

# Summary

One paragraph of plain text, so the PDF carries a real text layer, and a table.

| Item | Cost |
|---|---|
| Discovery | 1,200 |
EOF
doc-export pdf proposal.md -o proposal.pdf --max-pages 2 2>pdf.log
cat pdf.log
# The default Calibri must render as Calibri or its metric clone, never Typst's fallback serif.
if grep -q "fall back" pdf.log; then
  echo "FAIL: PDF fell back to the default font" >&2
  exit 1
fi
doc-export docx proposal.md -o proposal.docx
need_file proposal.docx
doc-export check proposal.pdf --max-pages 2 --text 5

echo "== rendercv"
cat >Jane_Doe_CV.yaml <<'EOF'
cv:
  name: Jane Doe
  location: Berlin, Germany
  email: jane@example.com
  phone: "+49 30 1234567"
  website: https://janedoe.dev/
  social_networks:
    - network: LinkedIn
      username: janedoe
  sections:
    summary:
      - Backend engineer, 7 years in payments; led the PSD3 migration at a 40-person fintech.
    experience:
      - company: Finly
        position: Senior Backend Engineer
        location: Berlin
        start_date: 2022-03
        end_date: present
        highlights:
          - Cut payment failure rate from 2.1% to 0.6% by redesigning retry logic (Go, Kafka)
    education:
      - institution: TU Munich
        area: Computer Science
        degree: MSc
        start_date: 2014-10
        end_date: 2017-03
    skills:
      - label: Languages
        details: Go, Python, SQL
design:
  theme: engineeringresumes
  page:
    size: a4
    show_top_note: false
    show_footer: false
  header:
    connections:
      show_icons: false
      phone_number_format: international
  templates:
    experience_entry:
      main_column: "**POSITION**, COMPANY -- LOCATION\nDATE\nSUMMARY\nHIGHLIGHTS"
      date_and_location_column: ""
    education_entry:
      main_column: "**INSTITUTION**, DEGREE_WITH_AREA -- LOCATION\nDATE\nSUMMARY\nHIGHLIGHTS"
      date_and_location_column: ""
EOF
rendercv render Jane_Doe_CV.yaml --pdf-path resume.pdf -nohtml -nopng
doc-export check resume.pdf --max-pages 1 --text 4
# Each date must follow its entry in the text layer, not drift to the page end.
pdftotext resume.pdf - | grep -A1 'TU Munich' | grep -q 'Oct 2014' || {
  echo "FAIL: education date detached from its entry in the text layer" >&2
  exit 1
}

echo "== video-thumbnail"
ffmpeg -v error -y -f lavfi -i "testsrc2=s=1920x1080" -frames:v 1 bg.png
video-thumbnail render bg.png -o thumb.jpg --text "I quit my job" --highlight quit --preview thumb-preview.png
need_file thumb.jpg
need_file thumb-preview.png

echo "== video-captions"
ffmpeg -v error -y -f lavfi -i "testsrc2=s=1080x1920:d=3" -f lavfi -i "sine=d=3" -shortest \
  -c:v libx264 -pix_fmt yuv420p -c:a aac clip.mp4
cat >words.json <<'EOF'
{"words": [
  {"word": "Churn", "start": 0.2, "end": 0.6},
  {"word": "drops", "start": 0.6, "end": 1.0},
  {"word": "in", "start": 1.0, "end": 1.2},
  {"word": "month", "start": 1.2, "end": 1.6},
  {"word": "two.", "start": 1.6, "end": 2.2}
]}
EOF
video-captions words.json -o captions.ass --video clip.mp4 --burn captioned.mp4
need_file captioned.mp4

echo "== social-preview"
cat >mark.svg <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect width="10" height="10" fill="#0969da"/></svg>
EOF
social-preview -o card.png --preview card-preview.png --name acme --tagline "Two-way sync for Postgres" \
  --badge "Open source · Go · MIT" --install "go install acme.dev/acme@latest" --url github.com/acme/acme \
  --logo mark.svg --accent "#0969da"
need_file card.png
need_file card-preview.png
echo
echo "ALL RENDERS OK"
