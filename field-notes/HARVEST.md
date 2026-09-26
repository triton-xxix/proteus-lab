# Harvest register

One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in
`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the
source says) and whether it is **testable** keyless tonight; testable ones are queued in `PROBES.md` with source
`harvest`. A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.

12 judged over 1 harvest days, 10 kept, 1 testable, 1 queued as probes, 0 with a probe verdict.

## Kept

| id | date | source | what | lens | interest | testable | probe |
|---|---|---|---|---|---|---|---|
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
| H-0011 | 2026-09-26 | youtube | [What does my MOT result mean](https://www.youtube.com/watch?v=gRRWBTRwmTQ) | Generic consumer explainer of MOT pass/fail categories with no mechanism, tool or number to record. |
| H-0008 | 2026-09-26 | youtube | [How to make lichess bot](https://www.youtube.com/watch?v=oTuZrYCpxNU) | Auto-captions and a direct page re-fetch both returned only music and boilerplate, no recoverable technical content to r |
