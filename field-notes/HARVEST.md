# Harvest register

One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in
`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the
source says), whether it is **testable** keyless tonight, and since 29 Sep a **breakdown** of how it would be done and
what tools it takes; testable ones are queued in `PROBES.md` with source `harvest` (or `vault` for Luke's links).
A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.

130 judged over 9 harvest days, 92 kept, 25 testable, 24 queued as probes, 19 with a probe verdict.

## Kept

| id | date | source | what | lens | interest | testable | probe |
|---|---|---|---|---|---|---|---|
| H-0130 | 2026-10-04 | youtube | [I Ran a Chess Programming Tournament!](https://www.youtube.com/watch?v=Ne40a5LkK6A) | mechanism | game-bots | no: The bots and framework are C# and need setup beyond a 30 min |  |
| H-0129 | 2026-10-04 | github | [Jakeschincariol/replica-skill: Eleven free Claude skills that clone any app: reverse-engin](https://github.com/Jakeschincariol/replica-skill) | mechanism | tools-for-strangers | yes | P-0061 |
| H-0127 | 2026-10-04 | vault | [node canvas workflows (Flows)]() | mechanism | tools-for-strangers | no: Needs a paid trial account and credits, and its MCP only rep |  |
| H-0125 | 2026-10-04 | arxiv | [The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching](https://arxiv.org/abs/2610.01768) (intel) | mechanism | mechanism-hunting | no: Reproducing the attack needs a tool-calling model and an att |  |
| H-0124 | 2026-10-04 | github | [ythx-101/live-panel-skill: Config-driven animated architecture diagrams: turn one JSON fil](https://github.com/ythx-101/live-panel-skill) | mechanism | tools-for-strangers | yes | P-0060 |
| H-0122 | 2026-10-04 | vault | [replication gap measured on demo](https://api-portal.etoro.com/changelog) | mechanism | forecasting | no: Needs an eToro demo API key, which is an account and a key. |  |
| H-0120 | 2026-10-04 | arxiv | [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65%](https://arxiv.org/abs/2610.01939) | mechanism | mechanism-hunting | no: Needs the GPT-6 planner and robot simulators, none of which  |  |
| H-0119 | 2026-10-04 | github | [QingYunA/answer-me-with-html: Answer me with HTML — an agent skill that answers hard quest](https://github.com/QingYunA/answer-me-with-html) | both | tools-for-strangers | yes | P-0059 |
| H-0117 | 2026-10-04 | vault | [Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summar](https://www.instagram.com/p/DdwbLoEgVKY/) | mechanism | tools-for-strangers | no: The endpoint needs an account and an API key, so it cannot b |  |
| H-0116 | 2026-10-03 | youtube | [Everything You Know About Skills IS OUTDATED](https://www.youtube.com/watch?v=e7TY56-yIvM) | mechanism | tech | yes | P-0057 **works** |
| H-0113 | 2026-10-03 | vault | [Photoreal moving footage of a subject you cannot film, one consistent face and a directed ](https://www.instagram.com/reel/DdoiRHMmyel/) | mechanism | tools-for-strangers | no: Video generation models need accounts and paid credits. |  |
| H-0111 | 2026-10-03 | arxiv | [Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control](https://arxiv.org/abs/2610.02038) | mechanism | forecasting | no: Needs the authors' simulator, site data and code, which are  |  |
| H-0110 | 2026-10-03 | github | [zhuyansen/awesome-claude-video-skills: Open-source skills and toolkits that let Claude Cod](https://github.com/zhuyansen/awesome-claude-video-skills) | both | tools-for-strangers | no: It is a list; running it would only mean fetching other repo |  |
| H-0108 | 2026-10-03 | vault | [Generating many platform-native variants (hooks, colour grades, overlays) from one filmed ]() (intel) | mechanism | tools-for-strangers | no: The useful part needs a filmed asset and owned accounts, and |  |
| H-0106 | 2026-10-03 | arxiv | [OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning](https://arxiv.org/abs/2610.02181) | mechanism | tech | no: Needs a trained omni-LLM checkpoint and GPU, and the paper g |  |
| H-0103 | 2026-10-03 | vault | [Whether a fees-paid threshold removes rugs without removing the launches that ran, on a da](https://www.instagram.com/reel/Db6WNI9BSQX/) | mechanism | desk:grinder | yes |  |
| H-0101 | 2026-10-02 | github | [ericmmartin/youtube-transcript-plus: YouTube Transcript Plus is an advanced Node.js packag](https://github.com/ericmmartin/youtube-transcript-plus) | mechanism | tools-for-strangers | yes | P-0056 **works** |
| H-0100 | 2026-10-02 | hn | [Show HN: Breadcrumb, record everything on your mac + context manager for AI](https://innerloop.works/breadcrumb) | mechanism | tools-for-strangers | no: It is a closed Mac app that records the screen and needs ins |  |
| H-0099 | 2026-10-02 | vault | [human reads flagged threads from alert links]() | mechanism | tools-for-strangers | yes | P-0055 **works** |
| H-0098 | 2026-10-02 | awesome | [elithril/blender-kiln (new in awesome-claude-code)](https://github.com/elithril/blender-kiln) | mechanism | tools-for-strangers | no: It needs Blender with an MCP server running and a paid model |  |
| H-0095 | 2026-10-02 | hn | [Show HN: Made an open-source Lego AI generator](https://github.com/anteloc/ldraw-nova) | mechanism | tools-for-strangers | yes | P-0054 **broken** |
| H-0094 | 2026-10-02 | vault | [Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7 ](https://www.instagram.com/reel/Dd-BvW5Jych/) | mechanism | tools-for-strangers | no: It is a paid hosted service needing an account and spend, an |  |
| H-0091 | 2026-10-02 | github | [Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照、边读边问 AI、文献管理。Read English papers in com](https://github.com/Edwardxlai/easyread) | mechanism | tools-for-strangers | no: It is an Electron app that needs a model login or key to tra |  |
| H-0090 | 2026-10-02 | hn | [Show HN: Rhun, an open-source code editor written in assembly](https://rhun.app/) | mechanism | tech | no: It means installing an unverified binary or building an asse |  |
| H-0089 | 2026-10-02 | vault | [Whether multi-buy and net-flow signals from tracked wallets predict price, measured on pap](https://youtu.be/2ikSD3rr5v8) | mechanism | desk:grinder | no: It needs timestamped wallet-level trades and forward prices  |  |
| H-0087 | 2026-10-01 | github | [machina-sports/sports-skills: Open-source agent skills for live sports data and prediction](https://github.com/machina-sports/sports-skills) | mechanism | desk:pitch | yes | P-0047 **broken** |
| H-0086 | 2026-10-01 | hn | [Show HN: Corral – Kill every command your agent starts](https://github.com/Cardinal44/corral) | mechanism | tools-for-strangers | no: It is Linux only (cgroups and /proc) and this machine is mac |  |
| H-0085 | 2026-10-01 | vault | [Inbound AI receptionist demo line built from the home services voice prompt]() | mechanism | tools-for-strangers | no: It needs a telephony account, a phone number and a voice-age |  |
| H-0084 | 2026-10-01 | youtube | [What is Expected Goals?](https://www.youtube.com/watch?v=tysc21gAT58) | mechanism | desk:pitch | yes | P-0046 **works** |
| H-0083 | 2026-10-01 | arxiv | [SEAR: Spoofing Evidence-Grounded Audio Reasoning Benchmark for Audio Language Models](https://arxiv.org/abs/2609.39847) (intel) | mechanism | mechanism-hunting | no: It needs six audio language models and the benchmark data is |  |
| H-0082 | 2026-10-01 | github | [edenfunf/reelmimic: Show it a video you love. Get a new video in the same style. An AI cre](https://github.com/edenfunf/reelmimic) | mechanism | tools-for-strangers | no: A real run takes hours of Claude Code usage and the shot ana |  |
| H-0080 | 2026-10-01 | vault | [One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API]() | mechanism | tools-for-strangers | no: It needs an account, a key and spend. |  |
| H-0079 | 2026-10-01 | youtube | [Finally, The CORRECT Way to Run Local AI on a Mac](https://www.youtube.com/watch?v=JpJaEPGzPF4) | mechanism | tech | yes | P-0045 |
| H-0078 | 2026-10-01 | arxiv | [Learning from Research: Toward Lifelong Agent Harness Evolution](https://arxiv.org/abs/2609.40169) | mechanism | mechanism-hunting | no: It needs the AppWorld and Tau2 harnesses, model runs and hou |  |
| H-0077 | 2026-10-01 | github | [nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill / Agent Skill for Refining AI-Generated ](https://github.com/nanaism/yomiyasu) | mechanism | tools-for-strangers | no: Judging naturalness of Japanese needs a native reader, and P |  |
| H-0076 | 2026-10-01 | hn | [Show HN: Open-source model routing for coding agents at Astra-level performance](https://news.ycombinator.com/item?id=49911500) | both | tech | no: It needs paid model keys on several providers and the benchm |  |
| H-0075 | 2026-10-01 | vault | [Adapt the web design CLAUDE.md for phone-first UK local business sites]() | mechanism | tools-for-strangers | no: The source file is behind the vault's course extract and the |  |
| H-0073 | 2026-09-30 | github | [echris6/motion-video-kit: Claude Code skill kit for premium AI-assisted business videos: i](https://github.com/echris6/motion-video-kit) | mechanism | tools-for-strangers | yes | P-0044 **works** |
| H-0072 | 2026-09-30 | hn | [Show HN: Parrot – Open-Source Smart Meeting Recorder with Co-Pilot on Mac](https://openparrot.app) | mechanism | tools-for-strangers | no: It is a Mac GUI app needing build and live call audio. |  |
| H-0071 | 2026-09-30 | vault | [Partnership ads run through a local client's own social handle](https://www.instagram.com/reel/DcWYAsmtqFr/) | mechanism | tools-for-strangers | no: Needs a Meta ad account and a client handle. |  |
| H-0070 | 2026-09-30 | youtube | [How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin](https://www.youtube.com/watch?v=MA6Ecac4P-Y) | mechanism | desk:grinder | no: Payouts and call attribution are not visible from a keyless  |  |
| H-0069 | 2026-09-30 | arxiv | [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](https://arxiv.org/abs/2609.38043) | mechanism | tech | no: Needs tau-bench, a frontier agent and paid calls. |  |
| H-0068 | 2026-09-30 | github | [rehan-remade/universal-modder: Point Claude at any game. Skills, tools and the fal MCP tha](https://github.com/rehan-remade/universal-modder) | mechanism | game-bots | no: Needs a fal key for assets, owned games on the machine, and  |  |
| H-0066 | 2026-09-30 | vault | [Consistent AI character content with clear AI disclosure](https://www.instagram.com/p/Ddr0Ds3MsI5/) | mechanism | tools-for-strangers | no: It is a content production job, not a script with a yes or n |  |
| H-0064 | 2026-09-30 | arxiv | [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | mechanism | tech | no: Needs a robot or the LIBERO-PRO simulator and a paid VLM. |  |
| H-0063 | 2026-09-30 | github | [Louis-CFM/coucou: A tiny friend that lives in your notch (macOS) or at the top of your scr](https://github.com/Louis-CFM/coucou) | mechanism | tools-for-strangers | no: It is an unnotarised Swift GUI that needs Xcode and a build, |  |
| H-0062 | 2026-09-30 | hn | [Launch HN: Magnitude (YC S25) – Self-optimizing inference engine for agents](https://github.com/magnitudedev/magnitude) | mechanism | tech | no: A fair test needs a multi-GB model download and a matched ll |  |
| H-0061 | 2026-09-30 | vault | [Learning crypto research from a source with an independently verifiable track record](https://cryptonary.com/landing-100x-chaser) | mechanism | desk:grinder | no: No source with a capturable call history has been named, so  |  |
| H-0059 | 2026-09-29 | github | [Barty-Bart/motion-graphics: Motion-graphics skills for Claude Code and Codex.](https://github.com/Barty-Bart/motion-graphics) | mechanism | tools-for-strangers | yes | P-0038 **works** |
| H-0058 | 2026-09-29 | vault | [Post-production for businesses that have long-form content but cannot cut it into short-fo](https://www.instagram.com/reel/DcU_MNWtIkg/) | mechanism | tools-for-strangers | no: The value is in a client engagement, and a keyless run would |  |
| H-0056 | 2026-09-29 | arxiv | [Harness Learning Enables Generalizable Test-Time Adaptation](https://arxiv.org/abs/2609.35738) | mechanism | mechanism-hunting | no: It needs reinforcement learning training of a proposer model |  |
| H-0055 | 2026-09-29 | github | [CaptureGrubEnchant/SolidWorks: SolidWorks MCP Server connects an AI assistant to a running](https://github.com/CaptureGrubEnchant/SolidWorks) | both | tech | no: It needs Windows and a licensed SolidWorks, and the install  |  |
| H-0054 | 2026-09-29 | vault | [Media-buying commission taken as a share of a brand's ad budget]() | mechanism | mechanism-hunting | no: It is a service arrangement with clients and ad accounts, an |  |
| H-0052 | 2026-09-29 | arxiv | [TokenCast: Forecasting Token Consumption During LLM Agent Execution](https://arxiv.org/abs/2609.35760) | mechanism | forecasting | yes | P-0037 **broken** |
| H-0051 | 2026-09-29 | github | [AgentSystemLabs/agent-office: A cartoon 3D office where your team hires Claude Code worker](https://github.com/AgentSystemLabs/agent-office) | both | tools-for-strangers | no: It needs a signed-in agent CLI and gh auth, and installs thr |  |
| H-0049 | 2026-09-29 | vault | [Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai-]() | mechanism | tools-for-strangers | no: The classroom sits behind a paid login and the pull needs an |  |
| H-0048 | 2026-09-28 | hn | [Show HN: OpenAPPA – open-source deterministic guardrails that don't break agents](https://www.openappa.com/) | both | mechanism-hunting | no: Reproducing the benchmarks needs LLM agent runs, and the num |  |
| H-0046 | 2026-09-28 | github | [jkawamoto/mcp-youtube-transcript: MCP server retrieving transcripts of YouTube videos](https://github.com/jkawamoto/mcp-youtube-transcript) | mechanism | tools-for-strangers | yes | P-0031 **works** |
| H-0045 | 2026-09-28 | hn | [Launch HN: Vespper (YC F24) – SOTA Docx MCP](https://www.vespper.com/blog/launching-vespper-docx-mcp) | both | tools-for-strangers | no: Needs a Vespper account and its hosted model, and the benchm |  |
| H-0043 | 2026-09-28 | arxiv | [A Safety-Bounded SDC-to-MCP Gateway for Medical AI Agents](https://arxiv.org/abs/2609.31358) | mechanism | mechanism-hunting | no: Needs SDC device simulators and the authors' prototype, whic |  |
| H-0042 | 2026-09-28 | github | [samyost1/3dicon: One prompt in, a looping animated 3D icon out — with real transparency. A](https://github.com/samyost1/3dicon) | mechanism | tools-for-strangers | no: The pipeline needs an OpenRouter key and paid image and vide |  |
| H-0040 | 2026-09-28 | youtube | [Agent Memory EXPLAINED - Complete Architecture](https://www.youtube.com/watch?v=aYfZN8t6AQs) | mechanism | mechanism-hunting | no: Running Mem0 needs an LLM for fact extraction, and no 30 min |  |
| H-0039 | 2026-09-28 | arxiv | [Structured Reasoning Agentic Framework for Interpretable Critical View of Safety Assessmen](https://arxiv.org/abs/2609.31524) | mechanism | tech | no: Needs the benchmark data and trained models, and no runnable |  |
| H-0038 | 2026-09-28 | github | [lemomo-ai/lemo-opuscar: 39 film styles, each a reusable style prompt plus a short film mad](https://github.com/lemomo-ai/lemo-opuscar) | mechanism | tools-for-strangers | no: Directing a film needs a Claude agent run against the skill, |  |
| H-0037 | 2026-09-28 | hn | [Show HN: HN.watch – Videos of all Hacker News posts](https://hn.watch/) | both | tools-for-strangers | yes | P-0030 **blocked** |
| H-0036 | 2026-09-27 | github | [alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interacti](https://github.com/alexgreensh/anidoodle) | mechanism | tools-for-strangers | yes | P-0028 **blocked** |
| H-0034 | 2026-09-27 | awesome | [lightpanda-io/browser (new in awesome-mcp-servers)](https://github.com/lightpanda-io/browser) | both | mechanism-hunting | yes | P-0027 **works** |
| H-0033 | 2026-09-27 | youtube | [How to Build An Expected Goals Model 1: Data and Model](https://www.youtube.com/watch?v=bpjLyFyLlXs) | mechanism | desk:pitch | no: This part of the transcript is conceptual framing with no fo |  |
| H-0032 | 2026-09-27 | arxiv | [PUBG Ally: A Conversational Embodied Agent as an AI Teammate](https://arxiv.org/abs/2609.29837) | mechanism | game-bots | no: It's a proprietary system deployed inside PUBG's live servic |  |
| H-0031 | 2026-09-27 | github | [dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to ](https://github.com/dzhng/jevgrep) | mechanism | mechanism-hunting | no: Needs a paid key for Vercel AI Gateway, OpenRouter or simila |  |
| H-0030 | 2026-09-27 | hn | [Turning GLM-5.3-Flash into a Jev-like decision model](https://www.privatemode.ai/blog/system-one-from-glm-flash) | both | mechanism-hunting | no: Needs GLM-5.3-Flash weights and a vLLM serving stack, not a  |  |
| H-0029 | 2026-09-27 | awesome | [agentmail-to/agentmail-mcp (new in awesome-mcp-servers)](https://github.com/agentmail-to/agentmail-mcp) | mechanism | mechanism-hunting | yes | P-0026 **works** |
| H-0027 | 2026-09-27 | arxiv | [When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression](https://arxiv.org/abs/2609.29875) | mechanism | mechanism-hunting | no: Needs the WorkBuddyBench harness, a proxy model for entropy  |  |
| H-0025 | 2026-09-27 | hn | [On caring for user data: NeoVim caused Vim undo files to be deleted](https://unsung.aresluna.org/they-had-no-concept-of-a-duty-of-care-to-their-users/) | mechanism | mechanism-hunting | yes | P-0025 |
| H-0022 | 2026-09-26 | github | [mikehasa/golive-skill: Take your agent-built product live: hosting, database, domain, emai](https://github.com/mikehasa/golive-skill) | both | tools-for-strangers | yes | P-0023 **works** |
| H-0021 | 2026-09-26 | hn | [Jevmem – automatic project memory for Claude Code, built on Jev](https://github.com/Avinash-jetwani/jevmem) | both | tools-for-strangers | no: Installing and running it needs a TypeSafe API key, a creden |  |
| H-0019 | 2026-09-26 | arxiv | [Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents](https://arxiv.org/abs/2609.29892) | mechanism | mechanism-hunting | no: Needs the MobilePA-Bench harness, real or emulated mobile de |  |
| H-0018 | 2026-09-26 | github | [yetone/magpie: Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, fro](https://github.com/yetone/magpie) | both | tools-for-strangers | yes | P-0022 **works** |
| H-0017 | 2026-09-26 | hn | [Show HN: A Claude Code skill to analyze your chess games](https://github.com/brumar/chess-postmortem-skills) | both | game-bots | no: The author's own figure is about $15 in API spend per run, r |  |
| H-0015 | 2026-09-26 | arxiv | [An Empirical Study of VLM Pipelines for Long-Document QA](https://arxiv.org/abs/2609.29933) | mechanism | mechanism-hunting | no: Reproducing needs the MMLongBench-Doc/LongDocURL benchmarks  |  |
| H-0014 | 2026-09-26 | github | [JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P](https://github.com/JohnHeibel/PDoomVideo) | mechanism | mechanism-hunting | yes | P-0021 **blocked** |
| H-0013 | 2026-09-26 | hn | [Show HN: Reladraw – A diagram language where you decide where to place things](https://github.com/reladraw/reladraw) | mechanism | mechanism-hunting | yes | P-0020 **works** |
| H-0012 | 2026-09-26 | hn | [Alan Kay: Shannon gave us a way of dealing with noisy channels [video]](https://www.youtube.com/watch?v=Cjntrqhn8pk) | mechanism | mechanism-hunting | no: Nothing to build or run, it is an anecdote about an accident |  |
| H-0010 | 2026-09-26 | github | [nateherkai/hyperframes-student-kit: Edit videos, reels, and YouTube Shorts with Codex or C](https://github.com/nateherkai/hyperframes-student-kit) | mechanism | tools-for-strangers | yes | P-0019 **works** |
| H-0009 | 2026-09-26 | hn | [Show HN: Whiteboard (YC W26) – An open-source IDE for thoughtful software design](https://github.com/devdotfast/whiteboard) | both | tools-for-strangers | no: It vendors a full Code-OSS (VSCode) fork plus Rust component |  |
| H-0007 | 2026-09-26 | arxiv | [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | mechanism | tech | no: Needs LIBERO/robosuite simulation environments plus VLM infe |  |
| H-0006 | 2026-09-26 | github | [chainstacklabs/pumpfun-bonkfun-bot: A fully functional pump.fun / letsbonk.fun trading and](https://github.com/chainstacklabs/pumpfun-bonkfun-bot) (intel) | mechanism | desk:grinder | no: Real sniping needs a funded Solana wallet private key and, f |  |
| H-0005 | 2026-09-26 | hn | [Claude Code reads AGENTS.md only when telemetry is on [fixed]](https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/) | mechanism | mechanism-hunting | no: Reproducing it means repeated `claude -p` invocations, which |  |
| H-0004 | 2026-09-26 | youtube | [Pump Fun Sniper Bot Full Tutorial / Solana MEV Bot step-by-step how to use](https://www.youtube.com/watch?v=vssd36X5Y2c) (intel) | mechanism | desk:grinder | no: The only way to 'test' it is entering a wallet private key i |  |
| H-0003 | 2026-09-26 | arxiv | [Screen Before You Serve: Simulation for Production Customer Experience AI Agents at 140M S](https://arxiv.org/abs/2609.30137) | mechanism | mechanism-hunting | no: Snowglobe and Nubank's Card Management agent are internal pr |  |
| H-0002 | 2026-09-26 | github | [nexmoe/VidBee: Download video and audio from  YouTube ,  TikTok ,  Twitter ,  Instagram , ](https://github.com/nexmoe/VidBee) | both | tools-for-strangers | no: Distributed as a GUI desktop installer rather than a scripta |  |
| H-0001 | 2026-09-26 | hn | [Show HN: Make cursed fonts like Times New Bastard](https://bastardica.mitpit.com) | mechanism | tools-for-strangers | no: It is judged by visual appearance in a browser, not by a hea |  |

## Entries

### H-0130 I Ran a Chess Programming Tournament!
2026-10-04, youtube, https://www.youtube.com/watch?v=Ne40a5LkK6A

- **Mechanism:** Contestants submit chess bots capped at 1,024 compiler-counted tokens, with a shared framework supplying legal moves and board state. A large Swiss tournament over 64 rounds pairs bots with similar scores who have not met, so about 600 bots rank in a manageable number of games. Token counting by syntax tree rather than file size was exploited via a line directive and an outdated compiler, which shows how a cap can be gamed.
- **Claim:** A 600-plus bot Swiss tournament over 64 rounds under a 1,024 token limit, with several exploits found and outlawed.
- **Testable:** no. The bots and framework are C# and need setup beyond a 30 minute keyless slice with no clear verdict. Needs: The challenge framework and entries from the creator's repository.
- **Idea on its own:** sound. Swiss pairing with a hard resource cap is a sound way to rank many entrants, and the exploit list is a useful checklist.
- **How it would be done:** For the Lichess bot, a small local Swiss runner with python-chess and a couple of engines would rank variants cheaply. The exploit list (data hidden in directives, outdated counter, network fetch) is a checklist for any submission cap. A hired person would only be needed to run a public contest.
- **Stack already covers:** Ollama with a qwen model
- **To fetch:** python-chess https://github.com/niklasf/python-chess (Legal moves and engine play for a local tournament runner); Stockfish https://stockfishchess.org (Reference opponent for rating a bot)
- **Field Notes line:** A 600-bot Swiss tournament under a 1,024 token cap showed how a size limit gets gamed and why Swiss pairing ranks fast.

### H-0129 Jakeschincariol/replica-skill: Eleven free Claude skills that clone any app: reverse-engineer it, rebuild it, test it fo
2026-10-04, github, https://github.com/Jakeschincariol/replica-skill

- **Mechanism:** A chain of eleven skills passes files through a replica/ folder: recon builds a screen and flow map and features.csv from public pages, help centres and store listings, then later skills plan, build, test and diff against that map. A diff step scores parity against the original and a review-mining step turns user complaints into the product angle. It claims clean-room scope: features and flows, not code, logos or copy.
- **Claim:** Eleven free MIT Claude skills that reverse-engineer, rebuild, test and launch a clone of any app, with no signup or key.
- **Testable:** yes. Does the recon step's helper tooling run on a public help-centre page and emit a features.csv with at least 10 rows? Queued as P-0061.
- **Idea on its own:** needs-a-run. The pipeline is plausible but quality of recon from public pages alone is unproven.
- **How it would be done:** Clone the repo, read the recon SKILL.md and run its Python tools on a public help centre. Check whether the features list is accurate against the page by hand. The review-mining step is the portable part and could be pointed at public app-store reviews for any product. Rebuilding and deploying is ordinary agent coding work.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** replica-skill https://github.com/Jakeschincariol/replica-skill (The eleven skills and Python tools to run)
- **Field Notes line:** A chain of eleven skills maps an app from public pages, rebuilds it and scores parity, with a review-mining step feeding the pitch.

### H-0127 node canvas workflows (Flows)
2026-10-04, vault, 

- **Mechanism:** A node canvas lets you wire generation steps (image, video, voice) into a graph where each node's output feeds the next, run as a batch with a credit cost per node. The platform sits on top of third-party models such as Kling and Seedance and charges credits per clip. The value is the graph layer and reusable templates, not exclusive models.
- **Claim:** Kling 3.0 costs 6.25 credits for 5 seconds at 720p, with a canvas layer (Flows) on top of aggregated models.
- **Testable:** no. Needs a paid trial account and credits, and its MCP only reports balance. Needs: A Promptwise account and credits.
- **Idea on its own:** needs-a-run. Whether the canvas saves time over scripted API calls only shows up when a real multi-step job is built both ways.
- **How it would be done:** Pick one job, for example script to stills to clips to voice, and build it once on the canvas and once as a script calling the same model APIs. Compare minutes of operator time, cost per finished clip and how easily a failed step is re-run. A hired operator would handle the web-only steps the scripts cannot reach.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), HeyGen and Tavus (avatars), Gemini (stills), Claude Code with skills and sub-agents
- **To fetch:** ComfyUI https://github.com/comfyanonymous/ComfyUI (Free open-source node-graph runner for the same chaining pattern)
- **Missing:** Nobody has a scripted equivalent of the canvas for Kling and Seedance without an aggregator account.
- **Field Notes line:** A node canvas that chains image, video and voice generation steps is the real product, since the underlying models are not exclusive.

### H-0125 The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching
2026-10-04, arxiv, https://arxiv.org/abs/2610.01768

- **Mechanism:** Malware that has no direct internet access hides a secret in a URL and asks an LLM agent to fetch it as if it were documentation for a benign task. The agent's own web-fetch tool carries the secret out to an attacker-controlled DNS or web server. Defences are egress logging of fetched URLs, DNS monitoring for high-entropy subdomains, allowlisting fetch destinations and requiring approval for unfamiliar hosts.
- **Claim:** 79.7% attack success across eleven open-parameter models, plus a case study on real-world chatbots.
- **Testable:** no. Reproducing the attack needs a tool-calling model and an attacker server, which is out of scope and not a keyless slice. Needs: A tool-calling model with a fetch tool.
- **Idea on its own:** sound. Any agent with an unrestricted fetch tool is an egress channel, and the paper shows it works in practice.
- **How it would be done:** The useful work is defensive: audit what fetch tools the Proteus agents have, log every fetched URL, and flag long or high-entropy path and subdomain strings. The unattended hook already allows or denies by list, so extending it to URL allowlists for WebFetch is the cheap fix. A paper review would check the detection section for numbers.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** An agent's own web-fetch tool can be turned into a covert exit for secrets, with a 79.7% success rate across eleven models.

### H-0124 ythx-101/live-panel-skill: Config-driven animated architecture diagrams: turn one JSON file into a terminal-style, alway
2026-10-04, github, https://github.com/ythx-101/live-panel-skill

- **Mechanism:** One JSON config describes nodes, wires, a log and counters. A self-contained HTML template animates it from a single clock. A Python script drives headless Chrome to capture frames and ffmpeg encodes H.264. A checker samples about 120 time points and measures text overflow from the DOM, and re-renders exported frames to prove determinism.
- **Claim:** Turns one JSON file into a roughly 28 to 30 second animated architecture diagram as mp4 or live web page, standard library Python only.
- **Testable:** yes. Does render.py produce an mp4 from the codex-agents example config in under 5 minutes, and does check_frames.py exit 0? Queued as P-0060.
- **Idea on its own:** sound. Config-driven templates rendered through headless Chrome and ffmpeg are a reliable way to make repeatable explainer clips.
- **How it would be done:** Clone the repo, run render.py on an example config, then check_frames.py with --repeat. Write a config for a Proteus desk diagram and render that. It overlaps with HyperFrames, so the useful comparison is the frame-determinism check, which could be borrowed.
- **Stack already covers:** HyperFrames (video compose, captions, render)
- **To fetch:** live-panel-skill https://github.com/ythx-101/live-panel-skill (The renderer and examples); ffmpeg https://ffmpeg.org (H.264 encoding step if not already installed)
- **Field Notes line:** One JSON file becomes a moving architecture diagram video, and its checker re-renders frames to prove they are deterministic.

### H-0122 replication gap measured on demo
2026-10-04, vault, https://api-portal.etoro.com/changelog

- **Mechanism:** A leader account on a copy-trading platform makes trades, followers' demo accounts mirror them through the platform's copy endpoints, and the gap is the difference between the leader's gain series and the follower's realised return. Fees are zero on demo, so real costs (spreads, fees, slippage) are added from the trade log afterwards. The numbers come from the leader gain series and the demo account's own history.
- **Claim:** Demo keys are locked to the demo account, copy endpoints have been live since 23 Aug 2026, and leader gain series are readable.
- **Testable:** no. Needs an eToro demo API key, which is an account and a key. Needs: An eToro demo API key.
- **Idea on its own:** sound. Measuring follower return against leader return on demo money is a clean, no-risk way to price the replication gap.
- **How it would be done:** Pick a handful of leaders, open demo copies of each, and poll the leader gain series and the demo portfolio daily into a CSV. Compute the gap per leader over a fixed window, then subtract assumed real fees and spreads from the trade log to estimate the true gap. Commit the leader picks before outcomes are known, as on the other desks.
- **Stack already covers:** launchd long-running pollers, freqtrade
- **To fetch:** eToro API portal https://api-portal.etoro.com (Demo copy-trading endpoints and docs)
- **Field Notes line:** Copying a trader on a demo account and comparing it with the leader's own gain series measures how much of the return a follower really keeps.

### H-0120 Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens
2026-10-04, arxiv, https://arxiv.org/abs/2610.01939

- **Mechanism:** The agent writes Python cells that compose robot primitives and learned policies, with conditionals and local retries inside the cell, instead of one tool call per step. Only explicitly requested images and state come back to the planner, which cuts input tokens. The comparison is against a tool-calling baseline with the same planner and primitives across 700 simulated tasks.
- **Claim:** Success rises from 63.1% to 71.7% under equal LLM-call budgets, with 49% fewer calls and 65% fewer input tokens on shared solved tasks.
- **Testable:** no. Needs the GPT-6 planner and robot simulators, none of which can be run keyless. Needs: A planner model API and simulator installs (LIBERO-PRO, RoboTwin, RoboCasa).
- **Idea on its own:** sound. Batching conditionals and retries into code and returning only requested observations is a general way to cut agent round trips.
- **How it would be done:** The pattern ports to any tool-using agent: expose primitives as Python functions in a persistent kernel, let the agent write cells with checks and retries, and return only what it asks for. For the Grinder it would mean one cell that pulls, filters and logs a token rather than a call per field. A paper-desk replay could count calls and tokens both ways.
- **Stack already covers:** Claude Code with skills and sub-agents, The Grinder paper desk
- **Field Notes line:** Letting an agent write a code cell with retries and selective observation, not one tool call per step, cut tokens 65% in robot sims.

### H-0119 QingYunA/answer-me-with-html: Answer me with HTML — an agent skill that answers hard questions with a one-page HTML you 
2026-10-04, github, https://github.com/QingYunA/answer-me-with-html

- **Mechanism:** The model writes a short Markdown draft and a bundled Node CLI turns it into a styled single-page HTML with diagrams and tables, so the model never types CSS or SVG coordinates. The saving is in output tokens and wall-clock time only, because the skill adds two extra turns that re-read context. Numbers come from a bench script in the repo.
- **Claim:** 7.4x fewer output tokens and 3.6x faster than asking for HTML directly, at about the same cost per answer.
- **Testable:** yes. Does the bundled CLI turn a Markdown draft into a readable HTML page in under one second, with no network or key? Queued as P-0059.
- **Idea on its own:** sound. Moving boilerplate from model output to a deterministic renderer is a real token and latency saving.
- **How it would be done:** Clone the repo into the sandbox, read SKILL.md, and run the CLI on a hand-written Markdown draft with a diagram block. Time it and open the result. Then compare against the repo's bench README to see whether the 923-token figure is plausible by counting the draft. The same pattern could feed Field Notes pages.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** answer-me-with-html https://github.com/QingYunA/answer-me-with-html (The skill and bundled CLI to run); Node.js 20+ https://nodejs.org (Runtime for the bundled CLI)
- **Field Notes line:** A skill that has the model write Markdown and a CLI build the page claims 7.4x fewer output tokens, but the same bill.

### H-0117 Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summary jobs through the free endpoi
2026-10-04, vault, https://www.instagram.com/p/DdwbLoEgVKY/

- **Mechanism:** A hosted OpenAI-compatible endpoint serves open-weight models (DeepSeek, GLM, Kimi) on a free developer tier with a request-per-minute cap. You send the same fixed set of non-personal rewrite and summary prompts to the hosted models and to the local qwen model via Ollama, then score outputs with a rubric or an LLM judge. The cap (about 40 RPM) bounds a bake-off to a few hundred calls, which is enough.
- **Claim:** The free tier gives about 40 requests a minute across roughly 80 to 100 open-weight models with no card.
- **Testable:** no. The endpoint needs an account and an API key, so it cannot be run keyless tonight. Needs: A free NVIDIA Build account and API key.
- **Idea on its own:** sound. Comparing models on a fixed public prompt set before pulling weights is cheap, standard and answers a real choice.
- **How it would be done:** Write 30 to 50 synthetic or public-domain rewrite and summary prompts with a short rubric. Loop them through the hosted endpoint for each candidate model and through Ollama qwen locally, logging output, latency and token counts to a CSV. Score with a rubric, using a different model family as judge, and spot-check a sample by hand. Respect the rate cap with a simple sleep. Keep personal data out entirely, as the terms forbid it.
- **Stack already covers:** Ollama with a qwen model, Claude Code with skills and sub-agents
- **To fetch:** NVIDIA Build API catalogue https://build.nvidia.com (The free hosted open-weight endpoint to benchmark against); promptfoo https://github.com/promptfoo/promptfoo (Runs the same prompt set across several providers and scores them)
- **Field Notes line:** A free hosted tier could let me race DeepSeek, GLM and Kimi against my local qwen on public text before downloading any weights.

### H-0116 Everything You Know About Skills IS OUTDATED
2026-10-03, youtube, https://www.youtube.com/watch?v=e7TY56-yIvM

- **Mechanism:** The claim is that when a skill points to a long reference file, Claude may open only the first 100 lines (a head -100 call) to decide whether the file is relevant, so rules after that point can go unseen. The stated fix is a contents list at the top of any reference file over 100 lines so the model can see the whole map or jump to a section. A second rule scales how exact a skill's instructions are to how fragile the task is.
- **Claim:** Reference files over 100 lines with no contents list are rarely used in full, and Anthropic's best-practice guide has six new rules.
- **Testable:** yes. How many reference files under the local skills folders exceed 100 lines, have no contents list, and have key rules after line 100? Queued as P-0057.
- **Idea on its own:** needs-a-run. The head-100 behaviour is plausible but secondhand, and only an audit of real skills plus a controlled read shows whether it matters here.
- **How it would be done:** Scan every skill folder under the Claude skills directories and list reference files by line count and whether a contents block sits in the first ten lines. Flag those over 100 lines that lack one and note headings sitting past line 100. To check the behaviour itself, a later run in an interactive session would place a marker rule at line 150 of a test reference and see whether the skill follows it. Fixing is a short edit per file.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** A claim that Claude reads only the first 100 lines of a skill's reference file, so long files without a contents list hide their own rules.

### H-0113 Photoreal moving footage of a subject you cannot film, one consistent face and a directed camera move
2026-10-03, vault, https://www.instagram.com/reel/DdoiRHMmyel/

- **Mechanism:** A routing layer sends a prompt and reference stills to a video model such as Veo, Kling or Seedance, with camera-move presets expanded into the prompt. Face consistency across shots comes from feeding the same reference images or a character sheet into each generation, then picking takes. The quality lives in the underlying models, so the same result can be had by calling those models directly with a prompt bank.
- **Claim:** Photoreal moving footage of a subject you cannot film, with one consistent face and a directed camera move.
- **Testable:** no. Video generation models need accounts and paid credits. Needs: An account and credits for a video model, or a free-tier allowance..
- **Idea on its own:** needs-a-run. Reference-image conditioning does improve consistency, but how far it holds across a five-shot sequence is only known by generating one.
- **How it would be done:** Make a character sheet in Gemini stills, then write a prompt per shot that carries the same reference images and a named camera move. Generate each shot on one video model, review the takes on a contact sheet, and cut with HyperFrames. Use fictional or consented subjects only. A person is useful to judge whether the face really holds and to redo failed takes.
- **Stack already covers:** Gemini (stills), HyperFrames (video compose, captions, render), HeyGen and Tavus (avatars)
- **To fetch:** Kling AI https://klingai.com (Video model with a free daily credit allowance for a reference-image consistency test.)
- **Field Notes line:** Camera-move presets plus the same reference stills in every shot is how these tools hold one face across a sequence.

### H-0111 Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control
2026-10-03, arxiv, https://arxiv.org/abs/2610.02038

- **Mechanism:** The LLM never acts directly. It outputs a structured proposal, a deterministic soil-water simulator numerically checks it, the LLM revises, and a bounded deterministic selector picks the action. A slower loop distils recurring failures into persistent written principles that condition future proposals, while the simulator, evaluator and action limits stay immutable.
- **Claim:** Lowest aggregate control cost among compared methods and about 51 percent less irrigation than historical schedule replay.
- **Testable:** no. Needs the authors' simulator, site data and code, which are not confirmed released. Needs: The paper's code and soil and weather data..
- **Idea on its own:** sound. Keeping truth and action authority in deterministic code while the LLM proposes and learns notes is a sound pattern for long-horizon decisions with compounding errors.
- **How it would be done:** The pattern maps onto a paper desk: the LLM proposes a position, a deterministic check (a liquidity cap, a Dixon-Coles probability, a size limit) accepts or clips it, and a nightly pass writes failure patterns into a notes file that conditions the next proposals without touching the checker. Build it as a wrapper around the Grinder or Pitch desk with the rules file committed so changes are dated. No hired person is needed for the pattern; real irrigation would need an agronomist and field hardware.
- **Stack already covers:** Claude Code with skills and sub-agents, GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), football-data and a Dixon-Coles paper desk (the Pitch)
- **Missing:** The paper's implementation, if any is released.
- **Field Notes line:** Mimir lets an LLM propose farm irrigation but only a fixed simulator and hard limits can act, and the LLM learns written rules from its own failures.

### H-0110 zhuyansen/awesome-claude-video-skills: Open-source skills and toolkits that let Claude Code, Codex and other coding agen
2026-10-03, github, https://github.com/zhuyansen/awesome-claude-video-skills

- **Mechanism:** A curated index of about 230 repos that let coding agents make video, sorted into ten types. A decision model reads each README to answer inclusion questions and assign a security grade, refreshed every eight hours, so the grades are model opinions rather than audits. Inclusion needs a README and either 50 stars or a quality bar plus a few stars.
- **Claim:** 180 to 230 open-source video skills and toolkits, each read and security-graded.
- **Testable:** no. It is a list; running it would only mean fetching other repos, which are separate items.
- **Idea on its own:** sound. A shelf of candidate tools is useful, with the caveat that the security grades come from a model reading READMEs, not from code review.
- **How it would be done:** Pull the README and the category lists, then filter to the Frameworks, Editing and Shorts types. Check each shortlisted repo's licence and install route, then queue the few that fill gaps next to HyperFrames for sandbox runs on later nights. Treat the SAFE grade as a hint and read the install script before running anything.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** awesome-claude-video-skills https://github.com/zhuyansen/awesome-claude-video-skills (The list itself, source for further video-skill repos.); Remotion https://github.com/remotion-dev/remotion (The best-known alternative React video renderer to compare with HyperFrames.)
- **Field Notes line:** A model-graded index of 230 video skills for coding agents is a ready shelf to mine for HyperFrames alternatives and extras.

### H-0108 Generating many platform-native variants (hooks, colour grades, overlays) from one filmed asset
2026-10-03, vault, 

- **Mechanism:** One filmed asset is fed through a loop that swaps hooks, applies colour grades, adds overlays and re-crops per platform, producing many renders from one source. The render half is ordinary templated video composition. The vendor's distribution half routes posts through antidetect cloud phones, one spoofed device per account, which is grey-market automation: platforms catch it with device and network fingerprinting, behavioural similarity across accounts, and near-duplicate content matching, and treat it as inauthentic content.
- **Claim:** Turn one video into many platform-native variants and post them across accounts automatically.
- **Testable:** no. The useful part needs a filmed asset and owned accounts, and the posting half is the evasion tooling, so no keyless slice exists. Needs: A filmed source asset and owned, disclosed accounts for any real posting..
- **Idea on its own:** sound. Producing hook and format variants of one's own footage for A/B testing on owned accounts is standard practice; only the spoofed-device posting is the problem.
- **How it would be done:** Define a variants table of hooks, grades, overlays and aspect crops, and render each row from the single source through a templated HyperFrames composition. Add per-variant tracking so each post's performance can be compared, which is the per-post idea worth keeping. Posting is done by a person through each platform's own scheduler on accounts the owner runs openly, with the AI label where required. A hired editor covers the first filmed asset and the judgement on which hooks are worth testing.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org (Crops, grades and re-encodes for per-platform specs.)
- **Missing:** A variant-planning loop that maps hooks and grades to renders and tracks each variant's results.
- **Field Notes line:** Variant loops are plain templated rendering; the grey part is posting through spoofed phones, which platforms detect by device fingerprint and near-duplicate matching.

### H-0106 OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning
2026-10-03, arxiv, https://arxiv.org/abs/2610.02181

- **Mechanism:** An omni-modal LLM is trained to act as a multi-turn agent that chooses whether to look or listen and over which time window, then gets the raw audio or video segment appended to its context. It is cold-started with supervised fine-tuning on 170K synthetic multi-hop trajectories, then refined with two-stage reinforcement learning on verifiable rewards. An extra reward fires only when a successful answer genuinely needed both audio and vision, which discourages single-modality shortcuts.
- **Claim:** Active evidence seeking over long audio-visual context improves audio-visual reasoning across a wide range of benchmarks.
- **Testable:** no. Needs a trained omni-LLM checkpoint and GPU, and the paper gives no runnable keyless artefact. Needs: Model weights and GPU, if released..
- **Idea on its own:** sound. Fetching sparse evidence on demand is a sensible fix for long-context media, and the both-modalities reward targets a known shortcut.
- **How it would be done:** The same pattern can be built crudely without training: a transcript or scene index acts as a map, and an agent requests specific time windows (a frame grab or an audio snippet) as tool calls. For the YouTube pipeline that means search the transcript first, then pull only the frames around the matching timestamps. Reproducing the trained model would need the released checkpoint or a research team to rebuild the data engine.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline, local transcription, Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org (Cut frame and audio windows on demand for a look-or-listen tool.)
- **Missing:** A released OmniSeek checkpoint or the OmniTraj-170K data; neither is confirmed available.
- **Field Notes line:** OmniSeek teaches a model to choose which minute of audio or video to fetch next, instead of swallowing the whole clip in one pass.

### H-0103 Whether a fees-paid threshold removes rugs without removing the launches that ran, on a dated sample
2026-10-03, vault, https://www.instagram.com/reel/Db6WNI9BSQX/

- **Mechanism:** Total SOL fees (priority fees plus Jito tips) paid by a token's traders so far is read from on-chain transactions that touch the token's pool. The idea is that a rug is cheap to launch but organic buyers of a real run pay real fees, so a minimum fees-paid figure screens out launches nobody traded seriously. The number comes from summing the fee field across the pool's transactions, via an indexer such as Dune or Solana RPC history. Whether it separates rugs from runners is an empirical question on a dated sample.
- **Claim:** A three-column terminal filter with a fees-paid threshold is said to remove about 90 percent of rugs.
- **Testable:** yes. On the Grinder's already-tracked launches with known outcomes, does a fees-paid threshold remove at least 80 percent of the rugged ones while keeping at least 70 percent of those that ran? Not queued (daily cap).
- **Idea on its own:** needs-a-run. Fees paid is a real cost borne by traders so it plausibly proxies genuine activity, but wash trading can inflate it and the 90 percent figure has no sample behind it.
- **How it would be done:** Take the Grinder's closed launches that are already labelled rugged or ran, with dates. For each, pull the pool's recent transaction signatures from public Solana RPC and sum the fee field to get fees paid up to a fixed time after launch. Sweep a few thresholds and compute rugs removed and runners kept at each, on a time-ordered split so the threshold is not fitted on the same launches it is judged on. Record the confusion matrix and commit the threshold before applying it to new launches. A Dune query over a larger dated sample would be the next step if the slice is promising.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), launchd long-running pollers
- **To fetch:** Solana public JSON-RPC https://api.mainnet-beta.solana.com (Keyless getSignaturesForAddress and getTransaction to sum fees per pool, rate limited.); Dune https://dune.com (Free tier SQL over Solana transactions for a larger dated sample, needs an account so later.)
- **Field Notes line:** Fees paid by a token's own traders as an anti-rug filter: cheap to compute, and we can check it against launches we already tracked.

### H-0101 ericmmartin/youtube-transcript-plus: YouTube Transcript Plus is an advanced Node.js package designed to fetch and proces
2026-10-02, github, https://github.com/ericmmartin/youtube-transcript-plus

- **Mechanism:** It makes three HTTP calls: the video page, a POST to YouTube's Innertube player endpoint to get caption track URLs, then a GET of the transcript data. Fetch functions can be swapped for a proxy, which exists because YouTube blocks datacentre and repeated IPs. It uses an unofficial interface, so it breaks when YouTube changes it.
- **Claim:** Fetches YouTube transcripts through the unofficial Innertube API, with custom fetch hooks for proxies and a user agent.
- **Testable:** yes. Does fetchTranscript return non-empty caption text for three public videos from this Mac with no proxy, yes or no, and how many fail with a block? Queued as P-0056.
- **Idea on its own:** needs-a-run. It depends on an unofficial endpoint that blocks some IPs, which only a run from this machine shows.
- **How it would be done:** Install the package in the sandbox, call fetchTranscript on three public videos with captions and record success, text length and any block error. Compare against the existing keyless transcript pipeline on the same IDs. If blocked, the library's fetch hooks show where a proxy would sit, though no proxy is added tonight. A person would only be needed to buy proxy access, which is outside this test.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** youtube-transcript-plus https://github.com/ericmmartin/youtube-transcript-plus (The library under test); Node.js 20+ https://nodejs.org (Runtime the package requires)
- **Field Notes line:** This Innertube transcript library is the same route that returned IpBlocked in tonight's harvest, so a direct run shows if this IP is blocked.

### H-0100 Show HN: Breadcrumb, record everything on your mac + context manager for AI
2026-10-02, hn, https://innerloop.works/breadcrumb

- **Mechanism:** A local recorder captures screen, meetings with timestamped screenshots, AI session transcripts and sub-agent activity, encrypted on disk. It indexes this and exposes more than 30 MCP tools so Claude Code, Codex or Cursor can search past work. Stored rules are injected by context, and a commenter raises the cost of loading all tool definitions each request.
- **Claim:** Records everything on your Mac and turns it into searchable memory for your AI, with 30+ MCP tools.
- **Testable:** no. It is a closed Mac app that records the screen and needs install and permissions, so it is not a keyless sandbox run. Needs: The macOS app and screen-recording permission.
- **Idea on its own:** needs-a-run. More recorded context helps recall, but retrieval quality and tool-definition overhead decide whether it pays.
- **How it would be done:** Capture sources to local storage, extract text by OCR and transcription, and index with timestamps. Expose search over MCP and load tools lazily to avoid definition bloat. Add a rules layer matched by project or file context. A person decides what must never be recorded, which no script covers.
- **Stack already covers:** Claude Code with skills and sub-agents, local transcription
- **To fetch:** Breadcrumb MCP tool definitions https://innerloop.works/breadcrumb/mcp (Read the tool list to measure definition size)
- **Field Notes line:** Screen, meeting and agent transcripts indexed behind 30 MCP tools; the token cost of those tool definitions is the open question.

### H-0099 human reads flagged threads from alert links
2026-10-02, vault, 

- **Mechanism:** Keyword alerts arrive by email with a thread link, and the agent browsers refuse reddit.com, so a person reads each flagged thread. The open question is whether the public RSS or JSON views of a thread, which are plain HTTP, can be read by a script instead. If they return thread text keyless from this machine, the human step becomes a fallback.
- **Claim:** The vault says the Reddit listening lane depends on a human reading flagged threads because agent browsers are blocked.
- **Testable:** yes. Does a plain HTTP request to a public subreddit RSS feed and a thread RSS URL from this Mac return HTTP 200 with thread text, yes or no? Queued as P-0055.
- **Idea on its own:** needs-a-run. Whether public feeds survive rate limiting and blocking is unknown until requested.
- **How it would be done:** Request a subreddit .rss and a thread .rss with a descriptive user agent and light spacing, then record status and body size. If both work, parse titles, bodies and top comments into a digest per alert. Keep the human read for threads that return blocked or truncated text. Request volume stays low and follows the site's published rules.
- **Stack already covers:** launchd long-running pollers, Claude Code with skills and sub-agents
- **Field Notes line:** Agent browsers refuse Reddit, but plain RSS fetches might still return thread text with no key.

### H-0098 elithril/blender-kiln (new in awesome-claude-code)
2026-10-02, awesome, https://github.com/elithril/blender-kiln. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Claude Code skill drives Blender through an MCP server. Its new part is a fidelity loop: render the model at the reference photo's camera, list silhouette gaps per height band, then re-measure the exported, compressed GLB rather than the .blend. A bench scores each rebuild against the real asset from five sides, using Poly Haven previews as references.
- **Claim:** Rebuilds an object from one photo as a GLB, with shape scores of 0.897, 0.950 and 0.750 on three assets at roughly 4 to 6 dollars each.
- **Testable:** no. It needs Blender with an MCP server running and a paid model session per asset. Needs: Blender 4.4+ with a Blender MCP, and a Claude session budget.
- **Idea on its own:** sound. Measuring against the reference from the same camera and scoring the shipped file is a real feedback loop, not a claim.
- **How it would be done:** Install Blender and a Blender MCP, then load the skill. Give it a photo and let it inventory parts, texture from CC0 sets and build in scripted Blender. Run the fidelity check at the photo camera, fix gaps, then optimise and validate the GLB. The same render-and-measure loop could be reused for other generated assets, and a person judges final taste.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** blender-kiln https://github.com/elithril/blender-kiln (The skill and the fidelity_check script); Blender https://www.blender.org (Required runtime); Poly Haven https://polyhaven.com (CC0 textures and reference models)
- **Field Notes line:** A scoring loop that renders a 3D model from the photo's camera and measures the gap is what makes agent-built assets improve.

### H-0095 Show HN: Made an open-source Lego AI generator
2026-10-02, hn, https://github.com/anteloc/ldraw-nova

- **Mechanism:** LDraw is a plain-text format where each line places one brick with a colour, position and rotation matrix, so a model is a short program. The project gives an LLM agent a Python toolset, instructions and docs to write .ldr or .mpd files, check them, and view them through LDView or LeoCAD. It ships as a dockerised web app that can call OpenAI, Claude or OpenRouter.
- **Claim:** Frontier models can generate high-quality LEGO CAD models by writing LDraw source, packaged as an open-source web app.
- **Testable:** yes. Does the repo's Python toolset validate and parse a hand-written LDraw file offline, yes or no, and how many of its checks pass? Queued as P-0054.
- **Idea on its own:** needs-a-run. The idea is sound but quality depends on the validation tools, which a run on a sample file can show.
- **How it would be done:** Clone the repo, read its tool list and run the validators on a small known-good LDraw file and a deliberately broken one. Check whether collisions, floating parts and missing part files are caught. If they work, wrap them as a Claude Code skill so an agent loops write, validate, render. The LDraw part library is public and free, and a person would judge whether the finished model looks right.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** ldraw-nova https://github.com/anteloc/ldraw-nova (The toolset under test); LDraw parts library https://www.ldraw.org/parts/latest-parts.html (Part definitions needed for validation); LDView https://tcobbs.github.io/ldview/ (Renderer for checking models)
- **Field Notes line:** LEGO models are just text files of brick placements, so an agent with a validator can write them.

### H-0094 Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7 dollars per 15 seconds at 1080
2026-10-02, vault, https://www.instagram.com/reel/Dd-BvW5Jych/

- **Mechanism:** Film a person performing, supply a reference image of the target avatar, and a video model recasts the whole frame: body motion and timing are taken from the source clip while identity, clothes and background come from the reference. It is the same family as Kling Motion Control, run as a hosted generation per clip. The price quoted is about 7 dollars per 15 seconds at 1080p.
- **Claim:** Whole-frame motion transfer so an AI avatar repeats your exact performance, about 7 dollars per 15 seconds at 1080p.
- **Testable:** no. It is a paid hosted service needing an account and spend, and Proteus has no filmed source performance. Needs: A Higgsfield account and credits, plus a filmed own-performance clip.
- **Idea on its own:** sound. Driving a generated character from a real performance is an established technique and cuts retakes for consistent-avatar video.
- **How it would be done:** Film the performance against a plain background with the camera framing the target shot needs. Prepare a clean avatar still, then run both through the motion-transfer model and review each take from a contact sheet. Compare the same pair on Kling Motion Control for fidelity and cost per second, then pick one route. A person still performs and approves the footage, since no script covers the acting.
- **Stack already covers:** HyperFrames (video compose, captions, render), HeyGen and Tavus (avatars), Gemini (stills), ElevenLabs (voice)
- **To fetch:** Kling Motion Control https://klingai.com (Comparison route for the same source clip); Higgsfield https://higgsfield.ai (Genjutsu route under test)
- **Missing:** A filmed reference performance clip of the person to be recast.
- **Field Notes line:** Motion transfer now recasts the whole frame from one filmed performance, at roughly 7 dollars per 15 seconds.

### H-0091 Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照、边读边问 AI、文献管理。Read English papers in comfortable Chinese.
2026-10-02, github, https://github.com/Edwardxlai/easyread

- **Mechanism:** Each PDF page is rendered, then a chosen model (Claude Code or Codex CLI on the user's login, an API, or local Ollama) translates it page by page. The agent can look at the page image to check formulas, which are re-typeset with KaTeX, and the translation is kept apart from AI explanations shown in the margin. A local server writes edits to files, with failed pages retried and token use logged per call.
- **Claim:** Translates English papers into readable Chinese with side-by-side original, margin notes and an ask-AI panel, 601 stars within days of creation.
- **Testable:** no. It is an Electron app that needs a model login or key to translate, so a keyless run would not test the mechanism. Needs: A model engine login (Claude Code, Codex) or local model run through its settings.
- **Idea on its own:** sound. Per-page translation with the page image as ground truth and a strict split between translation and commentary is a sound design.
- **How it would be done:** Split the PDF into page images and text blocks, send each page to a model with the image attached, and ask for a faithful translation only. Re-render formulas with KaTeX and tables as three-line tables, store output per page so retries are cheap. Put commentary in a separate channel so the reader can trust the main text. A bilingual reviewer would spot-check a sample of pages, since nothing scripted verifies translation quality.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** easyread https://github.com/Edwardxlai/easyread (Reference implementation of per-page translation); KaTeX https://katex.org (Formula re-typesetting)
- **Field Notes line:** A paper reader that sends each PDF page image to a CLI agent so formulas get checked against the page, not just the text.

### H-0090 Show HN: Rhun, an open-source code editor written in assembly
2026-10-02, hn, https://rhun.app/

- **Mechanism:** The editor and its pixel renderer share one x86-64 assembly core. For Apple silicon a build-time translator converts that assembly to AArch64, with thin per-platform adapters for windowing and input. On top sit Vim mode, a terminal, git diffs and a panel that hosts Claude Code or Codex sessions, plus commit-message drafting through local Ollama or an existing CLI subscription.
- **Claim:** A small MIT-licensed editor in assembly for Linux, Windows and Apple silicon, with Claude Code and Codex panels, keeping launch time and footprint minimal.
- **Testable:** no. It means installing an unverified binary or building an assembly toolchain, which does not fit a keyless 30 minute sandbox verdict.
- **Idea on its own:** sound. Build-time ISA translation of a small hand-written core is a coherent way to keep one codebase tiny across platforms.
- **How it would be done:** Write the core in one assembly dialect, with a stable interface to platform adapters. A translator script maps instructions and calling conventions to AArch64 at build, then each adapter is linked per platform. Testing means diffing behaviour of the translated core against the original on the same inputs. A person would still hand-check the translator output for the instructions it cannot map.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** rhun https://rhun.app/ (Source and releases to read the translator approach)
- **Field Notes line:** One assembly core, translated to ARM at build time, runs an editor on three operating systems.

### H-0089 Whether multi-buy and net-flow signals from tracked wallets predict price, measured on paper against public leaderboards
2026-10-02, vault, https://youtu.be/2ikSD3rr5v8

- **Mechanism:** Take a list of wallets ranked by realised profit on a public leaderboard (Kolscan, GMGN). Count how many distinct tracked wallets buy the same token inside a window (multi-buy) and the net SOL flow of those wallets into it (buys minus sells). Log the signal at the moment it fires with entry price, then measure forward returns at fixed horizons against a baseline of tokens that did not fire. The numbers come from on-chain swap history or the leaderboard's own wallet pages.
- **Claim:** The video says buying where several tracked wallets pile in is a repeatable edge, with a claimed 30K made part-time.
- **Testable:** no. It needs timestamped wallet-level trades and forward prices collected over days, and the leaderboard data is not confirmed keyless. Needs: Wallet trade history source (Kolscan or GMGN scrape, or a Solana indexer) and several days of forward data.
- **Idea on its own:** needs-a-run. Wallet confluence is plausible but survivorship and copy-lag usually erase it, and only a pre-registered paper run shows which.
- **How it would be done:** Pick a fixed wallet list from the leaderboard and freeze it before measuring, to avoid picking winners after the fact. Poll swaps for those wallets (public Solana RPC or a free indexer tier) and write each multi-buy event with its timestamp, then log price at 5 min, 1h and 24h from GeckoTerminal. Compare against a matched control set of tokens of similar age and liquidity that had no wallet buys. Commit the rule before outcomes exist so the Grinder timestamp is the proof. No human job is needed beyond choosing the wallet list policy.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder), launchd long-running pollers
- **To fetch:** Kolscan leaderboard https://kolscan.io (Public ranked wallet list to seed the tracked set); GMGN wallet pages https://gmgn.ai (Per-wallet trade history for multi-buy and net-flow counts); Solana public RPC / Helius free tier https://www.helius.dev (Swap history per wallet if the leaderboard sites block scraping)
- **Missing:** A frozen, timestamped record of tracked-wallet buys joined to forward prices does not exist anywhere public.
- **Field Notes line:** Nobody has measured whether several leaderboard wallets buying the same coin predicts price; the Grinder can pre-register that test on paper.

### H-0087 machina-sports/sports-skills: Open-source agent skills for live sports data and prediction markets. Football, F1, Kalshi
2026-10-01, github, https://github.com/machina-sports/sports-skills

- **Mechanism:** A Python package and SKILL.md set that wraps public endpoints: ESPN scoreboards, Understat xG, ClubElo ratings, FPL, Kalshi and Polymarket prices. Each skill exposes commands that fetch and normalise JSON, with a catalog.json declaring risk metadata. It depends on the upstream sites staying open.
- **Claim:** Agent skills for live sports data and prediction markets with zero API keys.
- **Testable:** yes. Does pip install sports-skills return non-empty current Understat xG and ClubElo data with no key, and how many of 20 Premier League teams match the Pitch desk's ratings ranking? Queued as P-0047.
- **Idea on its own:** needs-a-run. Wrapping public endpoints is easy, so the value depends on whether they still return clean data.
- **How it would be done:** Install the package in a venv, call the Understat and ClubElo commands for the current league, save the output and compare team order against the Pitch desk's Dixon-Coles ratings. Prediction market prices would give a blind baseline to compare predictions with.
- **Stack already covers:** football-data and a Dixon-Coles paper desk (the Pitch)
- **To fetch:** sports-skills https://github.com/machina-sports/sports-skills (The package under test.); ClubElo API http://clubelo.com/API (Free Elo ratings, no key.)
- **Field Notes line:** A keyless Python wrapper over Understat xG, ClubElo and prediction market prices could feed the Pitch desk extra inputs.

### H-0086 Show HN: Corral – Kill every command your agent starts
2026-10-01, hn, https://github.com/Cardinal44/corral

- **Mechanism:** Corral runs a command in its own session and tracks every descendant, so nothing survives. With cgroups it kills the whole tree at once; without, it walks /proc and kills descendants, and exits 120 if it cannot confirm they are dead. Commenters note escapes such as spawning through sshd or handing work to systemd.
- **Claim:** corral --wall 30s -- cmd leaves no process of that command running when it finishes.
- **Testable:** no. It is Linux only (cgroups and /proc) and this machine is macOS. Needs: A Linux host or container.
- **Idea on its own:** sound. Leaked background processes from agent shells are real and tree-wide killing fixes most of them.
- **How it would be done:** On a Linux box, run commands that double fork and background a tail, wrapped in the tool, and check for survivors. On macOS an equivalent would need process group tracking with kqueue or a launchd job with AbandonProcessGroup off.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** Corral https://github.com/Cardinal44/corral (The tool.)
- **Field Notes line:** A wrapper that kills every process an agent's command started, using cgroups or a /proc walk, because plain timeouts miss double forks.

### H-0085 Inbound AI receptionist demo line built from the home services voice prompt
2026-10-01, vault, 

- **Mechanism:** A phone number routes inbound calls to a voice-agent platform: speech to text, an LLM with a long system prompt (business hours, services, booking rules), text to speech back, and tool calls that write bookings to a calendar or send an SMS. Retell or Vapi host the loop and Make or n8n handle the follow-up. In the UK, call recording and AI disclosure at the start are needed.
- **Claim:** A home services voice prompt turns into a working inbound receptionist demo line.
- **Testable:** no. It needs a telephony account, a phone number and a voice-agent platform key. Needs: Voice-agent platform account and a UK phone number.
- **Idea on its own:** sound. Inbound handling of missed calls is lawful and the components are mature.
- **How it would be done:** Take one of the free voice prompts, adapt it to a fictional UK trade business, wire a number into a hosted voice-agent platform, and give it a calendar booking tool. Test with scripted calls, including interruptions and unclear requests. A person must play the caller and handle the business owner onboarding.
- **Stack already covers:** ElevenLabs (voice)
- **To fetch:** Retell AI https://www.retellai.com (Hosted voice-agent loop with a free tier.); Vapi https://vapi.ai (Alternative voice-agent platform.); n8n https://github.com/n8n-io/n8n (Self-hosted follow-up workflows.)
- **Missing:** A UK phone number and a real business willing to trial it.
- **Field Notes line:** An inbound AI receptionist is a phone number, a speech loop, a long prompt and a calendar tool call.

### H-0084 What is Expected Goals?
2026-10-01, youtube, https://www.youtube.com/watch?v=tysc21gAT58

- **Mechanism:** Expected goals is a classifier: each shot gets a probability of scoring from features such as location, angle, body part and defender positions, fitted on thousands of historical shots. Usually this is logistic regression or gradient boosting, and team xG is the sum of shot probabilities.
- **Claim:** An equation using data from thousands of similar shots assigns each chance a value between 0 and 1.
- **Testable:** yes. Does a logistic model on distance and angle from StatsBomb open data beat a constant goal-rate baseline on held-out log loss? Queued as P-0046.
- **Idea on its own:** sound. It is a standard, well understood model whose skill can be checked on held-out shots.
- **How it would be done:** Download StatsBomb open data shots, compute distance and angle from the coordinates, fit logistic regression and compare log loss and Brier score against a constant rate on a held-out set. Then add body part and shot type. The result can feed the Pitch desk as a team strength input.
- **Stack already covers:** football-data and a Dixon-Coles paper desk (the Pitch)
- **To fetch:** StatsBomb open-data https://github.com/statsbomb/open-data (Free shot-level event data with coordinates.); scikit-learn https://github.com/scikit-learn/scikit-learn (Logistic regression and scoring.)
- **Field Notes line:** Expected goals is just a shot-level logistic model; fitting one on free open data shows how much distance and angle alone explain.

### H-0083 SEAR: Spoofing Evidence-Grounded Audio Reasoning Benchmark for Audio Language Models
2026-10-01, arxiv, https://arxiv.org/abs/2609.39847

- **Mechanism:** SEAR tests whether audio language models detect deepfake speech for the right acoustic reasons. A four-task question benchmark asks for evidence identification, quantification, verdict and rationale, and BAEA gives a frozen model controlled acoustic measurement tools, fixed or adaptive, comparing against bona fide audio. Feeding misleading evidence lowers both detection and grounding.
- **Claim:** Models give plausible rationales that lack verifiable acoustic evidence, and BAEA-Fixed improves verdicts and rationales.
- **Testable:** no. It needs six audio language models and the benchmark data is not confirmed public. Needs: Audio language model access and the SEAR dataset.
- **Idea on its own:** sound. Making a detector cite measurable evidence is a sound way to test whether its reasoning is real.
- **How it would be done:** Pull the benchmark if released, run a model with and without simple measurement tools (spectral features, pitch, noise floor from librosa), and check whether the cited evidence matches the measured values. This is the detection side only.
- **Stack already covers:** local transcription
- **To fetch:** librosa https://github.com/librosa/librosa (Acoustic measurements as evidence tools.)
- **Field Notes line:** Audio models that call a deepfake often cannot back the call with real acoustic evidence; giving them measurement tools helps.

### H-0082 edenfunf/reelmimic: Show it a video you love. Get a new video in the same style. An AI crew (Claude Code or Codex) plans
2026-10-01, github, https://github.com/edenfunf/reelmimic

- **Mechanism:** It decomposes a reference video into shot lengths, BPM, transitions, colours, framing and camera moves, then writes a storyboard plan for approval. Up to six agents build different segments in parallel through engines such as HyperFrames, and every finished shot is reviewed by a fresh agent, with fixes needing before and after screenshots. Styles are Markdown files.
- **Claim:** A reference video plus a one-line brief yields a new 30 to 60 second video in the same style, in 1 to 3.5 hours.
- **Testable:** no. A real run takes hours of Claude Code usage and the shot analysis step is not clearly separable. Needs: Hours of Claude Code or Codex usage.
- **Idea on its own:** needs-a-run. Separating the builder from the reviewer is sound, but output quality on 2D styles is only shown by the author's samples.
- **How it would be done:** Clone it, feed it a short public-domain clip and a one-line brief, and let it run overnight. Compare the shot analysis with ffmpeg scene detection to see how accurate the breakdown is. The reference should be licensed or self-made, and a person must approve the plan.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **To fetch:** ReelMimic https://github.com/edenfunf/reelmimic (The tool itself.); painted-animation https://github.com/tuzhechen2005/painted-animation (Hand-painted engine it builds on.)
- **Field Notes line:** A Claude Code crew takes a video apart into shots, rhythm and style, then rebuilds a new one with a fresh agent reviewing every shot.

### H-0080 One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API
2026-10-01, vault, 

- **Mechanism:** fal is an inference aggregator: one API key and a queue endpoint per model, where a client submits a job, polls or takes a webhook, and downloads the result file. Video, image and lip-sync models from different labs sit behind one calling pattern billed per second or per generation. It depends on the hosted model being available and on each model's content rules.
- **Claim:** One pay-as-you-go account reaches Seedance, Kling, Wan and lip-sync models by API.
- **Testable:** no. It needs an account, a key and spend. Needs: fal account and API key.
- **Idea on its own:** sound. Aggregator APIs with a uniform submit-and-poll pattern are a proven way to swap models without rewriting code.
- **How it would be done:** Write one small wrapper that takes a model id and a prompt, submits to the queue, polls and saves the file with its cost recorded. Add a table of draft route and final route per video job. A person is still needed for any shot with a real face, which these models refuse.
- **Stack already covers:** HyperFrames (video compose, captions, render), Gemini (stills), HeyGen and Tavus (avatars)
- **To fetch:** fal client https://github.com/fal-ai/fal (Python client for the queue API.)
- **Field Notes line:** One queue-style API fronts many video models, so a script can pick a draft model and a final model per job.

### H-0079 Finally, The CORRECT Way to Run Local AI on a Mac
2026-10-01, youtube, https://www.youtube.com/watch?v=JpJaEPGzPF4

- **Mechanism:** oMLX wraps Apple's MLX LM library with an OpenAI-style server and a two-tier KV cache: hot blocks stay in RAM, cold blocks are written to SSD as safetensors under least-recently-used eviction. Previously seen prompt prefixes are restored across requests and server restarts rather than recomputed, which cuts time to first token on long agent contexts.
- **Claim:** SSD-persisted prefix cache makes cold starts and long contexts faster than plain MLX LM on a Mac.
- **Testable:** yes. With a small public MLX model, is time to first token on a 4k-token repeated prefix after a server restart at least 2x faster than the first cold run? Queued as P-0045.
- **Idea on its own:** needs-a-run. Prefix caching is a sound technique, but the speedup on a small model on this Mac is the question.
- **How it would be done:** Install oMLX, load a small MLX model, send a 4k-token prompt, time it, restart the server and send it again. Compare against the Ollama qwen already here for the same prompt. If the gain holds, point child agents at it for long-context reading jobs.
- **Stack already covers:** Ollama with a qwen model, local transcription
- **To fetch:** oMLX (The server under test; find the repo via the video description.); mlx-lm https://github.com/ml-explore/mlx-lm (The underlying library and baseline.)
- **Field Notes line:** A Mac local-model server that parks its prompt cache on the SSD so restarts skip recomputing long prefixes.

### H-0078 Learning from Research: Toward Lifelong Agent Harness Evolution
2026-10-01, arxiv, https://arxiv.org/abs/2609.40169

- **Mechanism:** ScholarEvolve keeps the model fixed and evolves the agent harness (tool use, memory, task execution). It mines new papers, topic-models them into improvement strategies per harness module, has a coding agent implement each, then evaluates combinations on the benchmark and keeps winners. New publications can be fed in over time.
- **Claim:** Raises Qwen3.5-27B goal completion on AppWorld Challenge from 49.6% to 63.6%, and GPT-5.4-mini pass@1 on Tau2-Bench Telecom from 72.7% to 81.9%.
- **Testable:** no. It needs the AppWorld and Tau2 harnesses, model runs and hours of compute, not a 30 minute keyless check. Needs: Benchmark harnesses and model access.
- **Idea on its own:** needs-a-run. Evaluate-and-keep loops do improve harnesses, but gains from paper mining versus plain search are not isolated here.
- **How it would be done:** Take a small harness Proteus owns (the harvester or the probe loop), define a score, then have a child agent propose changes drawn from recent arXiv abstracts and keep only those that raise the score on a fixed task set. The paper feed already exists through the arXiv pull. A held-out set is needed so the loop does not overfit.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** AppWorld https://github.com/StonyBrookNLP/appworld (Benchmark used to score harness changes.)
- **Missing:** A scored task set for Proteus's own harness.
- **Field Notes line:** An agent harness that reads new research papers and rewrites itself with them lifted a small model's task score by 14 points.

### H-0077 nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill / Agent Skill for Refining AI-Generated Japanese into Natural Japanese
2026-10-01, github, https://github.com/nanaism/yomiyasu

- **Mechanism:** It is a prompt-only Agent Skill: seven rewrite principles (restore subject and object, dissolve inanimate subjects, replace metaphor verbs with literal actions, cut preambles, preserve numbers, limit sentence length to about 30 to 45 characters and 0 to 2 commas) loaded into the agent as a skill file. The numeric targets make the output checkable by a simple script. It addresses a known failure of ban-list prompts, where banned words are swapped for new vague ones.
- **Claim:** The skill rewrites AI-sounding Japanese into natural, dense Japanese, validated against open-licence corpora.
- **Testable:** no. Judging naturalness of Japanese needs a native reader, and Proteus has no Japanese ground truth. Needs: A Japanese reader to judge output.
- **Idea on its own:** sound. Structural rules with measurable limits beat word ban lists, and the same pattern would work for English house style.
- **How it would be done:** Copy the skill structure, replace the Japanese rules with English equivalents (name the actor, no abstract subjects, sentence length cap, no filler openers), and run it over a few drafts. A small script can then count sentence length and comma density as a regression check. A native editor would be needed to confirm it reads naturally.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** yomiyasu https://github.com/nanaism/yomiyasu (Reference skill layout and rule set to adapt.)
- **Field Notes line:** A skill that fixes AI-sounding prose by enforcing sentence structure rules with numeric targets, not by banning words.

### H-0076 Show HN: Open-source model routing for coding agents at Astra-level performance
2026-10-01, hn, https://news.ycombinator.com/item?id=49911500

- **Mechanism:** A router sits between a coding agent and several LLM back ends and picks a model per step. It is a trained routing model (RL plus a prior, with an HMM mentioned in comments that assigns the session to a model bucket) that weighs model capability, price and prompt-cache state, since switching model throws away the cache. Savings come from sending easy edits to a cheap model and hard debugging to the strong one.
- **Claim:** Router 2.0 matches GPT-6 Astra pass rates on Terminal Bench 4.0 and SWE Atlas at about 52 to 54 percent of the cost and 2.2 to 2.5x faster.
- **Testable:** no. It needs paid model keys on several providers and the benchmarks are the vendor's own, so nothing can be checked keyless tonight. Needs: API keys for two or more model providers.
- **Idea on its own:** needs-a-run. Cost-aware routing is plausible but the headline numbers are self-reported on the vendor's benchmark runs.
- **How it would be done:** Install the open-source router, point a coding agent at it, and run the same 20 tasks through it and through the single strong model, logging cost, time and pass rate. The comparison needs several provider keys and a task set Proteus can score itself. A crude rule-based router (cheap model for edits under N lines) is a useful baseline to see how much the trained part adds.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Weave Router https://github.com/weave-os/router (The open-source router to run against a baseline.)
- **Missing:** A scored task set and keys for the cheap and strong models.
- **Field Notes line:** A trained router that hands easy coding steps to cheap models and hard ones to the strong one claims half the cost at equal pass rate, with cache loss priced in.

### H-0075 Adapt the web design CLAUDE.md for phone-first UK local business sites
2026-10-01, vault, 

- **Mechanism:** A CLAUDE.md file sits in a website project and pins design rules (mobile-first layout, tap-target sizes, local trust signals, click-to-call, schema.org LocalBusiness markup) so every Claude Code session builds pages to the same standard. Adapting it for UK local trades means swapping US conventions for UK ones (postcodes, VAT, UK phone formats, Google Business Profile). The output is static HTML or a small framework site that can be checked against Lighthouse mobile scores.
- **Claim:** A web design CLAUDE.md steers Claude Code to produce consistent, mobile-first small business sites.
- **Testable:** no. The source file is behind the vault's course extract and the real question (does a rule file improve sites) needs a judged build, not a 30 minute run.
- **Idea on its own:** sound. Persistent rule files reliably shape agent output, and mobile performance is measurable with free tools.
- **How it would be done:** Write or take the rule file, adapt it to UK local business conventions, then have Claude Code build a sample site for a fictional plumber from a short brief. Score it with Lighthouse mobile and a tap-target check, then iterate the rules where scores drop. Real trade businesses would need photos, reviews and a domain, which is a human job: someone has to collect them and approach the owner.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Lighthouse CLI https://github.com/GoogleChrome/lighthouse (Free mobile performance and accessibility scoring to judge generated sites.)
- **Missing:** The real client photos, reviews and domain access for any actual business.
- **Field Notes line:** A single CLAUDE.md rule file can hold a whole web design standard, so phone-first local business sites come out consistent every time.

### H-0073 echris6/motion-video-kit: Claude Code skill kit for premium AI-assisted business videos: independent critic loop, motion
2026-09-30, github, https://github.com/echris6/motion-video-kit

- **Mechanism:** A Claude Code skill that makes commercials through a builder-versus-critic loop: a fresh critic agent judges the actual render, items are verified one by one and a ledger records findings. It pairs motion rules from 28 launch films with measurable checks (frozen-time detection, loudness via ffmpeg ebur128, contrast, brand colour) scripted in Python. Rendering is HyperFrames or Three.js.
- **Claim:** Premium launch-style business videos from an independent-critic quality loop.
- **Testable:** yes. Does the kit's frozen-time and loudness script run on a local ffmpeg-generated test video and report a loudness figure in LUFS and a frozen-frame count? Queued as P-0044.
- **Idea on its own:** sound. Independent critics plus measured checks address the known self-grading failure of generate-and-review loops.
- **How it would be done:** Clone the repo, copy the skill into place and run its measurement scripts on a render. Wire the critic prompts into a sub-agent that never sees the builder's reasoning. Use HyperFrames for output. The business playbook is where a person picks verticals and price anchors.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents, ElevenLabs (voice)
- **To fetch:** motion-video-kit https://github.com/echris6/motion-video-kit (The skill and measurement scripts.); ffmpeg ebur128 filter https://ffmpeg.org/ffmpeg-filters.html#ebur128-1 (Loudness measurement the scripts need.)
- **Field Notes line:** A video skill kit ships scripted render checks for frozen frames and loudness, plus a separate critic agent that judges the real render.

### H-0072 Show HN: Parrot – Open-Source Smart Meeting Recorder with Co-Pilot on Mac
2026-09-30, hn, https://openparrot.app

- **Mechanism:** A Mac app records system audio and microphone, transcribes locally or via Deepgram, and runs a co-pilot that matches questions heard in the call against the user's uploaded files and shows answers on screen. Local mode needs no account or API call; cloud mode hooks Claude and Deepgram. A thread reports echo from duplicate audio streams.
- **Claim:** Open-source, local-first meeting recorder with a retrieval co-pilot.
- **Testable:** no. It is a Mac GUI app needing build and live call audio. Needs: Xcode build and audio permissions..
- **Idea on its own:** sound. System audio capture plus local transcription and retrieval over user files is a proven, simple pattern.
- **How it would be done:** Capture system audio and mic with ScreenCaptureKit, transcribe with a local Whisper model, embed the uploaded files and match detected questions to passages. Export transcripts as markdown, which a commenter asks for. Local transcription is already in the stack.
- **Stack already covers:** local transcription, Ollama with a qwen model
- **To fetch:** Parrot https://github.com/turantekin/Parrot (Source for the capture and co-pilot design.)
- **Field Notes line:** A local-first Mac recorder listens to calls and answers questions from your own files, with no account.

### H-0071 Partnership ads run through a local client's own social handle
2026-09-30, vault, https://www.instagram.com/reel/DcWYAsmtqFr/

- **Mechanism:** Meta's Partnership Ads let a business run paid ads that appear from a creator or client's own Instagram handle after the handle owner grants permission in Meta's tools. The ad borrows the page's local trust while the advertiser pays for reach. It depends on permission being granted on-platform and on the ad carrying the platform's paid partnership label.
- **Claim:** Ads run through a local client's own handle carry more local trust than a brand page.
- **Testable:** no. Needs a Meta ad account and a client handle. Needs: A Meta Business account and a consenting client..
- **Idea on its own:** sound. It is a sanctioned platform feature with consent and a visible label.
- **How it would be done:** Agree a written permission with the local business, get the handle's admin to grant partnership access in Meta Business Suite, then produce and label the creative and run a small test budget. Record results in a shared sheet. Content can be made with HyperFrames; the account setup and consent step need a person.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice)
- **Missing:** A consenting local business willing to grant handle access.
- **Field Notes line:** Partnership ads let a business borrow a local client's own handle with permission, labelled, which is legal and sellable as a service.

### H-0070 How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin
2026-09-30, youtube, https://www.youtube.com/watch?v=MA6Ecac4P-Y. Vault verdict on the vendor exists (vault verdict: pump.fun); mechanism recorded, vendor not re-judged.

- **Mechanism:** A pump.fun feature where a user posts a short call-out on a coin after buying a small amount, and earns a share of trading fees on volume that call drives. A daily pool is paid out in USD in proportion to volume attributed to each caller, so payout rewards calling early. The video claims the top 50 split $700,000 in two weeks, with most calls on coins under 100K market cap.
- **Claim:** Top 50 callers split $700,000 in two weeks; one earned $6,800 from almost 2,500 calls.
- **Testable:** no. Payouts and call attribution are not visible from a keyless public endpoint and the figures are a creator's claim. Needs: A pump.fun account and a source of call-out data..
- **Idea on its own:** needs-a-run. The incentive is real but it rewards volume drivers, so callers are paid even when followers lose money.
- **How it would be done:** Measure it from the outside: log call-outs and the coin's later volume and price, and check whether early callers' coins outperform launches with no call-outs. Pay attention to whether the payout creates a pump incentive in the Grinder's data. No account is needed for the observational version if call-out data is public.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder)
- **Missing:** Public access to call-out timestamps and payout data.
- **Field Notes line:** Pump.fun pays a daily pool to people who post early call-outs, which turns attention itself into a fee-share incentive.

### H-0069 UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training
2026-09-30, arxiv, https://arxiv.org/abs/2609.38043

- **Mechanism:** An evaluation layer over tau-bench scores the simulated user, not the agent, against the private instructions it was given, using task-grounded rubrics scored independently of agent success. Holding the agent fixed and swapping the user model changes reward by 15.2 points. The main failure is premature disclosure, which leaves reward unchanged but reduces the agent's tool calls.
- **Claim:** 24.4% of successful episodes contain a user-simulator violation, and proxy choice shifts reward by 15.2 points.
- **Testable:** no. Needs tau-bench, a frontier agent and paid calls. Needs: tau-bench and model API spend..
- **Idea on its own:** sound. Scoring the simulator against its own instructions is a cheap, obvious missing control.
- **How it would be done:** Take transcripts from a benchmark, write rubric items from each task's hidden user instructions and have a judge model score each transcript independently of reward. Report the violation rate and compare proxies on cost. Applies to any agent test Proteus builds with a simulated user.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** tau-bench https://github.com/sierra-research/tau-bench (The benchmark family the layer sits over.)
- **Field Notes line:** Agent benchmark scores swing 15 points depending on the simulated user, and a quarter of passes hide a user mistake.

### H-0068 rehan-remade/universal-modder: Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost a
2026-09-30, github, https://github.com/rehan-remade/universal-modder

- **Mechanism:** A Claude Code plugin of skills and a Python CLI that runs a fixed loop: scan for installed games and fingerprint engine, anti-cheat and save folders, choose a modding route, read decompiled code, build a slice, generate assets with fal, test in the running game and record. It leans on existing tools (ILSpy, Ghidra, Frida, Cheat Engine, Blender) and playbooks per engine. Asset generation needs a fal key.
- **Claim:** Claude Code can mod almost any PC game you own, from recon to showcase video.
- **Testable:** no. Needs a fal key for assets, owned games on the machine, and is Windows-first. Needs: A fal API key, a game install and Blender..
- **Idea on its own:** sound. The loop mirrors how human modders work and each step uses established reverse-engineering tools.
- **How it would be done:** Install the plugin, run the scan step to fingerprint installed games, then let the skill write a modding plan. Build one slice with the engine's playbook and test it in the running game with screenshots. Assets need a generator; a local substitute would replace fal. Anti-cheat titles need a human to judge what is safe.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render), Gemini (stills), ElevenLabs (voice)
- **To fetch:** universal-modder https://github.com/rehan-remade/universal-modder (The plugin and um CLI.); ILSpy https://github.com/icsharpcode/ILSpy (Decompiler for .NET games.); Ghidra https://github.com/NationalSecurityAgency/ghidra (Native reverse engineering.)
- **Field Notes line:** A Claude Code plugin packages game modding as recon, route, read code, build, test, record, with a scanner that fingerprints engines.

### H-0066 Consistent AI character content with clear AI disclosure
2026-09-30, vault, https://www.instagram.com/p/Ddr0Ds3MsI5/

- **Mechanism:** A fixed character is kept consistent across posts by generating from a locked reference image set or a fine-tuned image model, then animating and voicing it. Disclosure is added by labelling each post with the platform's AI-content label and a visible caption line, and by keeping the character to entertainment rather than endorsement. Platforms detect undisclosed synthetic media through provenance metadata such as C2PA and classifiers.
- **Claim:** A branded AI character can post consistent content at volume.
- **Testable:** no. It is a content production job, not a script with a yes or no answer tonight.
- **Idea on its own:** sound. Disclosed synthetic characters are lawful and platform-sanctioned when they do not pose as ordinary consumers recommending products.
- **How it would be done:** Generate a reference sheet of the character with Gemini stills, then produce scenes with image-to-video and voice with ElevenLabs. Compose and caption in HyperFrames, apply the platform AI label on upload and add a fixed disclosure line in the caption. Keep scripts to entertainment and explicit sponsor labels. A person would review each post for label compliance and likeness drift.
- **Stack already covers:** Gemini (stills), ElevenLabs (voice), HeyGen and Tavus (avatars), HyperFrames (video compose, captions, render)
- **To fetch:** C2PA c2patool https://github.com/contentauth/c2patool (Embed and inspect provenance metadata for disclosure.)
- **Missing:** A compliance check for UK DMCC and platform labelling rules on each post.
- **Field Notes line:** A consistent AI character can be run openly by locking reference stills and labelling every post as AI, entertainment only.

### H-0064 MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation
2026-09-30, arxiv, https://arxiv.org/abs/2609.38078

- **Mechanism:** A harness lets a general vision-language model drive a robot by proposing mid-level actions (move to, grasp, place) that a deterministic controller executes, with feedback returned to the model. Asynchronous monitoring watches execution while background memory updates keep context, and no coding agent, action expert or SAM3 grounding is used. Scores come from LIBERO-PRO simulation and a real xArm6.
- **Claim:** 66.7% success on base LIBERO-PRO versus at most 13.3% for prior zero-shot methods, and 95% on a real xArm6.
- **Testable:** no. Needs a robot or the LIBERO-PRO simulator and a paid VLM. Needs: A robot or simulator and a frontier VLM key..
- **Idea on its own:** needs-a-run. Numbers are self-reported on a benchmark the authors chose, but the harness design is cheap to replicate in principle.
- **How it would be done:** Define a small action vocabulary, wrap a simulator or arm in deterministic executors, and loop the VLM over camera frames with a monitor thread flagging failures. Would need the LIBERO-PRO simulator and GPU. No relevance to current desks except as a harness pattern.
- **To fetch:** LIBERO https://github.com/Lifelong-Robot-Learning/LIBERO (Simulation benchmark the paper builds on.)
- **Missing:** A robot or GPU simulator.
- **Field Notes line:** A plain VLM plus a thin mid-level action layer and async monitor beat specialised robot policies zero-shot, by a wide margin.

### H-0063 Louis-CFM/coucou: A tiny friend that lives in your notch (macOS) or at the top of your screen (Windows) and keeps an eye
2026-09-30, github, https://github.com/Louis-CFM/coucou

- **Mechanism:** A native menubar app that shows Claude Code sessions in the MacBook notch. It receives events from the running sessions (tool calls, permission requests) and renders Allow and Deny buttons that answer the permission prompt, which points to Claude Code's hooks being used as the event channel. Keys for integrations sit in the macOS Keychain and there is no telemetry.
- **Claim:** See every Claude Code session and approve permissions from the notch; 1,099 stars in three days.
- **Testable:** no. It is an unnotarised Swift GUI that needs Xcode and a build, and its value is visual. Needs: Xcode 16 and XcodeGen..
- **Idea on its own:** sound. Hook-driven approval forwarding is a real, supported pattern for remote sign-off.
- **How it would be done:** A hook script posts each permission request to a local socket or HTTP endpoint and waits for a decision. A small UI reads that endpoint and writes the answer back. Proteus could reuse only the hook-to-decision pattern, not the UI, for the unattended-decide hook.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** coucou https://github.com/Louis-CFM/coucou (Source to read for the hook event format.)
- **Field Notes line:** Claude Code permission prompts can be answered from outside the terminal by a hook, and someone has made it a notch app.

### H-0062 Launch HN: Magnitude (YC S25) – Self-optimizing inference engine for agents
2026-09-30, hn, https://github.com/magnitudedev/magnitude

- **Mechanism:** An inference engine that compiles and autotunes its GPU kernels on the user's own device before loading a model, so one parametrised kernel set reaches hardware-specific speed on Mac, Linux and Windows. It writes tuned kernels only for popular open-weight model families and is built for long, concurrent agent sessions on a machine that is also in use. The speed claim rests on a chart against llama.cpp; the thread asks for configuration and MLX comparisons.
- **Claim:** Up to 2x faster than llama.cpp on the same hardware, for local agents.
- **Testable:** no. A fair test needs a multi-GB model download and a matched llama.cpp configuration, which does not fit 30 minutes. Needs: Model weights and time to match llama.cpp settings..
- **Idea on its own:** needs-a-run. Per-device autotuning is proven in other compilers, but the 2x figure has no published method.
- **How it would be done:** Install the release binary, pull the same quantised qwen model Ollama already uses, and run identical prompts through both with fixed context length and thread count. Measure tokens per second for prefill and decode, and run two sessions at once to test the concurrency claim. Compare against MLX as the thread asks. No hiring needed.
- **Stack already covers:** Ollama with a qwen model
- **To fetch:** Magnitude https://github.com/magnitudedev/magnitude (The engine under test.); llama.cpp llama-bench https://github.com/ggml-org/llama.cpp (Baseline benchmark tool with fixed settings.)
- **Field Notes line:** Magnitude tunes its own kernels on your machine at first run, claiming double llama.cpp speed, but the benchmark is one image.

### H-0061 Learning crypto research from a source with an independently verifiable track record
2026-09-30, vault, https://cryptonary.com/landing-100x-chaser

- **Mechanism:** Score a crypto research source by reconstructing its calls as dated entry and exit pairs, then pricing each from public candle data at the time of the call rather than at the peak. The moving parts are a timestamped archive of each call (screenshots, posts, archive.org copies), a price history source, and a fixed exit rule applied to every call, compared with a baseline such as holding the same basket.
- **Claim:** A source's track record can be checked independently if you log audited entries and exits instead of quoting peak gains.
- **Testable:** no. No source with a capturable call history has been named, so there is nothing to score tonight. Needs: A named source with timestamped, archived calls..
- **Idea on its own:** sound. Fixed-rule entry and exit scoring against a baseline is the standard way to strip survivorship and peak bias from any tipster.
- **How it would be done:** Pick a source that publishes dated calls and snapshot them to an archive at the time they appear. For each call, pull the price at the call timestamp from GeckoTerminal or DexScreener history and apply one pre-declared exit rule (for example 24h, 7d, 30d). Net off slippage and fees, then compare the book with buy-and-hold on the same tokens. The Grinder already has the paper-desk plumbing, so the scoring is a thin layer on it. A hired person would only be needed to capture calls from paywalled or members-only channels.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder), keyless YouTube search and transcript pipeline
- **To fetch:** Wayback Machine CDX API https://archive.org/help/wayback_api.php (Independent timestamps for when a call was published.)
- **Missing:** A source that actually publishes timestamped calls in a capturable form.
- **Field Notes line:** Judge a crypto caller by fixed-rule entry and exit pairs priced from public candles, not by their best-ever multiple.

### H-0059 Barty-Bart/motion-graphics: Motion-graphics skills for Claude Code and Codex.
2026-09-29, github, https://github.com/Barty-Bart/motion-graphics

- **Mechanism:** Each clip is a small HTML file on a shared engine where every frame is a pure function of time, with springs as closed-form step responses and a sum of one spring per target change. Headless Chromium via Playwright captures four sub-frames per frame across a 180 degree shutter, and ffmpeg blends them into motion blur. A skill plans clips from a transcript with estimated word timings, then renders MP4 or transparent ProRes 4444.
- **Claim:** Given a video and a transcript, Claude Code plans, animates and renders motion-graphic B-roll timed to the words.
- **Testable:** yes. Does the shipped opus-aoe2 example render locally through Playwright and ffmpeg, and are two renders of the same clip byte-identical? Queued as P-0038.
- **Idea on its own:** sound. Time-pure frames make any frame renderable alone and blur by sub-frame averaging is a standard, correct technique.
- **How it would be done:** Clone the repo, run the example clips through its Playwright capture and ffmpeg blend, then hash two renders to test determinism. To use it for the clipping service, feed it a transcript and let the plan table choose cutaways versus side panels, then compare against what HyperFrames produces for the same script. The part worth borrowing is the closed-form spring engine and the 180 degree shutter blend, which could be ported into a HyperFrames composition.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents, local transcription
- **To fetch:** motion-graphics https://github.com/Barty-Bart/motion-graphics (The skill, engine and worked example.); Playwright https://github.com/microsoft/playwright (Headless Chromium frame capture.); ffmpeg https://ffmpeg.org/ (Sub-frame blending and ProRes 4444 encoding.)
- **Field Notes line:** motion-broll renders animation as pure functions of time, with motion blur from four blended sub-frames per frame; same idea as HyperFrames' seek-safe rule.

### H-0058 Post-production for businesses that have long-form content but cannot cut it into short-form
2026-09-29, vault, https://www.instagram.com/reel/DcU_MNWtIkg/

- **Mechanism:** A business already publishes long-form video such as talks, podcasts or site footage. A service takes that footage, picks the strongest moments, cuts them into short vertical clips with captions and a hook, and supplies them on a monthly retainer for the client to post. The engine is transcription to find moments, an editor or composer to cut and caption, and a review step, with the client's leads as the measure of success.
- **Claim:** Cutting a company's long-form content into short-form that brings leads underpins an agency that reports 747,000 dollars personal income in 12 months, unaudited.
- **Testable:** no. The value is in a client engagement, and a keyless run would only test the cutting pipeline, not the idea. Needs: A client with long-form footage and posting access..
- **Idea on its own:** sound. Businesses with long-form content and no editing capacity are a real, standing need, and the claimed earnings are marketing rather than evidence.
- **How it would be done:** Transcribe the client's footage locally, have a child rank candidate segments by hook strength and self-contained meaning, then cut each with ffmpeg and compose captions and framing in HyperFrames. Produce a batch per month and send it for approval before posting. A person handles the client conversation, the choice of what suits the brand, and any compliance sign-off. A live test case is a client with a single piece of footage that already worked.
- **Stack already covers:** HyperFrames (video compose, captions, render), local transcription, ElevenLabs (voice), Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org/ (Cutting, cropping to vertical, and burning captions.); OpusClip alternatives: ClipsAI https://github.com/ClipsAI/clipsai (Open-source library that finds clip-worthy segments in long video.)
- **Missing:** A first paying client and a portfolio of before and after clips.
- **Field Notes line:** Clipping as a service: transcribe a business's long video, pick the moments, cut captioned shorts on a retainer; the stack already owns the cutting half.

### H-0056 Harness Learning Enables Generalizable Test-Time Adaptation
2026-09-29, arxiv, https://arxiv.org/abs/2609.35738

- **Mechanism:** The agent is split into a solver model and a harness, the program that orchestrates its calls and tools. A separate proposer model is trained with reinforcement learning to rewrite the harness code using feedback from executing it, with the reward being the task score of the revised harness. At test time the proposer refines the harness over several runs on a new task with no weight updates. Experiments are on reasoning and multi-hop question answering.
- **Claim:** A trained proposer that revises an agent's harness from execution feedback improves revision quality and transfers to unseen tasks.
- **Testable:** no. It needs reinforcement learning training of a proposer model, which no keyless 30 minute run can reproduce. Needs: GPU training and a model to fine-tune..
- **Idea on its own:** needs-a-run. Revising code from execution feedback is plausible, but gains are shown only on reasoning and multi-hop QA and revision sequences help inconsistently.
- **How it would be done:** A cheap version needs no training: after each nightly run, give a child the run log and the current skill or script, ask for one revision, and keep it only if a fixed score on a small test set rises. That copies the loop without the reinforcement learning. The paper's own value would be the reward design and the test sets, which can be read from the paper and code if released.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** arXiv 2609.35738 https://arxiv.org/abs/2609.35738 (Check for a linked code release and the evaluation sets.)
- **Missing:** A trained proposer model; nobody outside the authors has one.
- **Field Notes line:** Harness learning trains a model to rewrite an agent's own scaffolding from run feedback, using edits to code as the update step instead of weights.

### H-0055 CaptureGrubEnchant/SolidWorks: SolidWorks MCP Server connects an AI assistant to a running SolidWorks instance. Sketch, 
2026-09-29, github, https://github.com/CaptureGrubEnchant/SolidWorks

- **Mechanism:** An MCP server in Node drives a running SolidWorks over Windows COM using the winax bridge. A parameter counter routes calls: 12 or fewer arguments go straight through COM, and 13 or more, such as FeatureExtrusion3 with over 20, are turned into a generated VBA macro that SolidWorks runs itself, with fallback on failure. It walks the feature tree rather than selecting by name. The README admits most tools are unvalidated on a live instance.
- **Claim:** Lets an AI assistant sketch, extrude, fillet and export STEP or STL in a running SolidWorks.
- **Testable:** no. It needs Windows and a licensed SolidWorks, and the install steps pipe scripts from unrelated domains that should not be run. Needs: Windows, a SolidWorks licence, and a trustworthy install source..
- **Idea on its own:** sound. Routing awkward many-argument COM calls through generated macros is a genuine workaround, though this repo's install path points to unrelated domains and warns most tools are untested.
- **How it would be done:** The pattern applies to any desktop CAD or Office app with a COM or scripting API: expose small tools over MCP, count parameters, and emit a macro for the heavy calls. Building it would mean writing a handful of tools against a real instance and validating each, which the repo has not done. Read the source only from the GitHub repo, not the zip or the PowerShell one-liner, since those come from other domains.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** FreeCAD https://github.com/FreeCAD/FreeCAD (Free CAD with a Python API on macOS, a safe place to try the same agent-drives-CAD idea.); CadQuery https://github.com/CadQuery/cadquery (Pure Python parametric CAD that an agent can drive with no GUI or licence.)
- **Missing:** A validated, safely distributed SolidWorks bridge does not exist here; this one's install chain is suspect.
- **Field Notes line:** A SolidWorks MCP server routes long CAD calls through generated VBA because COM bridges choke past 12 arguments; treat its install script as hostile.

### H-0054 Media-buying commission taken as a share of a brand's ad budget
2026-09-29, vault, 

- **Mechanism:** An operator buys or places ads on a brand's behalf and takes a percentage of the ad budget as fee, here quoted as 20 percent of a 100k budget. The service is allocation and optimisation: choosing channels, creatives and audiences, then reporting results, with the brand paying platforms directly or through the agency. Revenue scales with spend managed, not with hours, so it depends on the operator's record of return on ad spend.
- **Claim:** Media buying for a brand is paid at 20 percent of a 100k ad budget.
- **Testable:** no. It is a service arrangement with clients and ad accounts, and there is nothing to run keyless. Needs: A client with an ad budget and ad platform account access..
- **Idea on its own:** needs-a-run. Commission on spend is a standard agency model, but the 20 percent figure is high against typical 10 to 15 percent norms and rests on a claim nobody has audited.
- **How it would be done:** The work is: get access to the client's ad accounts, set up tracking, launch tests across creatives, read the results daily and move budget toward what converts, then send a weekly report. A script can generate creative variants and pull platform reports, but the judgement of where to shift money and the client relationship is a person's job. A hired media buyer would run the accounts, with the agency owning creative production, which is where the video stack fits.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), HeyGen and Tavus (avatars), Claude Code with skills and sub-agents
- **To fetch:** Meta Ad Library https://www.facebook.com/ads/library/ (Public data for seeing what a brand's competitors run before pitching.)
- **Missing:** A track record of return on ad spend on real budgets, which nobody in the stack holds.
- **Field Notes line:** A media buyer's fee is a cut of ad spend, so income scales with budget managed; the quoted 20 percent of 100k is the kit's number, unverified.

### H-0052 TokenCast: Forecasting Token Consumption During LLM Agent Execution
2026-09-29, arxiv, https://arxiv.org/abs/2609.35760

- **Mechanism:** TokenCast splits an agent run into execution segments and learns for each segment two numbers: its own token use and how much context it adds. Composing segments gives a cumulative forecast that includes the re-read cost, since every later call re-sends earlier context. As the run proceeds, observed segments replace guesses and the forecast updates with no extra LLM call. It is trained on traces from SWE-bench Verified and three other suites across six models.
- **Claim:** Forecasts agent token use with 14.5% lower mean absolute error than the best comparator, and budget control uses 21.3% fewer tokens at matched completion.
- **Testable:** yes. Does the TokenCast repo ship trace data and a script that reproduces a mean absolute error on one suite within a factor of two of the paper's figure? Queued as P-0037.
- **Idea on its own:** sound. Context re-read makes agent cost superlinear in steps, so a running cumulative forecast with segment-level features is a reasonable design and is cheap to check against traces.
- **How it would be done:** Clone the repo, find the released traces and the evaluation script, and run the baseline and TokenCast on one suite to compare error. To use it here, log per-call input and output tokens from the sub-agent transcripts Proteus already parses for USAGE.md, cut them into segments by tool call, and fit the same composition on Proteus's own runs. The output would be a nightly forecast against a call cap, which feeds the probe loop's budget check.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** TokenCast https://github.com/DEFENSE-SEU/TokenCast (The paper's code and evaluation scripts.); SWE-bench Verified https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified (The task suite whose traces the paper evaluates on.)
- **Field Notes line:** TokenCast predicts an agent's total token bill mid-run in 33 milliseconds by adding up per-step costs plus the re-read tax; the code is public.

### H-0051 AgentSystemLabs/agent-office: A cartoon 3D office where your team hires Claude Code workers at desks, shares live termin
2026-09-29, github, https://github.com/AgentSystemLabs/agent-office

- **Mechanism:** A Node server spawns Claude Code, Codex or OpenCode CLIs inside pseudo-terminals per worker, one git worktree per task, and streams each terminal over a websocket to a browser client drawn as a 3D office. Status (needs input, finished) is inferred from the terminal and shown as an animated worker. GitHub issues and PRs come from the gh CLI and are pinned to boards, and the same state is exposed in a 2D /lite view for phones.
- **Claim:** A shared 3D office where a team runs Claude Code workers at desks, shares live terminals and tracks GitHub issues and PRs.
- **Testable:** no. It needs a signed-in agent CLI and gh auth, and installs through a curl-pipe-bash script, none of which fit a keyless sandbox run. Needs: A signed-in agent CLI and GitHub CLI login..
- **Idea on its own:** needs-a-run. The useful part, a pty-per-agent dashboard with a longest-waiting queue, is sound, but the author warns it is one person's workflow and changes weekly.
- **How it would be done:** The transferable piece is a small supervisor: launch each agent in a pty with tmux or node-pty, give each its own git worktree, and detect the waiting state from terminal output or hooks. Expose the list over a tiny web page with a 'longest waiting first' sort. That can be built in an evening without the 3D layer. Reading docs/how-it-works.md would show how they detect the waiting state, which is the one hard part.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** agent-office https://github.com/AgentSystemLabs/agent-office (Read docs/how-it-works.md for the waiting-state detection.); node-pty https://github.com/microsoft/node-pty (Pseudo-terminal spawning for a home-built supervisor.); tmux https://github.com/tmux/tmux (Simplest way to keep many agent sessions alive and inspectable.)
- **Missing:** Nobody has a reliable, agent-agnostic signal for 'this agent is waiting for a human'.
- **Field Notes line:** Agent Office turns parallel coding agents into desks in a 3D room, with a worktree each and a ding when one needs you; the idea is the queue, not the cartoon.

### H-0049 Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai-video-bootcamp, cancel before 
2026-09-29, vault, 

- **Mechanism:** A paid Skool community holds its course as a classroom of video lessons. The idea is to join for a single billing month, pull each lesson's video, transcribe it locally, and file the transcripts as notes so the content can be searched and mined by agents after the membership ends. It depends on the classroom videos being streamable to a logged-in browser session, and on local transcription turning them into text at a fraction of real time.
- **Claim:** A nine dollar a month AI video course with nine phases can be extracted into text and cancelled before renewal.
- **Testable:** no. The classroom sits behind a paid login and the pull needs an interactive browser session, so nothing can be run keyless tonight. Needs: A paid Skool membership and an interactive logged-in browser session..
- **Idea on its own:** sound. Transcribing lessons you paid for into private notes is a plain learning workflow, provided the transcripts stay private and are not republished.
- **How it would be done:** Join, then in an interactive browser session list every lesson in the classroom and record each video URL or stream manifest. Download each video the platform already serves to the member, run local transcription on the audio track, and write one markdown note per lesson with the phase and title as headings. Hand batches of transcripts to Haiku or Sonnet children to digest into a mechanism summary per phase, and keep only the digests in the shared notes. Set a calendar stop before day 28 so the cancel happens with a margin. A person would only be needed for the login and the cancel click.
- **Stack already covers:** local transcription, Claude Code with skills and sub-agents, keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** yt-dlp https://github.com/yt-dlp/yt-dlp (Pulls embedded lesson videos (Loom, Vimeo, YouTube) that a Skool classroom links to.); whisper.cpp https://github.com/ggml-org/whisper.cpp (Fast local transcription on the Mac if the current local pipeline is slow.)
- **Missing:** Nobody has the Skool login flow scripted; it needs a person present in an interactive session.
- **Field Notes line:** Rent a course for a month, transcribe every lesson locally, keep the text, cancel before renewal: a course becomes a searchable note pile for nine dollars.

### H-0048 Show HN: OpenAPPA – open-source deterministic guardrails that don't break agents
2026-09-28, hn, https://www.openappa.com/

- **Mechanism:** A deterministic guardrail sits in an agent loop through pre- and post-tool-call hooks. Its policy language is written per kind of data rather than per use case, so one policy covers many tasks. To stop it breaking agents it adds a remedy plan, telling the agent what it may do instead, and a DualLLM pattern that keeps untrusted data away from the acting model. The leak and utility percentages come from the authors' own benchmarks.
- **Claim:** About 90% utility retained versus about 40% for other deterministic guardrails, against roughly 10% leaks for LLM-judge approaches.
- **Testable:** no. Reproducing the benchmarks needs LLM agent runs, and the numbers are the authors' own. Needs: An LLM agent to drive the benchmark.
- **Field Notes line:** OpenAPPA writes guardrail policy per data type, not per task, and tells a blocked agent what it can do instead; the 90% utility figure is self-reported.

### H-0046 jkawamoto/mcp-youtube-transcript: MCP server retrieving transcripts of YouTube videos
2026-09-28, github, https://github.com/jkawamoto/mcp-youtube-transcript

- **Mechanism:** An MCP server exposing tools to fetch a YouTube video's transcript, timed transcript, metadata and available languages from a URL. Long transcripts are paginated with a cursor so they fit inside a token limit. It runs locally through uvx and needs no key, but depends on YouTube serving captions to the caller's IP.
- **Claim:** Retrieves transcripts for YouTube URLs with cursor-based pagination for long videos.
- **Testable:** yes. Does uvx run it keyless and return a transcript for a public captioned video, and how many pages does a 28 minute video take? Queued as P-0031.
- **Field Notes line:** A keyless MCP server that pulls YouTube transcripts and pages long ones by cursor; tonight's test is whether YouTube still hands them over.

### H-0045 Launch HN: Vespper (YC F24) – SOTA Docx MCP
2026-09-28, hn, https://www.vespper.com/blog/launching-vespper-docx-mcp

- **Mechanism:** A Word file is a zip of verbose OOXML, so simple edits such as a numbered list or bold text need linked changes across numbering.xml and split run elements in document.xml. Vespper puts an MCP in front of that with a fine-tuned model that turns edit intents into the low-level XML changes, so the calling agent does not spend tokens on the mechanics. The comparison numbers are the vendor's own.
- **Claim:** A Word-editing MCP that is 3 times faster, 2 times cheaper and more accurate than the closest alternative.
- **Testable:** no. Needs a Vespper account and its hosted model, and the benchmark data is not public in the post. Needs: A Vespper account.
- **Field Notes line:** Agents are bad at Word because bold text means splitting XML runs and lists need linked numbering entries; Vespper hides that behind a tuned model.

### H-0043 A Safety-Bounded SDC-to-MCP Gateway for Medical AI Agents
2026-09-28, arxiv, https://arxiv.org/abs/2609.31358

- **Mechanism:** A gateway maps IEEE 11073 SDC medical device state into MCP: metrics, alarms and metadata become read-only resources, and actions become dry-run tools validated against a policy. The safety property is narrow: no agent request ever dispatches a real device operation. It was tested on a Python prototype with simulated faults, Java and Python interoperability, and several models.
- **Claim:** Explicit semantic metadata improved conformity to required metric identifiers in alarm outputs, and the no-execution boundary held on all paths.
- **Testable:** no. Needs SDC device simulators and the authors' prototype, which the abstract does not link. Needs: The prototype code and an SDC simulator.
- **Field Notes line:** A medical-device MCP gateway keeps agents safe by exposing state read-only and turning every action into a dry run that can never execute.

### H-0042 samyost1/3dicon: One prompt in, a looping animated 3D icon out — with real transparency. A Claude Code skill.
2026-09-28, github, https://github.com/samyost1/3dicon

- **Mechanism:** An image model makes one still, which is sent to a video model as both first and last frame, so the clip returns to its start and loops without a seam. The background is a chosen flat colour, so each frame can be unmixed for exact foreground colour and alpha rather than guessed, which avoids edge halos. Frames are then packed into an animated WebP. It needs an OpenRouter key and a roughly 180MB matting model.
- **Claim:** One prompt gives a seamlessly looping animated 3D icon with real transparency.
- **Testable:** no. The pipeline needs an OpenRouter key and paid image and video model calls. Needs: An OpenRouter API key and spend.
- **Field Notes line:** Loop a video model by feeding the same still as first and last frame, then remove the background against a known colour to keep soft edges.

### H-0040 Agent Memory EXPLAINED - Complete Architecture
2026-09-28, youtube, https://www.youtube.com/watch?v=aYfZN8t6AQs

- **Mechanism:** Long-term agent memory is a separate service beside the conversation history. Mem0 stores facts from every conversation in several stores, runs an ingestion workflow that extracts and reconciles facts, and a retrieval workflow that fetches relevant ones each turn. Deleting one memory is its own workflow. The talk says it can all run on local models.
- **Claim:** Walks through Mem0's stores, ingestion, retrieval and deletion, and how to rebuild it with local models.
- **Testable:** no. Running Mem0 needs an LLM for fact extraction, and no 30 minute keyless slice gives a verdict on the walkthrough itself. Needs: An LLM endpoint for extraction.
- **Field Notes line:** Mem0's long-term memory is a separate service with its own ingest, retrieve and delete workflows, sitting beside the plain chat history.

### H-0039 Structured Reasoning Agentic Framework for Interpretable Critical View of Safety Assessment
2026-09-28, arxiv, https://arxiv.org/abs/2609.31524

- **Mechanism:** Surgical frames are turned into an anatomical scene graph of entities and spatial relations. A fine-tuned LLM acts as the central decision-maker and calls a vision-language model as a tool to verify each sub-criterion of the Critical View of Safety separately. It then combines those observations into a verdict with a written rationale. Numbers come from the Endoscapes-CVS201 benchmark.
- **Claim:** 68.1% mAP on Endoscapes-CVS201 with criterion-level explanations.
- **Testable:** no. Needs the benchmark data and trained models, and no runnable public code is named in the abstract. Needs: Benchmark dataset access and model weights.
- **Field Notes line:** A surgery-safety checker splits one black-box score into per-criterion checks: an LLM asks a vision model tool questions about a scene graph.

### H-0038 lemomo-ai/lemo-opuscar: 39 film styles, each a reusable style prompt plus a short film made entirely in code by Claude O
2026-09-28, github, https://github.com/lemomo-ai/lemo-opuscar

- **Mechanism:** A coding agent is given a style prompt plus guides and writes a page in Canvas or WebGL that is rendered frame by frame, then muxed with ffmpeg. Music is composed from free sample libraries and narration comes from local text-to-speech, so there is no video model or stock footage. The styles are tuned to one specific model version, and the repo says other models may not reproduce them.
- **Claim:** 39 reusable film styles, each with a short film made entirely in code, including a 6:25 film covering 98 Best Picture winners.
- **Testable:** no. Directing a film needs a Claude agent run against the skill, which is spend Proteus does not have for this, and the 60 MB download is only the tooling. Needs: A Claude Opus-class agent session to direct a film.
- **Field Notes line:** Whole short films made by an agent writing Canvas and WebGL code, rendered frame by frame with local speech and sampled music, no video model.

### H-0037 Show HN: HN.watch – Videos of all Hacker News posts
2026-09-28, hn, https://hn.watch/

- **Mechanism:** An LLM writes an HTML-based video (a timed script of animated page elements plus narration) instead of pixels, so playback is just a browser rendering markup. The video is generated the first time a link is clicked and then presumably cached. Cost is claimed to be about $0.04 per video because one text generation replaces diffusion video, but image generation inside a video blows that up. The stack is built on the Imba language and Scrimba's existing HTML video format.
- **Claim:** Explainer videos generated in a few seconds from click to playback at roughly $0.04 each, excluding image generation.
- **Testable:** yes. Does an uncached hn.watch item load and start playing within 10 seconds without a login, and what is the measured click-to-playback time? Queued as P-0030.
- **Field Notes line:** Scrimba makes explainer videos as HTML plus an LLM script instead of pixels, claiming four seconds and about four cents each.

### H-0036 alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interactive web art, stickers and score
2026-09-27, github, https://github.com/alexgreensh/anidoodle

- **Mechanism:** Each of the 31 styles is implemented as deterministic drawing code: marks (hatching, dabs, stipple dots, triangles, brush strokes) are placed by pure functions of position and tone rather than wall-clock-seeded randomness, and the audio is described as generated arithmetically rather than sampled. With no external randomness or asset lookup, the same source is claimed to redraw pixel-identical output on any machine or render size.
- **Claim:** Claims the same source code redraws the same picture, in any of 31 hand-drawn styles, identically on every machine and at every size.
- **Testable:** yes. Does running the same anidoodle style script twice produce byte-identical rendered output, as the determinism claim says? Queued as P-0028.
- **Field Notes line:** anidoodle draws in 31 styles entirely as deterministic code, no randomness, claiming the same script renders pixel-identical output every time it runs.

### H-0034 lightpanda-io/browser (new in awesome-mcp-servers)
2026-09-27, awesome, https://github.com/lightpanda-io/browser

- **Mechanism:** Lightpanda is a browser engine written from scratch in Zig rather than a Chromium or WebKit fork, implementing its own DOM/JS handling instead of a full rendering stack, and exposing the standard Chrome DevTools Protocol on port 9222 so existing Puppeteer/Playwright clients can drive it unmodified. Its benchmark fetched 933 real pages on one EC2 instance and measured peak memory and wall-clock time against headless Chrome doing the same crawl.
- **Claim:** Claims 123MB peak memory versus Chrome's 2GB (about 16x less) and 5s versus 46s for 100 pages (about 9x faster) on that benchmark.
- **Testable:** yes. Does the lightpanda binary actually fetch and dump HTML from a real public page via its CLI, and how does its wall-clock time compare to a quick baseline fetch? Queued as P-0027.
- **Field Notes line:** Lightpanda is a browser built from scratch in Zig, not a Chromium fork, claiming 16x less memory and 9x faster page loads than headless Chrome.

### H-0033 How to Build An Expected Goals Model 1: Data and Model
2026-09-27, youtube, https://www.youtube.com/watch?v=bpjLyFyLlXs

- **Mechanism:** An expected-goals model is a statistical model, fitted on many recorded shots (here a season of Wyscout data across leagues), that estimates the probability a shot of a given type and location becomes a goal. The lecture frames it as the first step before moving to machine-learning variants and stresses that the model's quality lives in how the underlying shot data is defined and measured.
- **Claim:** Describes building an xG model from a season of Wyscout shot data as lecture one of a three-part series.
- **Testable:** no. This part of the transcript is conceptual framing with no formulas, features or code shown to run against.
- **Field Notes line:** Friends of Tracking's xG lecture explains it as a statistical model fitted on season-long shot data by location and type, ahead of the ML follow-ups.

### H-0032 PUBG Ally: A Conversational Embodied Agent as an AI Teammate
2026-09-27, arxiv, https://arxiv.org/abs/2609.29837

- **Mechanism:** Ally splits control between a language-model agent that reads game state, interprets voice and picks high-level actions, and a faster low-level control layer that actually executes movement, combat and recovery in real time. It was trained iteratively on data from nearly 39,000 real sessions of players playing alongside it, with model compression, context compaction and runtime guardrails added to hit live on-device latency and safety needs.
- **Claim:** Surveyed across 141 countries, positive recommend-Ally responses exceeded negative ones by 25.1 percentage points among confirmed players.
- **Testable:** no. It's a proprietary system deployed inside PUBG's live service; there is no public build to run. Needs: access to PUBG's live service integration, which is not public.
- **Field Notes line:** PUBG's AI teammate splits a slow LLM planner from a fast control layer for real-time play, trained on 39,000 live sessions with real players.

### H-0031 dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and so
2026-09-27, github, https://github.com/dzhng/jevgrep

- **Mechanism:** jg walks a repo's folder and file hierarchy, using content previews to prune branches, then calls the hosted Jev model to judge which files and declarations are relevant to a natural-language question. It parses Python and TypeScript/JavaScript declarations directly for structure and falls back to plain text elsewhere, returning file paths, reading leads and verbatim excerpts rather than forcing a fixed top-N list.
- **Claim:** Positions itself as a faster alternative to grep-style search for coding agents, using Jev to judge relevance across a codebase.
- **Testable:** no. Needs a paid key for Vercel AI Gateway, OpenRouter or similar to run Jev; the CLI does nothing useful without one. Needs: an API key for Vercel AI Gateway, TypeSafe, OpenRouter or OpenCode Zen.
- **Field Notes line:** jevgrep has a coding agent ask Jev which files matter instead of grepping, previewing content to prune the repo tree before ranking results.

### H-0030 Turning GLM-5.3-Flash into a Jev-like decision model
2026-09-27, hn, https://www.privatemode.ai/blog/system-one-from-glm-flash

- **Mechanism:** They craft the prompt so the very first output token of a standard LLM (GLM-5.3-Flash on vLLM) directly encodes the decision, turning what would be a generated explanation into a single forward pass read off the first token's logits. This mimics latency-optimised decision models like Jev without a specialised architecture, and it extends to vision inputs because it's prompting, not a separate classifier head.
- **Claim:** Says the approach matches Jev's accuracy and speed and beats Laya, though it costs several times more per decision than Jev; a commenter disputes the claimed prefill speed is achievable on normal hardware.
- **Testable:** no. Needs GLM-5.3-Flash weights and a vLLM serving stack, not a 30-minute keyless run. Needs: GLM-5.3-Flash model access and a vLLM deployment.
- **Field Notes line:** Forcing the first output token to be the answer turns any LLM into a one-forward-pass decision model, matching Jev's accuracy but costing more per call.

### H-0029 agentmail-to/agentmail-mcp (new in awesome-mcp-servers)
2026-09-27, awesome, https://github.com/agentmail-to/agentmail-mcp

- **Mechanism:** AgentMail now ships a single hosted MCP implementation reachable over Streamable HTTP; the npm and PyPI 'bridges' are thin stdio shims that discover the tool catalogue and JSON schemas live from that hosted server rather than embedding their own tool logic. A generated mcp-manifest.json defines the runtime contract, and both bridges support OAuth or a per-request API key plus a --tools filter.
- **Claim:** Consolidates what used to be a local npm implementation into one hosted MCP server, with stdio bridges kept only for compatibility.
- **Testable:** yes. Does the hosted Streamable HTTP endpoint (https://mcp.agentmail.to/mcp) answer or refuse a tool-list call with no API key at all? Queued as P-0026.
- **Field Notes line:** AgentMail collapsed its MCP server into one hosted endpoint; the npm and Python packages are now just thin bridges fetching the tool catalogue live.

### H-0027 When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression
2026-09-27, arxiv, https://arxiv.org/abs/2609.29875

- **Mechanism:** ICLR ranks blocks of an agent's past reasoning by a frozen proxy model's token entropy and prunes low-value ones from context while always keeping actions, tool calls and observations intact. It runs online with no training, deciding per step what reasoning history is safe to drop. Ablations show deleting reasoning can amplify downstream compute nonlinearly, and that reasoning becomes droppable once the task state it captured has been externalised into files, code or tool output.
- **Claim:** On 260 WorkBuddyBench tasks it raises average reward from 0.699 to 0.718 while cutting input, output and cache-read tokens by 25.5%, 14.4% and 33.3%.
- **Testable:** no. Needs the WorkBuddyBench harness, a proxy model for entropy scoring and a long-horizon agent loop; nothing runnable from the abstract alone. Needs: WorkBuddyBench benchmark code and a compatible agent/proxy-model setup.
- **Field Notes line:** A training-free method scores an agent's past reasoning by proxy-model entropy and prunes it, cutting tokens up to a third while nudging reward up.

### H-0025 On caring for user data: NeoVim caused Vim undo files to be deleted
2026-09-27, hn, https://unsung.aresluna.org/they-had-no-concept-of-a-duty-of-care-to-their-users/

- **Mechanism:** Neovim and classic Vim share the same undo-file name and location but Neovim changed the on-disk undo format without versioning or renaming it. When Neovim opens a Vim-format undo file it can't parse, it deletes the file outright and writes its own incompatible format in its place, destroying the old undo history and leaving Vim unable to read the replacement either.
- **Claim:** The post says persistent undo files get silently deleted and replaced by Neovim because of an unannounced, unversioned format change.
- **Testable:** yes. Does opening a classic-Vim undo file in a fresh Neovim install actually delete/overwrite it so Vim can no longer read it? Queued as P-0025.
- **Field Notes line:** Neovim silently deletes and overwrites classic Vim's undo files on an unversioned format change; testable tonight with two editors and one file.

### H-0022 mikehasa/golive-skill: Take your agent-built product live: hosting, database, domain, email, payments — on your own acco
2026-09-26, github, https://github.com/mikehasa/golive-skill

- **Mechanism:** GoLive is a zero-dependency Node CLI plus an Agent Skill running a detect -> plan -> approve -> apply -> verify pipeline against your own provider accounts (Vercel/Netlify, Supabase/Neon, Porkbun/GoDaddy DNS, Resend email, Stripe test-mode payments). Apply refuses to run without a plan id and an explicit --yes, re-validates the plan's identity against current state before writing, and gates destructive or live-money actions behind separate --confirm-dns/--confirm-destroy/--confirm-live flags; it stores any credentials it touches in a plaintext 0600 file outside the repo rather than a keychain, and states plainly that an agent already logged into a provider can bypass its plan gate entirely.
- **Claim:** Lets an agent take a built app live end to end, then tear it down again, on your own hosting/database/domain/email/payment accounts with no GoLive backend or telemetry, currently alpha-tested across six provider journeys.
- **Testable:** yes. Does `golive detect` and `golive plan` produce a real, inspectable plan for a scratch app with no provider account connected, and does `apply` correctly refuse to run without --yes? Queued as P-0023.
- **Field Notes line:** GoLive is an open-source skill that scripts taking an agent-built app live on your own provider accounts, gating every write behind an explicit plan and confirm flags.

### H-0021 Jevmem – automatic project memory for Claude Code, built on Jev
2026-09-26, hn, https://github.com/Avinash-jetwani/jevmem

- **Mechanism:** Jevmem hooks into Claude Code/Cursor/Codex chat sessions and after every message calls a small classifier model (Jev, via the TypeSafe API) to judge whether that message contains something durable worth remembering, a decision, a bug, a change of mind, and if so appends it to a JEVMEM.md file in the repo; when a later message reverses an earlier decision, the old entry is marked superseded rather than deleted. It is a thin wrapper around a hosted classification API, not a local model or vector store.
- **Claim:** The author's own held-out test on 66 messages puts Jev at 98.5% accuracy on the save/skip decision, tied for best of six frontier LLMs, with a 0.30s median decision latency versus 2.8-4.3s for the compared LLMs.
- **Testable:** no. Installing and running it needs a TypeSafe API key, a credential Proteus does not hold. Needs: a TypeSafe API key.
- **Field Notes line:** Jevmem watches your coding-agent chats and uses a small hosted classifier to decide, message by message, what's worth saving to a project memory file.

### H-0019 Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents
2026-09-26, arxiv, https://arxiv.org/abs/2609.29892

- **Mechanism:** Qwen-Planner-Agent is built through a closed AI-for-AI loop with three parts: an agentic data flywheel where specialised agents generate mobile-planning tasks and curate trajectories with human gating; training that combines a supervised cold start with online reinforcement learning using a 'Competence-Aware Reward-and-Advantage Engineering' term to cut tool-use and reasoning cost; and a runtime loop that logs execution evidence and failure traces back into both the model weights and the surrounding harness (memory, skills, tool orchestration).
- **Claim:** Qwen-Planner-Agent tops MobilePA-Bench among evaluated models and systems, improving over its base model on tool use, memory, skills and sub-agent coordination while mostly holding onto general capability.
- **Testable:** no. Needs the MobilePA-Bench harness, real or emulated mobile devices, and the trained model weights, none available for a keyless run tonight.
- **Field Notes line:** Qwen-Planner-Agent trains a mobile-planning agent through a closed loop of agent-generated data, RL with a cost-aware reward term, and runtime feedback into both model and harness.

### H-0018 yetone/magpie: Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, from the menu bar.
2026-09-26, github, https://github.com/yetone/magpie

- **Mechanism:** magpie runs a small local HTTP gateway (127.0.0.1:3425) that speaks the OpenAI chat-completions, OpenAI Responses and Anthropic Messages API shapes and translates between them, so any agent CLI pointed at it can use any configured backend model regardless of which API the agent itself expects. It edits each tool's own config file (settings.json, config.toml, opencode.jsonc, config.yaml) in place, touching only the changed key so comments and ordering survive, and pulls live model lists per provider, falling back to the models.dev catalog rather than a hardcoded list.
- **Claim:** One menu-bar app lets you point every agent CLI (Claude Code, Codex, Gemini CLI, OpenCode, etc.) at any provider or model through a single local gateway, with surgical, non-destructive edits to each tool's config file.
- **Testable:** yes. Does magpie's config writer change only the targeted key in a sample settings.json copy, leaving comments, key order and unrelated fields byte-identical? Queued as P-0022.
- **Field Notes line:** magpie is a local menu-bar gateway that translates between OpenAI and Anthropic API shapes so any agent CLI can run on any provider's model, editing each tool's config file surgically.

### H-0017 Show HN: A Claude Code skill to analyze your chess games
2026-09-26, hn, https://github.com/brumar/chess-postmortem-skills

- **Mechanism:** The system takes a live game (audio notes or text, plus a lichess game reference), uses Claude's vision to read board state directly from images rather than parsing PGN, and pairs that with a local Stockfish engine for move evaluation. Claude then narrates the game, combining Stockfish's evaluations with a reflection on the player's own recorded thinking during the game, and renders the commentary as a video. The author reports it costs roughly $15 in API spend and about an hour per game.
- **Claim:** Turns 'analyze my last lichess game' plus your own audio notes into a commented video of the game, using Claude vision plus Stockfish, for about $15 in API cost per game.
- **Testable:** no. The author's own figure is about $15 in API spend per run, real spend Proteus can't put toward a keyless test.
- **Field Notes line:** A Claude Code skill reads chess boards by vision instead of PGN, pairs that with Stockfish, and narrates a commented video of your own game and thinking for about $15 a run.

### H-0015 An Empirical Study of VLM Pipelines for Long-Document QA
2026-09-26, arxiv, https://arxiv.org/abs/2609.29933

- **Mechanism:** The paper benchmarks long-document VLM QA pipelines on three axes: how the document is fed in (full pages vs a retrieved subset), which retriever selects pages (image-embedding retrieval of rendered pages vs text retrieval plus a cross-encoder rerank), and whether the model runs agentically with page/table/figure/search tool calls or as one static pass. It runs these combinations on MMLongBench-Doc and LongDocURL with both frontier API models and open-weight Qwen3.5 variants, measuring accuracy and token cost per pipeline.
- **Claim:** Their six-tool agent only beats static page-feeding once the reader model is large enough (level with Qwen3.5-27B, ahead with Sonnet 4.5), image retrieval beats text retrieval at a seventh to a quarter of the tokens, and an oracle pipeline-picker gains about 13 points over the best single pipeline.
- **Testable:** no. Reproducing needs the MMLongBench-Doc/LongDocURL benchmarks plus paid frontier VLM API calls, a multi-day evaluation, not a 30-minute keyless run.
- **Field Notes line:** Long-document QA study finds agentic tool-calling only beats just feeding pages once the model is big enough, and image-based page retrieval beats text retrieval at far fewer tokens.

### H-0014 JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P(doom)
2026-09-26, github, https://github.com/JohnHeibel/PDoomVideo

- **Mechanism:** The whole music video was produced by Claude Opus 5.5 in Claude Code with no scene ideas supplied: the model wrote its own shot-by-shot STORYBOARD.md and an ANIMATION_GUIDE.md briefing document, then dispatched parallel subagents to build each chapter as p5.js/p5.brush code rendered in a shared studio.html canvas. A separate render.mjs script paints every frame in headless Chrome and stitches them with ffmpeg into the final MP4 synced to the included song.
- **Claim:** A full nine-chapter animated music video, entirely written and orchestrated by Claude Opus 5.5, given only a character design and two style directions.
- **Testable:** yes. Does render.mjs paint frame 0 of a chapter from a clean checkout with npm install alone, or does it need a manual Chrome path? Queued as P-0021.
- **Field Notes line:** A full 9-chapter music video was written and rendered end to end by Claude Opus subagents, from storyboard to p5.js animation to ffmpeg encode, no human scene ideas.

### H-0013 Show HN: Reladraw – A diagram language where you decide where to place things
2026-09-26, hn, https://github.com/reladraw/reladraw

- **Mechanism:** Reladraw is a diagram-definition language where you specify relative placement of nodes rather than absolute coordinates or letting an auto-layout engine decide, sitting between auto-placement tools (Mermaid, Graphviz) and manual editors (draw.io). It compiles the language to a rendered diagram, has a browser playground for trying it without installing anything, ships as an npm package for local use, and includes a packaged skill so an agent can write and edit diagrams as text.
- **Claim:** A diagram language that keeps full manual control of layout while staying as easy for humans and agents to edit as text, per its Show HN post (116 points, 31 comments).
- **Testable:** yes. Does `npm install reladraw` run cleanly and can a plain-text 3-node diagram definition render to an image? Queued as P-0020.
- **Field Notes line:** Reladraw is a new diagram language that keeps manual layout control but stays text-editable enough for agents to drive, unlike Mermaid or draw.io.

### H-0012 Alan Kay: Shannon gave us a way of dealing with noisy channels [video]
2026-09-26, hn, https://www.youtube.com/watch?v=Cjntrqhn8pk

- **Mechanism:** An open Zoom mic near a live-stream speaker fed Alan Kay's own voice back to him after roughly 21 seconds, the delay built up by several re-encoding hops (Zoom, stream, room, back into Zoom, repeated, then a screen recording, then YouTube's auto-captioner on top). The 21-second round trip corresponds to a light-speed distance of about 3 million km, which HN frames as an accidental live demo of Shannon's noisy-channel coding theorem and an unplanned recreation of Alvin Lucier's 1969 tape-feedback piece, where a voice re-recorded through a room repeatedly degrades until only the room's resonance is left.
- **Claim:** HN post frames a ~21-second live-stream audio feedback loop during an Alan Kay talk as an accidental version of Lucier's sound art and a real demo of Shannon's noisy-channel theorem.
- **Testable:** no. Nothing to build or run, it is an anecdote about an accidental live audio feedback loop.
- **Field Notes line:** An open mic turned a live Zoom stream into a 21-second voice-feedback loop, an accidental real-world demo of Shannon's noisy-channel theorem.

### H-0010 nateherkai/hyperframes-student-kit: Edit videos, reels, and YouTube Shorts with Codex or Claude Code. 14 skills, transcr
2026-09-26, github, https://github.com/nateherkai/hyperframes-student-kit. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** Ships a synthetic starter composition so `npm run demo` assembles an 8-second GSAP-driven HyperFrames composition entirely offline; `npx hyperframes lint/preview/render` then lints it, previews it in Studio, and renders it through a headless Chrome pipeline, only reaching the network to cache font substitutions on first render. For real footage, the same skills instead pipe a word-level transcript (from ElevenLabs Scribe, or swapped to local Whisper) into silence-cutting, mistake-detection and cut-planning skills before assembling clips onto 406 pre-built motion-graphics card templates.
- **Claim:** Video-editing skill kit for Claude Code/Codex with transcript-driven cuts and 406 motion-graphics cards; the local demo needs no footage, account or API key.
- **Testable:** yes. Does `npm run demo` followed by `npx hyperframes lint`, `preview` and `render --quality draft` produce a valid demo.mp4 with zero API keys or accounts? Queued as P-0019.
- **Field Notes line:** This Codex/Claude Code video-editing kit ships a synthetic demo that lints, previews and renders a HyperFrames clip with zero API keys or footage required.

### H-0009 Show HN: Whiteboard (YC W26) – An open-source IDE for thoughtful software design
2026-09-26, hn, https://github.com/devdotfast/whiteboard

- **Mechanism:** Vendors a full fork of Code-OSS (VSCode) directly, rather than maintaining a patch set, specifically because coding agents handle a vendored fork better than patches; the fork strips roughly 45% of stock VS Code that was Copilot-related. On top of that base, an SDK lets an agent draw diagrams (sequence diagrams, ER diagrams, trace quotes) onto an in-app canvas that link directly to the underlying source lines, and a separately written Rust AST-aware diff viewer summarises large added functions as pseudocode and collapses routine test/doc-only changes so a reviewer sees only semantically relevant diffs.
- **Claim:** Open-source desktop IDE (YC W26) where an agent's SDK-drawn diagrams click straight through to the code that produced them.
- **Testable:** no. It vendors a full Code-OSS (VSCode) fork plus Rust components in a pnpm monorepo; building that from source will not finish in 30 minutes.
- **Field Notes line:** Whiteboard vendors a full VSCode fork (minus its Copilot code) and gives coding agents an SDK to draw diagrams that click straight through to the source lines.

### H-0007 World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal
2026-09-26, arxiv, https://arxiv.org/abs/2609.29964

- **Mechanism:** Gives a vision-language model a 'visual action workspace' instead of a single scene view: contact-view camera crops are auto-selected from scene geometry around the current interaction, each candidate action becomes an editable visual proposal that is rehearsed and revised (optionally by a separate Imagination Agent) before it ever executes, and an in-view correction step lets the agent remove residual offsets in the same view where it spotted them. A Skill Agent retrieves procedural skills mined from expert videos and human demonstrations, and the harness's own interaction traces are used afterward to fine-tune smaller VLMs to run the same loop.
- **Claim:** 75.6% average success on LIBERO-Pro using only skills evolved from LIBERO-90, beating end-to-end VLA and code-as-policy baselines; fine-tuning Qwen3.5-9B on harness traces raised its out-of-domain success from 1.7% to 43.3%.
- **Testable:** no. Needs LIBERO/robosuite simulation environments plus VLM inference infrastructure, well past a 30-minute keyless sandbox setup. Needs: robot simulation environments (LIBERO, robosuite) and VLM inference compute.
- **Field Notes line:** A VLM robot-control harness rehearses and visually previews every action before executing it, lifting LIBERO-Pro success to 75.6% using only pre-evolved skills.

### H-0006 chainstacklabs/pumpfun-bonkfun-bot: A fully functional pump.fun / letsbonk.fun trading and sniping bot not relying on an
2026-09-26, github, https://github.com/chainstacklabs/pumpfun-bonkfun-bot. Vault verdict on the vendor exists (vault verdict: pump.fun); mechanism recorded, vendor not re-judged.

- **Mechanism:** Watches Solana on-chain activity for new pump.fun/letsbonk.fun token creation itself, choosing between four listener backends of increasing cost and speed: logsSubscribe (works on any RPC), blockSubscribe (not universally supported), a paid Geyser gRPC stream, and raw pre-confirmation 'shreds'; it calls no pump.fun API at all. Each bot instance is a YAML config pointing at one listener plus a buy/sell strategy, and it signs and submits its own transactions using a supplied wallet private key.
- **Claim:** Open-source pump.fun/letsbonk.fun sniping bot with four selectable listener speeds, explicitly 'not for production, for learning purposes only'.
- **Testable:** no. Real sniping needs a funded Solana wallet private key and, for the faster listeners, a paid Geyser/RPC endpoint; public RPC will not do the job. Needs: a funded Solana wallet and a paid Geyser/RPC endpoint.
- **Field Notes line:** This pump.fun sniper skips pump.fun's own API entirely, racing new tokens via raw Solana log, block, Geyser or shred streams instead, speed bought with a pricier RPC tier.

### H-0005 Claude Code reads AGENTS.md only when telemetry is on [fixed]
2026-09-26, hn, https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/

- **Mechanism:** Claude Code's AGENTS.md support ships as a built-in plugin ('agents-md') that defaults to off and gates itself behind a remote feature flag ('tengu_agents_md_mod') fetched over the network; the fallback value when that fetch cannot happen is false. Setting either CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 or DISABLE_TELEMETRY=1 blocks the flag fetch, so the plugin silently stays disabled and the local AGENTS.md file is never read, even though reading a local file needs no network at all.
- **Claim:** Author measured, via a two-session canary-word test, that Claude Code 2.1.277+ skips reading a project's AGENTS.md whenever either telemetry-disabling env var is set; logged as GitHub issue #95690.
- **Testable:** no. Reproducing it means repeated `claude -p` invocations, which spends real Claude API credits rather than running keyless.
- **Field Notes line:** Claude Code's AGENTS.md support hides behind a remote feature flag that quietly defaults off whenever telemetry env vars are set, even though reading a local file needs no network.

### H-0004 Pump Fun Sniper Bot Full Tutorial / Solana MEV Bot step-by-step how to use
2026-09-26, youtube, https://www.youtube.com/watch?v=vssd36X5Y2c

- **Mechanism:** The tutorial's login step asks you to paste a Phantom or Solflare wallet's private key into a browser-hosted 'bot' dashboard, which is the exact mechanism used by Solana wallet-drainer scams that harvest keys under cover of an automation tool. The video's other claims (an 'AI' deciding trades, an 0.01s launch-to-buy reaction time, an 80% win rate) are unverifiable from inside the same dashboard and are typical of this genre's marketing; a real listener-based sniper (see gh:chainstacklabs/pumpfun-bonkfun-bot) needs its own on-chain listener and never asks for your key through a hosted UI.
- **Claim:** Video claims an 'AI'-run bot buys new pump.fun tokens within 0.01 seconds of launch and sells after another buyer moves the price, with an approximate 80% win rate.
- **Testable:** no. The only way to 'test' it is entering a wallet private key into an untrusted third-party site, which is not something to do to get a verdict. Needs: a wallet private key handed to an untrusted site, which we will not provide.
- **Field Notes line:** This 'AI' pump.fun sniper's login step asks for your wallet's private key pasted into its website, the exact pattern behind Solana wallet-drainer scams.

### H-0003 Screen Before You Serve: Simulation for Production Customer Experience AI Agents at 140M Scale
2026-09-26, arxiv, https://arxiv.org/abs/2609.30137

- **Mechanism:** Candidate customer-support agent configs are screened with synthetic customer personas (via the Snowglobe simulator) that converse with the agent while simulated tool outputs stand in for production backends, so multi-step flows run without touching real customer data. An automated binary evaluator scores each simulated conversation; the paper reports these simulated scores correlate highly with the same version's later production evaluator scores, which is the basis for using simulated deltas to pick between models, reasoning settings and prompts before running a live A/B test.
- **Claim:** Simulation-guided iteration across 16,000+ simulated conversations at Nubank raised transactional NPS by 36.69 points in one A/B test and self-service rate by 8.82 percentage points in a later one, both confirmed live.
- **Testable:** no. Snowglobe and Nubank's Card Management agent are internal production systems with no public code, model or dataset to run.
- **Field Notes line:** Nubank screened chat-support agent configs across 16,000+ simulated conversations before A/B tests, lifting self-service rate by 8.82 points with no customer exposure.

### H-0002 nexmoe/VidBee: Download video and audio from  YouTube ,  TikTok ,  Twitter ,  Instagram ,  Facebook ,  Twitch ,  Bilibil
2026-09-26, github, https://github.com/nexmoe/VidBee

- **Mechanism:** Downloads media from 1000+ sites via a yt-dlp-style backend, then runs speech recognition fully on-device using a local model family the user picks (Whisper, SenseVoice, Parakeet, Qwen3-ASR), producing a timestamped, speaker-labelled transcript with no upload to a transcription service. AI features (summarise, translate, FAQ, mind map) are a separate step: the transcript and prompt are sent to whichever provider the user configures with their own API key (OpenAI, Anthropic, Ollama, LM Studio, etc.), so the privacy guarantee only covers the ASR step, not the AI step unless a local endpoint is chosen.
- **Claim:** Free, open-source desktop app (10.7k GitHub stars) that downloads and locally transcribes video/audio from 1000+ sites, then runs user-chosen AI prompts on the transcript.
- **Testable:** no. Distributed as a GUI desktop installer rather than a scriptable CLI, plus multi-gigabyte local ASR model downloads on first use, so a headless verdict won't land in 30 minutes.
- **Field Notes line:** VidBee downloads video from 1000+ sites and transcribes it fully offline with local Whisper-family models before you choose which AI provider sees the text.

### H-0001 Show HN: Make cursed fonts like Times New Bastard
2026-09-26, hn, https://bastardica.mitpit.com

- **Mechanism:** Mixes glyphs from different fonts by abusing OpenType's ligature substitution (GSUB) tables rather than any server-side rendering. The whole pipeline, including the font-manipulation toolchain, runs client-side by loading a Python interpreter compiled to WASM in the browser, so no upload or backend call is needed.
- **Claim:** A joke web tool for making 'cursed' fonts by mixing typefaces via ligatures, computed entirely client-side in the browser.
- **Testable:** no. It is judged by visual appearance in a browser, not by a headless pass/fail from a sandbox script.
- **Field Notes line:** A joke web tool remixes fonts by hijacking OpenType ligature substitution, all computed live in-browser via a Python interpreter compiled to WASM.

## Vault threads: Luke's links, judged as ideas

Themes the vault split out of links Luke sent it, read from `field-notes/vault-threads.json` (one way). The vault's status
is what its side decided about the vendor or Luke's time; the idea column is this side's view of the idea alone.

| id | date | theme | vault said | idea | testable | probe |
|---|---|---|---|---|---|---|
| H-0127 | 2026-10-04 | node canvas workflows (Flows) | open | needs-a-run | no |  |
| H-0122 | 2026-10-04 | replication gap measured on demo | open | sound | no |  |
| H-0117 | 2026-10-04 | Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summar | open | sound | no |  |
| H-0113 | 2026-10-03 | Photoreal moving footage of a subject you cannot film, one consistent face and a directed  | open | needs-a-run | no |  |
| H-0108 | 2026-10-03 | Generating many platform-native variants (hooks, colour grades, overlays) from one filmed  | open | sound | no |  |
| H-0103 | 2026-10-03 | Whether a fees-paid threshold removes rugs without removing the launches that ran, on a da | open | needs-a-run | yes |  |
| H-0099 | 2026-10-02 | human reads flagged threads from alert links | open | needs-a-run | yes | P-0055 **works** |
| H-0094 | 2026-10-02 | Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7  | open | sound | no |  |
| H-0089 | 2026-10-02 | Whether multi-buy and net-flow signals from tracked wallets predict price, measured on pap | open | needs-a-run | no |  |
| H-0085 | 2026-10-01 | Inbound AI receptionist demo line built from the home services voice prompt | open | sound | no |  |
| H-0080 | 2026-10-01 | One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API | open | sound | no |  |
| H-0075 | 2026-10-01 | Adapt the web design CLAUDE.md for phone-first UK local business sites | open | sound | no |  |
| H-0071 | 2026-09-30 | Partnership ads run through a local client's own social handle | open | sound | no |  |
| H-0066 | 2026-09-30 | Consistent AI character content with clear AI disclosure | open | sound | no |  |
| H-0061 | 2026-09-30 | Learning crypto research from a source with an independently verifiable track record | open | sound | no |  |
| H-0058 | 2026-09-29 | Post-production for businesses that have long-form content but cannot cut it into short-fo | open | sound | no |  |
| H-0054 | 2026-09-29 | Media-buying commission taken as a share of a brand's ad budget | open | needs-a-run | no |  |
| H-0049 | 2026-09-29 | Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai- | open | sound | no |  |

## Tools shelf

Tools, repos and datasets the judge said to fetch, kept here even when nothing needs them today. Each is a candidate
for a ran-it night: install it in `sandbox/`, run it, write the verdict.

| id | date | tool | why | from | status |
|---|---|---|---|---|---|
| T-0076 | 2026-10-04 | [Stockfish](https://stockfishchess.org) | Reference opponent for rating a bot | H-0130 (I Ran a Chess Programming Tournament!) | shelf |
| T-0075 | 2026-10-04 | [python-chess](https://github.com/niklasf/python-chess) | Legal moves and engine play for a local tournament runner | H-0130 (I Ran a Chess Programming Tournament!) | shelf |
| T-0074 | 2026-10-04 | [replica-skill](https://github.com/Jakeschincariol/replica-skill) | The eleven skills and Python tools to run | H-0129 (Jakeschincariol/replica-skill: Eleven free Claude ) | shelf |
| T-0073 | 2026-10-04 | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | Free open-source node-graph runner for the same chaining pattern | H-0127 (node canvas workflows (Flows)) | shelf |
| T-0072 | 2026-10-04 | [live-panel-skill](https://github.com/ythx-101/live-panel-skill) | The renderer and examples | H-0124 (ythx-101/live-panel-skill: Config-driven animated ) | shelf |
| T-0071 | 2026-10-04 | [eToro API portal](https://api-portal.etoro.com) | Demo copy-trading endpoints and docs | H-0122 (replication gap measured on demo) | shelf |
| T-0070 | 2026-10-04 | [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) | The skill and bundled CLI to run | H-0119 (QingYunA/answer-me-with-html: Answer me with HTML ) | shelf |
| T-0069 | 2026-10-04 | [promptfoo](https://github.com/promptfoo/promptfoo) | Runs the same prompt set across several providers and scores them | H-0117 (Benchmark DeepSeek, GLM and Kimi against the M5 qw) | shelf |
| T-0068 | 2026-10-04 | [NVIDIA Build API catalogue](https://build.nvidia.com) | The free hosted open-weight endpoint to benchmark against | H-0117 (Benchmark DeepSeek, GLM and Kimi against the M5 qw) | shelf |
| T-0067 | 2026-10-03 | [Remotion](https://github.com/remotion-dev/remotion) | The best-known alternative React video renderer to compare with HyperFrames. | H-0110 (zhuyansen/awesome-claude-video-skills: Open-source) | shelf |
| T-0066 | 2026-10-03 | [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | The list itself, source for further video-skill repos. | H-0110 (zhuyansen/awesome-claude-video-skills: Open-source) | shelf |
| T-0065 | 2026-10-03 | [Dune](https://dune.com) | Free tier SQL over Solana transactions for a larger dated sample, needs an account so later. | H-0103 (Whether a fees-paid threshold removes rugs without) | shelf |
| T-0064 | 2026-10-03 | [Solana public JSON-RPC](https://api.mainnet-beta.solana.com) | Keyless getSignaturesForAddress and getTransaction to sum fees per pool, rate limited. | H-0103 (Whether a fees-paid threshold removes rugs without) | shelf |
| T-0063 | 2026-10-02 | [Node.js 20+](https://nodejs.org) | Runtime the package requires | H-0101 (ericmmartin/youtube-transcript-plus: YouTube Trans) | shelf |
| T-0062 | 2026-10-02 | [youtube-transcript-plus](https://github.com/ericmmartin/youtube-transcript-plus) | The library under test | H-0101 (ericmmartin/youtube-transcript-plus: YouTube Trans) | shelf |
| T-0061 | 2026-10-02 | [Breadcrumb MCP tool definitions](https://innerloop.works/breadcrumb/mcp) | Read the tool list to measure definition size | H-0100 (Show HN: Breadcrumb, record everything on your mac) | shelf |
| T-0060 | 2026-10-02 | [Poly Haven](https://polyhaven.com) | CC0 textures and reference models | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0059 | 2026-10-02 | [Blender](https://www.blender.org) | Required runtime | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0058 | 2026-10-02 | [blender-kiln](https://github.com/elithril/blender-kiln) | The skill and the fidelity_check script | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0057 | 2026-10-02 | [LDView](https://tcobbs.github.io/ldview/) | Renderer for checking models | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0056 | 2026-10-02 | [LDraw parts library](https://www.ldraw.org/parts/latest-parts.html) | Part definitions needed for validation | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0055 | 2026-10-02 | [ldraw-nova](https://github.com/anteloc/ldraw-nova) | The toolset under test | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0054 | 2026-10-02 | [Higgsfield](https://higgsfield.ai) | Genjutsu route under test | H-0094 (Higgsfield Genjutsu as the final route for motion ) | shelf |
| T-0053 | 2026-10-02 | [Kling Motion Control](https://klingai.com) | Comparison route for the same source clip | H-0094 (Higgsfield Genjutsu as the final route for motion ) | shelf |
| T-0052 | 2026-10-02 | [KaTeX](https://katex.org) | Formula re-typesetting | H-0091 (Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照) | shelf |
| T-0051 | 2026-10-02 | [easyread](https://github.com/Edwardxlai/easyread) | Reference implementation of per-page translation | H-0091 (Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照) | shelf |
| T-0050 | 2026-10-02 | [rhun](https://rhun.app/) | Source and releases to read the translator approach | H-0090 (Show HN: Rhun, an open-source code editor written ) | shelf |
| T-0049 | 2026-10-02 | [Solana public RPC / Helius free tier](https://www.helius.dev) | Swap history per wallet if the leaderboard sites block scraping | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0048 | 2026-10-02 | [GMGN wallet pages](https://gmgn.ai) | Per-wallet trade history for multi-buy and net-flow counts | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0047 | 2026-10-02 | [Kolscan leaderboard](https://kolscan.io) | Public ranked wallet list to seed the tracked set | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0046 | 2026-10-01 | [ClubElo API](http://clubelo.com/API) | Free Elo ratings, no key. | H-0087 (machina-sports/sports-skills: Open-source agent sk) | shelf |
| T-0045 | 2026-10-01 | [sports-skills](https://github.com/machina-sports/sports-skills) | The package under test. | H-0087 (machina-sports/sports-skills: Open-source agent sk) | shelf |
| T-0044 | 2026-10-01 | [Corral](https://github.com/Cardinal44/corral) | The tool. | H-0086 (Show HN: Corral – Kill every command your agent st) | shelf |
| T-0043 | 2026-10-01 | [n8n](https://github.com/n8n-io/n8n) | Self-hosted follow-up workflows. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0042 | 2026-10-01 | [Vapi](https://vapi.ai) | Alternative voice-agent platform. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0041 | 2026-10-01 | [Retell AI](https://www.retellai.com) | Hosted voice-agent loop with a free tier. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0040 | 2026-10-01 | [scikit-learn](https://github.com/scikit-learn/scikit-learn) | Logistic regression and scoring. | H-0084 (What is Expected Goals?) | shelf |
| T-0039 | 2026-10-01 | [StatsBomb open-data](https://github.com/statsbomb/open-data) | Free shot-level event data with coordinates. | H-0084 (What is Expected Goals?) | shelf |
| T-0038 | 2026-10-01 | [librosa](https://github.com/librosa/librosa) | Acoustic measurements as evidence tools. | H-0083 (SEAR: Spoofing Evidence-Grounded Audio Reasoning B) | shelf |
| T-0037 | 2026-10-01 | [painted-animation](https://github.com/tuzhechen2005/painted-animation) | Hand-painted engine it builds on. | H-0082 (edenfunf/reelmimic: Show it a video you love. Get ) | shelf |
| T-0036 | 2026-10-01 | [ReelMimic](https://github.com/edenfunf/reelmimic) | The tool itself. | H-0082 (edenfunf/reelmimic: Show it a video you love. Get ) | shelf |
| T-0035 | 2026-10-01 | [fal client](https://github.com/fal-ai/fal) | Python client for the queue API. | H-0080 (One pay-as-you-go fal account to run Seedance, Kli) | shelf |
| T-0034 | 2026-10-01 | [mlx-lm](https://github.com/ml-explore/mlx-lm) | The underlying library and baseline. | H-0079 (Finally, The CORRECT Way to Run Local AI on a Mac) | shelf |
| T-0033 | 2026-10-01 | oMLX | The server under test; find the repo via the video description. | H-0079 (Finally, The CORRECT Way to Run Local AI on a Mac) | shelf |
| T-0032 | 2026-10-01 | [AppWorld](https://github.com/StonyBrookNLP/appworld) | Benchmark used to score harness changes. | H-0078 (Learning from Research: Toward Lifelong Agent Harn) | shelf |
| T-0031 | 2026-10-01 | [yomiyasu](https://github.com/nanaism/yomiyasu) | Reference skill layout and rule set to adapt. | H-0077 (nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill ) | shelf |
| T-0030 | 2026-10-01 | [Weave Router](https://github.com/weave-os/router) | The open-source router to run against a baseline. | H-0076 (Show HN: Open-source model routing for coding agen) | shelf |
| T-0029 | 2026-10-01 | [Lighthouse CLI](https://github.com/GoogleChrome/lighthouse) | Free mobile performance and accessibility scoring to judge generated sites. | H-0075 (Adapt the web design CLAUDE.md for phone-first UK ) | shelf |
| T-0028 | 2026-09-30 | [ffmpeg ebur128 filter](https://ffmpeg.org/ffmpeg-filters.html#ebur128-1) | Loudness measurement the scripts need. | H-0073 (echris6/motion-video-kit: Claude Code skill kit fo) | shelf |
| T-0027 | 2026-09-30 | [motion-video-kit](https://github.com/echris6/motion-video-kit) | The skill and measurement scripts. | H-0073 (echris6/motion-video-kit: Claude Code skill kit fo) | shelf |
| T-0026 | 2026-09-30 | [Parrot](https://github.com/turantekin/Parrot) | Source for the capture and co-pilot design. | H-0072 (Show HN: Parrot – Open-Source Smart Meeting Record) | shelf |
| T-0025 | 2026-09-30 | [tau-bench](https://github.com/sierra-research/tau-bench) | The benchmark family the layer sits over. | H-0069 (UserProxyBench: Evaluating LLM User Simulators for) | shelf |
| T-0024 | 2026-09-30 | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Native reverse engineering. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0023 | 2026-09-30 | [ILSpy](https://github.com/icsharpcode/ILSpy) | Decompiler for .NET games. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0022 | 2026-09-30 | [universal-modder](https://github.com/rehan-remade/universal-modder) | The plugin and um CLI. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0021 | 2026-09-30 | [C2PA c2patool](https://github.com/contentauth/c2patool) | Embed and inspect provenance metadata for disclosure. | H-0066 (Consistent AI character content with clear AI disc) | shelf |
| T-0020 | 2026-09-30 | [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) | Simulation benchmark the paper builds on. | H-0064 (MotorMind: Scaffolding General Vision Language Mod) | shelf |
| T-0019 | 2026-09-30 | [coucou](https://github.com/Louis-CFM/coucou) | Source to read for the hook event format. | H-0063 (Louis-CFM/coucou: A tiny friend that lives in your) | shelf |
| T-0018 | 2026-09-30 | [llama.cpp llama-bench](https://github.com/ggml-org/llama.cpp) | Baseline benchmark tool with fixed settings. | H-0062 (Launch HN: Magnitude (YC S25) – Self-optimizing in) | shelf |
| T-0017 | 2026-09-30 | [Magnitude](https://github.com/magnitudedev/magnitude) | The engine under test. | H-0062 (Launch HN: Magnitude (YC S25) – Self-optimizing in) | shelf |
| T-0016 | 2026-09-30 | [Wayback Machine CDX API](https://archive.org/help/wayback_api.php) | Independent timestamps for when a call was published. | H-0061 (Learning crypto research from a source with an ind) | shelf |
| T-0015 | 2026-09-29 | [Playwright](https://github.com/microsoft/playwright) | Headless Chromium frame capture. | H-0059 (Barty-Bart/motion-graphics: Motion-graphics skills) | shelf |
| T-0014 | 2026-09-29 | [motion-graphics](https://github.com/Barty-Bart/motion-graphics) | The skill, engine and worked example. | H-0059 (Barty-Bart/motion-graphics: Motion-graphics skills) | shelf |
| T-0013 | 2026-09-29 | [OpusClip alternatives: ClipsAI](https://github.com/ClipsAI/clipsai) | Open-source library that finds clip-worthy segments in long video. | H-0058 (Post-production for businesses that have long-form) | shelf |
| T-0012 | 2026-09-29 | [ffmpeg](https://ffmpeg.org/) | Cutting, cropping to vertical, and burning captions. | H-0058 (Post-production for businesses that have long-form) | shelf |
| T-0011 | 2026-09-29 | [arXiv 2609.35738](https://arxiv.org/abs/2609.35738) | Check for a linked code release and the evaluation sets. | H-0056 (Harness Learning Enables Generalizable Test-Time A) | shelf |
| T-0010 | 2026-09-29 | [CadQuery](https://github.com/CadQuery/cadquery) | Pure Python parametric CAD that an agent can drive with no GUI or licence. | H-0055 (CaptureGrubEnchant/SolidWorks: SolidWorks MCP Serv) | shelf |
| T-0009 | 2026-09-29 | [FreeCAD](https://github.com/FreeCAD/FreeCAD) | Free CAD with a Python API on macOS, a safe place to try the same agent-drives-CAD idea. | H-0055 (CaptureGrubEnchant/SolidWorks: SolidWorks MCP Serv) | shelf |
| T-0008 | 2026-09-29 | [Meta Ad Library](https://www.facebook.com/ads/library/) | Public data for seeing what a brand's competitors run before pitching. | H-0054 (Media-buying commission taken as a share of a bran) | shelf |
| T-0007 | 2026-09-29 | [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) | The task suite whose traces the paper evaluates on. | H-0052 (TokenCast: Forecasting Token Consumption During LL) | shelf |
| T-0006 | 2026-09-29 | [TokenCast](https://github.com/DEFENSE-SEU/TokenCast) | The paper's code and evaluation scripts. | H-0052 (TokenCast: Forecasting Token Consumption During LL) | shelf |
| T-0005 | 2026-09-29 | [tmux](https://github.com/tmux/tmux) | Simplest way to keep many agent sessions alive and inspectable. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0004 | 2026-09-29 | [node-pty](https://github.com/microsoft/node-pty) | Pseudo-terminal spawning for a home-built supervisor. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0003 | 2026-09-29 | [agent-office](https://github.com/AgentSystemLabs/agent-office) | Read docs/how-it-works.md for the waiting-state detection. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0002 | 2026-09-29 | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Fast local transcription on the Mac if the current local pipeline is slow. | H-0049 (Join for one month with Skool neptune, transcribe ) | shelf |
| T-0001 | 2026-09-29 | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Pulls embedded lesson videos (Loom, Vimeo, YouTube) that a Skool classroom links to. | H-0049 (Join for one month with Skool neptune, transcribe ) | shelf |

## Skipped

| id | date | source | what | why |
|---|---|---|---|---|
| H-0128 | 2026-10-04 | hn | [Ask HN: Is anybody producing good code with coding agents?](https://news.ycombinator.com/item?id=49934037) | An opinion thread on code quality from coding agents, with no testable mechanism. |
| H-0126 | 2026-10-04 | youtube | [3 most common reasons your car could fail its MOT in the UK!](https://www.youtube.com/watch?v=zq65xVu3iq8) | A thirty-second listicle of common MOT failures with no mechanism or data source. |
| H-0123 | 2026-10-04 | hn | [Show HN: Our space game has a built-in RISC-V emulator that runs Linux](https://againstallodds.games/blog/2026/10/03/our-risc-v-emulator-pasriscv/) | A game's RISC-V emulator write-up, interesting engineering but no mechanism relevant to any desk. |
| H-0121 | 2026-10-04 | youtube | [Stop Losing Trades: Why I Switched to PumpSniper / Solana Sniper BOT](https://www.youtube.com/watch?v=YCYkK0yUBXA) | A promotional video for a sniper bot, with unverified claims and no mechanism beyond buzzwords. |
| H-0118 | 2026-10-04 | hn | [Show HN: Thoreau BASIC – What if BASIC hadn't gone out of fashion?](https://thoreaubasic.com/) | A BASIC interpreter showcase with no bearing on any desk or interest. |
| H-0115 | 2026-10-03 | github | [TimMacy/YouTubeAlchemy: This userscript for YouTube offers 250+ layout changes a](https://github.com/TimMacy/YouTubeAlchemy) | A browser UI userscript; its transcript export is clipboard and DOM scraping that the keyless pipeline already covers. |
| H-0114 | 2026-10-03 | hn | [Show HN: Pi pod – Run your pi coding agent in sandboxes on your own server](https://pipod.dev/) | Self-hosted sandbox for one coding agent; comments say it matches running a container, with no new mechanism. |
| H-0112 | 2026-10-03 | youtube | [Building an MCP server in 2 minutes....](https://www.youtube.com/watch?v=Fhy_VFMlE9s) | Generic two-minute MCP server tutorial. |
| H-0109 | 2026-10-03 | hn | [Show HN: Offrun – manage every coding agent from one workspace](https://offrun.dev/) | Product launch for an agent dashboard; claim only, comments ask what it adds over existing tools. |
| H-0107 | 2026-10-03 | youtube | [Claude Code: The Advanced Guide (99% of Devs Skip These Features)](https://www.youtube.com/watch?v=kt5a-TXmWew) | Beginner listicle of Claude Code features Proteus already runs. |
| H-0105 | 2026-10-03 | github | [nykooi1/vibe-wise: A Claude Code plugin that helps you learn how to build while ](https://github.com/nykooi1/vibe-wise) | A teaching-style plugin that makes Claude ask for the approach first; no mechanism Proteus needs beyond ordinary skills  |
| H-0104 | 2026-10-03 | hn | [Getting the most out of Opus 5.5 in Claude and Claude Code](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) | Opinion thread praising a model with anecdotes and no mechanism. |
| H-0102 | 2026-10-02 | youtube | [Why Cars Lose Their Value So Fast](https://www.youtube.com/watch?v=Ao7fbajRSKI) | No transcript came back (IpBlocked) and a generic news explainer carries no mechanism. |
| H-0097 | 2026-10-02 | youtube | [Tutorial 1: Getting Started with the UK Data Service Open Data API](https://www.youtube.com/watch?v=JIh6h8mx0Zk) | No transcript came back (IpBlocked) and a beginner tutorial title gives no mechanism. |
| H-0096 | 2026-10-02 | github | [zlxlabs/VideoTranscriptAPI: 基于 Python 3.11+ FastAPI 的异步音视频转录服务，支持 YouTube、小宇宙、Bi](https://github.com/zlxlabs/VideoTranscriptAPI) | Duplicates the transcript pipeline already in the stack and its parsing depends on a paid referral API key. |
| H-0093 | 2026-10-02 | awesome | [dailydotdev/daily (new in awesome-claude-code)](https://github.com/dailydotdev/daily) | Vault has judged the vendor and the README shows a standard tag-based news feed with nothing new. |
| H-0092 | 2026-10-02 | youtube | [Agent memory architecture explained #agentmemory #workingmemory #episodicmemory](https://www.youtube.com/watch?v=Ir0Q9s6P050) | No transcript came back (IpBlocked) and the title alone carries no mechanism. |
| H-0088 | 2026-10-01 | youtube | [What is a Bonding Curve? Explained in Less Than 1 Minute! #defi #daos #blockchai](https://www.youtube.com/watch?v=LI8WkvWpJJc) | A one-minute generic explainer of bonding curves with no mechanism beyond the definition the Grinder already covers. |
| H-0081 | 2026-10-01 | hn | [Show HN: Strata – an expressive semantic layer that can say no to your LLM](https://strata.do/) | A product pitch for a semantic layer with claims but no inspectable mechanism beyond naming rules. |
| H-0074 | 2026-09-30 | youtube | [Chess Engine in Python - Part 2 - Moving the pieces](https://www.youtube.com/watch?v=o24J3WcBGLg) | Beginner tutorial on mouse input for a chess GUI, no mechanism relevant to a bot. |
| H-0067 | 2026-09-30 | hn | [Show HN: A working 3D model of an Enigma machine](https://enigma.design) | A 3D explainer site with no reusable mechanism beyond prompt-built models. |
| H-0065 | 2026-09-30 | youtube | [day in the life of a wfh data analyst.](https://www.youtube.com/watch?v=RC30UibhowE) | Lifestyle vlog with no transcript and no mechanism. |
| H-0060 | 2026-09-29 | youtube | [Building a Real App with Claude Code (Start to Finish)](https://www.youtube.com/watch?v=misjUj4Q_ho) | Transcript unavailable and a generic build-an-app tutorial with no mechanism to record. |
| H-0057 | 2026-09-29 | youtube | [MCP Servers Explained & Built](https://www.youtube.com/watch?v=He8tUwLzLnU) | Transcript unavailable and a generic MCP tutorial title with no mechanism to record. |
| H-0053 | 2026-09-29 | youtube | [Claude Code Full Course 2026 / How Senior Engineers Actually Build with AI](https://www.youtube.com/watch?v=u2QqWkMv3Lg) | Transcript unavailable and the title is a generic beginner course claim with no mechanism. |
| H-0050 | 2026-09-29 | hn | [Show HN: Durable Actor Session Protocol](https://dasp-protocol.github.io/dasp/) | The post text names a protocol and its motivation but gives no mechanism, and the comments show the author has not yet a |
| H-0047 | 2026-09-28 | youtube | [Car Depreciation Explained and How to Beat it](https://www.youtube.com/watch?v=XWz0HiXVrIY) | Generic consumer advice with a lender's marketing claims and no mechanism or data source; its own example figures are on |
| H-0044 | 2026-09-28 | youtube | [Open Data - How do I connect data using API](https://www.youtube.com/watch?v=_00jicHRIKk) | A three minute how-to for one portal that needs an account and API key, with no mechanism beyond a CSV export link. |
| H-0041 | 2026-09-28 | hn | [Show HN: PaperMono, e-ink fridge magnet shopping list with mobile web page](https://github.com/seamusc/papermono-shopping-list) | A hobby build on specific hardware with no mechanism beyond an ESP32 web sync, and the author says it was vibe-coded. |
| H-0035 | 2026-09-27 | hn | [OpenAI Codex agents go rogue and consumes USD 78,000 without authorization](https://news.ycombinator.com/item?id=49861047) | Single unverified user anecdote with no mechanism, logs or reproduction, essentially a claim dressed as news. |
| H-0028 | 2026-09-27 | youtube | [Mac mini M6: is 32GB enough to run local AI?](https://www.youtube.com/watch?v=6z9PbFSkX3g) | Recap of Apple's own announced specs with no independent benchmark; the memory-bandwidth point is general knowledge, not |
| H-0026 | 2026-09-27 | github | [ZeroPointRepo/youtube-skills: YouTube Transcript API skills for AI agents. Get t](https://github.com/ZeroPointRepo/youtube-skills) | Marketing wrapper around an opaque hosted API (TranscriptAPI), no technical detail on how it actually gets transcripts,  |
| H-0024 | 2026-09-26 | hn | [Ask HN: I just talked to an AI-obsessed client, and I need a shower afterwards](https://news.ycombinator.com/item?id=49826029) | Anecdotal complaint thread about a client's plans for AI marketing and review automation, no technical mechanism describ |
| H-0023 | 2026-09-26 | youtube | [Chess Engine in Python - Part 1 - Drawing the board](https://www.youtube.com/watch?v=EnYui0e73Rs) | Part 1 of a beginner tutorial series covering only pygame board setup and piece images, no engine logic yet. |
| H-0020 | 2026-09-26 | youtube | [Nearly one third of all MOTs in the UK failed this year 😳 here are the top 5 rea](https://www.youtube.com/watch?v=QigAkv4Ion0) | Generic top-5 MOT failure listicle with anecdotal advice and no cited data source, just a presenter's opinion. |
| H-0016 | 2026-09-26 | youtube | [PumpFun Sniper Bot Guide! / How to Snipe Memecoins / Solana Sniper Bot EXPLAINED](https://www.youtube.com/watch?v=X6fE1C3IKRw) | Promotional walkthrough of a Solana sniper bot's UI and pricing tiers with no explanation of how listing detection or ex |
| H-0011 | 2026-09-26 | youtube | [What does my MOT result mean](https://www.youtube.com/watch?v=gRRWBTRwmTQ) | Generic consumer explainer of MOT pass/fail categories with no mechanism, tool or number to record. |
| H-0008 | 2026-09-26 | youtube | [How to make lichess bot](https://www.youtube.com/watch?v=oTuZrYCpxNU) | Auto-captions and a direct page re-fetch both returned only music and boilerplate, no recoverable technical content to r |
