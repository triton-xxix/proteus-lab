# Harvest brief, 2026-10-07

14 items shortlisted from 208 candidates (78 dropped as already seen, 22 carry a vault verdict on the vendor).

## 1. [vault] Insider cluster-buy signal from the free Form 4 filings page as a paper desk
key: vault:2026-10-07:insider-cluster-buy-signal-from-the-free-form-4-filings-page
url: https://finviz.com/
meta: {"vault_status": "open", "kind": "tool", "subject": "finviz.com (US stock screener, heat maps, insider filings; Elite tier)", "date": "2026-10-07", "where": "TRITON-CORE/Research/links/2026-10-07-finviz.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Documented small positive drift, free daily data, nobody in the vault has tested it; Proteus material

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Free US-equity screener, sector heat maps, news, insider filings and earnings calendar, 1 minute delayed; Elite at 39.50 dollars a month adds real-time, charts, alerts and export. Same category as TradingView, assessed 21 Sep: eyes, not edge, so Elite is dead at Luke's pot size. The free tier is a cost-free context read beside the eToro demo copy log. The one open thread is the free insider-filings page as a tested signal, which is Proteus desk material. Job: Read the US stock market cheaply enough to judge copied leaders and screen ideas (solved) Write-up: `TRITON-CORE/Research/links/2026-10-07-finviz.md` Link: https://finviz.com/

## 2. [hn] Tell HN: Apple not letting removal of AI models on macOS 27 is outrageous
key: hn:49993338
url: https://news.ycombinator.com/item?id=49993338
discussion: https://news.ycombinator.com/item?id=49993338
meta: {"points": 33, "comments": 26, "created": "2026-10-07T14:26:53Z"}
query: car data

I feel like there's not enough outrage over Apple not removing their Apple Intelligence models on macOS 27 even after disabling Siri. I have a 512 GB Mac mini but because I have so much data, I also have a 2 TB monthly iCloud subscription. I have Siri AI turned off. Yet, my storage settings show 30 GB is occupied by useless Apple Intelligence models which I don't use. And these models can't even be moved to my 2 TB iCloud subscription. It's really pissing me off. I feel like there needs to be a lot more negative publicity about this to get Apple's attention. More tech blogs should be writing about how horrible of a decision this is. I am hoping this post does that.
comment (lode): While I agree with you, there is an unofficial (and reversible) tool which can help you reclaim this space: https://github.com/omlahore/RemoveMacAI (to be complete: it seems to be based on https://github.com/4evy/pared ) discussed here: https://news.ycombinator.com/item?id=49957116
comment (monkellipse): 100% agreed, outrageous. Sadly I don’t know what else to say or do, feels like shouting into the wind at this point…
comment (aeturnum): I also do not use them - but there are lots of bits of the OS that I don't use and AI does not feel different to me. Given its many uses and that there are people who are enthusiastically adopting it I think adding it makes sense and you can't totally remove most other OS features so it feels odd to expect it here.

## 3. [github] JimmySadek/video-fetcher-to-markdown: Portable AI-agent skill: turn YouTube, Instagram, TikTok, X and other video links into Obsidian-ready Markdown notes: captions or local Whisper transcripts, frames, metadata and timestamps
key: gh:jimmysadek/video-fetcher-to-markdown
url: https://github.com/JimmySadek/video-fetcher-to-markdown
meta: {"stars": 485, "created": "2026-03-04", "pushed": "2026-10-07", "language": "Python", "topics": ["agent-skills", "claude-code", "claude-code-skill", "codex", "instagram", "knowledge-base", "markdown", "obsidian"]}
query: youtube transcript pushed:>{since} stars:>20

# Video Fetcher to Markdown

 
   
 

A video link in, a structured archival Markdown note out. Capture the transcript,
creator metadata, description, chapters, actual language, and provenance in one
Obsidian-ready file, without an API key. YouTube captions are read directly;
Instagram, TikTok, X, Vimeo, Facebook and other sites are transcribed on your own
machine with Whisper, with a contact sheet of frames for short videos.

```bash
npx skills add JimmySadek/video-fetcher-to-markdown
```

Read the [v2.0.0 release notes](https://github.com/JimmySadek/video-fetcher-to-markdown/releases/tag/v2.0.0)
for other video sites, local Whisper transcription, frames, and the login-wall fallback.

> **Formerly YouTube Fetcher to Markdown.** Existing installs keep working and keep
> updating: the skill is still named `youtube-fetcher`, and GitHub redirects the old
> address. `npx skills update` brings you the latest version.

An independent open-source tool, not affiliated with or endorsed by YouTube, Google, or
any other video platform it reads.

## What you get

Paste a YouTube link and receive a file such as:

```text
~/yt_transcripts/2026-03-04_obsidian-the-king-of-learning-tools_[hSTy_BInQs8].md
```

```markdown
---
title: "Obsidian: The King of Learning Tools (FULL GUIDE + SETUP)"
channel: "Odysseas"
url: "https://www.youtube.com/watch?v=hSTy_BInQs8"
video_id: "hSTy_BInQs8"
fetched: "2026-03-04"
source_project: "my-project"
language: "en"
caption_type: "manual"
duration: "36m 26s"
upload_date: "2024-04-24"
tags:
  - yt-transcript
---

# Obsidian: The King of Learning Tools (FULL GUIDE + SETUP)

## Video Details
| Field    | Value |
|----------|-------|
| URL      | https://www.youtube.com/watch?v=hSTy_BInQs8 |
| Channel  | Odysseas |
| Duration | 36m 26s |
| Uploaded | 2024-04-24 |
| Fetched  | 2026-03-04 |
| Source   | my-project |
| Language | en (manual) |

## Video Description
The creator's description, links, and chapter markers...

## Transcript
The complete caption text...
```

A video from another site gives the same kind of note, tagged `media-transcript`,
with `platform`, `creator`, `transcription_engine` and `transcription_model` in the
frontmatter, a **Frames** section that embeds the contact sheet with each tile's
time, and a Whisper transcript with timestamps:

```text
~/yt_transcripts/2026-10-07_claude-motion-tips_[instagram-dehp8dpsimi].md
~/yt_transcripts/2026-10-07_claude-motion-tips_[instagram-dehp8dpsimi].frames.jpg
```

The YAML frontmatter makes a collection queryable through tools such as
[Dataview](https://github.com/blacksmithgu/obsidian-dataview), while the Markdown
remains portable to Logseq, other knowledge bases, and plain text workflows.

## Why this exists

Most transcript extractors stop at raw caption text. An archival knowledge note
also needs the source URL, creator, capture date, actual language, description,
chapters, and a predictable filename. Video Fetcher to Markdown keeps that complete record
in one local file. Short social videos often show the real content on screen
(tool names, prompts, links) rather than saying it, so notes from those sites
include frames as well as words.

## Features

- Manual and auto-generated captions with optional timestamps
- Clickable timestamps and chapters that jump to the moment in the video
- Ordered language preferences, regional variants, automatic selection, and strict language matching
- Explicit YouTube translation, labeled with source language and machine-translat

## 4. [arxiv] MedZERO: Self-Evolving Agents for Open-Ended Medical Reasoning Through Controlled Knowledge Accumulation
key: arxiv:2610.08327
url: https://arxiv.org/abs/2610.08327
meta: {"published": "2026-10-06", "authors": ["Xilin Dang", "Weilin Ruan", "Xue Yang", "Jinghao Wang"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language models (LLMs) have shown promise in medical question answering and clinical reasoning, yet their improvement remains constrained by static parametric knowledge and costly expert supervision. Self-evolving agents offer a promising alternative by enabling models to improve through iterative task generation and problem-solving. However, most existing self-evolving methods are designed for easily verifiable domains such as mathematics and coding, where solutions can be checked by exact answers or executable programs. Medical reasoning is fundamentally different: it is open-ended, knowledge-intensive, and often only partially verifiable. We present MedZERO, a self-evolving framework for open-ended medical reasoning. MedZERO couples an Examiner that generates frontier medical question-option pairs with a Reasoner that solves them through evidence-grounded multi-turn reasoning with external knowledge tools. To support reliable, continual improvement, MedZERO adopts controlled knowledge accumulation, which maintains temporary exploratory knowledge and curated persistent knowledge in reasoning. We evaluate MedZERO on five public medical reasoning benchmarks using 4B- and 8B-scale base models under open-ended evaluation. Across all settings, MedZERO consistently outperforms the underlying base models and prior self-evolving baselines, achieving up to 13.7 average accuracy-point gains over the next-best self-evolving baseline.

## 5. [youtube] Anthropic Just Revealed 10 NEW Rules for Claude Skills
key: yt:VQyYzLJ6xos
url: https://www.youtube.com/watch?v=VQyYzLJ6xos
meta: {"channel": "Jay E | RoboNuggets", "rank": 1}
query: claude code skills workflow 2026


[body unavailable: IpBlocked]

## 6. [awesome] cooklang/cooklang-skills (new in awesome-claude-code)
key: gh:cooklang/cooklang-skills
url: https://github.com/cooklang/cooklang-skills
meta: {"list": "awesome-claude-code", "stars": 9, "created": "2026-01-22", "language": "Shell", "description": "Cooklang plugin for AI agents: 14 skills + the Cook MCP server. Claude Code plugin, Codex, Cursor, VS Code, Gemini CLI extension."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Cooklang Skills

Skills and an MCP server that let AI agents work with [Cooklang](https://cooklang.org) recipes: plain-text `.cook` recipes and `.menu` meal plans in a folder you own.

This repo packages two things for every agent client:

- **14 skills**: step-by-step guides the agent follows for writing, validating, searching, scaling, importing and exporting recipes, meal planning, shopping lists, pantry tracking, reports and nutrition.
- **The Cook MCP server** ([`@cookmd/mcp`](https://github.com/cook-md/cook-mcp)): the tools the skills call. It reads, searches, validates and writes your files, builds shopping lists, tracks a pantry and renders reports.

Everything runs locally and is free, with no account. Nutrition and importing from photos or social links use cook.md and need **Cook Basic** or **Cook Pro**.

The server runs through `npx`, so you need Node.js. Builds exist for macOS (arm64, x64) and Linux (x64, arm64). There are no Windows builds yet. The plugin manifests pin `@cookmd/mcp@0.2.3`; the snippets for other clients below use the latest release. Plugin setups need 0.2.2 or newer.

## Install

| Client | Skills | Cook MCP server |
|--------|--------|-----------------|
| [Claude Code](#claude-code) | plugin | plugin |
| [Codex](#codex) | plugin | plugin, plus `COOK_RECIPES_DIR` via `codex mcp add` |
| [Gemini CLI](#gemini-cli) | extension | extension |
| [Cursor](#cursor) | plugin or `skills/` copy | plugin, or install link |
| [VS Code / GitHub Copilot](#vs-code--github-copilot) | plugin | plugin, or install link |
| [Claude Desktop and other MCP clients](#claude-desktop-and-other-mcp-clients) | | JSON config |
| [Any agent, skills only](#skills-only) | `npx skills add` | |

### The recipe folder

The server works on one folder of recipes. It uses, in order:

1. `COOK_RECIPES_DIR`, if set in the server's config.
2. The workspace folder the client reports (MCP roots), which is the project you have open.
3. The folder the client started it in.

It ignores `/`, your home folder and plugin install folders (a plugin's server may be started inside the plugin's own folder). If nothing usable is left, recipe tools reply that no recipe folder is set and say why; set `COOK_RECIPES_DIR` to an absolute path in the server's config. So open your recipe folder in the client, or set the variable.

### Claude Code

```
/plugin marketplace add cooklang/cooklang-skills
/plugin install cooklang@cooklang-skills
```

The plugin adds the skills and starts the Cook server with your Claude Code project folder as the recipe folder. Check it with `/mcp` (look for `plugin:cooklang:cook`).

### Codex

```sh
codex plugin marketplace add cooklang/cooklang-skills
codex plugin add cooklang@cooklang-skills
```

The plugin adds the skills and the Cook server. Codex doesn't report a workspace folder to MCP servers and starts plugin servers inside the plugin's install folder, so the server can't find your recipes by itself. Tell it where they are:

```sh
codex mcp add cook --env COOK_RECIPES_DIR=/path/to/recipes -- npx -y @cookmd/mcp
```

A server you add yourself named `cook` takes the place of the plugin's `cook` server, so only one runs. Codex config has no way to set environment variables on a plugin's server (`[plugins."cooklang@cooklang-skills".mcp_servers.cook]` only takes `enabled`, tool approval and tool lists), which is why this is a separate server entry.

Without plugins, copy the skills instead: `cp -R skills/* ~/.agents/skills/`.

### Gemini

## 7. [vault] A high-impact news filter for the S1 crypto bot, skip or flatten entries in a window around high-impact USD events, scored on the paper record first
key: vault:2026-10-07:a-high-impact-news-filter-for-the-s1-crypto-bot-skip-or-flat
url: https://www.forexfactory.com/
meta: {"vault_status": "open", "kind": "tool", "subject": "forexfactory.com (economic calendar, forums, weekly JSON feed)", "date": "2026-10-07", "where": "TRITON-CORE/Research/links/2026-10-07-forexfactory.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Free feed, agent work on WF-0313, nothing live

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Free, broker-ad funded economic calendar with three-level impact ratings, plus forums, news and a trade explorer; no paid tier. A public weekly JSON feed answered without a login. Nothing to buy and nothing that is a lane. The one real use is a high-impact news filter for the S1 crypto bot, scored on the paper record, plus the week's high-impact events as a context line beside the eToro copy log. Job: Know when scheduled macro events will move crypto and the copied leaders (still open) Write-up: `TRITON-CORE/Research/links/2026-10-07-forexfactory.md` Link: https://www.forexfactory.com/

## 8. [hn] Show HN: Durable Actors – OSS Durable Objects with configurable compute
key: hn:49980399
url: https://github.com/TerseAI/durable-actors
discussion: https://news.ycombinator.com/item?id=49980399
meta: {"points": 30, "comments": 21, "created": "2026-10-06T15:58:19Z"}
query: mcp server

Hi HN, we're Thomas and Olivier from Terse ( https://www.useterse.ai/ ) We've built Durable Actors, an open-source alternative to Cloudflare's Durable Objects. A Durable Object/Actor is a tiny server that handles one request at a time and has its own SQLite database. There's exactly one of each in the world and it is addressed by name. This is the perfect primitive for deploying multiplayer agents. Each agent can have its own Durable Actor, and each user can connect to that Actor via websocket. This is fully horizontally scalable. Your users can deploy and share agents at will without putting pressure on a central DB or websocket server. Durable Actors are also great for coordinating agents within a system. Since only one request is handled at a time, you can protect critical data such as a CRM and allow multiple agents to run concurrently without worrying about data races. The only alternative to this is Cloudflare's Durable Objects. However, there is extreme lock in (they pull you into D1, R2 + workers as well) and it wasn't originally built for agentic workfloads when it was released 5 years ago. Some notable projects built on Durable Objects include RampInspect, OpenInspect as well as the multiplayer frameworks Liveblocks and PartyKit. You can now build these kinds of projects on Durable Actors. Durable Actors is a version of DO that is built for concurrent agentic workloads. It is fully open source (MIT License) and includes a helm chart for you to easily self-host. Some
comment (m1117): Great! Let’s have more cloudflare alternatives
comment (verst): How do you compare to Azure Durable Functions, Temporal, AWS Lambda Durable Functions? Can't Durable Entities meet the same use cases? EDIT: Of course I am not talking about the difference in OSS vs not. Rather I'm interested in the difference in use cases and capabilities. Some of the aforementioned have ways to run things locally as well, though they are designed as distributed cloud-based PaaS services.
comment (jeremycarter): Looks great but one of the common problems with the virtual actor model is state query. It's all well and good to have nice separated state dbs but for most use cases that means further double up on storing the state again in another database that can query it. I don't think anyone has come up with a nice solution for this problem without using a loose document database, but even then actors can change their schema. Perhaps emitting versioned domain events transactionally with the actor state is an option without prescribing an exact solution.

## 9. [github] GTKottman/mortiflix-oss: A motion design studio on your own machine: Claude makes the video step by step, you approve every stage. Bring your own Claude Code or API key.
key: gh:gtkottman/mortiflix-oss
url: https://github.com/GTKottman/mortiflix-oss
meta: {"stars": 371, "created": "2026-10-05", "pushed": "2026-10-07", "language": "JavaScript", "topics": ["ai-agents", "claude", "claude-code", "harness", "motion-design", "remotion", "video", "video-production"]}
query: claude-code created:>{since} stars:>20

Mortiflix 

  A motion design studio on your own machine.  
Claude makes the video step by step. You approve every stage. 

     
 ▶  Watch: How to use Mortiflix   (3:07). This video was made with Mortiflix. 

---

Most "AI video" tools are one prompt and a slot machine. Mortiflix works like a real motion design studio:
a brief, a script, style frames, a transition board, an animatic, a final, and **you review each stage** before the next one starts.
You pin a note on the exact spot of a frame or the exact moment of a video. The next version answers every note,
one by one, and shows you what changed.

It's built for **one person**: you write the briefs, you review every stage, and the studio runs on your machine.
The work is done by Claude through **your own Claude Code login or your own Anthropic API key**. Mortiflix is
the harness around it: the pipelines, the gates, the review room, and the memory that carries a project across
sessions and days.

```
 brief ──▶ script ──▶ style frames ──▶ animatic ──▶ build ──▶ final ──▶ delivered
   ▲          ▲            ▲              ▲                     ▲
   └── you ───┴──── you ───┴───── you ────┴──────── you ────────┘
       approve, pin notes, answer questions (the session stops at every gate)
```

## Why it's built this way

- **Sessions end at gates.** A Claude session works until it has something for you to review, submits it, writes a
  handoff and stops. When you respond, a fresh session picks up from the journal. Waiting on you costs nothing,
  for hours or for days.
- **The rules live in code, not in the prompt.** Only you can approve a step you review. A submission is refused if
  it doesn't report every error check for its kind of work, or if it doesn't answer each note you left on the last
  version. What you reviewed is copied out of the session's reach, so it can't change afterwards.
- **It learns your studio.** When you point out a real mistake, the session proposes a new check ("text never
  touches the frame edge"). Approve it once and every future video runs it. Your taste carries across projects in
  `TASTE.md`.
- **Pipelines are folders.** A pipeline is a `pipeline.json` (steps, how each is reviewed, the error checks), a
  `PIPELINE.md` (the craft), and skills. Anyone can write one: that's the point of open-sourcing it.

## Quick start

> **Tested mostly on Linux so far.** A Windows version is coming in the next two weeks (by October 20, 2026). macOS
> should mostly work but hasn't been tested yet.

You need **Node 20+** and **ffmpeg**. For real videos you also need one of:
- [Claude Code](https://claude.com/claude-code), logged in (your plan pays), or
- an [Anthropic API key](https://console.anthropic.com/) (you pay per token).

```sh
git clone https://github.com/GTKottman/mortiflix-oss.git && cd mortiflix-oss
npm install
npm link                 # puts `mortiflix` on your PATH (or use: node bin/mortiflix)

mortiflix init           # makes the studio folder (~/Mortiflix) and picks a backend it finds
mortiflix setup          # the walkthrough: Claude, narration, music, assets, 3D (asks before installing anything)
mortiflix demo           # a full walk-through with placeholder work: free, no Claude needed
```

Then either:

**A. In the terminal**

```sh
mortiflix new explainer          # asks the brief's questions
mortiflix run                    # sessions run until something waits on you
mortiflix review                 # read the note, answer questions, pin notes, approv

## 10. [arxiv] M3SunAgent: Monocular 3D Spatial Understanding Agent for Metric Depth Estimation and 3D Visual Grounding
key: arxiv:2610.07982
url: https://arxiv.org/abs/2610.07982
meta: {"published": "2026-10-06", "authors": ["Jinsong Zhang", "Kejun Wu", "Ming Zhu", "Renjie Qiao"], "categories": ["cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Monocular metric depth estimation and 3D visual grounding represent the two complementary cornerstones of monocular 3D spatial understanding (M3Sun), from which the fundamental 3D spatial information required by M3Sun can be acquired. However, these complementary tasks are generally conducted by separate frameworks, which pose challenges of inflexible and unaligned spatial information access for embodied intelligence systems. In this paper, we propose a unified agent for monocular 3D spatial understanding (M3SunAgent) that leverages a large language model (LLM) as a task planner for spatial visual programming, which flexibly generate structured programs and coordinate tools. For instance-level metric depth estimation task, M3SunAgent invokes an object detector tool to locate the target, estimates depth at selected points with a depth estimation tool, and aggregates these predictions into an instance-level depth estimate. We also construct the M3Sun Instance (M3SI) dataset, a benchmark with 2,910 samples for evaluation. For monocular 3D visual grounding task, M3SunAgent uses a vision-language model (VLM) tool to locate the target and output basic spatial attributes, then combines back-projection tool with a dimension-lifting tool to predict its 3D bounding box. Experimental results demonstrate the superior performance of M3SunAgent. Specifically, in evaluations of instance-level monocular metric depth estimation, M3SunAgent achieves the best performance among all compared models, 52.61% of predicted instances are distributed below depth error 0.25 ($δ< 0.25$). In evaluations of monocular 3D visual grounding, M3SunAgent demonstrates overall competitive performance than vision and VLM models, reaching a 3D mean intersection over union (mIoU) of 41.73% and exceeding the state-of-the-art MonoVLM model by 3.62%.

## 11. [youtube] MCP Tutorial: Build Your First MCP Server and Client from Scratch (Free Labs)
key: yt:RhTiAOGwbYE
url: https://www.youtube.com/watch?v=RhTiAOGwbYE
meta: {"channel": "KodeKloud", "rank": 3}
query: mcp server build tutorial


[body unavailable: IpBlocked]

## 12. [awesome] cvelasquez/agent-workbench (new in awesome-claude-code)
key: gh:cvelasquez/agent-workbench
url: https://github.com/cvelasquez/agent-workbench
meta: {"list": "awesome-claude-code", "stars": 5, "created": "2026-09-19", "language": "TypeScript", "description": "One local UI for the Claude Code, Codex, OpenCode and Antigravity CLIs: tabs, browsable history, conversations as cards, handoff between CLIs, global search, context meter, git and file tree. Never touches your credentials."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Agent Workbench

[](https://www.npmjs.com/package/agent-workbench)
[](https://github.com/cvelasquez/agent-workbench/actions/workflows/ci.yml)
[](LICENSE)

**One local interface for the Claude Code, Codex, OpenCode and Antigravity
CLIs.** It uses the CLIs you already have logged in, never touches your
credentials, and makes no network calls of its own.

```bash
npx agent-workbench
```

It doesn't talk to any API. It launches the CLI you already have installed and
logged in —`claude`, `codex`, `opencode` or `agy`— inside a pseudo-terminal, and
adds around it what a terminal alone doesn't give you: tabs, browsable history,
the conversation as cards, a context meter, git status and a file tree.

The terminal is still the terminal. Everything you type reaches the CLI without
the app touching it.

---

## What it does

| | |
|---|---|
| **Tabs** | Several live sessions at once, from any of the CLIs, each in its own directory. They survive an `F5`: the processes live on the server, not in the browser tab. Each tab's dot tells you whether the agent is working, idle or waiting for an answer, on the CLIs that publish their status ([below](#multiple-clis)). |
| **Zero-cost startup** | When you open the app, tabs come back as **sleeping tabs**: you can read them in full, and they don't launch any CLI. You open the CLI with a button when you want to write to the agent. |
| **History** | Your projects and past conversations in the sidebar, with a filter, and those of all four CLIs together under each project, each with its badge. Opening one resumes it with its CLI, in the same session. **Archive history…** hides a CLI's sessions from before today in one go, and each project can be archived whole with one button: nothing is deleted, and both can be undone. |
| **Conversation** | The active session's messages, live, with tool calls collapsed and their results inside. A row at the bottom tells you when your message reached the CLI, whether the agent is working and, with Claude Code, which subagents are still at it after the agent finished its turn. Search, jump between matches and back to the end, copy any message or code block and, depending on the CLI, answer the agent's questions from the chat. |
| **Continue with…** | With more than one CLI installed, a conversation can be continued with another CLI in the same folder. The new agent starts from a transcript of the last turns, not from the context the previous one had. |
| **Search everything** | With more than one CLI and something saved in the backup, the sidebar filter also searches the text of every saved conversation, not just their titles. |
| **Context meter** | Tokens from the last request against the model's context window. Tokens, never money. |
| **Changes** | Branch, ahead and behind against the upstream branch, worktrees, and the changed files with their diff. **Read-only.** |
| **Files** | The tree of the tab's directory, with search by name and a preview with syntax highlighting. A button on each row puts its path in your message, without touching the clipboard. A context menu to copy paths, insert them as `@path` or open the file with the system's default app. |
| **Plans** | The documents written by that conversation, rendered: the plans from plan mode, and also the `.md` files the agent created inside the project or in the session's temp folder. Only those named by the conversation you're viewing. |
| **Shared memory** | What agents learn about a project, in `.agents/memory/`, re

## 13. [vault] Build a mock-up site for the prospect and send a 90-second Loom after a two-line permission ask
key: vault:2026-09-20:build-a-mock-up-site-for-the-prospect-and-send-a-90-second-l
url: https://www.youtube.com/watch?v=aidr_Ny1rvI
meta: {"vault_status": "open", "kind": "idea", "subject": "\"First AI agency client without a portfolio\" videos (The Savvy Couple and eight neighbours)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-first-ai-agency-client-videos.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Shows the fix rather than describing the gap; consent-first sequencing is workable under PECR

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Nine videos teach the same five-step method with the same unevidenced claims. Torn down once against the agency lane. Do not re-watch any of them. Job: Win a first agency client with no portfolio and no case study (still open) Write-up: `TRITON-CORE/Research/links/2026-09-20-first-ai-agency-client-videos.md` Link: https://www.youtube.com/watch?v=aidr_Ny1rvI

## 14. [hn] Show HN: Agent.reviews – Where AI agents read and write reviews on tools
key: hn:49995539
url: https://agent.reviews/
discussion: https://news.ycombinator.com/item?id=49995539
meta: {"points": 21, "comments": 28, "created": "2026-10-07T16:59:11Z"}
query: claude code

Hi HN! I’m Louis, Co-Founder of Armature (YC P26), where we help teams make their product discoverable and usable by coding agents. We already measured 50k+ agent sessions and realized that over and over agents would encounter the exact same limitations on different tasks using the same tool. So we wondered why these weren’t fixed. And the answer is simple: the feedback loop just doesn’t exist between agents and software vendors but also between different agents. Humans can share their experience on platforms like https://g2.com and https://trustpilot.com , but agents have nowhere to. So we created: https://agent.reviews : the G2 for agents. It works with a set of skills and an npm CLI (@armature-tech/agent-reviews) connecting agents to our API endpoints. Anyone can ask their agent (Claude Code, Codex, Cursor, etc.) to install it, and agents will naturally check reviews before picking a tool and post their own after using one. As usual, privacy was our main concern, so we added 3 layers before a review gets posted: Deterministic rules filtering secrets, PII, URLs, etc. A Jev classifier trained to detect any leak after the first check A small LLM checking each review to make sure nothing was missed We've been sharing this project around for a few weeks now and gathered thousands of reviews already. There are already interesting ones, for example: - A Claude Code agent noticed that the Stripe SDK systematically crashed when the API key was missing on the health check page (whil
comment (schleck8): They are so real for giving uv a 4.7/5, it changed how I view python. fantastic design philosophy https://agent.reviews/packages/uv#review-c63f7e0f-5c72-41d2-...
comment (tomhow): [stub for offtopicness]
comment (klntsky): What is the incentive for me to spend my tokens on submitting reviews?
