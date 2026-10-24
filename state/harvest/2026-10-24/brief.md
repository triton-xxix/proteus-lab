# Harvest brief, 2026-10-24

14 items shortlisted from 349 candidates (214 dropped as already seen, 12 carry a vault verdict on the vendor).

## 1. [vault] Video2X free local upscaler
key: vault:2026-10-24:video2x-free-local-upscaler
url: https://www.instagram.com/p/DemKvEhCDwm/
meta: {"vault_status": "open", "kind": "tool", "subject": "handlytech 10 free AI video tools carousel", "date": "2026-10-24", "where": "TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: test on the M5 against Topaz on fal for final-pass upscales

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Listicle with a comment-FREE DM funnel; three tools new to us (LTX Desktop local, Viggle, Video2X), the rest already routed or generic Write-up: `TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md` Link: https://www.instagram.com/p/DemKvEhCDwm/

## 2. [hn] Show HN: Corgi, a helpful {agent, terminal} multiplexer
key: hn:50214373
url: https://corgi.computer/
discussion: https://news.ycombinator.com/item?id=50214373
meta: {"points": 124, "comments": 42, "created": "2026-10-23T19:46:38Z"}
query: claude code

Hey everyone, Inspired by Herdr, I've built an agent multiplexer that I've been using as my daily driver for a few weeks now. I think I improved on the concept in a few ways, focusing on the ergonomics I always wished I had: I show you what the agents are up to, along with a running feed of their activity. There's also a simple shortcut (F1) to go to the next unread agent. I use multiple accounts, so I've added unified launcher for Codex/Claude Code/Pi. Theres some careful ergonomics there: fast search and resume over sessions, inline usage tracking etc. Many small quality of life improvements to the terminal experience: - Links can be copied with a click, so no need to drag-select over many lines - cmd+v just pastes images (even on SSH) - images have a thumbnail preview. - Built-in CPU/Memory/GPU usage tracking, broken down by workspace I assume you have access to cheap inference (Luna/Haiku/etc). It just reuses the agents to organize things for you: what is this http link? what is this worktree about? what is each agent doing? It's small but it made my environment feel more cozy. On a personal note, I've been on a frustrating sick leave for a while now. I created Corgi to challenge myself, and see if I can go back. The answer is more mixed than I had hoped, but I am happy with the result and thankful for the experience. I hope you like it! a few friends & myself have been using it for a few weeks and it's been pretty nice. There's still a lot to improve and some rough edges
comment (JakeSc): Looks awesome! Will give it a try. I've built something similar, just open-sourced it: https://exawatt.ai I'm big on agent ergonomics. Cool to see what others are doing in the space.
comment (pokpokpok): Been using this for about a month, for me it’s been a great replacement for cmux with good simple design
comment (robsalasco): please add it to brew, I don't like to use bash scripts https://nocurlbash.com/#en

## 3. [github] actionow-ai/vvv: Build a video template once, reuse it across coding agents. Editable Remotion templates and an Agent Skill for Claude Code, Codex and 25+ agents.
key: gh:actionow-ai/vvv
url: https://github.com/actionow-ai/vvv
meta: {"stars": 324, "created": "2026-10-22", "pushed": "2026-10-23", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

Swap in your photos and words for a new film. Or bring a film you love and get your own version. 

[](LICENSE)
[](https://vibevision.video)
[](https://linux.do)
[](docs/agent-compatibility.md)
[](docs/agent-compatibility.md)
[](https://vibevision.video/start/#mcp)

[Website](https://vibevision.video) · [简体中文](README.zh-CN.md) · [Get started](docs/getting-started.md) · [Templates](docs/templates.md) · [Community](https://vibevision.video/community/) · [Docs](docs/README.md)

 

## Made with the templates

 
   
          Doodle  · hand-drawn 
          Album  · clean album 
          DV Story  · camcorder 
   
   
          Comedy  · comic opener 
          Starter  · beat-cut reel 
          Album 9:16  · vertical short 
   
 

  Click a loop for the full preview with sound. All rendered straight from the templates and passing  vvv check ; the couples and photos are fictional.  All templates, formats and styles   

## Say one sentence. Your agent does the rest.

Picking the template, placing photos, writing copy, rendering, checking and delivering all happen in the conversation. You watch the sample and say what to change.

> Use the vvv skill to make a 9:16 wedding short from the photos in ./photos. We are Lin Yizhou and Xu Zhixia, married on October 18. Show me a checked sample first.

**Add it to your agent**, any one of:

| Agent | Install |
|---|---|
| **Claude Code** | `/plugin install vvv --marketplace actionow-ai/vvv` (the plugin includes the templates) |
| **Codex, Cursor, Gemini CLI, Copilot and 20+ more** | `npx skills add actionow-ai/vvv`, then clone this repository and set `VVV_KIT` ([details](docs/agent-compatibility.md)) |
| **WorkBuddy** | Upload the skill ZIP from [Releases](https://github.com/actionow-ai/vvv/releases) under 技能 → 添加技能 ([details](docs/workbuddy.md)) |
| **Any MCP client** | `claude mcp add --transport http vvv https://mcp.vibevision.video/mcp` to browse templates and guides with no install |

Rendering runs on your machine, which needs Python 3.9+, Node.js 26 and npm; the agent installs everything else.

## One template, every new film

The scenes, layouts, timing and checks are built once. A new film changes only what belongs to it.

 
     Built once   Scene structure and camera moves · layouts for 16:9 and 9:16 · beat-planned timing · render checks  
     Changed per film   Photos · names and dates · every line of copy · music and format  
 

`vvv.py describe` tells the agent each template's photo slots, copy fields and settings, and `validate` catches bad inputs before a render. The agent changes the template's inputs first and its React/TypeScript source only where the brief needs it. Reuse is meant to save the tokens otherwise spent redesigning, regenerating and debugging the same video code; no comparative benchmark is published yet (see the [roadmap](ROADMAP.md)).

## Show it a film you love. Get your own.

 

Give your agent a reference video and the attachments that make it yours: photos, a logo, copy, music. It studies how the reference works and rebuilds it as an editable project with your material.

 
   
      01 Reference + attachments  A local video file plus your photos, logo, copy and music. The reference is studied, never shipped. 
      02 Measure  Sections in beats, shot lengths, still frames and beat alignment, measured from the actual file. 
      03 Rebuild  On the closest template or a new composition. Missing artwork is generated; the result is checked against the reference. 
  

## 4. [arxiv] Ask About the Right Moment: Training-Free Object Identity Reasoning for Video-Language Models
key: arxiv:2610.31471
url: https://arxiv.org/abs/2610.31471
meta: {"published": "2026-10-22", "authors": ["Di Yang", "Xiaochang Li", "Muyang Liu", "Yufei Wang"], "categories": ["cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Many questions about a video concern one physical object. Where does the ball end up after the cups are shuffled? Which card is the queen? How often was the mug covered? Video-language models (Video-LMs) recognise such objects in single frames but do not keep them apart over time. On real shell-game videos, open models from 8B to 235B parameters, their thinking variants, a reinforcement-learned tool agent and three training-free tool agents all stay within ten points of chance. We separate semantic identity binding from temporal identity maintenance. An object's identity should be fixed at a moment when the evidence for it is visible, and carried afterwards by a tracker. \emph{Track, Then Bind} implements this principle without training. A promptable video tracker follows every candidate object and draws it with a track number. A frozen vision-language model answers a static question about the identifying evidence, which binds the target to a track. The answer is then derived from the tracked state in text, without asking the model to reinterpret the original video during read-out. A single configuration covers all benchmarks. With Qwen3-VL-32B it solves both VET-Bench tasks, where a fine-tuned trajectory model reaches 92\% and 90\% and the same VLM voting over 16 samples stays at 30--32\%. It answers 55.4\% of the hardest Perception Test cup games, where the best published model answers 41.5\%, and, using track-derived timelines, 48.6\% of TOC-Bench questions, against 37.1\% for the same model answering directly. Drawing the same tracks on the video and asking the question directly falls 12--19 points short of the agent on real cup games.

## 5. [youtube] DVSA Photo at Test: What do MOT Testers really think? #MOTscheme #MOTcompliance #dvsa #mottester
key: yt:ZLbmhgI2FFE
url: https://www.youtube.com/watch?v=ZLbmhgI2FFE
meta: {"channel": "MOT Expert", "rank": 1, "duration_min": 2}
query: MOT data analysis uk

# DVSA Photo at Test: What do MOT Testers really think? #MOTscheme #MOTcompliance #dvsa #mottester
# MOT Expert
# https://www.youtube.com/watch?v=ZLbmhgI2FFE

[00:01] I work for MIT, compliance and mobility expert. Today talking about the photo system and the what's been happening with the DVSA and the rollout, how well that's going. Um most of you will have experienced part of the rollout because your MTS stopped working. Um over the last sort of 3-4 weeks DVSA have been rolling it out to 2,500 stations um every couple of weeks. And inevitably what's happening is the system is falling over. It has a moment, it has a blip. Some of you experienced it, some of you haven't. It hasn't had an instant code released by the DVSA because it's only within segmented areas.
[00:34] Um so it's causing a few issues, but you know, hopefully hopefully we'll start seeing it get better. Um there's been a lot of people online saying oh photo system going to be terrible, this that and the other and it's it's not going to be work and they're all going to moan about it, but actually almost every test that I spoke to and every test that's actually on the system has realized it's not bad. It works. It doesn't take any extra time and it adds a level of security. Um system itself we've been using it for the best part of 18 months cuz we were on the original 300 garage trial
[01:06] effectively. >> [clears throat] >> But I have asked the DVSA um I've I've actually emailed two members of staff at the DVSA and asked them if we can actually have the photo system rolled out to the training test before it goes live on the proper system because one of the things that I do believe that you guys should have is access to practicing using it and seeing how good it actually is. So it will take away a lot of stress and a lot of the headaches and a lot of the a lot of people complaining basically um and it will stop you from doing that because you'll see how easy it is and how effective it is. Um I don't see that there is an issue
[01:38] with the photo system at all. It's a very smooth system, it works well. Test starts as you take the photo. Like I say, those people that are actually on it have been quite complimentary about it, but I do think that it should be part of the training test to allow you guys a chance to play with it before it goes live in your station. Um if you've got any thoughts on the photo test, whether you're using it, not using it, what you're, you know, if you think it's a good idea, bad idea, let us know. Um I personally think it's a great idea. I think it starts to take out those people who have been blatantly committing fraud, doing tests where they're not on site. Obviously, we call them ghost tests, but DVSA would
[02:12] call them a spurious test. Um but I do believe that it will help the scheme remove those individuals, or certainly help catch them. Um and take them out because ultimately those vehicles are going on the roads without a test, without meeting meeting the minimum standard that's required. And the things that you love the most, your families, your friends, your kids, or even yourselves, you're driving on those same roads. And if that vehicle hurts you or your family because somebody didn't test it correctly, how are you going to feel? So, I think that this photo scheme starts to make the risks more comparable
[02:46] and brings them down and allows us to actually catch these individuals that are doing MOT tests as such. What do you t
[transcript continues in field-notes/staging/ZLbmhgI2FFE.txt]

## 6. [vault] LTX Desktop local video generation
key: vault:2026-10-24:ltx-desktop-local-video-generation
url: https://www.instagram.com/p/DemKvEhCDwm/
meta: {"vault_status": "open", "kind": "tool", "subject": "handlytech 10 free AI video tools carousel", "date": "2026-10-24", "where": "TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: free per clip on the M5 for B-roll drafts; LTX-2.3 is only routed via fal today

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Listicle with a comment-FREE DM funnel; three tools new to us (LTX Desktop local, Viggle, Video2X), the rest already routed or generic Write-up: `TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md` Link: https://www.instagram.com/p/DemKvEhCDwm/

## 7. [hn] Google will pay people to use less electricity so its data centers can use more
key: hn:50215983
url: https://www.computerworld.com/article/4239858/google-will-pay-people-to-use-less-electricity-so-its-data-centers-can-use-more.html
discussion: https://news.ycombinator.com/item?id=50215983
meta: {"points": 55, "comments": 29, "created": "2026-10-23T22:03:40Z"}
query: car data

comment (benoau): > adjusting tens of thousands of smart thermostats at once, effectively moving their electricity usage to a time when there is less demand Somewhere amongst this was a great opportunity for reducing consumption of electricity from dirty sources, mass-optimizing millions of thermostats, car and electric bikes/etc charging, refrigerators, computer power settings etc to reduce emissions... but now it sounds like it should be illegal.
comment (Vaushite): (They'll still pay more for electricity, but less than if they hadn't taken the deal) Edit: why is this comment suddenly grounds for an auto shadowban??????
comment (BLKNSLVR): All these decades with little, slow action on climate change, and all it actually took was the seven largest companies in the world wanting more power than is commonly available and, yes, we can find ways of making the average household more efficient right away! It's a sad, but true, indictment about how scaled humanity works.

## 8. [github] appariciojunior/video-editor-skills: Skills that teach Claude Code to be a first-pass video editor in DaVinci Resolve: transcript cuts, vlog pacing, B-roll, music & SFX, clean captions, motion graphics, YouTube export. CC BY-NC 4.0 (no commercial use).
key: gh:appariciojunior/video-editor-skills
url: https://github.com/appariciojunior/video-editor-skills
meta: {"stars": 239, "created": "2026-10-23", "pushed": "2026-10-23", "language": null, "topics": ["claude-code", "claude-skills", "davinci-resolve", "remotion", "video-editing", "youtube"]}
query: youtube transcript pushed:>{since} stars:>20

# Video Editor Skills for Claude Code

Turn Claude Code into a **first-pass video editor** for your YouTube vlogs and classes in **DaVinci Resolve Studio**. You film and make the taste calls; Claude imports, cuts retakes and dead air, keeps your B-roll, scores the video, writes clean captions, adds brand motion graphics and helps you export.

These are **skills only**: the method, the numbers, the rules and the traps, learned on real edits. There is no code in this package. Claude reads the skills and builds the small scripts with you, for your setup.

## What's inside

| Skill | Teaches Claude |
|---|---|
| `video-editor-setup` | the workspace, safe key handling, your Resolve template, which scripts to build |
| `edit-video` | the one-command flow: ingest → cut → build in Resolve → report |
| `rough-cut` | what to keep: retakes, false starts, notes to the editor, punchlines |
| `vlog-pacing` | silence detection, pads, pause rules, room at scene edges, jump-cut zoom |
| `broll` | finding and watching B-roll, cutting it by action and story |
| `resolve-scripting` | what works in the Resolve API, what silently fails, what crashes it |
| `voice-and-audio` | loudness normalize, diagnosing a muffled voice, EQ recipe |
| `music-and-sound` | Epidemic Sound cues per section, ducking envelope, tasteful SFX |
| `captions` | clean, correct, one-line captions read before import |
| `motion-overlays` | a Remotion brand kit timed to your words, face- and caption-safe |
| `figma-roundtrip` | design the kit in Figma, keep code and boards in sync |
| `youtube-export` | Deliver settings for great quality without 25 GB files |

Plus `templates/config.example.json` (starting values) and `LEARNINGS.md`, the story of what went wrong and how it was fixed.

## Install

**As a plugin** (keeps the skills together):
```
/plugin install  
```
**Or copy the skills** into your project (`.claude/skills/`) or your user folder (`~/.claude/skills/`):
```
cp -R skills/* ~/.claude/skills/
```

## Use

1. Open Claude Code in an empty folder for your editing workspace.
2. Say: **"set up my video editor"**. Claude follows `video-editor-setup`, asks about your camera, Resolve project and brand, and builds the scripts with you.
3. Create `system/keys.env` yourself with one line, `SPEECH_TO_TEXT_API_KEY=your-key`. Claude never reads or prints it, and it must never be committed.
4. Drop a video in `raw video/`, open your Resolve project, say **"edit the new video"**.
5. Give feedback in plain words ("too choppy", "music louder on B-roll", "add captions", "graphics"). Claude adds every lesson to your `CLAUDE.md` so the next video starts smarter.

## You need
DaVinci Resolve **Studio** (external scripting), ffmpeg, Python 3.9+, a speech-to-text API with word timestamps. Optional: Epidemic Sound MCP, Figma MCP, Node + Remotion.

## Safety built in
Raw footage is never modified. In Resolve, Claude only **adds** (new timelines, new clips) and never touches your template or projects. Keys are never printed. Nothing is published without you.

## License
[CC BY-NC 4.0](LICENSE): free to use, share and adapt with credit. **Not for sale**: you may not sell these skills or a modified version, or use them in anything sold (paid courses, templates, products or services). For commercial use, ask the author.

## 9. [arxiv] Adaptive Skill Granularity for Coding Agents: Runtime Routing and Macro-to-Micro Recovery
key: arxiv:2610.31461
url: https://arxiv.org/abs/2610.31461
meta: {"published": "2026-10-22", "authors": ["Dingxuan Zhang", "Yanhui Jiang", "Jun Wang", "Hefeng Zhou"], "categories": ["cs.AI", "cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

Reusable skills allow large language model agents to package task-specific procedures, tool affordances, and execution guidance into modular units. Prior work has largely studied how agents retrieve, compose, or synthesize skills before execution. In coding agents, however, execution poses an additional runtime control problem: the same task may be solved through primitive tool calls, macro skills, or hybrid execution that starts with a macro and falls back to micro-level recovery. We introduce Adaptive Skill Granularity, a framework that treats skill granularity as an action-abstraction policy conditioned on task structure, execution state, and macro-skill failures. The system combines a feature-based granularity controller and a finite-state recovery executor. We evaluate the framework with a deterministic coding-agent protocol using verifier-defined success, total cost, and process metrics such as macro adoption, failure recovery, route match, and transition correctness. Results show that fixed macro execution is efficient when applicable but brittle under mismatch, while runtime routing and explicit macro-to-micro recovery improve robustness and recover controlled macro failures that fixed-granularity execution leaves unresolved. Our findings suggest that skill libraries for coding agents should be treated not only as retrievable resources, but also as controllable, verifiable, and recoverable execution abstractions.

## 10. [youtube] MOT Expert Assessor MOT Routine - UK MOT Tester Training #mottester #dvsa #mechanic #mottesting
key: yt:4LVa_w7Gg4M
url: https://www.youtube.com/watch?v=4LVa_w7Gg4M
meta: {"channel": "MOT Expert", "rank": 2}
query: MOT data analysis uk


[body unavailable: NoTranscriptFound]

## 11. [vault] Viggle motion transfer
key: vault:2026-10-24:viggle-motion-transfer
url: https://www.instagram.com/p/DemKvEhCDwm/
meta: {"vault_status": "open", "kind": "tool", "subject": "handlytech 10 free AI video tools carousel", "date": "2026-10-24", "where": "TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: compare with Kling Motion Control and Wan 2.2 Animate for the AI influencer track

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Listicle with a comment-FREE DM funnel; three tools new to us (LTX Desktop local, Viggle, Video2X), the rest already routed or generic Write-up: `TRITON-CORE/Research/links/2026-10-24-handlytech-free-ai-video-tools.md` Link: https://www.instagram.com/p/DemKvEhCDwm/

## 12. [hn] Show HN: agent-usage-guard – a Claude Code mod to protect your usage window
key: hn:50198936
url: https://github.com/rbartoli/agent-usage-guard
discussion: https://news.ycombinator.com/item?id=50198936
meta: {"points": 27, "comments": 12, "created": "2026-10-22T18:02:38Z"}
query: claude code

comment (Robin_Message): I was under the impression a compact resurrected the session anyway so it is not a good idea on a cold session. Is that true or is it actually cheaper?
comment (zzyyxx332211): After consuming my whole usage window in a few minutes multiple times, I realised I needed a hook to do some checks for me and prompt me before submitting when cache had expired and content is too big, so that it can suggest me to "compact then send". It can also prevent sub-agents from spawning when above 80% usage window. Control is handed over to the user. The first I built, based on hooks (run for 75 days), the biggest burst fell from 365 agent spawned to 27, and requests over 500k tokens of context from 14.5% to 0.6%. Lockouts still went up, because lots of parallel main sessions use up t
comment (plaguuuuuu): nobody is going to read that README

## 13. [github] devhims/youtube-caption-extractor: Extract YouTube captions, subtitles, auto-generated transcripts, and video metadata with a tiny TypeScript library
key: gh:devhims/youtube-caption-extractor
url: https://github.com/devhims/youtube-caption-extractor
meta: {"stars": 172, "created": "2023-05-04", "pushed": "2026-10-18", "language": "TypeScript", "topics": []}
query: youtube transcript pushed:>{since} stars:>20

youtube-caption-extractor 
    Turn public YouTube videos into clean, timestamped transcripts.  
   
    Extract YouTube captions, subtitles, auto-generated transcripts, and video metadata
    with a tiny TypeScript library: ~10.8 kB packed, ~31.1 kB unpacked.
   
   
     
       Need more YouTube data?  For new projects and AI agent workflows,
      we recommend  all-things-youtube ,
      our newer, more comprehensive YouTube package.
      It supports search, transcripts and captions, comments, video details,
      channels, and playlists, with built-in TypeScript types.
      See the  API documentation .
     
   
   
       
       
       
       
       
   
   
     Quickstart 
    ·  Live demo 
    ·  Sample app 
    ·  API 
    ·  Deployment notes 
   
 

---

## Why use it?

- **One-call transcript extraction** — `getSubtitles()` returns timestamped segments ready for search, summarization, indexing, RAG, slide ready research notes, or export.
- **Metadata included** — `getVideoDetails()` returns title, description, and captions in one response.
- **Manual + auto captions** — prefers exact language matches, then gracefully falls back to available tracks.
- **Tiny install** — ~10.8 kB packed on npm, with only two runtime dependencies.
- **Runtime-friendly** — uses global `fetch`, with an optional custom transport for retries, caching, regional routing, or proxies.
- **Production-aware sample** — includes a Next.js demo plus a token-protected Cloudflare Container API.

## Built for

- YouTube caption extraction, subtitle extraction, and timestamped transcript data.
- AI summaries, search indexes, RAG pipelines, and agent workflows that need clean video text.
- Slide ready notes, presentation research, and content workflows built from public YouTube videos.
- Lightweight video metadata enrichment without pulling in a large SDK.

```ts
import { getSubtitles } from 'youtube-caption-extractor';

const subtitles = await getSubtitles({ videoID: '7GeFt8suV8E', lang: 'en' });
// → [
//     { start: '1.12', dur: '4.56', text: 'This scraper can scrape almost anything' },
//     { start: '3.36', dur: '5.84', text: 'on the internet and you will be' },
//     { start: '5.68', dur: '6.64', text: 'surprised how easy it is to use it.' },
//     ...
//   ]
```

## Try it quickly

```sh
npm install youtube-caption-extractor
```

```ts
import { getVideoDetails } from 'youtube-caption-extractor';

const video = await getVideoDetails({
  videoID: '7GeFt8suV8E',
  lang: 'en',
});

console.log(video.title);
console.log(video.subtitles.map((s) => s.text).join('\n'));
```

Want to click around first? Try the hosted demo:
[youtube-caption-extractor.vercel.app](https://youtube-caption-extractor.vercel.app/).

Want a full app example? See [`sample/`](./sample), which includes:

- A polished Next.js UI
- Local API testing with your machine's network egress
- A Dockerized Hono API deployed through Cloudflare Containers
- A server-side token-protected proxy so the container API is not publicly open

## Installation

```sh
npm install youtube-caption-extractor
```

Requires **Node.js ≥ 18** when running on Node.js because the library uses the
global `fetch` API. It also works in Bun, Deno, Cloudflare Workers, and other
modern JavaScript runtimes that provide `fetch`. See
[Deployment notes](#deployment-notes) for tips on keeping calls reliable from
your runtime of choice.

## API

The library exports two functions and three types.

### `getSubtitles({ videoID

## 14. [youtube] How To SNIPE Pump Fun Memecoins & AVOID RUGS
key: yt:9Qhnc1B4ZhI
url: https://www.youtube.com/watch?v=9Qhnc1B4ZhI
meta: {"channel": "Sajad", "rank": 4, "duration_min": 17}
query: pump.fun sniper bot how it works

# How To SNIPE Pump Fun Memecoins & AVOID RUGS
# Sajad
# https://www.youtube.com/watch?v=9Qhnc1B4ZhI

[00:00] in this video I'm going to show you step by step exactly how to trade lower cap Market coins we're going to go into the trenches today you'll definitely need a pen and paper for this cuz I'm going to show you a lot of great tips here that will help you and obviously save the video if you need to watch it again we're going to look at pump fun launches and I'll show you all of the tools I use that helps me with these because there are so many scams and rugs on these new launch coins before I start thank you for all of the support I'm getting on my channel don't forget to hit the like button and subscribe for more tutorials like this and a quick warning about the
[00:32] comment section below for any large YouTuber make sure you only use any links or messages from the description section and pin comment section I'm mentioning this cuz I know a lot of you are new to crypto trading as well obviously there will be genuine comments uh below that but there will be some scam comments too like these ones where random coins are shilled and mentioned and I try my best to keep up with moderating these comments where it is very difficult because there are so many of them coming in especially on my most viewed videos so things like this where
[01:06] they're recommending random traders who help them um these are all scams so make sure you're not going into this section and messaging anybody who might be impersonating me that goes for my channel and any other large crypto YouTubers as well so just be very very careful right let's get straight to it so pump. fun if you're new to pump. fun this is where you get Fair launch meme coins and these are the ones that Trend nowadays and do really well uh on on that you see on Deck screen and you see people making a lot of money from but you have to understand how the mechanics works with pumped off fun launches if I go here to the left on this website and
[01:38] I click on creation time you can see here these are brand new launches and you can see they have very very low market caps and if people buy into them they'll start buying more and if I click on any of these I can see a chart I can see an area to trade here on the right bonding curve progress so it says here at the bottom as well graduate when this reaches 102,000 market cap so nowadays when it reaches k then it gets uh bonded and then potentially it gets new eyes and it could run a lot more as well because it comes quote unquote a real meme coin for your purposes you can trade on here and buy and sell and make
[02:12] money too it doesn't make any difference and then here we have something that's King of the Hill progress and you can see here it says 11% more on that in just a minute on the bottom right you've got holder distribution but again there's better uh tools you can use for this stuff now and then underneath here threads this is where people make comments now this becomes more important later generally for these new launches is not important but if the dev who created this coin buys and sells then how is the coin going to run who who's going to monitor the socials or pump the coin or kind of increase its attention
[02:45] on Twitter Etc so you need Community to do that and that's where you get sometimes a CTO Community takeover again more on that in just a minute let's just go back to the homepage first scroll up and we've got King of
[transcript continues in field-notes/staging/9Qhnc1B4ZhI.txt]
