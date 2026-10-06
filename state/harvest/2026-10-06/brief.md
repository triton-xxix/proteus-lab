# Harvest brief, 2026-10-06

14 items shortlisted from 195 candidates (66 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] A 10 to 30 pound a day local lead-gen test for one Neptune client using the course build and its testing discipline
key: vault:2026-10-06:a-10-to-30-pound-a-day-local-lead-gen-test-for-one-neptune-c
url: https://www.skool.com/theadsclinic
meta: {"vault_status": "open", "kind": "service", "subject": "The Facebook Ads Clinic (Skool community, Nick Boddington)", "date": "2026-10-06", "where": "TRITON-CORE/Education/Courses/facebook-ads-clinic/DIGEST.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Needs a client with budget; the gas-engineering client is the candidate

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Free Skool community, 7,000 members, extracted 2026-10-06: 8 of 11 courses, 98 lessons, 80 transcripts, three courses locked behind an owner unlock, a purchase and a paid tier. Real teaching in the Masterclass, Lead Gen, Testing and Local Businesses courses; the welcome and coaching pages are the funnel to his paid tiers. Digest in the vault. About two thirds transfers to a UK trades and dental agency, the ecommerce course and US clinic case studies do not. Job: Run profitable Meta lead-gen ads for small UK trades and dental clients (still open) Write-up: `TRITON-CORE/Education/Courses/facebook-ads-clinic/DIGEST.md` Link: https://www.skool.com/theadsclinic

## 2. [hn] Engineer says Claude Code has made his job "soul-sucking"
key: hn:49971473
url: https://www.techspot.com/news/113937-engineer-claude-code-has-made-job-soul-sucking.html
discussion: https://news.ycombinator.com/item?id=49971473
meta: {"points": 61, "comments": 84, "created": "2026-10-05T22:01:35Z"}
query: claude code

comment (blinkbat): quit
comment (TheAmazingRace): I should preface my comment with the fact that I’m ultimately neutral on the AI space right now. I’ve gone back and forth on the topic. That said, I think this article underscores the fact that software engineering as a discipline is already unrecognizable from what it was like even a few years ago. You now have to be more into architecture and directing how the AI development tools write out your code. I know a guy who works at Amazon, and the models at OpenAI and Anthropic are so good that he doesn’t even really write code in the classic sense anymore. However, because of his background and 
comment (isubkhankulov): I feel the only people struggling with this are people who loved programming and syntax. Product-minded software engineers are thriving. Less tedium, easier refactors, manageable scope creep. The “hard” part of engineering has moved up to higher level challenges: evals, sandboxes, etc

## 3. [github] Vincentwei1021/mg-styles-15: 15 motion design styles, each made by Claude Opus 5.5 writing code from one prompt: watch the films, copy the prompts, read the full source.
key: gh:vincentwei1021/mg-styles-15
url: https://github.com/Vincentwei1021/mg-styles-15
meta: {"stars": 333, "created": "2026-10-02", "pushed": "2026-10-05", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# 15 Motion Design Styles

**Fifteen styles, one 10-second film each, all made by Claude Opus 5.5 writing code.** 
**15 种 MG 动态设计风格，每种一支 10 秒成片，全部由 Claude Opus 5.5 写代码做出来。**

Every film comes with its style notes, its full prompt and its complete source. 
每支片都附风格说明、完整提示词和全部源码。

   

[**▶ Watch all 15 films with sound · 在线观看**](https://vincentwei1021.github.io/mg-styles-15/)

**English** | [简体中文](README.zh-CN.md)

   [](LICENSE) [](https://vincentwei1021.github.io/mg-styles-15/)

 

> **中文用户请看这里：[完整中文说明 README.zh-CN.md](README.zh-CN.md)** 
> English readers: keep reading below.

## What it is

Fifteen 10-second motion-design films, one style each, from frame-by-frame cel animation to a 9:16 variety-show edit. Claude Opus 5.5 made every film by writing code from a prompt: the picture, the animation, the music and the sound effects. This repository publishes all of it, so you can watch a style, read how it was made, copy its prompt and make a film of your own.

- **No image or video generation.** The picture is code: SVG, Canvas, WebGL and Three.js, with Blender for the 3D film. A few films use CC0 or public-domain photos.
- **The sound is code too.** Each film's `audio.py` synthesises its music and sound effects; the 15 soundtracks draw on 103 recorded instrument samples.
- **Everything is published.** The film, the style notes, the full prompt and the complete source, for all 15 styles.

## How a film is made

   

Every film is a web page that draws the frame for any time you give it (`window.renderAt(t)`). The renderer captures each frame in headless Chrome, then ffmpeg joins the frames and the soundtrack. The 3D film is the one exception: Blender renders its picture, and a web page adds the type and grain. Each film went through two rounds of review and revision. Final scores from the AI jury run from 7.57 to 8.21 out of 10.

## The 15 styles

Click a film to watch it with sound on the page.

 
 
      01 · Frame-by-Frame / Line Boil   HAND MADE    Prompt  ·  Source   
      02 · Isometric 2.5D   ISOPOLIS — Let the City Grow    Prompt  ·  Source   
      03 · Flat Vector   popwise — One Dot    Prompt  ·  Source   
 
 
      04 · Line Art   ATELIER LINEA — One Line    Prompt  ·  Source   
      05 · 3D Render   soft. — Soft Landing · C4D / Blender look    Prompt  ·  Source   
      06 · Shape Morph   morphe. — One Shape, Every Story    Prompt  ·  Source   
 
 
      07 · Sticker Explainer   How Many Elements Hide in a Phone?    Prompt  ·  Source   
      08 · Cyberpunk HUD / FUI   KESTREL-9 · Target Acquired    Prompt  ·  Source   
      09 · Collage / Cut-out   NOGGIN Quarterly    Prompt  ·  Source   
 
 
      10 · Aurora &amp; Glassmorphism   Aurora — Think in Light    Prompt  ·  Source   
      11 · Geometric Bauhaus   KONSTRUKTION · 20 Beats    Prompt  ·  Source   
      12 · 80s Synthwave / VHS   NEON DRIVE — Midnight 1986    Prompt  ·  Source   
 
 
      13 · Pixel Art   PIXEL QUEST    Prompt  ·  Source   
      14 · Liquid Motion   drop. — It All Starts with a Drop    Prompt  ·  Source   
      15 · Variety Captions   Miaowu Diary EP.07 · 9:16 vertical    Prompt  ·  Source   
 
 

On the page, each style has its own section: the film, what the style is and how this film was made. Below it, one click opens the full prompt or a browser for every source file. The page switches between English and Chinese.

[](https://vincentwei1021.github.io/mg-styles-15/)

## Make a film from a prompt

1. Open an AI assistant that can write code

## 4. [arxiv] Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents
key: arxiv:2610.06650
url: https://arxiv.org/abs/2610.06650
meta: {"published": "2026-10-05", "authors": ["Mohamed Chenene", "Carlos Rosas-Hinostroza", "Pierre-Carl Langlais", "Anastasia Stasenko"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Wikidata is one of the largest open knowledge bases, yet answering a complex question over it still requires a SPARQL query that names the right entities and properties and chains their relations. Language models offer a natural-language alternative but answer largely from memory, which is least reliable for less prominent entities. We study agents that instead answer by exploring the graph, and argue that two obstacles limit them: the lack of training data recording how a solver explores, and interfaces that add large graph results directly to the model's context. We test three hypotheses: that the difficulty of graph search can be controlled through the structure of a question rather than only through obscure entities or wording; that much of the failure on long-horizon search comes from how retrieved evidence is managed rather than from the model itself; and that, in a suitable environment, open-weight models can match commercial closed ones. We construct multi-hop questions on a frozen Wikidata snapshot by replacing named entities with nested conditions, checking after each expansion that the target remains unique and that every new condition is necessary. We release 10,235 solving traces over single-entity and multi-hop questions, together with the recursive language model (RLM) harness that produced them, in which models batch graph calls, keep results in persistent Python state and interpret selected evidence through sub-calls. On 100 questions, the harness improves both models we ran under both interfaces compared with direct tool calling over the same functions: gpt-6-luna rises from 49 to 61 correct answers, doubling its multi-hop accuracy, and Qwen3.8-27B, an open-weight model served on a single GPU, from 60 to 74.

## 5. [youtube] How Car Origin Affects Depreciation in the UAE? 🏎️
key: yt:1dbh-4kz8JA
url: https://www.youtube.com/watch?v=1dbh-4kz8JA
meta: {"channel": "Seez", "rank": 2, "duration_min": 0}
query: car depreciation data analysis

# How Car Origin Affects Depreciation in the UAE? 🏎️
# Seez
# https://www.youtube.com/watch?v=1dbh-4kz8JA

[00:00] The difference is honestly the origin makes a difference. Like a Japanese car that gets imported to the UAE normally tends to be clean. It's a clean car that just they wanted to provide for another market. Um and those they they have different depreciation sets. So a Japanese non-GCC car would probably depreciate 10 to 15% more than a GCC vehicle. Um now an American spec they're they're a whole different beast. Um they come from North America normally with salvaged uh titles. are not clean and they come here into this region and get rebuilt and then they get sold again. Um
[00:33] so for us we looked at that as more of a 25 to 30% depreciation from what it would normally be if it was not if it was GCC. Um, so the origin where the car comes from is definitely important, especially if you're looking to buy a car in this region.

## 6. [awesome] degordonstech/pwa2play (new in awesome-claude-code)
key: gh:degordonstech/pwa2play
url: https://github.com/degordonstech/pwa2play
meta: {"list": "awesome-claude-code", "stars": 1, "created": "2026-08-10", "language": "JavaScript", "description": "Package a PWA into a signed, Play-Store-ready Android app bundle. A Claude Code plugin."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# pwa2play

A Claude Code plugin for getting a PWA onto the Google Play Store without hitting the same wall three times.

I built this after packaging my own web app as an Android app and losing a weekend to problems that had nothing to do with my code: the app opening with a browser bar across the top, an update rejected for being "signed with the wrong key," a build bounced for targeting the wrong API level. None of the error messages told me what actually went wrong. This plugin is everything I learned, written down so the assistant walks you past each trap before you hit it instead of after.

## What it does

Under the hood you are building a Trusted Web Activity (TWA): a small Android app that opens your website full screen, no browser chrome, once your site proves it owns the app. Google's Bubblewrap does the building. The hard part was never the build command. It was the five or six rules around it that decide whether Google accepts the upload, and this plugin encodes those.

## Install

```
/plugin marketplace add degordonstech/pwa2play
/plugin install pwa2play@degordons
```

## Using it

Three commands, and a skill that the assistant pulls in on its own whenever you are talking about publishing a PWA to Android.

- `/pwa2play:package` walks you through a first release from scratch: init, build, the assetlinks file, and the first upload, stopping at each place people usually slip.
- `/pwa2play:update` rebuilds an already-published app for a new release, keeping the signing key and version code correct so the update is not rejected.
- `/pwa2play:check` reads the package id, version code, target SDK and min SDK straight out of a built `.apk`, so you can confirm what you are about to upload rather than trusting what the tool printed.

The check command uses a small script that needs one package. Run `npm install` once inside the plugin folder and it is ready.

## The short version of what it will save you from

- Generate your signing key once, then reuse that exact key for every update forever. A new key on an update is a hard rejection.
- Your `assetlinks.json` has to carry the app signing SHA-256 from Play Console, not the upload key. Get this wrong and the app opens with the browser address bar showing.
- Raise the version code on every single upload.
- Keep targeting the current API level (API 36 as of the 2026 deadline, raised roughly each August).
- Go through a test track first, and know that personal accounts owe Google a 12-tester, 14-day closed test before production while organization accounts do not.

## Requirements

Node.js and a JDK for Bubblewrap, a live PWA served over HTTPS with a valid web manifest, and a Google Play developer account.

## License

MIT. Use it, change it, ship with it.

## 7. [vault] Buying real human UGC clips from marketplaces and reselling them inside a client retainer
key: vault:2026-09-24:buying-real-human-ugc-clips-from-marketplaces-and-reselling-
url: https://www.instagram.com/reel/DdK9uWfRVRT/
meta: {"vault_status": "open", "kind": "scheme", "subject": "Paid UGC creator work (via @oliver.hustles reel)", "date": "2026-09-24", "where": "TRITON-CORE/Research/links/2026-09-24-paid-ugc-oliver-hustles-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Clips cost 25 to 60 dollars; a real human face is the one asset HyperFrames, avatars and ElevenLabs cannot produce

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) The account is a dead end: no footprint for the handle or its hashtags, reads as comment-farming on a viral clip. The mechanism is real and boring: a brand briefs a marketplace, a creator films 15-60s on a phone for a free product plus a fee, the brand owns the file and runs it as a paid ad, and the creator audience is irrelevant. Rates verified 24 Sep: JoinBrands from 25 dollars a video, Billo guide 50-100 for beginners and around 200 average. A beginner month is low hundreds and the failure mode is no briefs. The number that settles it as a job: JoinBrands lists AI-generated video at 5 dollars, one fifth of the human floor. INVERSION, which is the useful half: buy it rather than do it. Source clips at 25-60 dollars for trades and SMB clients and resell inside a retainer; a real human testimonial face is the one asset HyperFrames, the avatar engine and ElevenLabs cannot produce, and our stack owns everything after the raw clip. Job: Put a real human face in client ads at a price a trades retainer can carry, without filming it ourselves (still open) Write-up: `TRITON-CORE/Research/links/2026-09-24-paid-ugc-oliver-hustles-reel.md` Link: https://www.instagram.com/reel/DdK9uWfRVRT/

## 8. [hn] Claude Code’s suggested message feature: I think the real customer is the model
key: hn:49981905
url: https://www.zohaib.cc/blog/smartest-claude-code-feature
discussion: https://news.ycombinator.com/item?id=49981905
meta: {"points": 46, "comments": 22, "created": "2026-10-06T18:00:34Z"}
query: claude code

comment (noworld): I think this analysis is spot on.
comment (stavros): This isn't really convincing, since you can do this even without showing the prediction at all. Simply ask the model to predict what the user will send, then show the actual next prompt, and done. The only reason to show this would be to influence the user's next prompt, which the article doesn't touch on.
comment (ipython): We had processor level branch predictors. Now do we not only pre fill the next prompt, why not just start generating the response as well? Interesting thought at least.

## 9. [github] arielshad/3d-asset-server: 3d assets api and mcp
key: gh:arielshad/3d-asset-server
url: https://github.com/arielshad/3d-asset-server
meta: {"stars": 234, "created": "2026-10-04", "pushed": "2026-10-06", "language": "TypeScript", "topics": []}
query: mcp server created:>{since} stars:>30

```
       +------------+
      /            /|      _____ ____       _                 _
     /            / |     |___ /|  _ \     / \   ___ ___  ___| |_
    +------------+  |       |_ \| | | |   / _ \ / __/ __|/ _ \ __|
    |            |  |      ___) | |_| |  / ___ \\__ \__ \  __/ |_
    |            |  +     |____/|____/  /_/   \_\___/___/\___|\__|
    |            | /       ____
    |            |/       / ___|  ___ _ ____   _____ _ __
    +------------+        \___ \ / _ \ '__\ \ / / _ \ '__|
                           ___) |  __/ |   \ V /  __/ |
                          |____/ \___|_|    \_/ \___|_|

        one search box for 3D models, materials, textures, HDRIs & game assets
                         HTTP API  *  MCP server  *  web UI  *  CLI
```

**3d-asset-server** searches 19 asset sites at once and downloads what you pick, ready to drop
into a game or a website. Use it from a browser, from `curl`, from the command line, or let your AI
assistant drive it over MCP.

> *"I need a low-poly tree pack, a mossy rock material and a sunset HDRI for my Three.js scene."*
>
> Your assistant calls `search_assets` three times, shows you the options with their licences, and
> `download_asset` puts glTF, textures and the HDRI into your project's `assets/` folder.

- **One query, many sources.** Results are merged and ranked, with a status line for every site.
- **Real downloads.** From free sources you get files directly: glTF with its `.bin` and textures,
  PBR maps at the resolution you ask for, HDRIs, or zipped packs (extracted for you).
- **Licence first.** Every result says what licence it has, whether it is free, and whether you
  must credit the author.
- **Honest about what's blocked.** Sites that block bots come back as links to their own search,
  so you still know where else to look.

---

## Contents

- [How it works](#how-it-works)
- [Sources](#sources)
- [Quick start](#quick-start)
- [Web UI](#web-ui) (and [for AI agents](#for-ai-agents))
- [MCP: use it from an AI assistant](#mcp-use-it-from-an-ai-assistant)
- [HTTP API](#http-api)
- [CLI](#cli)
- [Downloads](#downloads)
- [Configuration](#configuration)
- [Project layout](#project-layout)
- [Development](#development)
- [Licences & etiquette](#licences--etiquette)

---

## How it works

```
   +-----------+   +-----------+   +-----------+   +-----------+
   |  Web UI   |   |   curl /  |   |  Claude,  |   |    CLI    |
   | (browser) |   |  your app |   |  Cursor.. |   |           |
   +-----+-----+   +-----+-----+   +-----+-----+   +-----+-----+
         |               |               |               |
         |   GET /       |  /v1/*        | MCP           | search
         |               |               | stdio or /mcp |
         v               v               v               v
   +-----------------------------------------------------------+
   |                      3d-asset-server                      |
   |                                                           |
   |   +-----------------+   +-------------------------------+ |
   |   |  REST API (Hono)|   |  MCP tools                    | |
   |   |  /v1/search     |   |  search_assets   get_asset    | |
   |   |  /v1/assets/..  |   |  download_asset  list_provid..| |
   |   +--------+--------+   +---------------+---------------+ |
   |            |                            |                 |
   |            +-------------+--------------+                 |
   |                          v                    

## 10. [arxiv] HERA: Harness-Environment Co-Evolution for Reliable Agentic Abstention
key: arxiv:2610.06563
url: https://arxiv.org/abs/2610.06563
meta: {"published": "2026-10-05", "authors": ["Han Luo", "Bingbing Wen", "Guang Yang", "Zora Zhiruo Wang"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM) agents are increasingly capable of acting in complex tool-use environments, yet they often fail to recognize when tasks are infeasible and no valid solution exists. Recent work has formalized this reliability gap as the problem of agentic abstention, and existing approaches typically optimize a model or agent harness against a fixed set of tasks, leading to limited generalization to unseen failure modes. We introduce HERA, a framework for harness-environment co-evolution for agentic abstention. HERA consists of (i) a pipeline to automatically construct verifiable pairs of feasible and infeasible tasks by applying controlled environment mutations that transform solvable tasks into cases requiring abstention, and (ii) a co-evolution procedure in which performance failures on previous tasks are used to drive harness adaptation and generate new execution environments and tasks geared towards previous weaknesses. On held-out evaluation tasks, an evolved harness from HERA improves abstention accuracy from 61.7% to 83.3% while improving feasible-task completion from 68.3% to 76.7%, achieving the highest abstention and feasible-task completion among the compared methods. The resulting best harness transfers across 19 other LLMs, improving abstention accuracy by 15.3 percentage points on average without any model-specific optimization, and enabling smaller models to match the performance of more powerful models at an estimated 85% lower cost.

## 11. [youtube] The Four Types of Memory Every AI Agent Needs
key: yt:BacJ6sEhqMo
url: https://www.youtube.com/watch?v=BacJ6sEhqMo
meta: {"channel": "IBM Technology", "rank": 3, "duration_min": 10}
query: agent memory architecture explained

# The Four Types of Memory Every AI Agent Needs
# IBM Technology
# https://www.youtube.com/watch?v=BacJ6sEhqMo

[00:00] AI agents have different ways to remember stuff and each serves a different purpose. So let's take a look at the four main types of AI agent memory from some pretty foundational stuff to what I think are some quite interesting emerging areas. And I think it's really, first of all, worth considering how we do it. How does human memory actually. We can think of human memory as having first of all short-term memory. So that's the stuff that is active in the brain right now like what I'm saying at this very moment.
[00:43] That's one type of memory but there's also a type of memory called factual knowledge. So this is things like the company security policies that you remember or it could be facts like Python is an interpreted language. Then there are learned skills. Like, I don't know, writing backwards on a sheet of glass, for example, which I am totally doing here. There is absolutely no camera trickery involved. And then there is personal experience.
[01:20] Like the time I spent three hours debugging a Kubernetes cluster only to discover... I was pointing at the wrong cluster the entire time. Seriously, that was three hours of my time. Anyway, anyway, it turns out that well-designed AI agents, they also need these three types of memory or these four types of memories that I've got here. And there's actually a well-known framework for this. And it's from a Princeton research team and they gave it the name of CoALA. That's Cognitive Architectures for Language Agents, and CoALA maps out four distinct types of memory that agents need.
[02:01] So let's walk through each one and see how they actually work in real agentic systems today. So type one, that is working memory. This is the agent's context window. It's everything the agent can see right now, the current conversation, if there's any system instructions, they'll be in there. If there's any files or data that have been loaded into the prompt, that's where they'll be as well. So it's really kind of the scratch pad. And the analogy everybody uses for this is this is just like RAM, random access memory.
[02:39] It's fast and immediately accessible, but it's volatile. When the session ends, it's gone. And it's also limited in size. I mean the- the biggest context windows available today are pretty big. I mean, it could be like one million tokens or even more than that, but that still has a ceiling and try to stuff too much in there and performance is gonna degrade as the model starts losing track of things that are kind of buried in the middle of the context window. So every agent has working memory, but then so does every chat bot, it's just the context windows.
[03:19] So the question is... What else do agentic systems need? Well let me add to that list number two semantic memory and this is the agent's knowledge base, so semantic memory stores facts and rules and conventions, documentation and in the academic literature this often gets described in terms of things like vector databases or as knowledge graphs, and yeah, those are real implementations, but, in a lot of production agentic systems today, semantic memory is something much simpler than that.
[03:59] It's just simply Markdown files, .md files. So take Claude code as an example of this. So it has one of these Markdown Files. It's one is called Claude.md and that sits in the root of a project. And that file co
[transcript continues in field-notes/staging/BacJ6sEhqMo.txt]

## 12. [vault] Getting a video into an agent as scene-change frames plus transcript, or via a bare URL to Gemini
key: vault:2026-09-21:getting-a-video-into-an-agent-as-scene-change-frames-plus-tr
url: https://www.instagram.com/reel/Db1USzsMNnZ/
meta: {"vault_status": "open", "kind": "repo", "subject": "bradautomates/claude-video skill (\"turn YouTube tutorials into Claude Code agents\", @jens.heitmann reel)", "date": "2026-09-21", "where": "TRITON-CORE/Research/links/2026-09-21-claude-video-skill-jens-heitmann-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Frames via ffmpeg and captions or Whisper fallback is the only mechanism; Gemini reads public YouTube URLs on its free tier, no install

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (repo) The repo is real (MIT, about 17.5k stars); the technique is theatre, since two models diffing the same video cannot tell which is right and a tutorial's failure mode is code that is correct on screen and wrong in your stack. Skip. Paste a URL into Gemini's free tier on the rare occasion a video needs reading. Never install a skill from a shortened link. Job: Get a long video's real content into an agent's context without watching it (still open) Write-up: `TRITON-CORE/Research/links/2026-09-21-claude-video-skill-jens-heitmann-reel.md` Link: https://www.instagram.com/reel/Db1USzsMNnZ/

## 13. [hn] Show HN: OpenChart – OSS TradingView alternative with your own AI agent
key: hn:49979793
url: https://github.com/longsurf-ai/openchart
discussion: https://news.ycombinator.com/item?id=49979793
meta: {"points": 34, "comments": 12, "created": "2026-10-06T15:16:45Z"}
query: claude code

Hi HN, I'm Weilun, cofounder of OpenChart. We built OpenChart because we wanted Claude and Codex to interface with the markets, like most of humans do, through charts rather than through CLIs. With your existing AI plans, your agent can work directly with your charts: annotate a setup, write an indicator, investigate a market move, or create an alert. The chart, conversation, and research live in the same workspace. OpenChart alerts on any market move: draw any shape on a chart and attach an alert. When price crosses it, the alert triggers your agent to investigate the move and save the research in your workspace. The agents can work with charts, indicators, and alerts. Custom indicators and alert conditions are written in [Tea]( https://github.com/longsurf-ai/tea ), a programming language we built for the markets. We believe software shouldn’t impose artificial friction on your workflow. OpenChart is built on that belief with no software cap. The source code is publicly available, and you can use free market data from day one. We also offer optional paid cloud market data for lower latency. Everything is private. Your charts, research, and indicator code are stored on your own computer, with the app's backend running locally too. We currently support only macOS on Apple Silicon, but we're expanding to more platforms. Website: https://openchart.co/ Download: https://downloads.longsurf.ai/openchart/darwin/arm64/OpenCha... We built OpenChart because we want to explore how asset
comment (keyuwus): Wow, amazing product!
comment (aurielws): Really like the design choice of keeping everything local (charts, research, indicator code). Privacy-first + open source + agent-native is a combination I haven't seen anyone else ship for markets. Following this closely.
comment (ranli): Very interesting work, finally we have a local first unification layer on codex and cc

## 14. [github] Charlesmpc/by2kb: Forward videos from IM to transcript, Markdown, and your knowledge base — with raw and skill-updated outputs.
key: gh:charlesmpc/by2kb
url: https://github.com/Charlesmpc/by2kb
meta: {"stars": 92, "created": "2026-08-13", "pushed": "2026-10-04", "language": "Python", "topics": ["agent-skills", "ai-agents", "bilibili", "hermes-agent", "knowledge-base", "markdown", "self-hosted", "video-transcription"]}
query: youtube transcript pushed:>{since} stars:>20

# by2kb

**Forward a video. Keep the knowledge.**

`by2kb` turns a video URL into three durable Markdown artifacts in your own knowledge
base: the evidence-preserving transcript, a short “is this worth reading?” abstract,
and long-form study notes.

The primary user is an **agent user**. Send a Bilibili URL or media attachment to an
agent such as Hermes; `by2kb` handles media retrieval and the selected local or cloud
ASR provider, while the agent uses its existing model authentication to produce both summaries.
Standalone users can run the same pipeline with their own OpenAI-compatible API key.

**Learning-topic discovery (new in 0.7.0).** Send
`by2kb 我想了解一下 TiDB 向量检索` through the updated Hermes plugin to get
3–5 numbered video recommendations, then reply with a number to enter the normal
transcription and knowledge-base workflow. Search sources are individually configurable;
caption-only previews never download audio or run ASR. See
[topic search and configuration](docs/topic-search.md) for CLI usage, selection
state, preview limits, and deployment requirements. Current built-in search sources
are Bilibili and YouTube; podcast and article ingestion remain future extensions.

## See it in action

**Save a video you like. Or explore a topic you want to learn.**

- **Save a video:** send its link to Hermes, then keep the transcript, short abstract,
  and study notes in your own knowledge base.
- **Explore a topic:** ask Hermes about a learning topic, browse relevant video
  recommendations, and reply with a number to transcribe and save your selection.

https://github.com/user-attachments/assets/0cbec29a-f2a7-4279-bff1-a3c021574808

*36.6-second demo (by2kb 0.7.3): two Hermes-on-Telegram workflows, with Chinese
captions. Processing waits have been cut for brevity, not shown in real time.
Sound optional.*

> **[Latest release](https://github.com/Charlesmpc/by2kb/releases/latest).** Agent-guided installation, a cloud-free local Whisper
> default, upgrade-safe personalization, Bilibili/YouTube ingestion, Agent/API
> enrichment, task control, and the Hermes plugin are implemented. A resident service,
> native Telegram/Lark bots, and remote knowledge-base sinks remain planned.

## Start here

Requires Python 3.12+, `pipx`, and `ffmpeg`/`ffprobe` on PATH.

### Ask your Agent to install it

Send this prompt to an Agent with terminal access:

```text
Read and follow the official by2kb installation skill:
https://raw.githubusercontent.com/Charlesmpc/by2kb/main/skills/install-by2kb/SKILL.md
```

The installation Skill defaults to local faster-whisper, Agent-hosted summaries,
Bilibili and YouTube sources, and a local Markdown knowledge base. It does not clone
the repository or ask for cloud credentials in chat.

Upgrades replace application and adapter code but preserve `$BY2KB_HOME` (normally
`~/.by2kb`), the configured knowledge-base folder, downloaded models, job history,
credentials, and custom Skills. See [Upgrading](docs/upgrading.md).

### Install it yourself

Install the published package with local Whisper and YouTube support:

```bash
pipx install "by2kb[asr-whisper,youtube]"
by2kb init --preset agent-local
by2kb models install
```

Cloud Doubao ASR remains available for machines that should not run Whisper locally:

```bash
pipx install "by2kb[asr-doubao,youtube]"
by2kb init
```

`by2kb init` guides you through four decisions:

1. where the local knowledge base should live;
2. whether transcription uses local faster-whisper or cloud Douba
