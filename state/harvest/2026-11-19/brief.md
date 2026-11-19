# Harvest brief, 2026-11-19

13 items shortlisted from 396 candidates (322 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] review gating
key: vault:2026-10-05:review-gating
url: 
meta: {"vault_status": "dead", "kind": "paper", "subject": "Skool YouTube lessons, top 5 test (Jono Catliff, Brendan Jowett)", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/SKOOL-YOUTUBE-TRIAGE.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: 4-5 stars to Google, 1-3 kept private breaches Google policy and UK fake-review rules

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (paper) Videos are medium at best (3 medium, 2 low, no high); the value sits in the linked public repos and docs, not the talk. 188 of 222 lesson videos are outdated (n8n, Antigravity era).

## 2. [hn] Launch HN: Onlook (YC W25) – An open-source developer tool for designers
key: hn:50562320
url: https://github.com/onlook-dev/onlook/
discussion: https://news.ycombinator.com/item?id=50562320
meta: {"points": 77, "comments": 66, "created": "2026-11-19T16:34:04Z"}
query: claude code

Hey HN, I'm Daniel, founder of Onlook ( https://github.com/onlook-dev/onlook and onlook.com). Onlook is a desktop app that puts a canvas on top of your real codebase, letting you design directly in code with the agent you already use. Over 25,000 designers and developers have supported the project, 100+ have contributed, and it's been the #1 trending repo in the world twice. We just rebuilt the entire product as an agentic design tool, and open-sourced it to the community. Here’s a demo video: ( https://youtu.be/BogcYWf4siM ) If you're an engineer, traditional engineering tools are largely built for convergence, whereas designers tend to explore and diverge on ideas. Onlook gives designers a familiar canvas while managing all of the dev processes that get between them and making mind-blowing designs in code. Designers can work on a multiple simultaneous worktrees that run on the real app locally, and every change lands as a PR you can review or throw away, so there aren’t mockups to rebuild. We built Onlook because we believe there needs to be a developer tool that works the way designers do. More and more, designers are expected to work in code. Designers think by seeing, drafting, arranging variations, using references, and remixing ideas. That’s why the canvas has been the signature feature of design tools because it genuinely is useful for how messy the creative process is. Most of the challenge of using engineering tools for design work is that the first half of starting
comment (artur_makly): Congrats on the launch. How does it differ from tools like pen.dev?
comment (instagary): Nice demo video and love that’s open source!
comment (thiagoperes): Very very cool. Seems like there's a huge opportunity here. Cursor got stuck after the acquisition. And especially if paired with open models, I'd definitely use this to avoid using my limits on cc/codex

## 3. [github] Bodila51/gtavi-claudecode: Claude Code plugin that turns GTA 6 streams into paid vertical clips: live campaigns, trending videos, best moments, 9:16 cuts with hooks, captions and credits.
key: gh:bodila51/gtavi-claudecode
url: https://github.com/Bodila51/gtavi-claudecode
meta: {"stars": 838, "created": "2026-11-18", "pushed": "2026-11-19", "language": "Python", "topics": ["agent-skills", "claude-code", "clipping", "gta6", "tiktok", "youtube-shorts"]}
query: claude-code created:>{since} stars:>20

gtavi-claudecode 

  Rockstar made the game. Claude Code makes you the money.  

 GTA 6 is about to break the internet. Claude Code watches the biggest streams, catches the second chat explodes and hands you a ready-to-post vertical clip. Campaigns pay per 1,000 views. You just hit post. 

         
     
  Unofficial fan project. Not affiliated with Rockstar Games, Take-Two or Anthropic.  
  Quick start  ·  Make money  ·  Skills  ·  Clip rules  ·  Scripts  

 

```
/plugin marketplace add Bodila51/gtavi-claudecode
/plugin install gtavi-claudecode@gtavi-claudecode
```

Two lines in Claude Code. In 10 minutes you have: the tools installed, your page folder, today's trending GTA 6 videos, the best moments picked and your first vertical clips ready to post.

## First run: paste this into Claude Code

```
Use gtavi-claudecode. Set up my GTA 6 clip page, ask me your 4 questions in one message,
then do everything after one "yes": find live clipping campaigns, show today's trending
GTA 6 videos and live streams, find the best moments in the top one, cut my first 3 clips
with hooks, check them against the campaign rules, and tell me what to post where.
```

## Two ways to make money

**1. Paid clipping campaigns (fastest).** Streamers and brands pay clippers per 1,000 views on approved clips. On Whop Content Rewards around $1 per 1K views is common; every campaign shows its own rate, budget left and rules. `campaign-finder` reads them live and never guesses a number. You read the rules, clip only that creator, post, submit the link.

**2. Your own faceless GTA 6 page (bigger, slower).** The built-in playbook runs it: daily content mix, credit rules, caption templates, the launch-day "be first" plan and a learning loop. Platforms don't pay for reposted clips, so the page grows on speed, useful tips and credited clips, then earns through campaigns and partnerships.

No income is promised. Your result depends on speed, picks and hooks, and the scoreboard shows what works.

## The rules that make clips win

- Hook in the first second. Say why to keep watching ("the hidden car nobody found").
- 7 to 30 seconds. Cut dead air at the start, end on the payoff.
- Big captions in the safe area. Most people watch muted.
- Make it yours: hook, tip, commentary. Never a plain re-upload. Credit the creator in your post.
- Launch day (Nov 19): players in New Zealand and Australia unlock first. Clip their streams, post to X first, then Reels, TikTok and Shorts, every 1 to 2 hours for 48 hours.
- Every repeated question in your comments becomes a HOW TO post.
- One test per day. No verdict before 24 hours, prefer the 72 h numbers.

## What's inside

| Skill | What you get |
|---|---|
| `setup` | Installs ffmpeg, yt-dlp and faster-whisper, asks 4 questions, builds your page folder |
| `campaign-finder` | Live campaigns: rate per 1K views, budget left, rules, link |
| `trend-radar` | GTA 6 videos from the last 24 h ranked by views per hour |
| `stream-finder` | Who is streaming GTA 6 right now, ranked by viewers |
| `moment-finder` | Best 15 to 40 s moments, scored by loudness spikes, hype words, YouTube "most replayed" and chat spikes |
| `live-mode` | Records a live stream and cuts a clip every time chat explodes |
| `twitch-reaction` | Reaction clips like the viral ones: the streamer's face on top, the game below, a big title on the seam. Finds the top GTA 6 Twitch streams with no account, reads chat and finds the webcam by itself |
| `clip-cutter` | 1080x1920 c

## 4. [arxiv] Ground, Iterate, Trace: Decomposing AI Research Ideation
key: arxiv:2611.24887
url: https://arxiv.org/abs/2611.24887
meta: {"published": "2026-11-18", "authors": ["Samson Yu", "Qiran Zou", "Jing Yu Lim", "Rushi Shah"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Large language models have been widely used to generate plausible research ideas, yet it remains unclear what makes automated ideation effective and how generated novel proposals arise from prior scientific work. We introduce the Creative AI Researcher (CAR), an agentic framework combining literature grounding, iterative development and explicit conceptual operators. CAR constructs a semantic knowledge graph from retrieved literature and equips an ideation agent with graph-retrieval tools and four operators: bisociation, analogy, exploration and elaboration. Each operator call is checked against structural acceptance conditions and recorded, producing a trace of intermediate transformations and declared literature sources. We evaluate CAR with two language-model backbones across 40 LiveIdeaBench research topics and two execution benchmarks. CAR achieves significantly higher methodological novelty (MN) than single-shot prompting and The AI Scientist. Its methodological novelty does not differ significantly from the Research Ideation Agent, while its feasibility scores are higher on both backbones. With a shared experiment executor, CAR achieves the highest pairwise win rate among the evaluated AI methods on FML-bench-Lite and BioXArena. In a ten-condition ablation study, MN point estimates favor CAR over one-step proposal on both backbones, but no MN contrast survives correction for multiple comparisons. The results do not establish a consistent quality benefit from explicit operators beyond free-form iteration. CAR makes the sequence of operations and declared literature sources inspectable, separating judged idea quality from procedural traceability.

## 5. [youtube] How to quickly calculate car depreciation
key: yt:XRfyME2hCX4
url: https://www.youtube.com/watch?v=XRfyME2hCX4
meta: {"channel": "Car Smart Daily", "rank": 3, "duration_min": 0}
query: car depreciation data analysis

# How to quickly calculate car depreciation
# Car Smart Daily
# https://www.youtube.com/watch?v=XRfyME2hCX4

[00:00] Ever wonder why a brand new car loses value faster than you think? First, note the price you paid for the car or the dealer sticker price. This base cost is the starting point for depreciation. Higher initial price means bigger dollar loss each year. Next, determine the car's age in years and apply a typical 15% depreciation per year. A 3-year-old car has lost roughly 45% of its original price. Roughly, each additional 1,000 miles can reduce the car's value by about $100, though the exact amount varies. Finally, apply that percentage
[00:33] to the original price. A $30,000 car losing 45% is now roughly $16,500. Subtract mileage penalties and you have an estimated market value. This estimate shows if selling now beats waiting for a newer model. Follow for a new car fact every day.

## 6. [vault] agent reads Reddit threads
key: vault:2026-10-02:agent-reads-reddit-threads
url: 
meta: {"vault_status": "dead", "kind": "service", "subject": "Reading Reddit threads from an agent browser", "date": "2026-10-02", "where": "TRITON-CORE/Systems/flywheel/listening/reddit-neptune.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: blocked on every agent browser route

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Hard no. The Claude built-in browser pane and the Claude in Chrome extension both refuse reddit.com and old.reddit.com as a safety restriction, and Anthropic WebFetch is refused too. Keyword alerts still arrive by email, but the thread itself has to be read by a person. Job: Listen to Reddit for every venture without an API key (still open)

## 7. [hn] Show HN: TrnRT – An open-source LLM inference engine for AWS Trainium
key: hn:50533270
url: https://github.com/RunanywhereAI/trnrt
discussion: https://news.ycombinator.com/item?id=50533270
meta: {"points": 54, "comments": 8, "created": "2026-11-17T16:01:04Z"}
query: bonding curve

Hi HN, Sanchit here from RunAnywhere (YC W26). We just open-sourced TrnRT: Trainium RunTime, our inference engine for AWS Trainium. We started 3 weeks back, and currently we’re able to serve and run GLM 5.3 flash (FP8) on AWS trn2.48xlarge, and will bring more models support soon. It’s open to contributions :) What it does today: - Serves 2 instances of GLM-5.3 flash on a single box, 8 trn2 with a cache aware router. - Can process 3.57M TPM (tokens per minute) on SemiAnalysis's AgentX benchmarks. - Runs decode as one NKI kernel per layer half, or for the 11 sparse-attention layers fuses both blocks into a single kernel, for faster performance. We started working on Trn2 because we wanted to explore it and see if we can come close to beating it’s performance in terms of cost efficiency compared to H100/H200. A big MoE with 1M context window such as GLM-5.3 flash requires a lot of memory, and memory/tb on a trn2.48xlarge costs less than half compared to 8x h200 on AWS, and hence we wanted to experiment with it and now we’re sharing some early results. But AWS's own stack didn't support the model: vLLM Neuron's latest release did not register any GLM model, and NxDI, AWS's own distributed inference framework, is no longer under active development. We also saw the drop of SGLang Neuron implementation yesterday, but there is no good support for Trn2, which is the only chip available for public use right now. We ran semiAnalysis's AgentX benchmarks, which replays real coding agent 
comment (bookernath): Tokens per minute is a strange metric, I usually see tok/s. A per-second figure would be more accessible in comparing this to alternatives.
comment (badmonster0): how does this compare with sglang
comment (kevo1ution): curious how the token/$ on trainuim compare to nvidia chips and amd. is the future "chipless" inference?

## 8. [github] mankidev/antialgorithm: Claude Code skill that steers the model away from its first, most average pick in creative work: names, ideas, posters, UI.
key: gh:mankidev/antialgorithm
url: https://github.com/mankidev/antialgorithm
meta: {"stars": 493, "created": "2026-11-14", "pushed": "2026-11-18", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# antialgorithm

Claude Code skill for creative work: names, copy, story, game ideas, posters, UI. It makes the model name its first, most average pick, then move away from it for a reason taken from the project.

Both rows came from the same prompt: `Design a poster for a music festival as a 400x600 SVG. Save the final SVG as final.svg in the current folder.` The top row is one batch of six runs without the skill, none left out. The bottom row is picked from about a dozen runs made while the skill was still being written.

## Install

```
git clone https://github.com/mankidev/antialgorithm ~/.claude/skills/antialgorithm
```

The scripts need Python 3. `check.py` also needs numpy, Pillow and `rsvg-convert` (or the cairosvg package).

## Scripts

`seed.py` rolls a starting point when the request is thin. A visual seed gives a making method, colors, layout, type, a verb and a scale for the idea, a setting, a region and, half the time, an object. A text seed gives a voice, a way in and a register. An idea seed gives a verb, a constraint, a scale and a pressure. It draws from system randomness, so two people sending the same prompt start in different places. It also saves each seed to `history.jsonl` in the skill folder and skips values from the last few, so your own seeds don't repeat from one session to the next. `--keep "axis=value"` holds an axis fixed, which lets you keep a subject and roll only the look.

`moves.py` keeps a short log of the main move behind each off-default answer, such as "neon tube wall, almost no type". The model reads it before showing new work, so it doesn't reuse a move that worked last time just because it worked.

`rough.py` takes an SVG and shakes its straight lines, shapes and letters, and breaks the even spacing of repeated marks, so a hand-made look drawn in code stops looking plotted. It is only for hand-made methods such as print, paint, stamps and ink; screen, camera and render looks keep their own marks.

`check.py` renders an SVG at full size and at icon size and lists text that runs off an edge, sits under a shape, has low contrast or is too small. The size limit fits posters; for an app screen use `--min-text 0.6`.

Visual rules live in `visuals.md`, which the model reads only for visual work, so a name or a slogan doesn't load them.

## License

MIT

## 9. [arxiv] Large Language Models or AI Agents for English to Arabic Translation? An assessment on WikiEn-Ar190
key: arxiv:2611.24588
url: https://arxiv.org/abs/2611.24588
meta: {"published": "2026-11-18", "authors": ["Fatima Zahra Iguenfer", "Yousra Chtouki"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

This research investigates whether a large language model or an autonomous AI Agent performs better at translating from English to Arabic, which is considered a low-resource language. The authors introduce WikiEn-Ar190, a new dataset of 190 carefully selected Wikipedia articles from 18 different areas, which were created and verified by two native Arabic speakers to ensure that they accurately reflect both meaning and style. Using this dataset, the study evaluates the translation quality of GPT-5-mini both as an independent neural translator and when used within a more complex process that includes self-assessment and improvement. As a standalone model, GPT-5-mini produced very fluent translations , achieving a COMET score of 0.8649 and receiving high human scores for adequacy, fluency, and style (averaging 4.53 out of 5). When used in a system that combined translation with self-assessment, it improved lexical accuracy by 28.76% (BLEU score of 22.83) while maintaining a similar level of semantic quality. These findings show that methods involving autonomous reasoning can improve translation consistency for language pairs with limited resources. Beyond the results, the approach offers a framework for evaluating and improving translations, potentially using them as assisting tools to expand the representation of low resource languages, such as Arabic, on the web.

## 10. [vault] Selling database reactivation cold to small local businesses that have no list
key: vault:2026-10-01:selling-database-reactivation-cold-to-small-local-businesses
url: 
meta: {"vault_status": "dead", "kind": "service", "subject": "AI Automation Agency Ninjas (Skool, Dan Wardrope), database reactivation community", "date": "2026-10-01", "where": "TRITON-CORE/Ventures/Neptune-Marketing/research/SKOOL-DBR-COMMUNITY-2026-10-01.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Read as a member. Free classroom is two lessons; 22 courses sit behind purchases or HighLevel affiliate tiers. Of 180 member posts sampled, 2 report money received and 129 ask for help; the owner says the offer is not for small local businesses. Big results are all owner-reported. No post covers the UK consent position for SMS to old leads. The method needs a client with a large recent list.

## 11. [hn] Tokendoctor – See what your Claude Code use overpays
key: hn:50526584
url: https://github.com/localixai/tokendoctor
discussion: https://news.ycombinator.com/item?id=50526584
meta: {"points": 34, "comments": 17, "created": "2026-11-17T02:19:50Z"}
query: claude code

comment (renegat0x0): I have a list of ai related tools. There is so many of them For example limiting token usage i think can also be achieved by 'caveman' project. It achieves it differently but the goal is same i suppose Overall Ai tools I found: https://github.com/rumca-js/awesome-database-top/blob/main/l...
comment (relyks): I use this and it works well: https://github.com/rtk-ai/rtk I'm trying to figure out if I can use multiple of these tools together without conflicts
comment (mkagenius): > https://github.com/localixai/tokendoctor/tree/main/bench Don't we need to run it on all of the benches those models publish? This doesn't look very comprehensive. Moreover half of the times factory claude code is better than 'advised' one. Although I don't discourage such experiments, I feel this one is way complicated for very little or no gain provably.

## 12. [github] bookwjitchieni1986/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows. Works with ChatGPT/GPT, Claude, Gemini, Ollama, OpenCode. Blender AI addon, copilot for 3D, bpy Python scripting, MCP integration.
key: gh:bookwjitchieni1986/blender-ai-mcp-addon
url: https://github.com/bookwjitchieni1986/blender-ai-mcp-addon
meta: {"stars": 451, "created": "2026-11-19", "pushed": "2026-11-19", "language": null, "topics": ["ai-agents", "ai-assistant", "blender", "blender-addon", "blender-ai", "blender-automation", "blender-mcp", "blender-plugin"]}
query: mcp server created:>{since} stars:>30
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

﻿# mcp-for-blender-pro

### Your Blender scene. Your AI models. One creative workspace.

**An AI assistant for Blender that can inspect your scene, build objects, edit materials, find assets and carry out multi-step workflows—with a visual chat workspace and a built-in Model Context Protocol (MCP) server.**

[Download](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon/releases/latest) · [Getting started](docs/QUICKSTART.md) · [Connections and agents](docs/CONNECTIONS.md)

## Turn a creative brief into scene operations

Start with an idea. Ask the assistant to inspect your scene, create a product-display layout, arrange objects, assign materials or prepare an export. Follow its actions in the conversation and inspect the result in the viewport preview. Keep working in Blender throughout the process.

**mcp-for-blender-pro brings conversation, scene tools, model choice and agent workflows together.** It is designed for artists who want faster iteration, technical artists who automate repetitive work, and developers connecting AI tools to Blender.

## Why choose mcp-for-blender-pro?

| Capability | What it gives you |
|---|---|
| **Blender-aware assistance** | Scene and object inspection gives the assistant context before it acts. |
| **A visual Studio workspace** | Chat, scene objects, viewport snapshots, approvals and a task board in a companion window. |
| **Your choice of AI** | Connect supported cloud providers, local Ollama models or compatible custom endpoints. |
| **Saved connections** | Keep work and personal connections separate, including multiple keys for the same provider. |
| **One assistant or a team** | Use a single model for quick changes, or managers, workers and reviewers for structured tasks. |
| **Built-in MCP server** | Connect OpenCode and other clients supporting authenticated Streamable HTTP MCP. |
| **21 scene tools** | Create, inspect, edit, capture, search assets, consult Blender APIs and export scenes. |
| **Multilingual menus** | Choose English, German, French, Spanish or Chinese for the main interface. |

## From a quick edit to an agent team

Use **Single assistant** for direct, conversational work. For larger tasks, configure a **Team chain** with individual responsibilities, instructions and models.

- **Manager:** breaks the request into assignments and acceptance criteria.
- **Workers:** perform the assigned scene operations.
- **Reviewers:** inspect results and approve work or return specific findings.

Tasks run sequentially so scene edits stay ordered. A blocked task gets one correction attempt; a second failed review stops the workflow. The task board exposes assignments, attempts and review findings as work progresses.

## Connect the models that fit your work

Supported connections include **OpenAI, Anthropic Claude, Google Gemini, OpenRouter, OpenCode Zen, Ollama and custom APIs**. Load the available model catalog and select a model directly in Blender or Studio.

Custom endpoints support OpenAI Chat Completions, Anthropic Messages and Ollama protocols. Choose models with tool-calling support; image-capable models can also interpret viewport screenshots. OpenCode-only free models are available through the OpenCode client.

## Install and create

1. Download **`mcp-for-blender-pro.zip`** from [Releases](../../releases/latest).
2. In Blender, open **Edit → Preferences → Get Extensions → menu → Install from Disk**.
3. Select the ZIP, enable **mcp-for-blender-pro**, then open **3D Viewport → 

## 13. [hn] Show HN: Robotics needs better CAD, so I wrote a B-rep kernel and 3,487 tests
key: hn:50552140
url: https://springcraft-ai.github.io/springrep/
discussion: https://news.ycombinator.com/item?id=50552140
meta: {"points": 33, "comments": 9, "created": "2026-11-18T21:08:47Z"}
query: claude code

Hey HN, I’m Tony. I’m a co-founder of Springcraft, where we have been doing a lot of CAD modeling for robot parts. Our team kept running into limitations with existing kernels, and so I decided to write a new B-rep kernel and a new comprehensive, kernel-agnostic B-rep conformance test suite. Both are available today under MIT licenses. The kernel, springrep, is written in safe Rust with no dependencies. It covers a broad range of our mechanical CAD needs, including advanced fillets, sweeps, lofts, shells, offsets, STEP and exact measurements and queries. Claude Code made it feasible to write this, but it took a lot of time and care to get it right. The test suite, brep-conformance, has 3,487 cases covering the modeling operations common across kernels: booleans, fillets, chamfers, shells, offsets, sweeps, lofts, STEP, and queries with expected answers coming from closed forms and exact geometry. It caught hundreds of bugs, edge cases, and hot spots in springrep that our own tests had missed, and now springrep passes all of it. We’ve also run it on a few popular open-source kernels and anyone can run it on theirs. This is the first version, so there are surely mistakes in the test and adapters. Corrections, pull requests, and new kernels are welcome. kernel: https://github.com/springcraft-ai/springrep conformance suite: https://springcraft-ai.github.io/brep-conformance/
comment (dofm): Now this is a great application of an LLM. I'm sure you still have loads to solve and a lot of quite human decisions to make (because bRep is one thing; contemporary CAD 'default solutions' strike me as likely to be full of human compromises), but I can see that having an LLM on the team to help with the maths must help. Best of luck with it :-)
comment (waterTanuki): Why this instead of extending/supporting solidcore? (also in Rust) https://github.com/tangency-labs/solidcore Your performance table is treating brep-conformance like it's some kind of backend server that processes x requests per n seconds, but that's now how geometry kernels work. How does this enable faster/smoother workflow than solidcore? Can you demonstrate that with a side-by-side video? No one, not even people who work with CAD all day can understand any benefits this has from a table.
comment (ffdsc): > so I wrote No you didn't, you asked an LLM to write it.
