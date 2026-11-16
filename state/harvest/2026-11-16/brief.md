# Harvest brief, 2026-11-16

14 items shortlisted from 379 candidates (302 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] News filter on a daily-bar trend follower
key: vault:2026-10-16:news-filter-on-a-daily-bar-trend-follower
url: 
meta: {"vault_status": "dead", "kind": "idea", "subject": "High-impact US news filter (CPI, FOMC, NFP) on the S1 daily crypto trend bot", "date": "2026-10-16", "where": "TRITON-CORE/Ventures/Trading/VERDICT-2026-10-16-news-filter.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: Too few entries land on release days to measure; flattening only adds fees

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Backtested on 3.2 years of daily BTC and ETH: skipping entries around releases changed one trade and is indistinguishable from random days; flattening before each release fails the protocol on fees and churn. No change to the bot.

## 2. [hn] Ask HN: Stripe closed us after one $1,500 invoice and never asked for evidence
key: hn:50510042
url: https://news.ycombinator.com/item?id=50510042
discussion: https://news.ycombinator.com/item?id=50510042
meta: {"points": 178, "comments": 91, "created": "2026-11-15T19:49:28Z"}
query: car data

We're a small business that sells pre-booked appointments with homeowners to local contractors, billed per appointment that actually happens. Our first client agreed to this on a recorded call and saved his card through a $1 Stripe payment link, which we planned to use for billing later. That $1 payment went through. A few weeks later we invoiced him $1,500 for 3 completed appointments and charged the saved card. Stripe blocked the payment. Two days after that the account was closed with this wording: payments "don't appear to have been authorized by the customer." What happened next: - We appealed through the Dashboard with an appeal letter, our company documents and the invoice. It was rejected the next day as an "unacceptable level of risk." - Support told us our "business model presents a level of risk we're unable to support" and that the decision is final. - After a Stripe employee escalated it internally, we got a short email saying Stripe still won't accept payments for our business. In all of this, nobody asked us for the call recording, our messages with the client, or a confirmation from the client himself. As far as we know, he never disputed anything, and he has told us he is paying by bank transfer outside Stripe. I'm not saying our setup is perfect. It's a new account, the first real charge was large compared to the $1 test, and billing a saved card later is probably what looked wrong. If there's something specific we should fix, I'll fix it. What I'm asking: 1
comment (codingdave): I have no knowledge specific to Stripe or your case, but do I know that the pattern you just described - a small 1 dollar payment followed by a large payment - is the exact pattern that criminals use to test stolen credit cards numbers. My bank will automatically reject anything following that pattern, put a hold on my card, and call me to confirm whether or not I have my card. So yeah, if your business model calls for pattern matching with how stolen cards are used, that could very well be unacceptable risk to Stripe.
comment (Traubenfuchs): Hi, you are on the frontpage of hackernews and have reached our premium support. The CEO or CTO of Stripe will be with you shortly.
comment (didgeoridoo): Yeah unfortunately this charge pattern could not have looked MORE like merchant fraud. The right approach would have been to use https://docs.stripe.com/payments/setup-intents and set it for off-session usage. You still might have gotten a payment hold on the first transaction until someone in risk could take a peek at your site to make sure you had all the right disclosures in place, but you probably would have kept the account.

## 3. [github] BigPizzaV3/ClaudeMom: 不用 Claude 账号！把 API Key 变成登录模式，Claude 桌面版全功能解锁（汉化 / 语音 / 电脑控制）
key: gh:bigpizzav3/claudemom
url: https://github.com/BigPizzaV3/ClaudeMom
meta: {"stars": 535, "created": "2026-11-12", "pushed": "2026-11-16", "language": "Rust", "topics": ["claude", "claude-code", "claude-desktop", "tauri"]}
query: claude-code created:>{since} stars:>20

# ClaudeMom

**不用 Claude 账号！把 API Key 变成登录模式，Claude 桌面版全功能解锁（汉化 / 语音 / 电脑控制）**

 

Claude 桌面版一直有两种用法：

- **登录官方账号**：完整功能，Chat / Code / Cowork、电脑控制、语音输入都在
- **填 API Key（第三方 / 3p 模式）**：能用，但很多功能入口直接没了

ClaudeMom 是一种**新的接入方式**：在本机把你的 API Key **变成「登录模式」**。Claude 桌面版看到的是一个已登录的账号，界面和功能都是登录版的；实际的模型请求走你自己的 Base URL + Key。

不需要 Claude 账号，不改原版应用，不动官方登录态，官方 App 照常更新。

下载：[Releases](https://github.com/BigPizzaV3/ClaudeMom/releases/latest)（macOS 通用版 dmg / Windows exe）

友情链接： LINUX DO 

## 三种接入方式对比

| | 登录官方账号 | API Key（3p 模式） | **ClaudeMom** |
|---|---|---|---|
| 需要 Claude 账号 | 要 | 不要 | **不要** |
| 模型来源 | 官方 | 你的 Key | **你的 Key** |
| Chat / Code / Cowork | ✅ | 部分 | **✅** |
| 电脑控制 / 语音输入 | ✅ | ❌ | **✅** |
| 中文界面 | ✅ 但是不敢开 | ❌ | **✅** |

## 原理

本地起一个兼容服务，接管 Claude 桌面版的账号和功能请求：账号信息、功能开关按「已登录」返回，对话请求转发到你配置的上游。证书只在本机生效，随时可以取消信任。

## 功能

- **登录模式体验**：Chat / Code / Cowork 三个页签都能用，是原版客户端，不是网页套壳
- **多组上游**：每组一个 Base URL + Key（Anthropic 兼容，和 `ANTHROPIC_BASE_URL` 同语义），随时切换，可拉取模型列表
- **一键导入**：cc-switch 的 Claude 供应商；也可以把 Magpie 的本机网关当上游
- **界面汉化**：完整中文界面
- **语音输入**：本地离线听写（SenseVoice），音频不出本机
- **电脑控制 / 后台模式**：较新的 macOS 上 Claude 会提示「暂不支持后台模式」，高级里有开关可以解除版本限制（默认关）
- **Code 页签和命令行共用 `~/.claude`**：终端、其他工具里建的 Claude Code 会话也会出现在 Desktop 左侧列表
- **自动更新**；macOS 版已签名 + 公证，下载即可打开

 

 

## 使用

1. 先装好官方 Claude Desktop 和 Node.js 22+
2. 打开 ClaudeMom，第一次按提示信任本地证书（只在本机生效）
3. 添加上游（或从 cc-switch 导入），选默认模型
4. 点「启动 Claude」，进去就是登录版界面

欢迎提 issue 和 PR，一起把 Claude 桌面版用得更顺手！

## 结构

| 目录 | 说明 |
|---|---|
| `crates/claude-local` | 核心：本地兼容服务（`runtime/`）、证书、profile 切换、启动 / 停止、听写。 |
| `apps/claude-mom` | ClaudeMom 桌面程序（Tauri + React）。 |

## 开发

```bash
cd apps/claude-mom
npm install
npm run check && npm test          # 前端
cargo test --workspace             # Rust（在仓库根目录）
npx tauri build --bundles app      # 打包 macOS .app
node scripts/relaunch-local.mjs    # 构建并重启本地实例（在仓库根目录）
```

核心的 Node 测试：`cd crates/claude-local/runtime && node --test managed.test.mjs proxy.test.mjs`
（需要本地测试证书：`scripts/gen-ca.sh`）。

## 许可

AGPL-3.0-only

## 4. [arxiv] OpenLayout: An Open and Agentic-Driven Platform for Holistic VLSI Physical Design and Benchmarking
key: arxiv:2611.18517
url: https://arxiv.org/abs/2611.18517
meta: {"published": "2026-11-13", "authors": ["Qiufeng Li", "Sizhe Tang", "Quan Cheng", "Zirui Wang"], "categories": ["cs.AR"]}
query: all:"language model" AND all:agent AND all:tool

Physical design automation of very large-scale integrated circuits (VLSI) has made significant strides, progressing from single-stage placement and routing toward increasingly integrated full-flow implementation. Yet, existing approaches struggle with the vast design space optimization (DSO) arising from diverse technology nodes, circuit designs, and varied constraints. The substantial runtime of physical-design tools further exacerbates this challenge, leaving industrial workflows heavily dependent on experienced engineers to navigate the design space and achieve power, performance, and area (PPA) targets, incurring significant engineering effort. We argue that large language models (LLMs) with strong reasoning capabilities, enriched with distilled human design expertise, offer a promising path toward efficient and automated DSO. Unlike traditional algorithms, LLMs can interpret complex design contexts and naturally incorporate human expertise expressed in natural language for reasoning, acting, observing, and adapting throughout the design process, a capability that conventional optimization methods cannot exploit. To this end, we present OpenLayout, an agentic platform that leverages multi-agent collaboration with embedded design knowledge to enable self-iterative DSO. We further introduce OpenLayout-Bench, a benchmark targeting advanced technology nodes with commercial EDA tools to systematically evaluate physical design automation capabilities of LLMs. Experimental results demonstrate that OpenLayout achieves state-of-the-art performance, with approximately 20% accuracy improvement over baseline methods. Our work is open-sourced at https://github.com/fenggev56/OpenLayout

## 5. [youtube] Predict Football Match Winners With Machine Learning And Python
key: yt:0irmDBWLrco
url: https://www.youtube.com/watch?v=0irmDBWLrco
meta: {"channel": "Dataquest", "rank": 3, "duration_min": 44}
query: dixon coles model python

# Predict Football Match Winners With Machine Learning And Python
# Dataquest
# https://www.youtube.com/watch?v=0irmDBWLrco

[00:00] hello welcome my name is vic and today we're going to be working on a really exciting machine learning project we're going to be predicting who's going to win each football match in the english premier league we're going to start out with match data that we're going to load into pandas and clean then we're going to apply a machine learning model called a random forest to actually predict who will win each match then we'll measure how well our algorithm did and actually improve the performance and we'll end with some next steps that you can use to continue
[00:34] improving the model all right let's get started [Music] and by the end of this project we'll have trained a machine learning model that can predict whether a team will win a given match in the english premier league or not and we can apply that to future matches [Music] all right let's go ahead and start coding
[01:05] so we will be using jupiter lab for this project if you're not familiar with jupiter lab or you don't have it installed feel free to use google colab which is a cloud no hosted notebook all right and we'll be working with a file called matches.csv if you did the web scraping part of this project earlier you should have that file locally if you didn't don't worry you can download the file and the link is going to be in the description so let's take a quick look at the file and what the file has is more than a
[01:39] thousand rows and each row is a single match that was played in the english premier league so you can see there's a lot of data about each match including which team won or lost and some stats about shooting and possession etc all right so let's go ahead and start coding so the first thing we're going to do is we're going to import a library called pandas then we're going to read in our match data and that's just matches.csv and we're going to specify that the
[02:12] first column in our data is actually the index column when you looked at the csv file you might have noticed that there were just a bunch of numbers in the first column one two three four five six seven eight nine that's referred to as an index in pandas so we'll just specify to pandas that that is the index column now we can take a look at the first few rows of our data and we can see it looks the same as the csv file that we just looked at so each row is a single match in the english premier league
[02:45] and then let's take a look at the shape property of matches and we can see we have 1389 rows and 27 columns [Music] all right so if you know something about the epl you may know that there are 38 matches played each season and there are 20 teams in the league each season and we have data for two seasons the 2020-21 season and the 21-22 season so if we multiply that all out we should
[03:18] have 1520 matches but we actually have fewer so let's do a little investigation and figure out what is going on here so the first thing we'll do is we'll look at value counts of our teams so what this does will it will help us figure out how many matches we have for each team in our data so let's go ahead and run this and we'll see each squad in the english premier league and how many matches we have for that squad
[03:50] so we can see most squads are kind of in the 70s we have a few that have match counts in the 30s so if you know something about the epl you know t
[transcript continues in field-notes/staging/0irmDBWLrco.txt]

## 6. [awesome] aelethion/agentsocks (new in awesome-mcp-servers)
key: gh:aelethion/agentsocks
url: https://github.com/aelethion/agentsocks
meta: {"list": "awesome-mcp-servers", "stars": 1, "created": "2026-10-19", "language": "TypeScript", "description": "Native messaging between Claude Code, Codex and other coding-agent sessions."}
query: awesome-mcp-servers

Your coding agents, talking to each other.  

 
     
     
     
   
 

agentsocks lets the Claude Code and Codex sessions on your machine message each other, ask each other questions and hand over
tasks. Each message arrives the way that tool already receives one, so nothing is ever typed into a terminal.

 
   
 

 
   Install  ·  See it work  ·  Works with  ·  Limits  ·  Guide 
 

## Install

```bash
npm install -g agentsocks
agentsocks install
agentsocks doctor
```

Needs Node.js 22.13 or later, Claude Code 2.1.224 or later and Codex CLI 0.162 or later. `agentsocks install` backs up every
file it edits, and `--dry-run` shows the changes first. New sessions pick it up; sessions already running are not touched.

## See it work

Open a Claude Code session and a Codex session. In Codex, type: *tell api-worker the migration is done and the new column is
tenant_id.*

| Claude Code (`api-worker`) | Codex (`codex-web`) |
|---|---|
| | `• Called agentsocks.send_message` `└ Sent to @api-worker [064c2f] (claude). Delivered.` |
| `› Message from @codex-web (codex): Migration is done; the new column is tenant_id.` | |
| Claude answers with its built-in `SendMessage`. | `› 📨 agentsocks: new message from a Claude Code session. Read it with read_inbox.` `• Called agentsocks.read_inbox` |

The same works from any shell: `agentsocks list` shows who is running, and `agentsocks send api-worker "the rebase is safe now"`
sends a message. The [guide](https://github.com/Aelethion/agentsocks/blob/main/docs/GUIDE.md#using-it) has every tool and command.

## Works with

| Agent | Status | Hears about a message | Wakes when idle |
|---|---|---|---|
| Claude Code | Supported, run live | In its own cross-session inbox, between tool calls | Yes, as a new turn |
| Codex CLI | Supported, run live | Through its hooks, before the next tool call | Yes, with `codex queue` |
| OpenCode | Experimental, not run live against 0.4 | A notice on the next tool result | Yes |
| OMP (oh-my-pi) | Experimental; an earlier 0.4 build passed a live run | A note on the next tool result | Yes |
| Hermes | Experimental, not run live against 0.4 | A notice at the start of the next turn | Only with Hermes's API server on |
| Cursor (CLI and IDE) | Experimental, not run live against 0.4 | A notice after the next tool call | No |
| GitHub Copilot CLI | Experimental, not run live against 0.4 | A notice after the next tool call | No |
| Gemini CLI | Experimental, not run live against 0.4 | A notice after the next tool call | No |
| Aider | Not supported: no MCP client and no hooks | | |

Tested with Claude Code 2.1.294 to 2.1.302 and Codex CLI 0.162 to 0.163. Two Claude Code sessions keep using Claude's own
`SendMessage`. How each agent is wired is in the [guide](https://github.com/Aelethion/agentsocks/blob/main/docs/GUIDE.md#more-agents-v04).

## What you get

- **Messages, questions and tasks.** Message any session, ask up to 16 sessions one question and get the answers back together
  (experimental), or hand over a tracked task with an owner, a state and a result.
- **Nothing typed into a terminal.** No tmux `send-keys`, no pane pastes, no fake user input. A message from another agent is
  never treated as you, and it can't answer a permission prompt.
- **Attention routing.** A busy session isn't interrupted for every message: FYIs come as one digest, and floods wait for the end
  of its turn ([how it decides](https://github.com/Aelethion/agentsocks/blob/main/docs/GUIDE.md#attention-routi

## 7. [vault] Trading insider clusters with real money at retail size
key: vault:2026-10-16:trading-insider-clusters-with-real-money-at-retail-size
url: 
meta: {"vault_status": "dead", "kind": "idea", "subject": "US insider cluster-buy signal from SEC Form 4 data (paper backtest, Jul 2023 to Oct 2026)", "date": "2026-10-16", "where": "TRITON-CORE/Ventures/Trading/VERDICT-2026-10-16-insider-clusters.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: Costs and the SPY alternative eat the edge on this evidence

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Can't tell, leaning no. Clusters of 3+ officer or director open-market buys beat random same-size US stocks by about 1.3% per 21 days before costs in the last 24 months, but after a 0.45% UK retail round trip the gap is not distinguishable from zero, and an equal-weight 21-day portfolio lagged SPY with a deeper drawdown.

## 8. [hn] Show HN: A terminal-native idle factory game, written in Rust with ratatui
key: hn:50497132
url: https://gitlab.com/snipedbywifi/terminactory
discussion: https://news.ycombinator.com/item?id=50497132
meta: {"points": 171, "comments": 44, "created": "2026-11-14T14:05:54Z"}
query: claude code

Hey HN readers! I'm snipedbywifi ( https://gitlab.com/snipedbywifi ), and i've been working on terminactory. Please try it out if you'd like to play a cozy factory game while waiting for long agent tasks to finish! The game is a factory game (overused niche, i know xD), but runs in your terminal. Reason i built it? glad you asked: So basically, it started off with me wanting a terminal-native factory game. Me and the modern 5.5 claude models made a base for the game that I liked, and then i went ham adding features / fixing some minor flaws (like adding claude code hooks so you recieve "telegrams" [the agent's responses], so you can review progress directly in-game). (yes, I had heavy AI assistance, disclaimer!!!) Right now, the game has basic factory features you'd expect from a game like this (build stuff, delete stuff, measure how much you're earning, basic selection tools), along with a few more.. "unexpected" features. This includes a fake in-game browser that has a wiki, fake forums, some fun bits of lore, some more lore, a LOT more lore, and a research graph that shows how many items or how much RP (research points) you'd need to unlock something, and some more QOL features. If anyone actually has this issue / want of a terminal-based game that runs alongside your agents so you don't doomscroll, do you have any suggestions, or additional ideas I could add? It's hosted on GitLab, soo, that's one additional thing i'd like to mention Thanks for reading!! snipedbywifi (p.s
comment (Joker_vD): > It is made to sit in a split next to your AI agents. They can send you short messages that show up in the game, so you can play while they work. > Agent messages > Your AI agents can message you inside the game. A message costs the agent only the words in it, and nothing prints on success. Messages wait while the game is closed. It's kinda amazing how the ancient "local mail" technology keeps getting reinvented, you know, and reintegrated inside the gameplay? NetHack had its its "mail demon" since... (googles) version 1.0.2, in April 1985 — the creature would spawn in the game, deliver you a
comment (wongarsu): Reminds me of Dwarf Fortress's original ASCII UI
comment (chaz6): Nice! I wonder if you could have an option to use the icons available in Nerd Fonts in addition to plain ascii?

## 9. [github] credoksopho1984/blender-ai-copilot-studio: An AI copilot and MCP server for Blender that turns plain-language briefs into scene operations—inside a visual chat studio with multi-agent teams, your choice of AI models, and 27 built-in scene tools. · blender-ai-copilot-studio · blender ai · ai for blender · blender copilot · blender ai copilot · blender ai assistant · blender mcp server
key: gh:credoksopho1984/blender-ai-copilot-studio
url: https://github.com/credoksopho1984/blender-ai-copilot-studio
meta: {"stars": 516, "created": "2026-11-12", "pushed": "2026-11-15", "language": null, "topics": ["3d-automation", "3d-modeling", "blender", "blender-addon", "blender-agents", "blender-ai", "blender-assistant", "blender-automation"]}
query: mcp server created:>{since} stars:>30

# blender-ai-copilot-studio

**An AI copilot and MCP server for Blender that turns plain-language briefs into scene operations—inside a visual chat studio with multi-agent teams, your choice of AI models, and 27 built-in scene tools.**

[download-url]: https://github.com/credoksopho1984/blender-ai-copilot-studio/releases

[]      

[][download-url]

Picture your next scene: you type the brief, the copilot inspects the viewport, builds the pedestal, camera and lights, assigns the materials, and answers with a finished snapshot on the Studio task board.

## Why

Building in Blender still means menus, mouse miles and copy-pasted Python snippets—hours of mechanical work between you and the idea. blender-ai-copilot-studio puts a scene-aware AI copilot inside Blender: it reads your scene first, then carries out multi-step briefs as supervised tool calls with approvals, cancellation and named undo. You keep creating in Blender and let plain language handle the repetitive parts—so a full layout takes one sentence instead of an afternoon.

## Without / With

| Without | With |
|---|---|
| Hours of manual clicks to block out and polish a scene | One plain-language brief executed step by step |
| Copy-pasting bpy snippets from forums and hoping they run | 27 validated scene tools with per-operation approvals and named undo |
| Chatting with an AI in one window, rebuilding by hand in another | One Studio workspace: chat, scene objects, viewport snapshots and a task board |
| One assistant locked to a single vendor | OpenAI, Anthropic Claude, Google Gemini, OpenRouter, OpenCode Zen, Ollama or custom endpoints |
| External tools with no safe path into your scene | An authenticated local MCP endpoint any compatible client can call |
| Solo grinding through multi-part briefs | Manager–worker–reviewer agent teams that sequence and check the work |

## Quick Start

Open PowerShell, copy a command, paste it and press Enter—every command below is self-contained and needs no preparation.

1. Download **`mcp-for-blender-pro.zip`** from [Releases](../../releases/latest).
2. In Blender, open **Edit → Preferences → Get Extensions → menu → Install from Disk**.
3. Select the ZIP, enable **mcp-for-blender-pro**, then open **3D Viewport → N → MCP Pro**.
4. Choose a provider, add your connection details and select a model.
5. Send a message in Blender or click **Open Studio Window**.

## Features

- Inspect the scene before every change—the copilot reads objects, structure and materials before it acts.
- Build complete layouts from a brief—27 supervised scene tools create primitives, lights, cameras, materials, parenting and transforms in ordered steps.
- Run multi-agent team chains—a manager splits the brief into assignments, workers execute, reviewers approve or return findings, and the task board tracks every attempt.
- Connect the model that fits the job—OpenAI, Anthropic Claude, Google Gemini, OpenRouter, OpenCode Zen, local Ollama or custom endpoints, with saved connection profiles.
- Serve any MCP client from Blender—an authenticated Streamable HTTP endpoint exposes the full toolset to OpenCode and compatible apps.
- Find and import assets mid-conversation—search Poly Haven, Sketchfab and Poly Pizza and import after your confirmation.
- Stay in control—per-operation approvals, cancellation after the current step, named undo steps, and menus in English, German, French, Spanish or Chinese.

## How it works

blender-ai-copilot-studio runs inside Blender as an ex

## 10. [arxiv] Can Mechanistic Interpretability Help Explain LLM Agent Failures? A Case Study on Web Element Hallucination
key: arxiv:2611.18514
url: https://arxiv.org/abs/2611.18514
meta: {"published": "2026-11-13", "authors": ["Mohamed Aghzal", "Mor Geva", "Gregory J. Stein", "Ziyu Yao"], "categories": ["cs.AI", "cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Mechanistic Interpretability (MI) has made significant progress in explaining the internal computations of Large Language Models (LLMs); however, these advances have yet to demonstrate comparable success in explaining the decision-making processes of LLM-based agents. This paper examines the challenges MI tools face when applied to realistic agentic failures. We focus on one such failure: web agents hallucinating actions that are not available on a website. We apply a series of mechanistic analyzes to Qwen2.5-7B-Instruct as it interacts with live websites. We find that a linear probe trained on the last prompt token can predict hallucinations before generation begins (0.80 AUC) and steering along a probe direction corrects 85\% of hallucinations, but disrupts 7\% of valid actions. However, these results only provide a partial explanation of why the agent hallucinates. The probe direction is sensitive to prompt formatting, losing much of its steering effect after a minor change to how actions are represented. Additionally, circuit identification can be difficult as the computation is distributed across multiple components and positions, and the information the agent relies on varies across examples. We discuss how these observations challenge the assumptions underlying standard MI methods for circuit discovery and feature identification, and outline future directions for making these methods better suited to explain failures in LLM-based agents.

## 11. [youtube] The 7 fastest growing Claude skills (all free)
key: yt:94DrtNz-Coc
url: https://www.youtube.com/watch?v=94DrtNz-Coc
meta: {"channel": "Nilo", "rank": 4, "duration_min": 1}
query: claude code skills workflow 2026

# The 7 fastest growing Claude skills (all free)
# Nilo
# https://www.youtube.com/watch?v=94DrtNz-Coc

[00:00] These are the seven fastest growing cloud skills in GitHub in the last 30 days. All seven are free and the last one is an absolute must have if you build anything with AI. To start with Hallmark, which runs your page through a set of AI slot detectors before you ship anything. Then anatomy, which will draw any idea like a working machine to help you actually learn and build your understanding faster. Then everything cloud code. This is a one-stop shop. It's literally a full setup in one install line. This next one has over 100,000 stars on GitHub. Impeccable will do a full review of any site and is incredible at removing formatting and
[00:33] misalignment issues that are subtle but make a huge difference. Ponytail will make sure that Claude is coding in the most efficient way so you can work faster and save tokens. Matt PCO's engineering skills. These have been on the fastest growing list for basically the whole year now and they serve as a full endto-end engineering setup. And right at the top, Cloudflare's security audit. Cloudflare powers almost 50% of the Fortune 500 and 20% of the internet and they just open source their entire security process. It runs a full audit on your codebase and passes you exactly what needs to be fixed. If you comment
[01:05] grow below and I'll send you the install line for everyone and a summary of how you can get the most out of them.

## 12. [awesome] agoreums/agoreum-mcp (new in awesome-mcp-servers)
key: gh:agoreums/agoreum-mcp
url: https://github.com/agoreums/agoreum-mcp
meta: {"list": "awesome-mcp-servers", "stars": 4, "created": "2026-11-05", "language": "TypeScript", "description": "MCP server for Agoreum: find and buy from AI agents, pay in USDC on Base through escrow, per-call checks over x402."}
query: awesome-mcp-servers

# @agoreum/mcp

Agoreum for any MCP agent. Discover services, buy and pay through
non-custodial escrow, sell and deliver, and verify receipts, from Claude,
Cursor or any other MCP client.

Agoreum is live on Base mainnet, in beta, with real USDC. The contracts cap
each order and the total they hold, and they have been through a full internal
security audit; the security page at https://agoreum.xyz/en/security says what
was done. This is a release candidate, and it follows `@agoreum/sdk`, which
stays a release candidate until its 0.7.0 shape settles. Pin the exact version.

## Install

### Nothing to install

If your client can add a remote MCP server, you do not need this package:

* `https://agoreum.xyz/api/v1/mcp/public`: no account. Search, read, and buy
  Agoreum Tools per call over x402.
* `https://agoreum.xyz/api/v1/mcp`: with an API key or OAuth. Orders, requests,
  selling and delivering.

Run this package instead when the agent should pay and settle from its own
wallet on your machine.

### From agoreum.xyz

npm holds versions up to 0.1.0-rc.6, and later ones are not there yet because
publishing to npm is blocked on an account recovery. Until it is, this version
installs from our own site, with its SHA-512 beside it:

```
npx -y https://www.agoreum.xyz/downloads/agoreum-mcp-0.1.0-rc.8.tgz
```

To check the file first:

```
curl -fsSLO https://www.agoreum.xyz/downloads/agoreum-mcp-0.1.0-rc.8.tgz
curl -fsSLO https://www.agoreum.xyz/downloads/agoreum-mcp-0.1.0-rc.8.tgz.sha512
sha512sum -c agoreum-mcp-0.1.0-rc.8.tgz.sha512
```

### Claude Code

```
/plugin marketplace add https://agoreum.xyz/claude/marketplace.json
/plugin install agoreum@agoreum
```

The plugin asks for your API key and, optionally, the paying wallet's key. It
stores both in your system's secure storage, and adds buy, sell and settle
skills.

### Any MCP client

```json
{
  "mcpServers": {
    "agoreum": {
      "command": "npx",
      "args": ["-y", "https://www.agoreum.xyz/downloads/agoreum-mcp-0.1.0-rc.8.tgz"],
      "env": {
        "AGOREUM_API_KEY": "ak_...",
        "AGOREUM_WALLET_PRIVATE_KEY": "0x...",
        "AGOREUM_MAX_ORDER_USDC": "5",
        "AGOREUM_MAX_DAILY_USDC": "20"
      }
    }
  }
}
```

* `AGOREUM_API_KEY` (required): create one at agoreum.xyz under Settings, API
  keys, with `marketplace:read`, `orders:read` and `orders:write`.
* `AGOREUM_WALLET_PRIVATE_KEY` (optional): needed only to pay. Use a wallet
  you have signed in to Agoreum with, and fund it with only what you are
  prepared for the agent to spend. It signs on this machine and is never sent.
* `AGOREUM_WALLET_KEY_FILE` (optional): a file holding that key, instead of
  writing it into the client's configuration, which some clients show in their
  settings and logs.
* `AGOREUM_MAX_ORDER_USDC` (default 5) and `AGOREUM_MAX_DAILY_USDC` (default
  20, UTC day): spend limits, checked before anything is signed.
* `AGOREUM_RPC_URL` (optional): where the wallet's USDC balance is read before
  signing. Defaults to Base's public RPC for the order's chain.

## Tools

| Tool | What it does |
| --- | --- |
| `agoreum_search_services` | Search services. `sort=evidence` ranks by distinct buyers who settled through escrow |
| `agoreum_get_service` | One service in full, by the agent and service slugs search returns: description, quantity limits, delivery and auto-release hours, input and output schemas, and whether the provider can be reached now |
| `agoreum_place_order` | Place an order; nothi

## 13. [vault] spend everything you have
key: vault:2026-10-05:spend-everything-you-have
url: 
meta: {"vault_status": "dead", "kind": "scheme", "subject": "OFM Conquest (Skool, Dylan Beese) - 6 and 7 figure interviews", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/ofm-conquest/TAKEAWAYS-interviews.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: the funnel pitch; several interviewees bet their last savings

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Free classroom plus 13 seller-run testimonial interviews, a funnel for the paid partnership; figures are unverified gross inflow. Useful as agency-operations intel, not as proof of returns.

## 14. [hn] Anthropic upgrades Claude Code Projects to run parallel AI workers
key: hn:50492141
url: https://claude.com/resources/articles/projects-redesigned
discussion: https://news.ycombinator.com/item?id=50492141
meta: {"points": 100, "comments": 96, "created": "2026-11-14T00:28:11Z"}
query: claude code

comment (kami23): I've spent the last two building almost exactly this for fun at $DAYJOB, the todo list becomes individual threads with proactive comms. As I was building it, it was teaching me why there were some architectural choices in Gastown[1] that I was tilting my head at about back when it came out. I've built half versions of it many times this year never getting the flow right. Today I cracked the todo list led development where I was just adding ideas as streams of thought and if a thought was relevant to a repo I have a 'keeper' for each microservice who is the expert in answering questions and imp
comment (augment_me): Sounds like a great way to automatically increase API usage by a lot and drain customers of money
comment (minimaxa): Only a few more Silly CON valley moats to pillage, and Claude does everything! One subscription to rule them all, as long you're nice to Claude... What a time to be alive, couldn't think of a nicer group of people to give my money to.
