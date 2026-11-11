# Harvest brief, 2026-11-11

14 items shortlisted from 387 candidates (301 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] parallel tasks plus one-prompt CRM and dashboard builds
key: vault:2026-11-11:parallel-tasks-plus-one-prompt-crm-and-dashboard-builds
url: https://www.instagram.com/p/DfmyrUTgSmi/
meta: {"vault_status": "open", "kind": "tool", "subject": "Abacus AI Agent (agent.abacus.ai)", "date": "2026-11-11", "where": "TRITON-CORE/Research/links/2026-11-11-abacus-ai-agent-promo.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: check if any claim beats current builds, only if slide 7 shows something specific

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) untested, overlaps Claude Code builds Write-up: `TRITON-CORE/Research/links/2026-11-11-abacus-ai-agent-promo.md` Link: https://www.instagram.com/p/DfmyrUTgSmi/

## 2. [hn] Show HN: Yogurt – Free, private, open-source alternative to Granola
key: hn:50454625
url: https://github.com/FrigadeHQ/yogurt
discussion: https://news.ycombinator.com/item?id=50454625
meta: {"points": 148, "comments": 68, "created": "2026-11-11T15:33:06Z"}
query: mcp server

Hey HN, I’m Eric and I want to share an OSS project that I’ve been building in my free time. Yogurt is a free, MIT licensed desktop app that uses on-device AI models to transcribe, summarize, and chat with your meetings. Here's a quick demo video: https://www.youtube.com/watch?v=BFfbXAwRq98 Similar to Granola, Yogurt runs in the background and does not join your calls. But unlike Granola, Yogurt is open-source, free to use, and private. Your meeting transcripts, call recordings, and summaries never leave your computer. As small OSS models have gotten faster and more powerful, Yogurt seemed like a pretty obvious win for privacy and cost conscious folks. You do not need a frontier model to summarize meeting notes or answer questions about them. And if you want to make your notes available to a frontier model, you can just share it with Anthropic, OpenAI, etc. directly via Yogurt’s local MCP server. There’s no need to use a paid cloud service as a middleman. I tried some of the most popular OSS note taking tools, and most were missing features like calendar integration, MCP server, etc. or required you to connect or create an account. And more than that, they didn’t feel polished enough for it to be something I actually wanted to use daily, and so I built Yogurt to scratch that itch. I spent a lot of time fine-tuning every UI interaction/animation and optimizing the model calls to get the most out of your hardware + make it snappy. To support Windows/Mac/Linux, I decided to go w
comment (kokugle): Been waiting for this for so long. very cool product
comment (anoojb): looks amazing! if you used AI coding agents to build this, any reason why you couldn't refactor this to use gpui or rune to still get cross platform but have better performance?
comment (arjgoel30): Love the name

## 3. [github] alexeyw/lot-map: A live map beside the chat that shows what Claude Code is doing: tool calls, model steps, hooks, skills and subagents light up as they happen. Local only, in five languages.
key: gh:alexeyw/lot-map
url: https://github.com/alexeyw/lot-map
meta: {"stars": 389, "created": "2026-11-09", "pushed": "2026-11-11", "language": "TypeScript", "topics": ["agent-observability", "ai-agents", "claude", "claude-code", "claude-code-plugin", "developer-tools", "svg-animation", "typescript"]}
query: claude-code created:>{since} stars:>20

# lot-map

A mod for Claude Code: a live map of the work, in a pane beside the chat. Every tool call, model step, hook and skill sends a pulse from the centre to its station, so you see memory, files, shell, web and agents at work instead of reading a list of commands.

*A made-up session replayed through the mod's own drawing code.*

## Install

At the prompt of a terminal session:

```
/plugin install lot-map --marketplace alexeyw/lot-map
```

Answer `y` to add the marketplace, then choose a scope. From a shell:

```bash
claude plugin install lot-map --marketplace alexeyw/lot-map
```

In the desktop app: click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `alexeyw/lot-map`, then **Add plugin**.

The pane opens by itself when a session starts. In a terminal it needs at least 144 columns and draws text only; otherwise type `/lot-map`. Built and tested on Claude Code 2.1.321 on macOS; users report it working on Windows as well.

## Updating

From a shell:

```bash
claude plugin marketplace update lot-map
claude plugin update lot-map@lot-map
```

Then start a new session. The first command is needed: without it the second one reports the installed version as the latest.

What each version changed is in [CHANGELOG.md](CHANGELOG.md).

## What lights up

