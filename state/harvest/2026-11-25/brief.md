# Harvest brief, 2026-11-25

14 items shortlisted from 393 candidates (340 dropped as already seen, 5 carry a vault verdict on the vendor).

## 1. [vault] seven-prompt path from empty chat to a shippable game
key: vault:2026-11-24:seven-prompt-path-from-empty-chat-to-a-shippable-game
url: https://www.instagram.com/p/DgGDejhjjDA/
meta: {"vault_status": "open", "kind": "service", "subject": "@godofprompt AI dragon game seven prompts carousel", "date": "2026-11-24", "where": "TRITON-CORE/Research/links/2026-11-24-godofprompt-ai-dragon-game.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: on the slides, unseen; compare with the 5 Nov Sumiro 24h game link before any game lane

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Unverified solo-dev-with-Claude game story and prompt-guide funnel; slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-24-godofprompt-ai-dragon-game.md` Link: https://www.instagram.com/p/DgGDejhjjDA/

## 2. [hn] Launch HN: Versine (YC F26) – MCP to send and receive money
key: hn:50634426
url: https://news.ycombinator.com/item?id=50634426
discussion: https://news.ycombinator.com/item?id=50634426
meta: {"points": 84, "comments": 65, "created": "2026-11-24T20:44:15Z"}
query: claude code

Hey HN, we’re Harshith, Param, and Vishnu and we're building Versine ( https://versine.com ). Versine lets you send and request money just by talking or texting with your AI (think Venmo with an MCP). We’re software engineers who have worked on distributed systems at Stripe, Databricks, and Amazon. Versine is an MCP that sits in front of a wallet with a balance. With it, your agent can do things like: - Send money to someone with your approval (via passkey in our app) - Send and request money to/from up to 100 people at once - Send money to people without a Versine account (they cash out to their bank in 2 mins) - Pay people without your explicit approval to trusted contacts (you can set this) Here’s a demo: https://youtube.com/shorts/Q9X7zioEqi0 We started working on this because assistants are frustratingly hands-off when it comes to finance and money movement. You can have your assistant go through a receipt and map out all the amounts owed taking care of splitting the subtotal, taxes, tips, but at the end of it the assistant hands back work to you when you have to go out and make the Venmo transfer. Our current solution is oriented towards power users: those who want to automate everything through their agent use us to split dinners, group trips, or settle poker ledgers. We see ourselves unlocking more value for the general consumer as 1. More people turn into power users of agents, and 2. We expand to a more complete banking solution: deposits, transfers, wires, everythi
comment (moecables): great job on building something that actually moves money using AI. to me this sounds like something CashApp and Venmo will copy pretty quickly.
comment (GreggHyram): Cool idea! How do you make money?
comment (Oras): Congrats on launch and well done on the landing page. When I read this post, first thing came to my mind was meh, every payment provider will replicate this, and how’s it different from wallets but seen your landing page of requesting payment from multiple people, I think you’re onto something big. Also it tells me you actually talked to people facing this issue. My daughter is in some clubs and most of them are on WhatsApp, I can see how this would be super useful for that kind of small businesses where it will chase for them in bulk. I wish you all the success and will keep checking your pro

## 3. [github] Developing-Gamer/agent-sim: iOS simulators for AI agents, on Linux. The agent layer for x86Sim.
key: gh:developing-gamer/agent-sim
url: https://github.com/Developing-Gamer/agent-sim
meta: {"stars": 575, "created": "2026-11-21", "pushed": "2026-11-25", "language": "Rust", "topics": ["ai-agents", "claude-code", "ios", "ios-simulator", "linux", "mcp", "mobile-testing", "testing"]}
query: claude-code created:>{since} stars:>20

# agent-sim

**iOS simulators for AI agents, on ordinary Linux machines.** No Mac, no GPU.

   

 Safari on Apple's iOS runtime, on a Linux VM, recorded at 60 fps (the GIF is 15).
 Full clip  ·
 An agent driving
Settings and Safari  

> **agent-sim is built on [x86Sim](https://github.com/x86sim/x86sim) by [designgears](https://github.com/designgears).**
> x86Sim is what runs Apple's iOS simulator on Linux, and it has done that since its first release. agent-sim is the
> agent layer on top of it. If agent-sim is useful to you, [star x86Sim](https://github.com/x86sim/x86sim) too.

agent-sim takes the iOS simulator that x86Sim runs on an x86-64 Linux VM and gives agents what they need to test iOS
apps: install an `.ipa`, read the screen as text, tap, type, scroll, and watch it live in a browser. One command line
for scripts and CI, and an MCP server for Claude Code, Cursor, Codex and other agents.

```
$ agent-sim launch com.apple.Preferences && agent-sim snapshot
app com.apple.Preferences
@e1 button "Apple Account, Sign in to access your iCloud data, the App Store, Apple services, and more." (201,213)
@e2 button "General" id="com.apple.settings.general" (201,320)
@e3 button "Accessibility" id="com.apple.settings.accessibility" (201,372)
...
$ agent-sim tap @e2
tapped @e2 button "General"
```

> **Status: early.** It works end to end; expect rough edges, and see [what does not work yet](docs/KNOWN_ISSUES.md).

## Quick start

On an x86-64 Linux machine with Ubuntu 24.04 (8+ CPUs, 16 GB of memory, 60 GB of free disk):

```sh
curl -fsSL https://raw.githubusercontent.com/Developing-Gamer/agent-sim/main/install.sh | bash
agent-sim setup      # once, about half an hour: x86Sim, Apple's iOS runtime (8 GB, from Apple), a first phone
agent-sim up         # boot it: 12-30 s, depending on the CPU
agent-sim snapshot
```

From a checkout instead: `cargo build --release`, then `scripts/setup-vm.sh` and `target/release/agent-sim`.

`agent-sim setup --fidelity high --device hifi` adds a phone that looks exactly like Apple's simulator (3x, every
blur and animation) for screenshots; the default draws at 2x with reduced effects and scrolls twice as fast.

## Use it from an agent

As an MCP server:

```sh
claude mcp add agent-sim -- agent-sim mcp          # Claude Code
```

```json
{ "mcpServers": { "agent-sim": { "command": "agent-sim", "args": ["mcp"] } } }
```

An agent on another machine (your laptop) runs the same server over SSH; MCP's stdio passes through unchanged:

```sh
claude mcp add agent-sim -- ssh my-linux-vm agent-sim mcp
```

The tools are `snapshot`, `tap`, `type`, `scroll`, `swipe`, `press`, `launch`, `terminate`, `install`,
`uninstall`, `apps`, `open_url`, `wait_for`, `screenshot` and `boot`. Actions answer with the screen that follows,
so an agent sees the result of each step without asking again. For agents that work in a shell,
[skills/agent-sim/SKILL.md](skills/agent-sim/SKILL.md) teaches the command line.

## The command line

```sh
agent-sim install MyApp.ipa        # a device build is converted for the simulator; a simulator .app works too
agent-sim launch com.example.myapp
agent-sim snapshot                 # the screen as text, one element per line (--json for frames, ids, states)
agent-sim tap @e4                  # an element from the last snapshot; or: tap "Sign in"; or: tap 201 320
agent-sim type "hello@example.com"
agent-sim scroll down
agent-sim wait "Welcome" --timeout 20
agent-sim screenshot -o screen.png
agent-sim press h

## 4. [youtube] The 10-Year-Old Cars That Fail Their MOT Least (and the 5 That Fail Most)
key: yt:uxUVGL8t2us
url: https://www.youtube.com/watch?v=uxUVGL8t2us
meta: {"channel": "First Time Pass", "rank": 1, "duration_min": 11}
query: MOT data analysis uk

# The 10-Year-Old Cars That Fail Their MOT Least (and the 5 That Fail Most)
# First Time Pass
# https://www.youtube.com/watch?v=uxUVGL8t2us

[00:00] At 10 years old, one car fails its about one time in seven, and another fails more than four times in 10, which is three times as often at exactly the same age. We've used the DVSA's record of every MOT test in Great Britain last year to find out which cars they are, and you'll see the 10 that held up best, the five that struggled most, and a check you can run on any used car from your armchair. [music] Number one is probably not the car you're thinking of. So, if you're picturing something small and sensible from Japan, keep that guess in mind because we'll test it against
[00:33] the data. Our numbers come from the research site Car Control, [music] which went through every one of those tests, and we're using its figures for cars first used in 2015 [music] at the first attempt for every model with at least 2 and a half thousand tests with vans left out. A second analysis by Autosa agrees with it to within half a point. The bar to beat across all cars aged 10. About three in 10 failed first time and every car in our top 10 failed less than one time in five. From 10 down to six then. [music]
[01:07] And for each one, what does it do better than cars its age? At number 10, the Mini 1 failed 18% of the time across more than 5 and a half thousand tests. Its answer to the question is consistency because the rest of the family sits right beside it with the Kooper on 18.3. the Countryman on 18.2 and even the Kooper S under 20. The Volkswagen Golf at number nine answers the question with sheer numbers. [music] Nearly 38,000 10-year-old Golfs were tested, far more than any other car in the top 10, and 17.9% of them failed
[01:41] first time. With that many cars behind it, the figure is about as solid as these numbers get, and the second analysis put it at 18.1. Number eight is the Audi Q5 at 17.7% and its answer comes with the miles. 10-year-old Audi's had covered about 90,000 mi on average, some 10,000 more than the [music] typical car that age. And the Q5 still failed far less often than the average. With the Q5, it's the miles that stand out. Whereas for the Range Rover at number seven, it's the whole family. The full-size Range Rover
[02:15] failed 17.4%, 4%, the Evoke 19.3, and the Range Rover Sport 19.8. So, all three Range Rovers of that age beat the average by at least nine points. That leaves number six, the Audi A6, at 17.2% across nearly 6,000 tests, which is lower than every popular small hatchback of the same age, bar one, and you'll meet that one in the top five. Hold on to those five because the other end of the table looks very different. And we'll come back for the top five once you've seen it. Now, the five with the
[02:47] weakest records. And for each one, you'll hear two numbers. The first is how often it failed at the first attempt. A car that failed and was put right at [music] the test center within the hour still counts because that's how the DVSA works out its own figures. The second is how many were still a fail once [music] that hour was up. the ones whose problem couldn't be fixed on the spot, which usually means a repair bill and a second trip back [music] for a retest. Number five is the Citroen C4, which failed 38.8% of the time, about a third more often than the average car
[03:19] its age, and almost 32% still had a fail after the hour. It's also the most tested ca
[transcript continues in field-notes/staging/uxUVGL8t2us.txt]

## 5. [awesome] luca-network/spr (new in awesome-mcp-servers)
key: gh:luca-network/spr
url: https://github.com/luca-network/spr
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-10-28", "language": "JavaScript", "description": "SPR, the Sealed Payment Record: an open format, library and SDKs for sealed accounting records of AI agent payments. Apache-2.0"}
query: awesome-mcp-servers

# SPR: the Sealed Payment Record
[](https://glama.ai/mcp/servers/luca-network/spr)

Your AI agent pays for data, compute and services, and your finance team and auditor can't see what each payment was for. SPR records every payment your agent makes, before and after it pays, sealed with your company's own key on your own machine. Anyone can check the seals. No service has to be trusted, Luca's included.

```
npx -y @luca-network/spr-mcp
```

Free and open: Apache-2.0, with a royalty-free patent commitment ([`PATENTS.md`](PATENTS.md)).

## Use it from your AI tool

Every setup below runs the same MCP server on your machine. Set `SPR_AGENT_ID` (your agent) and `SPR_ENTITY` (the company it pays for); records go to `SPR_DIR`.

**Claude Desktop**: add to `claude_desktop_config.json`:

```json
{ "mcpServers": { "spr": { "command": "npx", "args": ["-y", "@luca-network/spr-mcp"],
  "env": { "SPR_AGENT_ID": "agt_research", "SPR_ENTITY": "Example Co", "SPR_DIR": "/Users/you/spr-books" } } } }
```

**Cursor**: the same block in `.cursor/mcp.json`.

**Claude Code**:

```
claude mcp add spr -e SPR_AGENT_ID=agt_research -e SPR_ENTITY="Example Co" -- npx -y @luca-network/spr-mcp
```

**OpenAI Agents SDK** and **LangChain** (JavaScript):

```js
import { SprBook, toOpenAIAgentsTools, toLangChainTools } from "@luca-network/spr-sdk";
const book = new SprBook({ dir: "./books", agentId: "agt_research", entity: "Example Co" });
const tools = toOpenAIAgentsTools(book, tool);   // tool from "@openai/agents"; or toLangChainTools(book, tool)
```

**CrewAI, Microsoft Agent Framework, Google ADK and the Claude Agent SDK** (Python): each connects to the MCP server in a few lines. See [`examples/`](examples).

**Any other MCP client**: run `npx -y @luca-network/spr-mcp` over stdio with the two settings above.

The agent then calls `record_intent` before it pays, `check_payment` to see whether the payment is inside what it declared, goes to the payee it named and wasn't paid already, and `record_settlement` after it pays. Each record is sealed in the book's folder.

A merchant's book works the same way for payments received: it can keep the buyer's own sealed intent, how the buyer authenticated, and the order and processor references, and export one payment's evidence for a chargeback response (`export_dispute_pack`).

A record shows:
- what the agent declared before it paid: the purpose, the most it could spend, and when the permission expired;
- what was actually paid, on which rail, to whom and when;
- whether the payment stayed inside what was declared;
- for x402 payments, whether the chain itself recorded which declaration the payment was made under. The payer signs a fingerprint of the sealed intent as the payment's nonce.

This repository holds:

| Path | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The format, draft 1 |
| [`packages/spr`](packages/spr) | `@luca-network/spr`, the reference library for JavaScript and TypeScript, with no dependencies, plus the test vectors and `spr-verify` |
| [`packages/spr-sdk`](packages/spr-sdk) | `@luca-network/spr-sdk`: seal your agents' payments locally, with `withLuca(fetch)` for x402 and tools for the OpenAI Agents SDK and LangChain |
| [`packages/spr-mcp`](packages/spr-mcp) | `@luca-network/spr-mcp`: the same calls as an MCP server, for Claude Desktop, Cursor or your own agent (`npx @luca-network/spr-mcp`) |
| [`python`](python) | `spr-sdk` for Python: the same format and the same books |

## Seal an x402 payment in

## 6. [vault] comment-FABLE-for-the-guide funnel
key: vault:2026-11-24:comment-fable-for-the-guide-funnel
url: https://www.instagram.com/p/DgGDejhjjDA/
meta: {"vault_status": "intel", "kind": "service", "subject": "@godofprompt AI dragon game seven prompts carousel", "date": "2026-11-24", "where": "TRITON-CORE/Research/links/2026-11-24-godofprompt-ai-dragon-game.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: understand only, never operate

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Unverified solo-dev-with-Claude game story and prompt-guide funnel; slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-24-godofprompt-ai-dragon-game.md` Link: https://www.instagram.com/p/DgGDejhjjDA/

## 7. [hn] Show HN: Mason – A lightweight Postgres read-replica, built on columnar storage
key: hn:50630294
url: https://masondata.ai/
discussion: https://news.ycombinator.com/item?id=50630294
meta: {"points": 93, "comments": 17, "created": "2026-11-24T16:11:52Z"}
query: open data api

Hi HN! TLDR: we’ve built an open-source drop-in replacement for a postgres read-replica, powered by duckdb’s columnar compute engine. It’s very fast. And it looks like postgres. So, this started out as: let’s just connect Clickhouse to our postgres dbs and throw our analytics queries at it instead. That will speed everything up. But we quickly found that 1) Clickhouse comes with quite the learning curve (engine optimisation) to make it fast (we needed something we could easily drop in to any customer’s postgres scenario), and 2) we had underestimated how different clickhouse’s SQL syntax was to postgres. Don’t get me wrong: we love Clickhouse (it’s ridiculously fast if you know what queries to expect), it just didn’t work for our ad-hoc postgres workloads. So we went searching for alternatives that were 1) more plug-and-play and 2) looked a lot more like postgres. We dismissed a bunch based on desk research alone: - pg_mooncake (seems to have stalled since data bricks bought them) - pg_duckdb (seems to offer fast queries, or fresh data, but not both - we needed both) - materialize/risingwave/readyset (like Clickhouse, they require knowing the query shapes upfront - not ideal for ad-hoc workloads) - firebolt (license makes it challenging to offer to our customers) - redshift / alloydb / etc (we wanted something cloud-provider agnostic) And we shortlisted 3: - pg_clickhouse (Postgres extension that parses SQL in Postgres and pushes the work down to ClickHouse) - cedarDB (closed
comment (hum3hum3): I did something sort of similar which is to rewrite postgres so that I could use it against a single file sqlite DB and run in a browser with WASM. https://github.com/drummonds/go-postgres
comment (richardmeng): Very cool.
comment (nylonstrung): Outside of the dashboard and team features stuff what does this add over just DuckDB + ADBC connected to postgres? Is pglite and the node stuff even necessary here?

## 8. [github] pritamux/gridlines: An agent skill for alignment passes: draw guide lines down an interface, find every item that misses its line, fix the padding.
key: gh:pritamux/gridlines
url: https://github.com/pritamux/gridlines
meta: {"stars": 234, "created": "2026-11-21", "pushed": "2026-11-22", "language": "JavaScript", "topics": ["agent-skills", "claude-code", "design-engineering", "ui"]}
query: claude-code created:>{since} stars:>20

# gridlines

An agent skill for alignment passes. It draws vertical guide lines down an interface, finds every item that misses its line, and fixes the padding so sidebars, toolbars, panels, menus and tables share a small set of edges.

Draw the lines first, then move the items.

[](media/before-after.mp4)

## Install

```sh
npx skills add pritamux/gridlines
```

Or copy `skills/gridlines/` into your agent's skills folder (for Claude Code, `~/.claude/skills/gridlines/`).

Then ask your agent for an alignment pass, or call it directly:

```
/gridlines line up the settings sidebar
```

## What's inside

| File | What it does |
| --- | --- |
| `skills/gridlines/SKILL.md` | The process and the rules the agent follows |
| `skills/gridlines/probe.js` | Runs in the page: measures the ink edges of text, icons and controls, draws the guides, lists every miss |
| `skills/gridlines/audit.mjs` | Loads a page in headless Chromium, runs the probe, saves a 2x capture with the guides and a JSON report |
| `examples/sidebar.html` | A sidebar with four planted misses, to see a report before pointing it at your app |

## Try the probe

The audit script needs Playwright. Install it anywhere and point `PW_DIR` at that folder:

```sh
npm i --prefix /tmp/gridlines-pw playwright
npx --prefix /tmp/gridlines-pw playwright install chromium
PW_DIR=/tmp/gridlines-pw node skills/gridlines/audit.mjs "file://$PWD/examples/sidebar.html" .gridlines 800
```

```
## Sidebar  x0 w240
   lead 12px  box -  icon centre 20px  label 36px  trailing 12px  trailing centre -
   MISS y56 trailing: 15px vs 12px  [12]
   MISS y88 leading: 15px vs 12px  Workspace
   MISS y120 label: 38px vs 36px  Views
   MISS y120 vertical-centre: 3px vs 0px    … Views
```

The probe also works without the script: paste `probe.js` into any page's console and call `window.__gridlines()`.

## Credits

The rules come from Karri Saarinen's redraw of the Linear sidebar and his notes on rhythm, edges and centring, backed by the layout chapter of Apple's Human Interface Guidelines.

## License

MIT

## 9. [youtube] Failed your MOT? Can you drive it, the free retest, and what the repair costs
key: yt:HewpPDuJ4KI
url: https://www.youtube.com/watch?v=HewpPDuJ4KI
meta: {"channel": "MOTFaults", "rank": 2, "duration_min": 2}
query: MOT data analysis uk

# Failed your MOT? Can you drive it, the free retest, and what the repair costs
# MOTFaults
# https://www.youtube.com/watch?v=HewpPDuJ4KI

[00:00] About one car in twelve fails its MOT. If yours does, three questions come next. Can I drive it? Do I pay for the retest? And what will the repair cost? Can you drive it away? Two things decided. If your old MOT certificate is still in [music] date and the result lists no dangerous defect, you can drive the car to a garage for the repair. If the old certificate has run out, you may only drive to a repair or to a test you have booked. Otherwise, the fine is up to £1,000 [music] and your insurance may
[00:33] not cover you. And a dangerous defect means the car does not move until it is fixed. The retest can be free. [music] Leave the car at the test centre for the repair and the retest is free within ten working days. Take it away and bring it back by the end of the next working day and the retest is also free if it failed only on simple items. [music] Lights, tyres, wheels, wipers and washers, mirrors, number plates, the horn, seats and seat belts. [music] Not brakes and not suspension. Bring it back later within ten working days and
[01:06] you pay a partial retest fee. [music] After that, it is a full test again at up to £54.85. What will it cost? Typical prices at an independent garage with parts and labour. A bulb, nine to £45. A pair of wiper blades, ten to £50. A tyre, 55 to £130. Brake pads for one axle, 55 to £120. Discs [music] and pads, 130 to £255. A pair of shock absorbers, 120 to £305.
[01:41] Some of the cheap ones you can fit yourself. A bulb is two to £10 as a part. A pair of wiper blades, ten to £30. To pay less, ask for a written quote before any work starts [music] and compare a second garage. You do not have to repair at the test centre [music] and read the advisories your result. They are what fails next year. The full guide is on our site, [music] what each result means, the retest rules, and repair costs for every failure. Free at motfaults.co.uk. The link is in the description.

## 10. [awesome] neoma-pcam/pcam-live (new in awesome-mcp-servers)
key: gh:neoma-pcam/pcam-live
url: https://github.com/neoma-pcam/pcam-live
meta: {"list": "awesome-mcp-servers", "stars": 1, "created": "2026-10-06", "language": "Python", "description": "NEOMA P-CAM: Deterministic Sub-0.03ms Physical Reflex Core (Rust Axum). 64-Spin Ising Physical Solver (Measured Latency: 0.011ms), Phi-3 Embodied Cognitive Synthesis, and Zero-Trust 1:1.1 PoPW Ledger with Silicon Root-of-Trust (SEAL-CORE)."}
query: awesome-mcp-servers

# NEOMA P-CAM v7.0.0 — 5-Node Parallel Analog HIL Cluster Gateway

[](https://glama.ai/mcp/servers/@neoma-pcam/pcam-live)
[](https://mcpservers.org/servers/neoma-pcam/pcam-live)
[](https://glama.ai/mcp/servers/neoma-pcam/pcam-live)
[](https://mcprush.com/to/neoma-p-cam-physical-ai-ising-mcp?ref=badge)
[-10b981?style=for-the-badge)](https://neoma-pcam.github.io/pcam-live/)
[-06b6d4?style=for-the-badge)](https://neoma-pcam.github.io/pcam-live/bio.html)
[-3b82f6?style=for-the-badge)](https://api.neoma-pcam.com/docs)
[-8b5cf6?style=for-the-badge)](https://bio.neoma-pcam.com/bio/docs)
[](https://doi.org/10.5281/zenodo.23644655)
[](LICENSE)

> **v7.0.0 Architectural Milestone — 100% Real Hardware-in-the-Loop (5-Node Parallel Analog HIL):**
> NEOMA P-CAM executes **zero CPU physics substitution, zero PRNG/CPU annealing fallbacks, and zero artificial latency clamping**. Every API request drives real physical excitation on the **parallel analog HIL substrates** and a 16-bit analog measurement, reports the genuine on-chip cycle-counter settling time (`measured_us`) separately from link round-trip latency (`uart_rtt_ms`), and enforces strict **Fail-Closed HTTP 503 (`HARDWARE_MEASUREMENT_UNAVAILABLE`)** whenever hardware measurement is unavailable.

> **Embodied Brain ↔ Spine:**
> **Brain** — embodied language model on the client side that interprets the live physical state and puts it into words.
> **Spine** — 5-node P-CAM analog silicon cluster (`cluster_alive_mask 0x1f`) that performs the sub-millisecond physical equilibrium measurement (`measured_us`).
> Every `/v1/*` POST response carries a one-line `cognitive_synthesis` log of this Spine → Brain hand-off. The gateway itself runs no language model; it supplies the measured state.

## Quick Index

| Resource | Address |
| :--- | :--- |
| **Physical API (Track A, 17 domains + 5 alias routes)** | `https://api.neoma-pcam.com` |
| **Bio API (Track B, 23 domains)** | `https://bio.neoma-pcam.com` |
| **Swagger UI** | [api.neoma-pcam.com/docs](https://api.neoma-pcam.com/docs) · [bio.neoma-pcam.com/bio/docs](https://bio.neoma-pcam.com/bio/docs) |
| **OpenAPI specs** | [`openapi.json`](openapi.json) (served at `/openapi.json`) · [`openapi-bio.json`](openapi-bio.json) (served at `/bio/openapi.json`) |
| **Live hardware telemetry (public, no key)** | `GET https://api.neoma-pcam.com/v1/telemetry` |
| **Domain index** | [§3 API Domains](#3-api-domains-40-live-hil-endpoints) · [NASA B0005 benchmark](#nasa-b0005-live-benchmark-168-discharge-cycles) |
| **Language models (LLM)** | [LLM grounding and MCP](#language-model-llm-grounding) · MCP endpoint `POST https://api.neoma-pcam.com/mcp` |

### Language-Model (LLM) Grounding

P-CAM is not a language model. It gives LLMs and AI agents a source of **physically measured facts**.

- **Grounding via MCP / API:** agents call `POST /mcp` (MCP Streamable HTTP, tools `solve_nonlinear_equilibrium` and `solve_ising_optimization`) or the REST domain routes. Every answer is a live hardware measurement (`v_out_measured_v`, `measured_us`, `entropy_ent`, `ok_mask`, `routed_node`) bound to a hardware seal, so a model can cite measured values instead of generating them.
- **Hallucination control:** physical statements are taken from these measured, sealed fields. When the hardware cannot measure, the gateway returns `HTTP 503` instead of a fabricated value, so an agent never receives invented physics. This constrains hallucination about the physical state; it does not verify the

## 11. [vault] setup 3k+ plus 500 to 1k monthly pricing benchmark
key: vault:2026-11-21:setup-3k-plus-500-to-1k-monthly-pricing-benchmark
url: https://www.instagram.com/p/Df5Ec0nnew_/
meta: {"vault_status": "intel", "kind": "service", "subject": "@basharjkatou AI automation agency carousel", "date": "2026-11-21", "where": "TRITON-CORE/Research/links/2026-11-21-basharjkatou-ai-automation-agency.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: US dollars, claims only

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Standard AI automation agency pitch; market and price signal only, slides unseen Write-up: `TRITON-CORE/Research/links/2026-11-21-basharjkatou-ai-automation-agency.md` Link: https://www.instagram.com/p/Df5Ec0nnew_/

## 12. [hn] Anthropic and OpenAI employees fear unreleased AI models too unsafe to release
key: hn:50631691
url: https://tech.yahoo.com/ai/claude/articles/scoop-anthropic-openai-employees-fear-104505580.html
discussion: https://news.ycombinator.com/item?id=50631691
meta: {"points": 22, "comments": 27, "created": "2026-11-24T17:46:41Z"}
query: claude code

page: Scoop: Anthropic and OpenAI employees fear unreleased AI models are too unsafe to release Skip to main content Advertisement Advertisement Advertisement Illustration: Brendan Lynch/Axios. Stock: Getty Images Anthropic and OpenAI are facing an increasingly urgent problem: Internal, unreleased models are becoming so powerful that many employees no longer believe they can be safely released, according to more than two dozen sources familiar with the internal debates. Why it matters: The challenge could significantly slow the AI boom, as the gap between what the best AI systems can do and humans' ability to control them continues to widen , sources told Axios. Researchers haven't found technical solutions for controlling the most advanced models. Some insiders believe it's fixable. Others aren't convinced and say companies should stop training new models entirely. Advertisement Advertisement Driving the news: Top AI leaders have long forecast that the technology would one day far surpass human intellect in virtually every field. Although internal models have yet to cross that threshold, recent breakthroughs at OpenAI and Anthropic have shocked researchers. The rapid advances in reasoning across domains including math, science, cybersecurity and AI research have also made the models difficult, if not impossible, to contain or control in internal tests, the sources said. Anthropic and OpenAI have unreleased models that are far more powerful than what they've already released publicly, but the AI companies have struggled to ensure that they are safe enough for public release, sources said. This has led to debate within Anthropic, OpenAI and the AI research community about whether to stop releasing future frontier models publicly, instead reserving them for internal deployment only. There has also been debate around whether to train new models at all, sources inside and outside those companies told Axios. What they're saying: "If we continue trying to make models much smart
comment (proc0): How many times are they going to say this.
comment (watwut): Yeah yeah, we already heard that. Many times.
comment (cendyne): All right, then. Keep your secrets.

## 13. [github] EL4CTEO/shrink-anything: Less code, same tests passing: delete the dead code, files, dependencies and assets in any codebase, and keep each cut only if your own tests still pass.
key: gh:el4cteo/shrink-anything
url: https://github.com/EL4CTEO/shrink-anything
meta: {"stars": 215, "created": "2026-11-23", "pushed": "2026-11-23", "language": "Rust", "topics": ["ai-agents", "bundle-size", "claude-code", "cli", "code-cleanup", "dead-code", "mcp", "refactoring"]}
query: claude-code created:>{since} stars:>20

Less code. Same tests passing.  

 
     
     
     
   
   
   
     
 

Coding agents write code faster than anyone deletes it. Functions nothing calls, files nothing imports, packages nothing uses, images nothing shows: your agent reads all of it, your CI builds it, your users download it.

**shrink-anything** finds it, deletes it, and runs *your own tests* after every cut. What passes stays. What breaks is put back. One command, fully reversible.

Every line it removes is a line your agent stops reading on the next task. The report counts that too: on the demo app, 46% fewer tokens to read.

   

## Install

```sh
npm i -g @el4cteo/shrink-anything      # or: cargo install shrink-anything
```

## Use

```sh
shrink-anything go --agent claude -- npm test     # or: -- pytest / cargo test / go test ./... / anything that fails when your app is broken
```

Or step by step:

| command | what it does |
|---|---|
| `scan` | lists what could go. Changes nothing |
| `cut --  ` | deletes what's dead and runs your check: what passes stays, what breaks is put back |
| `task --agent claude` | hands the judgment calls (duplicates, public methods) to your agent, and keeps its work only if the check agrees |
| `weigh dist` | where the weight of a build is: by kind of file, the heaviest files, what's in there twice |
| `verify` | runs your check now, against the test count from before the first cut |
| `undo` | takes the last cut back, byte for byte (`--all` for every cut) |
| `report` | markdown + SVG card for your PR |
| `doctor` | what's installed: parsers, package managers, agents |

`--agent` takes `claude`, `codex`, or any command that reads a prompt on stdin. Without it, hand `.shrink/TASK.md` to whatever you use.

## Proof, not vibes

   

Nothing in that code mentions `secretly_used`: a test reaches it through a name it reads from a data file. The cut broke that test, so it was put back, alone.

- **Your check decides.** A cut stays only if your command exits 0 *and* at least as many tests run as before. A check that already fails is refused: it can't prove anything.
- **One bad cut doesn't sink the rest.** Cuts go in as a batch. If the check fails, the batch is split until the one cut that breaks it is found and put back. Every state left on disk has passed.
- **Parsed before it's tested.** Each edited file goes through the language's own parser (Python, Node, Ruby, PHP, Lua, Bash) before your check runs.
- **Tests are never touched**, and `shrink-anything undo` restores every file byte for byte.
- **What can't be proven isn't cut.** A public method, an export of a library, a subclass a framework may register, a file in a folder loaded by convention: these go to your agent with the reason, or behind `--aggressive`.

The proof is as strong as your check. A project with no tests gets a scan, not a cut you should trust.

   

## What it finds

| | how it decides | where |
|---|---|---|
| **dead code** | every mention of the name is inside its own definition. Any other mention anywhere (another file, a string, a template, a config) keeps it | 19 languages |
| **dead files** | no other file names it | Python, JS/TS, PHP, Ruby, Dart, Lua/Luau |
| **unused dependencies** | nothing imports it or runs its commands | npm · pnpm · yarn · bun · Cargo · pip · Go modules |
| **dead weight** | an image, font or sound no code, config or README names; the same file stored twice | any project |
| **duplicates** | the same code twice, whatever it's called and 

## 14. [youtube] Coding Adventure: Making a Better Chess Bot
key: yt:_vqlIPDR2TU
url: https://www.youtube.com/watch?v=_vqlIPDR2TU
meta: {"channel": "Sebastian Lague", "rank": 3, "duration_min": 60}
query: lichess bot python engine

# Coding Adventure: Making a Better Chess Bot
# Sebastian Lague
# https://www.youtube.com/watch?v=_vqlIPDR2TU

[00:00] hello everyone welcome to another episode of coding Adventures today we're back to chess so what I'd like to do is take this little chess playing program that we made about two or three years ago now and figure out how good it actually is my plan for doing that is to Simply Let it Loose on a popular chess website called leeches as a registered bot account of cons and see what sort of rating it ends up with before we do that though I can't resist trying to make it just a little bit
[00:33] stronger so that it's hopefully able to put up a good fight now to test whether the changes we make are actually helpful or not I've started by making a little program called the match manager and the idea is that we'll be able to connect up two different versions of our chess program so we can have the new version battle the old version to make sure we haven't accidentally made it worse they need to play a wide variety of positions for it to be a good test though so I'd like to start each game from a random position to get some random test positions I've
[01:06] gone over to the leeches database to First download a bunch of games wait a minute this is 35 gigabytes for one month of games that's that's too much chess let's go back in time to something a bit more manageable okay 500 megabytes I can work with [Music] so we now have this file of two and a half million games in the portable game notation format and I like that it also includes the name of the opening because if we choose games that started with different openings that should ensure some more variety in our test set
[01:40] okay I've just finished struggling to write some simple python code for a change because I wanted to use this nice library to extract random positions from the games where there are still lots of pieces left to avoid any totally boring positions running this took a couple of minutes to finish but if we just fast forward time we now have a list of physicians in the fan notation that we talked about last video which I only want Physicians that are roughly equal for our test set so with some help from the internet I've managed to get some code working that
[02:12] automatically feeds each position into stockfish one of the strongest chess programs in existence to filter out all the ones that are unfair to either side with that done I'm going to try running a full match between two copies of version one just to make sure that everything goes smoothly they're playing 500 different positions both as black and white so a thousand games in total with a generous thinking time of 100 milliseconds per month this will probably take a few hours to run so feel free to have a nap and I'll
[02:46] wake you up when it's done you won't fish up till then that it was a pretty even match between version 1 and version 1 with the one version one winning 347 games and losing 355. so with our test setup working let's try to actually improve the program I'd say there are two main areas we can focus on search and evaluation and let's start with search because while that test was running I've been looking back at some of this old code and I noticed something nice and easy that we can begin with
[03:18] so we're doing something here called iterative deepening which is a fancy name for just first searching one move ahead then if the search hasn't been canceled yet we increase that to 
[transcript continues in field-notes/staging/_vqlIPDR2TU.txt]
