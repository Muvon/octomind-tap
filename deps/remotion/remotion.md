# remotion/remotion

Remotion — programmatic React-based video composition. Scaffold a project with `create-video`, write compositions as React components, and render locally with `npx remotion render` (or at scale with Remotion Lambda). Best for templated explainers, motion-graphics overlays, and data-driven creative variants where a copy change should be a one-line diff. The tap drives the official CLI through the shell tool; there is no MCP server to run (Remotion's own `@remotion/mcp` serves documentation only). Requires Node.js 20.19+ / 22.13+ / 24+; Remotion downloads its headless Chrome on the first render.

## Key Commands

| Command | Description |
|---------|-------------|
| `npx create-video@4.0.538 --yes --blank remotion-project` | Scaffold an empty project non-interactively |
| `npx create-video@4.0.538 --yes --tiktok remotion-project` | Scaffold the TikTok-style word-highlight captions template |
| `npx remotion compositions` | List compositions in the project |
| `npx remotion render <CompositionId> out/video.mp4 --props=props.json` | Render a composition with input props |
| `npx remotion still <CompositionId> out/frame.png --frame=45` | Render one frame for a visual check |

## Common Usage

```bash
npx create-video@4.0.538 --yes --blank video-out/demo/remotion-project
cd video-out/demo/remotion-project && npm i
# edit src/Root.tsx and src/*.tsx compositions, then:
npx remotion still Main out/check.png --frame=60
npx remotion render Main out/master-16x9.mp4 --codec=h264 --crf=18
```

Captions: `@remotion/captions` takes `Caption[]` JSON (`text`, `startMs`, `endMs`, `timestampMs`, `confidence`) and `createTikTokStyleCaptions()` pages it for word-highlight rendering.

Licensing: free for individuals, for-profit companies with up to 3 employees, and non-profits; larger companies need a Remotion Company License.

## Links

- [Remotion docs](https://www.remotion.dev/docs/)
- [create-video CLI](https://www.remotion.dev/docs/cli/create-video)
- [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills)
- [@remotion/captions](https://www.remotion.dev/docs/captions/)
- [License](https://www.remotion.pro/license)
