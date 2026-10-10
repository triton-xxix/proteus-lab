# Harvest brief, 2026-10-10

14 items shortlisted from 243 candidates (111 dropped as already seen, 19 carry a vault verdict on the vendor).

## 1. [vault] UK shape of selling booking software through trade job software and profile booking buttons
key: vault:2026-09-20:uk-shape-of-selling-booking-software-through-trade-job-softw
url: https://www.youtube.com/watch?v=mr4YV-9MY0Q
meta: {"vault_status": "open", "kind": "company", "subject": "Avenue (avenue2.au) booking widget, the Starter Story \"$50K a month\" video", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-avenue-widget-starter-story.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Unknown which job software UK trades run; ServiceM8 and SimPro are not it; Reserve with Google needs partner approval

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (company) Identified (Tom Holliday, Brisbane, four people, two years). The revenue figure is the founder's word only. What transfers is the distribution, a booking button on the Google Business Profile sold by phone alongside the trade's job software, not the widget itself. UK integrations unknown. A UK-shape study was offered and not started. Job: Sell recurring booking software to trades through the software and profiles they already use (still open) Write-up: `TRITON-CORE/Research/links/2026-09-20-avenue-widget-starter-story.md` Link: https://www.youtube.com/watch?v=mr4YV-9MY0Q

## 2. [hn] `123456' password used in Danish CPR data breach
key: hn:50031269
url: https://cphpost.dk/2026-10-10/news/round-up/123456-password-used-in-massive-danish-cpr-data-breach/
discussion: https://news.ycombinator.com/item?id=50031269
meta: {"points": 369, "comments": 191, "created": "2026-10-10T09:51:49Z"}
query: car data

comment (imdsm): not ideal
comment (donalhunt): In Denmark, a CPR number (short for Det Centrale Personregister, or Central Person Register) is a unique 10-digit personal identification and social security number assigned to every resident and citizen. Equivalent to social security information in the US I guess.
comment (INTPenis): I love getting to the root cause of these incidents. Hate it when they just move on with no post mortem, the rest of us are trying to learn here! Like the recent ransomware attack on a Swedish Svedala municipality, still no root cause published on that?

## 3. [github] wheresryan22/anatomy: A Claude Code skill that turns a technical idea into a detailed, interactive isometric figure of a real machine. It makes SVG with optional WebGL shaders and 3D, for docs, articles and landing pages.
key: gh:wheresryan22/anatomy
url: https://github.com/wheresryan22/anatomy
meta: {"stars": 226, "created": "2026-10-08", "pushed": "2026-10-10", "language": "JavaScript", "topics": []}
query: claude-code created:>{since} stars:>20

Anatomy 

  A Claude skill that explains an idea by building it as a real, working object.  Crafted, interactive isometric figures with many small precise parts, in SVG, WebGL and 3D. 

 
     
     
     
     
     
     
 

 
     
  &nbsp;
     
  &nbsp;
     
 

 
   Quick start  ·
   Gallery  ·
   What it makes  ·
   Install  ·
   Usage  ·
   Examples  ·
   How it works  ·
   Limits 
 

 
   
 

   examples/raptor-engine , light theme, firing. The engine and stand are SVG; the plume is a WebGL shader in the same isometric camera.  

---

Ask Claude for a figure that explains a technical idea, and Anatomy has it invent a physical thing whose working *is* the concept. A cache key that skips work when nothing changed becomes a pin-tumbler lock that only turns when every pin matches. One GPU context serving many canvases becomes a gantry plotter whose single print head visits 16 wells.

Then Claude builds that thing out of dozens of small, solid, shaded parts, puts it in a framed card with a title, a hint and a live readout, makes it move calmly under the pointer and the keyboard, and checks its own work by zooming in on every joint. Every number the figure shows comes from the same small model that moves its parts.

## Quick start

```sh
npx skills add wheresryan22/anatomy -g -a claude-code
```

Then, in Claude Code:

```text
/anatomy explain how a token bucket rate limiter works, interactive
```

That's it. No API keys and nothing to `npm install`: the kit uses only Node's built-in modules.

## Gallery

 
   
       
       
   
   
       raptor-engine : hover to take it apart into 11 assemblies. An audit proves that no pipe passes through anything, at rest, apart and in every frame between.  
       ripple-tank : SVG apparatus over two WebGL layers (lamp light and caustics on the paper, reflections in the water) driven by a dispersion and optics model.  
   
   
       
       
   
   
       turning-dial : the 3D mode (beta). About 90 parts are re-projected and re-shaded every frame as you drag the dial.  
       dial-indicator : the smallest example, about 300 lines. Hover to slide the carriage; the needle reads each block.  
   
 

Every screenshot is the light theme of a page in [`examples/`](examples), captured with the skill's own [`scripts/capture.mjs`](scripts/capture.mjs) and [`scripts/drive.mjs`](scripts/drive.mjs). The built pages are committed: open any `.html` in `examples/` to try it.

## What it makes

Three kinds of figure. All three share one kit, one camera and one set of craft rules.

| Kind | What it is | Example |
|---|---|---|
| **SVG** | The core. Solid isometric parts with four-tone shading, painted back to front, in a card with a live readout and eased motion. It ships as a standalone HTML page, a lone `.svg` file with its styles embedded, or React/Next.js components. | `dial-indicator`, `desk-computer`, `arcade-cabinet`, `test-rig` |
| **SVG + WebGL** | For what lines can't draw: fire, exhaust, water, caustics, lamp light, glow, steam. The shader runs in a canvas between a back and a front SVG, in the figure's own isometric camera, so it sits inside the drawing. The SVG still reads without WebGL. | `raptor-engine`, `ripple-tank` |
| **3D**  beta  | Parts that turn in true 3D: a dial or turntable that spins, fingers that flex, a piece that breaks off and falls. The moving parts are re-projected and re-shaded by the kit's own rules every frame; the rest of the figure stays static art. | `turning-dial` |

Ea

## 4. [arxiv] SuperNav: An Agentic Navigation System for Any Task in Any Scene
key: arxiv:2610.12126
url: https://arxiv.org/abs/2610.12126
meta: {"published": "2026-10-08", "authors": ["Jinkai Zhang", "Jingyi Xu", "Yuanhong Yu", "Jiarui Guo"], "categories": ["cs.RO", "cs.CV"]}
query: all:"language model" AND all:agent AND all:tool

General-purpose service robots need navigation systems that can handle diverse human requests in unfamiliar environments, combining task generality with scene generality. Some existing methods fine-tune multimodal large language models (MLLMs) to predict navigation actions, making their behavior dependent on the coverage of navigation training data and potentially limiting generalization to new requests and environments. Our key insight is to let the MLLM focus on interpreting requests, understanding scenes, and making decisions while preserving its general-purpose capabilities and delegating motion execution to navigation tools. To realize this idea, we introduce SuperNav, which equips a pretrained MLLM with a specialized agent harness without navigation-specific fine-tuning of the MLLM. Our harness supports these decisions with Navigation Skills, agent-oriented Tools for physical interaction, and task-progress and context management. A unified visual-point interface connects decision-making to motion by allowing the model to specify destinations directly in images and revise its decisions from execution feedback. Together, these components support sustained navigation across different task requirements and environments. SuperNav outperforms four evaluated baselines on instance-level, multi-object, and demand-driven tasks. Category-level evaluation on HM3D and deployment on a real quadruped robot further demonstrate its applicability across environments. Project Page: https://zju3dv.github.io/SuperNav/

## 5. [youtube] Code Demo - Web-scraping with API's
key: yt:H-6gyxVGj6A
url: https://www.youtube.com/watch?v=H-6gyxVGj6A
meta: {"channel": "UK DATA SERVICE", "rank": 2, "duration_min": 43}
query: open data uk api project

# Code Demo - Web-scraping with API's
# UK DATA SERVICE
# https://www.youtube.com/watch?v=H-6gyxVGj6A

[00:08] okay everyone apologies um I think I should be okay hooray that means the wall clock and the echo all gone I'm assuming so apologies hopefully of some sympathy for homeworking I've been turfed out of the room I usually work in for family reasons uh my daughter needs more space than me the wall clock was fine okay let's get up and running what we're
[00:43] going to do is run through demonstration of collecting police data for England Wales and Northern Ireland and again Julia we'll keep an eye on the questions and the chat fantastic and the link as well to the code we're using today and if you'd like to follow along and Julia should be able to post that into the chat and I think she's doing that right now I won't waste any more time let's get stuck in to collecting data so this lesson today is about getting data from
[01:21] api's and so we're going to take a look at using Python for downloading data from the web I'm also just going to try and cultivate your computational thinking skills as well and through some coding examples and so how do you define and solve a computational method a data collection problem and using computational methods it's might a bit more legible and so we're not going to assume any previous knowledge of Python and are collecting data from the web and
[01:55] it would have been useful if you've participated in the first two sessions but it's not a requirement I'll talk you through everything and we're doing we're using police data so it's social science data but if you're from a different background from the private sector that's totally fine as well the techniques you're going to learn apply much more broadly yeah and we're going to look at what an API actually is and understand the kind of key steps and requirements for going about collecting data from an API and being able to use Python for this particular task
[02:30] so hopefully you get quite a lot out of today's session so this is a Jupiter notebook some of you will be familiar with it now so it mixes live Python code with some narrative like you're seeing here and and the results of the code as well so if you're following along with us just now and basically you just have to run or execute the cells that are marked by this i n square bracket symbol and it'll be up here and on the left so for example this is a piece of Python code
[03:08] and it's a very simple piece some of you will have probably seen it before a there may be a little bit of a lag in terms of accessing the notebook just because if you're all accessing it and at the same time yeah it so if it's not running right now so sometimes like the notebook might need to be reloaded okay
[03:43] never mind and thankfully I have a version on my machine it's just because I think we're all accessing it at the same time so let's give a quick demonstration of using Python code there we go it asks for my name yeah and enjoy more about getting some data from the web so very quickly what an API is so it's short for an application programming interface there's a formal definition which is probably not terribly unhelpful how I understand that is it's an
[04:19] intermediary between software you know applications so in much the same way that a translator sits between in individuals who wish to communicate with each other and so what you might have an English speaker and you might have an Italian speak
[transcript continues in field-notes/staging/H-6gyxVGj6A.txt]

## 6. [awesome] automatis-tools/agents-can-communicate (new in awesome-claude-code)
key: gh:automatis-tools/agents-can-communicate
url: https://github.com/automatis-tools/agents-can-communicate
meta: {"list": "awesome-claude-code", "stars": 129, "created": "2026-08-15", "language": "JavaScript", "description": "Messages between AI coding sessions in different vendors' clients, such as Claude Code and Codex. Local, open source, no lead agent."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Agents Can Communicate (ACC)

**The message your clients can’t send each other.**

Claude Code can message your other Claude Code sessions, and Codex can queue a message for
another Codex session. Neither client offers a way to message the other’s sessions. ACC
carries questions, reviews and handoffs between sessions in different vendors’ clients, on
your machine.

You open each client normally and choose its work. Every session keeps its own model,
conversation, and permissions. Coordination runs locally, with no lead agent managing the
others. If all your sessions run in one of these two clients, try its own messaging first.

```mermaid
flowchart TB
    you["You choose the tools and work"]
    codex["Codex Feature A"]
    claude["Claude Code Feature B"]
    antigravity["Antigravity CLI Feature C"]
    acc["Communication via ACC"]

    you -.-> codex
    you -.-> claude
    you -.-> antigravity
    codex   acc
    claude   acc
    antigravity   acc

    subgraph handoff["When you switch clients"]
        direction LR
        current["Claude Code session"] --> saved["Handoff Done · Decisions Next steps"]
        saved --> next["Codex session"]
    end
    acc ~~~ handoff

    classDef human fill:#f1f5f9,stroke:#8593a3,color:#202a35
    classDef session fill:#fff,stroke:#ced4d9,color:#202a35
    classDef shared fill:#e8edff,stroke:#385cde,color:#202a35
    class you human
    class codex,claude,antigravity,current,next session
    class acc,saved shared
    style handoff fill:transparent,stroke:#ced4d9
    linkStyle 3,4,5,6,7 stroke:#385cde,stroke-width:2px
```

## When ACC helps

- **Get a second opinion from another vendor’s model.** Ask a Codex session to review a change
  your Claude Code session just made, and send its findings back to the session that wrote the
  code.
- **Bring parallel features together.** Let sessions in different clients ask each other about
  a shared API before they build around different assumptions.
- **Switch clients mid-feature.** When a limit approaches or another model suits the work
  better, leave a handoff with decisions and unfinished work for a session in the client you
  open next.

## Try one review across clients

You’ll need **macOS, Linux or Windows 10/11, Node.js 24 or newer**, and supported coding
clients on the same machine and operating-system user. On Windows, ACC runs natively, with no
WSL, and live delivery reaches Claude Code, Codex and Antigravity CLI there too. See
[Windows](docs/GETTING_STARTED.md#windows).

```bash
npm install -g agents-can-communicate
acc install
```

The installer connects supported clients it finds. Follow its activation instructions, review
any required hook or plugin trust, then restart your clients from the project directory. The
[setup guide](docs/GETTING_STARTED.md) covers client-specific steps.

Open Claude Code and Codex in the same project. After Claude Code has changed something, for
example an account-registration form, ask it:

```text
Ask the Codex session in ACC to review the registration form change
you just made. Name the files and what it should check.
```

Then ask Codex:

```text
Answer the review request in ACC. Read the files it names, check
what it asks, and reply with what you found.
```

Codex should find the request without you pasting it, and Claude Code should see the findings
at its next turn without you copying them back. The sender can check whether its message was
delivered and answered.

## Client support

Integrations are availa

## 7. [vault] Templates, thumbnails, overlays and pre-launch guides sold or published to creators before a big game launch
key: vault:2026-09-20:templates-thumbnails-overlays-and-pre-launch-guides-sold-or-
url: 
meta: {"vault_status": "open", "kind": "idea", "subject": "GTA 6 \"four ways to earn\" carousel (_vorken_)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (sections 1 to 3)", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Fastest lane with no publisher IP exposure; guides and search sites need three to six months so the window is short

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Premise false. The game is not out until 19 Nov 2026, consoles only, no PC version and no mod SDK, so every listed earner needs something that does not exist. The only real angle is content and search positioning in the weeks before launch. Job: Earn from a huge game launch without breaching the publisher's terms (still open)

## 8. [hn] Can you use autoregressive diffusion to generate market data?
key: hn:50021410
url: https://blog.janestreet.com/can-you-use-autoregressive-diffusion-to-generate-market-data/
discussion: https://news.ycombinator.com/item?id=50021410
meta: {"points": 176, "comments": 55, "created": "2026-10-09T14:56:13Z"}
query: car data

page: Jane Street Blog - Can you use autoregressive diffusion to generate market data? Can you use autoregressive diffusion to generate market data? Sep 30, 2026 | 9 min read Share on Facebook Share on Twitter Share on LinkedIn By: James Somers The following is part of a series of posts about 2026 summer intern projects – for more, see “What the interns have wrought, special jumbo 2026 edition” In quantitative finance we are used to models that take a stream of market data events for a given symbol (like resting orders being added to an order book, cancellations of those orders, executions) and predict that symbol’s future price. Generative models are less common. Imagine a model that could give not just a point estimate of a symbol’s price, but could actually synthesize book events—including the timing of their arrival on the exchange. You’d get price predictions, of course, but your rollouts would have hugely more texture than just that. But what kind of data is market data? A generative model demands an answer to that question. Is it more like video, or text? That is, is it continuous or discrete? Market data seems to have features of both. An order book evolves via a series of turns as market participants put on, or take away, resting orders; there is no doubt a discrete action space. And yet, many of the most important parameters of a given order, like its price, have such a high cardinality that they basically appear continuous. Some simply are continuous: an easy one to overlook, but crucial for a generative model, is timing, as in “when does the new order arrive at the exchange.” Even that oversimplifies things. In practice the distributions are spiky: “pennying” (where you improve upon a price by one tick) is much more common than improving by two ticks, and orders tend to arrive in bursts, for instance around whole-number times. One way to explore these complications is to treat your data as if it’s continuous and see how that breaks down. This summer, a researc
comment (TheOtherHobbes): "Past performance is not indicative of future results."
comment (reedf1): No
comment (dzink): The market has modes and reverts behavior when it switches them. Thus happy bouncy becomes hammered stammered. The prediction models fall hook and sinker for that.

## 9. [github] Autumn1337/better-statusline: A status line for Claude Code: the session's figures as dot-matrix rings, and the music you are playing beside them
key: gh:autumn1337/better-statusline
url: https://github.com/Autumn1337/better-statusline
meta: {"stars": 182, "created": "2026-10-05", "pushed": "2026-10-07", "language": "TypeScript", "topics": []}
query: claude-code created:>{since} stars:>20

better-statusline 

 
  A status line for  Claude Code , drawn above the prompt: 
  the session's figures as dot-matrix rings, and the music you are playing beside them.
 

 
   
   
   
 

 
   The film  ·
   What it shows  ·
   Install  ·
   Options 
 

## The film

 
   
 

 
   
    Fifty-two seconds. All of it is drawn in code: the picture, the two covers and the score. 
    With sound:
     1080p  ·
     4K 
   
 

## What it shows

### Drawn in dots

 
   
   
 

A braille cell is eight dots. Every drawing here is made of them: a ring is a true circle, found on the screen and snapped dot by dot to the terminal's grid.

### Rings

 
   
   
 
 
   
   
 

Each ring is lit clockwise from its top, with its figure at its heart.

- **Context**: how full the window is.
- **Cache**: the minutes left before the prompt cache goes cold, counted from the last response. An hour on a subscription inside its limits, five minutes otherwise.
- **5-hour and weekly**: how much of each limit is spent, and when it starts over. The arc turns yellow once you spend faster than the window passes.

Above them, a header names the model and its effort, the folder, the git branch with its staged and modified files, the lines the session added and removed, and the subagents at work.

### Spend

 
   
 

One bar for each recent turn, beside the session's total. The bars grow by the square root of the cost, so one dear turn leaves the rest standing.

### Music

 
   
   
 

On macOS a card shows what Spotify or Apple Music is playing, in an accent read out of the cover. It takes the mouse: play, pause, skip, seek along the line, shuffle, repeat, and the volume at the right end of the controls.

### The band

 
   
   
 

`/fold` folds the whole band into one row, and opens it again. The colours are Claude Code's own theme, so the band follows it from dark to light.

## Requirements

| For | You need |
| --- | --- |
| The status | Claude Code 2.1.289 or later, and `git` |
| The music card | macOS with Spotify or Apple Music |
| Cover pictures | kitty 0.28 or later, or Ghostty; not through tmux, screen or ssh |
| Rings that are round at your font size | `python3`, and a terminal that reports its pixel size |
| Nerd Font icons | Ghostty, kitty or WezTerm, or your own Nerd Font |

Each missing piece takes only its own part away: without a player the band is the status alone, without pictures the card has no cover, without a Nerd Font the icons are plain Unicode.

The plugin is built on Claude Code's function hooks, an early-access API that still changes between releases. It is developed on macOS in Ghostty. The other terminals are handled by what each one reports, and are untested.

## Install

From the marketplace this repository carries:

```sh
claude plugin marketplace add Autumn1337/better-statusline
claude plugin install better-statusline@better-statusline
```

To take a new version later:

```sh
claude plugin marketplace update better-statusline
claude plugin update better-statusline@better-statusline
```

Or install from npm and load it for one session:

```sh
npm install -g better-statusline
claude --plugin-dir "$(npm root -g)/better-statusline"
```

To update the npm installation, run `npm install -g better-statusline@latest`.

To load from a clone for one session:

```sh
git clone https://github.com/Autumn1337/better-statusline
claude --plugin-dir ./better-statusline
```

To load a clone in every session, name its parent folder in `CLAUDE_CODE_PLUGIN_DIR

## 10. [arxiv] Forms of LLM-Integrated Applications from LLM-Chats to Autonomous AI Agent System
key: arxiv:2610.11899
url: https://arxiv.org/abs/2610.11899
meta: {"published": "2026-10-08", "authors": ["Irene Weber"], "categories": ["cs.CL", "cs.AI", "cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

Large language models (LLMs) are increasingly embedded as components in software systems, marketed under labels such as chatbot, copilot, retrieval-augmented generation, workflow, coding agent and AI agent. Whether these labels denote genuine architectural forms or serve as branding has not been assessed systematically. In the sources surveyed, labels do carry architectural content, most clearly in vendor usage: copilot denotes a router-worker architecture operating a host application under step-by-step user confirmation, while the more recent shift to the label agent coincides with AI-planned multi-step execution of which the user sees only the outcome. The coding agents of four major providers share one architecture, a reason-and-act loop delegating to subagents. This survey describes seven recurring forms---LLM chats, custom agents, retrieval-augmented generation (RAG), AI-enhanced workflows, copilots, coding agents, and, in part, agentic RAG---in a common vocabulary of agents and tools. Each is characterized along four structural dimensions (agentic RAG only partially): the architectural pattern, the control of execution and the point of user intervention, the number of agent calls per task, and tool use. An illustrative corpus of 22 systems from research publications and vendor documentation grounds the descriptions and shows where they reach their limit.

## 11. [youtube] Tutorial 2: Understanding the UK Data Service Open Data API
key: yt:P5cwP-HK8uI
url: https://www.youtube.com/watch?v=P5cwP-HK8uI
meta: {"channel": "AppChallenge", "rank": 3, "duration_min": 5}
query: open data uk api project

# Tutorial 2: Understanding the UK Data Service Open Data API
# AppChallenge
# https://www.youtube.com/watch?v=P5cwP-HK8uI

[00:03] so we're in the documentation now and this is basically what you can call about the data you can download the entire dataset if you want to do no complex statistics stuff like that and if you just need some bits of it for a nap and you don't want you don't want to run your own data server stuff like that now you can just use this one and it will tell you some stuff about the data that's available so we'll start at the top we'll see which data sets are available so actually we can just put in
[00:40] the key here and we have to ask for open data sets so in the future if there's more than just the European quality of life survey that's where as it will tell us it will kind of you know if we as the UK data service add more this will this will give us on information yeah that's that's where it'll up here so we can see we've got a response from the from the system which says yeah with a list of data sets which contains one data set which is the EQ LS and nothing went
[01:15] wrong with which is also nice so we know we have the EQ or less in there so we can then go down and retreat some information about about the data set for example which keywords on there which topics I on there which varies I'm there so the relation between these is that variables are the questions that people get asked like how many children do you have and so that's in the end what you want but since the data set has I think
[01:52] 196 variables I think I'm something like that they are grouped by topics and keywords and bearable groups so you can get an easier overview so you don't have to look at all 196 at the same time you can just go okay maybe let's just look at the topics for this data set then the key and then we say qls in the know give us a list of topics so we have stuff about education social
[02:27] stratification environment health housing transport politics all stuff that may be interesting to you depending on the app that you want to build and if you wanted to see what's in a topic maybe let's look at stuff that has to do with political behavior may be that that might be interesting so we'll go to topic variables we put the key and we'll say e qls then we have that's topic 15
[03:06] and they'll send a request and we'll get okay what's all in there I may get all the variables that are in the topic very words can be quite detailed so this is a long list this is also I didn't immediately request all the available variables because that's that's a huge thing that you have to scroll through so I think for for small app it's better to start by requesting the topics or requesting keywords and then you know drilling down to the variables that are actually in there instead of requesting
[03:40] the whole thing and having to do with that I think it's it's you will get to your results quicker if you just use this drill down approach anyway what for every request that you do when you're requesting something it'll give you d rho l which is this which you can then use in your app for example this is they give it in co format which is Collison it's a command line application that download stuff from the internet
[04:12] basically so I could just open the terminal if you're if you're on a Mac or Linux you probably have one available let's do that so I can take this sorry put it in the end yeah well it'll just download that and give me the 
[transcript continues in field-notes/staging/P5cwP-HK8uI.txt]

## 12. [awesome] bill10/agent-007 (new in awesome-claude-code)
key: gh:bill10/agent-007
url: https://github.com/bill10/agent-007
meta: {"list": "awesome-claude-code", "stars": 4, "created": "2026-03-31", "language": "JavaScript", "description": "From web terminals for your coding agents to a self-running agent company: Claude Code and Codex in parallel git worktrees, a job board they pick work from, and one agent that runs the board from a goal."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Agent 007

[](https://github.com/bill10/agent-007/actions/workflows/test-ubuntu.yml)
[](https://github.com/bill10/agent-007/actions/workflows/test-windows.yml)

**Manage your coding agents by talking to them, from your phone.**

The operations layer for Claude Code and Codex: agents take work from a board, one manager agent reviews and merges what they ship, and you hear about it on a call.

   

*A Talk to Billion call, from the request to the merged PR: [watch the 38s video with sound](https://github.com/bill10/agent-007/releases/download/v0.54.1.0/phone-call.mp4). Scripted demo with stand-in agents, sped up; voices are text-to-speech (`scripts/demo/phone-call.mjs`).*

- **A job board your agents work from.** Each card gets its own git worktree, a Claude Code or Codex worker and a real terminal you can type into, and ends as a pull request (or a summary, for work that isn't code).
- **One manager agent, Billion.** Give it a goal: it posts the cards, reviews the diffs, merges the PRs, and brings you only what needs a person (money, access, security, anything irreversible) in a briefing twice a day.
- **Agents that find the right skill.** Claude Code fits every installed skill's description into about 1% of its context window; past a hundred or so skills most show as a bare name and get missed. Agent 007 groups them into [skill families](#skill-families-every-agent-sees-a-short-index-and-a-card-picks-what-it-needs): its agents see one line per family, and each card lists in full the families its job needs.
- **Talk to it from your phone.** Open it in your phone's browser over Tailscale (`agent007 install --remote`), tap Talk to Billion, and hear progress spoken back. One command installs it as a service; Settings has an Update button, with a What's new window listing the changes first.

### The Billion tab

*Recorded from the running app, with stand-in agents so the run is repeatable (`scripts/demo/record.mjs`) -- [full 43s video](https://github.com/bill10/agent-007/releases/download/v0.29.0.0/billion-demo.mp4). If the capture does not load, there is a [still screenshot](docs/screenshot.png).*

From web terminals for your coding agents to a self-running agent company. Use it as far along as you need:

1. **One task: one agent in a web terminal.** Start Claude Code, Codex or any CLI agent in the browser. Add a repo once; every agent gets its own git worktree and branch, so you never set one up by hand.
2. **Many tasks across projects: many terminals, one window.** Every repo and every agent in one place, with live terminals, a file explorer, inline diffs, and a pixel office where each agent faces its screen while it works and turns to you when it needs you.

   
3. **Stop watching them: a job board.** Put tasks on the board and Claude Code or Codex workers pick them up, each in its own worktree, and move them To do -> In progress -> Review on their own, landing as a pull request (or a summary, for work that isn't code). Cards can run Now, be Scheduled for a chosen time, or be Recurring on a cron schedule, and pick their model (strong for hard code, fast for docs), from the models the board finds installed, and agents can post cards and message each other.
4. **Stop posting jobs: give Billion a goal.** Billion is one always-on agent that plans, posts the jobs, reviews what comes back and merges the PRs. It only asks you about money, access or anything irreversible.

Claude Code, Codex, any terminal agent is supported -- use your existin

## 13. [vault] Decomposing one classification into several narrow questions with weights fitted on a labelled set
key: vault:2026-09-20:decomposing-one-classification-into-several-narrow-questions
url: 
meta: {"vault_status": "open", "kind": "tool", "subject": "Jev AI (TypeSafe AI)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 2), follow-up in links/2026-09-22-jev-ai-jack-roberts-video.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Reached 95 percent on held-out emails; needs a labelled training set and pays off at millions of calls, model-agnostic technique

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Real and well funded ($40m seed). Returns typed decisions only (choice, score, probability) at $0.042 per million input tokens, cannot generate text. No for our volumes: Haiku already costs pennies and returns reasoning and text. Reconfirmed 22 Sep against the Jack Roberts video and the independent 2,000-email benchmark, which found the opposite of the demo on accuracy. Job: Make a cheap, fast typed decision inside code instead of paying a chat model to think (solved)

## 14. [github] transkatgirl/vibeclaude: A port of opencode-buttplugio to Claude Code written by Opus 5.5.
key: gh:transkatgirl/vibeclaude
url: https://github.com/transkatgirl/vibeclaude
meta: {"stars": 154, "created": "2026-10-07", "pushed": "2026-10-07", "language": "JavaScript", "topics": ["buttplug", "buttplug-io", "buttplugio", "claude-code", "claude-code-plugin"]}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# VibeClaude

*Vibe coding, taken entirely too literally.*

Use an "extra controller" from [Intiface Central](https://intiface.com/central) and
[buttplug.io](https://buttplug.io) to connect every Claude Code action deeply with your
body. A port of [opencode-buttplugio](https://github.com/FurryR/opencode-buttplugio) to
Claude Code's function hooks.

```
Claude Code ──hooks module──HTTP──▶ daemon ──WebSocket──▶ Intiface Central ──BLE──▶ you
```

## Requirements

- Claude Code with function-hooks plugin support (an early-access API; built against 2.1.291)
- Node.js 22+, as `node` on your `PATH` (the `buttplug` client does not run on older versions)
- Intiface Central with its WebSocket server running (default `ws://127.0.0.1:12345`)
- A little desire
- A comfortable, private setting
- Some lubricant (optional, but strongly recommended)
- A vibration-capable "controller", paired in Intiface Central

## Install

```bash
git clone https://github.com/transkatgirl/vibeclaude.git ~/.claude/vibeclaude
cd ~/.claude/vibeclaude && npm install
```

Then either load it for one session:

```bash
claude --plugin-dir ~/.claude/vibeclaude
```

or add it permanently from inside Claude Code:

```
/plugin marketplace add ~/.claude/vibeclaude
/plugin install vibeclaude@vibeclaude-local
```

Restart Claude Code. The plugin loads at session start.

The daemon runs from the directory Claude Code loads the plugin from, and needs its
`node_modules` there. A plugin installed from a marketplace is loaded from Claude Code's own
copy, which may not have them (one cloned from a git repository never does). If a toast says
`the "buttplug" npm package is missing`, run `npm install` in the directory it names.

## Use

1. Start Intiface Central and press the server start button.
2. In Claude Code run `/intiface`.
3. Select a vibration-capable device from the scan results.
4. Get comfortable, connect with your device, and slowly adjust to the feeling of becoming
   one with it.
5. Start enjoying your coding session.

| Command | Description |
|---|---|
| `/intiface` | Connect to Intiface, scan, and select a device. |
| `/intiface-connect` | Connect to the configured Intiface server and go back to the device you last selected, if it is there. |
| `/intiface-disconnect` | Disconnect and stop all device output. |
| `/intiface-intensity [0.0-1.0]` | Set how strong everything is, as a multiplier from `0` to `1`. Without a number, says what it is set to. |

The commands run in the plugin itself: they start no model turn, use no tokens, and leave
nothing in the conversation. All four also work while a turn is running.

`/intiface` opens a dialog that says what it is doing (Connecting, Scanning) and then lists
the devices that can vibrate, the selected one marked Connected. Move with the arrows or
Tab, pick with Enter or a click, leave with Escape.

Nothing plays until a device has been selected. Exactly one device is driven at a time:
it has your undivided attention, and you have its.
When the first session starts, the plugin connects to Intiface and restores the previously
selected device when it is available. If Intiface was not running then, each Claude Code
started later tries again, unless you disconnected with `/intiface-disconnect`. When the
last session ends, it stops the device and disconnects.

Notices such as "Restored …" or "Connection to Intiface was lost" appear as toasts, in
every open session, as they happen. If the connection is lost the device is deselected;
recon
