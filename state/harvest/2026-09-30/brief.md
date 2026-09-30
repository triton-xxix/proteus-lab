# Harvest brief, 2026-09-30

14 items shortlisted from 145 candidates (23 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] Learning crypto research from a source with an independently verifiable track record
key: vault:2026-09-26:learning-crypto-research-from-a-source-with-an-independently
url: https://cryptonary.com/landing-100x-chaser
meta: {"vault_status": "open", "kind": "service", "subject": "Cryptonary 100x Chaser", "date": "2026-09-26", "where": "TRITON-CORE/Research/links/2026-09-26-cryptonary-100x-chaser.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Nobody in the vault has named such a source yet; the test is audited entry and exit pairs, not peak figures

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) No. The agent read their JavaScript bundles rather than the page and found that 100x Chaser is not a product, it is a customer PERSONA: one landing template with eight psychographic variants (100x-chaser, boomer-near-retirement, burnt-out-9-5-worker, college-student, complete-beginner, passive-income, portfolio-builder, side-hustle-seeker, plus landing-burned and landing-skeptic), all 997 dollars, all sharing the page title Make Your First Million in Crypto in 2026. The 100x page promises asymmetric plays while the boomer page, from the same file, warns never to risk what you cannot afford to lose, and the team section rewrites itself per persona. Hard facts: CRYPTONARY LIMITED 10958868 was dissolved 16 March 2021 so the billing entity is unidentified; Trustpilot 4.2 across 1,679 reviews but one-stars cluster on inability to cancel, AURA memecoin losses and months of support silence, and Trustpilot flags the profile for high-risk investments; every performance figure is a PEAK (WIF +114,509 percent) with no audited record or entry-exit pairs, and the figures drift between their own bundles. Compliance: no FCA risk warning, no cooling-off, no capital-at-risk line, no UK disclaimer, no geoblock, which the October 2023 financial promotions regime requires for cryptoasset promotions to UK consumers. Job: Learn crypto research from a source whose track record is independently verifiable rather than measured at peak prices (still open) Write-up: `TRITON-CORE/Research/links/2026-09-26-cryptonary-100x-chaser.md` Link: https://cryptonary.com/landing-100x-chaser

## 2. [hn] Launch HN: Magnitude (YC S25) – Self-optimizing inference engine for agents
key: hn:49911995
url: https://github.com/magnitudedev/magnitude
discussion: https://news.ycombinator.com/item?id=49911995
meta: {"points": 110, "comments": 45, "created": "2026-09-30T17:37:40Z"}
query: local llm benchmark

Hey HN, Anders and Tom here. We're building Magnitude, an inference engine for agents that optimizes itself to run as fast as possible on your hardware. It works on Mac, Linux, and Windows on any hardware and is up to 2x faster than llama.cpp. We're both software engineers and previously built an open source browser agent to 4k+ GH stars and 100k+ downloads. We increasingly wanted to run it on local models, but found that no inference engine worked for our use case. Inference engines today all make a performance tradeoff. They are either: - Built for batched inference on datacenter hardware at the cost of single-session performance (vLLM, SGLang) - Designed for broad compatibility instead of optimizing for specific hardware (llama.cpp, Ollama) - Specialized for specific hardware or models but lacking engine completeness (oMLX, ds4) Plus none of them are designed for running agents locally. Sessions are long, several often run at once, and you still want to use your computer for other things. Magnitude is built for maximum performance on your hardware and running local agents: - On-device compilation and tuning: Kernels are written with flexible parameters that are tuned on your actual device before the model runs. This gives you broad hardware compatibility with the same performance ceiling as hardware-specific kernels. - Focus on best architectures: We write our tunable, highly efficient kernels for the most popular open-weights families. This allows us to achieve and surpas
comment (p-e-w): What is the business model?
comment (amirhesham): Oh this is so cool. Curious about the business model, too.
comment (nateb2022): Any source on the benchmarks/methodology besides the image? There's a ton of variance possible in llama.cpp's performance depending on how it was configured. I'd also like to see benchmarks against MLX.

## 3. [github] Louis-CFM/coucou: A tiny friend that lives in your notch (macOS) or at the top of your screen (Windows) and keeps an eye on your Claude Code sessions.
key: gh:louis-cfm/coucou
url: https://github.com/Louis-CFM/coucou
meta: {"stars": 1099, "created": "2026-09-27", "pushed": "2026-09-30", "language": "Swift", "topics": ["ai-agents", "anthropic", "claude", "claude-code", "dynamic-island", "macos", "macos-app", "menubar-app"]}
query: claude-code created:>{since} stars:>20

