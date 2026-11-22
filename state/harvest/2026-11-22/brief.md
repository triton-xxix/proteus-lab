# Harvest brief, 2026-11-22

13 items shortlisted from 409 candidates (335 dropped as already seen, 6 carry a vault verdict on the vendor).

## 1. [vault] the ten Claude commands
key: vault:2026-11-22:the-ten-claude-commands
url: https://www.instagram.com/p/Df4Pg_FH4iS/
meta: {"vault_status": "open", "kind": "tool", "subject": "@alamin.8020ai ten Claude commands carousel", "date": "2026-11-22", "where": "TRITON-CORE/Research/links/2026-11-22-alamin-10-claude-commands.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: on the slides, need screenshots, keep only what is new against our Claude Code setup

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Listicle of ten Claude commands; names on the slides, unseen, nothing assessed Write-up: `TRITON-CORE/Research/links/2026-11-22-alamin-10-claude-commands.md` Link: https://www.instagram.com/p/Df4Pg_FH4iS/

## 2. [hn] Show HN: agent-mcts – Monte Carlo tree search on top of Claude Code
key: hn:50589235
url: https://github.com/natsu0529/agent-mcts
discussion: https://news.ycombinator.com/item?id=50589235
meta: {"points": 16, "comments": 2, "created": "2026-11-21T13:53:08Z"}
query: claude code

comment (Bataino): Interesting...
comment (joe-esquibel): What type of problems is this well suited for? Ive found that I can just linearly improve on one idea and get further to my goal. Like in 10 directed back and forths. I feel like this would create x options for every step that need to be independently evaluated with some Oracle and then again for the next steps, I feel like tokens are too expensive to random walk an llm through a solution space. Id like to see a validation of taking a small AI and then have to chug through a tough problem like a chess engine to a specific standard and compare that to just one shot it with fable. Maybe we could

## 3. [github] EL4CTEO/fast-anything: Don't rewrite it in Rust. Rewrite the 5% that's slow: profile Python, Node or Ruby apps, port the hot functions with your coding agent, prove they behave the same.
key: gh:el4cteo/fast-anything
url: https://github.com/EL4CTEO/fast-anything
meta: {"stars": 1842, "created": "2026-11-21", "pushed": "2026-11-22", "language": "Rust", "topics": ["agent-skills", "ai-agents", "claude-code", "claude-code-plugin", "codex", "developer-tools", "ffi", "mcp"]}
query: claude-code created:>{since} stars:>20

Don't rewrite it in Rust. Rewrite the 5% that's slow.  

 
     
 

 
     
     
     
   
   
   
     
 

Rewriting a whole app in Rust costs months, minute-long compiles and gigabytes of `target/`. Most of the runtime sits in a few functions anyway.

**fast-anything** finds those functions, has your coding agent port *only them* to Rust, proves the port gives the same results on real recorded calls, and swaps it in. One command, fully reversible.

   

## Install

```sh
npm i -g @el4cteo/fast-anything      # or: cargo install fast-anything
```

Ports are compiled with your Rust toolchain ([rustup](https://rustup.rs)).

## Use

```sh
fast-anything go --agent claude -- python app.py     # or: -- node app.ts / bun app.ts / deno run -A app.ts / ruby app.rb / java App.java / mvn exec:java / gradle run / go run . / php app.php / clang -O2 main.c
```

Or step by step:

| command | what it does |
|---|---|
| `scan --  ` | profiles the app, ranks functions by time × how portable they are |
| `port [id]` | records up to 500 real calls, creates a one-function Rust crate + `TASK.md` |
| `verify` | release-builds the port and replays every recorded call |
| `enable` / `disable` | swaps the Rust in or out (one marked block, removed byte for byte) |
| `bench` | times the whole app, original vs Rust, interleaved runs |
| `report` | markdown + SVG card for your PR |
| `doctor` | checks Rust, your runtimes and your agents |

`--agent` takes `claude`, `codex`, or any command that reads a prompt on stdin. Without it, hand `TASK.md` to whatever you use.

## Proof, not vibes

   

That port looked right but compared bytes instead of characters. 148 of 500 real calls caught it. On top of the recorded calls, fast-anything derives extra cases and lets the original answer them: edge cases (NaN, ±infinity, -0.0, zero and ±1, non-ASCII text, empty and up to 16× bigger inputs) and shrunk inputs (tiny and random slices). Nothing is enabled until every case matches: same values (floats within 1e-9), errors where the original errors. A port that is right but slower per call than the original (calling into Rust costs more than the work saved) isn't enabled either. `FAST_ANYTHING_DISABLE=1` runs the original any time.

## Results

Real runs on an i5-10500, Windows 11 (C and C++: a 4-core GitHub Actions Linux runner). Reproduce them from [`examples/`](examples).

| app | before | after |
|---|---|---|
| Python fuzzy dedupe (700 names) | 4.91s | **42ms, 116×** |
| TypeScript fuzzy dedupe (2,000 names) | 3.11s | **155ms, 20×** |
| PHP fuzzy dedupe (600 names) | 2.94s | **53ms, 55×** |
| Go fuzzy dedupe (3,000 names) | 3.02s | **144ms, 21×** |
| Ruby fuzzy dedupe (400 names) | 3.13s | **228ms, 14×** |
| C# fuzzy dedupe (4,000 names) | 4.03s | **312ms, 13×** |
| Java fuzzy dedupe (4,000 names) | 3.50s | **1.18s, 3×** (11× on the function; the rest is JVM startup) |
| C mandelbrot (8 zoom levels) | 431ms | **127ms, 3.4×** |
| C++ fuzzy dedupe (6,000 names) | 3.02s | **1.09s, 2.7×** |

fast-anything ports the outermost loop it can, not the tiny function called inside it, so the app crosses into Rust once instead of millions of times. Porting only the inner `levenshtein` gave 35× and 1.9×.

## Why not rewrite it all?

- **Compile time**: each port is a one-function crate. Seconds, not minutes.
- **Cache**: every port shares one `.fast/target`. Delete it whenever you like.
- **Risk**: your code stays as it is. Rust is opt-in per function, checked against real behavior.

## A

## 4. [arxiv] Sightline: Calibrated Data-Flow Summaries for LLM-Integrated Applications
key: arxiv:2611.26221
url: https://arxiv.org/abs/2611.26221
meta: {"published": "2026-11-19", "authors": ["Zihao Xu", "Yuekang Li", "Ruitao Feng", "Haifeng Shen"], "categories": ["cs.PL", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Programs increasingly call large language models (LLMs), filling prompt placeholders with program values and consuming the output. Such a call crosses the boundary between natural language and programming language (NL/PL). To follow data across it, an analysis needs a data-flow summary of which placeholders the output uses, but no code describes what the model does. Analyses of these LLM-integrated applications therefore taint every output with every input, creating spurious flows, or ask a second model to label each call, which is costly. We prove, and mechanize in Lean 4, that a placeholder flows to the output of a transformer, to first order, only through the attention that reads it (no reading, no flow), and that a faint reading or sensitivity cannot certify that a placeholder does not flow. Unlike reading, the log-probability gradients and Fisher signals of existing methods vanish on confident outputs, and single-span removal fails on duplicated content. Our tool, Sightline, reads a recorded call in one forward pass, learns from labels which reads are uses, and calibrates the pruning to miss at most a chosen fraction $α$ of true flows, on average over call sites, when deployment is exchangeable with calibration. On 2,103 unseen repository families and four models, Sightline is the most accurate summary against the seven closest methods and a hidden-state probe. Calibrated at $α$ = 1%, it misses about 1% of true flows and prunes 43.9-65.6% of spurious flows, 1.6 to 2.6 times as many as the best baseline, and still 43.8-60.1% when calibrated on another collection. Through an open surrogate, it reads models treated as closed about as accurately as they read themselves, without their labels. In the information-flow control of an LLM agent, it removes about half of the labels from inputs that do not flow.

## 5. [youtube] Apple messed up the M5 Ultra 😂
key: yt:Jx6dw1Yu6rk
url: https://www.youtube.com/watch?v=Jx6dw1Yu6rk
meta: {"channel": "Alex Ziskind", "rank": 3, "duration_min": 0}
query: local llm mac benchmark m5

# Apple messed up the M5 Ultra 😂
# Alex Ziskind
# https://www.youtube.com/watch?v=Jx6dw1Yu6rk

[00:00] All right, let's see. We've got the M3 Ultra. The Apple is uh whatever that is. It's not digital, so I don't know how to read it. And this is the M5 Ultra. And we've got Wait, they're the same size. The Apple is the same size on the M3 and the M5 Ultra. It should be bigger on the M5. Come on, Apple.

## 6. [awesome] scrapecrate/mcp-server (new in awesome-mcp-servers)
key: gh:scrapecrate/mcp-server
url: https://github.com/scrapecrate/mcp-server
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-11-22", "language": "Python", "description": "ScrapeCrate mcp-server"}
query: awesome-mcp-servers

# ScrapeCrate MCP server

 

Gives Claude, Cursor, Windsurf and any MCP client every ScrapeCrate endpoint as a tool:
YouTube (transcripts, metadata, comments, channels, search), Google Maps (places, details,
reviews), Trustpilot (companies, reviews), App Store and Google Play (apps, reviews) and the Meta
Ad Library (ads, advertisers).
One tool per endpoint, built from the live catalog, plus `account_balance`.

## Hosted server (no install, no key)

Add `https://api.scrapecrate.com/mcp` as a remote MCP server (Streamable HTTP) and sign in with your
ScrapeCrate account when the client asks: Claude (Settings → Connectors → Add custom connector),
ChatGPT (developer mode connector, OAuth), or Claude Code:

```bash
claude mcp add --transport http scrapecrate https://api.scrapecrate.com/mcp
```

Same tools and prices as the local server below, billed to the signed-in account.

## Local server (API key)

Create an API key at https://scrapecrate.com/dashboard/api-keys, then add to your client:

```json
{
  "mcpServers": {
    "scrapecrate": {
      "command": "uvx",
      "args": ["scrapecrate-mcp"],
      "env": { "SCRAPECRATE_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

Claude Code: `claude mcp add scrapecrate -e SCRAPECRATE_API_KEY=YOUR_API_KEY -- uvx scrapecrate-mcp`

Tool calls cost the same credits as API calls; failed calls are free.
Docs: https://scrapecrate.com/docs/mcp

## Development

```bash
uv venv && uv pip install -e ".[dev]" && pytest
SCRAPECRATE_BASE_URL=http://localhost:8070 SCRAPECRATE_API_KEY=... scrapecrate-mcp
```

## 7. [vault] the actual setup on the slides
key: vault:2026-11-21:the-actual-setup-on-the-slides
url: https://www.instagram.com/p/Df7veiBjiP-/
meta: {"vault_status": "open", "kind": "service", "subject": "@sebastianhardy_ Claude trades stocks 24/7 carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-sebastianhardy-claude-trades-stocks.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: only worth reading if it names a broker API, data feed and risk rules

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Comment-for-DM funnel on AI trading; caption has no method or results, slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-21-sebastianhardy-claude-trades-stocks.md` Link: https://www.instagram.com/p/Df7veiBjiP-/

## 8. [github] pierridotite/mobile-agent-testers: 20 AI testers on 20 different phones, in parallel, on GitHub's free runners: Claude Code agents on iOS Simulators and Android emulators that find broken flows, translation, layout and accessibility bugs
key: gh:pierridotite/mobile-agent-testers
url: https://github.com/pierridotite/mobile-agent-testers
meta: {"stars": 496, "created": "2026-11-16", "pushed": "2026-11-22", "language": "Python", "topics": ["accessibility-testing", "ai-agents", "ai-testing", "android", "android-emulator", "claude", "claude-code", "e2e-testing"]}
query: claude-code created:>{since} stars:>20

# mobile-agent-testers

      
      

**20 AI testers on 20 different phones, in parallel, on GitHub's free runners.**

**[Examples](docs/examples.md)** · **[Compare](docs/compare.md)** · **[FAQ](#faq)** · **[Personas](personas.json)** · **[Releases](https://github.com/pierridotite/mobile-agent-testers/releases)**

English · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Português](README.pt-BR.md)

No test scripts to write. Each tester is a Claude Code agent with its own iOS
Simulator or Android emulator on GitHub Actions. It plays a persona (iPhone SE
in Swedish at the largest text size, Pixel 7 at 200%, iPad in German, Arabic
right to left...), uses your app like a new user (or runs through the feature you
point it at) and writes a bug report with screenshots. Flutter, React Native, Expo, native Kotlin and Swift, Kotlin
Multiplatform, Capacitor and .NET MAUI.

GitHub's runners are free for public repos. You only pay for the model, with your
Claude subscription or API key: about $0.15 to $0.55 per phone in [these runs](docs/runs/).

     
 Real screen recordings of the LocalSend run, idle time cut.  Full video (MP4)  ·  The run, device by device   

[](https://github.com/pierridotite/mobile-agent-testers/actions/workflows/tests.yml)
[](https://github.com/pierridotite/mobile-agent-testers/stargazers)
[](LICENSE)

[](https://github.com/pierridotite/mobile-agent-testers/commits/main)

## What it does

One use per run, set with the inputs of [Test your own app](#test-your-own-app).

- **Explore like new users** (the default). Each persona tries to reach its goal and reports what gets in the way, with numbered screenshots.
- **Run one feature end to end.** Your own brief sends every agent through a whole mechanic: a booking in several steps, an editor with undo, a sync between two screens. Agents tap, long press, swipe and type, leave the app and come back, relaunch it to check what was saved, or open a deep link to start right at the feature, and a brief can raise the budget of about 30 actions. [AnkiDroid's](briefs/ankidroid.md) found the Back field of a new card hidden behind the keyboard.
- **Reproduce a bug report** on every phone: give an issue or the steps, and each agent answers yes, no or unclear, with screenshots ([briefs/reproduce.md](briefs/reproduce.md)).
- **Get an improvement report.** Each persona uses the app once, then says where it hesitated, what it expected and what to change first, by area and impact ([briefs/improve.md](briefs/improve.md)).
- **Compare two versions.** The same personas on two branches or builds, then one table: goals reached, actions, scores, issues seen on one version only ([docs/compare-versions.md](docs/compare-versions.md)). A check before a real A/B test, not a replacement for one.
- **Use a cheaper model**: Claude Haiku, or any Anthropic-compatible API (OpenRouter, DeepSeek, Kimi, GLM, MiniMax, Qwen). The findings are only as good as the model's reading of screenshots and its reasoning ([docs/cheaper-models.md](docs/cheaper-models.md)).

## Applied examples

Real runs on open-source apps, with nothing planted.

| App | Phones | What the agents found | Time, model usage |
|---|---|---|---|
| [LocalSend](https://github.com/localsend/localsend) (Flutter, 100k stars) | 20: 10 Android, 10 iOS, 14 languages | 46 distinct bugs, 1 blocker: on an iPhone SE in Swedish at the largest text size, you can't send a text message at all | 69 min, $4.62 |
| [AnkiDroid](https://github

## 9. [arxiv] EmbodyAgent: Post-Training Embodied VLM Agents via Distillation, SFT, and RL
key: arxiv:2611.26196
url: https://arxiv.org/abs/2611.26196
meta: {"published": "2026-11-19", "authors": ["Wei Dai", "Jinkun Liu", "Jiayi Chen", "Han Liu"], "categories": ["cs.RO"]}
query: all:"language model" AND all:agent AND all:tool

Vision-language models (VLMs) can act as closed-loop robot-use agents (RUAs) by writing and executing control code through tool interfaces. However, turning an open-weight VLM into a high-performing embodied agent requires a complete post-training stack: out-of-the-box open VLMs fail completely at interactive tool contracts, strong frontier teachers are accessible only as black-box endpoints without exposed weights or token probabilities, and supervised imitation alone plateaus under rollout distribution shift. We present EmbodyAgent, an end-to-end post-training framework with three tightly coupled pipelines: (1) a black-box data synthesis pipeline that queries a strong teacher under a forced think-then-code contract and filters trajectories by task success; (2) an SFT pipeline that distills the explanation-and-program targets into an open-weight 9B VLM with both vision and language encoders trainable; and (3) an online RL pipeline that optimizes student-generated episodes via group-relative advantage with a runtime-error-penalized outcome reward. All three pipelines share one primitive-free Python execution tool exposing only raw visual observation and seven-dimensional end-effector control, with no action decoder and no interface shift across stages. Under a strictly separated evaluation protocol on ten LIBERO Spatial tasks (disjoint state splits, greedy test-time decoding, training-only safeguards), held-out success on 100 test states rises from 0/100 (base 9B VLM) to 14/100 (after SFT) and 84/100 (after RL), while training rollout success climbs from 8.4% to 87.7% and median model calls per episode drop from 36 to 11. We further identify a self-reinforcing runtime-error mode induced by outcome-based RL on executable code, and establish a failure-category monitoring and sampling-side curation protocol that stabilizes training.

## 10. [youtube] 🚨 Apple just changed local AI with the M5 Max MacBook Pro 🤖💻
key: yt:ZCa2B0Re36Q
url: https://www.youtube.com/watch?v=ZCa2B0Re36Q
meta: {"channel": "The Anil Lobo Ai", "rank": 4, "duration_min": 0}
query: local llm mac benchmark m5

# 🚨 Apple just changed local AI with the M5 Max MacBook Pro 🤖💻
# The Anil Lobo Ai
# https://www.youtube.com/watch?v=ZCa2B0Re36Q

[00:00] Apple just put a $40,000 GPU cluster in inside a laptop. Nvidia didn't see this coming. They announced the M5 Max MacBook Pro this morning and local AI game just changed forever. You can now run Lama 70B locally. A model that required a $40,000 GPU cluster months ago now runs locally on a laptop. 20 to 30 tokens per second, fast enough to actually use. No cloud, no API bills, no one reading your data, just raw intelligence in your [music] back. Want the link? Comment M5 and I'll send it to you.

## 11. [vault] the free AI video tool on the slides
key: vault:2026-11-21:the-free-ai-video-tool-on-the-slides
url: https://www.instagram.com/p/DfUfbrUDk7S/
meta: {"vault_status": "open", "kind": "tool", "subject": "@tech_hacks.ai make AI videos for free carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-tech-hacks-ai-free-ai-videos.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: need screenshots, compare with the alamin.8020ai list in one pass

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) One-line caption, tool unnamed, slides unseen, nothing assessed Write-up: `TRITON-CORE/Research/links/2026-11-21-tech-hacks-ai-free-ai-videos.md` Link: https://www.instagram.com/p/DfUfbrUDk7S/

## 12. [github] sybil-solutions/skill-distill: Distill a good Claude Code / Codex session into a skill an open-weight model can follow to reproduce the task
key: gh:sybil-solutions/skill-distill
url: https://github.com/sybil-solutions/skill-distill
meta: {"stars": 453, "created": "2026-11-21", "pushed": "2026-11-21", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# skill-distill

A frontier model did a task well. Can an open-weight model do the same task, given the right instructions?

`skill-distill` is a skill for Claude Code or Codex (the **teacher**). You call it at the end of a good
session and name a **student**: an agent harness plus a model, for example omp with DeepSeek-V4.1-Flash.
The teacher then loops:

1. reads the session and writes a skill for the student;
2. starts the student in tmux, on a fresh copy of the starting state, with the original prompt and the skill;
3. compares what the student produced with what the reference produced;
4. finds the first place the student went wrong and fixes the skill there;
5. runs again, three trials per version, until the student matches the reference.

You make the final call: the teacher shows you the reference and the student's best results side by side,
and the skill counts as done only when you accept it.

The result is two things: the reusable **operator skill** in this repo, and a **produced skill** for one task,
one model and one harness.

## Install

```
git clone https://github.com/sybil-solutions/skill-distill
ln -s "$PWD/skill-distill/skills/skill-distill" ~/.claude/skills/skill-distill    # Claude Code
ln -s "$PWD/skill-distill/skills/skill-distill" ~/.agents/skills/skill-distill    # Codex
```

Requirements: `tmux`, `git`, Python 3.10+, and the student harness installed and pointed at its model.
For web results, `pip install playwright pillow && playwright install chromium`.

## Use

At the end of a session that went well:

> distill this session into a skill for omp with deepseek-v4.1-flash on my local server

The teacher follows [`skills/skill-distill/SKILL.md`](skills/skill-distill/SKILL.md). You can watch the
students work with `tmux attach -t distill- `.

## What's in it

| path | what |
|---|---|
| `skills/skill-distill/SKILL.md` | the loop the teacher follows |
| `skills/skill-distill/scripts/distill.py` | run bookkeeping: `init`, `trial`, `status`, `wait`, `evidence`, `verdict`, `ledger`, `report`, `accept` |
| `skills/skill-distill/scripts/extract_session.py` | Claude Code / Codex / omp session log → readable reference (drops system and AGENTS.md text) |
| `skills/skill-distill/scripts/capture_web.py` | serve a web app, drive it in headless Chromium, save screenshots and errors |
| `skills/skill-distill/adapters/` | one script per student harness: omp, pi, Codex, Claude Code, opencode |
| `skills/skill-distill/templates/student-skill/` | the starting shape of a produced skill |
| `examples/` | finished runs: the prompt, the produced skill, the ledger, screenshots |

## Rules the teacher follows

- The student gets the reference's prompt verbatim, a clean starting state, and the skill. Nothing else:
  the student harness's own global context files and skills are turned off where the harness allows it.
- The skill may not contain the reference's finished output or a script that writes it. It teaches the
  steps, decisions, traps and checks; short snippets only where the student can't get a part right otherwise.
- Three trials per skill version. One lucky run proves nothing.
- Checks are tested on the reference first. A check that fails on the reference is a broken check.
- Raw session logs stay in `runs/`, which is git-ignored: they contain your machine's paths and context.

## Adapters

| harness | status |
|---|---|
| omp (oh-my-pi) | tested |
| Codex CLI | tested as the teacher; as a student needs a provider in `STUDENT_

## 13. [youtube] the bonding curve, explained in 30 seconds
key: yt:YBVozFI3lnw
url: https://www.youtube.com/watch?v=YBVozFI3lnw
meta: {"channel": "1EDGE", "rank": 4, "duration_min": 0}
query: solana bonding curve explained

# the bonding curve, explained in 30 seconds
# 1EDGE
# https://www.youtube.com/watch?v=YBVozFI3lnw

[00:00] Why does the price go up every time someone buys? It's not hype, it's a ladder. New coins start on a bonding curve. Every buy is a step up, so the next person pays a bit more. Every sell is a step down, but the ladder has a top, and that's where most coins die. On Solana, the top is 85 SOL. Fill it and the [music] coin graduates into a real pool. Here's the catch. If the dev can pull that pool, the whole ladder was fake. On OneEdge, the pool is locked the second it graduates. Nobody can pull it, not even the dev. Save [music] this and check the next coin you see. Then when
[00:32] someone asks you,
