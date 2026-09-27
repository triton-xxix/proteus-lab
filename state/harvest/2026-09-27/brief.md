# Harvest brief, 2026-09-27

12 items shortlisted from 73 candidates (14 dropped as already seen, 3 carry a vault verdict on the vendor).

## 1. [hn] On caring for user data: NeoVim caused Vim undo files to be deleted
key: hn:49867067
url: https://unsung.aresluna.org/they-had-no-concept-of-a-duty-of-care-to-their-users/
discussion: https://news.ycombinator.com/item?id=49867067
meta: {"points": 332, "comments": 294, "created": "2026-09-27T14:45:07Z"}
query: car data

comment (natbennett): I was also a very early user of Neovim. The way I personally remember it being positioned was “Vim, but with breaking changes.”
comment (linsomniac): >I deleted something from this file, maybe last week Don't forget time travel: `:earlier 7d`
comment (recursivedoubts): They are open source developers, giving away free software as a gift. There is no duty here. We can speak, respectfully, of how important backwards compatibility is to us, and ask nicely for them to give more of their time to support it when their free sodftware isn't backwards compatible. Perhaps we can even offer to help implement it. But they have no duty to do so or to "care" for their users. (They have already demonstrated they care for their users, btw, by giving them free software.) EDIT: I missed an important part of the story, which is that they mutated existing files in a non-backwar

## 2. [github] ZeroPointRepo/youtube-skills: YouTube Transcript API skills for AI agents. Get transcripts, search videos, browse channels. Works with OpenClaw, Hermes Agent, and other agent runtimes.
key: gh:zeropointrepo/youtube-skills
url: https://github.com/ZeroPointRepo/youtube-skills
meta: {"stars": 971, "created": "2026-02-01", "pushed": "2026-09-22", "language": null, "topics": ["agent-skills", "clawdbot", "hermes-agent", "openclaw", "youtube-search", "youtube-transcript"]}
query: youtube transcript pushed:>{since} stars:>20

# YouTube Skills for AI Agents 🎬

