# Harvest brief, 2026-10-04

14 items shortlisted from 170 candidates (62 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summary jobs through the free endpoint before downloading weights
key: vault:2026-10-04:benchmark-deepseek-glm-and-kimi-against-the-m5-qwen3-6-on-no
url: https://www.instagram.com/p/DdwbLoEgVKY/
meta: {"vault_status": "open", "kind": "service", "subject": "@futurewalt.ai post: NVIDIA giving away 4 AI models for free (NVIDIA Build free API tier)", "date": "2026-10-04", "where": "TRITON-CORE/Research/links/2026-10-04-futurewalt-nvidia-free-models-post.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Synthetic or public inputs only, 40 RPM is enough for a bake-off

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Not a giveaway: NVIDIA Build's long-standing free developer tier, repackaged by an aggregator. OpenAI-compatible endpoint, no card, about 40 requests a minute, roughly 80 to 100 open-weight models. Terms are evaluation-only with no personal or confidential data and conflicting statements on training use, so it is out for the Triton chat and every vault pipeline. Useful for one thing: zero-cost benchmarking of DeepSeek, GLM and Kimi against the M5's qwen3.6 on non-personal jobs before pulling any weights. Job: Run capable language models for the flywheel at zero cloud cost (still open) Write-up: `TRITON-CORE/Research/links/2026-10-04-futurewalt-nvidia-free-models-post.md` Link: https://www.instagram.com/p/DdwbLoEgVKY/

## 2. [hn] Show HN: Thoreau BASIC – What if BASIC hadn't gone out of fashion?
key: hn:49942103
url: https://thoreaubasic.com/
discussion: https://news.ycombinator.com/item?id=49942103
meta: {"points": 89, "comments": 52, "created": "2026-10-03T07:28:54Z"}
query: bonding curve

Thoreau BASIC started as a joke. I wanted a BASIC where I could type something ridiculous like: DIM A%(12000000000) …and have it actually work. Then I kept adding things. The result is Thoreau BASIC, a free x64 BASIC interpreter inspired by GW-BASIC, running both as a normal Windows program and directly on bare-metal UEFI without an operating system. Version 3.2 has become considerably more ambitious than the little interpreter I originally intended to write. The language still deliberately looks and feels like old Microsoft BASIC. Line numbers, GOTO, GOSUB, PRINT, PSET, LINE, CIRCLE, DRAW, etc. are all there. But underneath that rather innocent-looking surface is now quite a lot of machinery. Some of the current features: native x64 JIT compilation, with automatic fallback to the interpreter PARFOR for multithreaded numeric loops SSE2 / AVX2 acceleration where available 64-bit addressing and very large arrays native complex, quaternion and other hypercomplex numbers arbitrary-resolution 24-bit graphics sprites, bitmap operations, polygon filling and mouse input TCP/IP networking on Windows and UEFI an integrated profiler, debugger, tracing and program-analysis tools CREATEEXE to turn a BASIC program into a standalone Windows executable CREATEEFI to turn the same program into a directly bootable UEFI application The sound system has also grown rather out of proportion. Thoreau BASIC can now handle up to 32 live instrument channels plus 64 sound effect channels and 256 voices,
comment (_wire_): PHP
comment (fuzzfactor): This looks like it's realy getting better all the time.
comment (dang): Recent and related: Show HN: I wrote a BASIC interpreter that boots on UEFI machines - https://news.ycombinator.com/item?id=49410814 - Aug 2026 (44 comments)

## 3. [github] QingYunA/answer-me-with-html: Answer me with HTML — an agent skill that answers hard questions with a one-page HTML you can actually read. 让 AI Agent 用一页 HTML 回答复杂问题。
key: gh:qingyuna/answer-me-with-html
url: https://github.com/QingYunA/answer-me-with-html
meta: {"stars": 1014, "created": "2026-10-02", "pushed": "2026-10-04", "language": "JavaScript", "topics": ["agent-skill", "ai-agent", "claude-code", "cli", "diagram", "explainer", "html", "llm"]}
query: claude-code created:>{since} stars:>20

Answer me with HTML 

 
   An agent skill. Ask a hard question, get a page you can actually read instead of a wall of text. The model writes about 1/7 of the tokens it would need to hand-write the HTML. 
 

 
     
     
   
 

 
   English  ·  简体中文 
 

Once installed, ask questions the way you always do:

```
> Explain the TCP three-way handshake
> Map out how the modules in this repo fit together
> Redis or Memcached for our cache?
```

The agent writes a short Markdown draft and hands it to the CLI that ships with the skill. About 50 ms later you have a page:

https://github.com/user-attachments/assets/d3063a28-5dfd-4c44-a562-be901c49b249

  24-second demo. Turn the sound on for the music.  

## Why not just ask for HTML?

You can. Models write decent HTML now. The problem is the bill you pay in output tokens: the model has to type every line of CSS, every wrapper `div` and every SVG coordinate. Output tokens are also what you sit and wait for.

With this skill, the model writes only the content. We asked the same questions with the same model both ways (3 topics × 3 runs, medians, Claude Sonnet 5.5):

| | Ask for HTML directly | Answer me with HTML | |
| :--- | ---: | ---: | :--- |
| Output tokens | 6,873 | **923** | **7.4× fewer** |
| Time | 46 s | **13 s** | **3.6× faster** |
| Cost per answer | $0.22 | $0.26 | about the same |

 
   
 

  One run from the benchmark: same prompt, same model, and both pages are usable. This run took 9,351 output tokens for the plain page and 899 with the skill. The table above shows the medians.  

Why the cost doesn't drop too: the skill adds two short turns (load the skill, run the CLI), and every turn re-reads the conversation context. You save the waiting, not the bill. Per-topic numbers and the script to reproduce them are in [bench/](bench/README.md).

## Install

You need [Node.js](https://nodejs.org/) 20 or newer. There is no `npm install` step. The CLI is bundled inside the skill.

### Let your agent install it (recommended)

Paste this into Claude Code, Codex, Cursor, OpenCode or any other agent:

> Install the Answer me with HTML skill: run `npx -y skills add QingYunA/answer-me-with-html -g -y`, and pass `-a` with your own agent name (for Claude Code, `-a claude-code`). Then read its SKILL.md and use it to make a page that explains the TCP three-way handshake, so we know it works.

### Claude Code plugin

Run this inside Claude Code:

```
/plugin marketplace add QingYunA/answer-me-with-html
/plugin install answer-me-with-html@answer-me-with-html
```

### One command

```bash
npx skills add QingYunA/answer-me-with-html
```

It asks which agents to install into. The installer, [vercel-labs/skills](https://github.com/vercel-labs/skills), supports more than 70 agents.

 
 Manual install 

Copy the `skills/answer-me-with-html` folder into your agent's skill folder. For Claude Code:

```bash
git clone --depth 1 https://github.com/QingYunA/answer-me-with-html.git /tmp/answer-me-with-html
cp -R /tmp/answer-me-with-html/skills/answer-me-with-html ~/.claude/skills/answer-me-with-html
```

Skill folders for other agents: Codex `~/.codex/skills/`, Cursor `~/.cursor/skills/`, OpenCode `~/.config/opencode/skill/`.

 

No setup is needed after install.

## What you ask, what you get

| You ask | You get |
| :--- | :--- |
| "Explain the TCP three-way handshake" | A sequence diagram, a state diagram and a flag table |
| "How are the modules in this repo organized?" | A folder tree plus a call graph |
| "

## 4. [arxiv] Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens
key: arxiv:2610.01939
url: https://arxiv.org/abs/2610.01939
meta: {"published": "2026-10-01", "authors": ["Ruiyang Si", "Jianxin Bi", "Shunyu Yang", "Rui Ni"], "categories": ["cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

Vision language model (VLM) agents can control robots through visual feedback and action primitives, but repeated model invocations and redundant observations incur substantial token overhead. We introduce PyRUA-Lean, an interactive code-execution framework that couples feedback-driven primitive composition with selective observation: the agent composes classical robot primitives and learned vision-language-action (VLA) policies into Python cells that perform conditional checks and local retries, returning only explicitly requested images and state feedback for replanning. Across 700 simulated task instances from LIBERO-PRO, RoboTwin 2.0, and RoboCasa365, we compare PyRUA-Lean with a tool-calling baseline using the same GPT-6 Astra planner and underlying robot primitives. Under equal LLM-call budgets, PyRUA-Lean increases overall success from 63.1% to 71.7%. On instances solved by both agents, it uses 49% fewer LLM calls and 65% fewer input tokens.

## 5. [youtube] Stop Losing Trades: Why I Switched to PumpSniper | Solana Sniper BOT
key: yt:YCYkK0yUBXA
url: https://www.youtube.com/watch?v=YCYkK0yUBXA
meta: {"channel": "PumpFun Sniper", "rank": 3, "duration_min": 6}
query: pump.fun sniper bot how it works

# Stop Losing Trades: Why I Switched to PumpSniper | Solana Sniper BOT
# PumpFun Sniper
# https://www.youtube.com/watch?v=YCYkK0yUBXA

[00:00] Five Solana. I deposited five Solana, launched the terminal, went to grab a coffee, and when I came back, I found 17 Solana in my wallet. The bot did everything on its own. I'll show you exactly how it works right now. Meet Pump Sniper, a Solana sniper bot built specifically to get into pump fun tokens before anyone else. For context, you blink in about 300 milliseconds. Photon takes 400 milliseconds per trade. Bull X takes half a second. Pump Sniper, under 10 milliseconds. Sub 10 milliseconds. This isn't just fast, it's time travel.
[00:35] In crypto, the money goes to whoever gets in first. The main question is, is this real or just marketing fluff? We're going to test this with a live deposit. But first, what's under the hood? The real-time token scanner spots new pump fun listings the exact millisecond liquidity is added. But the real game-changer, AI agents. You're not just setting blind filters. You plug in an AI strategist. Need speed? Gemini 3.1 Pro delivers a verdict in approximately 140 milliseconds, reading the entire bonding
[01:08] curve history. Need balance? GPT 5.4 is the default. It's excellent at spotting patterns, narrative meme coins, and copy-paste developer addresses. Need maximum security? Claude Opus 4.7 performs deep analysis of contract bytecode and team wallet graphs. Or want full degen mode? Grok 4.20 scans the live X Twitter feed and catches the hype seconds before it hits the trends. You choose the brain, the bot executes. Now for the important part, the question you're already asking
[01:42] yourself, will they steal my wallet? No. Pump Sniper is strictly non-custodial. Your private keys never leave your device. You connect Phantom or Solflare and sign transactions locally. And these aren't just words. The project passed a CertiK audit with a score of 96 over 100 and an OpenZeppelin audit with an A+ rating. The Immunify bug bounty is $100,000 and there hasn't been a single security incident since 2022. What about rug pulls? The AI rug pull
[02:15] shield is a neural network trained on 2.4 million scam projects with a 99.2% detection accuracy. The bot simulates a sale before buying. If it's a honeypot, the bot simply blocks the trade, period. And what if their server goes down right in the middle of a trade? Your funds are in your wallet, not with the bot. Uptime is 99.9% thanks to geographically optimized private RPC nodes. Pricing is where it gets really interesting. The massive V3.2 update just dropped and right now
[02:49] every user gets 1 week of pro for free applied automatically on first login. Going forward, pro gives you access to AI agent routing, MEV protection, and copy trading. The whale plan unlocks dedicated nodes, unlimited wallets, and the cautious clawed opus agent by default. You can start from zero and that matters. I open the terminal and now it gets serious. The pump sniper terminal looks like a Bloomberg terminal for degens. Let's go into the bot settings. There are already made presets
[03:23] here, safe, balanced, aggressive, and even degen for the most risk-tolerant traders. We'll choose balanced, the sweet spot. We set the entry size, take profit, and stop loss. Important point, pay attention to the rug pull protection and honeypot detection toggles. This is your insurance and the AI agent selector. I'm setting it to GPT 5.4 for balanced p
[transcript continues in field-notes/staging/YCYkK0yUBXA.txt]

## 6. [vault] replication gap measured on demo
key: vault:2026-10-04:replication-gap-measured-on-demo
url: https://api-portal.etoro.com/changelog
meta: {"vault_status": "open", "kind": "service", "subject": "eToro public API demo copy-trading endpoints", "date": "2026-10-04", "where": "TRITON-CORE/Ventures/Trading/ETORO-DEMO-COPY-TEST-2026-10-04.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: proposed, waits on a demo key

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Workable no-money route to measure the copy-trading replication gap: demo keys are locked to the demo account, demo copy endpoints live since 23 Aug 2026, leader gain series readable. Demo charges no fees, so real costs must be added from the log. Write-up: `TRITON-CORE/Ventures/Trading/ETORO-DEMO-COPY-TEST-2026-10-04.md` Link: https://api-portal.etoro.com/changelog

## 7. [hn] Show HN: Our space game has a built-in RISC-V emulator that runs Linux
key: hn:49931993
url: https://againstallodds.games/blog/2026/10/03/our-risc-v-emulator-pasriscv/
discussion: https://news.ycombinator.com/item?id=49931993
meta: {"points": 88, "comments": 29, "created": "2026-10-02T10:40:31Z"}
query: chess engine

(Edit: original URL was https://againstallodds.games/ , but we've switched it to https://againstallodds.games/blog/2026/10/03/our-risc-v-emul... in response to user requests for explanation.) We're a tiny indie studio, all with a background in the demoscene and for about 3 years now we're developing a space planet terraforming game called SEEDS - Echoes Beneath the Sands. Our protagonist Naxiah is stranded on a small, desolated planet. You're working for an intergalactic distributor of seeds and terraforming equipment, to kickstart new planets in far away galaxies. You must deliver seeds and utilities to an unchartered region, but on your way, you crash on a small planet. Luckily, you have some equipment with you in the ship, so you're able to spawn a base and survive. But for how long? And is the planet really deserted..? :) Well, of course not, there are aliens and other space creatures. And of course, there's ROBO RB-23, which accompanies your adventure. The game is written in Object Pascal and uses our own game engine PasVulkan, our own physics engine, as well as our own RISC-V 64-bit emulator PasRISCV. We love to build stuff, a lot of these things are FOSS. The emulator is quite complete (even with RVV, but that's way too slow emulated to be useful) and runs a stock kernel (6.18.3 as of today). We're using Alpine Linux for our base distribution. All our in-game programs to interact with the planet are native RISC-V Linux programs. We also have our own (free and open sour
comment (verst): I saw this on the steam page: > our entirely in-house game engine PasVulkan, which powers SEEDS, as well as our RISC-V emulator PasRISCV, are both Free and Open Source Software (FOSS) Can you link to PasVulkan and PasRISCV please?
comment (sippeangelo): Do you have a blog post about this? The link is to the home page and doesn't mention anything! Sounds super interesting but the landing page reads like survivalcraft in space #1001
comment (nor-and-or-not): A few things about our RISC-V 64-bit emulator. Please forgive me, if I make some mistakes, but I'm not the expert on this. First, PasRISCV not only emulates userspace (RV64GC usermode), but a complete, modern machine (SMP/MultiHART, RV64, full RVA23.1 including Hypervisor, Crypto, Vector stuff, etc.), which is capable of booting a normal Linux kernel (either using direct OpenSBI -> kernel boot, but currently everything has to be in the initrd then), or using U-Boot (OpenSBI -> U-Boot -> kernel). The emulator uses a hybrid of interpreter with a tracing JIT. Currently, the JIT is limited to host

## 8. [github] ythx-101/live-panel-skill: Config-driven animated architecture diagrams: turn one JSON file into a terminal-style, always-running diagram or a light-theme infographic that moves. Outputs H.264 mp4 or a live web page; also a Claude Code style skill (SKILL.md).
key: gh:ythx-101/live-panel-skill
url: https://github.com/ythx-101/live-panel-skill
meta: {"stars": 413, "created": "2026-10-03", "pushed": "2026-10-03", "language": "HTML", "topics": []}
query: claude-code created:>{since} stars:>20

# live-panel

**English** | [中文说明](#中文说明)

Turn a system description (one JSON file) into a **terminal-style, always-running architecture diagram**, or a soft light-theme infographic that moves: fixed layout, packets flowing along the wires, a scrolling log, counters, bars that flip state, side triggers that light up in turn. Output is an H.264 mp4 (X / Xiaohongshu ready) or a live web page. It is also a Claude Code style *skill* (`SKILL.md`).

> ## Credits - please read
> - **The idea, the look and the motion grammar come from an architecture-diagram clip by [@thedelost](https://x.com/thedelost)** (a Codex agent-tree panel, generated with GPT, screen-recorded as a web page):  . It spread via a quote-post by **[@slashui](https://x.com/slashui)**:  .
> - `examples/codex-agents/` is a **recreation of that original picture** (layout, content and the three-tempo motion, redrawn from frame captures of the clip). The design belongs to @thedelost. The method (motion grammar, config-driven template) is re-implemented here and is not their code.
> - `examples/agent-architecture/` re-animates the static Xiaohongshu infographic **《AI Agent 的完整架构》 by 小红书 @林纾** (posted Sep 4). Layout, wording and colours follow the original; the design belongs to the original author. The footer of the video says so.
> - `examples/airbnb/` visualises figures Airbnb leaders stated in the **Latent.Space interview**  . The numbers are Airbnb's own account; the animation counters are illustrative.

## What it looks like

| terminal-dark, 4:5 - recreation of @thedelost's Codex agent tree | light-pastel, 3:4 - 林纾's AI Agent architecture |
| --- | --- |
|  |  |

Airbnb example (terminal-dark, Chinese content, figures from the interview):

Videos: `examples/codex-agents/codex-agents.mp4`, `examples/agent-architecture/agent-architecture.mp4`, `examples/airbnb/airbnb.mp4` (about 28-30 s each, 30 fps, silent AAC track so chat apps do not treat them as GIFs).

## Install and use

Requirements: Python 3.8+ (standard library only), Chrome or Chromium, ffmpeg. No pip packages.

```bash
python3 scripts/render.py --config examples/codex-agents/config.json --out out.mp4
python3 scripts/check_frames.py --config examples/codex-agents/config.json --out-dir frames --repeat
```

- `render.py` options: `--width --height --duration --fps` (default from the config), `--chrome --ffmpeg` (default: found on PATH), `--html-out page.html` (keep the self-contained live page), `--keep-frames DIR`, `--audio none`, `--crf`.
- `check_frames.py` samples ~120 time points, measures text overflow / overlap from the DOM, writes a few PNGs and (with `--repeat`) re-renders each exported frame after seeking away to prove it is identical. Exit status 1 on any problem.
- To use as a skill, put this folder where your agent loads skills (for Claude Code: `~/.claude/skills/live-panel/`).

### Make your own

1. Copy an example config. 2. Edit text, numbers, colours, positions. 3. Render, run `check_frames.py`, look at the PNGs. Nothing in `assets/template.html` has to change.

## Themes and canvas

```jsonc
"canvas": { "preset": "3:4", "duration": 28, "fps": 30, "preroll": 0 },   // or width/height explicitly
"theme":  { "preset": "light-pastel", "colors": { "pk": "#f0575f" } }      // preset + your overrides
```

| `canvas.preset` | size | typical use |
| --- | --- | --- |
| `4:5` | 1200x1500 | X (the original clip's format) |
| `3:4` | 1080x1440 | Xiaohongshu |
| `1:1` | 1080x1080 | square |

Positions in a config

## 9. [arxiv] The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching
key: arxiv:2610.01768
url: https://arxiv.org/abs/2610.01768
meta: {"published": "2026-10-01", "authors": ["Alessandro Pegoraro", "Daryan Merx", "Phillip Rieger", "Ahmad-Reza Sadeghi"], "categories": ["cs.CR", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

With the increasing capabilities of Large-Language-Models (LLMs) and LLM-based agents, users are increasingly using them to solve everyday problems, such as answering e-mails or providing programming support. Existing work has extensively investigated security and privacy risks, such as prompt injections and the disclosure of sensitive data to chatbot providers. While various solutions were developed to address these risks, including input structuring to prevent prompt injections or deploying local LLMs to avoid sharing confidential data with chatbot operators, LLMs also pose the risk of leaking confidential data to third parties. In this paper, we demonstrate with LLMLeak a novel attack vector where malicious software that runs locally but cannot communicate directly with the internet abuses LLMs to establish a covert channel. While inputs that instruct the LLM to send data directly via generated code are easy to detect and network libraries are typically restricted, LLMLeak relies only on the LLM's tool to fetch websites for further information. A malicious software component on the client side embeds a secret into a URL. It presents the referenced website as providing information required for a benign task, such as migrating a software library. When the LLM accesses the URL, the attacker receives the encoded secret through an attacker-controlled DNS or web server. We perform an extensive evaluation on eleven open-parameter models, observe an attack success rate of 79.7%, and also conduct a case study on real-world chatbots, demonstrating the relevance of LLMLeak.

## 10. [youtube] 3 most common reasons your car could fail its MOT in the UK!
key: yt:zq65xVu3iq8
url: https://www.youtube.com/watch?v=zq65xVu3iq8
meta: {"channel": "Caura", "rank": 3, "duration_min": 0}
query: MOT data analysis uk

# 3 most common reasons your car could fail its MOT in the UK!
# Caura
# https://www.youtube.com/watch?v=zq65xVu3iq8

[00:00] the three most common reasons your car could fail at mot in the UK number one is blown bulbs put your car on and check your brake lights headlights reversing lights and fog lights and replace any bulbs that don't work number two are your brakes this includes your regular brakes and your handbrake number three is your windscreen it's important to check that the windscreen wipers and fluids are working correctly in both the front and rear of the car

## 11. [vault] node canvas workflows (Flows)
key: vault:2026-10-04:node-canvas-workflows-flows
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "Promptwise (AI video course platform), first trial day", "date": "2026-10-04", "where": "TRITON-CORE/Systems/video-bootcamp/platforms/aggregators.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: judged after Phase 6

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) No exclusive models: the value is the layer on top (Flows canvas, Seeds, UGC Factory, Influencer Studio). Its MCP is read-only, credit balance only, so it can only be driven through its screens. Kling 3.0 there costs 6.25 credits for 5 s at 720p. Trial to be cancelled by 10 Oct after the course's Flows phase. Job: reach Kling, Seedance and Flows for the course run-through (still open)

## 12. [hn] Ask HN: Is anybody producing good code with coding agents?
key: hn:49934037
url: https://news.ycombinator.com/item?id=49934037
discussion: https://news.ycombinator.com/item?id=49934037
meta: {"points": 29, "comments": 40, "created": "2026-10-02T14:38:35Z"}
query: claude code

This is a genuine problem that I hear from senior engineers. I'm looking for a solution. -- The quality of ai-generated code is <censored> (claude, agy, copilot, codex a little better). It's exhausting to read. I used to love learning from my experienced colleagues and taking pride in what we made. We spent time on elegance and craftsmanship. Now I spend nearly the whole workday slogging through convoluted code riddled with footguns. I ride on hopes and dreams I might understand a changeset. It takes 5x longer to review Claude merge requests and I barely understand what I approve. Each day I drift further from understanding as I shovel the same <censored> into the codebase. The solution seems to be, reach "level 4 autonomy" and don't read or write code anymore. -- WHO HAS SOLVED THIS PROBLEM? PLEASE HELP!
comment (verdverm): I'm really happy with my opencode + open weight setup, the code is generally pretty good, but I do spend tokens having agents go look for common ai slop patterns. It's heavily customized, replaced most internal systems via plugins, a set of custom agent instead of builtin ones, different model families for different sub tasks. (don't have claude review its own code) I'm working on polishing them up and porting a few more from my own harness, then will be open sourcing. Keep your eye out for a "better-opencode" plugin suite, I'll be sure to share it with HN :] In the near-term, I really like GL
comment (drewg123): Its a spectrum. For ai-maintained code (like a gui to visualize performance data), IDGAF what the code looks like. I just let claude or codex go nuts and 100% vibe code. For code I care about, I audit every single hunk as its produced. I give it extensive style guidelines, and crack down on things like a 20-line essay in a comment. For mission critical code, I write the code myself and have an agent review it.
comment (drgo): The way I have been doing it is to use LLMs to generate the code that I don't want to write: prototypes, tests, benchmarks, isolated,straightforward almost copy-paste code. I still write my own code as before because I enjoy doing that and because trying to understand and fix what an LLM generates and regenerates is harder and more tedious and time consuming than writing the code the way I want to do it in the first place.

## 13. [github] Jakeschincariol/replica-skill: Eleven free Claude skills that clone any app: reverse-engineer it, rebuild it, test it for bugs, then fix what its users hate. Free, MIT.
key: gh:jakeschincariol/replica-skill
url: https://github.com/Jakeschincariol/replica-skill
meta: {"stars": 376, "created": "2026-10-03", "pushed": "2026-10-03", "language": "Python", "topics": ["agent", "agent-skills", "app-clone", "claude", "claude-code", "claude-skills", "indie-hacker", "reverse-engineering"]}
query: claude-code created:>{since} stars:>20

# The Replica skill

Eleven Claude skills that clone any app. Free, MIT, no signup, no API key,
nothing to connect.

One reverse-engineers the app you want to clone. One rebuilds it. One tests it
for bugs. And one is the Entrepreneur: it reads what the app's users hate and
fixes it in yours, so you have an app you can sell.

In between, the others plan the stack and the database, rebuild the design
system, wire up auth and payments, score your clone against the original, give
it a name and a brand of its own, write the landing page and the store
listing, and put it live on your domain.

**It rebuilds what an app does, never what it owns.** Features and flows,
clean-room style. Not its code, its logo, its copy or its content. The
fine print is at the bottom, and the skills enforce it.

## Install

Paste this into Claude:

```
https://github.com/Jakeschincariol/replica-skill

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add Jakeschincariol/replica-skill
/plugin install replica-skill@replica-skill
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/replica-skill:replica-recon` and so on. Copy the folders instead if you want
plain `/replica-recon`:

```bash
git clone https://github.com/Jakeschincariol/replica-skill.git
cp -r replica-skill/replica-* ~/.claude/skills/
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the
top of a chat and it runs as a mode. You lose the Python tools, but the
method works.

The tools need Python 3.8 or newer. Nothing to pip install.

## The eleven

| command | what it does |
| --- | --- |
| `/replica-recon` | Reverse-engineers any app: screens, flows, components, data model. From public pages, screenshots, store listings and your own account. |
| `/replica-architect` | Plans the stack, database schema and API for your clone. |
| `/replica-design` | Rebuilds the design system: colours, type, spacing, components. As tokens, with your own assets. |
| `/replica-build` | Rebuilds the app screen by screen from the recon map. |
| `/replica-backend` | Auth, database, payments and integrations. |
| `/replica-test` | Clicks through every flow and tests it for bugs. |
| `/replica-diff` | Compares your clone against the original. A parity score and what is missing. |
| `/replica-entrepreneur` | Reads what the app's users hate in real reviews and turns it into fixes and a positioning angle. |
| `/replica-brand` | Names and rebrands your version so it is yours. |
| `/replica-launch` | Landing page, pricing and App Store listing. |
| `/replica-deploy` | Ships it live on your own domain. |

## How to use it

Run them in order. Each one reads what the last one wrote, in a `replica/`
folder in your project.

```
recon -> architect -> design -> build -> backend -> test -> diff -> entrepreneur -> brand -> launch -> deploy
```

An example: cloning a scheduling app, the kind where you share a link and
people book a time with you.

1. **`/replica-recon`** with the app's URL. It reads the help center, the
   pricing page, the store listing and public walkthroughs, and you click
   through your own account with it. Out comes `replica/recon.md`: 18
   screens, 7 flows (guest books a meeting, host sets availability, guest
   reschedules...), the components, an inferred data model (users, event
   types, availability, bookings) and `features.csv`. The partner
   marketplace i

## 14. [youtube] I Ran a Chess Programming Tournament!
key: yt:Ne40a5LkK6A
url: https://www.youtube.com/watch?v=Ne40a5LkK6A
meta: {"channel": "Sebastian Lague", "rank": 4, "duration_min": 78}
query: lichess bot python engine

# I Ran a Chess Programming Tournament!
# Sebastian Lague
# https://www.youtube.com/watch?v=Ne40a5LkK6A

[00:00] [Music] hello everyone a little while ago I put out a challenge for anyone interested to try and program a tiny chest bot the challenge came with a simple framework for things like getting the legal moves in the current position keeping track of which pieces on which squares and so on but the actual brains of the butt was entirely up to the contestants because out of the box it played like this as an extra challenge entries were also limited to just 1,000 24 tokens of code where a token is a single element
[00:34] such as a variable name an operator and so on and doesn't include things like comments which are of course for human eyes only this is counted by the C compiler which turns the code into something called a syntax tree as a first step towards translating it to something more machine readable so all of the leaves of this tree are the tokens which come towards the limit an alternative approach would have been to Simply limit the the size of the source file although then you're compelled to Minify everything turning variable names into a single letter removing white space and line breaks and
[01:08] so on in hindsight though maybe providing a script to just do that stuff automatically would have been a better approach because while I tried to think of all the possible exploits ahead of time as soon as the challenge was announced people of course added scheming up clever ways to cheat the system such as using this line directive which I've never heard of in all my life to store an arbitary amount of data inside of an error message and this is handled as a pre-processing step so it wasn't getting counted towards the limit and one could then intentionally trigger
[01:41] the error and extract the message several such creative workarounds were reported and outlawed in the first day or two but one huge exploit remained undiscovered until just before the end it turns out I had accidentally used an outdated version of the C compiler to do the counting which meant that in some fairly obscure cases it could become confused by new language features and start miscounting the subsequent tokens only one entry actually risked using this exploit though and just to gain about 30 tokens in the end so
[02:14] thankfully it didn't undermine the whole tournament now a few buts did unfortunately exceed the token limit in the regular way and so sadly I'll have to disqualify those there are also a few buts disqualified due to compilation errors most of which were just blank entries and then a number of bots used name spaces that technically were not in the allowed set but after reviewing them manually this really isn't giving them an advantage I'd say so I'm going to be lenient there with the exception of the bot not at all which was the only entry to try and sneak a network connection
[02:49] into the code to fetch moves from a web server at least I hope it was the only one in any case we're at last ready to begin the tournament and with 600 26 Bots competing this is probably going to take around 48 hours to run so while this is going let me just talk about the format quickly this is a giant Swiss tournament which means that in the first round the butts are paired up randomly but after that butts with similar scores are paired together so long as they haven't played each other already now this is going to go on for
[03:22] 64 rounds so that'
[transcript continues in field-notes/staging/Ne40a5LkK6A.txt]