# Coucou

**A tiny friend that lives in your MacBook's notch — or at the top of your screen on Windows — and keeps an eye on your Claude Code sessions.**

Approve permissions, watch your agents work, drop a file, chat with Claude — all without leaving what you're doing.

 

 

---

## Why

Some studios showed off gorgeous notch companions… and never let anyone use them.
**Coucou is the open version.** Every line of code, every animation, every sound — free to use, read, fork and remix.

Meet **Mochi**: a soft little squircle with big eyes that pops out of your notch, waves hello, follows your cursor with its eyes, gets annoyed when you poke it (and dizzy if you insist), and tells you the moment Claude Code needs you.

## Features

- 🤖 **Claude Code, live** — see every session in your notch: what it reads, edits and runs, step by step. Finished? Mochi does a happy little jump.
- ✅ **Approve from the notch** — Claude Code permission requests show up with **Allow / Deny**. One click, back to work.
- 🧑‍💻 **Jump to the right terminal** — open the exact terminal window of a session *(macOS)*.
- 💬 **Ask Claude anything** — built-in chat, straight from the notch.
- 📎 **Drop a file on the notch** — Mochi turns into a box and swallows it, then ask a question about it or send it by email *(email: macOS, Mail.app)*.
- 🪟 **Drag Mochi onto any window** — attach that window as context for Claude *(macOS)*.
- 🔌 **Integrations** — Stripe payments, n8n workflows, GitHub, Vercel deployments, Resend emails, Notion, Cal.com. Each one gets its own little colored Mochi.
- 🎭 **A real character** — idle breathing, blinks, eyes on a sphere that follow your mouse, emotes, 28 handcrafted sounds, a greeting on launch.
- 🫥 **Invisible when idle** — hides away when nothing is running, peeks out when you hover the notch (the top edge of the screen on Windows).
- 🔒 **Private by design** — no telemetry, no account. Keys live in your macOS Keychain or Windows Credential Manager. The app only talks to the services you plug in.

 
 
   
   
 
 
   
   
 
 

## Install

### Download for macOS

