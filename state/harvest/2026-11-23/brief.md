# Harvest brief, 2026-11-23

13 items shortlisted from 410 candidates (336 dropped as already seen, 4 carry a vault verdict on the vendor).

## 1. [vault] spin-tax email variants and 3-step plain-text sequence
key: vault:2026-11-23:spin-tax-email-variants-and-3-step-plain-text-sequence
url: https://www.youtube.com/watch?v=hv0G75NVVkQ
meta: {"vault_status": "open", "kind": "service", "subject": "Dylan Power: sell AI websites to local businesses (YouTube course)", "date": "2026-11-23", "where": "TRITON-CORE/Research/links/2026-11-23-dylan-power-ai-websites-course.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: new to us, test once the list is refilled

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Mechanism sound and mostly already ours; income claim unverified, ends in a mentoring pitch Write-up: `TRITON-CORE/Research/links/2026-11-23-dylan-power-ai-websites-course.md` Link: https://www.youtube.com/watch?v=hv0G75NVVkQ

## 2. [hn] Show HN: Hermit CRM – Free open-source CRM for solopreneurs
key: hn:50609708
url: https://hermitcrm.io/
discussion: https://news.ycombinator.com/item?id=50609708
meta: {"points": 30, "comments": 2, "created": "2026-11-23T10:09:02Z"}
query: open data api

I was about to keep track of my clients and prospecting in Google Sheets for my solopreneur business, when I remembered that's exactly what I advise my clients not to do. Created Hermit CRM, an open source CRM for 1 person. Hermit helps to keep track of deals and prospecting. The platform is built for AI by storing the data in Markdown files in git, stored locally and can be accessed with a web app, CLI or MCP. No telemetry on the app. Building in public, even the website stats are public as well. It’s macOS first. Linux is less tested, and Windows isn’t supported. Features I'm proud of: - import somebody from LinkedIn into to the CRM with 1 click - adding a LinkedIn convo to the CRM with 1 click. Both work without LinkedIn or CRM subs. Don't like what you see? Fork the Hermit with your AI. Would love to learn how you're using Hermit and where it doesn't fit your workflows.
comment (dominotw): how did this make it to frontpage of HN. Genuinely curious. Seems like someones openclaw finally got through.
comment (gijsbos): A few extra details: Code: https://github.com/Hermit-CRM/hermit-crm Why Markdown in git? So you can grep it, edit it in an editor, and an AI agent can read and update it without an API. I use the MCP server a lot. I ask Claude things like "who haven't I followed up with in the last two weeks?". Happy to implement what would make hermit-crm more useful for you.

## 3. [github] erkamyaman/safe-anything: Find the holes before someone else does. A fast, 100% Rust vulnerability scanner: XSS, SQL injection, leaked secrets, dependency CVEs and AI agent setups.
key: gh:erkamyaman/safe-anything
url: https://github.com/erkamyaman/safe-anything
meta: {"stars": 481, "created": "2026-11-22", "pushed": "2026-11-23", "language": "Rust", "topics": ["ai-agents", "claude-code", "claude-code-plugin", "cli", "codex", "cursor", "devsecops", "mcp"]}
query: claude-code created:>{since} stars:>20

safe-anything 

  Find the holes before someone else does.  
One command finds XSS, SQL injection and other vulnerabilities in your code, leaked secrets, 
risky mobile and cloud config, vulnerable dependencies, and the AI agent setup that writes it all. 
Every finding comes with the line, the reason and the fix. 

 
   
   
     
     
     
   
     
     
 

   Install   ·  Releases  ·  Claude Code plugin  ·  GitHub Action  ·  All 74 rules  ·  Agent setups  
Made in Türkiye 🇹🇷 by  erKam Yaman , who also made  rust-anything  ·  ❤️ Sponsor me  · Sponsored by  CodeRabbit  

 
   
   
   A real run on  OWASP Juice Shop  and on an agent setup with the usual mistakes (Apple M4).  What it finds on other repositories . 
 

 
   
     
       Your code  
      SQL and command injection, XSS,  eval , SSRF, path traversal, unsafe deserialization, weak crypto. Nine languages and SQL.
     
     
       Your secrets  
      Cloud and AI keys, tokens, private keys, passwords, and  .env  mistakes: committed env files, real values in  .env.example , secrets behind  NEXT_PUBLIC_  or  VITE_ . Always redacted in the output.
     
     
       Your stack  
      Android and iOS settings, Docker, GitHub Actions, Kubernetes, Terraform, nginx, and every locked dependency against OSV.dev.
     
     
       Your agent  
      MCP servers, Claude Code, Codex, Cursor, Gemini and OpenCode settings, hooks and skills: the files that decide what your agent may do.
     
   
 

## Quick start

```bash
cargo install safe-anything    # or: npx safe-anything .
safe-anything .
```

That's it. No config, no account, no upload. It exits with 1 when something high or critical is
found, so it works as a pre-commit or CI check as is.

```bash
safe-anything . --json             # machine-readable report
safe-anything . --sarif            # GitHub code scanning
safe-anything . --offline          # no network (skips the dependency check)
safe-anything . --severity medium  # hide low findings
safe-anything . --fail-on never    # always exit 0 (or low, medium, high, critical)
safe-anything . --include-tests    # also report findings in tests and fixtures
safe-anything --list-rules
```

- `.gitignore` is respected, and `node_modules`, `vendor`, `target`, `dist`, `build`, virtualenvs
  and `.claude/worktrees` are skipped. List more paths in `.safe-anything-ignore`.
- `safe-anything:ignore` in a comment silences that line (or the next one).
- In tests, specs and fixtures only real provider keys and private keys count, unless you pass
  `--include-tests`.

## What it finds

74 rules, each with a CWE id, an OWASP category and a link to the OWASP page that explains it.
The full list is in [docs/rules.md](docs/rules.md).

| | |
| --- | --- |
| **Code** | SQL injection, command injection, XSS (`innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `echo $_GET`, `raw`), `eval` and `new Function`, path traversal, SSRF, unsafe deserialization (pickle, `yaml.load`, `ObjectInputStream`, `BinaryFormatter`, `unserialize`, `Marshal`), TLS checks turned off, MD5/SHA-1, DES/RC4/ECB, JWT `none`, template injection, debug mode, insecure cookies, `Math.random` tokens. JS/TS, Python, Go, Java, Kotlin, PHP, Ruby, C#, SQL |
| **Secrets** | AWS, GitHub, Slack, Stripe, OpenAI, Anthropic and Google keys, private keys, passwords in code, credentials in connection strings, committed `.env` files, real values in `.env.example`, a `.gitignore` that misses `.env`, secrets behind public prefixes (`NEXT_PUBLIC_`, `VI

## 4. [arxiv] A Cognitive Agentic AI Framework for Interactive Process Analysis and Optimization
key: arxiv:2611.27725
url: https://arxiv.org/abs/2611.27725
meta: {"published": "2026-11-20", "authors": ["Trung Ngoc Trinha", "Roman Tschentscher", "Trong Dong Nguyen", "Trung Thanh Nguyen"], "categories": ["cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Complex multivariable process analysis and optimization require coordinated access to simulation, structured data, machine learning (ML), optimization, and scientific literature, often across disconnected software tools. We present a Cognitive Agentic AI Framework (CAAF) that enables interactive, iterative process investigation through natural-language prompts within an established flowsheet. Following harness-engineering principles, CAAF assigns task interpretation, planning, knowledge synthesis, and context management to a large language model while delegating numerical calculations to specialized tools. Dedicated providers connect databases, scientific-document retrieval, ML-assisted Bayesian optimization (BO), and COCO process simulation. The framework is demonstrated on methyl acetate production. Guided by successive prompts, an engineer explored multivariable relationships, conducted 4,000 BO iterations to maximize carbon conversion yield (C-Yield) and minimize specific energy cost (C-SEC), refined operating bounds, and verified selected candidates through process simulation. Re-simulation of 16 candidates within the restricted domain showed close agreement with ML predictions, with a mean absolute C-Yield error of 0.0085 (0.85 percentage points). The highest BO-derived C-Yield, verified by COCO, was 0.921 versus approximately 0.81 in the initial dataset, an improvement of about 11 percentage points. CAAF also detects and reports non-converged simulations, excludes invalid outputs, and continues subsequent evaluations. The results demonstrate how human-guided agentic coordination can combine engineering tools for iterative analysis and optimization with rigorous simulation-based verification under a fixed process topology.

## 5. [youtube] Top 5 fastest and slowest depreciating cars – a data driven analysis
key: yt:zvpGUyVa-3o
url: https://www.youtube.com/watch?v=zvpGUyVa-3o
meta: {"channel": "Fourwheel Trader - Car depreciation analysis", "rank": 1}
query: car depreciation data analysis


[body unavailable: NoTranscriptFound]

## 6. [awesome] taddeimania/lathe (new in awesome-mcp-servers)
key: gh:taddeimania/lathe
url: https://github.com/taddeimania/lathe
meta: {"list": "awesome-mcp-servers", "stars": 6, "created": "2026-11-07", "language": "C++", "description": "a minimal daw made for jamming with my buds"}
query: awesome-mcp-servers

# Lathe

[](https://tdqs.dev/reports/pij4jfw0uj) [](https://glama.ai/mcp/servers/taddeimania/lathe)

A small, dependable DAW. It opens, finds your interface, loads a template, and records. It hosts VST3 plug-ins, has a mixer with returns and sends, routes audio and MIDI to and from your interface, and exports a mix and stems. It doesn't try to do everything else.

Built with C++20 and JUCE 8.0.9, the same setup as the plug-in projects. It runs on macOS (CoreAudio), Windows (ASIO, WASAPI) and Linux.

Download it at **[getlathe.app](https://getlathe.app)**. How to use it is in **[docs/](docs/README.md)**.

---

## Downloads on getlathe.app

Publishing a release also puts it on the website: `.github/workflows/publish-downloads.yml` copies the three archives to the site's bucket, so the download buttons on [getlathe.app](https://getlathe.app) always get the newest published release.

## Build

### macOS

You need the Xcode command line tools and CMake (`brew install cmake`).

```sh
cd ~/Projects/lathe
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j
open build/Lathe_artefacts/Release/Lathe.app
```

The first configure downloads JUCE, which takes a minute. macOS asks for microphone access the first time Lathe opens the interface. Allow it, or nothing will record.

### Windows

You need Visual Studio 2022 (with "Desktop development with C++") and CMake. Install your audio interface's driver from its maker first, since its ASIO driver is what gives low latency.

```bat
cd lathe
cmake -B build -G "Visual Studio 17 2022" -A x64
cmake --build build --config Release
build\Lathe_artefacts\Release\Lathe.exe
```

ASIO support is built in automatically. Steinberg's ASIO SDK has been GPLv3 since October 2025, and CMake fetches it. To build without it, pass `-DLATHE_ASIO=OFF`. To use your own copy, pass `-DLATHE_ASIO_SDK_DIR=...`.

### Tests

```sh
cmake -B build -DLATHE_BUILD_TESTS=ON
cmake --build build
ctest --test-dir build --output-on-failure
```

These are headless engine checks that run a fake audio device through the real audio callback. They cover clip timing, plug-in delay compensation, mute, solo and faders, sends, looping, record-latency offset, export, project round-trip, clip splitting, undo (clips, tracks, plug-ins and routing), the AI assistant's tools (building a session, measuring CPU on a real-time audio thread), and joining clips (the joined audio plays back sample-identical). The test build also makes three tiny VST3s (one that works, one that crashes while loading, and one that hangs). With those, the tests check that scanning skips the bad plug-ins without freezing or crashing Lathe. They also test the plug-in store: release parsing against the real release format, picking the right platform archive, zip (with Unix permissions) and tar.gz installs, updates over an existing copy, staged updates, and the full download-and-install flow.

The engine renders tracks on several cores (docs/multicore.md). `ctest` also runs every test with each block shared over 4 threads (`LATHE_TEST_THREADS=4`), and compares 200 random sessions rendered on 1 and 4 threads sample for sample. CI's **Thread check** job runs both under ThreadSanitizer. For the speed: `LatheTests --bench out.csv 1,full`, or `Lathe --benchmark` on any machine (docs/performance.md).

## Third-party code

The sound engines of Multi Synth, Resonator, Grains and Random Notes are Émilie Gillet's open-source DSP (MIT licence), vendored in `ThirdParty

## 7. [vault] exact amount, date and exchange goal-to-plan prompt pattern
key: vault:2026-11-21:exact-amount-date-and-exchange-goal-to-plan-prompt-pattern
url: https://www.instagram.com/p/Dfy7_zAmIJh/
meta: {"vault_status": "open", "kind": "service", "subject": "@thinkgpt_ai Napoleon Hill Claude prompts carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-thinkgpt-napoleon-hill-claude-prompts.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: simple prompt frame, check the four slides before using

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Prompt-pack lead funnel; the exact-goal-to-plan frame is reusable, slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-21-thinkgpt-napoleon-hill-claude-prompts.md` Link: https://www.instagram.com/p/Dfy7_zAmIJh/

## 8. [github] JimLiu/open-artifact: Open, agent- and model-agnostic artifacts, all saved locally as plain files — edit, comment on, and export slides, UI designs, design systems, whiteboards, sheets, dashboards, docs, and motion.
key: gh:jimliu/open-artifact
url: https://github.com/JimLiu/open-artifact
meta: {"stars": 435, "created": "2026-11-17", "pushed": "2026-11-23", "language": "TypeScript", "topics": ["agent-skills", "ai-agents", "artifacts", "claude-artifacts", "claude-code", "claude-design", "codex", "coding-agent"]}
query: claude-code created:>{since} stars:>20

# Open Artifact

English · [简体中文](README.zh-CN.md) · [日本語](README.ja.md)

> **Formerly `baoyu-design`.** This project started as
> [baoyu-design](https://github.com/JimLiu/baoyu-design) (the old URL redirects here), which brought claude.ai-style
> Artifact types to local coding agents as one skill per type. Open Artifact rebuilds them as an open, agent-agnostic
> format: one local daemon, one page frame, one `/open-artifact` skill, and a plugin for each agent app.

**Open Artifact lets any coding agent make things people can open, edit and comment on, not just files.** You ask
your agent for a slide deck, a UI design, a design system, a whiteboard, a spreadsheet, a data dashboard, a doc or a short animated film. The agent writes a plain folder of files.
A local page opens it in a real editor, where you can fix a title, move a sticky note, leave comments, and export. Then
"Send to agent" sends your comments back to the agent's session.

https://github.com/user-attachments/assets/9f34dc69-2e90-4118-92fd-63f36d7bc5f9

Everything runs on your machine. No account, no upload, no specific model or vendor.

```
  you ──"/open-artifact slides a 6-slide pitch"──▶ agent (Claude Code, Codex, Cursor, Copilot, …)
                                                     │ writes files
                                                     ▼
                                           ./my-deck/project/deck.json + slides/*.html
                                                     │ served by the local daemon
                                                     ▼
  you ◀── edit · comment · export (PDF/PPTX/PNG/HTML) ── http://127.0.0.1: /a/ 
   └──────────────── "Send to agent" ──────────────▶ comments arrive back in the agent's session
```

## Documentation

Start in [docs/](docs/README.md) for full bilingual (English / 中文) guides for both users and AI agents:

- [What is Open Artifact?](docs/overview.md) — Core concept, key advantages, and quick start.
- [Artifact types overview](docs/artifact-types.md) — Compare all 8 types, how to choose, and storage models.
- [How agents use Open Artifact](docs/agent-guide.md) — MCP tools, CLI fallback, workflow lifecycle, comments, and safety rules.

### Building an agent product?

If you ship an agent app (desktop, IDE extension, command line, or a web app with a local helper), you can make Open
Artifact part of it: your agent makes artifacts through its own tools, the pages show in your UI, and the comments
people send from a page arrive in the right session. Start at
[Integrating Open Artifact into an agent product](docs/integrating.md); the Node SDK is
[`@open-artifact/harness-kit`](packages/harness-kit/README.md), and [examples/](examples/README.md) has runnable
adapters. Apps not written in JavaScript use the stdio bridge (`open-artifact harness --stdio`).

## Artifact types

| Type | What you get | Folder marker | Exports | Guides |
|---|---|---|---|---|
| **Slides** | A 1920×1080 (or 4:3) deck: slide rail, overview, speaker notes, builds, transitions, presenter mode | `project/deck.json` | PDF, PPTX, HTML, PNG | [Guide](docs/types/slides.md) · [SKILL](artifact-types/slides/SKILL.md) |
| **Design** | An infinite canvas of live `.dc.html` artboards: screens, components, click-through prototypes, notes, pages | `project/canvas.json` | PNG, JPEG, PDF, HTML | [Guide](docs/types/design.md) · [SKILL](artifact-types/design/SKILL.md) |
| **Design System** | A brand book: tokens, colors with contrast checks, type specimens

## 9. [arxiv] Can Language Models See the Circuit in Pixelated RFIC Passives?
key: arxiv:2611.27559
url: https://arxiv.org/abs/2611.27559
meta: {"published": "2026-11-20", "authors": ["Jonathan Zhou", "Kaushik Sengupta"], "categories": ["cs.AI", "cs.AR", "physics.app-ph"]}
query: all:"language model" AND all:agent AND all:tool

The emergence of inverse-designed, pixelated passives for microwave and millimeter-wave applications has been a major development in the field of RFIC design. These devices, which appear to be QR-code-like in structure, exist in a generalizable, high-dimensional design space that includes conventional passive topologies. However, these structures are naturally unintuitive for designers, and failures or deviations in performance are difficult to debug. In this work, we ask whether a frontier language model can understand, predict, and edit the responses and layout structure of pixelated passives. The agent, run with all tools disabled, is first asked to read layouts on 18x18 and 27x27 tile grids and, in a single reply, predict the input impedance and loss of the structure from 20-100 GHz. On eight GA-synthesized layouts and five random fills, the predicted Smith-chart locus follows full-wave simulation results closely, with a systematic shift that places features about 16% lower in frequency than EM. On multipath loop structures it identifies notches successfully but shows a smaller frequency bias, about half that of an ideal transmission-line model that ignores bends. The agent is then asked to debug seven designs that fail their specification, and given a budget of five EM simulations and at most twelve changed tiles, it is able to improve all seven and bring five designs within specification. These experiments suggest language models can serve as an interpretability and debugging tool for traditionally non-intuitive inverse-designed passives.

## 10. [youtube] The Fastest And Slowest Depreciating Affordable Sports Cars - Q4 2025
key: yt:VhYMxY77Oi4
url: https://www.youtube.com/watch?v=VhYMxY77Oi4
meta: {"channel": "Fourwheel Trader - Car depreciation analysis", "rank": 2, "duration_min": 14}
query: car depreciation data analysis

# The Fastest And Slowest Depreciating Affordable Sports Cars - Q4 2025
# Fourwheel Trader - Car depreciation analysis
# https://www.youtube.com/watch?v=VhYMxY77Oi4

[00:00] So, you want to buy an affordable sports car in 2025, but don't want to lose a fortune to depreciation? No worries. I'll guide you through the cars you should steer clear of if you care about resale values and those that should definitely be on your short list. Strong values are often associated with expensive Porsches and Ferraris. But you don't need to spend hundreds and thousands of dollars [music] to get yourself into a low depreciating sports car. But what's affordable? In this video, I'll interpret it as cars that are cheaper than the ones that usually feature [music] on this channel. The border will be at approximately $80,000,
[00:33] but don't worry, I'll also include cars that are way cheaper. This means that some brand new cars will be included that didn't feature before on the channel, but also some 15-year-old exotics. The video is packed with data, so let's get started. Before we dive into the individual models, it's important to set the context. So, let's first look at the general sports and supercar market. We can see that the average yearly price change has been recovering from its low of minus 12% per year. Depreciation rates decreased to more normal levels. In October 25, the average year-over-year decrease was
[01:06] -0.7% and most cars sit between -4.5 and + 1.9%. This might seem low, but remember that it includes everything from 986 Boxers to 458 specialis and Nissan Z's. Let's see now how the affordable cars are doing. Over here we have the big overview with the year-over-year price changes [music] for all the different models. The average decrease was 1.6% but there are major swings up and down. Some models increased by 10% while others are down by 15%. Now if you're a
[01:40] value conscious buyer, you probably want to avoid the cars at the top of the chart. So let's find out which affordable cars have the highest depreciation rate. I made the overview a bit smaller and only included the top 25% worse depreciating models, meaning the ones that lost more than 5%. Starting at the top, we can see that the Nissan Zenismo lost 14.6% during last year, making it the quickest depreciating model in this video. It did worse than the normal version, which lost only 9.5%. Let's inspect the price trends a bit
[02:13] closer. Prices for the Nismo started around MSRP and fell immediately after its introduction. The current medium price is $51.3,000 and this is 14.6% lower than a year ago. Naturally, supply ramped up in the meantime, helping to push prices down. The trend for the Z shows that prices were far above MSRP after its introduction and quickly corrected. The current depreciation rate of 9.5% is therefore relatively low compared to the car's price history. Nevertheless,
[02:46] [music] compared to all the other models we're looking at, it is on the high side. Back to the overview, the FType P380 and four cylinders sit at the second and third spot respectively. That's remarkable given their age. Looking at the trends, we can see that prices have been falling quickly and are compared to last year 12.5% lower in the four-cylinder market and 14.9% in the P380 market. The trend in the four-cylinder market seems to be flattening while this is not evident in the P380 market. And with that, we go
[03:20] back to the overview. Next on the list is the Aston
[transcript continues in field-notes/staging/VhYMxY77Oi4.txt]

## 11. [vault] one niche one offer one channel for 3 months
key: vault:2026-11-23:one-niche-one-offer-one-channel-for-3-months
url: https://www.youtube.com/watch?v=hv0G75NVVkQ
meta: {"vault_status": "open", "kind": "service", "subject": "Dylan Power: sell AI websites to local businesses (YouTube course)", "date": "2026-11-23", "where": "TRITON-CORE/Research/links/2026-11-23-dylan-power-ai-websites-course.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: decide whether to narrow from several lanes

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Mechanism sound and mostly already ours; income claim unverified, ends in a mentoring pitch Write-up: `TRITON-CORE/Research/links/2026-11-23-dylan-power-ai-websites-course.md` Link: https://www.youtube.com/watch?v=hv0G75NVVkQ

## 12. [github] hovocope135-tech/DSH-projects: 探索人与 AI 的最佳协作方式 · Exploring the best way for people and AI to work together. DSH-projects is an open-source plugin for DeepSeek Harness: state a goal in one sentence, it asks what is unclear, runs the tasks in parallel, and brings finished work back to you.
key: gh:hovocope135-tech/dsh-projects
url: https://github.com/hovocope135-tech/DSH-projects
meta: {"stars": 410, "created": "2026-11-17", "pushed": "2026-11-23", "language": "JavaScript", "topics": ["ai-agents", "claude-code", "context-engineering", "deepseek-harness", "task-management"]}
query: claude-code created:>{since} stars:>20

# DSH-projects

**你的下一个 Agent 产品，不需要你操心 Agent。探索人与 AI 的最佳协作方式。**

[English](README.en.md)

[](https://hovocope135-tech.github.io/DSH-projects/launch/dsh-projects-film.mp4)

你是否也经常在各个Session间反复切换，为配置各个agent感觉头疼？你是否也希望能够管理好大量的agent对话，而不需要自己来回搬运上下文？

如果你也希望探索更好的context管理方式，DSH-projects希望提供下一代的人机协作模式，隐藏所有不必要的细节，让人focus在真正重要的事情上，降低人机协作的成本。

以下是DSH-projects构建的核心哲学，也是和其他同类agent产品的最主要差异：

**1. 一切围绕任务本身的属性去组织context，管理多agent是伪命题，真正需要管理的只有context**

- 多agent的本质是上下文隔离：只有任务可分解、子任务之间没有顺序依赖时，才值得拆给多个agent并行；否则协调开销和错误放大会吃掉收益，沦为对人类会议室的肤浅模拟。
- 比起让agent互相审查，真正提升执行效果的，是每次执行都有意识地维护一份Goal/Loop文档，写清目标、完成标准和进展，否则AI会在长任务里目标漂移，自己发散掉。
- 有了任务的目标和规范，coordinator自然知道该用哪个model、加载哪些Skills、放开哪些权限。agent只是任务的一次临时Session，需要并行时仍然可以在任务层级开启多个Session；让人逐个去分配Skills、权限和runtime是额外的负担。我们认为，用户只需要感知model的差异就足够了。

**2. 最大化吸收 context，把人从整理上下文的杂活里解放出来**

- DSH-projects基于开源项目screenpipe，能够收集本地各个渠道的信息，帮助你起草邮件回复，做到真正想你所想
- 随时随地不用你搬运context，不需要操心环境、文件、开启新对话，个人助理会自己帮你把上下文组织和分配好

左：常见的多 Agent 产品，上下文、Skills 和 runtime 绑定在每个 Agent 上。右：DSH-projects，一个个人助理对应多个项目，每个项目按上下文边界拆分为多个任务；runtime 与上下文解耦，可按任务替换。标号对应[工程架构一文](https://hovocope135-tech.github.io/DSH-projects/site/blog/deep/)的章节。

**快安装DSH-projects试试看吧!**

## 上手

> npm 上的 `preview.1` 还是上一版界面。想要图里这一版，用「想从源码装」那几行。

需要 DeepSeek Harness（`npm install -g @deepseek-ai/dsh`，在 0.2.1 上测过）、Node 24 以上和模型的 API key。

```sh
dsh plugin --profile web add deepseek-harness-projects-plugin@preview
dsh --profile web        # 启动，在浏览器里打开它给的地址
```

 
 想从源码装 

```sh
git clone https://github.com/hovocope135-tech/DSH-projects
cd DSH-projects/plugin
dsh plugin --profile web add "$(pwd)"    # 把插件装进 DeepSeek Harness
dsh --profile web
```

 

详细步骤见[上手指南](docs/GETTING-STARTED.md)。

### 1. 快速配置助理

第一次打开，跟着**捏一个你的助理**选样子和性格，起名字，定一个呼出它的快捷键。它默认叫 Tacit。

### 2. 一切都交给你的私人助理！

在DSH-projects中，我们鼓励一切需求都直接通过和个人助理对话，向个人助理直接阐述你的需求，个人助理会自己把你的需求拆分为项目，创立新项目：

> 我们要招一名偏交互动效的前端工程师。帮我建个项目「前端招聘」，先做两件事：写一份二面题目 interview.md，出 3 道动效和交互细节的题，每题附评分要点；再做一个能挂到官网的招聘页 jobs.html。

任务做完，会出现在右侧的**待你决定**里，等你验收。

### 3. 在项目中，开始任务的管理

每个任务都有自己的一份长期上下文。点开任务，右侧的**任务详情**里是背景和你的原话、产出、进展、完成标准，以及这个任务用哪个模型。

交付的文件在**交付**里直接看：没问题点**验收通过**，要改点**请求修改**。

### 4. 持续工作，上下文不断累积，你的个人助理将越来越懂你

**电脑活动记录**（Computer History）把你在电脑上做过的事整理成一条时间线：每 10 分钟一段，写明在做什么、用了哪些应用。需要本机装有 Screenpipe，在**助理设置**的**活动与设备**里开启，之后可以直接问：

> 用一张可视化的图，展现我今天做了什么

它把这件事交给项目，交回来的就是图里这一张。

### 5. 再次回来

下线前把要做的事交代给 Tacit：

> 我先下线了，明早回来验收。夜里把这三件事做完：把招聘页出一版英文的 jobs-en.html；写一份发在招聘网站上的职位文案 jd.md；整理一份面试流程说明 process.md，写清一面、二面、终面各看什么。

回来时看右侧的**待你决定**：**项目进展**写着每个项目到哪了、哪些等你验收，**新消息与建议**是它夜里留给你的几条。

### 6. 截一块屏幕，直接问

在任何应用里按 ⌥⇧M，框住屏幕上的一块，在弹出的小窗里问一句，回答就显示在小窗里。目前只支持 macOS，小助手还没有放进这个仓库。

## 使用说明

**你可以对 Tacit 说：**

| 你说 | 它做什么 |
| --- | --- |
| 「帮我建个项目：招聘前端工程师」 | 新建一个项目 |
| 「把这件事交给招聘那个项目：……」 | 把你的原话原样交给项目，开成任务 |
| 「还有什么在等我？」「今天做了什么？」 | 读看板和时间线回答，每条带出处 |
| 「跟二面题目那个任务说，再加一道 CSS 的题」 | 给这个任务带话 |
| 「验收吧」 | 先告诉你改了什么，等你回「确认」再验收 |
| 「记住：我看东西习惯先看结论」 | 记进「关于你」，带着原话 |
| 「这个项目以后用便宜点的模型」 | 记成项目的模型策略，再按策略换模型 |

它不以你的名义发消息。没有你的一句话，它不拍板，也不验收。

## 更多思考

- [你的下一个 Agent 产品，不需要你操心 Agent](https://hovocope135-tech.github.io/DSH-projects/site/blog/)
- [工程架构：管理 agent，就是管理 context](https://hovocope135-tech.github.io/DSH-projects/site/blog/deep/)

## 现在到哪一步了

1.0 版。只能跑在 DeepSeek Harness 里，界面目前只有中文，飞书只读。Claude Code 当执行者实跑验证过；Codex 能选，但还没有验证到它跑完一个完整任务。这两者当执行者时不弹权限确认，也没有沙箱：你的系统用户能读写的，它都能读写。

许可证：[MIT](LICENSE)。

## 13. [youtube] Mid-Engine Cars Ranked: Depreciation Traps vs Smart Buys (2025)
key: yt:vF7tAj8Z8ek
url: https://www.youtube.com/watch?v=vF7tAj8Z8ek
meta: {"channel": "Fourwheel Trader - Car depreciation analysis", "rank": 3, "duration_min": 12}
query: car depreciation data analysis

# Mid-Engine Cars Ranked: Depreciation Traps vs Smart Buys (2025)
# Fourwheel Trader - Car depreciation analysis
# https://www.youtube.com/watch?v=vF7tAj8Z8ek

[00:00] Mid-enine cars are some of the most exciting machines you can buy. Not all of them are smart buys. Some hold their value incredibly well, while others are depreciation traps that could cost you tens and thousands of dollars. In this video, I've ranked the most popular mid-enine cars from smart buys to money pits. So, by the end, you'll know exactly which models to consider and which ones to avoid in 2025. Now, before we dive into the details, we first need to have a look at the market trend for mid-enine models. It provides us with a good context for interpreting the depreciation rates. The US yearly depreciation rate was still increasing
[00:33] in 2023 as the market corrected from its pandemic high. The average depreciation rate was approximately 12% per year and most models lost between 8 and 16% during that year. Rather extreme numbers. Mid-enine models bounced back fairly quickly and depreciated at a relatively stable rate till the end of 2024. In 2025, the market strengthened significantly. Depreciation rate started to decrease and now we can see that they even crossed the zero point. The average rate in September was plus 0.9% and prices for most cars changed between
[01:07] minus2.9% and plus 2.4%. Seems too good to be true. Well, it turns out that the mid-enine market isn't that unique. Over here, I added the general market trend and you can see that the mid-enine market is heavily correlated to the general trend. Most recently, the mid-enine cars increased slightly more, but we can't read too much into that. Now, the problem with these trends is that they're averages. There are mid-enine models that lost as much as 20%. So, buying one of these models if the market is basically flat isn't such a great idea if you're a value conscious buyer. So, which car should you avoid?
[01:42] the ones that belong to the top 25% quickest depreciating mid-enine models. So, let's look at the overview with all the price changes and zoom into the ones that lost more than 5%. The quickest depreciating car in the mid-enine data is a Ferrari, the 296. This is no surprise for those of you who look to mid-enine Ferrari market update. Switching to the price trends, we can see that both spiders and coups are dropping rapidly. Coups are down by 19.6% and spiders by 16.7%. In terms of value, this isn't Ferrari's strongest model. Now, I also looked a little bit deeper into the data, and it
[02:15] shows that the rate is decreasing slowly for higher mileage examples. So, I think it's unlikely that we'll see another 20% drop during next year, but it's likely that the drop will still be significant. Let's have a look now at some other models. Going back to the overview chart, we can see that also the Corvette C806 depreciated relatively quickly. They lost on average 14.5%. Diving into the price trends, we can see that most of this loss results from the deflating price premiums that were added on top of MSRP and that the situation is improving quickly. As I explained in
[02:48] other videos, I use the MSRP plus price premium because that gives the best estimate of the buyers loss. Looking at the numbers, we can see that coups lost 14% and spiders 14.9%. Now, buying a 296 or Z06 means that the depreciation rate will be a significant part of the total cost of ownership. So, it's not a bad idea to
[transcript continues in field-notes/staging/vF7tAj8Z8ek.txt]
