#!/usr/bin/env bash
# scripts/smoke-render.sh
# End-to-end check of the artifact CLIs the tap ships. Installs their deps with
# the dep scripts, then renders a slide deck, a PDF and DOCX, an ATS resume, a
# thumbnail, burned-in captions, and a GitHub social preview. Fails on any missing output or failed check.
#
# Usage: bash scripts/smoke-render.sh [workdir]   # default: a fresh temp dir

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FIXTURES="$REPO_ROOT/scripts/fixtures/smoke-render"
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
cp "$FIXTURES/proposal.md" .
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
cp "$FIXTURES/Jane_Doe_CV.yaml" .
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
cp "$FIXTURES/words.json" .
video-captions words.json -o captions.ass --video clip.mp4 --burn captioned.mp4
need_file captioned.mp4

echo "== social-preview"
cp "$FIXTURES/mark.svg" .
social-preview -o card.png --preview card-preview.png --name acme --tagline "Two-way sync for Postgres" \
  --badge "Open source · Go · MIT" --install "go install acme.dev/acme@latest" --url github.com/acme/acme \
  --logo mark.svg --accent "#0969da"
need_file card.png
need_file card-preview.png
echo
echo "ALL RENDERS OK"
