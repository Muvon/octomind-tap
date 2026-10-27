#!/usr/bin/env bash
# Run one comprehension test on several models in parallel.
# Usage: run_models.sh <id> <iteration> <model>...
# Reads texts/<id>.i<iteration>.txt and tail-<id>.txt from the current directory,
# writes prompts/<id>-i<iteration>.txt and out/<id>-i<iteration>-<model-slug>.{txt,err}.
set -eu

if [[ $# -lt 3 ]]; then
  echo "usage: run_models.sh <id> <iteration> <model>..." >&2
  exit 2
fi

id=$1 iter=$2
shift 2
mkdir -p prompts out

{
  echo "Read the text below, then do both parts. Use only the text, no outside assumptions."
  echo "<text>"
  cat "texts/$id.i$iter.txt"
  echo "</text>"
  cat "tail-$id.txt"
} >"prompts/$id-i$iter.txt"

for model in "$@"; do
  slug=$(printf '%s' "$model" | tr '/:' '__')
  octomind run assistant:plain -m "$model" --format plain \
    <"prompts/$id-i$iter.txt" >"out/$id-i$iter-$slug.txt" 2>"out/$id-i$iter-$slug.err" &
done
wait
