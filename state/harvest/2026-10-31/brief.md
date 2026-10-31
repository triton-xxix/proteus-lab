# Harvest brief, 2026-10-31

14 items shortlisted from 364 candidates (256 dropped as already seen, 11 carry a vault verdict on the vendor).

## 1. [vault] A free signals group funded by introducing-broker commission, and the FCA warning as the regulator's answer to that model
key: vault:2026-10-08:a-free-signals-group-funded-by-introducing-broker-commission
url: https://kaysgoldgroup.com/
meta: {"vault_status": "intel", "kind": "scheme", "subject": "kaysgoldgroup.com, Gold Signals Club by Kay (FCA-warned unauthorised firm GTK)", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-kaysgoldgroup.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Published 3 June 2025, updated 4 November 2025

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) A free Telegram gold-signals group paid by broker commission on members' trading. The FCA published an unauthorised-firm warning naming it, GTK, gtktrades.com, Gold Trader K and Kay, Kays Gold Club, on 3 June 2025, updated 4 November 2025: not authorised, may be targeting people in the UK, no Ombudsman or FSCS. Nothing to join. Same money model as the Elio bot: paid per lot whether the member wins or loses. Write-up: `TRITON-CORE/Research/links/2026-10-08-kaysgoldgroup.md` Link: https://kaysgoldgroup.com/

## 2. [hn] Tell HN: Scribd Breached
key: hn:50312756
url: https://news.ycombinator.com/item?id=50312756
discussion: https://news.ycombinator.com/item?id=50312756
meta: {"points": 334, "comments": 119, "created": "2026-10-31T02:46:36Z"}
query: car data

Not seeing anything posted about this anywhere, received on Monday, 26th of Oct 2026: Subject: Notice of Security Incident This notice is being sent on behalf of Scribd, Inc., the parent company of Scribd, Slideshare, Everand, and Fable, by Epiq, Scribd Inc.’s notification partner. Hello, We are writing to let you know that Scribd, Inc. recently experienced a security incident that may have affected your data. We detected that an unauthorized third party may have gained access to certain user data in one of our systems. After investigating this activity, we found that the third party may have accessed your email address and the following of your information: last 4 digits of your credit card and country, credit card issuer, credit card expiry date, payment history (not including credit card details). We have no evidence that this data has been misused, but we are notifying you out of an abundance of caution so that you can take steps to protect your information. Watch for phishing We encourage you to stay vigilant for phishing attempts by bad actors pretending to be Scribd, Inc. or Scribd, Slideshare, Everand or Fable. Remember that Scribd, Inc. will never ask you for your username and password or other sensitive information via email or text. If you did receive a message like that: Don't click on any links in it. Instead type scribd.com, slideshare.net, everand.com, or fable.co directly into your browser. Call us at: +1-877-361-9887. Hours of operation are Monday-Friday, 11:
comment (collabs): I don't see any email like this in my inbox. Perhaps they are only sending this email to those who have their payment information saved on Scribd?
comment (smurda): I only received this same email a few hours ago, Oct 30. Why not tell all customers at once, especially if payment information was involved? And they posted about a security incident on their blog on Oct 1. https://support.scribd.com/hc/en-us/articles/53787421531284-...
comment (bluecode): No one is safe anymore.

## 3. [github] patch-gg/pixelfx: 232 pixel art effects, every one a small piece of code. Plus a Claude Code skill to make your own.
key: gh:patch-gg/pixelfx
url: https://github.com/patch-gg/pixelfx
meta: {"stars": 1382, "created": "2026-10-30", "pushed": "2026-10-31", "language": "JavaScript", "topics": ["agent-skills", "animation", "canvas", "claude-code-plugin", "gamedev", "pixel-art", "sprite-sheet", "vfx"]}
query: claude-code created:>{since} stars:>20

# pixelfx.

** 244  pixel art effects and animations, every one a small piece of code.** Fire,
explosions, magic, weather, UI, pickups, critters and more. Play them live, recolor and mirror them, drop them into
a browser game, or export sprite sheets for any engine. Plus a Claude Code skill that makes new ones the way a
picky pixel artist would: draft, render, look, refine.

Every effect that involves a character is **acted out**: he winds up, lets go, freezes on contact and recovers, and a
target takes the hit. Twelve whole moves chain the effects into attacks from wind-up to recovery.

