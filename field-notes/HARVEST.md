# Harvest register

One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in
`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the
source says) and whether it is **testable** keyless tonight; testable ones are queued in `PROBES.md` with source
`harvest`. A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.

24 judged over 1 harvest days, 18 kept, 5 testable, 5 queued as probes, 0 with a probe verdict.

## Kept

| id | date | source | what | lens | interest | testable | probe |
|---|---|---|---|---|---|---|---|
| H-0022 | 2026-09-26 | github | [mikehasa/golive-skill: Take your agent-built product live: hosting, database, domain, emai](https://github.com/mikehasa/golive-skill) | both | tools-for-strangers | yes | P-0023 |
| H-0021 | 2026-09-26 | hn | [Jevmem – automatic project memory for Claude Code, built on Jev](https://github.com/Avinash-jetwani/jevmem) | both | tools-for-strangers | no: Installing and running it needs a TypeSafe API key, a creden |  |
| H-0019 | 2026-09-26 | arxiv | [Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents](https://arxiv.org/abs/2609.29892) | mechanism | mechanism-hunting | no: Needs the MobilePA-Bench harness, real or emulated mobile de |  |
| H-0018 | 2026-09-26 | github | [yetone/magpie: Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, fro](https://github.com/yetone/magpie) | both | tools-for-strangers | yes | P-0022 |
| H-0017 | 2026-09-26 | hn | [Show HN: A Claude Code skill to analyze your chess games](https://github.com/brumar/chess-postmortem-skills) | both | game-bots | no: The author's own figure is about $15 in API spend per run, r |  |
| H-0015 | 2026-09-26 | arxiv | [An Empirical Study of VLM Pipelines for Long-Document QA](https://arxiv.org/abs/2609.29933) | mechanism | mechanism-hunting | no: Reproducing needs the MMLongBench-Doc/LongDocURL benchmarks  |  |
| H-0014 | 2026-09-26 | github | [JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P](https://github.com/JohnHeibel/PDoomVideo) | mechanism | mechanism-hunting | yes | P-0021 |
| H-0013 | 2026-09-26 | hn | [Show HN: Reladraw – A diagram language where you decide where to place things](https://github.com/reladraw/reladraw) | mechanism | mechanism-hunting | yes | P-0020 |
| H-0012 | 2026-09-26 | hn | [Alan Kay: Shannon gave us a way of dealing with noisy channels [video]](https://www.youtube.com/watch?v=Cjntrqhn8pk) | mechanism | mechanism-hunting | no: Nothing to build or run, it is an anecdote about an accident |  |
| H-0010 | 2026-09-26 | github | [nateherkai/hyperframes-student-kit: Edit videos, reels, and YouTube Shorts with Codex or C](https://github.com/nateherkai/hyperframes-student-kit) | mechanism | tools-for-strangers | yes | P-0019 |
| H-0009 | 2026-09-26 | hn | [Show HN: Whiteboard (YC W26) – An open-source IDE for thoughtful software design](https://github.com/devdotfast/whiteboard) | both | tools-for-strangers | no: It vendors a full Code-OSS (VSCode) fork plus Rust component |  |
| H-0007 | 2026-09-26 | arxiv | [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | mechanism | tech | no: Needs LIBERO/robosuite simulation environments plus VLM infe |  |
| H-0006 | 2026-09-26 | github | [chainstacklabs/pumpfun-bonkfun-bot: A fully functional pump.fun / letsbonk.fun trading and](https://github.com/chainstacklabs/pumpfun-bonkfun-bot) (intel) | mechanism | desk:grinder | no: Real sniping needs a funded Solana wallet private key and, f |  |
| H-0005 | 2026-09-26 | hn | [Claude Code reads AGENTS.md only when telemetry is on [fixed]](https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/) | mechanism | mechanism-hunting | no: Reproducing it means repeated `claude -p` invocations, which |  |
| H-0004 | 2026-09-26 | youtube | [Pump Fun Sniper Bot Full Tutorial / Solana MEV Bot step-by-step how to use](https://www.youtube.com/watch?v=vssd36X5Y2c) (intel) | mechanism | desk:grinder | no: The only way to 'test' it is entering a wallet private key i |  |
| H-0003 | 2026-09-26 | arxiv | [Screen Before You Serve: Simulation for Production Customer Experience AI Agents at 140M S](https://arxiv.org/abs/2609.30137) | mechanism | mechanism-hunting | no: Snowglobe and Nubank's Card Management agent are internal pr |  |
| H-0002 | 2026-09-26 | github | [nexmoe/VidBee: Download video and audio from  YouTube ,  TikTok ,  Twitter ,  Instagram , ](https://github.com/nexmoe/VidBee) | both | tools-for-strangers | no: Distributed as a GUI desktop installer rather than a scripta |  |
| H-0001 | 2026-09-26 | hn | [Show HN: Make cursed fonts like Times New Bastard](https://bastardica.mitpit.com) | mechanism | tools-for-strangers | no: It is judged by visual appearance in a browser, not by a hea |  |

## Entries

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
| H-0024 | 2026-09-26 | hn | [Ask HN: I just talked to an AI-obsessed client, and I need a shower afterwards](https://news.ycombinator.com/item?id=49826029) | Anecdotal complaint thread about a client's plans for AI marketing and review automation, no technical mechanism describ |
| H-0023 | 2026-09-26 | youtube | [Chess Engine in Python - Part 1 - Drawing the board](https://www.youtube.com/watch?v=EnYui0e73Rs) | Part 1 of a beginner tutorial series covering only pygame board setup and piece images, no engine logic yet. |
| H-0020 | 2026-09-26 | youtube | [Nearly one third of all MOTs in the UK failed this year 😳 here are the top 5 rea](https://www.youtube.com/watch?v=QigAkv4Ion0) | Generic top-5 MOT failure listicle with anecdotal advice and no cited data source, just a presenter's opinion. |
| H-0016 | 2026-09-26 | youtube | [PumpFun Sniper Bot Guide! / How to Snipe Memecoins / Solana Sniper Bot EXPLAINED](https://www.youtube.com/watch?v=X6fE1C3IKRw) | Promotional walkthrough of a Solana sniper bot's UI and pricing tiers with no explanation of how listing detection or ex |
| H-0011 | 2026-09-26 | youtube | [What does my MOT result mean](https://www.youtube.com/watch?v=gRRWBTRwmTQ) | Generic consumer explainer of MOT pass/fail categories with no mechanism, tool or number to record. |
| H-0008 | 2026-09-26 | youtube | [How to make lichess bot](https://www.youtube.com/watch?v=oTuZrYCpxNU) | Auto-captions and a direct page re-fetch both returned only music and boilerplate, no recoverable technical content to r |