| Station | When |
| --- | --- |
| You | your messages, questions and files sent to you |
| Model | each model request, context compaction |
| Memory | Claude Code's memory folder, plus whatever you name in the options |
| Files | Read, Write, Edit, Grep, Glob, and shell commands that work on files and nothing else: they read, search, move, delete or edit in place (`cat`, `grep`, `mv`, `sed -i`, `tee`, `find … -delete`) |
| Shell | every other shell command |
| Network | web fetch and search, MCP servers, and shell commands known to reach the network: `curl`, `gh`, `ssh`, `rsync`, `git push`, `npm install`, `docker pull` and the like, also inside `$(…)` |
| Browser | browser tools |
| Agents | subagents and workflows; their own calls start from this station |
| Skills | skills and tool search |
| Hooks | settings hooks that refuse a call, ask for permission, add context or take a moment |

On Windows the PowerShell tool is read the same way as Bash, with PowerShell's own names: `Get-Content` and `Select-String` light Files, `Invoke-WebRequest` lights Network. A program run by its full path is read by its name, also from a quoted path with a space, and `CURL.EXE` is `curl`.

The shell stations go by the command's name, not by what it does: a script that opens a connection itself, such as `python -c "…"`, shows as Shell.

A pulse flies out when something starts and returns when it ends. Refusals and errors turn red.

## Reading the map

- **The route.** A thin line joins the last few stations the main loop went through, in order, and its newest leg draws itself. A leg stays for 40 seconds and then fades over 20, so a minute after the work stops only the spokes are left; their thickness keeps where the work went. Model steps are left out, or every leg would pass through Model.
- **Worn spokes.** A spoke grows thicker and brighter the more its station is used, so at the end of a session the map shows where the work went.
- **How long.** Two clock hands grow around a station while a call runs: the inner one goes round in a minute, the outer one in ten.
- **Background work.** A command sent to the background, a monitor, a background subagent or a workflow stays lit on it

