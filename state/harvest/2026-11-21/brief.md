# Harvest brief, 2026-11-21

14 items shortlisted from 409 candidates (327 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] ten free or cheap AI video generators
key: vault:2026-11-21:ten-free-or-cheap-ai-video-generators
url: https://www.instagram.com/p/Df7PXm4H9rr/
meta: {"vault_status": "open", "kind": "tool", "subject": "@alamin.8020ai ten free AI video tools carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-alamin-10-free-ai-video-tools.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: tool names are on the slides, need screenshots to compare against Kling, Seedance, Veo, HeyGen

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Listicle of ten AI video tools; names live on the slides, unseen, nothing assessed Write-up: `TRITON-CORE/Research/links/2026-11-21-alamin-10-free-ai-video-tools.md` Link: https://www.instagram.com/p/Df7PXm4H9rr/

## 2. [hn] Ask HN: I have been unemployed for 2y. 15 years of experience, US. What to do?
key: hn:50583761
url: https://news.ycombinator.com/item?id=50583761
discussion: https://news.ycombinator.com/item?id=50583761
meta: {"points": 585, "comments": 643, "created": "2026-11-20T23:18:32Z"}
query: bonding curve

I'm Senior software engineer in the US (DMV area), with 15y of experience. Worked for Fortune 50+ company and bunch of mid-size companies. Been unemployed for 2y and can't find a job, within those 2 years, I pretty much spent my savings that I've saved through years, maybe have 4-5 months left to support my household. Currently, I tutor math and probably about to start working as manager in pizzaria. In Jan 2025, I quit from a mid-size insurance tech company(1000+) after working there for almost 4y, because I was tipped off the they were about to start layoffs and they did. Well, since then I have zero luck finding any job in SWE. At this point, I have massive gap in my resume that I can't explain to recruiters, I can still code (C#/.NET/AWS) and learned the AI, but who cares if date of my last employment is Jan2025. What should I do ? If you have an alternative path (something completely different from SWE or SWE adjacent) that pays "well", I would like to hear.
comment (jareklupinski): my last few positions were from people messaging one mailing list i was on or another, asking if anyone wants to join their team keep checking that junk folder :)
comment (mxfactorial): when ur done looking for a job from corporations ur welcome to help eliminate them @gradienterp.cloud
comment (pluc): 3y/25yoe for me so clearly I have no advice to give, just want to say that it's not you, it's a terrible state of affair out there right now.

## 3. [github] kimtaeyoon83/mcp-server-youtube-transcript: This is an MCP server that allows you to directly download transcripts of YouTube videos.
key: gh:kimtaeyoon83/mcp-server-youtube-transcript
url: https://github.com/kimtaeyoon83/mcp-server-youtube-transcript
meta: {"stars": 609, "created": "2024-11-29", "pushed": "2026-11-21", "language": "TypeScript", "topics": []}
query: youtube transcript pushed:>{since} stars:>20

[](https://mseep.ai/app/kimtaeyoon83-mcp-server-youtube-transcript)

# YouTube Transcript Server
[](https://archestra.ai/mcp-catalog/kimtaeyoon83__mcp-server-youtube-transcript)

[](https://smithery.ai/server/@kimtaeyoon83/mcp-server-youtube-transcript)

A Model Context Protocol server that enables retrieval of transcripts from YouTube videos. This server provides direct access to video captions and subtitles through a simple interface.

   

### Installing via Smithery

To install YouTube Transcript Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kimtaeyoon83/mcp-server-youtube-transcript):

```bash
npx -y @smithery/cli install @kimtaeyoon83/mcp-server-youtube-transcript --client claude
```

## Components

### Tools

- **get_transcript**
  - Extract transcripts from YouTube videos
  - Inputs:
    - `url` (string, required): YouTube video URL, Shorts URL, or video ID
    - `lang` (string, optional, default: "en"): Language code for transcript (e.g., 'ko', 'en'). Automatically falls back to available languages if requested language is not found.
    - `include_timestamps` (boolean, optional, default: false): Include timestamps in output (e.g., '[0:05] text')
    - `strip_ads` (boolean, optional, default: true): Filter out sponsorships, ads, and promotional content from transcript based on chapter markers

- **analyze_video** (optional, requires a TwelveLabs API key)
  - Analyze a video with [TwelveLabs](https://twelvelabs.io) Pegasus, a video-understanding model. Unlike `get_transcript`, this reasons over what is *shown* on screen, so it produces useful summaries and answers even for videos with little or no speech (demos, gameplay, b-roll, music videos).
  - Inputs:
    - `url` (string, required): A publicly reachable **direct video URL** (e.g. an `.mp4`/`.mov`/`.webm` link or a pre-signed URL). TwelveLabs fetches the file server-side, so a YouTube watch page URL will not work — it serves HTML, not a raw video stream.
    - `prompt` (string, optional): Instruction or question for the model (e.g. `"Summarize this video in 3 sentences"` or `"What products are shown?"`). Defaults to a general summary.
    - `model` (string, optional, default: `"pegasus1.2"`): Pegasus model to use (`"pegasus1.2"` or `"pegasus1.5"`).
    - `max_tokens` (number, optional, default: 2048): Maximum response length in tokens.
  - Requires the `TWELVELABS_API_KEY` environment variable. The transcript tool works without it; analysis is fully opt-in. Grab a free key at [twelvelabs.io](https://twelvelabs.io) — there's a generous free tier.

## Key Features

- Support for multiple video URL formats (including YouTube Shorts)
- Language-specific transcript retrieval with automatic fallback
- Optional timestamps for referencing specific moments
- Built-in ad/sponsorship filtering (enabled by default)
- Zero external dependencies for transcript fetching
- Detailed metadata in responses

## Configuration

To use with Claude Desktop, add this server configuration:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "npx",
      "args": ["-y", "@kimtaeyoon83/mcp-server-youtube-transcript"]
    }
  }
}
```

To enable the optional `analyze_video` tool, add your TwelveLabs API key:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "npx",
      "args": ["-y", "@kimtaeyoon83/mcp-server-youtube-transcript"],
      "env": {
        "TWELVELABS_API_KEY": "your-twelvelabs-api-key"
      }
    }
  }
}
``

## 4. [arxiv] ZeroVLN: Learning to Navigate without Supervised Fine-Tuning of the VLM Brain
key: arxiv:2611.26414
url: https://arxiv.org/abs/2611.26414
meta: {"published": "2026-11-19", "authors": ["Zixuan Huang", "Yang Zhou", "Guli Zhang", "Sunzhu Li"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Representative vision-language navigation (VLN) methods typically couple a vision-language model (VLM) brain with a learnable action head and fine-tune the VLM brain on navigation-domain data to predict geometric goals. However, such adaptation can substantially alter base VLM weights and degrade general visual capabilities. We introduce ZeroVLN, a slow-fast navigation framework that achieves effective navigation with zero navigation-domain SFT of the VLM brain. Rather than teaching the brain to predict geometric goals, we equip it with a semantic tool-calling interface for conveying movement decisions to an action expert in natural language. We first adapt the action expert to carry out these movement requests, then jointly improve the brain's movement decisions and the action expert's continuous execution through closed-loop reinforcement learning (RL). Trained on the same navigation episodes, ZeroVLN substantially outperforms representative SFT-based hierarchical VLN methods on standard VLN-CE (continuous environments) benchmarks, while inducing only minor changes to the brain's weights and largely preserving its general capabilities. To our knowledge, ZeroVLN is the first slow-fast VLN framework with zero navigation-domain SFT of the VLM brain, and the first to jointly optimize its slow and fast policies through closed-loop agentic RL in VLN-CE.

## 5. [youtube] The UK MOT postcode lottery: 8.4 points between best and worst
key: yt:mdzIXanauYk
url: https://www.youtube.com/watch?v=mdzIXanauYk
meta: {"channel": "MOTFaults", "rank": 2, "duration_min": 0}
query: MOT data analysis uk

# The UK MOT postcode lottery: 8.4 points between best and worst
# MOTFaults
# https://www.youtube.com/watch?v=mdzIXanauYk

[00:00] Same cars, same [music] age, very different MOT results. In Scotland, 81.4 % pass. In London, 89.8 [music] %. 8.4 points between the best region and the worst. Cars built 2015 to 2019. Where a car has lived can matter. [music] Check its MOT history before you buy. Every model, every year, and MOT pass rates in your local area. [music] Free at motfaults.co.uk.

## 6. [vault] Hook, Problem, Solution, Proof, CTA audit pass and the generic-opener ban list
key: vault:2026-11-21:hook-problem-solution-proof-cta-audit-pass-and-the-generic-o
url: https://www.instagram.com/p/DfO05yDle-w/
meta: {"vault_status": "open", "kind": "service", "subject": "@jayantcreates.ai three Claude reel-writing skills carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-jayantcreates-claude-reel-scriptwriter-skills.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: cheap checklist to add to the script step, read the slides first

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Hook, script audit and voice Projects for reel scripts; same shape as existing bank, slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-21-jayantcreates-claude-reel-scriptwriter-skills.md` Link: https://www.instagram.com/p/DfO05yDle-w/

## 7. [hn] Show HN: AgentMall – Let your AI agent buy groceries
key: hn:50562508
url: https://getagentmall.com
discussion: https://news.ycombinator.com/item?id=50562508
meta: {"points": 21, "comments": 10, "created": "2026-11-19T16:46:14Z"}
query: bonding curve

Hey HN, we’re Nel and Kosi. We noticed personal agents like Instinct, Muse were terrible at buying stuff. Most of the time the checkout would fail. So we built reliable automations for agents to checkout at 9 leading grocery merchants. We grapple with anti bot, logins, OTP codes, and changing checkout structures. Loved revisiting this stuff given our backgrounds sneaker-botting and building computer use models. Honestly full circle haha. It currently works on these sites with ~70% checkout success rate: - Walmart - Albertsons - Ocado - Wegmans - FreshDirect - Best Buy - Instacart Our goal is to hill climb to 90%+ across each. Test keys are free and run the real flow without placing an order. New accounts get 10 free completed orders. https://docs.getagentmall.com/quickstart
comment (kidnertom): how is this different to browserbase or kernel??
comment (henrylamb07): I would love for an agent to do my grocery shopping for me, but then I have to give it access to my bank card. No way.
comment (y_els): Are you planning to run it on airline sites? They change things very regularly and have anti-scraping.

## 8. [github] danielwh2/sprite-stacking: Agent skill: turn four pixel art views into fake-3D sprites you can spin. Works with Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Pi.
key: gh:danielwh2/sprite-stacking
url: https://github.com/danielwh2/sprite-stacking
meta: {"stars": 360, "created": "2026-11-20", "pushed": "2026-11-21", "language": "HTML", "topics": ["agent-skills", "claude-code", "codex", "cursor", "fake-3d", "gamedev", "pixel-art", "sprite-stacking"]}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# sprite-stacking

An agent skill that turns four pixel art views into fake-3D sprites you can spin. By Daniel White.

## Install

```bash
npx skills add danielwh2/sprite-stacking
```

Installs to the current project. Add `-g` for every project, `-a claude-code` (or `codex`, `cursor`, ...) to pick an agent. Uses the [skills CLI](https://github.com/vercel-labs/skills), Node 22.20 or later.

Or copy `skills/sprite-stacking` into your agent's skills folder:

| Agent | Folder |
| --- | --- |
| Claude Code | `~/.claude/skills/` |
| Codex, Cursor, OpenCode, Gemini CLI, Pi | `~/.agents/skills/` |

## Use

Ask your agent:

- "Make a rotatable pixel art car."
- "Sprite stack this 4-view sheet and give me a turntable."
- "Add a fake 3D pixel art tree to my Godot game."

No image generator? The agent draws the views itself in a short Python script.

## How it works

1. **Views:** top, side, front and back, orthographic, one row.
2. **Carve:** a voxel survives only where all four views cover it.
3. **Slices:** the volume is cut into a strip of flat layers, ground first.
4. **Render:** each layer is rotated, squashed for pitch and lifted 1 px.

## Slicer CLI

```bash
python3 skills/sprite-stacking/scripts/views_to_slices.py views.png slices.png \
  --slices 36 --preview check.png --html viewer.html
```

- `--slices N`: layer count. 15-20 chunky, 32-48 detailed.
- `--order reading`: force TOP, SIDE, FRONT, BACK. Default matches views by proportion.
- `--round`: towers, balloons, pots carve round, not square.
- `--side-nose right`: the side view faces right.
- `--colours N`: shared palette size, `0` keeps every colour.
- `--normals path.png`: save a matching 3D normal-map slice strip.
- `--emissive path.png`: save an auto-detected emissive mask strip (headlights, windows, neon).

## Viewer

`--html` writes a standalone page:
- **Modes:** Turntable, **Scene** (Living Diorama with **Neon Street** and **Meadow Island** procedural stacked props, unified Y-sorting, and multi-PNG drop / `+ Add Prop`), Slice scan, Exploded view, and **Play** mode (**Drive** with WASD/arrows + drift across infinite Street/Meadow/Grid worlds, **Wind** sway, **Shatter** & rebuild).
- **Lighting & Weather:** Live **Time of Day** (Day → Sunset → Night with auto-emissive glow and ground light pools), draggable sun (`Shift+drag`) with projected 3D shadows, and **Weather** (**Rain** with pixel streaks, ground ripples, and wavy upside-down wet reflections; **Snow** with real-time snow cap accumulation on upward-facing voxels via `normZ`).
- **Performance:** Vectorized NumPy carving, zero-allocation typed-array software rasterizer, and angle/lighting-keyed prop sprite caching (~0.2–1.5 ms/frame in Chrome).
- **Export:** 16-direction baked PNG sprite sheet export. `skills/sprite-stacking/scripts/viewer.html` also opens on its own and accepts dropped slice strips.

## Requirements

Python 3 with Pillow and NumPy (`pip install pillow numpy`).

## Contributing

```bash
python3 tests/check.py
```

Prints `ok`.

## Prior art

Sprite stacking is a long-standing indie game technique, not invented here. This skill adds the four-view carving and the agent workflow.

## Licence

MIT

## 9. [arxiv] ResVision: Spectrum-Matched Resizing and Context-Preserving Inspection for Visual Reasoning
key: arxiv:2611.26318
url: https://arxiv.org/abs/2611.26318
meta: {"published": "2026-11-19", "authors": ["Guojian Zhan", "Jiahao Xu", "Yahui Liu", "Yao Hu"], "categories": ["cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Agentic visual reasoning improves vision-language models by selectively enlarging evidence without adding new scene content, but the benefit depends on whether fine structure remains accessible and whether local observations stay grounded in the full scene. We identify three recurring bottlenecks: high-frequency detail can be attenuated during visual-token formation; spatially distributed evidence can remain encoded yet difficult for the language model to retrieve; and isolated crops can weaken whole-detail correspondence through scale and positional mismatch. ResVision addresses these limitations with two complementary components. Spectrum-Matched Resizing (SMR) estimates image complexity and selects an adaptive global sampling scale, avoiding unnecessary enlargement on simple inputs while allocating more visual tokens to detail-rich images. Context-Preserving Inspection (CPI) returns each inspected crop together with the complete working view, preserving local detail and global context across tool turns. We evaluate Direct and Agentic variants on four frontier VLMs and 29 benchmarks spanning six visual-reasoning families. Complete ResVision (Agentic Base plus SMR plus CPI) is best for every model, improving by 3.36 to 4.94 points over Direct Base and 1.87 to 2.94 points over Agentic Base. These results show that adaptive visual sampling and context-preserving inspection address distinct, complementary constraints in multimodal reasoning.

## 10. [youtube] Martin Has Beaten The Worst Lichess Bot?
key: yt:co33P6bb0eg
url: https://www.youtube.com/watch?v=co33P6bb0eg
meta: {"channel": "Studying Chess", "rank": 4, "duration_min": 0}
query: lichess bot python engine

# Martin Has Beaten The Worst Lichess Bot?
# Studying Chess
# https://www.youtube.com/watch?v=co33P6bb0eg

[00:00] Martin the worst chess.com bot has finally won a game I paired him against the worst Lee chess bot and they played a tough game with 40 blunders and numerous mistakes but eventually on 80c move Martin checkmated the worst leeches bot click the link down below to watch the full game

## 11. [vault] repurpose one piece into reels, shorts, threads and LinkedIn
key: vault:2026-11-21:repurpose-one-piece-into-reels-shorts-threads-and-linkedin
url: https://www.instagram.com/p/DftKkuIjiJn/
meta: {"vault_status": "open", "kind": "service", "subject": "@seb.ai four-agent AI content team carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-seb-ai-four-agent-content-team.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: check the social engine for this step before adding it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Four chained prompt roles (hook, value, repurpose, schedule); mostly branding, repurpose step may be missing; slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-21-seb-ai-four-agent-content-team.md` Link: https://www.instagram.com/p/DftKkuIjiJn/

## 12. [hn] Show HN: Zpup – Zdog style 3D scenes in JSON, SVG from any angle
key: hn:50556534
url: https://github.com/rxolve/zpup
discussion: https://news.ycombinator.com/item?id=50556534
meta: {"points": 16, "comments": 0, "created": "2026-11-19T05:56:41Z"}
query: claude code

Hi. I made small project called Zpup. It takes small 3D scene written in JSON and gives back a flat SVG from any angle. There is no JavaScript in the file, so it works in img-tag or README. I needed 3D for small project at my company, and Zdog make big impression on me. But Zdog has not had a release for several years, so I wanted to make modern version. One thing works different. Zdog sorts each shape by one point. so small thing on big floor gets covered when you turn it. Zpup compares the shapes that overlap. You can see both in the README. I wrote it with Claude Code Fable 5.2. No canvas renderer, no text shape, and it is 0.2 version. Playground: https://rxolve.github.io/zpup Feedback is always welcome :)

## 13. [github] staryone/motlab: Video as code: canvas scenes rendered with WebCodecs in headless Chrome, a review viewer, and agent skills that build the video from your references.
key: gh:staryone/motlab
url: https://github.com/staryone/motlab
meta: {"stars": 346, "created": "2026-11-16", "pushed": "2026-11-21", "language": "JavaScript", "topics": ["agent-skills", "canvas", "claude-code", "headless-chrome", "motion-graphics", "video", "webcodecs"]}
query: claude-code created:>{since} stars:>20

# motlab

A video engine where every scene is code, and an agent skill that writes the scenes for you.

 npm install -g @motlab/cli && npx @motlab/cli setup 

[Demo](#watch-the-demo) · [Install](#install) · [Quick start](#quick-start) · [Speed](#speed) · [How it works](#how-it-works) · [Docs](#documentation) · [FAQ](#faq) · [Roadmap](ROADMAP.md)

[](https://github.com/staryone/motlab/actions/workflows/ci.yml)
[](LICENSE)
[](package.json)

 

---

Every scene is a canvas page with one function, `renderAt(t)`, that draws the frame at time `t`. motlab plays the pages in a web viewer where you step through them frame by frame, and renders them to MP4 in headless Chrome. You hand your agent a folder of references (logos, screenshots, footage, fonts, music, voice) and a direction, and it builds every scene, opens the viewer and revises from your notes. No AI image or video model is involved.

The ad above (19 seconds, 7 scenes) was made with motlab and its skill, reviewed in the viewer and exported at 4K. The preview is silent; [watch it with sound](https://github.com/user-attachments/assets/5e2ff219-697c-459f-a273-f36cb11db1d1).

## What it does

- Your agent writes each scene as a canvas page, from your references and a short brief.
- The viewer plays the real pages with their audio, frame by frame, with a timeline you can zoom and step through.
- You point at what to change: click a frame, drag a box over a part of it, or mark a time range, and type a note on it. The agent reads every note from `selection.json` and works through them by number.
- Versions of a project sit side by side in the viewer, so a second cut does not overwrite the first.
- Export renders 720p, 1080p, 1440p or 4K MP4, with the scenes' transitions, music and voice mixed in. Scenes render three at a time by default (fewer on a small machine, and the Export menu lets you pick 1 to 4), which took a project of 12 short scenes from 93 to 53 s at 4K, and `"qp"` in `project.json` makes the file smaller (about 30% at `22`) when you need that.
- The viewer can run on your own server behind a domain and a password, so you can review and export from your phone.
- Notes are a box, a point or a pencil drawing on the frame. The viewer loads a scene again by itself when the agent saves it, and marks the scenes the agent says it is working on.
- A long talking-head take is cut at its pauses and can be split into one scene per section, with captions placed from a transcript.
- Frames are encoded with WebCodecs inside the page, so they never leave Chrome as images. On a GPU that made it 2 to 4 times as fast as Remotion and HyperFrames on the [benchmark scene](#speed).
- A second skill, `motlab-assets`, builds reusable asset kits the same way: icons, illustrations, 2D characters with a rig, transitions, 3D objects and textures, rendered to transparent PNG plus SVG, or GLB, FBX and OBJ with PBR textures. Every video that uses the kit shares one look.

## Watch the demo

Two minutes in English, made with motlab too: the install, the brief to the agent, the build, playing it in the viewer, notes on frames, versions, the revision and the export.

https://github.com/user-attachments/assets/8f70bc60-5f56-4c4f-b55e-bf9f87ba1e34

## Install

You need Node 24 or newer, Google Chrome or Chromium, and ffmpeg with ffprobe on PATH. Python 3 is optional and only used by the skills' helper scripts. Blender is optional too, for the asset skill's main 3D path.

```bash
npm install -g @motlab/cli
npx @mo

## 14. [youtube] Which car fails its MOT the least? (UK 2025) #shorts
key: yt:odRxggAh3G8
url: https://www.youtube.com/watch?v=odRxggAh3G8
meta: {"channel": "CompareAutoParts", "rank": 4}
query: MOT data analysis uk


[body unavailable: TranscriptsDisabled]
