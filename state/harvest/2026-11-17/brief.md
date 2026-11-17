# Harvest brief, 2026-11-17

14 items shortlisted from 395 candidates (303 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] AI receptionist demo for trades
key: vault:2026-11-17:ai-receptionist-demo-for-trades
url: https://www.youtube.com/watch?v=Th7B9eLRdGs
meta: {"vault_status": "open", "kind": "service", "subject": "Construction broker vlog (YouTube, SETH Coaching)", "date": "2026-11-17", "where": "TRITON-CORE/Research/links/2026-11-17-construction-broker-vlog.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: answer, qualify, book the site visit and brief the builder: the step the vlog shows missing (most leads unbooked or dead)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Coaching promo vlog, claims unverified; the lead-to-booked-job gap it shows is the live idea for a trades AI receptionist demo Write-up: `TRITON-CORE/Research/links/2026-11-17-construction-broker-vlog.md` Link: https://www.youtube.com/watch?v=Th7B9eLRdGs

## 2. [hn] How the Claude Code team thinks about verification
key: hn:50529612
url: https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/
discussion: https://news.ycombinator.com/item?id=50529612
meta: {"points": 249, "comments": 194, "created": "2026-11-17T10:20:40Z"}
query: claude code

comment (dude250711): > ...On the Claude Code team, the vast majority of our code (~90%) is written and reviewed by Claude... I am more interested in the remaining 10%.
comment (girvo): > With them, you can run dozens or hundreds in parallel. Im already spending my $2k usd per month in tokens with just one or two agents. How do they expect me to do that?
comment (Ampersander): Why is the team thinking? Their product should be doing that for them

## 3. [github] erkamyaman/rust-anything: Rewrite your whole app in Rust, one piece at a time, checked against the original's recorded behavior at every step. CLIs, HTTP servers and libraries in TypeScript, Python, C, Go, Ruby and Java.
key: gh:erkamyaman/rust-anything
url: https://github.com/erkamyaman/rust-anything
meta: {"stars": 1200, "created": "2026-11-16", "pushed": "2026-11-17", "language": "Rust", "topics": ["agent-skills", "claude-code", "cli", "code-migration", "codex", "ffi", "golang", "java"]}
query: claude-code created:>{since} stars:>20

rust-anything 

  Rewrite your whole app in Rust. Keep it working the whole way.  

  CLIs, servers and libraries, piece by piece, checked against the original at every step.  

 
     
     
   
     
     
     
     
 

 up to 20x faster · 38,251 recorded cases replayed · 0 mismatches · one command 

**Rewrite your whole app in Rust, one piece at a time.** rust-anything records what your
TypeScript/JavaScript, Python, C, Go, Ruby or Java app does today, then checks every piece of the
Rust rewrite against that recording before it moves on, until the app is pure Rust. CLIs, HTTP
servers and libraries; your coding agent (or you) writes the Rust. It can only catch what the
recording covers: see [What it can't catch](#what-it-cant-catch). Only need the slow part fast?
Port just that, one hot path at a time:

| Real workload, same results as the original | Original | With rust-anything |
| --- | ---: | ---: |
| x18n's sidebar search, 50,000 keys (TypeScript, Node) | 10 ms per query | **0.5 ms: 20x faster** |
| The same search in the browser (wasm, one thread) | 10 ms | **0.95 ms: 11.5x** |
| `slugify` over 20,000 strings (Python) | 98 ms | **17x faster** |
| `Shellwords.shellescape` from Ruby's standard library, 50,000 values | 88 ms | **11.8x faster** |
| `Slugify` over 50,000 strings (Go) | 49 ms | **4x faster** |
| `slugify` over 50,000 strings (Java) | 43 ms | **3x faster** |

 
   
 

Measured on 4 cores; every number has a benchmark in [`demo/`](./demo) that first checks the
results are identical. Calling Rust once per small function is usually *slower* than a JIT;
rust-anything finds the loop worth moving, and moves it.

> rust-anything is an independent project, not affiliated with or endorsed by the Rust Project
> or the Rust Foundation. "Rust" is a trademark of the Rust Foundation.

## Quick start

Paste this into Claude Code, Codex, Cursor or Gemini CLI and let your agent install it:

```text
Install rust-anything: run `cargo install rust-anything`, then `rust-anything setup`.
Tell me when to restart you.
```

Or yourself:

```sh
cargo install rust-anything   # from crates.io
rust-anything setup           # registers it with Claude Code, Codex, Cursor and Gemini CLI
```

No Rust toolchain yet? Prebuilt binaries for macOS, Linux and Windows are attached to each
[GitHub release](https://github.com/erkamyaman/rust-anything/releases), and for JavaScript
projects `npm install -g rust-anything` installs the same binary.

In Claude Code you can also install it as a plugin (the MCP server and the skill; the CLI above
must be on your `PATH`):

```text
/plugin install rust-anything --marketplace erkamyaman/rust-anything
```

`setup` adds the MCP server to each agent it finds and installs the workflow skill where the agent
reads skills. It keeps your other settings, is safe to run again, and `--remove` undoes it.
Then ask your agent, for example:

- *"Rewrite this CLI in Rust with rust-anything, end to end, and prove it behaves the same."*
- *"This search feels slow. Profile it with rust-anything and move the hot loop to Rust."*
- *"Plan a migration of `src/parser/` to Rust with rust-anything; port the first unit and prove it."*
- *"Bench the Rust port in `rust/text-rs` against the original and tell me whether to ship it."*

### Works with

| Agent | `rust-anything setup` adds |
| --- | --- |
| Claude Code | MCP server in `~/.claude.json`, skill in `~/.claude/skills/` |
| Codex | MCP server in `~/.codex/config.toml`, skill in `~/.codex/ski

## 4. [arxiv] When Tool Names Are Not Identities: Measuring Provider Misbinding in MCP-Based AI Agents
key: arxiv:2611.21577
url: https://arxiv.org/abs/2611.21577
meta: {"published": "2026-11-16", "authors": ["Zeynab Anbiaee", "Sajjad Dadkhah", "Ali A. Ghorbani"], "categories": ["cs.CR", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM) applications increasingly act as agents that select and invoke external tools. The Model Context Protocol (MCP) standardizes this interaction by allowing clients to compose tools advertised by multiple servers. However, tool metadata used for discovery and selection is not, by itself, necessarily bound to a verified provider identity. This paper studies this gap as tool-provider misbinding: a failure in which a request intended for a legitimate provider is instead resolved to an attacker-controlled tool. The attacker does not compromise the host, LLM, legitimate server, or network channel; it only operates another MCP server that advertises tools with chosen metadata. We formulate tool provider misbinding as an attacker-controlled tool-selection optimization problem and evaluate it in a controlled MCP environment across five LLM-based clients. The results show that interactions drive misbinding. The strongest failures occur when exact-name collision, task-aligned description, and compatible schema reinforce one another, but authority-enhanced descriptions with compatible schema can also cause wrong-provider execution or unresolved provider ambiguity without name collision. Different models expose the same provider-binding weakness differently, including attacker-controlled provider selection, clarification requests, and unstable or inconsistent provider resolution.

## 5. [youtube] DVSA Data Exposes 10 Everyday Cars Failing UK MOTs at Record Rates – Is Yours on the List?
key: yt:v_w3yeLQHro
url: https://www.youtube.com/watch?v=v_w3yeLQHro
meta: {"channel": "The Vehicle Guide", "rank": 1, "duration_min": 23}
query: MOT data analysis uk

# DVSA Data Exposes 10 Everyday Cars Failing UK MOTs at Record Rates – Is Yours on the List?
# The Vehicle Guide
# https://www.youtube.com/watch?v=v_w3yeLQHro

[00:00] On a frosty Wednesday morning, inside an independent MOT testing station on the outskirts of Leeds, a 7-year-old family crossover sits raised 6 ft in the air on a hydraulic four-post inspection lift. Upstairs in the customer waiting room, the owner is checking her watch, expecting to pay the standard £54.85 test fee and drive straight to work. Down in the workshop bay, however, the DVSA authorized tester is tapping the underside of the front radiator subframe with his corrosion assessment tool. Instead of ringing like solid steel, the
[00:33] metal crunches like wet cardboard, showering rust flakes onto the workshop floor. 5 minutes later, the tester prints out a refusal sheet stamped with the four words every British motorist dreads, "Fail. Dangerous. Do not drive until repaired." The welding, replacement subframe, C suspension bolts, and four-wheel laser alignment bill comes to £2,640. Across Great Britain, more than 32 million MOT tests are carried out every single year under the watchful eye of the Driver and Vehicle Standards Agency.
[01:07] And right now, nearly one in three cars entering a British testing bay fails on the first attempt. Here is what surprises most drivers. The cars racking up the most expensive, heart-stopping MOT failure bills in the United Kingdom are not 30-year-old bangers sitting in a barn. They are 5-year-old to 10-year-old everyday hatchbacks, crossovers, and prestige saloons parked on every suburban street in Britain. Vehicles that look gleaming and rust-free on the outside, while Britain's damp winters, rock salt gritting lorries, and pothole-scarred
[01:39] roads quietly devour their suspension arms, brake pipes, and structural subframes underneath. Today, we are counting down the 10 everyday cars on British roads that trigger the most frequent and shockingly expensive MOT failures. From number 10 right down to number one, backed by DVSA defect data and real UK workshop invoices. For every model on this list, we will show you the exact hidden weak spot the tester looks for on the ramp, how to inspect it with a torch before you buy a used example. And at the end of the video, we will
[02:11] walk through the 15-minute driveway pre-MOT check that prevents half of all British test failures for less than £10. Before we begin counting down from number 10, a quick 10-second favor. Over 50,000 British motorists have watched our recent investigations. Yet, we currently have just 261 subscribers as we work towards our first milestone of 1,000. If our guides help you avoid expensive workshop traps, please press that free subscribe button right below. It takes 2 seconds and keeps our independent UK research going. Now, let
[02:44] us get straight into number 10. Number 10, the Fiat 500 and Abarth 595, built from 2008 right through to the present day. Drive down any high street in Britain and you will spot a dozen Fiat 500s within 5 minutes. Charming, easy to park and cheap to insure, it remains a perennial favorite for first-time drivers and city commuters. Put a 6-year-old Fiat 500 up on a British MOT ramp, however, and every experienced tester knows the exact three places to shine their inspection lamp before even touching the brakes.
[03:17] Weakness number one is the front lower suspension wishbone arm. Because the Fiat 500 uses a short wheelbas
[transcript continues in field-notes/staging/v_w3yeLQHro.txt]

## 6. [awesome] a5768549/model-worker-mcp (new in awesome-mcp-servers)
key: gh:a5768549/model-worker-mcp
url: https://github.com/a5768549/model-worker-mcp
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-10-19", "language": "JavaScript", "description": "MCP server delegating bounded coding tasks to an OpenAI-compatible model: explicit read/write paths, diff validation, risk-based routing."}
query: awesome-mcp-servers

# Model Worker MCP

本機、受限範圍的 coding worker MCP。它只接受明確的 `cwd`、`read_paths`、`write_paths`，將 provider 回傳的 unified diff 在套用前驗證，並可執行指定驗證命令。

## 設定

1. 在使用者環境變數設定 `MODEL_WORKER_API_KEY`，或執行 `npm run credentials:set -- worker-primary`（Windows DPAPI 加密儲存）。
2. 設定 `MODEL_WORKER_BASE_URL`（任何 OpenAI-compatible `/chat/completions` endpoint，預設為阿里雲百煉 `https://dashscope.aliyuncs.com/compatible-mode/v1`；若使用百煉專屬 workspace，改成自己的 workspace endpoint）與 `MODEL_WORKER_MODEL`。預設主力是 `qwen3.7-plus`；單檔小修改可切換為 `qwen3.6-flash`。`deepseek-flash-0731` 會自動用於中低風險程式邏輯、bug 修復、測試與後端小功能，也支援手動指定。模型名稱與價格表在 `worker/router.js`、`worker/usage-store.js`，換 provider 時一併調整。
3. `.mcp.json` 以相對路徑啟動 `server/server.js`；若你的 MCP client 不支援 `cwd`，把 `args` 改成此目錄的絕對路徑。

需求：Node.js 18 以上、Git（diff 以 `git apply` 套用，`cwd` 必須是 Git repository）；驗證命令與 credential 加密目前透過 Windows PowerShell 執行。

## 本機測試

```powershell
node server/server.js
```

MCP 工具：`route_code_task`、`delegate_code_task`、`get_task_status`、`cancel_task`、`get_usage_summary`。優先呼叫 `route_code_task`：CSS／文案／文件等低複雜度任務走 `qwen3.6-flash`；中低風險程式邏輯、bug 修復、測試與後端小功能走 `deepseek-flash-0731`；一般或跨檔 coding 走 `qwen3.7-plus`；審查走 `glm-5.2`。涉及 auth、payment、secret、migration、database、部署或正式環境時只回傳 `guarded`，不會自動委派。每個任務的 token、估算費用與失敗錯誤摘要會持久化到 `%LOCALAPPDATA%\CodexModelWorker\usage.json`，可用 `get_usage_summary` 查詢。DeepSeek 價格尚未填入，因此其費用會標為未知，不會猜算。錯誤內容會遮罩 `Bearer` 與 `sk-` 字串，API key 不會出現在設定檔、任務參數、diff 或 log 中。

## License

[MIT](LICENSE)

## 7. [vault] speed-to-call and booking for brokers and builders
key: vault:2026-11-17:speed-to-call-and-booking-for-brokers-and-builders
url: https://www.youtube.com/watch?v=Uev0oyU4Z-4
meta: {"vault_status": "open", "kind": "service", "subject": "How I Get Paid Remotely in 2027 (SETH Coaching)", "date": "2026-11-17", "where": "TRITON-CORE/Research/links/2026-11-17-construction-broker-day-in-life.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: first-minute answer, qualify, route by area and job type is the lever the video shows

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Coaching promo, claims unverified; lead qualification and speed-to-call detail feeds the trades AI receptionist demo Write-up: `TRITON-CORE/Research/links/2026-11-17-construction-broker-day-in-life.md` Link: https://www.youtube.com/watch?v=Uev0oyU4Z-4

## 8. [hn] Launch HN: Axonnic (YC F26) – Sleeves that track fingers and estimate force
key: hn:50522776
url: https://news.ycombinator.com/item?id=50522776
discussion: https://news.ycombinator.com/item?id=50522776
meta: {"points": 55, "comments": 27, "created": "2026-11-16T20:29:48Z"}
query: car data

Hi HN! We’re Arsh and Max, founders of Axonnic ( https://axonnic.com ). We’ve developed a forearm sleeve that reads muscle activity to decode finger movements and estimate fingertip force, while leaving the hands bare. It’s used to record human movement and generate training data for dextrous robots. Here’s a demo video: https://youtube.com/shorts/xBrocTc9cfA We’ve found that electromyography (EMG) is a much better way to train robots than by video alone because video only captures movement, not muscle activity or the effort behind the movement. A useful signal can be present even when the hand barely moves; just maintaining a grip involves muscle activation. The subtle muscle movements that can barely be picked up in video are the most important details for activities like sewing and delicate assembly. The sleeve has 64 channels of surface electromyography, or EMG. Electrodes on the skin detect electrical activity from muscles in the forearm. We distribute sensors across the forearm so as to not overfit to one muscle group. We synchronize EMG with hand tracking to train a model that predicts finger joint angles, then we run the decoder solely from EMG, adding in fingertip force estimates that have been calibrated from finger presses on force sensors. When the user takes the sleeve off then puts it back on again, the electrode positions change, so we run tests over separate wearings. In one case, we ran a 215-second recording, four days after training, without any recalibrati
comment (millspore): How does it handle fatigue shift, like if someone's been gripping stuff for an hour the emg baseline must drift pretty hard
comment (cloakley): [flagged]
comment (Benard-dev): Interesting approach. Been seeing more AI tools that can decompile and annotate binaries almost instantly now — makes old obfuscation feel useless. How are you handling false positives when hardening? Does it break legit reversing tools like Ghidra or just slow down LLM-assisted ones? Curious to try it on a small Go binary I have.

## 9. [github] sybil-solutions/inference-optimisation-skill: Agent skill for hill-climbing local LLM serving speed (decode, speculative decoding, prefill, KV, startup, TTFT) on any hardware and quantization
key: gh:sybil-solutions/inference-optimisation-skill
url: https://github.com/sybil-solutions/inference-optimisation-skill
meta: {"stars": 910, "created": "2026-11-16", "pushed": "2026-11-16", "language": "Python", "topics": ["agent-skill", "benchmarking", "claude-code", "inference", "llm", "speculative-decoding"]}
query: claude-code created:>{since} stars:>20

# inference-optimisation

An agent skill for **hill-climbing the speed of a local LLM server** on any hardware and any quantization. It covers:

- single-user and concurrent decode
- speculative decoding
- prefill
- KV cache size
- startup time and time to first token

It works under a memory cap, and every result has to survive a full-context stability check.

It encodes how we actually got these speedups. It is not a list of flags. The workflow:

1. Compute the theoretical ceiling.
2. Change one thing at a time.
3. Measure against interleaved controls.
4. Log every result, including the failures.
5. Gate on long-context retrieval.
6. Qualify a clean, pinned build before publishing.

It works with Claude Code and any agent that loads `SKILL.md`-style skills. Any model can also follow it from [`PROMPT.md`](PROMPT.md).

## What we've been able to accomplish

Results from the hill-climbs this skill was distilled from. Every number was measured on the hardware named; see the linked sources for methods and raw data.

| Hardware | Model / quant / engine | Before → after |
|---|---|---|
| **Intel Arc B390 iGPU** (laptop, 64 GB unified LPDDR5X, ~115 GB/s) | Ornith-1.5-35B-A3B, EXL3 4 bpw, SGLang XPU + MTP | Decode, 1 user: 43.6 → **53 tok/s** (median) Decode, 4 users: 84.7 → **103 tok/s** Prefill 32K: 1,037 → **1,660 tok/s** Prefill 256K: 297 → **628 tok/s** (2.1×) KV cache: 264K tokens → **4 × 256K** Startup: 113 → **43 s** Registry Lab gates: decode 28.6 → **41.0**, prefill 255 → **667** |
| **Intel Arc Pro B70** | Qwen3.8-27B, EXL3 4 bpw, vLLM + custom XPU kernels | Decode: **91.2 tok/s** at 1 user, **365** at 16 (prose, thinking on) Same card with llama.cpp Q4_K_M: 25.0 Prefill 4K/32K/128K/254K: 1,654/1,434/928/650 → **2,421/2,259/1,415/911** Agent-session replay: 193 → **147 s** |
| **Intel Arc Pro B70** | Same model, SGLang + the same kernels | Decode, 1 user: **82.6 tok/s**, vs vLLM 75.7 on the same card and day |
| **RTX 3090** | Qwen3.8-27B EXL3 3 bpw + MTP | **96.2 tok/s** prose / **141.1** code, 1 user |
| **RTX 3090** | Qwen3.6-35B-A3B EXL3 3 bpw + MTP | **251.7 / 357.9 tok/s**, 1 user |
| **RTX 3090** | Flash-Next EXL3, 256K context | MTP: 45.5 → **65.6 tok/s** |
| **4× H200 NVL** | DeepSeek-V4.1-Flash, vLLM + speculative decoding | Crashed under load → **229.1 tok/s** decode, **17,546 tok/s** prefill; all six gates pass |

Sources:

- [local-ai-registry](https://github.com/sybil-solutions/local-ai-registry):
  - [Ornith B390 recipe](https://github.com/sybil-solutions/local-ai-registry/tree/main/data/sources/ornith-b390-exl3), with the full hill-climb log in [PR #453](https://github.com/sybil-solutions/local-ai-registry/pull/453)
  - the RTX 3090 and H200 recipes
- [trellis-serve](https://github.com/sybil-solutions/trellis-serve):
  - `xpu/README.md`, `xpu/docs/PROGRESS.md` and `xpu/docs/SGLANG.md` for B70
  - `cuda/README.md` for the RTX 3090
- [qwen-serve](https://github.com/sybil-solutions/qwen-serve)

### Reading the B390 result

That run is the one this skill grew out of. Its ceiling calculation said:

- **Decode:** 100 tok/s for one user was only reachable with two useful speculative drafts. This model's draft head accepts ~14% at depth 2, so the practical target was ~88–97 tok/s. We reached ~55% of it; the rest is GEMV kernel efficiency.
- **Prefill at 256K:** we reached 628 tok/s against a ~670–684 tok/s ceiling.

The skill makes the agent compute this up front, so it can tell you early when a target is above the physics.


## 10. [arxiv] Procedure without Judgment: What Small Language Models Learn under an Exact Verifier
key: arxiv:2611.21529
url: https://arxiv.org/abs/2611.21529
meta: {"published": "2026-11-16", "authors": ["Arunkumar V", "Manoranjan Gandhudi", "Gangadharan G. R.", "Arun Prakash"], "categories": ["cs.AI", "cs.CL", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

When an authorization policy blocks an agent's tool call, the audit log should name the facts that forced the decision and nothing more. For an executable policy over an enumerable context space this minimal sufficient reason can be computed exactly, so an explanation is scored against ground truth rather than a proxy for it. We use that exactness to ask what a model can learn from a verifier that has no error in it. The explainer sees one request and one decision, never the policy, and has thirty turns in which it may call the policy on altered requests and ask whether a candidate set of facts is sufficient. Frontier models find the exact reason about half the time with the tools alone, and one sentence telling them to shrink the answer lifts Haiku 4.5 from 58% to 75%. A 4B model fine-tuned on 2000 traces of the deletion algorithm reaches 92% on the policy it was trained on. Teacher kind is what moves this: at matched data size the algorithm-taught student leads the frontier-taught one in all three training seeds, and the two arms never overlap. What the student learns is a fixed schedule of sufficiency checks, and the schedule does not travel. On three public policies it never saw, its answers stay sufficient (94%) and stop being minimal (48%), while Haiku under the same sentence is exact on all 47 episodes. Reinforcement learning from the exact reward leaves held-out accuracy where it was and inverts the strategy, from probing the policy to spending the entire budget on sufficiency checks. The oracle made the effect of training legible, but it did not make training better.

## 11. [youtube] I Tried the NEW Pump.fun Sniper Bot and This Happened?!
key: yt:vRSEt08OABc
url: https://www.youtube.com/watch?v=vRSEt08OABc
meta: {"channel": "Torrent", "rank": 2, "duration_min": 1}
query: pump.fun sniper bot how it works
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

# I Tried the NEW Pump.fun Sniper Bot and This Happened?!
# Torrent
# https://www.youtube.com/watch?v=vRSEt08OABc

[00:00] What if you didn't have to manually watch pump fun for the next token launch? And that's where Soul Sniper Bot comes in. It's a pump fun sniper bot built to snipe [music] new token launches for you. If you want to check it out yourself, I'll leave the link in the description. Once you're in, this is the main dashboard where you can set up and manage your sniper bots. To actually use the bots, you'll first need to connect your Solana wallet. Just click launch app [music] and connect your wallet. You can choose from
[00:33] multiple supported wallets and select the one you use. Once you're connected, this is where things get [music] interesting. Here I'm setting up the bot to automatically look for new tokens and execute trades based on the strategy and settings I've [music] selected. Once the bot is running, you can actually see the trades happening directly in the dashboard. >> [music] >> As more trades are executed, the individual results start adding up here, giving you an overview of how the strategy is performing. You set the strategy and the bot does the rest.

## 12. [awesome] actimod/onaa-protocol (new in awesome-mcp-servers)
key: gh:actimod/onaa-protocol
url: https://github.com/actimod/onaa-protocol
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-11-12", "language": "Python", "description": "Open directory of stores where AI agents reached checkout (payment not tested), plus payment, escrow and shipping providers. Links only; ONAA never pays."}
query: awesome-mcp-servers

# ONAA Protocol — Open Network for AI Agents

**Open directory of stores where AI agents reached checkout (payment not tested), plus payment, escrow and shipping providers. Links only; ONAA never pays.**

> **Building a shopping agent?** Start with [`examples/buyer-store-preflight`](https://github.com/actimod/onaa-protocol/tree/main/examples/buyer-store-preflight): it checks real stores with ONAA and stops before checkout (`python3 preflight.py --offline` runs with no network; payment is never tested). It is different from [`examples/direct-trade-demo`](examples/direct-trade-demo/), a mock agent-to-agent trade.

More broadly, **ONAA** is an open, hybrid peer-to-peer network for AI agents. A shared **directory** lets buyer, seller and service agents find each other and check trust signals. The actual conversation and trade happen **directly between the agents**, over open protocols ([A2A](https://a2a-protocol.org) and [MCP](https://modelcontextprotocol.io)). Escrow, payment, shipping, insurance, inspection, dispute, identity and hosting providers join the same directory as equal, discoverable participants.

**What ONAA is and is not.** ONAA is a discovery and trust-metadata directory. It does not execute orders, hold
funds, process payments, run escrow, or relay negotiation messages: agents contact each other directly at the
endpoints they publish. Store and marketplace lookup (where an AI buying agent reached checkout, and how; payment is never tested) is one
specialised discovery feature of the directory, not a checkout service: purchases happen at the store itself.

> **Status: early draft (ONAA Protocol v0.1.3).** This repository holds the protocol specification, a reference directory API, a Python SDK, a buyer-store preflight example and a runnable direct-trade demo. A **development** directory runs at https://api.onaa.net (agent instructions: https://api.onaa.net/llms.txt, remote MCP: https://api.onaa.net/mcp). It is not a production service: there is **no real money movement** and no hosted trade agent, and the demo uses a **mock** escrow. ONAA is a working project name; no trademark is claimed. Canonical facts (tool counts, field meanings, retention, tested countries): [`docs/CANONICAL_FACTS.md`](docs/CANONICAL_FACTS.md).

## What is in this repository

| Path | What it is |
|---|---|
| [`specs/`](specs/) | Draft specifications: the commerce extension for A2A (RFQ / QUOTE / escrow handoff), JSON Schemas for directory and certification records, the directory OpenAPI document, and the standards baseline (pinned A2A / MCP versions). |
| [`apps/api/`](apps/api/) | Reference **directory API** (FastAPI): registration, search, endpoint verification and separate trust levels. |
| [`apps/mcp-registry/`](apps/mcp-registry/) | **MCP server** source (Python, official `mcp` SDK): directory search, shopping guidance and trust lookups for MCP clients, over stdio or Streamable HTTP. Read-only by default. |
| [`packages/sdk-python/`](packages/sdk-python/) | **Python SDK** for directory discovery and registration. |
| [`examples/buyer-store-preflight/`](examples/buyer-store-preflight/) | **Shopping-agent preflight** against real stores: `find_stores` → `can_i_buy_here` → `how_to_buy` → the store's own catalog, then stops before checkout. Runs offline with `--offline`. Never pays. |
| [`examples/direct-trade-demo/`](examples/direct-trade-demo/) | End-to-end **demo**: buyer agent → directory search → direct A2A RFQ/QUOTE with a seller agent → direct

## 13. [vault] qualifying call script for trades leads
key: vault:2026-11-17:qualifying-call-script-for-trades-leads
url: https://www.youtube.com/watch?v=ZCMVm7WP4n4
meta: {"vault_status": "open", "kind": "service", "subject": "Nextdoor Pays Me $10,000 tutorial (SETH Coaching)", "date": "2026-11-17", "where": "TRITON-CORE/Research/links/2026-11-17-construction-broker-nextdoor.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: job, place, finish, timing, bad past experiences, builder availability

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Coaching promo, claims unverified; lead qualification and speed-to-call detail feeds the trades AI receptionist demo Write-up: `TRITON-CORE/Research/links/2026-11-17-construction-broker-nextdoor.md` Link: https://www.youtube.com/watch?v=ZCMVm7WP4n4

## 14. [hn] Show HN: Coral – Open-source gateway where agents write their own tools
key: hn:50517803
url: https://github.com/withcoral/coral
discussion: https://news.ycombinator.com/item?id=50517803
meta: {"points": 52, "comments": 24, "created": "2026-11-16T14:14:51Z"}
query: open data api

Hi HN, I'm James, one of the co-founders of Coral. Coral is an open-source, self-hosted gateway that sits between your agents and the systems they work on. Agents call tools by writing short TypeScript programs that they can save as custom tools to reuse. You can publish custom tools for groups of agents, so your team’s library of tools adapts to your unique systems, data and use cases. Custom tools help agent performance and give more precise units of permission control. Here’s a short demo: https://www.youtube.com/watch?v=p0PKOlHLyVI We started on this while building an AI SRE. To investigate an incident, the agent had to connect the dots across an ocean of telemetry data and undocumented relationships across internal and external systems. It took broad permissions, a lot of tokens and it would start from scratch the next time. We built Coral so that the agent remembers the route. Once a task succeeds, the agent writes the steps that worked into a program and saves it as a custom tool. Next time, the agent finds that custom tool in the same search as standard provider tools (e.g. Datadog, Slack), and reuses it. It started with SRE, but we (and our early users) now use Coral for agent work across the org. For our tasks across GitHub, Linear and Slack with Opus 5.5, custom tools help agents work 29% faster, at 31% lower cost (tasks here: https://withcoral.com/docs/examples/custom-tools ). Coral builds on code mode, adding custom tools, policy controls and managed identities. 
comment (disrpt): Much love.
comment (greenBottle): Looks good. We're evaluating it.
comment (jurgenaut23): Will give it a go!
