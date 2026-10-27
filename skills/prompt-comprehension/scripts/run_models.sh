#!/usr/bin/env bash
# Run one comprehension test on several models in parallel.
# Usage: run_models.sh <id> <iteration> <model>...
# Reads texts/<id>.i<iteration>.txt and tail-<id>.txt from the current directory,
# writes prompts/<id>-i<iteration>.txt and out/<id>-i<iteration>-<model-slug>.{txt,err}.
# The model runs isolated: from an empty sandbox/ (it cannot read keys or other outputs),
# with no auto-activated tools, and with the supervisor and learning off so their injected
# rules cannot answer the questions for it.
set -eu

if [[ $# -lt 3 ]]; then
  echo "usage: run_models.sh <id> <iteration> <model>..." >&2
  exit 2
fi

id=$1 iter=$2
shift 2
work=$(pwd)
mkdir -p prompts out sandbox

{
  echo "Read the text below, then do both parts. Use only the text, no outside assumptions."
  echo "<text>"
  cat "texts/$id.i$iter.txt"
  echo "</text>"
  cat "tail-$id.txt"
} >"prompts/$id-i$iter.txt"

for model in "$@"; do
  slug=$(printf '%s' "$model" | tr '/:' '__')
  (cd sandbox && octomind run assistant:plain -m "$model" --format plain \
    -c skills.auto_activation=false -c supervisor.enabled=false -c supervisor.learning.enabled=false \
    <"$work/prompts/$id-i$iter.txt" >"$work/out/$id-i$iter-$slug.txt" 2>"$work/out/$id-i$iter-$slug.err") &
done
wait
