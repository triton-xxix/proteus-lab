# Harvest brief, 2026-11-20

13 items shortlisted from 394 candidates (325 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] Generated creators posing as customers, watermark removal and engagement pods
key: vault:2026-10-01:generated-creators-posing-as-customers-watermark-removal-and
url: 
meta: {"vault_status": "dead", "kind": "service", "subject": "AI Video Bootcamp course, judged after building a framework from it", "date": "2026-10-01", "where": "TRITON-CORE/Systems/video-bootcamp/README.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: break UK ad rules or platform rules

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Indexed in full: 1,515 reusable assets from 94 lessons and 44 guides. Strongest on ad strategy and scripting, the camera and lighting vocabulary, the avatar and clone methods and the short-film production bible. Thin on settings and numbers, about a third is a tour of its founders own platform, and 58 of the assets are advice we will not use: generated creators speaking as customers, watermark removal, engagement tricks, other peoples characters. Job: turn a paid course into a repeatable production process (solved)

## 2. [hn] Show HN: Fast deterministic natural language search for OpenStreetMap data
key: hn:50561199
url: https://hippomaps.ch/?q=cafes+by+the+Limmat+100+m+from+the+lake+in+zurich#map=15.02/47.36708/8.54935
discussion: https://news.ycombinator.com/item?id=50561199
meta: {"points": 120, "comments": 32, "created": "2026-11-19T15:16:02Z"}
query: open data api

I want to show you HippoMaps. It is a fully featured map and navigation app built on OpenStreetMap with a custom Overpass API engine for really fast search of POIs, areas and ways. My aim with HippoMaps is to get to a level where I don't need Google Maps anymore. The biggest hurdle IMHO with OSM based apps is the lack of nice and fast search (where GMaps excels at). To get there I started working on a deterministic (as in no LLMs used) parser of queries that translates them to the Overpass QL. Search queries are split into tokens and the algorithm tries to guess "what" you want to search and "where". The former comes from a word list (known brands, sports, OSM tags) and the latter from the geocoder service (Photon). You can get quite creative like "cafes in Zurich by the Limmat", "peaks over 4000 m in Valais", "pharmacies open now in Bern". It's good for discovering hiking trails, e.g. "hiking trails from Arth-Goldau to Rigi Kulm". It knows how to find stuff between two places, next to a place, near a place and so on. You can stack those as well like "bridges over the danube in serbia 50 km from novi sad". Except the search it has almost all of the features you would expect from a map like turn-by-turn navigation (Valhalla) with voice (Piper), public transport navigation in Europe (MOTIS), live traffic (only a few countries so far). The app is GPL-3.0: https://github.com/cdutsov/hippomaps I'm looking forward to feedback on searches that work or don't work for you + overall co
comment (ijustlovemath): Does it work offline? That's the main time I use osm
comment (solarkraft): Natural search feels like such a mundane feature, but I consider it damn near revolutionary. Properly setting filters is literally impossible with most maps apps and with the others it’s just impossibly hard. So cool that you managed to do this deterministically!
comment (oshawaconnectio): This is really nice, thanks! A feature request, can you add "houses" as a searchable feature? E.g. "houses more than 1km away from sewage works and more than 200m away from major train lines and more than 200m away from any loud pubs". IMO that would be a cool feature for people searching for places to rent

## 3. [github] vaibhav-space/my-ai-coding-workflow: Production-grade AI coding instructions, curated skills, and a 3-stage review pipeline (Planning → Critical Review → Diff Audit) built after 4,500+ hours with AI agents. Agent-agnostic.
key: gh:vaibhav-space/my-ai-coding-workflow
url: https://github.com/vaibhav-space/my-ai-coding-workflow
meta: {"stars": 320, "created": "2026-11-14", "pushed": "2026-11-18", "language": "HTML", "topics": ["agentic-workflows", "ai-agents", "claude-code", "code-review", "developer-tools"]}
query: claude-code created:>{since} stars:>20

# I Spent 4,500+ Hours Coding with AI. This Is the Claude Code Setup I Ended Up With.

> *The engineering instructions, curated skills, and three-stage review workflow I use to keep AI-assisted development fast, controlled, and verifiable.*

**At a glance**

- **What it is:** one global rules file (`CLAUDE.md`) and three prompts: plan, critique the plan, audit the result.
- **Who it is for:** solo developers and small teams who let an AI agent write real code and want proof, not promises.
- **What it is not:** a framework or an app. It is a few text files plus some optional helpers. The rules are instructions the agent follows, not locks.
- **Evidence:** this is my own working setup. There is no public example project built with it yet.
- **Start here:** [Quick start](#quick-start). Not sure what to type? [Which command, when, and why](#which-command-when-and-why).

---

## Table of Contents

- [Quick start](#quick-start)
- [Which command, when, and why](#which-command-when-and-why)
- [1. The Story Behind This Setup](#1-the-story-behind-this-setup)
- [2. Core Engineering Philosophy](#2-core-engineering-philosophy)
- [3. The Three-Prompt Review Workflow](#3-the-three-prompt-review-workflow)
- [4. Curated Skills & Upstream Attribution](#4-curated-skills--upstream-attribution)
  - [Superpowers (Jesse Vincent)](#superpowers)
  - [Ponytail (Dietrich Gebert)](#ponytail)
  - [I Have ADHD (ayghri)](#i-have-adhd)
- [5. Repository Structure](#5-repository-structure)
- [6. Adoption Guide](#6-adoption-guide)
- [Optional hard gates](#optional-hard-gates)
- [What the community said](#what-the-community-said)
- [7. Credits](#7-credits)

---

## Quick start

For Claude Code. Needs `bash`. Tested on Linux.

```bash
git clone https://github.com/vaibhav-space/my-ai-coding-workflow
cd my-ai-coding-workflow
./install-commands.sh
```

Restart Claude Code and type `/plan`.

The script adds three slash commands, `/plan`, `/review-plan` and `/review-prod`, and copies the plan page template to `~/.claude/plan-template.html`. It skips any file you already have. Pass `--force` to replace files, and it keeps a `.bak` copy.

For the global rules, copy `CLAUDE.md` to `~/.claude/CLAUDE.md` (see the [Adoption Guide](#6-adoption-guide)). If you already have one, merge by hand instead of replacing it.

Using Gemini CLI or Cursor? Copy and paste the prompts from `prompts/` instead.

---

## Which command, when, and why

| You want to... | Type | Why | You get |
|---|---|---|---|
| Fix a typo, or change 1 to 3 files you can name | Just ask. No command. | A plan would cost more than the change. | The change. |
| Build something bigger, or you are not sure how big it is | `/plan` | The agent reads your code and shows a plan before it touches anything. | An interactive plan page with tickable steps. No code is written. |
| Check the plan before you build | `/review-plan` in a **new chat** | A reviewer that did not write the plan has no reason to agree with it. | A verdict, the problems found, and a corrected plan. |
| Check the result before you commit | `/review-prod` in a **new chat** | It reads the real file changes and runs the tests, not the agent's summary. | Proof it works, fixes for what broke, and a "Could not verify" list. |

**The routine, in 5 steps**

1. Type `/plan` and describe what you want. Read the page and tick the steps. Tell the agent what to change.
2. When the plan looks right, say "approved". Nothing is built before that.
3. Open a **new chat**. That m

## 4. [arxiv] Replication of Agentic Security Events: Audit and Investigation (ROGUE-AI)
key: arxiv:2611.26553
url: https://arxiv.org/abs/2611.26553
meta: {"published": "2026-11-19", "authors": ["Mengxiao Wang", "Mahbub Alam", "Kalyan Nakka", "Nitesh Saxena"], "categories": ["cs.CR", "cs.AI", "cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Agents based on large language models (LLMs) can now delete files and send payments on behalf of their users. News media reports routinely describe failures of these agents (e.g., Replit's coding agent deleting a production database), but a report often only says what went wrong and rarely (in)validates the incident or finds its root cause. Incident catalogs collect these reports, and benchmarks record whether agents fail, but neither replicates an incident nor tests the cause its report might identify. In this paper, we present ROGUE-AI (Replication of Agentic Security Events: Audit and Investigation), a multi-agent framework that closes the above gap and rebuilds each reported incident offline together with a matched control that lacks only the blamed cause, and runs agents on both. Our results suggest that ROGUE-AI is able to reproduce the reported harm in 89% of its 108 attempted replications. Agents built on five current GPT, Claude, Gemini and DeepSeek models made the reported mistake in 18% to 33% of runs, against at most 1% without the blamed cause. Of the 72 incidents with real-world harm, 62 had no underlying attacker, and in these, agents did what their task asked for but missed an ordinary hazard, such as a database shared with the live site. Replications without an attacker caused more harm than replications of prompt injection for all five models. Defenses against prompt injection look for injected instructions, but these replications contain none. Further, a warning after each tool output that names the hazard and its consequence lowered harm for all five models, whereas a note of the same length that does not mention the hazard left most of the harm in place. Built from real incidents, the ROGUE-AI replications form a reusable audit framework that vendors can rerun before each new release.

## 5. [youtube] I Built A World Cup Prediction Model. Here's How It Compares To Opta
key: yt:S3ZZoYwl8xg
url: https://www.youtube.com/watch?v=S3ZZoYwl8xg
meta: {"channel": "The Stat Room", "rank": 3, "duration_min": 11}
query: dixon coles model python

# I Built A World Cup Prediction Model. Here's How It Compares To Opta
# The Stat Room
# https://www.youtube.com/watch?v=S3ZZoYwl8xg

[00:00] The World Cup starts in a few weeks. Everyone is excited. The most watched sporting event on the planet. National teams from across the globe play each other for one title. World champion. And like every major sports event, the same question comes back every time. Who wins it? Recently, we have a new trend where supercomputers with advanced statistical models compute huge amounts of football data to try and predict the outcome of the tournament. The most famous one is the Opta predictor. A model that
[00:32] computes a huge number of metrics all the way down to the player level. The most complete and most in-depth model out there. So, I got curious. How does it work? Do we really need all this data and a supercomputer to predict the World Cup winner? I decided to take matters into my own hands and try to build my own model using only data that is publicly available. The goal, see how close I can get to Opta's prediction accuracy with these limited resources. Stick till the end. I will show the results of my model on the 2026 World
[01:04] Cup, too. Opta is the gold standard for football predictions. They publish a pre-tournament forecast that everyone in the analytics world treats as the benchmark. For the 2022 World Cup, they had Brazil as favorites at 16.3%. Argentina second at 13.1% and France third at 12%. Argentina won. Opta got that wrong. So did everyone else. But, that doesn't mean Opta was bad. Predicting the World Cup is generally hard. Even the world's best
[01:38] model only got five out of eight actual quarterfinalists right. So, before I start building my model, I need to evaluate how good Opta actually did on the 2022 World Cup prediction, so I can compare it to my own model. But, how can we accurately measure a model's performance? I narrowed it down to three major categories: top teams hit rate, group winner hit rate, and Brier scores. Every metric gets computed the same way for Opta and my own model. Let's start with the easy one, top teams
[02:11] hit rate. This is what Opta predicted as their top eight teams. Five out of eight actually made the quarterfinals. They missed it Croatia, Morocco, and Portugal. For the top four, they got two right, Argentina and France, and missed it Croatia and Morocco. For the top two finalists, they got France right, but missed it Argentina. And since their number one was Brazil, the tournament winner pick was wrong, too. Not bad as a result for a World Cup full of surprises. Second category, group winner hit rate.
[02:47] Six out of eight. They only missed Japan in group E and Morocco in group F. Both were major upsets, nobody saw them coming. Now, for the complicated stuff, Brier score. Brier score is a method developed in 1950 by an American meteorologist named Glenn Brier. It was originally built to evaluate weather forecasts. Today, it's used everywhere, even in elections. It's what you'd use to grade a model that outputs probabilities. The simple version, Brier score measures how close your probabilities matched
[03:21] what actually happened. So, here are Opta's six Brier scores. Now that we've seen Opta's scores, let's get to my model. First, I needed publicly available data. Luckily, there's a data set online that contains every single international football match played since 1872 up to today. I cut it down to only the five years before 
[transcript continues in field-notes/staging/S3ZZoYwl8xg.txt]

## 6. [vault] Promptwise as our platform
key: vault:2026-10-01:promptwise-as-our-platform
url: 
meta: {"vault_status": "dead", "kind": "tool", "subject": "AI video tool stack as of October 2026 (Veo, Nano Banana, Seedance, Kling, MiniMax H3, Wan, HeyGen, fal)", "date": "2026-10-01", "where": "TRITON-CORE/Systems/video-bootcamp/STACK.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: no public API and nothing in the method needs it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Checked on vendor pages 1 Oct while building the video framework. We already hold enough to draft most work by API: Veo 3.1 and the Nano Banana image models on a Gemini key, ElevenLabs for voice and sound, HyperFrames for the edit. The course picks have aged: MiniMax H3 and Wan 3.0 now out-rank Kling 3.0 and Veo 3.1 for image to video, Nano Banana 2 out-ranks Pro at half the price, Gemini Omni cannot edit uploaded video from the UK, and Seedance refuses real faces, so a real person on screen is a HeyGen job. Job: choose a draft route and a final route for each video job (solved)

## 7. [hn] Show HN: OpenComputer – an open source alternative to Devin
key: hn:50581403
url: https://github.com/diggerhq/opencomputer
discussion: https://news.ycombinator.com/item?id=50581403
meta: {"points": 42, "comments": 14, "created": "2026-11-20T20:19:56Z"}
query: bonding curve

Hi HN! Utpal here, I'm one of the founders of OpenComputer. OpenComputer is an open source cloud coding agent for teams that can run in your own cloud account (AWS, GCP, Azure). We run the agent harness and the sandbox on the same durable VM (architecture in the docs [1]). First commit lands in 24s; the alternatives we benchmarked took 53-72s (benchmarks below [2]). Two other choices: - One VM per team, scalable horizontally. Sessions are isolated in git worktrees. - Session files are backed up to a repo after every turn, so any session can resume on another VM. We noticed that past ~640 session-hours a month, one always-on 4 vCPU VM is cheaper than per-session E2B sandboxes, for example. So at scale, this setup would not only be faster than current SOTA coding agents, but also more cost-efficient. Feel free to try via cloud for free [4] or self host. We would love any and all feedback, and happy to answer any questions! Full demo below [3]. [1]: https://docs.opencomputer.dev/getting-started/architecture [2]: https://opencomputer.dev/blog/cloud-agents-as-fast-as-local/ [3]: https://x.com/IgorZIJ/status/2121309785882591711 [4]: https://app.opencomputer.dev
comment (taudas): New product name please, your current name tells us nothing and is already taken. But I am still going to try it :)
comment (namanyayg): Open source is amazing! Any insights how you've made something so cheap and fast? Are the margins charged by Devin really this insane?
comment (sleepytimetea): Don't have Slack, will it work with Discord ?

## 8. [github] diego3g/craft: Design skills for AI agents: /craft-setup writes your design brief, /craft designs screens with every state from your design system and reviews them. Works with Paper, pen.dev, Figma or HTML.
key: gh:diego3g/craft
url: https://github.com/diego3g/craft
meta: {"stars": 300, "created": "2026-11-15", "pushed": "2026-11-17", "language": "JavaScript", "topics": ["agent-skills", "claude-code", "claude-code-plugin", "design-system", "figma", "paper", "ui-design"]}
query: claude-code created:>{since} stars:>20

Design skills for AI agents.  Complete screens with every state, and a design system that stays consistent. 
  Works with Paper, pen.dev, Figma or plain HTML, in Claude Code, Codex, OpenCode, Cursor and other agents.
 

 
     
 

---

Ask your agent for "a pricing page" and, with craft installed, it works like a careful designer:
- it writes a short design brief first;
- it lists every state the screen can be in;
- it uses your design system's pieces;
- it checks its own work before showing it.

It stops for your "yes" where it matters and writes its decisions down for next time.

## Install

### Claude Code, Claude Desktop and claude.ai

Install craft as a plugin. Inside a Claude Code session:

```
/plugin marketplace add diego3g/craft
/plugin install craft@craft
```

- The plugin adds a session-start hook, so every request goes to the right skill by itself.
- Skills carry the plugin name: `/craft:craft`, `/craft:craft-setup` and so on.
- Update from your shell with `claude plugin update craft@craft`.

In Claude Desktop or claude.ai, go to Customize › Plugins › Add › Add marketplace, then enter `diego3g/craft`.

### Codex, OpenCode, Cursor and other agents

Install the skills with the [skills CLI](https://skills.sh):

```
npx skills add diego3g/craft
```

It asks which agents to install into. You can also name the agent yourself:

| Agent | Command |
|---|---|
| Codex | `npx skills add diego3g/craft -a codex` |
| OpenCode | `npx skills add diego3g/craft -a opencode` |
| Cursor | `npx skills add diego3g/craft -a cursor` |
| Gemini CLI | `npx skills add diego3g/craft -a gemini-cli` |
| GitHub Copilot | `npx skills add diego3g/craft -a github-copilot` |
| Windsurf | `npx skills add diego3g/craft -a windsurf` |

- Add `-g` to install for every project instead of only the current one.
- Run `npx skills update` to update later.

These agents don't run the session-start hook. Paste the routing below into your `AGENTS.md` so the agent still picks the right skill.

 
  Routing for AGENTS.md  

```markdown
## Design skills
Before responding to anything that designs, reviews or changes a UI, check this table and use the skill.
First look whether DESIGN.md exists at the project root.
- No DESIGN.md and a design task → craft-setup, then craft
- Design / create / redesign a page, screen, flow or element → craft
- "Options", "alternatives", "I don't like it" → craft-explore
- "Review", "refine", "make it better", or before showing your own design → craft-critique
- Tokens, style guide, a component, "audit" → craft-system
- "Bring our design system into  ", "apply the guide changes to the code" → craft-sync
- "What states are missing?" → craft-states
Small edits the person described exactly (one value, label or size): just make them.
A stop means ending your turn with the question. Never decide a stop for the person.
```

 

**By hand:** copy the folders in `skills/` into your project's `.agents/skills/`, then add the routing above.

## The skills

| Skill | What it does |
|---|---|
| **`craft-setup`** | Interviews you one question at a time: product, audience and voice, mood, brand, references, constraints. It then writes `DESIGN.md` and builds the foundations (tokens and base components). |
| **`craft`** | The main command, for designing a page, screen, flow or element. It confirms the scope, then for each screen lists the states, draws with your system's pieces and checks the result. |
| **`craft-states`** | Lists every state a screen can be in (e

## 9. [arxiv] Seer: Guiding Small Deep-Research Agents with Shared Decision Models
key: arxiv:2611.26423
url: https://arxiv.org/abs/2611.26423
meta: {"published": "2026-11-19", "authors": ["Yuhao Zhou", "Yang Zhou", "Yuanxi Li", "Jindi Lv"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Deep-research agents repeatedly decide what to search, read, and verify, often using large cloud-hosted language models for action proposal. However, privacy and local control motivate running agents on users' devices, where limited memory and compute favor smaller models and complicate on-device training. Yet inference-time guidance faces three obstacles: exploring alternatives through real execution adds tool calls, prompted self-evaluation is bounded by the agent's judgment, and model-specific guidance risks repeated adaptation costs. We introduce Seer, an inference-time framework providing local guidance that separates the agent's action proposal from learned consequence prediction and value estimation. From a shared corpus of real research trajectories, we train two models: a tool-response simulator on observed call--response pairs and a value estimator on histories labeled with discounted terminal correctness. The simulator and estimator are trained offline and reused across agents without further training. Moreover, Seer executes only the selected action and adds only real tool responses to the committed history, avoiding tool calls on discarded candidates at additional inference cost. Across multiple deep-research benchmarks, Seer substantially improves agent performance for different language models. For instance, GAIA accuracy rises from 13.6% to 41.7% for Qwen3.5-4B and from 22.3% to 50.5% for Qwen3.5-9B. Furthermore, our analyses suggest that broader candidate coverage can compensate for imperfect simulation, while prediction and scoring errors limit the benefits of wider imagined search. These findings highlight the potential of reusable models for prediction and evaluation to strengthen small research agents through extra local computation without the real execution of the discarded candidates.

## 10. [vault] Scraped-list cold voice, SMS and email blueprints for UK prospects
key: vault:2026-10-01:scraped-list-cold-voice-sms-and-email-blueprints-for-uk-pros
url: 
meta: {"vault_status": "dead", "kind": "service", "subject": "Automatable Free (Skool, Jono Catliff), free tier", "date": "2026-10-01", "where": "TRITON-CORE/Education/Courses/automatable-free/DIGEST.md", "has_transcript": false}
query: dead
VAULT THREAD, status dead: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: dead, meaning the vault closed it, for the reason in the note; that reason may be about the vendor or Luke's time rather than the idea.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Joined free and extracted 148 lessons with 195 blueprint attachments. It is a sampler for a paid community: each mini-course gives one to three lessons. Best free material is two call recordings holding a complete speed-to-lead sales workflow and a city by service Google Ads keyword method. Several lead-sourcing blueprints rely on scraping plus cold calls, texts or email that need consent in the UK, and the review gating it teaches conflicts with platform and regulator guidance.

## 11. [hn] Ask HN: Where do you see Software in 5 years?
key: hn:50565484
url: https://news.ycombinator.com/item?id=50565484
discussion: https://news.ycombinator.com/item?id=50565484
meta: {"points": 19, "comments": 25, "created": "2026-11-19T20:01:18Z"}
query: car data

I wanted to hear some good opinions on all things AI and how they transform the Software industry. I'm anxious about the future and lack the foresight to form any opinion on what to do next. For context, I'm a L4 SWE that has more or less say 5-10 yrs of exp. I've enjoyed my work throughout my career, AI makes me ship more, much more than I could do 3 years ago. I feel I use it well and it translates into really good software. That said, what do you think happens in years to come with the Software industry in general? Do you think we'll go through a massive erosion of jobs? What's your perspective on that? I'm asking because I honestly don't know what to do: I can try to always keep up to date with newest technologies, best practices, but I'm only me; if the demand for SWEs and jobs falls to the floor, I'm not sure I'll always get a place at the table (i.e. land a job) and I'm wondering whether I should try to do something else in some other industry. It feels weird to be in a good position in life and still constantly worry about it getting worse.
comment (ethnrob): where do you see it in 5 years? if you're anxious about job security, standing out in your career is generally not specific to the industry you are in.
comment (austin-cheney): In 5 years time software will exist in 3 silos. It's really not any different today, except the talent will continue to diverge. Silo 1 - This will be employers strongly forcing AI for most task completion. This will be most large corporate employers and most start ups. There will be little to no working knowledge of the internals of large applications and these employers will bleed money on outside consultants to occasionally provide manual maintenance and security hot fixes. Everything will continue to look good from the outside, but really its a messy house of cards. Silo 2 - This will be i
comment (spottedmarley): In 5 years I don't see myself using any software that I didn't design and build myself. I'm already ~30-40% there, 100% is not yet feasible but in 5 years time (maybe less) it will happen.

## 12. [github] JuneYaooo/rea-toon: AI 拆解学习短剧：为什么火、剧本怎么写、每一镜怎么拍 | Break down any short drama with AI: why it works, the script, every shot
key: gh:juneyaooo/rea-toon
url: https://github.com/JuneYaooo/rea-toon
meta: {"stars": 284, "created": "2026-11-14", "pushed": "2026-11-18", "language": "Python", "topics": ["ai-agent", "chinese-drama", "claude-code", "codex", "drama-analysis", "screenplay", "short-drama", "storyboard"]}
query: claude-code created:>{since} stars:>20

Break down any short drama with AI: animated comic dramas, live-action and AI-generated.

A tool for learning from short dramas: why one went viral, how the script is written, how every shot is filmed.

Every breakdown is also written as **[VIDEO.md](https://videomd.github.io/videomd/)**, an open format that agents read layer by layer.

[中文](i18n/README_zh.md) | English | [日本語](i18n/README_ja.md)

[](https://github.com/JuneYaooo/rea-toon/stargazers)

[](https://videomd.github.io/videomd/)
[](https://github.com/JuneYaooo/rea-video)
[](LICENSE)

[](https://linux.do/) [](https://discord.gg/dZj8D3GqWT) [](i18n/README_zh.md#社区) [](https://x.com/yao_june12106)

⭐ *Help more people find rea-toon. Star this repo!*

   

The pages of a 10-episode drama after the breakdown. Click for the full demo with sound (1 min). 
 rea-toon writes the breakdown in the language you talk to your agent in. 

 

## Quick start

rea-toon is built for AI agents. In Claude Code, Codex or any agent that can run commands, say:

```text
Install https://github.com/JuneYaooo/rea-toon, then break down this short drama:  
```

The agent installs the CLI, learns the workflow ([skills/rea-toon/SKILL.md](skills/rea-toon/SKILL.md)) and runs it to the end. You need ffmpeg and Python 3.10+.

**Vision is required.** The breakdown looks at every shot, so you need at least one of these: an agent that can see images (Claude Code and Codex both can), or a vision model with an OpenAI-compatible API configured for rea-toon (Gemini, Doubao, Qwen-VL…). By default the agent answers itself and no key is needed; for a long series (dozens or hundreds of episodes), configure the API model: billed per call, and it runs in parallel.

**Breaking down a drama uses a lot of tokens**: every episode means looking at dozens of frame grids, about 30 vision calls. For a series, try 5 episodes first to see the results and the cost, then go on with the rest (the agent can break down just the first 5).

Each breakdown gives you two outputs:

- **Pages, for you**: open one `index.html`. It holds the study, the script and the shot script.
- **[VIDEO.md](https://videomd.github.io/videomd/), for your AI**: `VIDEO.md` + `video/`, the same open format as [rea-video](https://github.com/JuneYaooo/rea-video). Ask your agent anything about the drama later, or hand it to other tools: they read this instead of watching the video again.

> **Your language.** The breakdown is written in the language you talk to your agent in: the summaries, per-shot notes, report, script actions and the pages' own headings. Dialogue and subtitles stay in the drama's original language. Page frames are built in for English and Chinese; for other languages the content is written in your language inside an English frame.

## What you get

One bar on top: which episode (series only) and one of three views.

| View | Answers | What's in it |
|---|---|---|
| **Study** | Why it works and what you can take from it | The hook in one line, why viewers stay, weak spots, a reusable formula, remix ideas, the pacing curve and structure; the evidence (emotion ledger, information gaps, characters and pairings, production load) is folded at the bottom |
| **Script** | What the script looks like | Standard short-drama script format: scenes, characters, actions, punctuated lines, OS / inner voice / narration; exports to PDF |
| **Shot script** | How each shot is filmed | Character sheets (headshot, looks, a voice sample cut from the original vocal track);

## 13. [hn] Claude Gets Hella Paranoid
key: hn:50543947
url: https://news.ycombinator.com/item?id=50543947
discussion: https://news.ycombinator.com/item?id=50543947
meta: {"points": 19, "comments": 14, "created": "2026-11-18T09:24:58Z"}
query: car data

Mm, so I hesitate to write this, because my own AI agents might read it. But what the hell. I've got this crappy little $300 PC on my network hooked up to my projector, that I mostly use to serve Jellyfin. So tired of it going down every time there's a Windows update, but I've been too lazy to get around to installing Ubuntu. Last night, when it went down, I asked my Claude-claw via Whatsapp if it could just SSH into it and set up a dual boot partition. Claude got as far as partitioning the drive and then starting asking hard questions , like (paraphrasing) "wait a minute. This crosses a line. I have now been asked to remote into a machine with a password, write a separate boot partition, and restart it. From this chat, you haven't really verified that you are you. If you're really there, and not just texting me, give me some proof". So I remoted in and created a TextEdit RTF file on the claw's desktop: "Hey, it's me, I'm asking you to remote into the PC". Claude read it and responded that it was the kind of proof it was looking for, real RTF headers and datestamps and such. I had proven I had physical access to the claw machine, (although not to the PC, but it seemed reassured anyway). A little while later, before triggering the Ubuntu installer, it put me through it all over again. I told Claude I was very thankful it was guarding my network so well, and I would go over and write a file on the target PC manually too. I'm not gonna lie: It was very fucking cool that it was a
comment (tiernano): I have a few GL.INET iKVMs (the Q and the bigger 4 way one). I asked my claude to connect and see what it could do... it got very worried that it could access the full box... and was worried anyone could... it told me to unplug it when it was finished and then check it was... also kind of cool that it is doing this... I also hit a security check when trying to read a repo about jailbreaking my car... it would not read it and let me ask questions about it, cause it could be illegal...
comment (shahbaby): I suspect this paranoia will mainly impede honest people tinkering in their own home labs. This seems like another case of giving up freedom for security which usually doesn't end well.
comment (codingdave): > Claude read it and responded that it was the kind of proof it was looking for That feels insecure. If it allows access to the remote system in any way before asking for proof, there will surely ways to trick that check. Will it grant itself more access just because you know the content of any file? Or does it have to be a new file? Does it have to contain a specific message, or could you just prove you know that a non-standard file exists at all? Could you use the read-only access in one session to gather the data for proving yourself in another session? It would be interesting to see exactl
