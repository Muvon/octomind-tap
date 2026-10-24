# muvon/video-captions

video-captions — the tap's caption renderer for social video. It turns word-level timestamps (faster-whisper / whisper-ctranslate2, OpenAI verbose_json, whisper.cpp, WhisperX, AssemblyAI, Deepgram, ElevenLabs Scribe or TTS alignment, Remotion `Caption[]`) into a styled ASS subtitle file with an animated active-word highlight, and burns it with an ffmpeg that has libass (it finds Homebrew's keg-only `ffmpeg-full` on its own). The installer links the `video-captions` skill's bundled `scripts/captions.py` onto PATH so agents can call it whether or not the skill is loaded. Python 3.9+, standard library only.

## Key Commands

| Command | Description |
|---------|-------------|
| `video-captions vo.json --video cut.mp4 -o captions.ass --fontsdir fonts --burn out.mp4` | Render the default `pop` preset and burn it into the video |
| `video-captions vo.json --res 1080x1920 -o captions.ass --preset box` | Render only; prints the matching ffmpeg burn command |
| `video-captions vo.json --video cut.mp4 -o c.ass --hook "Stop scrolling" --hook-end 3` | Add a top hook box for the first 3 s |
| `video-captions vo.json --res 1920x1080 -o c.ass --preset clean --srt c.srt` | 16:9 sentence captions plus an upload SRT |
| `video-captions vo.json --res 1080x1920 -o c.ass --remotion captions.json` | Also write Remotion `Caption[]` JSON |
| `video-captions --help` | All options: presets, colors, position, paging, fixes |

## Common Usage

```bash
whisper-ctranslate2 captions/vo.wav --model small --word_timestamps True --output_format json --output_dir captions
video-captions captions/vo.json --video work/mix.mp4 -o captions/captions.ass \
  --preset pop --fontsdir fonts --replace octamind=Octomind --srt captions/captions.srt \
  --burn cuts/master-9x16.mp4
```

Presets: `pop` (1–3 words, active word recolored and scaled), `karaoke` (spoken words stay lit), `word` (one big word), `box` (TikTok-native text box), `clean` (sentence captions on a translucent box for 16:9).

## Links

- [Homepage](https://github.com/muvon/octomind-tap)
- [ASS override tags](https://aegisub.org/docs/latest/ass_tags/)
- [ffmpeg ass filter](https://ffmpeg.org/ffmpeg-filters.html#ass)
