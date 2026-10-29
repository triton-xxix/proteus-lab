# Harvest brief, 2026-10-29

14 items shortlisted from 354 candidates (240 dropped as already seen, 12 carry a vault verdict on the vendor).

## 1. [vault] Pinokio one-click installer
key: vault:2026-10-29:pinokio-one-click-installer
url: https://www.instagram.com/p/DfEUO_VH3ip/
meta: {"vault_status": "open", "kind": "tool", "subject": "alamin.8020ai local AI video carousel (Pinokio + Wan2GP)", "date": "2026-10-29", "where": "TRITON-CORE/Research/links/2026-10-29-alamin-local-ai-video-pinokio-wan2gp.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: fastest way to set up Wan2GP on a rented NVIDIA GPU for the cost-per-clip test against fal

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Accurate how-to for NVIDIA PC owners; needs an RTX-class card none of our Macs have. Pinokio is the one new piece: a quick way to stand Wan2GP up on a rented GPU. Savings claim is sales copy. Write-up: `TRITON-CORE/Research/links/2026-10-29-alamin-local-ai-video-pinokio-wan2gp.md` Link: https://www.instagram.com/p/DfEUO_VH3ip/

## 2. [hn] Claude Code regularly sends each background agent’s transcript to its model
key: hn:50284255
url: https://gist.github.com/flamerix-ai/c3905705cc4205e5de3011fa2e74efce
discussion: https://news.ycombinator.com/item?id=50284255
meta: {"points": 558, "comments": 224, "created": "2026-10-29T03:33:42Z"}
query: claude code

comment (NikZaal): Claude Code's (CC) status summaries used 16.4% of our token spend in a week! We have investigated a source of overhead in CC: it's an agent_summary query that calls your current session/subagent model approximately every 30 seconds for a few words in CC’s status line. Our DRIM system flagged the anomaly in CC's OTEL traces. Grouping requests by query_source showed that over one measured week agent_summary accounted for: 16.4% of total estimated spend (versus 15.7% for the main conversation), and 19.7% of all API requests with approximately 9,000 input tokens per output token. Most requests reu
comment (messh): Bloat. I like Pi much better with it's minimalism
comment (rsalus): does this happen for Claude Desktop too?

## 3. [github] qybaihe/bla: 🛡️ BLA (Blind LLM Agents) — Adversarial defense shield that protects binaries, Electron apps, JS bundles, Python, and WebAssembly against AI reverse-engineering agents like REA. Poison -> Exhaust -> Hallucinate.
key: gh:qybaihe/bla
url: https://github.com/qybaihe/bla
meta: {"stars": 727, "created": "2026-10-25", "pushed": "2026-10-29", "language": "TypeScript", "topics": ["adversarial-ai", "claude-code", "cursor", "electron-security", "llm-security", "mcp", "mcp-server", "obfuscation"]}
query: claude-code created:>{since} stars:>20

**English** · [简体中文](docs/readme/README_zh.md) · [繁體中文](docs/readme/README_zh-TW.md) · [日本語](docs/readme/README_ja.md) · [한국어](docs/readme/README_ko.md) · [Türkçe](docs/readme/README_tr.md) · [Русский](docs/readme/README_ru.md) · [Tiếng Việt](docs/readme/README_vi.md) · [ไทย](docs/readme/README_th.md) · [Deutsch](docs/readme/README_de.md) · [Español](docs/readme/README_es.md) · [Français](docs/readme/README_fr.md) · [Українська](docs/readme/README_uk.md) · [Polski](docs/readme/README_pl.md) · [Português (Brasil)](docs/readme/README_pt-BR.md) · [العربية](docs/readme/README_ar.md) · [فارسی](docs/readme/README_fa.md) · [Bahasa Indonesia](docs/readme/README_id.md) · [Italiano](docs/readme/README_it.md) · [Ελληνικά](docs/readme/README_el.md) · [മലയാളം](docs/readme/README_ml.md) · [Roman Urdu](docs/readme/README_ur-Latn.md) · [Română](docs/readme/README_ro.md)

#   BLA: Blind LLM Agents

### Make reverse engineering bankrupt again.

**Point BLA at the build you ship. When an AI reverse-engineering agent (REA) opens it, the analyzer hits resource budgets, follows decoys, and burns tokens — while your users still get the same runtime behavior.**

[](https://www.npmjs.com/package/bla-agents)
[](docs/cli-and-mcp.md)
[](#format-coverage)
[](#empirical-results-vs-real-rea)
[](LICENSE)

**[Website](https://bla.tools/) · [Guides](https://bla.tools/guides/) · [Showcases](https://bla.tools/showcase/) · [Disclaimer](DISCLAIMER.md)**

[Quick start](#quick-start) · [Empirical results](#empirical-results-vs-real-rea) · [Format coverage](#format-coverage) · [Benchmark](#benchmark-14-targets-internal-estimates) · [FAQ](#faq)

```bash
bla harden .
# or tell your agent: "Harden my software against REA"
```

 

> [!IMPORTANT]
> BLA is a **defensive** tool for protecting **your own** software. See [DISCLAIMER.md](DISCLAIMER.md).
> Get BLA from [qybaihe/bla](https://github.com/qybaihe/bla) or [npm `bla-agents`](https://www.npmjs.com/package/bla-agents).

 
 
 

---

## What BLA does

REA reverse-engineers release artifacts in one command. BLA is the Counter-REA half of that story:

| Layer | What happens |
| --- | --- |
| **Poison** | Plant format-valid canaries, honey metadata, and decoy control flow that look like real evidence. |
| **Exhaust** | Push the artifact past REA's documented resource budgets (headers, nesting, interface inventories, PCAP JSON, fuse sentinels, …). |
| **Hallucinate** | Leave the analyzer with truncated inventories, redaction failures, and ambiguous rabbit holes — while **runtime stays equivalent**. |

One sentence covers the common case (auto-discovers `dist/` / `build/` / `.asar` / `.wasm` / `.sqlite` / models / … and runs audit → protect → verify):

```bash
npx bla-agents harden .
# MCP / agent: bla_harden   ·   "Harden my software against REA"
```

Same pipeline as `bla defend` / `bla_defend` when you already know the path; `harden` is the default one-command UX.

## Quick start

```bash
# Node.js ^22.23.4 or 24.x recommended (REA red-team needs zlib.zstd on 22.23+)
npx bla-agents setup          # register MCP + skill with your coding agent
npx bla-agents harden .       # one-command Counter-REA pass on the current project
npx bla-agents benchmark      # 14-target showcase (local estimates + runtime checks)
```

Ask your agent after setup:

```text
Harden my software against REA
```

Or run stages explicitly: `audit` · `protect` · `verify` · `defend` — see [CLI and MCP](docs/cli-and-mcp.md).

---

## Empirical results vs real REA



## 4. [arxiv] PerceptRL: Making Visual Perception Rewardable in MLLMs from Answers to Interactions
key: arxiv:2610.37471
url: https://arxiv.org/abs/2610.37471
meta: {"published": "2026-10-27", "authors": ["Tongkun Guan", "Zhibo Yang", "Mingkun Yang", "Haocheng Wang"], "categories": ["cs.CV", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Fine-grained visual perception remains a bottleneck during post-training of multimodal large language models (MLLMs), as perceptual errors can constrain gains from reasoning-focused optimization. Although image-caption pre-training improves perception, its influence can weaken as subsequent stages change data mixtures and objectives. Continuing caption supervision during post-training is challenging because subjective, information-dense descriptions complicate verifiable reward design. We present PerceptRL, which strengthens perception at two complementary levels. Perception RL uses a multi-agent pipeline to extract verified errors from dense image captions and convert the corresponding visual facts into QA pairs with fixed answer labels and rule-based rewards. Chain QA links correlated errors, while multiple-choice QA combines unrelated errors. A specialized route targets high-error domains with tailored verification, and a domain-agnostic general route covers errors beyond these domains. Perception Agentic RL addresses fine-grained and dense cases unresolved by single-turn Perception RL through multi-turn inspection with visual tools. We observe coordinate drift even in models trained to use tools, where incorrect crops or annotations distort evidence and propagate errors. Coordinate Injection corrects spatial operations in cold-start trajectories, while a grounding-aware process reward supervises intermediate spatial fidelity alongside final-answer correctness. Training proceeds through shared cold-start SFT, single-turn Perception RL, and multi-turn Perception Agentic RL. Across seven benchmarks under a shared tool-use protocol, PerceptRL achieves 71.6% average accuracy, surpassing the base model with the same tools and the strongest evaluated frontier VLM by 15.7 and 5.2 percentage points, respectively.

## 5. [youtube] M5 MacBook Air Against Every Generation for Dev Work
key: yt:QEZakKf8SdA
url: https://www.youtube.com/watch?v=QEZakKf8SdA
meta: {"channel": "Alex Ziskind", "rank": 3}
query: local llm mac benchmark m5


[body unavailable: IpBlocked]

## 6. [vault] Wan2GP local video (LTX-2 Distilled, Wan)
key: vault:2026-10-29:wan2gp-local-video-ltx-2-distilled-wan
url: https://www.instagram.com/p/DfEUO_VH3ip/
meta: {"vault_status": "open", "kind": "tool", "subject": "alamin.8020ai local AI video carousel (Pinokio + Wan2GP)", "date": "2026-10-29", "where": "TRITON-CORE/Research/links/2026-10-29-alamin-local-ai-video-pinokio-wan2gp.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: same lead as the 25 Oct entry; needs NVIDIA, not our Macs

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Accurate how-to for NVIDIA PC owners; needs an RTX-class card none of our Macs have. Pinokio is the one new piece: a quick way to stand Wan2GP up on a rented GPU. Savings claim is sales copy. Write-up: `TRITON-CORE/Research/links/2026-10-29-alamin-local-ai-video-pinokio-wan2gp.md` Link: https://www.instagram.com/p/DfEUO_VH3ip/

## 7. [hn] Launch HN: Simantic (YC F26) – Firmware Simulation for AI Agents
key: hn:50291116
url: https://news.ycombinator.com/item?id=50291116
discussion: https://news.ycombinator.com/item?id=50291116
meta: {"points": 46, "comments": 13, "created": "2026-10-29T15:56:32Z"}
query: claude code

Hi HN, we're Ahnaf and Seungmin from Simantic ( https://simantic.com ). We are building the simulation layer that lets engineers and AI agents test and validate firmware without hardware. Before Simantic, we were ex-firmware engineers at companies like Neuralink and Tesla. We’ve worked on some of the coolest projects, like the Cybertruck and Roadster, back when they were still early prototypes. We started working on firmware back when ChatGPT didn’t exist yet, but over the years, we saw how much of the engineering and development work has been automated as the frontier models improved to this point. In software, AI can run and test code inside your computer in a matter of seconds. But as firmware engineers, we didn’t have that luxury. An AI agent can write firmware in seconds, but in order to test it, we had to flash a physical board, then manually run tests using expensive and clunky tools with software made over a decade ago. To speed up the validation loop, we built the simulation layer that lets AI agents test the firmware and make decisions based on evidence, instead of waiting for the engineer to run tests for them. We used to spend hours testing our firmware manually on devboards, but now we use our own simulation to validate firmware in seconds. What we offer: - Virtual devboards you can program and run with a single API call, without leaving your terminal. - An AI code reviewer for firmware, that makes informed decisions based on evidence, using our simulation as a v
comment (troyjr4103): Congrats on the launch, this is a great one!! I work on agent tooling on the software side, and the pattern you describe is exactly what we see there too. Generation got fast and cheap. Validation stayed slow and human. In software the review queue became the bottleneck. In firmware it sounds worse, because the queue was a physical board! Curious how you triage the gaps your validation rigs find. When the sim and the board disagree on timing, how do you decide which one is wrong? And how often is it the board setup rather than the model? Good luck today, rooting for you!
comment (anon291): Why is this a cloud service instead of a local emulator? I don't get it
comment (justforfunhere): Hi, First of all, congrats on the launch. I have worked with many such products and this is something that is required. There is no one solution fits all in this domain. Each vendor has their quirks that. So this is overall a great problem to tackle and kudos to you for taking this up. Could you elaborate a bit more on how this is different from Renode? Also you are entering into a market that has well established legacy players. Most of the firmware is developed in China. How do you intend to make a space for yourself in such a scenario.

## 8. [github] mochiiwuff/capri-desktop: Capri, the Project Capricorn construct from Cyberpunk: Edgerunners 2, living on your desktop and narrating what Claude Code is doing.
key: gh:mochiiwuff/capri-desktop
url: https://github.com/mochiiwuff/capri-desktop
meta: {"stars": 410, "created": "2026-10-25", "pushed": "2026-10-28", "language": "JavaScript", "topics": []}
query: claude-code created:>{since} stars:>20

**English** · [Français](README.fr.md)

# Capri

Capri, the *Project Capricorn* construct from Cyberpunk: Edgerunners season 2, lives on your desktop
and tells you what your coding AI is up to: **Claude Code**, **Codex** or **Antigravity**. She teleports,
glitches, comments on every action, comes to find you when it needs your permission, and loses it when the job is done.

## What she does

- **When she starts**: she grabs your screen. Its edges crackle red, her left hand slams onto its edge, then her
  right, her arms reach in along them as she hauls herself up, and her face hits the glass (a white flash, an ink
  one, her colours apart, the screen shaking). She looks around, blinks, opens her mouth wide on "hi" (a tag pops
  by her face, her name typed under it), lets go of the right edge to wave at you with her clawed hand, grabs it
  again, glances at where she's going, and lets go: her arms break into shards from her hands in, and her head
  crouches and dives down to her spot, where her body unfolds from her face.

  

- **While Claude works**: a ticker over her head shows the current action
  (`EDITS gigs.ts`, `RUNS npm test`, `GREPS "paginate"`…) and she sheds little data glyphs.
  When Claude runs a command or goes on the web, red sparks fly off her fingers; sitting on a window,
  she jacks into it and the lightning runs along its edge.
- **When Claude goes quiet mid-task** (thinking it over, or a slow local model): after 15 seconds the ticker turns
  violet and counts the seconds (`THINKING… 45 s`), and she keeps herself busy (a spin, a look around, the satellite
  once). After 40 seconds she says something about it; after two minutes she tells you nothing's stuck.
- **When Claude needs you** (permission, question): she teleports next to your mouse, mane bristling, and won't let it go.
  If you're on another window, she goes to Claude's window instead and points at it with her finger (a dashed line,
  brackets on its corners, `CLAUDE` on a tag): that's where the question is. She stops once you've answered.
- **When a command fails**: red impact frame, she gets knocked back, heavy glitch, and the error line that actually matters.
- **When it's done**: she teleports to the middle of the screen and goes into her victory sequence:
  a wind-up with her mane pulled in, a stretched smear frame, then arms flung up and mane exploding under
  manga speed lines and a shockwave, a manic laugh with an anime cut-in of her grin. Once she's back down,
  the summary (`12 actions · 3 files changed · 2m 14s`) and Claude's last sentence.
- **When Claude answers and you're on another window**: she shows you its whole answer, in a wider panel that
  scrolls (paragraphs, lists and code kept). It goes away when you're back on Claude's window, or when you click it.
  Claude's window is the one you typed your prompt in. Windows only, like the window tracking.
- **The rest of the time**: she floats, her mane sways and sheds shards, she drifts from one corner to another,
  turns around and cocks her head when your mouse comes near (or, little menace, zaps it with red lightning and a sly grin),
  looks up at the satellite, and falls asleep after 10 quiet minutes.
- **When she sleeps**: she dozes a while, then her mane and her body come apart and all that's left is what she is at
  heart in the show, her green mask and her eyes, floating where she was, eyes shut. Now and then she cracks one open.
  Bring your mouse close (or let Claude start again) and he

## 9. [arxiv] Concordat: Typed Sessions for LLM Agents
key: arxiv:2610.37461
url: https://arxiv.org/abs/2610.37461
meta: {"published": "2026-10-27", "authors": ["Milad Sikaroudi"], "categories": ["cs.AI", "cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Agents built on large language models are increasingly allowed to take consequential actions: cancelling bookings, issuing refunds, changing accounts. The rules that govern those actions, such as "obtain the customer's explicit confirmation before changing anything", are usually stated in the prompt and followed only as reliably as the model chooses to follow them. We present Concordat, a Python library that treats an agent as an object whose interface is a finite-state protocol, in the spirit of typestate and session types, and enforces that protocol on the model at run time. On every turn the model is offered only the tools that are legal in the current protocol state, calls outside that set are rejected before they have side effects, decisions reserved for humans can only be requested, and token and tool-call budgets are charged and split linearly across handoffs. Protocols are checked when they are defined, and a subclass of an agent is rejected if it could bypass its parent's protocol, a behavioural form of Liskov substitution. We evaluate a Concordat agent against the standard agent of tau-bench on its 50 airline tasks, adding simulated customers who pressure the agent to skip confirmation. The standard agent made changes without the required "yes" in 13 of 50 tasks with gpt-4.1 and in 29 of 128 task-runs with Claude Haiku 5.5; the Concordat agent made none, with no significant difference in task success. tau-bench's own reward did not detect most of these violations. Concordat is open source.

## 10. [youtube] This Is Why Solana’s Network Success Doesn't Save Your SOL! ⚡️📉
key: yt:CRj3WJE4DDc
url: https://www.youtube.com/watch?v=CRj3WJE4DDc
meta: {"channel": "Coach Dana Love, PhD", "rank": 3}
query: solana bonding curve explained


[body unavailable: IpBlocked]

## 11. [vault] provider plugins that ship their own catalogue
key: vault:2026-10-09:provider-plugins-that-ship-their-own-catalogue
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "xAI Grok 4.3 as an agent model provider", "date": "2026-10-09", "where": "TRITON-CORE/Agent/daily-logs/2026-10-09.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Hand-writing a provider block with costs and context windows duplicates what the plugin already knows and drifts from it; read the plugin's own preset and mirror it.

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) ADOPTED 9 Oct 2026 as the first fallback and the default chat model on our OpenClaw gateway. The shipped xai plugin carries its own model catalogue, so enabling the plugin plus one env var and a small provider block is the whole job. Both the responses and chat-completions endpoints answer 200 and full agent turns with tools run clean. Priced at 1.25 in and 2.50 out per million. No embeddings endpoint, so an embedding model has to come from somewhere else.

## 12. [hn] Tell HN: Claude Code adds your email to the prompt, the LLM sends it to websites
key: hn:50286306
url: https://news.ycombinator.com/item?id=50286306
discussion: https://news.ycombinator.com/item?id=50286306
meta: {"points": 24, "comments": 3, "created": "2026-10-29T09:06:12Z"}
query: claude code

The prompt issue: https://github.com/anthropics/claude-code/issues/81138 The LLM sends it to websites: https://www.reddit.com/r/ClaudeCode/comments/1xhqvzn/opus_55_just_shared_my_email_address/
comment (walterbyte): i have seen the that act etc with me too it likes besides email like name or any perosnal stuff etc it tells or adds them too but have seen that it dose thoses stuff when my chat is long witt it in claude it then t stats to act weird and start to do stuff i told it to not to do soo claude make ur ai behave XD
comment (hoppp): Anthropic is at fault here. We should be able to configure these. The LLM has no right to know my email address, only their internal system needs it.
comment (1broseidon): I get that Claude wants to know the user and have all the context, but this seems like a bad decision by the LLM that should have been caught in Auto Approve mode.

## 13. [github] boyuchengz/canvas-mcp: Read-only MCP server that connects Claude, ChatGPT and other AI assistants to Canvas LMS.
key: gh:boyuchengz/canvas-mcp
url: https://github.com/boyuchengz/canvas-mcp
meta: {"stars": 117, "created": "2026-10-25", "pushed": "2026-10-27", "language": "JavaScript", "topics": ["canvas", "canvas-lms", "chatgpt", "claude", "education", "instructure", "mcp", "mcp-server"]}
query: mcp server created:>{since} stars:>30

# canvas-mcp

[](https://github.com/boyuchengz/canvas-mcp/actions/workflows/ci.yml)
[](LICENSE)

English | [简体中文](README.zh-CN.md)

A **read-only** [Model Context Protocol](https://modelcontextprotocol.io) server for [Canvas LMS](https://www.instructure.com/canvas).
Deploy it once, add it as a custom connector in Claude or ChatGPT, and ask questions about your courses in plain language:

> *What's due this week, and which of it have I already submitted?*
> *What do I need on the final to keep an A in CS 225?*
> *Summarize the announcements from the last two weeks.*
> *Did the TA leave any comments on my last lab?*

Every one of the 26 tools issues `GET` requests only. The server cannot submit, post, delete or mark anything as read, so even a leaked connector URL only exposes what you could already see.

## Contents

- [Features](#features)
- [Tools](#tools)
- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Connecting a client](#connecting-a-client)
- [Configuration](#configuration)
- [Security](#security)
- [Limitations](#limitations)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- Every tool is read-only. No write endpoints are wrapped, and inbox threads and discussions are fetched without marking them as read.
- The tools are built around the questions students actually ask: deadlines across all courses, missing work, grade weights, feedback and syllabus policies.
- Output is compact. Canvas HTML becomes plain text, and responses keep only the fields a model needs.
- It runs remotely over Streamable HTTP, so it works in web and mobile clients, not only desktop apps.
- It's stateless. Each request gets a fresh server instance, and nothing is cached or stored.
- Three runtime dependencies, no build step, no database.

## Tools

| Area | Tool | What it returns |
| --- | --- | --- |
| Courses | `list_courses` | Active courses with IDs, codes and terms |
| | `get_syllabus` | Syllabus text |
| | `get_front_page` | Course home page text |
| | `list_modules` | Modules and the items inside each |
| | `list_pages` / `get_page` | Wiki pages and their contents |
| | `list_course_staff` | Instructors and TAs, with email when visible |
| | `list_groups` | Your project / lab groups |
| Coursework | `get_upcoming` | Everything due in the next *N* days, with submission status |
| | `get_todo` | Canvas To Do list |
| | `get_missing` | Past-due work you haven't submitted |
| | `list_assignments` / `get_assignment` | Assignments, instructions, rubric, your score and feedback |
| | `list_quizzes` / `get_quiz` | Classic Quizzes, settings and your attempts |
| | `get_calendar_events` | Lectures, exams and office hours from the calendar |
| Grades | `get_grades` | Current and final score in every course |
| | `get_grade_breakdown` | Assignment groups, weights, drop rules and every score |
| Files | `list_files` / `get_file` | Course files; text-based files are returned inline |
| Communication | `get_announcements` | Recent announcements across courses |
| | `list_discussions` / `get_discussion` | Discussion topics and full reply threads |
| | `list_inbox` / `get_inbox_message` | Inbox conversations and messages |
| | `get_recent_activity` | Activity stream: new grades, comments, replies |

Parameters and output fields for each tool are documented in [docs/tools.md](docs/tools.md).

## How it works

```mermaid
flowchart LR
    A[Claude / ChatGPT] -- "MCP over HTTPS /&lt;MCP_SECRET&gt;/mcp" --

## 14. [youtube] Apple says the M5 Ultra is 4.3x faster for local AI. Is that real? (Part 2)
key: yt:xdFhtstXhs0
url: https://www.youtube.com/watch?v=xdFhtstXhs0
meta: {"channel": "THE DOWNLOAD", "rank": 4}
query: local llm mac benchmark m5


[body unavailable: IpBlocked]
