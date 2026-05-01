# ffmpeg/ffmpeg

ffmpeg — the de-facto multimedia framework. Used by every video agent for final stitching, transcoding to platform specs, and burning captions/overlays. Invoked via shell (no MCP wrapper needed).

## Key Commands

| Command | Description |
|---------|-------------|
| `ffmpeg -i in.mp4 -vf "scale=1080:1920" out.mp4` | Resize / aspect-ratio fit |
| `ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4` | Lossless concat |
| `ffmpeg -i v.mp4 -i a.mp3 -c:v copy -shortest out.mp4` | Overlay voiceover |
| `ffmpeg -i in.mp4 -vf "subtitles=cap.srt" out.mp4` | Burn captions |
| `ffmpeg -i in.mp4 -vf "fps=30,scale=1080:-2" -c:v libx264 -crf 23 -preset veryfast -pix_fmt yuv420p out.mp4` | Re-encode for social platforms |

## Common Usage

```bash
# Concat clips for a TikTok ad (vertical 9:16, 30fps, H.264)
printf "file 'clip1.mp4'\nfile 'clip2.mp4'\nfile 'clip3.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy concat.mp4
ffmpeg -i concat.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -crf 23 -preset veryfast -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 128k tiktok.mp4

# Burn auto-generated SRT captions
ffmpeg -i tiktok.mp4 -vf "subtitles=captions.srt:force_style='Fontsize=44,Outline=2,Shadow=1'" tiktok-final.mp4
```

## Links

- [Homepage](https://ffmpeg.org/)
- [Documentation](https://ffmpeg.org/ffmpeg.html)
- [Filters reference](https://ffmpeg.org/ffmpeg-filters.html)