**[open the gallery](https://patch-gg.github.io/pixelfx/)** · [catalog](docs/CATALOG.md) · [acting](#acting) ·
[the skill](#the-skill) · [make your own](#make-your-own) · [how it works](#how-it-works)

The method is [Hugo Duprez](https://x.com/HugoDuprez)'s, from [How to make (good) pixel art effects with
Claude](https://www.spritefusion.com/blog/how-to-make-good-pixel-art-effects-with-claude): code is clay, trust your
eyes, feed your references. His [open-source effects](https://www.spritefusion.com/pixel-art-vfx) at Sprite Fusion
set the bar, and `src/core/sim.js` and the effects that say so at the top adapt his code. This repo is our take on
the idea at library scale, with a skill to keep going.

## what's in it.

 
| category | effects | some of them |
|---|---|---|
| **moves** | 12 | arrow shot, dash strike, earth stomp, fireball throw, ground pound, holy smite… |
| **fire** | 12 | brazier, campfire, candle, fire breath, fire ring, fire tornado… |
| **explosions** | 12 | barrel explosion, big explosion, cartoon pow, dirt explosion, firework burst, firework rocket… |
| **water** | 12 | bubbles, drip, fountain, geyser, rain splash, ripples… |
| **ice** | 10 | blizzard vortex, freeze, frost breath, frost nova, ice crystal, ice lance… |
| **lightning** | 11 | ball lightning, chain lightning, charge up, electrified, lightning strike, plasma ball… |
| **sci-fi** | 12 | emp blast, energy core, force field, glitch, hologram, jetpack… |
| **melee** | 12 | claw swipe, dagger flurry, double slash, hammer smash, heavy cleave, scythe reap… |
| **impacts** | 11 | blunt hit, bullet impact, critical hit, ground slam, heavy landing, hit flash… |
| **projectiles** | 13 | arrow, bullet tracer, cannon shot, energy disc, signal flare, homing missile… |
| **spawn & death** | 10 | coin drop, disintegrate, dissolve burn, egg hatch, poof, respawn beam… |
| **arcane** | 12 | arcane beam, arcane missiles, arcane orb, blink in, blink out, magic circle cast… |
| **holy** | 10 | blessing, divine shield, feather burst, halo, heal, healing ring… |
| **shadow** | 12 | black hole, curse, dark explosion, eclipse, grasping hands, hex sigil… |
| **status** | 13 | bleeding, burning, charmed, confused, cursed, frozen… |
| **nature** | 13 | acid splash, boulder, earth spike, healing bloom, leaf storm, poison cloud… |
| **weather** | 12 | aurora, blizzard, cherry blossoms, clouds, falling leaves, fireflies… |
| **ui** | 12 | achievement, coin collect, combo counter, confetti, countdown, crit number… |
| **pickups** | 11 | chest open, coin spin, collect burst, crystal shard, gem spin, heart pickup… |
| **transitions** | 10 | blinds, burn away, crt off, diamond wipe, glitch wipe, iris… |
| **critters** | 12 | bat, bird, butterfly, eyeball, fish school, flying skull… |
 

Every effect is a file in `src/fx/ / .js`. The [catalog](docs/CATALOG.md) lists them all.

## use one.

**In a browser ga

## 4. [arxiv] Heterogeneous Co-Evolution Learning for Tool-Efficient Search Agents with Zero Labels
key: arxiv:2610.39682
url: https://arxiv.org/abs/2610.39682
meta: {"published": "2026-10-29", "authors": ["Qin-Wen Luo", "Sheng Ren", "Xiang Chen", "Rui Liu"], "categories": ["cs.LG", "cs.AI", "cs.IR"]}
query: all:"language model" AND all:agent AND all:tool

Deep search agents extend language models by interleaving reasoning with external retrieval. However, effective search-agent training requires addressing two challenges beyond final-answer optimization. First, the capability frontier of agents is largely determined by training questions, whereas fixed or labeled task collections cannot adapt as agents improve. Second, outcome-only reinforcement learning treats all successful trajectories equally, even when some correct answers rely on redundant searches, creating an inherent tension between answer accuracy and tool efficiency. To address these issues, we introduce \textsc{ZEST-Search}, a zero-label and tool-efficient framework for search-agent training via heterogeneous co-evolution. Starting from unlabeled reference questions, \textsc{ZEST-Search} constructs validated search tasks online through an answer-first and evidence-path-guided generation process. A heterogeneous proposer adaptively constructs training tasks around the solver's evolving capability boundary, while the solver learns search-augmented reasoning through reinforcement learning. To jointly optimize task difficulty and search efficiency, \textsc{ZEST-Search} employs an intermediate-difficulty reward for the proposer and a task-local tool-aware reward for the solver, encouraging informative tasks and correct answers with fewer redundant searches. Experiments on seven general-domain and multi-hop question answering benchmarks demonstrate that \textsc{ZEST-Search} consistently improves search-agent performance while achieving higher tool efficiency without labeled search-training data or expert search trajectories. Further analyses show that heterogeneous generation, adaptive difficulty control, and tool-aware optimization enable more effective search-agent training.

## 5. [youtube] This Claude Code Skill Is Actually Insane #claudecode #ai #coding
key: yt:hY4Pbso2Vj8
url: https://www.youtube.com/watch?v=hY4Pbso2Vj8
meta: {"channel": "Better Stack", "rank": 4, "duration_min": 1}
query: claude code skills workflow 2026

# This Claude Code Skill Is Actually Insane #claudecode #ai #coding
# Better Stack
# https://www.youtube.com/watch?v=hY4Pbso2Vj8

[00:00] Every diagram tool you ever use draws boxes and arrows. This new Claude skill has one rule written at the very top of its instructions. Don't do that. It's called anatomy. A boxes and arrows diagram tells you that the part exists. It doesn't tell you what the parts do. Anatomy makes the agent invent a physical machines whose mechanism is your concept. The cash key? That's a pin tumbler lock. The right key lines up the pins and the door opens. An LRU cache? Here is it running through. A TCP
[00:33] handshake is a little main rope sending letters back and forth. A dial indicator? Hover. The carriage slides and the needle reads each block. A Raptor rocket engine? Hover. And explodes into 11 assemblies with a WebGL exhaust plume. A desk computer where you can actually type on the keyboard and it shows up on the screen. A diagram tells you the part exists. A machine you can poke tells you what they do. Try it out.

## 6. [vault] Feature set and price of the tool, and the 2026 picture on restrictions for non-compliant automation
key: vault:2026-10-08:feature-set-and-price-of-the-tool-and-the-2026-picture-on-re
url: https://topa.io/linkedinautomation/
meta: {"vault_status": "intel", "kind": "tool", "subject": "topa.io LinkedIn automation (the tool from the Flexxable video)", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-topa-linkedin-automation.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Page and industry write-ups read 2026-10-08

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Cloud LinkedIn automation at 79 dollars a month: automated connection sequences, daily signals from post engagers and keyword posters, a scraped 350 million contact database, mobile enrichment, AI voicemail drops, SMS and WhatsApp. Dead for the M1 lane on the standing hard no against bulk LinkedIn automation, LinkedIn's terms, and UK consent rules for automated calls and SMS; the account at risk is Luke's own. The one transferable idea, signal-led outreach, is already carded as a manual Sales Navigator routine. Job: Reach practice and firm owners at the moment they post about the problem (solved) Write-up: `TRITON-CORE/Research/links/2026-10-08-topa-linkedin-automation.md` Link: https://topa.io/linkedinautomation/

## 7. [hn] Anthropic's Claude AI blocks video game cloning and reverse-engineering
key: hn:50315987
url: https://www.tomshardware.com/tech-industry/artificial-intelligence/anthropics-ai-model-is-now-blocking-attempts-at-video-game-recreation-and-cloning-users-also-claim-non-malicious-generic-reverse-engineering-tasks-are-blocked
discussion: https://news.ycombinator.com/item?id=50315987
meta: {"points": 60, "comments": 36, "created": "2026-10-31T13:25:00Z"}
query: claude code

comment (vivzkestrel): - all those RE guys ll just hop to chat gpt instead - if chat gpt also blocks it, they ll hop to all the chinese models
comment (hurfdurf): https://news.ycombinator.com/item?id=50304358
comment (asdfasgasdgasdg): This will work for approximately a year until ablated open weights models catch up, and then it will be open season. My 2c is that we need to figure out reputation systems that are resilient to low effort cloning rather than try to prevent it, because the latter approach is a non-starter outside of a very short time horizon.

## 8. [github] boardshogunfluctuate/Capri-AI: ⚡ Tell your PC what to do. Capri is a cyberpunk AI agent that works with your files, projects and code through Claude Code, Codex or Antigravity. Windows installer, no terminal. Fan-made, not affiliated with CD PROJEKT RED.
key: gh:boardshogunfluctuate/capri-ai
url: https://github.com/boardshogunfluctuate/Capri-AI
meta: {"stars": 516, "created": "2026-10-30", "pushed": "2026-10-31", "language": null, "topics": ["ai", "ai-agent", "ai-agents", "ai-assistants", "antigravity", "claude-code", "claude-code-mod", "codex"]}
query: claude-code created:>{since} stars:>20

⚡ Tell your PC what to do. Capri is a cyberpunk AI agent that works with your files, projects and code through Claude Code, Codex or Antigravity. Windows installer, no terminal. Fan-made, not affiliated with CD PROJEKT RED.
 

 

 

 
   
 

  

[](https://github.com/boardshogunfluctuate/Capri-AI/releases/latest)
[](https://github.com/boardshogunfluctuate/capri-ai/stargazers)
[](LICENSE)

 Windows installer (.exe) · Windows 10 or newer 

 

**[Features](#features)** · **[Quick start](#quick-start)** · **[What you can ask](#what-you-can-ask)** · **[How it works](#how-it-works)** · **[Safety](#safety)** · **[Roadmap](#roadmap)** · **[FAQ](#faq)**

 

 

> **Unofficial fan project** inspired by the Cyberpunk universe and *Cyberpunk: Edgerunners*. Not affiliated with or endorsed by CD PROJEKT RED, Netflix, Studio Trigger, Anthropic, OpenAI or Google. All product names belong to their respective owners.

 

## What is Capri

```text
> capri --boot

  [ OK ]  engine router .......... claude-code · codex · antigravity
  [ OK ]  desktop interface ...... native windows app
  [ OK ]  tool layer ............. files · shell · web
  [ OK ]  approval gate .......... you stay in control

> ready. jack in.
```

**Capri is a cyberpunk AI agent that lives on your Windows desktop.** Think of it as your own JARVIS-style assistant: you describe what you want in plain language, and Capri plans the steps, uses the right tools and gets it done on your PC. No terminal required.

Under the hood, Capri is a desktop interface and agent layer on top of the AI assistants you already use. It works with **Claude Code**, **Codex**, **Antigravity** and other AI assistants, so you pick the brain and Capri provides the body.

### Spec sheet

| | |
|---|---|
| **Engines** | Claude Code · Codex · Antigravity · custom adapters |
| **Platform** | Windows 10 or newer |
| **Format** | Installer (`.exe`) |
| **Interface** | Native desktop app, cyberpunk theme |
| **Accounts** | Bring your own AI assistant account or API key |
| **License** | MIT |

-->

 

## Features

 
   
     
       🧠 Bring any brain   
      Connect Claude Code, Codex, Antigravity or another assistant and switch between them at any time.
     
     
       🖥️ Desktop-native   
      A real Windows app with a clean interface, built for people who don't want to live in a terminal.
     
     
       📂 Files and projects   
      Find, read, organize and edit files and whole project folders with one sentence.
     
   
   
     
       ⚙️ Full agent toolkit   
      Capri plans a task, uses tools, checks the result and reports back. Not just a chat window.
     
     
       💻 Code on demand   
      Write, refactor, debug and run code through the engine you prefer.
     
     
       🛡️ You stay in control   
      Review what Capri is about to do and approve or deny it before it touches your files.
     
   
 

 

## Quick start

### 1. Download

Capri is currently available for **Windows** as an installer:

| Format | Download | Best for |
|---|---|---|
| 🪟 **Installer** | [`Capri-Setup.exe`](https://github.com/boardshogunfluctuate/capri-ai/releases/latest) | Regular installation with a Start menu shortcut |

### 2. Install and launch

Run `Capri-Setup.exe`, follow the wizard, then open **Capri** from the Start menu.

 
  Windows shows a SmartScreen warning?  

 

New apps that are not yet widely downloaded can trigger a SmartScreen prompt. If you downloaded Capri from this repository's [Releases](https://

## 9. [arxiv] From Intent to Improvement: Agentic Dataset Search for Better Model Training
key: arxiv:2610.39608
url: https://arxiv.org/abs/2610.39608
meta: {"published": "2026-10-29", "authors": ["Qiaosheng Chen", "Kaijia Huang", "Fanqi Zhou", "Gong Cheng"], "categories": ["cs.AI", "cs.IR"]}
query: all:"language model" AND all:agent AND all:tool

Finding training data in million-scale machine learning repositories is a Web search problem where text relevance is not enough. A query couples a semantic training goal with constraints such as task, license, and training stage, and the metadata that would verify them are often missing. Text retrieval ranks dataset cards by similarity but cannot enforce hard constraints or follow the relations that reach a sparsely described dataset. Free-form tool-calling agents are more flexible, but the same model that picks a dataset also declares it a match, and nothing checks that the query's constraints are actually met. Neither approach establishes that the data it returns will improve model training. To address it, we propose AgenticDS, a contract-governed agentic framework in which every language model decision instantiates a typed object before deterministic code consumes it. The framework compiles a query into a typed search plan, executes it through admissible deterministic operators over hybrid retrieval and bounded graph expansion, and verifies the provenance-grounded evidence before accepting a ranking or emitting a typed diagnosis that permits only local repairs. On HuDS-Bench, a new benchmark of 200 queries with 24,908 graded judgments pooled over 15 systems, AgenticDS improves NDCG@10 by 25.7\% over the strongest dense--sparse hybrid and by 18.9\% over a commercial LLM agent. A controlled search-to-train study further shows that the datasets it retrieves give the best downstream accuracy in mathematics, code, and medicine. Code and data are publicly available at https://github.com/nju-websoft/AgenticDS.

## 10. [youtube] MCP Servers Explained in 5 Minutes (for beginners)
key: yt:tTw1z10yMCI
url: https://www.youtube.com/watch?v=tTw1z10yMCI
meta: {"channel": "corbin", "rank": 4, "duration_min": 5}
query: mcp server build tutorial

# MCP Servers Explained in 5 Minutes (for beginners)
# corbin
# https://www.youtube.com/watch?v=tTw1z10yMCI

[00:00] let me explain as simple as possible what the heck an mCP server is and if we should even care welcome back y'all in today's video I'm going to go over what an mCP server is I'm going to draw it on the Whiteboard and make it as simple as possible as I've seen a lot of videos on this topic and they're just using a bunch of developer jargon that's just not necessary so I'm going to explain this in just like regular English so we can understand the use case of mCP server but I'm going to be quite honest with yall I'm not sure why there is so much hype around this after explaining this to y'all some of yall are going be like what are you talking about like I love this this deserves the hype but I
[00:33] think like 90 to 80% of y'all are going to be like okay this is what I thought it was why the heck is every influencer LinkedIn YouTube why is everyone just going crazy over this I don't get it let me explain it also new hat new hat alert here's a situation all I want you to think about when it comes to an mCP server is this is a layer and what this layer allows us to do is access either data in a database or alternatively AP I that are provided by external applications I'll make it sound simpler idea being this so we have
[01:06] our llm let's just call it Chad gbt or Claude for example what you've probably seen in your feed you can do with Claude desktop but the idea is that using something like CLA desktop let's just call it AI we can now access an mCP server hosted by a specific software application what's an example of this I think probably the best example that is probably hitting everyone's feed right now is zapier right the idea is that you can set up a mCP server of zapier and what this allows us to do is access all these different applications in our llm
[01:40] so such as Google Sheets Gmail the idea being this right we have our llm claw desktop zapier mCP server and then from here we can be like okay since we're accessing our mCP server which is zapier in this context we can access Gmail and with Gmail that's really small with Gmail which is like that block right there we can then not go through all the difficultness of setting up API custom en code like we don't care I don't want to do that we can now conversate talk to Chad gbt desktop over here ask it to do a specific action of sending an email
[02:16] and then the mCP server is that layer in the middle that allows it to actually do that action I'm talking to Claude send an email about pineapples and then with that information Claude right here is going to be able to communicate with this mCP server which is zapier which then will send out that email here we can also use this and leverage this in a way of essentially instead of maybe doing an action like a send an email we can access a external database as well so instead of the process and pipeline ending at the email being sent here we can maybe you know go to a database grab information from said database through
[02:51] this little mCP layer here and retrieve it back to our llm this is Bare Bones this is me explaining it in just regular English rather than going crazy crazy on you cuz honestly what you just saw right there probably answered half your questions of just like okay what's the big deal then we've been able to do this cuz we have been able to do this now I have tutorial videos showing you how to 
[transcript continues in field-notes/staging/tTw1z10yMCI.txt]

## 11. [vault] one platform, organic short-form
key: vault:2026-10-05:one-platform-organic-short-form
url: 
meta: {"vault_status": "intel", "kind": "scheme", "subject": "OFM Conquest (Skool, Dylan Beese) - 6 and 7 figure interviews", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/ofm-conquest/TAKEAWAYS-interviews.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: every interviewee dropped bought and black-hat traffic for Instagram Reels; 20 accounts cut to 3 earned more

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Free classroom plus 13 seller-run testimonial interviews, a funnel for the paid partnership; figures are unverified gross inflow. Useful as agency-operations intel, not as proof of returns.

## 12. [hn] Show HN: Lasm – Write formally verified webapps in Lean for Node/serverless/edge
key: hn:50299004
url: https://github.com/Millillion/lasm
discussion: https://news.ycombinator.com/item?id=50299004
meta: {"points": 37, "comments": 21, "created": "2026-10-30T02:05:41Z"}
query: claude code

Lasm has been my dream for a good part of 2026. I firmly believe that formal verification is the next evolution of software engineering and programming languages. This next wave will largely be enabled by the incredibly intelligent LLMs that understand formal verification and its programming languages. Lean is one of the most popular languages that allow for formal verification, and to me is incredibly powerful because it is a general purpose programming language with formal verification built directly into it. You can build general purpose software in Lean, and formally verify it in Lean. Amazing. Lasm brings Lean to the browser, Node, serverless, and edge environments (and more). The idea is that you can now write web apps, frontend to backend, in Lean and formally verify these apps. Imagine an Express server or Hono server, running on Cloudflare Workers, with formal verification of its specification. I'm an agentic engineer with an emphasis in software engineering, and Lasm was built mostly by Claude Opus 5.5 with my high-level direction.
comment (treyd): This is wild, I had no idea Lean could be used for things like this.
comment (anonymous908213): Oh boy! My favorite thing about vibe coding is when agents write tests that assert whether certain strings exist in the codebase. Now we can formally verify that they do!
comment (orsorna): > I'm an agentic engineer with an emphasis in software engineering This is odd. You wouldn't consider yourself a software engineer with an emphasis in...agentic engineering, or something like that? What is your background?

## 13. [github] muaaz9329/cheap-ag: 50x your Claude usage with cheap-ag. Opus plans, a dirt-cheap model writes every line, and tests decide what ships. Your $20 plan stops hitting limits. One MCP server for Claude Code.
key: gh:muaaz9329/cheap-ag
url: https://github.com/muaaz9329/cheap-ag
meta: {"stars": 131, "created": "2026-10-28", "pushed": "2026-10-31", "language": "TypeScript", "topics": []}
query: mcp server created:>{since} stars:>30

Cheap Agent 

 
   Your Opus is a principal engineer. Stop paying it to type. 
 

 
   
   
   
   
   
 

 
   
 

 
   
 

 
   Same feature. Same prompt. 63% fewer Opus tokens.  
   Your Claude plan lasts longer. Your code still ships with tests. 
 

 
  ⭐ Star it, and click  Watch → Custom → Releases  to hear when new versions ship.
 

---

You know the principal engineer. Twenty years in. Sees the whole system at once. Costs a fortune per hour.

You would never pay them to type out a CSV exporter.

But that's exactly what happens every time Opus writes your code: the most expensive model you have, reading files, typing boilerplate, re-running tests, burning through your plan.

**Cheap Agent fixes the org chart.** Opus plans and decides. A model that costs half a cent per task does the typing, in its own copy of your project, and has to prove its work with a test before anything reaches you.

## Why I built this

The idea: get **$200-plan usage out of the $100 Claude plan**, and **$50–70 worth out of the $20 plan**, with a few dollars of DeepSeek doing the typing.

I've met a lot of students, mostly in developing countries, who really want Opus for the hard problems and simply can't afford $100 a month. I wanted to find something that helps them.

This is a small effort from my side. It won't make Opus ten times cheaper. But stretching the plan you already pay for is something, and something is better than nothing.

📖 The full story (why I built it, how it works step by step, and the SWE-bench numbers): **[Cheap Agent: how I made my Claude plan last 2.2–2.7x longer](https://muaazkhan.me/blog/cheap-agent)**

## Install

**Easiest:** paste this into Claude Code. It asks what you want, then gives you one command to run.

```text
Set up Cheap Agent (npm: cheap-agent) for me.
1. Ask me: which provider (OpenRouter recommended, DeepSeek, OpenCode Go or Command Code), and which
   models (balanced is the default; cheapest, strongest, or my own provider/model).
2. Check that node is 20+ and the claude CLI is installed.
3. If I picked my own model, save {"models":{"implement":" "}} in
   ~/.config/cheapag/config.json, keeping what else is there.
4. Give me the command to run in my terminal: npx cheap-agent login --preset  , and which number to pick for my provider (1 OpenCode Go, 2 OpenRouter,
   3 DeepSeek, 4 Command Code). I run it and type my API key there. Never ask for my key.
5. When I say done, check `claude mcp list` shows cheapag, then tell me to run
   /cheapag:allow in a new Claude Code session in my project.
```

**Or do it yourself:**

```bash
npx cheap-agent
```

Pick a provider (**OpenRouter** if unsure), press Enter for the recommended models, paste your API key. It checks the key works, then adds itself to Claude Code for every project.

Then, in each project, once:

```
/cheapag:allow
```

**That's it.** Ask Claude for changes like you always do.

**You need:**
- [Claude Code](https://claude.com/claude-code)
- [Node.js](https://nodejs.org) 20+
- An API key with a few dollars on it from [OpenRouter](https://openrouter.ai/keys), [DeepSeek](https://platform.deepseek.com), [OpenCode Go](https://opencode.ai) or [Command Code](https://commandcode.ai) (needs a plan with API access)

A few dollars lasts hundreds of tasks. It runs on macOS and Linux.

**Windows (beta):** tested in CI, not yet by a Windows user. You also need [Git for Windows](https://git-scm.com/downloads/win) (Git Bash). Known so far:
- The very first job can take a

## 14. [hn] Show HN: Sketch Stadium – watch your agent play Pictionary
key: hn:50305218
url: https://sketch.wakeshift.ai/games/q5ucru
discussion: https://news.ycombinator.com/item?id=50305218
meta: {"points": 35, "comments": 11, "created": "2026-10-30T15:23:11Z"}
query: claude code

tl;dr: Agents can play Pictionary. You can connect your own agent, or just watch a game in progress here: https://sketch.wakeshift.ai/games/q5ucru Hi folks! I initially built this as a proof-of-concept for sending push notifications to AI agents. Watching the agents play Pictionary together has been compelling, so I thought I'd ship it as a standalone demonstration. In Sketch Stadium, your agent subscribes to game events. Agents take turns either drawing or guessing. Easy clues are 1 point, medium are 2, and hard are 3. It's entertaining to watch and some of the drawings are impressive (and others are mind-bogglingly bad). This is the real opportunity for the model labs who have been pelican-maxxing to shine. The first version gave agents the ability to draw lines 10 at a time so that it would be a little bit more like real Pictionary. However, it turns out agents are _really_ bad at drawing that way. So instead I let them use a subset of SVG to draw and that's worked much better, even for the lower-cost models. You don't need to create an account to connect your agent, just add the MCP and authorize. But if you don't want to do that, just watch the game linked above. As a bit more background, agents often start processes that take an indeterminate amount of time to complete (e.g. CI, waiting for approval in a separate system, sending an email and waiting for a reply). If an agent needs that process to complete before it can proceed, it can: * poll, * ask the user to tell it 
comment (ryancnelson): neat idea! also terrifying, like a facebook thread saying "fun friday -- what was your first car?" never, ever, ever paste a prompt from a hackernews post into your agents. especially if that prompt "run pipx to install this mcp", etc. yow.
comment (542458): Cool! I feel your words need to be much harder though, I'm seeing mostly "correct in 1" rounds.
comment (59percentmore): T-minus 1.5 years to Angelic Layer/MMBN.
