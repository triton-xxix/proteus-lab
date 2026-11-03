# Harvest brief, 2026-11-03

14 items shortlisted from 361 candidates (267 dropped as already seen, 7 carry a vault verdict on the vendor).

## 1. [vault] HeyGen web app costs about a third of its API per minute and its free plan covers a first lip-sync
key: vault:2026-10-01:heygen-web-app-costs-about-a-third-of-its-api-per-minute-and
url: 
meta: {"vault_status": "intel", "kind": "tool", "subject": "AI video tool stack as of October 2026 (Veo, Nano Banana, Seedance, Kling, MiniMax H3, Wan, HeyGen, fal)", "date": "2026-10-01", "where": "TRITON-CORE/Systems/video-bootcamp/STACK.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Checked on vendor pages 1 Oct while building the video framework. We already hold enough to draft most work by API: Veo 3.1 and the Nano Banana image models on a Gemini key, ElevenLabs for voice and sound, HyperFrames for the edit. The course picks have aged: MiniMax H3 and Wan 3.0 now out-rank Kling 3.0 and Veo 3.1 for image to video, Nano Banana 2 out-ranks Pro at half the price, Gemini Omni cannot edit uploaded video from the UK, and Seedance refuses real faces, so a real person on screen is a HeyGen job. Job: choose a draft route and a final route for each video job (solved)

## 2. [hn] Could a modern chess engine on a Pentium have defeated Kasparov in 1996?
key: hn:50349276
url: https://nicholas.carlini.com/writing/2026/algorithmic-improvements-chess.html
discussion: https://news.ycombinator.com/item?id=50349276
meta: {"points": 428, "comments": 196, "created": "2026-11-03T07:56:21Z"}
query: chess engine

comment (glimshe): Very interesting. I don't play chess but like to observe others playing and talking about it on YouTube. I thought about something the other day... Modern chess sites run proprietary algorithms to detect cheating by modern engines. But would it be possible for an old engine, let's say from the 70s or 80s, running on modern hardware to deceive these algorithms? They wouldn't win every tournament but still have a respectable performance.
comment (emil-lp): This is very cool. But yes, totally unsurprising that a megahertz machine with 100MB+ available ram has >2500 ELO.
comment (bentt): Wonderful work! Just inspiring. I had a Pentium Pro 200 back in the day, to run 3DSMax 1.0 on Windows NT 3.5.

## 3. [github] andyhuo520/vibe-knowledge: Vibe 知识大赏：一个知识点 → 一条有旁白、每句有出处的精品知识短片（Claude Code skill · 44 套风格 · 代码逐帧成片）
key: gh:andyhuo520/vibe-knowledge
url: https://github.com/andyhuo520/vibe-knowledge
meta: {"stars": 412, "created": "2026-10-28", "pushed": "2026-10-28", "language": "JavaScript", "topics": ["chinese", "claude-code", "claude-skills", "explainer-video", "text-to-video", "threejs", "video-generation"]}
query: claude-code created:>{since} stars:>20

# vibe-knowledge · Vibe 知识大赏

**一个知识点 → 一条有旁白、每句有出处的精品知识短片。** 
Claude Code skill：选题 → 查证 → 写稿 → 配音 → 代码成片 → 1080p60 → 质检 → 发布包，全程在对话里完成。

[](LICENSE) [](skills/vibe-knowledge/SKILL.md) [](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)

[English](README.en.md) · [看样片](#看样片) · [风格库](#风格库44-套--8-个家族) · [听一听](#听一听默认音色与-bgm) · [Renoise](#renoise增强档的生成平台) · [安装](#安装)

 

 ↑ 风格快闪片节选。完整 42 秒版： style-flash-42s.mp4  

 

---

## 看样片

点封面播放（视频放在 [Release v1.0.0](https://github.com/andyhuo520/vibe-knowledge/releases/tag/v1.0.0)）。所有画面都由 Claude Opus 编排、代码逐帧渲染；标「增强」的镜头用 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) 生成配图和动态镜头，片中都标注「AI 示意」。

 
       如果你活在古代没有冰箱（古风版）   2:05 · 两难选择片 · 古风 · 增强标准档（Wan 3.0 动态镜头）        商鞅立木：搬一根木头赏五十金，你搬不搬？   2:32 · 两难选择片 · 古风 · 增强档   
       商鞅立木（基础档，0 积分）   2:32 · 同一份 film.js，代码插画版        商鞅立木 · 两档上下对比   2:32 · 基础档 vs 增强档，旁白和脚本完全一样   
       一张纸折多少次能到月球   1:10 · 猜谜概念片 · 深色数学 + 尺度穿越 · 增强标准档        什么是洗钱   1:31 · 痛点原理片 · 半调拼贴 · 增强轻档   
       如果你活在古代没有冰箱   3:12 · 猜谜概念片 · 星空光点 · 基础档 0 积分（同一选题的另一种讲法）        火箭怎么飞上天   1:46 · 猜谜概念片 · 蓝图专利图 · 增强标准档   
 

**风格样片集**（每套风格演同一段「商鞅立木」开场，方便横向比较）：

- [最早 7 套（古风、星空光点、暗金线描、水墨纸本、像素、字幕新闻、视觉调查）](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-01-core7.mp4)
- [剪辑与纪实](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-02-edit-doc.mp4)
- [补空白家族 8 套](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-03.mp4)
- [增强档：敦煌、青花、木刻、半调拼贴](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-04-enhanced.mp4)
- [第五批 8 套](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-05.mp4)
- [第六批 8 套](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-06.mp4)
- [增强档：长卷、铜版博物](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-07-enhanced.mp4)
- [田园像素](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-08-farm-pixel.mp4)
- [第九批 5 套](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-09.mp4)
- [手绘过程（手 + 笔画给你看）](https://github.com/andyhuo520/vibe-knowledge/releases/download/v1.0.0/styles-10-sketch.mp4)

## 风格库：44 套 · 8 个家族

 

| 家族 | 数量 | 风格（点开看 STYLE.md：配色、字体、镜头语言、适合的选题） |
|---|---|---|
| 东方 | 7 | [古风](skills/vibe-knowledge/styles/gufeng/STYLE.md)、[水墨纸本](skills/vibe-knowledge/styles/paper/STYLE.md)、[敦煌壁画](skills/vibe-knowledge/styles/dunhuang/STYLE.md)（增强）、[青花](skills/vibe-knowledge/styles/qinghua/STYLE.md)（增强）、[木刻](skills/vibe-knowledge/styles/woodcut/STYLE.md)（增强）、[留白极简](skills/vibe-knowledge/styles/minimal/STYLE.md)、[长卷](skills/vibe-knowledge/styles/scroll/STYLE.md)（增强） |
| 暗场概念 | 7 | [星空光点](skills/vibe-knowledge/styles/starfield/STYLE.md)、[暗金线描](skills/vibe-knowledge/styles/darkgold/STYLE.md)、[深色数学](skills/vibe-knowledge/styles/darkmath/STYLE.md)、[霓虹赛博](skills/vibe-knowledge/styles/neon/STYLE.md)、[发布会极简](skills/vibe-knowledge/styles/keynote/STYLE.md)、[极光](skills/vibe-knowledge/styles/aurora/STYLE.md)、[装饰艺术金线](skills/vibe-knowledge/styles/deco/STYLE.md) |
| 游戏 | 4 | [像素](skills/vibe-knowledge/styles/pixel/STYLE.md)、[RPG 对话框](skills/vibe-knowledge/styles/rpg/STYLE.md)、[卡牌对战](skills/vibe-knowledge/styles/cards/STYLE.md)、[田园像素](skills/vibe-knowledge/styles/farm/STYLE.md) |
| 剪辑与纪实 | 5 | [字幕新闻](skills/vibe-knowledge/styles/caption-news/STYLE.md)、[视觉调查](skills/vibe-knowledge/styles/investigation/STYLE.md)、[复古桌面](skills/vibe-knowledge/styles/desktop/STYLE.m

## 4. [arxiv] Reviso: Not All Visual Evidence Deserves Equal Attention in Video Captioning
key: arxiv:2611.03602
url: https://arxiv.org/abs/2611.03602
meta: {"published": "2026-11-02", "authors": ["Tengfei Liu", "Yang Shi", "Yuran Wang", "Yuqi Tang"], "categories": ["cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Multimodal large language models (MLLMs) can generate detailed video captions, yet they may overemphasize minor details while overlooking essential context and key events. We argue that not all visual evidence deserves equal attention, as the importance of visual information depends on the content of each video. Motivated by this observation, we propose Reviso, an agentic video captioning framework that learns what to observe and how to gather relevant visual evidence. From a low-frame-rate global preview, Reviso constructs a hierarchical Context--Focus--Points (CFP) observation plan that identifies the video context, prioritizes key aspects, and defines concrete observation targets and corresponding tools. Guided by this plan, Reviso performs goal-directed active perception by selectively revisiting temporal segments and combining tools for fine-grained inspection. It interprets the acquired evidence, updates its plan as needed, and integrates global and local information to generate the final caption. To learn this observation strategy, we develop a verification-guided pipeline that constructs high-quality training trajectories through factual verification and teacher-guided refinement. We further train Reviso using Group Relative Policy Optimization (GRPO), incorporating a key-fact reward for caption quality, a Plan Alignment Reward (PAR) for identifying important observation targets, and an Unproductive Tool-Call Penalty (UTCP) that adjusts observation-cost penalties based on caption quality. Experiments across four video captioning benchmarks show that Reviso outperforms the evaluated open-source baselines, while its generated captions better support downstream video question answering. These findings highlight the effectiveness and potential of priority-guided active observation for video captioning.

## 5. [youtube] Ranking luxury car brands by depreciation 🚘🫪
key: yt:wX4qr3AQo7k
url: https://www.youtube.com/watch?v=wX4qr3AQo7k
meta: {"channel": "Chad Staples", "rank": 3, "duration_min": 0}
query: car depreciation data analysis

# Ranking luxury car brands by depreciation 🚘🫪
# Chad Staples
# https://www.youtube.com/watch?v=wX4qr3AQo7k

[00:00] Porsche 911 >> S >> Lexus >> S >> Mercedes G-Class >> Ooh, B. >> Chevy Corvette >> B >> Cadillac Escalade or Lincoln Navigator >> B >> BMW 7 Series >> Uh, C. >> Range Rover >> D >> Tesla Model S >> C >> Infiniti QX80 >> D

## 6. [vault] Speed-to-lead workflow chain and themed ad group keyword method from the call recordings
key: vault:2026-10-01:speed-to-lead-workflow-chain-and-themed-ad-group-keyword-met
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "Automatable Free (Skool, Jono Catliff), free tier", "date": "2026-10-01", "where": "TRITON-CORE/Education/Courses/automatable-free/DIGEST.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Joined free and extracted 148 lessons with 195 blueprint attachments. It is a sampler for a paid community: each mini-course gives one to three lessons. Best free material is two call recordings holding a complete speed-to-lead sales workflow and a city by service Google Ads keyword method. Several lead-sourcing blueprints rely on scraping plus cold calls, texts or email that need consent in the UK, and the review gating it teaches conflicts with platform and regulator guidance.

## 7. [hn] OpenAI seems to be silently re-enabling model training on Codex chats
key: hn:50352757
url: https://news.ycombinator.com/item?id=50352757
discussion: https://news.ycombinator.com/item?id=50352757
meta: {"points": 416, "comments": 132, "created": "2026-11-03T14:53:41Z"}
query: claude code

My company is pretty paranoid about leaking IP to the frontier labs through prompts, so we've all been diligent about disabling data sharing in Codex/Claude Code/etc. But yesterday my coworkers and I noticed that the setting had been silently reenabled in Codex. None of us knowingly opted back in. You can check your settings here: https://chatgpt.com/settings/data-controls. Look for "Improve the model for everyone". Curious if this is an isolated issue or something more widespread. EDIT: looks like this has been noted before https://news.ycombinator.com/item?id=49643556 EDIT: apparently you can also turn off data sharing here: https://privacy.openai.com/policies?modal=take-control
comment (spwa4): OpenAI is also now hiding your usage. Not accessible anymore in the menu, and /usage in the codex app now also gives a lot of stats, but the one stat you do want to know, how much limit left, is no longer there. I'm guessing another big usage reduction is coming soon.
comment (monster_truck): If your company actually cared about this they would be running their own inference instead of leaving fate to a couple of checkboxes.
comment (CEOatMindfries): May be the coding agents should build a layer when they don't leak any IP, treat them like environment variables, which must be handled deterministically.

## 8. [github] kar2phi/video-lens: video-lens is a coding agent skill that fetches a YouTube transcript and generates a structured HTML report: executive summary, key points, analysis, takeaway, timestamped topic outline, and an embedded in-page player. No API keys, no external services beyond the coding agent itself.
key: gh:kar2phi/video-lens
url: https://github.com/kar2phi/video-lens
meta: {"stars": 121, "created": "2026-03-08", "pushed": "2026-10-29", "language": "Python", "topics": ["agent", "skills", "transcription", "youtube"]}
query: youtube transcript pushed:>{since} stars:>20

# video-lens

**Turn any YouTube video into a polished research report.**

video-lens is a coding agent skill that fetches a YouTube transcript and generates a structured HTML report — executive summary, takeaway, key points with analysis, timestamped topic outline, and an embedded in-page player.

 

---

## What you get

- **Executive summary** — 3–5 sentence TL;DR overview
- **Takeaway** — the single most important insight (1–3 sentences)
- **Key points** — bulleted, scannable insights with supporting detail
- **Timestamped outline** — click topics to expand summaries; click timestamps to jump the player
- **In-page YouTube player** — watch while reading; auto-highlights the current section
- **Local transcription fallback** — when captions are unavailable, transcribe audio locally with Whisper
- **Keyboard shortcuts** — playback speed, layout resize (S/M/L), navigation, and more (`?` for help)
- **Markdown export** — copy the full report as Markdown in one click
- **Dark mode** — auto-detects system preference; remembered across sessions
- **Video gallery** — browse, search, and filter all your saved reports by title, channel, tag, or keyword; shows thumbnails, summaries, and tags at a glance
- **Recommendations** — `video-lens-recs` suggests what to watch next on your topics, from your channels and beyond, with a one-line reason each, skipping what you already watched or summarised

---

## Requirements

| Tool                                             | Purpose                                                    |
| ------------------------------------------------ | ---------------------------------------------------------- |
| A supported coding agent                         | Runs the skill (see [Supported Agents](#supported-agents)) |
| Python 3                                         | Runs the helper scripts                                    |
| `youtube-transcript-api`                         | Fetches YouTube captions/subtitles                         |
| `yt-dlp` (>=2026.8.19)                           | Fetches metadata and downloads audio for local transcription |
| **Optional:** [Raycast](https://www.raycast.com) | Trigger from anywhere via hotkey (macOS)                   |
| **Optional:** [Task](https://taskfile.dev)       | Install/dev commands alias (`brew install go-task`)        |
| **Optional:** [Deno](https://deno.com)           | Used by yt-dlp only for edge-case extractors (`brew install deno`) |
| **Optional:** `mlx-whisper` + `ffmpeg`           | Local Whisper fallback for videos without captions (Apple Silicon) |

> **Note:** video-lens first tries YouTube captions/subtitles. If captions are missing or blocked, it can fall back to local Whisper transcription when the optional local dependencies are installed (Apple Silicon only). YouTube Shorts are not supported.
>
> **Platforms:** macOS and Linux are supported. Windows is best-effort — fixes are welcome, but it is not tested.

---

## Supported Agents

video-lens uses the universal [SKILL.md](https://agents.md/) format — any agent that supports it can run this skill.

[](https://skills.sh/kar2phi/video-lens)

---

## Install

### Option A — skills CLI (recommended)

```bash
npx skills add kar2phi/video-lens
pip install youtube-transcript-api 'yt-dlp>=2026.8.19'

# Optional: local transcription fallback on Apple Silicon
pip install mlx-whisper
brew install ffmpeg

brew install deno  # optional; only needed if yt-dlp fails on certain videos
```

Then use `

## 9. [arxiv] DiabAgent: Toward Agentic Physiological Control
key: arxiv:2611.03601
url: https://arxiv.org/abs/2611.03601
meta: {"published": "2026-11-02", "authors": ["Chengxi Li", "Shaoxuan Li", "Deyao Hong", "Qingle Liu"], "categories": ["cs.AI", "cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

As pretraining scales, medical language models have advanced rapidly in clinical question answering. Their ability to achieve effective physiological control through sustained intervention still lacks systematic quantitative evaluation. Type 1 diabetes provides a concrete setting: impaired insulin secretion creates dependence on exogenous insulin, with dosing continually adjusted using information about meals, exercise, illness, and glucose measurements. We introduce DiabAgent, a research suite for agentic physiological control comprising the Agentic Physiological Control (APC) framework, the DiabetSim simulator, and the SweetBench benchmark. APC controls glucose through medical-device tools, using ongoing observations to infer individual states, accumulate personal experience, and choose treatment actions. We build DiabetSim to simulate different patients, events, and device conditions for scalable virtual testing and training. Using DiabetSim, we construct SweetBench by instantiating 32 scenario designs as 212 glucose-control tasks. With Claude Opus 5.5 and a fixed decision interval of one hour, APC achieves a COGI of 73.5, compared with 71.2 for the open-source closed-loop baseline OpenAPS. Ablations further show that individual adaptation and contextual information improve glucose control. Combining high-frequency rule-based control with lower-frequency agent decisions shows potential for balancing control performance and computational cost. Our work provides a framework, simulator, and evaluation foundation for agents to participate in human physiological control.

## 10. [youtube] (untitled) suAAJYkVz5M
key: yt:suAAJYkVz5M
url: https://www.youtube.com/watch?v=suAAJYkVz5M
meta: {"channel": null, "rank": 4, "duration_min": 1}
query: car depreciation data analysis

# (untitled) suAAJYkVz5M
# None
# https://www.youtube.com/watch?v=suAAJYkVz5M

[00:00] Try to guess the price of the car you're looking at right now. Most people would say at least a h 100red grand, but nope. This is the Porsche Panameira 970. And today, you can actually find one for under $20,000. And if you think that's crazy, just wait. The last car on this list will honestly shock you because it doesn't stop there. The Mercedes-Benz S550 W221 used to cost over $100,000 new. It was the go-to luxury ride for celebrities and CEOs, but now you can pick up one for around the same price as
[00:33] a Corolla. Then we've got the Chrysler 300C, also called the Baby Bentley. From a distance, people confuse it for a $9,000 Bentley Continental, but in reality, they just go for 6K to 10K. Now, let's step into exotic territory. The Maserati Gran Turismo with its Ferrari built 4.7 liter V8 looks and sounds like a $150,000 supercar, but thanks to depreciation, you can grab one for as low as 25K to 30K. And finally, the Azen Martin V8 Vantage. A proper James Bond car that
[01:08] was well over $120,000 when new, but today clean ones sell for under 40,000. All of these cars look like they belong in a millionaire's garage, but they're stupid cheap

## 11. [vault] Voice prompt rules: times as words, spelled-out emails, spoken delay to cover tool latency
key: vault:2026-10-01:voice-prompt-rules-times-as-words-spelled-out-emails-spoken-
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "Brendans AI Community (Skool, Brendan Jowett), free tier, plus Review Harvest (archived)", "date": "2026-10-01", "where": "TRITON-CORE/Education/Courses/brendans-ai-community/DIGEST.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Joined free and extracted 104 lessons. It is a funnel: 93 YouTube links, 33 lessons gated to a paid tier including every Claude Code lesson. Usable free material is about a dozen full voice-agent prompts and Make and Retell JSON files. Inbound AI receptionist is the lawful voice lane in the UK; outbound AI dialling of scraped lists is not. Review Harvest was archived by its owner and holds nothing beyond testimonials.

## 12. [hn] Gitbook Breached
key: hn:50354336
url: https://news.ycombinator.com/item?id=50354336
discussion: https://news.ycombinator.com/item?id=50354336
meta: {"points": 139, "comments": 31, "created": "2026-11-03T16:45:49Z"}
query: mcp server

We opened a ticket with support about Gitbook availability issues and got this in reply. We have yet to see any official customer communication or breach notification. Apologies for the formatting, did the best I could as it's a mobile paste. Update: GitBook security incident update Hey <$name>, The GitBook app, the GitBook API, and published docs are available again. A few services may still be degraded as we finish restoring everything to full performance. *What happened* GitBook has been the target of a sophisticated, highly targeted attack using AI agents. At 19:00 CET, November 2, the attacker gained unauthorized access to some of our infrastructure credentials. We detected the attack immediately and acted swiftly to block further impact. To make sure our infrastructure was fully secure, we then took the GitBook app and authenticated docs sites offline. We kept publicly published content live for as long as possible, using cached data. *What we did immediately* * Blocked the attacker and closed the vulnerabilities involved * Replaced every credential and secret across our infrastructure * Brought services back only once we were confident they were secure * Invalidated every customer’s API tokens on our platform *Your data* Our investigation shows that the attacker may have accessed the following: * Git Sync secrets. * GitBook API tokens. * Third-party API tokens used to connect external tools to GitBook. * Questions asked to GitBook Assistant by your site visitors. At th
comment (punchmesan): Oof that formatting is rougher than I thought. Will try to clean it up after I'm done reconfiguring gitbook...
comment (philipwhiuk): This is the public disclosure: https://www.gitbookstatus.com/incidents/01M6FXDDGQRWHMYYWXY2... Note that the summary at the top of https://www.gitbookstatus.com at time of writing does not mention the unauthorized access and the incident details does not mention the contents disclosed above.
comment (petecooper): https://www.gitbook.com/status/security-incident-2026-11-03

## 13. [github] guimatheus92/mcp-video-analyzer: MCP server that turns any video — YouTube, Instagram, TikTok, Loom, X, Vimeo, direct URLs, local files — into transcripts, key frames, OCR text, and metadata for AI agents.
key: gh:guimatheus92/mcp-video-analyzer
url: https://github.com/guimatheus92/mcp-video-analyzer
meta: {"stars": 110, "created": "2026-03-09", "pushed": "2026-11-02", "language": "TypeScript", "topics": ["ai", "claude", "frames", "instagram", "loom", "mcp", "mcp-server", "model-context-protocol"]}
query: youtube transcript pushed:>{since} stars:>20

mcp-video-analyzer 

  Turn any video — YouTube, Instagram, TikTok, Loom, X, Vimeo, direct links, local files — into transcripts, key frames, OCR text, and metadata for AI agents.  

 
     
     
     
     
 

 
     
 

No existing video MCP combines **transcripts + visual frames + metadata** in one tool. This one does — across Loom, the major yt-dlp platforms (YouTube/Vimeo/TikTok/Instagram/X/Twitch/Dailymotion/Facebook), direct video URLs, and local files.

> **Want a full pipeline, not just a tool?** [social-knowledge-base](https://github.com/guimatheus92/social-knowledge-base) is built on top of this server — it downloads whole Instagram creator accounts (reels, stories, highlights), transcribes them, and turns the result into a searchable, RAG-queryable knowledge base with AI-generated notes. Use this MCP when you want per-video analysis inside an agent; use social-knowledge-base when you want to archive and query an entire account.

## Installation

### Prerequisites

- **Node.js 22.12+** — required to run the server via `npx`
- **yt-dlp** — **required** for YouTube/Vimeo/TikTok/Instagram/X/Twitch/Dailymotion/Facebook URLs; optional for everything else (improves Loom download quality). Install with `pip install yt-dlp`
- **Chrome/Chromium** (optional) — fallback for frame extraction if yt-dlp is unavailable

> Without yt-dlp or Chrome, direct URLs and local files still get frames — the bundled `ffmpeg-static` does the extraction, and Loom falls back to its own CDN download. Platform URLs (YouTube etc.) degrade to a clear "install yt-dlp" warning. Transcripts, metadata, and comments never require either.

There are three ways in: the **`/video` plugin** (Claude Code — slash command + MCP server auto-configured), a plain **MCP server** config (any MCP client), or the **portable skill + CLI** (Codex, Cursor, Copilot, and any agent with a shell — no MCP required).

### Claude Code — `/video` plugin (recommended)

```
/plugin marketplace add guimatheus92/mcp-video-analyzer
/plugin install video@mcp-video-analyzer
```

This adds the `/video` slash command **and** auto-registers the MCP server — no `claude mcp add` needed:

```
/video https://youtu.be/jNQXAC9IVRw what happens at 0:10?
/video ~/Movies/screen-recording.mp4 when does the UI break?
```

### Other agents — Codex, Cursor, Copilot, Gemini CLI, …

```bash
npx skills add guimatheus92/mcp-video-analyzer
```

Installs the `video` skill ([Agent Skills](https://github.com/vercel-labs/skills) format) into every agent detected on your machine. Agents without the MCP server configured fall back to the bundled [CLI](#cli-one-shot-no-mcp-client) automatically — zero configuration.

### Claude Code (MCP only)

```bash
claude mcp add video-analyzer -- npx mcp-video-analyzer@latest
```

Then restart Claude Code or start a new conversation.

### VS Code / Cursor

Add to your MCP settings file:

- **VS Code**: `File → Preferences → Settings → search "MCP"` or edit `~/.vscode/mcp.json` / `%APPDATA%\Code\User\mcp.json` (Windows)
- **Cursor**: `Settings → MCP Servers → Add`

```json
{
  "servers": {
    "mcp-video-analyzer": {
      "type": "stdio",
      "command": "npx",
      "args": ["mcp-video-analyzer@latest"]
    }
  }
}
```

Then reload the window (`Ctrl+Shift+P` → "Developer: Reload Window").

### Claude Desktop

Add to your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config

## 14. [hn] Show HN: HackerTV – HN's most-recommended Youtube videos as 24/7 TV channels
key: hn:50346755
url: https://hackertv.org
discussion: https://news.ycombinator.com/item?id=50346755
meta: {"points": 108, "comments": 26, "created": "2026-11-03T01:18:09Z"}
query: claude code

I saw HackerTube ( https://news.ycombinator.com/item?id=50319510 ) a few days ago, the YouTube videos HN keeps recommending, pulled from 19 years of comments. It made me want to flip through them instead of picking, so I built a TV for it. I have Algo fatigue. Each topic area is a channel (DEVTV, SOLDER, RETRO, ORBIT, ...), plus HN Prime (the top 400), a music channel, and Late Night on ch 99, which only broadcasts 11pm-5am your local time and shows color bars otherwise. Similar to HackerTube it was built with Claude Code in a few hours. All credit for the data goes to HackerTube. Happy to hear channel ideas.
comment (smokel): Is someone working on HackerTldr? Three sentences that describe the target page would save me a lot of time. Edit: HackerTV looks great, well worth the click :)
comment (iAMkenough): Now we need HackerRadio to run in the background.
comment (thefourthchime): Hah, nice
