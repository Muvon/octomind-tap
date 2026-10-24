# softcatala/whisper-ctranslate2

whisper-ctranslate2 — a Whisper-compatible command-line client built on faster-whisper (CTranslate2). Runs locally on CPU or CUDA with no API key and writes word-level timestamps to JSON, which the `captions` capability's default provider uses for word-timed burned captions. Installed with `uv tool install`, pinned to an exact version; Whisper models download from Hugging Face on first use (`small` ≈ 480 MB, cached afterwards).

## Key Commands

| Command | Description |
|---------|-------------|
| `whisper-ctranslate2 vo.wav --model small --word_timestamps True --output_format json --output_dir out` | Transcribe with per-word start/end times (`segments[].words[]`) |
| `whisper-ctranslate2 vo.wav --language en --initial_prompt "Octomind, HeyGen"` | Fix the language and bias spelling of names and jargon |
| `whisper-ctranslate2 talk.wav --vad_filter True --output_format srt` | Skip silence with Silero VAD and write a sentence-level SRT |
| `whisper-ctranslate2 vo.wav --compute_type int8 --device cpu` | Low-memory CPU run |

## Common Usage

```bash
# 16 kHz mono WAV in, word-timed JSON out (./video-out/<slug>/captions/vo.json)
ffmpeg -i final-mix.mp4 -vn -ar 16000 -ac 1 captions/vo.wav
whisper-ctranslate2 captions/vo.wav --model small --language en \
  --word_timestamps True --output_format json --output_dir captions

# Larger model for noisy creator footage or non-English speech
whisper-ctranslate2 captions/vo.wav --model large-v3-turbo --word_timestamps True --output_format json --output_dir captions
```

Model guide: `small` / `small.en` for clean voiceover (fast on a laptop CPU), `medium` or `large-v3-turbo` for noisy footage, accents, or non-English. Whisper drops some filler words ("um", "uh"); an `--initial_prompt` written with fillers makes it keep more of them when you need to cut them.

## Links

- [Homepage](https://github.com/Softcatala/whisper-ctranslate2)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- [PyPI](https://pypi.org/project/whisper-ctranslate2/)
