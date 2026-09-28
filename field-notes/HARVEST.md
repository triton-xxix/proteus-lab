# Harvest register

One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in
`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the
source says) and whether it is **testable** keyless tonight; testable ones are queued in `PROBES.md` with source
`harvest`. A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.

48 judged over 3 harvest days, 36 kept, 11 testable, 11 queued as probes, 6 with a probe verdict.

## Kept

| id | date | source | what | lens | interest | testable | probe |
|---|---|---|---|---|---|---|---|
| H-0048 | 2026-09-28 | hn | [Show HN: OpenAPPA – open-source deterministic guardrails that don't break agents](https://www.openappa.com/) | both | mechanism-hunting | no: Reproducing the benchmarks needs LLM agent runs, and the num |  |
| H-0046 | 2026-09-28 | github | [jkawamoto/mcp-youtube-transcript: MCP server retrieving transcripts of YouTube videos](https://github.com/jkawamoto/mcp-youtube-transcript) | mechanism | tools-for-strangers | yes | P-0031 |
| H-0045 | 2026-09-28 | hn | [Launch HN: Vespper (YC F24) – SOTA Docx MCP](https://www.vespper.com/blog/launching-vespper-docx-mcp) | both | tools-for-strangers | no: Needs a Vespper account and its hosted model, and the benchm |  |
| H-0043 | 2026-09-28 | arxiv | [A Safety-Bounded SDC-to-MCP Gateway for Medical AI Agents](https://arxiv.org/abs/2609.31358) | mechanism | mechanism-hunting | no: Needs SDC device simulators and the authors' prototype, whic |  |
| H-0042 | 2026-09-28 | github | [samyost1/3dicon: One prompt in, a looping animated 3D icon out — with real transparency. A](https://github.com/samyost1/3dicon) | mechanism | tools-for-strangers | no: The pipeline needs an OpenRouter key and paid image and vide |  |
| H-0040 | 2026-09-28 | youtube | [Agent Memory EXPLAINED - Complete Architecture](https://www.youtube.com/watch?v=aYfZN8t6AQs) | mechanism | mechanism-hunting | no: Running Mem0 needs an LLM for fact extraction, and no 30 min |  |
| H-0039 | 2026-09-28 | arxiv | [Structured Reasoning Agentic Framework for Interpretable Critical View of Safety Assessmen](https://arxiv.org/abs/2609.31524) | mechanism | tech | no: Needs the benchmark data and trained models, and no runnable |  |
| H-0038 | 2026-09-28 | github | [lemomo-ai/lemo-opuscar: 39 film styles, each a reusable style prompt plus a short film mad](https://github.com/lemomo-ai/lemo-opuscar) | mechanism | tools-for-strangers | no: Directing a film needs a Claude agent run against the skill, |  |
| H-0037 | 2026-09-28 | hn | [Show HN: HN.watch – Videos of all Hacker News posts](https://hn.watch/) | both | tools-for-strangers | yes | P-0030 |
| H-0036 | 2026-09-27 | github | [alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interacti](https://github.com/alexgreensh/anidoodle) | mechanism | tools-for-strangers | yes | P-0028 |
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
| H-0014 | 2026-09-26 | github | [JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P](https://github.com/JohnHeibel/PDoomVideo) | mechanism | mechanism-hunting | yes | P-0021 |
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

## Skipped

| id | date | source | what | why |
|---|---|---|---|---|
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