## 4. [arxiv] ReTrace: Distilling Tool-Using Agents into Planner-Free Workflows
key: arxiv:2611.14492
url: https://arxiv.org/abs/2611.14492
meta: {"published": "2026-11-10", "authors": ["Kaiyuan Hou", "Yang Ping Kuo", "Indranil Bhattacharya", "Rohith Nama"], "categories": ["cs.AI", "cs.LG", "cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Business process automation runs the same Standard Operating Procedure (SOP) again and again on new inputs. Large Language Model (LLM) agents can follow an SOP written in natural language, but they call an LLM to choose every step of every run, which adds latency and cost at scale. We present ReTrace, which turns an SOP and a few logged agent runs into a reusable workflow in which code, not an LLM, selects the next step. The agent's reasoning, the explanation it writes with each tool call, often states why it took an action; the tool calls alone do not. ReTrace extracts the condition behind each step, merges these conditions across runs into a compact rule document, and generates an executable workflow from it. Only this last stage depends on the platform, so rule documents can be compiled for different orchestration platforms. On $79$ procedures from our production platform, ReTrace workflows reach $93.8\%$ completion, against $96.8\%$ for the agent, at $24\%$ lower cost per task. On $τ^2$-Bench, they reach $75.8\%$ task success (agent: $80.6\%$) and run in $1.3$s instead of $170$s; three rounds of repair on training failures lift $k{=}2$ workflows from $66.7\%$ to $81.2\%$. On eight SOP-Bench procedures, ReTrace without repair trails few-shot generation ($80.6\%$ vs. $83.6\%$), but repair from labeled training failures lifts it to $87.8\%$ at $0.40$s per task, compared to $85.5\%$ in $46.6$s for the agent.

## 5. [youtube] EV Depreciation Is Unbelievable Right Now 😮
key: yt:1ZUZEYi5538
url: https://www.youtube.com/watch?v=1ZUZEYi5538
meta: {"channel": "HeelToe", "rank": 2}
query: car depreciation data analysis


[body unavailable: IpBlocked]

## 6. [vault] pain-first hook plus five-bullet outcome list for a niche community
key: vault:2026-11-11:pain-first-hook-plus-five-bullet-outcome-list-for-a-niche-co
url: https://www.instagram.com/p/Den4ud4sOgC/
meta: {"vault_status": "open", "kind": "service", "subject": "Skool: Claude Code Club promo", "date": "2026-11-11", "where": "TRITON-CORE/Research/links/2026-11-11-skool-claude-code-club.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: test on a Neptune community offer

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) mechanism noted, community unassessed Write-up: `TRITON-CORE/Research/links/2026-11-11-skool-claude-code-club.md` Link: https://www.instagram.com/p/Den4ud4sOgC/

## 7. [hn] Show HN: Black Ops II statically recompiled to native ARM64 macOS
key: hn:50449891
url: https://github.com/adrbn/bo2-mac
discussion: https://news.ycombinator.com/item?id=50449891
meta: {"points": 137, "comments": 60, "created": "2026-11-11T04:56:47Z"}
query: claude code

I grew up with Black Ops 2 and wanted to see if I could make it work on my 2020 MacBook Pro. So I used Claude Opus 5.5 to create a tool that converts your copy of the game (from Steam) to a native ARM64 Mac app, with almost 60fps in all areas. The whole game is statically recompilated ahead-of-time (AOT) and does not use any emulator whatsoever, be it Wine, Crossover or Rosetta. The best thing is the performance, although some heat issues are still to fix. You get to play the whole Campaign, local Multiplayer (with bots) and local Zombies (all DLCs maps; you need to have them in your Steam library obviously) at about 60fps. Split-screen was not in the PC version, but I've been working on it lately; it's coming soon! LAN mode is on the roadmap for later too :)
comment (phaser): what was your workflow for creating this? there's now extra guardrails around decompiling / reverse engineering, do you think this is still possible to do or were you just lucky enough to do it before the guardrails?
comment (Benard-dev): This is great, I also grew up on Black Ops 2. How big is the recompiled binary compared to original?
comment (cedws): How does it actually recompile, does it use an existing tool? I can’t imagine the agent combs through every routine and hand translates the assembly.

## 8. [github] vzroslieigry/maxagent: Experience for AI agents: hooks that make Claude Code, Codex, Antigravity and OpenClaw recall and record what worked, plus maxagent-bridge for your own Chrome.
key: gh:vzroslieigry/maxagent
url: https://github.com/vzroslieigry/maxagent
meta: {"stars": 265, "created": "2026-11-08", "pushed": "2026-11-10", "language": "JavaScript", "topics": []}
query: claude-code created:>{since} stars:>20

# maxagent

[Русский](README.ru.md)

Experience-first operating rules for every AI agent on your machine — Claude Code, Codex, Antigravity, OpenClaw.

Agents keep solving the same problem from scratch: they search, try, fail and find the way again, every session. maxagent gives all of them **one workspace**: an **experience** base of short, checked recipes ("atoms"), projects that remember where work stopped, and the same rules before every task. Hooks surface the right atom by themselves — on your message, before a command, after an error — so an agent does it the known way instead of guessing.

| Package | What it is |
|---|---|
| [`maxagent`](packages/maxagent) | rules, workspace, experience engine, hooks for each agent, setup wizard |
| [`maxagent-bridge`](packages/maxagent-bridge) | "hands" for agents: an MCP server that drives **your own** Chrome (your profile, your sign-ins) through a small extension — no open port, per-agent approval, site blocklist, action log, stop button |

## Install

Say it to your agent in one phrase:

> Install maxagent: run `npx maxagent init`. Without a terminal it prints the questions: ask me all of them, choose nothing for me and skip nothing, then pass me its report.

Or run it yourself:

```
npx maxagent init
```

Node.js 18+ is the only requirement. Nothing runs at `npm install` time (npm v12 does not run install scripts, and we do not need them): everything heavy is downloaded by the wizard, and only after you say yes.

## What the wizard sets up

1. **Workspace** (`~/maxagent` by default): `AGENTS.md`, `experience/`, `projects/`, `sync.md`, `inbox/`. These files are yours — updates never overwrite them. Optionally a private Git repository for sync.
2. **Rules and hooks** for every agent it finds (Claude Code, Codex, Antigravity, OpenClaw): a short marked block in each agent's global rules file and hooks that surface experience on every turn. Your own rules and hooks stay untouched; every edited file gets a backup first.
3. One question — **"Install everything / Choose / Nothing"** — for the extras:
   - **Browser bridge and Chrome extension** (`npx maxagent bridge`). The extension is loaded unpacked for now: three clicks in `chrome://extensions` (Developer mode → Load unpacked → the folder). The wizard waits until the bridge connects.
   - **Meaning search** (`npx maxagent vectors`, ~270 MB): the `multilingual-e5-small` model (pinned revision, checked by sha256) and its Python libraries in `~/.maxagent/vector`. Without Python the wizard offers to install it (on Windows via `winget`, after a separate yes); without it search works by words only.
   - **Shared experience packs** (`npx maxagent experience add all`).
4. A summary: what is on, what was skipped and the command to turn it on later.

| Command | What it does |
|---|---|
| `npx maxagent init` | first-time setup |
| `npx maxagent setup` | change settings |
| `npx maxagent doctor` | what is installed and whether it is healthy |
| `npx maxagent update` | update rules, hooks and agent blocks; your workspace is untouched |
| `npx maxagent bridge` · `vectors` | install an extra later |
| `npx maxagent experience list \| add  \|all \| update \| mute   \| adopt " "` | shared experience |
| `npx maxagent uninstall` | remove blocks and hooks from agents; your workspace stays |

## Two shelves of experience

- **Your own** — `experience/` in your workspace. Written by your agents as they work, in the format of `experience/_spec.md`. Your atoms surfac

## 9. [arxiv] Coding Agent Memory Post-Training II: Unlocking the Memory Potential of Pre-trained File Operations for Long-Horizon Tasks via On-Policy Distillation
key: arxiv:2611.14009
url: https://arxiv.org/abs/2611.14009
meta: {"published": "2026-11-10", "authors": ["Lirui Luo", "Kelong Mao", "Xinwei Yang", "Rongqing Li"], "categories": ["cs.LG", "cs.AI", "cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Language-model agents increasingly tackle long-horizon tasks whose interaction histories exceed the model's active context. They must therefore decide what to write down and what to read back, and when to do either. Recent work has begun to use on-policy distillation (OPD) to make memory control part of the policy, relying on memory tools and compaction protocols that lie outside either model's pre-training. However, this weakens the distillation on both sides: the teacher cannot give useful guidance on an interface it has never used, and the student samples too few meaningful memory actions for that guidance to take effect. To study this problem, we introduce Coding Agent Memory Gym II (CAMG-II), a suite of long-horizon agentic-RL environments spanning Shop, Coding, AutoResearch, General, and Visual. Alongside each environment's native task interface, CAMG-II provides ordinary Bash access and an episode-persistent workspace, enabling the policy to create, revise, search, and reuse files as memory across context replacements. We also introduce Coding Agent Memory Post-Training II (CAMP-II), which trains a single policy jointly across all five environments with fully asynchronous OPD to learn this file-based memory behavior directly from a frozen teacher with a prior for file operations. On CAMG-II, CAMP-II obtains 2.97 times the gain of the strongest OPD baseline. The memory behavior CAMP-II learns generalizes to two external benchmarks, Terminal-Bench 2.1 and SWE-Bench Pro V2, with improved success rates.

## 10. [youtube] The Truth About Luxury Car Depreciation and Personal Finance
key: yt:t6QTmKIV4J8
url: https://www.youtube.com/watch?v=t6QTmKIV4J8
meta: {"channel": "Carbiscuit", "rank": 3}
query: car depreciation data analysis


[body unavailable: IpBlocked]

## 11. [vault] comment-for-DM-link funnel (same poster as the NVIDIA free models post)
key: vault:2026-11-11:comment-for-dm-link-funnel-same-poster-as-the-nvidia-free-mo
url: https://www.instagram.com/p/DfmyrUTgSmi/
meta: {"vault_status": "intel", "kind": "tool", "subject": "Abacus AI Agent (agent.abacus.ai)", "date": "2026-11-11", "where": "TRITON-CORE/Research/links/2026-11-11-abacus-ai-agent-promo.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: understand it, never operate it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) untested, overlaps Claude Code builds Write-up: `TRITON-CORE/Research/links/2026-11-11-abacus-ai-agent-promo.md` Link: https://www.instagram.com/p/DfmyrUTgSmi/

## 12. [hn] Show HN: Klad, a paint app your coding agent can drive (source-available)
key: hn:50454951
url: https://github.com/klad-app/klad
discussion: https://news.ycombinator.com/item?id=50454951
meta: {"points": 68, "comments": 28, "created": "2026-11-11T16:00:50Z"}
query: claude code

I've been developing applications for a long time and have turned to game development as well lately. One of the things that frustrated me the most was that using AI agents for game development is very annoying in the art department. Your only options right now are to either use an image genAI model and roll the dice every time you want to make an edit, or have your agent draw with something like vectors. I was looking for an application that would allow me to ask an agent to make a first draft of whatever art I needed with actual brushes, and then be able to go in myself and edit every last stroke or layer that it created. Klad is that application. Written in Rust, it can be fully controlled by an agent through the CLI, and every function is available in a nice UI as well: a brush engine, frame-by-frame animation (and bones/IK), vectors, text layers, colours, layer effects, infinite undo (even after re-opening the file!),… Why I think it's useful for a wider audience: Adobe showed agents editing Photoshop files at MAX this week, with a private beta planned for early 2027. Klad is built on the same core idea, with editable paint strokes as core architecture, and it works today. Clone the repo to try it out: https://github.com/klad-app/klad You can basically point Claude to the repo, ask it to build it, and pick up the drawing skills. Then ask it to make any drawing you want! (After that, you or the agent can change absolutely every brush stroke in the app again, which makes e
comment (chaostheory): In the future, I wonder if agents will still try to leave some sort of hard to detect “watermark” using this new generation of tools? This is a really great tool that solves a specific pain point with image models though
comment (geooff_): Very cool. Can't wait to try this!
comment (tamimio): This looks very interesting, so the outputs are svg? Will definitely give it a try

## 13. [github] nishant-Tiwari24/cracked: Skills for getting hired. Company-wise mock interviews, OAs with hidden tests and brutal resume roasts for 470+ companies, straight from your terminal.
key: gh:nishant-tiwari24/cracked
url: https://github.com/nishant-Tiwari24/cracked
meta: {"stars": 252, "created": "2026-11-06", "pushed": "2026-11-06", "language": "TypeScript", "topics": ["agent-skills", "ai-agents", "ats", "career", "claude-code", "claude-skills", "codex", "coding-interview"]}
query: claude-code created:>{since} stars:>20

# Skills For Getting Hired

[](https://github.com/nishant-Tiwari24/cracked/stargazers)
[](https://github.com/nishant-Tiwari24/cracked/releases)
[](https://github.com/nishant-Tiwari24/cracked/actions/workflows/validate.yml)
[](#reference)
[](./skills/core/company-intel/SKILL.md)
[](LICENSE)

Agent skills for tech placements and coding interviews. Straight from your terminal.

**[cracked-skills.vercel.app](https://cracked-skills.vercel.app)**: browse every skill, and search 470+ companies' most-asked questions.

**cracked** turns Claude Code, Codex, Cursor, GitHub Copilot or Gemini CLI into your **interviewer, coach and career team**: company-wise mock DSA interviews for Google, Amazon, Microsoft, Flipkart and 470+ more; timed online assessments graded against hidden test cases; system design and HR rounds; a brutal resume roast with an ATS score; and a prep plan built from your real weak spots.

**Built for** final-year and pre-final-year CS students preparing for campus placements, new grads applying off-campus, and engineers switching jobs.

 
   
 

Preparing for tech interviews is hard. Sheets, courses and grind lists try to help by handing you a list of 450 problems. But a list doesn't interview you, doesn't tell you *why* you'd be rejected, and has no idea which company you're walking into on Monday.

These skills are small, composable and honest. They work with any model. They run your code instead of guessing about it. They never invent a single fact about you. Hack around with them. Make them your own.

## Installation (30-second setup)

A plugin updates itself. [skills.sh](https://skills.sh) copies editable files into your setup, and you update them by hand. Pick one per agent, because installing both gives you every skill twice.

### 1. Get the skills

 
  Claude Code  

```bash
claude plugin marketplace add nishant-Tiwari24/cracked
claude plugin install cracked@cracked
```

Updates itself by default.

 

 
  Codex  

```bash
codex plugin marketplace add nishant-Tiwari24/cracked
codex plugin add cracked@cracked
```

 

 
  Any other agent, or editable files  (manual updates) 

```bash
npx skills@latest add nishant-Tiwari24/cracked -a    # cursor, copilot, gemini, opencode, windsurf, amp…; omit -a to choose
```

When the installer asks which skills to take, include `setup-cracked` and `cracked-profile`. To update, run `npx skills@latest update`.

 

 
  Using cracked in agents without a Skill tool  

Skills hand off to each other ("Call the Skill tool with `company-intel`"). Claude Code and Codex do this natively. In other agents, the skills tell the model to open the named skill's `SKILL.md` and follow it, so install the whole pack, not single skills, and always include `cracked-profile`.

 

### 2. Run `/setup-cracked`

Run it once. It will:

- Ask up to six short questions (status, target roles, target companies, language, DSA level, deadline) and save your profile
- Build a prep brief for each target company
- Check your machine for the tools some skills use (Python, SQLite, `gh`, text-to-speech)
- Suggest your first three sessions

### 3. Bam, you're ready to go.

```text
> roast my resume ~/Downloads/resume.pdf
> mock interview for Google, medium, voice mode
> /oa-sim Amazon
```

## Why These Skills Exist

I built these skills to fix the ways interview prep fails the people doing it.

### #1: Practice Doesn't Feel Like The Real Thing

> "Everybody has a plan until they get punched in the mouth."
>
> Mike Tyson

**The Prob

## 14. [youtube] Why Does Your Car Lose Value Every Year? 🚗 | Depreciation Explained
key: yt:baChlHk8HQw
url: https://www.youtube.com/watch?v=baChlHk8HQw
meta: {"channel": "Accountonic", "rank": 4}
query: car depreciation data analysis


[body unavailable: IpBlocked]