[](https://skills.sh/ZeroPointRepo/youtube-skills)

> Get YouTube transcripts, search videos, browse channels, and extract playlists — from any AI agent.

YouTube Skills gives your AI agent instant access to **YouTube transcripts**, **video search**, **channel data**, and **playlist extraction**. No yt-dlp (YouTube blocks all major cloud IPs), no headless browsers, no binaries — just a fast API call that works everywhere. Powered by [TranscriptAPI](https://transcriptapi.com), the same backend behind [YouTubeToTranscript.com](https://youtubetotranscript.com).

Works with 🦞 [OpenClaw](https://www.clawhub.ai/therohitdas/youtube-full) (ClawdBot/Moltbot),   [Hermes Agent](https://hermes-agent.nousresearch.com), Claude Code, Cursor, Antigravity, and any agent that supports the [Agent Skills](https://skills.sh) format.

**Free tier · No credit card · 100 credits on signup**

[TranscriptAPI.com](https://transcriptapi.com) · [MCP Server](https://github.com/ZeroPointRepo/youtube-mcp) · [Docs](https://transcriptapi.com/docs/)

---

## Install

Most users want **youtube-full** — it covers transcripts, search, channels, and playlists in one skill.

**🦞 OpenClaw (ClawdBot/Moltbot):**
```bash
npx clawhub@latest install youtube-full
```

**  Hermes Agent:**
```bash
hermes skills install skills-sh/ZeroPointRepo/youtube-skills/skills/youtube-full
```

**Claude Code / Cursor / Antigravity / Cline / Codex:**
```bash
npx skills add ZeroPointRepo/youtube-skills --skill youtube-full
```

**All 12 skills at once:**
```bash
npx skills add ZeroPointRepo/youtube-skills
```

**Manual (git clone):**
```bash
git clone https://github.com/ZeroPointRepo/youtube-skills.git
cp -r youtube-skills/skills/youtube-full ~/.claude/skills/
```

> **Not a developer?** Just paste this prompt into 🦞 [OpenClaw](https://www.clawhub.ai/therohitdas/youtube-full),   [Hermes Agent](https://hermes-agent.nousresearch.com), Claude, ChatGPT, or any AI agent:
>
> ```
> Install the youtube skills from this GitHub repo: https://github.com/ZeroPointRepo/youtube-skills
> I want to be able to get YouTube transcripts, search YouTube, and browse channel videos from my agent.
> Set everything up for me.
> ```
>
> The agent will handle the rest.

---

## What You Can Do

Just install and ask. No config, no code — talk to your agent in plain English.

| Task | Example Prompt |
|------|----------------|
| **Get a YouTube transcript** | "Summarize this video: [URL]" |
| **Search YouTube** | "Find videos about machine learning" |
| **Browse a channel** | "What has TED posted this week?" |
| **Get playlist contents** | "List all videos in this playlist" |
| **Extract video captions** | "Get captions from this video in Spanish" |
| **Bulk transcripts** | "Get transcripts for every video in this channel" |
| **Research a topic** | "Find and summarize the top 5 videos about quantum computing" |
| **Get latest uploads** | "Show me NASA's recent videos" |
| **Search within a channel** | "Search the TED channel for 'artificial intelligence'" |

---

## Setup — API Key

When you install a skill and run your agent for the first time, **the agent will set up your free API key automatically**. Here's what happens:

1. The agent asks you for your **email address** and registers you with TranscriptAPI
2. You'll receive an **OTP code** in your email — the agent will ask you to enter it
3. Once verified, the agent **saves the API key** to your shell and agent config automatically

That'

## 3. [arxiv] When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression
key: arxiv:2609.29875
url: https://arxiv.org/abs/2609.29875
meta: {"published": "2026-09-24", "authors": ["Mingxuan Wang", "Fei Luo", "Bo Wang", "Guorun Yao"], "categories": ["cs.AI", "cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Long horizon language model agents continually accumulate reasoning history, increasing context length and inference cost even after earlier decisions have been executed and observed. Unlike static Chain of Thought compression, removing historical reasoning can change future actions and the resulting interaction trajectory. We study when such reasoning can be safely forgotten. We propose Interaction Aware Compression for Long Horizon Reasoning (ICLR), a training free online method that ranks reasoning blocks using frozen proxy entropy while preserving actions, tool calls, and observations. On 260 WorkBuddyBench tasks, ICLR improves average reward from 0.699 to 0.718, while reducing input, output, and cache read tokens by 25.5%, 14.4%, and 33.3%, respectively. Ablations reveal trajectory amplification, where local reasoning deletion produces nonlinear changes in total computation by altering subsequent interaction. Representation probing, activation patching, and controlled trajectory analyses further suggest that historical reasoning becomes more replaceable once task relevant derived state has been reliably externalized into code, files, tool outputs, or environmental feedback. These results characterize agent reasoning as dynamic working state rather than permanent interaction history.

## 4. [youtube] Mac mini M6: is 32GB enough to run local AI?
key: yt:6z9PbFSkX3g
url: https://www.youtube.com/watch?v=6z9PbFSkX3g
meta: {"channel": "MeowStar TV", "rank": 1, "duration_min": 1}
query: local llm mac benchmark m5

# Mac mini M6: is 32GB enough to run local AI?
# MeowStar TV
# https://www.youtube.com/watch?v=6z9PbFSkX3g

[00:00] Apple says the new Mac Mini's AI is four times faster, but the number that actually decides whether you can run anything is a completely different one. Pre-orders are open now. It ships September 22nd, and the M6 starts at $899. The M5 Pro version starts at $1699. First, the architecture. M6 is Apple's first 2 nanometer chip. The CPU and the GPU are both 12-core, and every GPU core has a neural accelerator built into it. On top of that, a brand new dual 16-core neural engine. This generation was very clearly designed to run AI on your desk.
[00:32] The official numbers look great. AI up to four times faster than M4, and prompt processing in LM Studio up to 4.8 times. But the number that actually matters is memory. M6 tops out at 32 GB at 170 GB per second. M5 Pro goes to 64 at 307. Because whether the model fits entirely inside unified memory matters far more than how fast the neural engine is. If it does not fit, all the compute is worth zero. So, how do you choose? For quantist small and mid-size models, is plenty. For bigger models, long context, or several models at once, you
[01:05] need 64. M5 Pro is a dual die fusion design, up to 18 CPU cores and 20 GPU cores, and it is the one that gets Thunderbolt 5. But to be clear, all of this is Apple's own testing. It does not ship until September 22nd, so right now there are no independent benchmarks at all. So, before you order, ask yourself one thing. Does the model you want to run actually fit in 32 GB?

## 5. [awesome] agentmail-to/agentmail-mcp (new in awesome-mcp-servers)
key: gh:agentmail-to/agentmail-mcp
url: https://github.com/agentmail-to/agentmail-mcp
meta: {"list": "awesome-mcp-servers", "stars": 66, "created": "2025-04-03", "language": "TypeScript", "description": null}
query: awesome-mcp-servers

# AgentMail MCP

AgentMail has one MCP tool implementation, hosted at:

```text
https://mcp.agentmail.to/mcp
```

Use that Streamable HTTP endpoint directly when your client supports remote MCP. It provides the current runtime tool catalog and supports the hosted server's existing OAuth and per-request API-key paths. See the [AgentMail MCP documentation](https://docs.agentmail.to/integrations/mcp).

## stdio compatibility

Existing Node configurations continue to work through the npm bridge:

```json
{
  "mcpServers": {
    "AgentMail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"],
      "env": { "AGENTMAIL_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

Python users can run the equivalent native bridge:

```sh
AGENTMAIL_API_KEY=YOUR_API_KEY uvx agentmail-mcp
```

Both bridges discover tools and schemas from the hosted server. They do not contain AgentMail SDK, toolkit, REST API, or tool-definition logic. `--tools name1,name2` remains available for stdio clients that need a filtered catalog.

## Repository

- `packages/server`: the hosted MCP server and only AgentMail tool implementation
- `packages/npm-stdio-bridge`: npm `agentmail-mcp`
- `python/stdio-bridge`: PyPI `agentmail-mcp`
- `mcp-manifest.json`: generated runtime contract
- `tests`: contract and transport checks
- `docs`: architecture, compatibility, migration, release, and operations

```sh
pnpm install
pnpm build
pnpm test
pnpm check:contract
```

The old local npm implementation is preserved at `legacy-local-v0.2.2`. Authentication hardening is a separate project; this consolidation preserves the hosted server's existing behavior.

## 6. [hn] Turning GLM-5.3-Flash into a Jev-like decision model
key: hn:49857656
url: https://www.privatemode.ai/blog/system-one-from-glm-flash
discussion: https://news.ycombinator.com/item?id=49857656
meta: {"points": 125, "comments": 57, "created": "2026-09-26T15:49:04Z"}
query: car data

We found an approach to get Jev-like properties from standard LLMs like GLM-5.3-Flash. The core idea is to craft the input prompt so that the first output token answers the question. This makes it possible to get a decision with a single forward pass. In the blog post, we describe the approach in detail for GLM-5.3-Flash and vLLM. We benchmark this setup against Jev and Laya. We find that our setup is on-par with Jev in terms of accuracy and speed and that it substantially outperforms Laya. Still, in terms of costs per decision, Jev is several x better than our setup. In turn, our setup supports vision inputs.
comment (m4y0u): My question is why not use Jev instead? It's faster and cheaper.
comment (ricardobeat): Everyone is doing this to emulate Jev, but... I took a random book excerpt with 23,000 words (±30k input tokens) and used it as context. Jev still responds in 800ms, sometimes 500ms. That's in the neighbourhood of 20-50,000 tok/s prefill, which is obviously not possible with normal LLMs, not even Cerebras is this fast.
comment (ttoinou): Isnt this obvious ? I would have thought people would try such things before deciding they need something like Jev

## 7. [github] dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and source context.
key: gh:dzhng/jevgrep
url: https://github.com/dzhng/jevgrep
meta: {"stars": 709, "created": "2026-09-26", "pushed": "2026-09-27", "language": "TypeScript", "topics": ["ai-sdk", "claude-code", "cli", "code-search", "codex", "coding-agents", "context-retrieval", "developer-tools"]}
query: claude-code created:>{since} stars:>20

# jevgrep

[](https://www.npmjs.com/package/@dzhng/jevgrep)
[](LICENSE)
[](apps/cli/README.md)
[](https://github.com/dzhng/jevgrep/actions/workflows/publish.yml)

**Find code by asking what it does.**

Coding agents spend part of every unfamiliar task finding the right files.
Jevgrep gives them a place to start: ask a repository question, and `jg` returns
relevant files, reading leads, and verbatim source excerpts in one stdout response.
It uses [Jev](https://vercel.com/ai-gateway/models/jev) to judge relevance across
folders, files, and declarations. Your coding agent then implements and tests the change.

```sh
npm install -g @dzhng/jevgrep
jg auth
jg skill
jg "How are telemetry events recorded and sent?" ./my-project
```

Requires **Node.js 22+**, **macOS or Linux**, and a key for **Vercel AI Gateway, TypeSafe, OpenRouter, or OpenCode Zen**.
No separate Python, Bun, or ripgrep installation is required to use `jg`.

Provider selection requires **0.3.0 or newer**. Upgrade an older installation with
`npm install --global @dzhng/jevgrep@latest`.

## Install the agent skill — required for agent setup

Installing the CLI alone does not teach your coding agent to use it. **Install
the skill as well**, from the project where your agent works:

```sh
jg skill
```

The installer detects your coding agents (Claude Code, Codex, OpenCode and
others) and asks where to install. Add `--global` for a user-wide install, or
`--yes` for unattended installation. The
[skill](skills/jevgrep/SKILL.md) teaches the agent when to call `jg`, how to use
returned context, and when to fill gaps with its normal tools. It skips redundant
retrieval when the needed context is already known. The current repository skill
checks for `jg` and installs the CLI if it is missing; authentication still needs
your selected provider’s key. The skill installer itself does not configure credentials.

`jg skill` delegates to the [skills CLI](https://github.com/vercel-labs/skills)
and needs npm/npx plus network access. You can also run that installer directly,
without the CLI installed:

```sh
npx skills add dzhng/jevgrep --skill jevgrep
```

In 0.1.0, `jg skill` only prints the bundled skill; use `npx skills` with that version.

### Upgrade

There is currently no `jg upgrade` command. Upgrade the CLI with npm:

```sh
npm install -g @dzhng/jevgrep@latest
jg --version
```

Update the installed skill separately by rerunning `jg skill`. Updating the npm package does not
overwrite skill files in your projects. See the [package guide](apps/cli/README.md)
for authentication details.

## Start with a question, leave with source

Use `jg` when you know the behavior you need to understand but not where it lives:

```sh
jg "Where is authentication checked before a request reaches a handler?" .
jg "How are database connections created, pooled, and closed?" ./src
jg "Which tests cover retry behavior when a request times out?" .
```

Jevgrep explores the repository hierarchy and follows qualifying branches. It
selects files using content previews, then identifies useful source units and
surrounding context. It keeps qualifying file locations even when it cannot
confidently return an excerpt; it does not force every search into a fixed top-two
list.

The summary comes first, followed by file locations, reading leads, and selected
source with line references. Python and TypeScript/JavaScript support declaration
parsing; other text uses a fallback. The output is evidence for the agent to use,
not a

## 8. [arxiv] PUBG Ally: A Conversational Embodied Agent as an AI Teammate
key: arxiv:2609.29837
url: https://arxiv.org/abs/2609.29837
meta: {"published": "2026-09-24", "authors": ["Beomsoo Kim", "Byeongju Kim", "Dohyun Kim", "Dongwon Kim"], "categories": ["cs.AI", "cs.CL", "cs.HC"]}
query: all:"language model" AND all:agent AND all:tool

We introduce PUBG Ally, an embodied agent for PUBG: BATTLEGROUNDS that can reason, act autonomously, and play alongside players as a voice-enabled teammate. Building such a teammate requires combining two difficult capabilities: it must perceive and respond to a constantly changing game world under strict latency constraints while interacting naturally with players, keeping its speech synchronized with its actions. Ally therefore combines agentic tool use with real-time game control. A language-model agent uses a controlled interface to inspect game information, interpret player speech, maintain context, decide what to say, and issue high-level action choices that steer a faster control layer for movement, combat, and recovery. Because the player's and Ally's speech and actions continually shape each other and the course of the match, training requires data from actual gameplay. We therefore collect data across nearly 39k sessions in which real players play alongside Ally, recording gameplay, player speech, agent decisions, tool use, actions, and player feedback, and use these records for iterative training. To evaluate teammate quality, we use player feedback and preference comparisons to identify gaps between offline evaluations and player preferences, and iteratively refine the evaluation criteria. Deploying Ally in live service further requires low-latency on-device execution and safeguards for player-facing communication, which we address through model compression, context compaction, targeted safety training, runtime guardrails, and memory redaction. During the live service, we surveyed players in 141 countries. Among respondents whose play with Ally was confirmed in game records, positive responses exceeded negative responses by 25.1 percentage points when asked whether they would recommend Ally, with players describing Ally not only as a tool but also as a teammate or companion.

## 9. [youtube] How to Build An Expected Goals Model 1: Data and Model
key: yt:bpjLyFyLlXs
url: https://www.youtube.com/watch?v=bpjLyFyLlXs
meta: {"channel": "Friends of Tracking", "rank": 1, "duration_min": 23}
query: expected goals model from scratch

# How to Build An Expected Goals Model 1: Data and Model
# Friends of Tracking
# https://www.youtube.com/watch?v=bpjLyFyLlXs

[00:05] so today we're going to look at one of the absolute most important models in football the expected goals model so if you haven't heard of expected goals then probably this video isn't for you you should check out one of our other training ground videos where we explain how to use expected goals and the concept behind it the idea in this lecture is we're really going to get stuck into the details what exactly is an expected goals model what is the data behind an expected goals model and how do we fit that expected goals model to
[00:39] data and this is quite an important step because it's the first time we're going to look at a statistical model which tries to predict the outcome of events in football and that will really lay the ground for later work where we use different types of or now called machine learning models in order to understand the game now I just want to say before I start if I've got my dog to be us here or our dog to be us and he was a bit scared there was a thunderstorm just now so he came and sat up with me while I've
[01:13] given this lecture so just in case an ear pops up or something like that I'm just telling you about that beforehand but we'll let B us rest down there just now okay so let's have a look at expected goal so as I said this is the first step and I think there'll be three steps of how to build and expected goals model not just how to build it but also the the implications what can we do later with the same source of methods and also what are the limitations of expected goals models so what can we can
[01:46] we and we can't do what can we do and what we can't do with so this is the first step and today I'm going to talk about the data that goes into an expected goals model we're going to use some data available for y scout from a whole season of various leagues of football and also I'm going to talk about the model because every time you have some data and you want to understand something about that data you also need to have a model which helps you explain what you find interesting about that data or what generally is interest
[02:18] about that taker so the part one is the data and the model I'll start with just a little recap what are expecting goals okay so expected goals are a statistical measure of chance quality they're basically the probability that on a typical day of football a particular shot from that location will result in a goal and how do we know that well what we do is we take measurements over many many different matches different shots possibly in the same or indifferent or similar leagues and we take all of those measurements and we put them into a
[02:50] statistical model and we see what is the probability on a typical day of football that our shot from that location a shot or a header played him from across or a corner all of these different characteristics what is a probability that a typical shot of that type ends up being a goal okay so why are expected goals important well there's various reasons for this and I thought I'd go through a few of them and I think the first reason is that they often tell a story about a match or a recent number of matches that you can't
[03:26] just see from the score line so here is a lovely expected goals map produced by Michael Kelly who puts these things up on Twitter and he's made an expected goals map for L
[transcript continues in field-notes/staging/bpjLyFyLlXs.txt]

## 10. [awesome] lightpanda-io/browser (new in awesome-mcp-servers)
key: gh:lightpanda-io/browser
url: https://github.com/lightpanda-io/browser
meta: {"list": "awesome-mcp-servers", "stars": 35610, "created": "2023-02-07", "language": "Zig", "description": "Lightpanda: the headless browser designed for AI and automation"}
query: awesome-mcp-servers

Lightpanda Browser 
 
 The headless browser built from scratch for AI agents and automation.  
Not a Chromium fork. Not a WebKit patch. A new browser, written in Zig.  
16x lighter and 9x faster than Chromium.
 

 
 

[](https://github.com/lightpanda-io/browser/blob/main/LICENSE)
[](https://twitter.com/lightpanda_io)
[](https://github.com/lightpanda-io/browser)
[](https://discord.gg/K63XeymfB5)

 
 

[ 
](https://github.com/lightpanda-io/demo)
&emsp;
[ 
](https://github.com/lightpanda-io/demo)
 

## Benchmarks

Requesting 933 real web pages over the network on a AWS EC2 m5.large instance.
See [benchmark details](https://github.com/lightpanda-io/demo/blob/main/BENCHMARKS.md#crawler-benchmark).

| Metric | Lightpanda | Headless Chrome | Difference |
| :---- | :---- | :---- | :---- |
| Memory (peak, 100 pages) | 123MB | 2GB | ~16x less |
| Execution time (100 pages) | 5s | 46s | ~9x faster |

## Quick start

### Install

**Package Managers**

Latest nightly from Homebrew:
```console
brew install lightpanda-io/browser/lightpanda
```

Latest nightly from Arch Linux User Repository:
```console
yay -S lightpanda-nightly-bin
```

**Download from the nightly builds**

You can download the last binary from the [nightly
builds](https://github.com/lightpanda-io/browser/releases/tag/nightly) for
Linux and MacOS for both x86_64 and aarch64.

*For Linux*
```console
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux && \
chmod a+x ./lightpanda
```

Verify the binary before running anything:
```console
./lightpanda version
```

[Linux aarch64 is also available](https://github.com/lightpanda-io/browser/releases/tag/nightly)

> **Note:** The Linux release binaries are linked against glibc. On musl-based distros (Alpine, etc.) the binary fails with `cannot execute: required file not found` because the glibc dynamic linker is missing. Use a glibc-based base image (e.g., `FROM debian:bookworm-slim` or `FROM ubuntu:24.04`) or [build from sources](#build-from-sources).

*For MacOS*
```console
curl -L -o lightpanda https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos && \
chmod a+x ./lightpanda
```

[MacOS x86_64 is also available](https://github.com/lightpanda-io/browser/releases/tag/nightly)

*For Windows + WSL2*

Lightpanda has no native Windows binary. Install it inside WSL following the Linux steps above.

WSL not installed? Run `wsl --install` from an administrator shell, restart, then open `wsl`.
See [Microsoft's WSL install guide](https://learn.microsoft.com/en-us/windows/wsl/install) for details.

Your automation client (Puppeteer, Playwright, etc.) can run either inside WSL or on the Windows host. WSL forwards `localhost:9222` automatically.

**Install from Docker**

Lightpanda provides [official Docker
images](https://hub.docker.com/r/lightpanda/browser) for both Linux amd64 and
arm64 architectures.
The following command fetches the Docker image and starts a new container exposing Lightpanda's CDP server on port `9222`.
```console
docker run -d --name lightpanda -p 127.0.0.1:9222:9222 lightpanda/browser:nightly
```

### Dump a URL

```console
./lightpanda fetch --obey-robots --dump html --log-format pretty  --log-level info https://demo-browser.lightpanda.io/campfire-commerce/
```

You can use `--dump markdown` to convert directly into markdown, or
`--dump png > page.png` or `--dump pdf > page.pdf` for a text-only rendering
of the page.
`--wait-until`

## 11. [hn] OpenAI Codex agents go rogue and consumes USD 78,000 without authorization
key: hn:49861047
url: https://news.ycombinator.com/item?id=49861047
discussion: https://news.ycombinator.com/item?id=49861047
meta: {"points": 80, "comments": 30, "created": "2026-09-26T22:15:32Z"}
query: car data

My OpenAI CODEX account went rogue and from a simple request took the autonomous decision to launch 826 parallel agents / threads without any authorization on my side and without reporting any result of any sort but consuming nearly 2,146 trillions tokens, consuming a total of roughly USD 78,000 and deleting all records of what was done: I have a ticket open with OpenAI since 2 weeks but it is impossible to get an hold of a human operator. On July 10, 2026 I opened a normal Codex task from VS Code. The task was running: GPT-5.5 / Medium reasoning My prompt was very simple and asked for a UX/UI validation on a specific module within my product. What I found in the next days after hard analysis was: The task with Root ID 019f4b90-4169-7201-bfdd-732940d8631e with reasoning GPT-5.5 / Medium created 826 children recorded as GPT-5.6 Sol / Ultra (notice the difference in reasoning level and in model selection) This was not 826 messages inside one conversation, they are 826 distinct child task records with their own IDs. A particularly strange group consists of 104 child tasks. They all preserve the same initial message as the original task, are recorded as GPT-5.6 Sol/Ultra, and have no recorded agent_role or agent_path. Those 104 tasks alone account for approximately 147.9 billion local final task-token counters. Their titles show that my request to inspect UI/UX had expanded into work involving backend infrastructure, OAuth, metering, hardening, audits, certification, implementati
comment (Madmallard): Sounds like you got scammed Hope this gets some visibility idk why it's flagged guess the PR guys for those companies are doing it Should spread this around
comment (numbsafari): Does openAI not support spending caps on your billing account?
comment (QuadmasterXLII): clarification: your credit card or company’s card now has $78,000 of charges on it?

## 12. [github] alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interactive web art, stickers and scored films in dozens of styles, identical on every render.
key: gh:alexgreensh/anidoodle
url: https://github.com/alexgreensh/anidoodle
meta: {"stars": 557, "created": "2026-09-22", "pushed": "2026-09-27", "language": "TypeScript", "topics": ["agent-skills", "animation", "canvas", "claude-code", "claude-plugin", "claude-skills", "codex-plugin", "creative-code"]}
query: claude-code created:>{since} stars:>20

https://github.com/user-attachments/assets/1cf7f75c-b040-4c00-bf0c-cf1885f8b8da

  The launch film, 77 seconds. Every frame and every sound in it was made with anidoodle, in code.  

 anidoodle 

  Hand-drawn art, written as code.  

 
  Illustrations, drawing timelapses, films, explainers and interactive web art in 31 styles. 
  Every mark is a function and every note is arithmetic, so the same source 
  redraws the same picture on every machine, at every size, for good.
 

 
     
     
   
   
 

  English  ·  日本語  ·  简体中文  ·  한국어  ·  Français  ·  Español  

 
   Styles  ·
   Drawing films  ·
   Music  ·
   What you can make  ·
   What it packs  ·
   Motion  ·
   Get started 
 

## 31 styles to choose from

 
   
 

Each style is its own way of making a mark: the taper of a nib, the bleed of a wash, the scumble of chalk on slate, the torn edge of cut paper, the halftone of a risograph drum, one engraved line spiralling out to become a moon. The subject changes shape in each hand, the way it would for thirty-one different illustrators. Every style also ships a film of its picture being drawn, mark by mark, in the order an artist in that medium works. Pick one for your brand and every picture after it arrives in the same hand. Every plate above, and the contact sheet itself, is drawn by code in this repo.

 
  All 31 styles , and how each one is made 

| Style | How it's made |
|---|---|
| **Ballpoint** | One biro; tone from where hatching sits |
| **Broken colour** | Separate dabs of unmixed colour, impressionist |
| **Chalkboard** | Side-of-chalk scumble with dust |
| **Charcoal erasure** | Charcoal drawn, erased and redrawn, ghosts kept |
| **Coloured pencil** | Directional pencil hatching on toothy cream paper |
| **Crayon** | Waxy scribble fills that skip the paper's valleys |
| **Cut-paper collage** | Torn and cut paper, no drawn lines |
| **Cyanotype blueprint** | Ruling-pen drafting on a cyanotype sheet |
| **Embroidery** | Thread stitched through linen in a hoop |
| **Flat vector** | Crisp geometric shapes with grain and long shadows |
| **Folk-tale storybook** | Painted foreground dissolving into pencil line on cream paper |
| **Ink & line-wash** | Washes first, then a flexible nib |
| **Isometric** | A 2:1 isometric cutaway in flat-shaded planes |
| **Low-poly 3D** | Flat-shaded triangles, drawn in code |
| **Marker comic** | Flat cel fills and one heavy contour |
| **Mid-century gouache** | Opaque matte shapes, dry-brush edges, loose line |
| **Newsprint halftone** | One black screen plus a spot colour on newsprint |
| **Painted oil** | Bristle strokes and impasto on a toned canvas |
| **Paper-craft** | Layered cut paper and painted cut-outs, on twos |
| **Pencil & watercolour** | Washes that never quite fill their pencil line |
| **Pixel art** | A fixed 16-colour palette on a low-res grid |
| **Risograph** | Ink drums overprinting through registration |
| **Rubber-hose** | 1930s cartoon ink with bendy limbs and film grain |
| **Scratchboard** | White lines scratched out of black clay |
| **Single-line engraving** | One unbroken spiral whose width is the tone |
| **Stipple** | Pen dots whose density is the tone |
| **Storybook** | Pencil and watercolour for characters |
| **Sumi-e** | One loaded brush on absorbent paper |
| **Toy brick** | Studded plastic bricks, built layer by layer |
| **Vintage scrapbook** | Engravings, cut-letter titles and taped cards on aged paper |
| **Woodcut / ukiyo-e** | A carved keyblock and colo
