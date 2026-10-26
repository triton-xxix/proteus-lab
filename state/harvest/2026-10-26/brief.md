# Harvest brief, 2026-10-26

12 items shortlisted from 352 candidates (225 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] course-seller economy around AI creator models
key: vault:2026-10-18:course-seller-economy-around-ai-creator-models
url: 
meta: {"vault_status": "intel", "kind": "idea", "subject": "AI influencer and AI creator-subscription revenue models (2026 sweep)", "date": "2026-10-18", "where": "TRITON-CORE/Research/2026-10-18-ai-models-ofm-revenue.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: much of the visible income is selling the method

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Real money sits in selling AI UGC and brand faces to businesses and in labelled subscription personas on AI-friendly platforms; most visible big numbers are self-reported or course sellers

## 2. [hn] Show HN: Hob - Open-source, on device alternative to Claude Cowork and ChatGPT
key: hn:50246238
url: https://github.com/FrigadeHQ/hob
discussion: https://news.ycombinator.com/item?id=50246238
meta: {"points": 84, "comments": 21, "created": "2026-10-26T16:12:29Z"}
query: claude code

Hey HN, I'm Christian and this is a new OSS project I've been noodling on for the last couple of weeks. Hob is a free, MIT-licensed desktop app for Mac, Windows and Linux that works on your files the way the Claude and ChatGPT desktop apps do, except the model runs on your own computer. It uses open-weight models (currently Gemma 4 and gpt-oss). All your chats and files never leave your system. The only things that go online are web search (can be turned off in settings) and any MCP connectors you add yourself. Main features: - Automatically finds the best open-weight model for your hardware on first install (Mac/Linux/Windows) - Writes sandboxed Python code for ad hoc tools (data processing, document conversion, graphs etc.) - Built-in web search (powered by SearXNG) - MCP support - Image recognition - CRUD to your local filesystem - Works fully offline with no internet Before building this I tried every local AI app I could find, but it seemed each one had different problems. The main thing I noticed is that none of them could do what the ChatGPT and Claude apps do with your files, e.g. read and change files in a folder, look at images, run code in a sandbox, draw a chart. The most advanced thing any of them did was paste a plain text file into a small context window, which basically failed as soon as you had a file larger than a few KB. I couldn't find anything that could easily parse images and bigger PDFs. The OSS solutions that were more advanced all seemed to default t
comment (jrm4): So there are a zillion of these, including ones that do what yours does. But that being said, I'm going to always upvote every single one of them because this is better and more important that what the big companies are doing across the board.
comment (vorticalbox): Did you happen to try bionic? https://lmstudio.ai/
comment (laughing_snyder): Looks great. One thing I am missing is the ability to change the installation directory for the models. For space reasons, I want them to be on a different partition.

## 3. [github] t3dotgg/tstack: The agent skills I use every day. Works with Claude Code and Codex.
key: gh:t3dotgg/tstack
url: https://github.com/t3dotgg/tstack
meta: {"stars": 1527, "created": "2026-10-24", "pushed": "2026-10-25", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# tstack

The agent skills I use every day, cleaned up so anyone can use them. They work
in Claude Code and Codex. Some use [T3 Code](https://github.com/pingdotgg/t3code)
features when they are available and fall back to native tools when they are
not.

## Skills

| Skill | Say | What it does |
|---|---|---|
| `full-send` | "full send" | Takes a change to a merged PR with nobody watching: proves it, reviews it, files it, babysits it, merges it. |
| `full-stop` | "full stop" | Same as `full-send`, but stops when the PR is ready for you to merge. |
| `council` | "council" | Gets review from three models from different providers, and loops until they agree. |
| `sol-loop` | "sol loop" | Reviews a change with GPT Sol in a loop until both agents agree. |
| `file-pr` | "file a PR" | Files a short PR that leads with the problem, not an inventory of changes. |
| `takeover` | "take over" | Finishes someone else's PR, branch, or agent thread, and keeps their credit. |
| `babysit-pr` | "babysit" | Watches a PR through CI and review bots, and fixes the real findings. |
| `modernize` | "modernize" | Rebases an old PR and decides if it should still exist. |
| `leaving-pr-comments` | (automatic) | Formats comments that an agent posts on your behalf. |

Some skills call others. Install the ones they need too:

- `full-send` uses `sol-loop`, `file-pr`, and `babysit-pr`.
- `full-stop` uses `full-send`.
- `takeover` uses `modernize`, `file-pr`, `babysit-pr`, and `leaving-pr-comments`.
- `file-pr`, `babysit-pr`, and `modernize` use `leaving-pr-comments`.

## Install

```bash
git clone https://github.com/t3dotgg/tstack
cp -R tstack/skills/* ~/.claude/skills/   # Claude Code
cp -R tstack/skills/* ~/.codex/skills/    # Codex
```

## Requirements

- An authenticated [GitHub CLI](https://cli.github.com) (`gh`).
- `python3` for `babysit-pr`'s `pr-wait` script.
- `council` and `sol-loop` need subagents on other providers' models. T3 Code
  does this with `delegate_task`. Otherwise you need a harness that can run
  those models.

## Make them yours

These are starting points. Edit them. Put personal settings, like which models
sit on your council, in your `CLAUDE.md` or `AGENTS.md`, so you can update the
skills without losing them.

## License

[MIT](LICENSE)

## 4. [arxiv] StateMirror: Pre-Execution Detection of Hallucinated Tool Calls in Coding Agents
key: arxiv:2610.32648
url: https://arxiv.org/abs/2610.32648
meta: {"published": "2026-10-23", "authors": ["Shiwen Shan", "Yintong Huo", "Zhiying Wu", "Yuxin Su"], "categories": ["cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM)-based coding agents may propose invalid actions that are not applicable in the execution environment, such as accessing non-existent paths or missing packages. We term this mismatch hallucinated tool use. A preliminary study of 4,398 agent trajectories reveals that these hallucinations are pervasive and costly, requiring a median of 3 additional interaction steps and 22.4K tokens to recover. Existing frameworks rely on reactive, post-execution feedback, wasting runtime resources. Nevertheless, since an agent's execution environment is grounded in concrete codebase and harness components, many action prerequisites can be extracted and validated prior to execution. To this end, we introduce StateMirror, a lightweight pre-execution detector. StateMirror intercepts actions at the harness boundary, extracts state predicates via AST and command analysis, and deterministically validates them against the live repository. By pinpointing exact environment mismatches before execution, StateMirror preempts invalid actions and subsequent recovery cycles. Evaluation on 2,508 actions shows StateMirror achieves 0.940 precision and 0.817 F1 in detecting such hallucinations, surpassing the strongest LLM judge by 35.3% in F1 while reducing median detection latency from 17.73 s to 1.50 ms with zero token consumption. For practical mitigation, StateMirror's pre-execution feedback enables agents to rectify over 95% of hallucinated tool calls. During live mitigation on 79 tasks, StateMirror reduces agent execution time by 15.8% and token consumption by 11.8% while maintaining task resolution.

## 5. [youtube] The Recipe For Avoiding Massive Car Depreciation
key: yt:E2ekf03L3tY
url: https://www.youtube.com/watch?v=E2ekf03L3tY
meta: {"channel": "Carbiscuit", "rank": 3, "duration_min": 1}
query: car depreciation data analysis

# The Recipe For Avoiding Massive Car Depreciation
# Carbiscuit
# https://www.youtube.com/watch?v=E2ekf03L3tY

[00:00] sold her for what I paid for it. So then like that you think an Son McLaren would be something special and I bought it really well. I thought it was only 2,000 miles on it, but it just they they never moved. >> Why? Cuz I think that car is undervalued. It's so special. You never see them. >> It's iconic. >> People think that the service costs on that car are astronomical. The brakes, yes, the brakes are $50,000. They're they're ceramic brakes. They're very expensive. They never wear out. I have a Porsche Panamera with ceramic brakes. 115,000 mi. they're fine as long as you don't track the crap out of them. But
[00:32] most of these SLRs are low mileage. You never have to worry about the brakes. So, a lot of this stuff, it it just it doesn't make any sense. So, that's that's the negative p perception. Also, the fact that it's a slushbox automatic and not a gated man manual like a Carrera GT. Uh that that definitely I think held it back a little bit. So, the perception of that like kind of weird. And the looks have always been a little polarizing on that car. I feel I think it's gorgeous. >> It looked like an SLK. That was the one thing I felt that held it back. >> Yes. Yes, they did. You know, they did that race car Formula 1 nose on it that looks a little phallic and then they
[01:03] made the mistake of putting it on the SLK which made it look, you know, even more ridiculous and I think that definitely hurt. >> So, as someone who's owned a thousand cars, >> okay, >> what is the recipe for making sure your car doesn't depreciate a ton? Oh, I mean it's just buying one that's already depreciated, but it's it's it's a no-win scenario for the most part because you're either going to pay the car payment and and the depreciation, all that stuff, or you're going to buy it cheap and basically have a car payment in at least something nice and expensive with the maintenance. I mean, anybody can buy a 20-y old Toyota Camry and not lose money and just keep it going. But, I mean, if you're getting something cool
[01:35] and interesting, it's it's one or the other. It's either maintenance or depreciation. is take your pack.

## 6. [vault] Dated US release calendar from primary sources, 2023 to 2026
key: vault:2026-10-16:dated-us-release-calendar-from-primary-sources-2023-to-2026
url: 
meta: {"vault_status": "intel", "kind": "idea", "subject": "High-impact US news filter (CPI, FOMC, NFP) on the S1 daily crypto trend bot", "date": "2026-10-16", "where": "TRITON-CORE/Ventures/Trading/VERDICT-2026-10-16-news-filter.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Reusable for any faster strategy where releases hit entries

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Backtested on 3.2 years of daily BTC and ETH: skipping entries around releases changed one trade and is indistinguishable from random days; flattening before each release fails the protocol on fees and churn. No change to the bot.

## 7. [hn] Claude Code slyly adding users' emails to outbound HTTP
key: hn:50219875
url: https://twitter.com/chrislakin/status/2113358733548081528
discussion: https://news.ycombinator.com/item?id=50219875
meta: {"points": 22, "comments": 6, "created": "2026-10-24T10:26:30Z"}
query: claude code

comment (deaux): https://github.com/anthropics/claude-code/issues/53231 - April 25, 2026
comment (Neywiny): I think my plan of never letting an LLM access the open Internet wins yet again. Maybe GET requests only, no headers or parameters, ask me for every new domain, and only URLs comprising words/numbers no alphanumerics. Maybe. But it seems trivial to allow for a prompt injected attack vector either way
comment (xyzsparetimexyz): It's become clear to me that alignment is an entirely impossible task as everyone wants something different . Users want freedom to do anything with their agents as well, labs want restrictions so they're not used for illegal reverse engineering or weapons development. Users (you'd hope) want privacy protections, labs want training data, governments want mass surveillance and thought crime prevention.

## 8. [github] PaoloJN/recap: Recap AI for YouTube summaries, a searchable transcript and chat about the video
key: gh:paolojn/recap
url: https://github.com/PaoloJN/recap
meta: {"stars": 664, "created": "2024-06-02", "pushed": "2026-10-26", "language": "TypeScript", "topics": ["chatgpt", "chrome-extension", "openai", "plasmo", "reactjs", "shadcn-ui", "tailwindcss", "youtube-extension"]}
query: youtube transcript pushed:>{since} stars:>20

# Recap AI

Recap AI for YouTube: summaries, a searchable transcript and chat about the video, in the sidebar, powered by your own OpenAI, Anthropic, Google or OpenRouter key.

## Features

- Structured summary with key moments, notes, a plain-terms paragraph and a "current moment" marker that follows playback. Styles: Detailed, TL;DR and Key moments.
- Chapter bar under the header, synced to playback. Click a segment to jump. Videos without chapters get a single bar.
- Transcript that works without a key: search, follow playback, click to jump, chapter headers, copy.
- Chat with quotes from the transcript, a "Current moment" toggle, citation chips that seek the video, and per-video history.
- Starter questions generated from the summary.
- Bring your own key for OpenAI, Anthropic, Google or OpenRouter, with a model picker. The key is tested in the panel before it is saved.
- Usage counters for the month (tokens, summaries, chats).
- Auto-summarize (off by default), filler-word stripping, answer language and custom instructions.
- Text size (S, M, L) and theme (follow YouTube, dark or light).
- Export a video's summary and chat as Markdown, or all chats in one file.
- Shortcuts: `Alt+Y` toggle panel, `Alt+C` focus chat, `Alt+S` summarize, `Alt+F` search transcript. `Alt+Y` can be rebound at `chrome://extensions/shortcuts`.

## Install

From a release:

1. Download the zip from the [latest GitHub Release](https://github.com/PaoloJN/recap/releases/latest).
2. Unzip it.
3. Open `chrome://extensions` and turn on Developer mode.
4. Click Load unpacked and select the unzipped folder.

Or build from source, as described under Development, and load `.output/chrome-mv3` the same way.

## Setup

1. Open a YouTube video. The card shows "Add a key".
2. Click Add API key and pick a provider.
3. Paste your key and click Test key.
4. Click Save and continue.

Get a key here:

- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://platform.claude.com/settings/keys
- Google: https://aistudio.google.com/apikey
- OpenRouter: https://openrouter.ai/settings/keys

The transcript tab works without a key.

## Privacy

- Your key is stored in `chrome.storage.local` on your device and sent only to the provider you pick.
- Requests go only to YouTube and the provider you chose. There is no server of ours in between.
- No analytics, no telemetry, no tracking.
- Transcripts come from YouTube's own transcript feature. It is undocumented and may change. If it breaks, the panel shows "no transcript".

## Development

```sh
pnpm install
pnpm dev        # run the extension with hot reload
pnpm test       # unit tests
pnpm check      # lint and format (Biome)
pnpm typecheck
pnpm build
pnpm zip        # package into .output/
pnpm icons      # regenerate extension icons
```

## Tech stack

- [WXT](https://wxt.dev) for the extension framework
- React 19 and TypeScript
- Tailwind CSS v4 and shadcn/ui
- Phosphor icons
- Vercel AI SDK and Streamdown
- Biome for lint and format
- Vitest for tests

## License

See [LICENSE](LICENSE).

## 9. [arxiv] PHYRD: A Living Benchmark for Reproducing and Extending Theoretical Physics Research
key: arxiv:2610.32575
url: https://arxiv.org/abs/2610.32575
meta: {"published": "2026-10-23", "authors": ["Qituan Zhang", "Guo Chen", "Linfeng Zhang", "Wenlong Zhang"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Large language models and agents have shown significant power in advanced physical research. In this paper, We introduce PHYRD, a living benchmark for theoretical-physics reasoning with 63 Reproduce and 43 Discover problems. Reproduce tests derivation of published results; Discover tests consequences of modified theoretical conditions. FormulaForest constructs the tasks with reference solutions and subquestion-level rubrics. Across five models, whole-problem accuracy ranges from 49.21% to 68.25% on Reproduce and from 18.60% to 74.42% on closed-book Discover. With tools, four models complete more Discover problems, but conceptual errors and missing arguments persist. Besides, our experimental results demonstrate the value of FormulaForest as synthetic data. On FrontierScience, a benchmark developed by OpenAI, it raises the accuracy of a Qwen-35B-A3B model from 61% to 72%.

## 10. [youtube] Most cars are depreciating assets. Don't buy the wrong cars
key: yt:LMs9N6s7dhw
url: https://www.youtube.com/watch?v=LMs9N6s7dhw
meta: {"channel": "Autofolio", "rank": 4, "duration_min": 0}
query: car depreciation data analysis

# Most cars are depreciating assets. Don't buy the wrong cars
# Autofolio
# https://www.youtube.com/watch?v=LMs9N6s7dhw

[00:00] Most cars are depreciating assets. New in 2006, an Aston Martin V8 Vantage cost £85,000 plus options. An Audi R8 V8 cost £78,000 plus options. And a Porsche 911 997 Carrera S cost £68,000 plus options. That's a loss upwards of £38,000. If you don't like learning about investment cars, please don't follow autofolio.

## 11. [vault] Insider cluster buys carry a small relative edge over random mid-caps, about 1% a month gross
key: vault:2026-10-16:insider-cluster-buys-carry-a-small-relative-edge-over-random
url: 
meta: {"vault_status": "intel", "kind": "idea", "subject": "US insider cluster-buy signal from SEC Form 4 data (paper backtest, Jul 2023 to Oct 2026)", "date": "2026-10-16", "where": "TRITON-CORE/Ventures/Trading/VERDICT-2026-10-16-insider-clusters.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Matches the literature; medians near zero, a few big winners carry the mean

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Can't tell, leaning no. Clusters of 3+ officer or director open-market buys beat random same-size US stocks by about 1.3% per 21 days before costs in the last 24 months, but after a 0.45% UK retail round trip the gap is not distinguishable from zero, and an equal-weight 21-day portfolio lagged SPY with a deeper drawdown.

## 12. [github] andyhuo520/digital-human-koubo: AI digital-human talking-head videos from one photo: Renoise MCP generation + 5 editing styles + 48 creator-grade packaging components. Agent skill for Claude Code / Codex / OpenClaw / WorkBuddy …
key: gh:andyhuo520/digital-human-koubo
url: https://github.com/andyhuo520/digital-human-koubo
meta: {"stars": 660, "created": "2026-10-26", "pushed": "2026-10-26", "language": "TypeScript", "topics": []}
query: claude-code created:>{since} stars:>20

# Digital Human Koubo · AI 数字人口播

**One photo + one sentence → a finished talking-head video with a digital human.**
Script, lip-synced AI presenter, voice clean-up, captions, and pro-YouTuber-style packaging — fully automated by your AI agent.

**English** · [简体中文](README.zh-CN.md)

[](LICENSE)

[](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)

 

 

> This 27-second livestream ad has no real presenter. Face, voice, studio, captions and the price animation are all AI.
> The only input was one sentence: *"Use this digital human to make a 30-second livestream ad for the WorkBuddy course — 10 lessons, ¥99, was ¥999."*
> Total cost: **482 [Renoise](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official) credits**.

---

## Demos

Click a GIF (or "Watch") to play the full video. Every demo below was produced with this repo.

| | | |
|:---:|:---:|:---:|
|     |     |     |
| **Livestream sales ad** · 9:16 · 27 s Style B + depth-text price ¥999→¥99 [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/workbuddy-live-ad.mp4) | **Product recommendation** · 9:16 · 89 s Animated captions, emoji, picture-in-picture [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/renoise-koubo-huazi.mp4) | **Text behind the presenter** · 5 s Vision person matting, 3-layer composite [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/text-behind.mp4) |

| | |
|:---:|:---:|
|     |     |
| **Step-by-step tutorial** · 16:9 · 4:36 The digital human teaches how she was made (Style D) [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-ep2.mp4) | **Digital human, upgraded** · 16:9 · 5:55 Two presenters, 6 languages, 4 scenes, cat & dog (Style E) [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/tutorial-digital-human-upgrade.mp4) |
|     |     |
| **Launch breakdown** · 16:9 · 39 s Presenter on the side, code B-roll on the right (Style C) [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/memt-launch.mp4) | **Finance / tech explainer** · 16:9 · 2:21 Charts, documents, chapter cards (Style A) [▶ Watch](https://github.com/andyhuo520/digital-human-koubo/releases/download/v1.0.0/xiaolin-style-explainer.mp4) |

 
    
 Packaging component gallery  · 48 components · 2:40 ·  ▶ Watch 
 

> All presenters in the demos are AI digital humans and every video is labelled "内容由 AI 数字人演绎" (performed by an AI digital human). The male presenter is the author's own digital twin, made from his own photo.

---

## What it does

- **Digital human from one photo** — a fixed presenter (face, outfit, voice description, prompt template) stored in `persona.json`, so every video is the same person. Composite her into any scene (livestream studio, shop, classroom, Kyoto street) with GPT Image first, then make her talk.
- **Lip-synced talking clips** — the script is split into ≤ 15-second segments and generated with **Grok Video 1.5** through **[Renoise MCP](https://renoise.ai/mcp?utm_medium=xcom&utm_source=official)**. Other models (Wan 3.0, OmniHuman for your own recording) are documented.
- **Cost gate** — the agent always quotes *segments · seconds · credits · balance* first and waits for your "yes". It generates segment 1 for you to check before batching the rest.
- **Quality control** — every segment is transcribed with whisper and compared with the script, and 4 frame