1. Grab the latest `Coucou.zip` from [Releases](https://github.com/Louis-CFM/coucou/releases).
2. Unzip and move **Coucou.app** to `/Applications`.
3. Launch. This build isn't notarized by Apple yet, so the first time macOS says it can't verify the developer: open **System Settings → Privacy & Security**, scroll down and click **Open Anyway** (only once).

### Windows

The Windows installer is **temporarily unavailable**. Microsoft Defender wrongly
flags the unsigned installer as malware; a false-positive report is under review
at Microsoft and the installer will come back once it is cleared and signed.
Until then you can [build it from source](#build-from-source).

There is no notch on a PC, so the island slides out of the top edge of the screen
instead of hiding inside one. See [`windows/README.md`](windows/README.md) for the
rest of the differences.

### Build from source

**macOS** — requirements: macOS 15+, Xcode 16+, [XcodeGen](https://github.com/yonaskolb/XcodeGen).

```bash
brew install xcodegen
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/NotchBuddy
xcodegen
open NotchBuddy.xcodeproj   # then ⌘R
```

**Windows** — requirements: [Rust](https://rustup.rs), Node 20+, MSVC build tools.

```powershell
git clone https://github.com/Louis-CFM/coucou.git
cd coucou/windows
npm install
npm run pack                # installer lands in windows/release/
```

## Setup

Click 

## 4. [arxiv] MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation
key: arxiv:2609.38078
url: https://arxiv.org/abs/2609.38078
meta: {"published": "2026-09-29", "authors": ["Bingxuan Li", "Siqi Song", "Yizhuo Wu", "Jiarui Yao"], "categories": ["cs.RO"]}
query: all:"language model" AND all:agent AND all:tool

Vision-language-action (VLA) models have advanced robotic manipulation, but their zero-shot generalization in new tasks and environments remains limited, and their reliance on specialized training keeps them from benefiting directly from rapidly advancing general-purpose vision-language models (VLMs). In parallel, recent agentic robotic systems leverage VLMs for high-level reasoning or coding agents for robot control, but often depend on extensive external models and tools, introducing additional complexity and cost. This motivates us to ask: Can a general-purpose VLM itself operate a robot more like the human teleoperator by reasoning directly from observations, issuing actions, and continuously adapting to execution feedback, without relying on external models such as learned action experts, coding agents or grounding tools like SAM3? In this work, we introduce MotorMind, a robot manipulation harness that connects VLM-proposed mid-level actions to deterministic robot control and feedback, with asynchronous monitoring and background memory updates. Without task-specific policy training, coding agents, or additional grounding tools such as SAM3, MotorMind achieves 66.7% success on the base LIBERO-PRO suites and 53.8% under perturbations, compared with at most 13.3% and 19.2%, respectively, for the prior zero-shot methods we evaluate. The same interface reaches 95% average success on a real xArm6 robot across direct manipulation and human-perturbation settings. Replacing the backbone with a stronger VLM further improves performance, while the remaining failures - primarily due to visual grounding, embodied reasoning, and action knowledge - decrease as VLM capability improves. These results show that a general-purpose VLM, when equipped with an appropriate mid-level action representation and asynchronous execution harness, can perform effective zero-shot robotic manipulation.

## 5. [youtube] day in the life of a wfh data analyst.
key: yt:RC30UibhowE
url: https://www.youtube.com/watch?v=RC30UibhowE
meta: {"channel": "Charlotte Chaze | Break Into Tech", "rank": 2}
query: MOT data analysis uk


[body unavailable: TranscriptsDisabled]

## 6. [vault] Consistent AI character content with clear AI disclosure
key: vault:2026-09-26:consistent-ai-character-content-with-clear-ai-disclosure
url: https://www.instagram.com/p/Ddr0Ds3MsI5/
meta: {"vault_status": "open", "kind": "service", "subject": "EasyInfluencers.ai", "date": "2026-09-26", "where": "TRITON-CORE/Research/links/2026-09-26-easyinfluencers.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: The character may entertain; it must not recommend products while appearing to be an ordinary person

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) No, and nothing new: the fourth AI-influencer vendor this week, chasing a job already open from Eromify with the DMCC constraint attached. The promoting account has 161 followers and zero posts, so the reel is a paid ad rather than organic traction. The site carries no pricing, no company, no founder and no country, only a copyright line. Two things decide it: it sells 'none of these people exist' as the headline feature, and it answers detection concerns by promising consistent appearances across all content, so the product is an undetectable fake person. That is the second vendor this week whose selling point is evading platform detection, after Butter and its GeeLark antidetect cloud phones; different market, identical shape, the feature is the thing the platform is trying to stop. No disclosure language, no AI labelling, no platform-terms mention anywhere, which is precisely where DMCC 2024 Schedule 20 practice 25 bites, a trader posing as a consumer, banned with no consumer-harm test. Job: Produce consistent AI character content with disclosure that survives DMCC practice 25 and platform inauthenticity rules (still open) Write-up: `TRITON-CORE/Research/links/2026-09-26-easyinfluencers.md` Link: https://www.instagram.com/p/Ddr0Ds3MsI5/

## 7. [hn] Show HN: A working 3D model of an Enigma machine
key: hn:49896757
url: https://enigma.design
discussion: https://news.ycombinator.com/item?id=49896757
meta: {"points": 93, "comments": 34, "created": "2026-09-29T17:15:56Z"}
query: car data

I watched the excellent Veritasium video [1] on the Enigma machine, and watched the full animation by Jared Owen [2], but was still a bit confused on how the inner mechanics of an Enigma machine work. I used Astra to build out the inner components through a combination of reference images, writing out hundreds of extremely detailed prompts, and building my own inspection tools to ensure that every part is sized and positioned in a historically accurate way. It's still a work in progress, but would love any feedback on the experience so far! 1. https://www.youtube.com/watch?v=JsBZOcqZerk 2. https://www.youtube.com/watch?v=ybkkiGtJmkM
comment (psolidgold): Seems pretty cool but unfortunately the poor performance on mobile (Chrome 154 and Android 17) makes it unusable for me. I'll have to check it out on desktop.
comment (anonydsfsfs): I love the presentation! Would you mind sharing the source code?
comment (ted_dunning): It would be nice to be able to back up in the sequence. There were a few times where I realized I had not fully understood a previous step and would have like to be able to review some previous steps. Otherwise this is completely excellent!

## 8. [github] rehan-remade/universal-modder: Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own: recon, reverse engineering, fal-generated art/3D/audio, in-game testing, showcase videos.
key: gh:rehan-remade/universal-modder
url: https://github.com/rehan-remade/universal-modder
meta: {"stars": 763, "created": "2026-09-30", "pushed": "2026-09-30", "language": "Python", "topics": ["age-of-empires", "claude-code", "claude-code-plugin", "fal", "game-assets", "game-modding", "mcp", "modding"]}
query: claude-code created:>{since} stars:>20

Skills, tools and the fal MCP that let Claude Code mod almost any PC game you own.  
  It finds the game, works out the engine and the modding route, reads the real code, builds the mod, 
  generates art, 3D and sound with  fal , tests it in the running game, and cuts the showcase video.
 

 
     
     
     
 

 
   
 

## Install

**As a Claude Code plugin** (recommended):
```
/plugin marketplace add rehan-remade/universal-modder
/plugin install universal-modder@universal-modder
```

**Or clone it and run Claude inside it** (works with Codex/Cursor via `AGENTS.md` too):
```bash
git clone https://github.com/rehan-remade/universal-modder && cd universal-modder && claude
```

Then give it a [fal API key](https://fal.ai/dashboard/keys) for assets. It powers both the bundled fal MCP
server and the `um fal` CLI:
```bash
export FAL_KEY=...
```
You also need Python 3.10+ and ffmpeg. `uv` is recommended; the CLI sets up its own env with it. Blender is
needed for 3D → sprite renders. Windows games are driven natively or from WSL.

## Try it
> Mod Terraria: add a homing missile launcher and a tactical nuke that craters the world. Make the sprites with fal.

> Make a new civilization for Age of Empires II with a unique unit rendered from 3D.

> I own Skyrim SE. What would it take to put a Minecraft-style block-building mode in it?

> What engine is `C:\Games\Foo`, and how do people mod it?

Claude starts with the **mod-any-game** skill and runs the same loop every time: recon, pick a route, set up a
safe lab (saves backed up), read the actual code, build one working slice, generate assets, verify in the
real game, record, then package.

## What's inside

**Skills** (`skills/`)

| Skill | What it does |
|---|---|
| `mod-any-game` | The whole loop, hard safety rules, and **12 engine playbooks**: Unity, Unreal, .NET/XNA (Terraria, Stardew, Celeste), Godot, Source 1/2, Bethesda, Minecraft, AoE2/Genie, RE Engine/FromSoft/GTA/Cyberpunk/BG3, native C++, indie engines (GameMaker, RPG Maker, Ren'Py, Paradox, Doom, HTML5, LÖVE, Java), retro decomps |
| `game-recon` | Which engine and version, managed or native, anti-cheat, loaders, save folders, community route → `MODDING_PLAN.md` |
| `reverse-engineering` | ILSpy / Cpp2IL / Vineflower / Ghidra and IDA over MCP / Cheat Engine / Frida / RenderDoc; reverse-engineer a file format and prove it with a round trip |
| `fal-assets` | Sprites with real transparency, consistent variants, pixel art, seamless textures, PBR maps, image-to-3D, auto-rigging, SFX, music, voice, cutscene video |
| `asset-pipeline` | Art → engine-exact frames: cutout, nearest-neighbour fit, palettes, sheets, team-colour masks, 3D → 8/16-heading sprites |
| `game-automation` | Launch, screenshot (GPU-safe), click/type, windowed mode, crash-reporter cleanup, in-game agent bridges |
| `showcase-video` | Record the window with only the game's audio, pick moments, cut a styled video from an EDL |
| `mashup-mods` | Game-inside-a-game: content ports, passthrough mods, decomps as libraries, reimplementations |
| `publish-mod` | Lint, package per platform, credits, the post |

**The `um` CLI** (`bin/um`, Python). Every command has `--help` with examples.

| | |
|---|---|
| `um scan` | Find Steam/Epic/Xbox installs; fingerprint engine and version, .NET vs native, anti-cheat, installed loaders, save folders, ranked routes |
| `um fal` | `sprite`, `image`, `edit`, `rmbg`, `pixelate`, `upscale`, `texture`, `pbr`, `model3d`, `rig`, `sfx`, `music`, `voic

## 9. [arxiv] UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training
key: arxiv:2609.38043
url: https://arxiv.org/abs/2609.38043
meta: {"published": "2026-09-29", "authors": ["Ashish Jain", "Armaan Sandhu"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Interactive agent benchmarks and multi-turn reinforcement learning increasingly place a second language model in the role of the user. This simulated user controls what information the agent receives and when, yet current benchmarks score only the agent and do not directly measure whether the user correctly executed its assigned role. We introduce UserProxyBench, an evaluation layer over the tau-bench family, and the User Fidelity Score (UFS), which measures adherence to the benchmark's private user instructions using task-grounded rubric criteria scored independently of agent success. Holding the agent fixed at GPT-5.5 and varying only the user proxy across 375 enterprise tasks changes mean task reward by 15.2 points, while 24.4% of successful episodes contain a user-specification violation. The dominant failure is premature disclosure: users provide information before it is requested. This behavior has little effect on task reward, yet among successful episodes it causes the agent to make 1.06 fewer tool calls on average, changing the interaction being evaluated while preserving the reward. Finally, across seven proxies we identify an empirical cost-fidelity frontier, enabling practitioners to select the least expensive simulator that satisfies a required fidelity level.

## 10. [youtube] How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin
key: yt:MA6Ecac4P-Y
url: https://www.youtube.com/watch?v=MA6Ecac4P-Y
meta: {"channel": "Torin", "rank": 3, "duration_min": 1}
query: pump.fun sniper bot how it works
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

# How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin
# Torin
# https://www.youtube.com/watch?v=MA6Ecac4P-Y

[00:00] These 50 people have made over $25,000 posting, not trading, posting. This is how pump fun calls actually work and how you can make money posting meme coins. Step one, you're going to sign up for the pump fun app and you're going to find a coin you think is interesting. Purchase $1 of that coin and you make a call out. Now, everyone following you gets a notification, but if you don't have any followers, no worries. It goes up on the chart and anyone looking at that chart can find your call out. Step
[00:32] two is that if anyone sees this call out, reads your thesis, and is interested in it, and proceeds to trade this coin, you get a part of those trading fees. So, step three is that every single day pump fun opens a USD pool for all of their call outs. It has everything to do with how much volume you drove. So, make sure you are the earliest in calling the next major runner. If you do, you get paid out to your account and it just sits in there, not for trading, but for actually posting meme coins. But, this is where
[01:04] it gets even sillier. The first 2 weeks of these call outs, the top 50 traders split $700,000 in these fees. 80% of them were calling coins under a 100K market cap. One guy fired off almost 2,500 call outs for $6,800 payout, and another guy posted 11 times and made $11,000. If you want to try this out for yourself, the link is down below and go make some great calls.

## 11. [vault] Partnership ads run through a local client's own social handle
key: vault:2026-09-24:partnership-ads-run-through-a-local-client-s-own-social-hand
url: https://www.instagram.com/reel/DcWYAsmtqFr/
meta: {"vault_status": "open", "kind": "scheme", "subject": "@jasontabinass AI Influencer System, and creator seeding as a method", "date": "2026-09-24", "where": "TRITON-CORE/Research/links/2026-09-24-jasontabinass-creator-seeding.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Local trust sits with their page; permission-based, legal and sellable as a service rather than a trick

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) The account sells AI-influencer personas, not the fashion ecommerce its hashtags imply, and pushes Higgsfield trials in an affiliate pattern; no brand traceable to him, education product only. The research around it was the value. Seeding is honestly weak: 94 percent of marketers gift product but only 19 percent see meaningful advocacy, and nearly every ROI figure in circulation is vendor-published and unaudited; it works only for physical consumer products, so it does not transfer to trades. What does transfer: partnership ads run through a client own handle, seed-then-amplify applied to free work, and DMCC compliance as a sellable service. Tooling note after Butter: of twelve creator tools only Insense carries verifiable Meta and TikTok partner badges, and Modash states on its own site that it scrapes. Job: Sell a local trades business more reach without pretending to be someone else, on rails the platforms actually sanction (still open) Write-up: `TRITON-CORE/Research/links/2026-09-24-jasontabinass-creator-seeding.md` Link: https://www.instagram.com/reel/DcWYAsmtqFr/

## 12. [hn] Show HN: Parrot – Open-Source Smart Meeting Recorder with Co-Pilot on Mac
key: hn:49910328
url: https://openparrot.app
discussion: https://news.ycombinator.com/item?id=49910328
meta: {"points": 25, "comments": 10, "created": "2026-09-30T15:33:12Z"}
query: claude code

Hello Hacker News I am Uygar, I am an entrepreneur from London. I run my businesses on calls everyday, customers, partners and suppliers. And i have a horrible memory i forgot things. So months ago with the help of Claude i have built Parrot. I have designed and coded for my work and what i need. An to be honest worked very well and helped me alot. Parrot records what your mac hears and everything stays in your computer if you use local models, no account, no API calls. There is something called copilot which made my life easier, you can upload your files and when parrot hears that question on the screen recommends the answer. Which i believe very handy. If you want to make it smarter and dont mind cloud you can hook up your Claude API and Deepgram account, that gives super powers to Parrot. You still keep it locally but eventually you need to make API calls. So local or cloud totally up to you. Then after months of thinking i have decided share it as open source and this is my first open source project, so please go easy on me :) No account, no membership, open source and free. Code: https://github.com/turantekin/Parrot This project made me so excited and really would like to share with you guys so i hope can help you too. Again, i am new so go easy on me and if you have any feedback i would like to hear. Thank you Uygar
comment (moecables): instead of calling it "co-pilot" maybe call it something like "Coach", Assistant, or anything that doesn't connect it to Copilot from Microsoft b/c that's what I thought it meant
comment (nilleb): amazing! Great initiative, thank you! I have contributed to a similar app (called Recap) a few months ago and wanted to change it to something similar to Parrot - you anticipated me, thank you!
comment (joshstrange): Tried this out, and it might be due to other apps on my computer or something but the audio it records has a echo. When I go to play back a speaker's voice it sounds I can hear what sounds like 2 audio streams, slightly offset. Maybe it's something to do with SoundSource/ARC or my other meeting transcribing app. One more feature I'd love is the ability to export the text/transcript in markdown automatically. I have another tool (MeetingTranscriber) that does this and I like that so I can put the transcripts in my Obsidian Vault which I already expose to the various agents I use.

## 13. [github] echris6/motion-video-kit: Claude Code skill kit for premium AI-assisted business videos: independent critic loop, motion principles from 28 launch films, quality bar, sound design, business offers, Three.js patterns, scripts
key: gh:echris6/motion-video-kit
url: https://github.com/echris6/motion-video-kit
meta: {"stars": 545, "created": "2026-09-27", "pushed": "2026-09-28", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# Motion Video Kit

A Claude Code skill (also usable as plain context for any LLM) for making **premium, launch-style commercials for real businesses** with AI-generated footage, code-built motion (HTML/GSAP), selective Three.js, and an independent-critic quality loop.

It packages what was learned from studying 28 professional SaaS launch films and from building two full sample commercials through dozens of rounds of independent critique: a calm service film, and a 40 s Three.js product spec ad for a foldable phone in which every frame is code:

- **The Gauntlet loop:** builder ≠ judge, fresh critics on the actual render, item-by-item verification, and a ledger. Includes ready-to-use critic prompts.
- **Motion grammar:** six rules and a catalog of 16 reusable mechanisms, plus notes on all 28 reference films (links to the originals; no footage redistributed).
- **Quality bar:** measurable checks (frozen time, loudness, contrast, brand colour) and the visual and business criteria clients actually enforce.
- **Audio rules:** matching music to the buyer's customer, sparse clean sound effects, mix targets.
- **Business playbook:** verticals with buying evidence and price anchors, a pilot-offer template, honesty rules.
- **Three.js patterns:** deterministic, seekable scenes; exploded layers with projected callouts; photos pinned in 3D context; animated option patches; a realism checklist.
- **Product hero realism:** how to match a real device's motion frame by frame (measured angle keys, a monotone cubic, locked camera), screen continuity and frost, deterministic accumulation motion blur, and lights that reveal the angle without flashing.
- **Scripts and templates:** frozen-time and loudness measurement, contact sheets, sound-effect softening, an isolated component lab, and a projected-overlay module.

## Install (Claude Code)

```sh
git clone https://github.com/echris6/motion-video-kit.git
cp -r motion-video-kit/business-motion-film ~/.claude/skills/        # all projects
# or, per project:
cp -r motion-video-kit/business-motion-film  /.claude/skills/
```

Then ask for a business commercial, sample reel or explainer, or for a review of one, and the skill loads. It works best with [HyperFrames](https://hyperframes.heygen.com) for rendering, but the principles, prompts and checks are renderer-agnostic.

**Other LLMs:** paste `business-motion-film/SKILL.md` plus the reference files you need into the context.

## Requirements for the scripts

`ffmpeg`/`ffprobe` (with the `ebur128` filter). Optional: Node 22+ and HyperFrames for the lab template.

## Layout

```
business-motion-film/
  SKILL.md                      workflow + non-negotiables
  references/
    gauntlet.md                 the review loop, with real findings
    critic-prompts.md           component / full-film / verification / storyboard prompts
    motion-grammar.md           6 rules + mechanism catalog + pacing numbers
    launch-film-notes.md        notes on 28 reference films (links only)
    quality-bar.md              measured + visual + business ship criteria
    audio.md                    music, SFX, mix
    business-offers.md          verticals, evidence, price anchors, pilot offer
    three-js-patterns.md        render contract, patterns, realism checklist
    case-study-alder.md         a full worked example (calm service film)
    product-hero-realism.md     making a 3D device move like the real one
    case-study-duo.md           a Three.js product film, round by rou

## 14. [youtube] Chess Engine in Python - Part 2 - Moving the pieces
key: yt:o24J3WcBGLg
url: https://www.youtube.com/watch?v=o24J3WcBGLg
meta: {"channel": "Eddie Sharick (Eddie)", "rank": 3, "duration_min": 34}
query: lichess bot python engine

# Chess Engine in Python - Part 2 - Moving the pieces
# Eddie Sharick (Eddie)
# https://www.youtube.com/watch?v=o24J3WcBGLg

[00:01] hello everybody and welcome back to part two of our test video series today the the goal is to get be well let me let me start with where we left off we left off yesterday with this sort of window here where we have all the pieces drawn up the checkerboard pattern so we can now start to play chess but clicking on stuff doesn't do anything so today what
[00:33] we're gonna do is try to handle user input from our mouse so it should look something like this when we're finished today we're now you can click on a piece you can click on a square and you can move piece to that Square and if you have two people that know the rules chess then they can pretty much play using this user interface but they can also play like a toddler where they can move piece wherever they they want even
[01:07] making move multiple moves in a row being illegal moves white doesn't have their King in or it's fine it's not real chest it's like toddler chest but that that's the idea and then we'll worry about adding an logic for making sure the moves that they make are valid but right now we're just gonna handle the mouse input get the two squares the user clicks on and make them accordingly alright so let's go ahead and jump right in
[01:40] um so where we left off yesterday we had our main class that handled loading in the images drawing the gamestate drawing the board trying the pieces all that good stuff so we've got a lot of UI and you can imagine where we're heading today is right in this event you where we can handle the mouse events we're gonna have to add a little bit to our chess engine namely what we're gonna add today is a move class - in order to make said move we actually need to keep track of two
[02:14] squares the starting row and starting column ending row and column and we're gonna use a class for that and we don't have to just necessarily use a class you could just continually keep track of like a list of of coordinates basically of first click second click and you don't have to make the class but I think making a class makes it a little bit easier for us - I think it's a good abstraction it makes this a little bit easier for us to program when we can
[02:50] just cetera so let's go back to the main and let's go into our event queue here you right it right in here after running false and we're going to start by putting in the mouse event handles so if you'll recall from our earlier
[03:30] Python PI game coding we've done mouse clicks before we look at the event type is and here we're gonna we're just gonna do mouse button down no there are some engines like if you play online a lot of engines will let you click and drag the piece to the square that you want to move it to we could add that functionality and maybe that's something that will add in on a later date but for right now we're just gonna simply have it functionality where we click a piece and we click where we want it to go and it goes
[04:01] we'll keep it we'll keep it simple it's the simplest way to do the logic again we could make it a little bit more complicated and and maybe that's something that you want to try on as well all right so we have this location where we're gonna keep track of the mouse x and y coordinates get position this is the XY location of the mouse if you do add a side panel in here then you do just have to make sure that when you're

[transcript continues in field-notes/staging/o24J3WcBGLg.txt]
