# Harvest brief, 2026-10-09

14 items shortlisted from 243 candidates (97 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] A scoped UK test of one flip with the compliance costs priced first, only if Luke wants the lane
key: vault:2026-10-09:a-scoped-uk-test-of-one-flip-with-the-compliance-costs-price
url: https://www.skool.com/ai-car-trader-9959
meta: {"vault_status": "open", "kind": "service", "subject": "AI Car Trader (Skool, Ethan, 29 dollars a month, car flipping with AI prompts)", "date": "2026-10-09", "where": "TRITON-CORE/Research/links/2026-10-09-ai-car-trader-skool.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Nothing starts without his word

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A ten-week-old Skool community, 65 members, 29 dollars a month, selling a car-flipping playbook with AI prompts and a no-money-down angle, headlined by an unverifiable 100 million dollars in trades and a 30-day money-back line. The model is American; in the UK two cars bought to resell make you a trader, every sale carries Consumer Rights Act liability with a 30-day right to reject and a six-month fault presumption, and driving stock needs motor trade insurance at 1,500 to 3,000 pounds a year. Not worth the subscription; a UK flip is a scoped test with compliance priced first, only if Luke wants that lane. Job: Make money buying and reselling used cars part time in the UK (still open) Write-up: `TRITON-CORE/Research/links/2026-10-09-ai-car-trader-skool.md` Link: https://www.skool.com/ai-car-trader-9959

## 2. [hn] Yandex Takes a Second Data Center Hit in 48 Hours
key: hn:50020927
url: https://united24media.com/war-in-ukraine/yandex-takes-a-second-data-center-hit-in-48-hours-now-its-biggest-russian-site-is-damaged-23277
discussion: https://news.ycombinator.com/item?id=50020927
meta: {"points": 198, "comments": 272, "created": "2026-10-09T14:20:19Z"}
query: car data

page: Yandex Takes a Second Data Center Hit in 48 Hours—Now Its Biggest Russian Site Is Damaged — UNITED24 Media Language en Language English Español Search Latest News War in Ukraine Defense Tech Investigations World Life in Ukraine Opinion Inside Ukraine Inside Ukraine See all Photoreports Videoreports Web-stories Newsletter Account About us Our team Privacy Policy | How We Protect Your Data at UNITED24 Media A drone attack struck a major Yandex data center in Russia’s Kaluga region, knocking several modules completely out of service, according to Russian state media TASS on October 9. We bring you stories from the ground. Your support keeps our team in the field. DONATE NOW “Several modules of the Yandex data center in Kaluga have been completely taken out of operation as a result of a UAV attack, the company reports,” TASS said. The Kaluga facility, located in the Grabtsevo industrial park, was designed as Yandex’s largest data center in Russia. Construction began in 2022, with the site entering operation in the second half of 2023. Read more Category World Drone Strike on Yandex Data Center Triggers Widespread Internet Outages Across Russia Oct 08, 2026 20:16 The complex covers roughly 130,000 square meters and has a planned power capacity of 63 megawatts—about 50% greater than some of Yandex’s other major data centers. It can accommodate more than 3,800 server racks, each designed for loads of up to 15 kilowatts. The facility supports Yandex’s internal services and was also built to expand Yandex Cloud, including the company’s fourth availability zone. Earlier, satellite images revealed the extent of the damage to a data center operated by Russian technology company Yandex in Sasovo, Russia’s Ryazan region, after a Ukrainian drone strike. Discuss this article: PERPLEXITY CHATGPT CLAUDE GEMINI Help us understand what you already know Join United24 audience survey Related articles Author Katherina Popilnichenko Category War in Ukraine Kyiv Faces Internet Disruptions a
comment (lapkaaaa): New Startup idea - private anti-air batteries for data centers
comment (cyanydeez): someone go correlate whether this leads to a drop in bot/AI traffic.
comment (thinkcontext): Interesting to see this and the targeting of data centers in the Middle East. Its critical infrastructure and a hit gets the attacker a lot of bang for the buck in terms of economic damage.

## 3. [github] franzenzenhofer/big-arrow-on-the-screen: Let your AI agents paint big arrows, boxes and text on your Mac screen. One CLI, click-through, gone by itself. Skill for Claude Code and Codex. MIT.
key: gh:franzenzenhofer/big-arrow-on-the-screen
url: https://github.com/franzenzenhofer/big-arrow-on-the-screen
meta: {"stars": 428, "created": "2026-10-08", "pushed": "2026-10-09", "language": "Swift", "topics": ["accessibility", "ai-agents", "claude-code", "cli", "codex", "macos", "swift"]}
query: claude-code created:>{since} stars:>20

# Let your AI agents paint big arrows, boxes and text on your screen

**big-arrow-on-the-screen** (`bigarrow`) is a macOS command-line tool, plus a skill for Claude Code and Codex, that draws an arrow and a sign on top of every window. Clicks go through, your keyboard focus stays put, and the arrow removes itself. MIT licensed.

[](https://github.com/franzenzenhofer/big-arrow-on-the-screen/actions/workflows/ci.yml)
[](LICENSE)

[Real apps](#real-apps-real-use-cases) · [Copy & paste](#copy--paste) · [What is it for?](#what-is-this-actually-for) · [Install](#install) · [Commands](#the-three-commands-an-agent-needs) · [Looks](#looks) · [Creative arrows](#creative-arrows) · [Starred by](#starred-by) · [FAQ](#faq) · [How we know it works](#how-we-know-it-works) · [For agents](#for-agents-and-the-humans-who-configure-them) · [Plan](#plan-decisions-research) · [Prior art](#prior-art-and-thanks) · [License](#license)

> Your AI agent can refactor a monorepo, write a migration and explain monads, but when it needs you to click one button it prints *"please click Allow in the dialog"* into a terminal you are not looking at. `bigarrow` gives it a finger.

```bash
bigarrow point --element "Allow" --app "System Settings" --text "Franz, click Allow: Ghostty may control your Mac"
```

One transparent window above everything, on every display and every Space. Drawing needs **no macOS permission at all**. One Swift binary: no daemon, no menu-bar icon, no account, no telemetry, and, we checked twice, no AI inside. It is an arrow.

## Real apps, real use cases

Real apps on a real Mac (macOS 27), the real `bigarrow`, staged by `scripts/real-scenes.sh`.

### macOS Desktop & Dock: stop "click wallpaper to show desktop"

["The most annoying change in Mac update history"](https://www.imore.com/mac/macos/macos-sonoma-click-to-reveal-desktop-turn-off), fixed in six arrows ([MP4](docs/videos/wallpaper.mp4)).

### System Settings: grant a permission

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
bigarrow start --element Terminal_Toggle --app "System Settings" \
  --text "Franz, switch this on: Terminal may control your Mac" --from right --color green --close-button
bigarrow start --element Add --role button --app "System Settings" \
  --text "Not in the list? Plus. Then find it." --from bottom-right --style ring --color orange --shape zigzag --size S
```

### Keynote: a three-step how-to

```bash
bigarrow start --element Animate --app Keynote --role radiobutton --text "1. Click Animate" --from right \
  --style ring --color purple
bigarrow start --element "Add an Effect" --app Keynote --text "2. Add an Effect" --from right \
  --style box --corners sharp --color "#FF9F0A" --shape straight
bigarrow start --element Play --app Keynote --role button --text "3. Press play. Bask in the applause." \
  --from top --color teal --shape zigzag --size S
```

### Print dialog: helping Mom save a PDF

```bash
bigarrow start --element PDF --role button --app TextEdit \
  --text "Mom, click PDF, then Save as PDF" --from bottom --color pink --border white-black
bigarrow start --element Cancel --role button --app TextEdit \
  --text "Not this one, Mom" --from bottom-right --color black --size S
```

### Chrome: the right tab out of 14

```bash
bigarrow start --app "Google Chrome:Sourdough" --element "Sourdough - Wikipedia" --role radiobutton \
  --text "It's this tab, not the other 13" --from top --shape zigzag --color "#5856D6" --siz

## 4. [arxiv] Unlocking the Regulatory Genome by ARGUS: An Evidence-Constrained Agentic Framework for Interpreting Single Nucleotide Variants
key: arxiv:2610.12281
url: https://arxiv.org/abs/2610.12281
meta: {"published": "2026-10-08", "authors": ["Pratik Dutta", "Matthew B. Obusan", "Max Chao", "Rekha Sathian"], "categories": ["q-bio.GN", "cs.AI", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

Over 90% of disease-associated variants from genome-wide association studies fall in noncoding regulatory regions, yet their functional interpretation remains a central open problem in genomic medicine. Large language models prompted to interpret such variants routinely hallucinate transcription factor (TF) binding changes, fabricate experimental support, and assign biological significance to statistically negligible signals. We present ARGUS (Agentic Regulatory Genomics for an Uncertainty-aware Scientist), which strictly separates deterministic biological computation from LLM-mediated reasoning. ARGUS wraps 458 DNABERT-based TF binding models in a hypothesis-directed investigation loop where a planner selects evidence sources based on current uncertainty, a verifier deterministically interprets each observation, and intermediate results change the investigation path. On variant rs6983267 at the 8q24 cancer risk locus, the same planner produces four divergent trajectories for four TFs. FOXA1 is rescued in 3 steps when real ADASTRA allele-specific binding data (15 experiments, FDR = 0.030) reveals a model false negative masked by saturation. KLF6 traverses 8 steps across ADASTRA, JASPAR motif analysis, and ENCODE cCRE regulatory annotation before abstaining due to mixed indirect evidence. RAD21 abstains in 8 steps after ADASTRA returns a coverage-qualified but nonsignificant allelic test (5 experiments, FDR = 0.65), and SP1, which shares FOXA1's saturated retained prediction, abstains because no direct experimental evidence exists at this locus. All observations come from real ADASTRA, JASPAR, and ENCODE cCRE queries; none are simulated. A comparison of fixed-priority and LLM-mediated planning shows that the LLM planner reaches identical verdicts with fewer tool calls by declining evidence that cannot resolve the claim under test.

## 5. [youtube] Local AI on a Mac Is a Waste of Money (M5 Pro vs a $20 Subscription)
key: yt:kLNDGwaHohE
url: https://www.youtube.com/watch?v=kLNDGwaHohE
meta: {"channel": "JSyntax", "rank": 1}
query: local llm mac benchmark m5


[body unavailable: IpBlocked]

## 6. [awesome] 4da-systems/4da (new in awesome-mcp-servers)
key: gh:4da-systems/4da
url: https://github.com/4da-systems/4da
meta: {"list": "awesome-mcp-servers", "stars": 2, "created": "2026-01-19", "language": "Rust", "description": "Privacy-first developer intelligence — surfaces what matters from the noise"}
query: awesome-mcp-servers

[](https://github.com/4DA-Systems/4DA/actions/workflows/validate.yml)
[](LICENSE)
[](https://www.npmjs.com/package/@4da/mcp-server)
[](#download)

**All signal. No feed.**

 

---

**4DA reads the internet for developers — privately, locally. Your codebase decides what's relevant.**

It scans your codebase — `Cargo.toml`, `package.json`, `go.mod`, Git history — and scores every article, advisory, and release from 20+ sources against what you actually build. An item needs 2+ independent signals to survive. Everything else is rejected.

Benchmarked across 9 developer personas against a 245-item labeled corpus — 1,997 scored evaluations: **93% of content is rejected, and 98.9% of labeled noise is correctly rejected.** Those are measured numbers, and you can [reproduce them in one command](#benchmarks). Your real rejection rate — computed from your own data, not ours — is shown in the Signal tab.

Saves and dismissals build a preference profile you can inspect, pin, or forget — and teach the Brief what to stop showing you. Relevance scoring itself stays grounded in your actual stack. And when the engine improves, it re-judges everything it already holds: yesterday's noise becomes tomorrow's signal.

### The fastest way to try it

Already using Claude Code, Cursor, or Windsurf? One command:

```bash
npx @4da/mcp-server
```

This scans your project, detects your stack, and gives your AI assistant live vulnerability scanning, dependency health, upgrade planning, and ecosystem intelligence. No API keys. No accounts. Works standalone — no desktop app required. [Full MCP documentation.](https://github.com/4DA-Systems/4da-mcp-server)

 
   
 

---

## How It Works

### Scoring

5 independent signal axes. An item must pass **2 or more** to surface. Single-axis matches are hard-capped at 28% — no matter how strong one signal is, it cannot pass alone.

| Axis | What it measures |
|------|-----------------|
| **Context** | Semantic similarity to your active codebase |
| **Interest** | Alignment with your declared topics |
| **ACE** | Real-time signals from your Git commits and file edits |
| **Dependency** | Direct matches against your installed packages |
| **Learned** | Reserved — held out of scoring until it can be validated against your explicit feedback |

What passes the gate goes through 12 quality multipliers: content depth, novelty detection, competing tech penalties, title-body coherence, and intent scoring from recent work. Every constant is calibrated across 9 simulated developer personas with 245 labeled test items.

### LLM Verification

After keyword scoring, an LLM layer verifies the top items against your full developer context — stack, dependencies, recent commits, anti-technologies, and engagement history. Strict 1-5 rubric:

- **5 = MUST-READ**: Security alert for YOUR dependency, breaking change YOU must act on
- **3 = WORTH KNOWING**: Useful tool that fits YOUR exact stack
- **1 = NOISE**: Mentions your tech but isn't actionable

This is where the gold surfaces — articles the keyword pipeline misses because there's no keyword overlap, but the LLM understands the conceptual relevance to your specific project.

**You own the compute.** Use [Ollama](https://ollama.com/) for free local inference (fully private), or bring your own Anthropic/OpenAI key. 4DA never pays for your compute, never stores your keys remotely, never makes API calls you didn't configure.

### Anti-Gaming

Content creators who learn the scoring algorithm still ca

## 7. [vault] Join and extract the four free communities that cover both asks: Emerging Fashion Designers, Rich Off Clothes, RiseWise, SandersConsulting
key: vault:2026-10-08:join-and-extract-the-four-free-communities-that-cover-both-a
url: https://www.skool.com/discovery?q=fashion+design
meta: {"vault_status": "open", "kind": "market", "subject": "Skool fashion design, marketing and branding communities (survey of 65)", "date": "2026-10-08", "where": "TRITON-CORE/Ventures/Luxury-Clothing/research/SKOOL-FASHION-COMMUNITIES-2026-10-08.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Desktop pane, Luke approves each join, extractor kit, digest

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (market) Read-only survey from Skool discovery, about and classroom pages, no login. 65 fashion-relevant communities; the large free ones are drop-and-scale business groups (Rich Off Clothes 1,067, RiseWise 360, SandersConsulting 297), the design-led one is Emerging Fashion Designers (504, free, designer-run), and the biggest overall is an AI fashion design group at 9 dollars a month (THE BLUEPRINT, 1,619). Private groups hide course lists; joining is Luke's tap via the desktop pane. The Luxury Clothing venture stays parked; this answers the question only. Job: Learn fashion design and clothing-brand marketing from working practitioners cheaply (still open) Write-up: `TRITON-CORE/Ventures/Luxury-Clothing/research/SKOOL-FASHION-COMMUNITIES-2026-10-08.md` Link: https://www.skool.com/discovery?q=fashion+design

## 8. [hn] Show HN: Edi Life OS – self-hosted life dashboard with an MCP server for AI
key: hn:50014150
url: https://github.com/edrisranjbar/lifeos
discussion: https://news.ycombinator.com/item?id=50014150
meta: {"points": 39, "comments": 15, "created": "2026-10-09T00:02:19Z"}
query: mcp server

page: GitHub - edrisranjbar/lifeos: Self-hosted life OS: habits, goals, Kanban, finance and focus, with an MCP server for AI. · GitHub Skip to content You signed in with another tab or window. Reload to refresh your session. You signed out in another tab or window. Reload to refresh your session. You switched accounts on another tab or window. Reload to refresh your session. Dismiss alert {{ message }} main Branches Tags Go to file Code Open more actions menu Latest commit History 61 Commits 61 Commits Folders and files Name Name Last commit message Last commit date .github .github docker docker docs docs lib lib mcp mcp public_html public_html site site tests tests .dockerignore .dockerignore .env.example .env.example .gitattributes .gitattributes .gitignore .gitignore CONTRIBUTING.md CONTRIBUTING.md Dockerfile Dockerfile LICENSE LICENSE README.md README.md _en_map.json _en_map.json _post.js _post.js _script_step1.js _script_step1.js _transform.js _transform.js api.php api.php api_auth.php api_auth.php attachments.php attachments.php auth.php auth.php config.example.php config.example.php credentials.php credentials.php db.php db.php docker-compose.yml docker-compose.yml finance-obligations.php finance-obligations.php intro-preview.gif intro-preview.gif kanban.php kanban.php login.php login.php logout.php logout.php migrate-sqlite.php migrate-sqlite.php server.php server.php state.php state.php weather.php weather.php View all files Repository files navigation Edi Life OS One self-hosted home for your focus, habits, goals, money and projects — with an MCP server so your AI assistant can work alongside you. Quick start · Tour · AI / MCP · Deploy · API Most of us run our lives across a to-do app, a habit tracker, a budgeting spreadsheet, a Pomodoro timer and a notes app — and none of them know about each other. Edi Life OS puts all of it in one calm, private dashboard and connects the small things you do today to the direction you want your life to take. Everything in one 
comment (ceejayoz): Have you asked Claude to critique this code? It's... not super complimentary. There are design anti-patterns I haven't seen in two decades.
comment (esseph): This is a neat idea!
comment (onaclov2000): I'm attempting to do the same thing but for personal health Data.

## 9. [github] Jakeschincariol/founder-skill: Eleven free Claude skills that test a business before you launch it: a board trained on Hormozi, Thiel and Jobs, a marketing director, a CFO, and a consumer panel of 100 buyer agents. Free, MIT.
key: gh:jakeschincariol/founder-skill
url: https://github.com/Jakeschincariol/founder-skill
meta: {"stars": 187, "created": "2026-10-07", "pushed": "2026-10-07", "language": "Python", "topics": ["business-plan", "claude-code", "claude-skills", "startup", "subagents", "unit-economics"]}
query: claude-code created:>{since} stars:>20

# The Founder skill

Eleven Claude skills that test a business before you launch it. Free, MIT, no
signup, no API key, nothing to connect.

`skills/founder-board` `skills/founder-marketing` `skills/founder-cfo`
`skills/founder-consumer` `skills/founder-launch` `skills/founder-pricing`
`skills/founder-offer` `skills/founder-competitors` `skills/founder-brand`
`skills/founder-ops` `skills/founder-plan`

One of them is your board of directors, trained on the frameworks of Alex
Hormozi, Peter Thiel and Steve Jobs. One is your marketing director. One is your
CFO and finds your real profit margins. And one is the consumer panel: it spins
up 100 buyer agents trained on your target customer and runs your business
through 100 buyer scenarios.

So you know how to launch, how to market and how to actually make money, before
you spend thousands of dollars finding out the hard way.

## Install

Paste this repo link into Claude and say `install skill`:

```
https://github.com/Jakeschincariol/founder-skill

install skill
```

Or as a plugin, in Claude Code:

```
/plugin marketplace add Jakeschincariol/founder-skill
/plugin install founder-skill@founder-skill
```

Claude Code namespaces plugin skills, so installed as a plugin they show up as
`/founder-skill:founder-board` and so on. Copy the folders instead if you want
plain `/founder-board`:

```bash
git clone https://github.com/Jakeschincariol/founder-skill.git
cp -r founder-skill/skills/founder-* ~/.claude/skills/
```

Project-local instead of global: copy the same folders into your repo's
`.claude/skills/`. No Claude Code at all? Paste any single `SKILL.md` at the top
of a chat and it runs as a mode. You lose the sub-agents and the Python tools,
but the method works.

The tools need Python 3.8 or newer. Nothing to pip install.

## The eleven

| command | job | what it does |
| --- | --- | --- |
| `/founder-board` | Board of Directors | Three board members, each a sub-agent applying one published framework (Offers, from *$100M Offers*; Monopoly, from *Zero to One*; Product, from Isaacson's *Steve Jobs*), score the idea, name what would kill it and vote. |
| `/founder-competitors` | Competitor Scout | Maps direct competitors, indirect ones and substitutes from public sources, with prices, positioning and what their customers complain about, every fact linked. |
| `/founder-consumer` | Consumer Panel | Spins up a swarm of buyer agents (100 by default) from your target customer, each with its own income, habits and objection, and tallies who buys, who doesn't and why. |
| `/founder-pricing` | Pricing Strategist | Turns the panel's price answers into an acceptable price range, sets it against competitors and your margin, and picks what to test. |
| `/founder-offer` | Offer Architect | Builds the offer stack (bonuses, guarantee, real urgency, a name) that answers the panel's objections, then re-tests it on the panel. |
| `/founder-cfo` | CFO | Unit economics: contribution per sale, the real profit margin, break-even per day, year 1 month by month, cash needed, payback, what-ifs. |
| `/founder-marketing` | Marketing Director | Positioning, the channels your buyers use, a dated 30-day launch campaign, ten hooks and the most you can pay for a customer. |
| `/founder-brand` | Brand Designer | Name candidates with the trademark, domain and handle checks to run, a voice, a promise and a brief for the look. |
| `/founder-ops` | Operations Manager | Suppliers, staffing, day-one routines, tools, the permits to ch

## 10. [arxiv] A Closer Look at Agentic BBO: Benchmarking LLM Agents for Black-Box Optimization
key: arxiv:2610.12183
url: https://arxiv.org/abs/2610.12183
meta: {"published": "2026-10-08", "authors": ["Ming Chen", "Rong-Xi Tan", "Ke Xue", "Yu-Jie Zhou"], "categories": ["cs.LG", "cs.AI", "cs.NE"]}
query: all:"language model" AND all:agent AND all:tool

Black-box optimization (BBO) arises in many scientific and engineering problems where objective evaluations are expensive and limited. Recent large language model (LLM) agents offer a new way to approach BBO by combining task semantics, computation, optimization tools, and feedback-driven decision making, showing great potential due to the integration with mathematically rigorous tools. However, existing agentic BBO studies use different task domains and system configurations, making their results difficult to compare and the effects of individual design choices hard to isolate. We therefore introduce AgenticBBO-Bench, a cross-domain benchmark for agentic BBO spanning synthetic functions, hyperparameter optimization, database tuning, chip design, and molecular design under a unified finite-budget evaluation protocol. In our experiments, agentic BBO achieves higher family-averaged scores than direct LLM-based methods in all five domains and outperforms the best numerical optimizers in four. We further study three factors shaping agent performance: optimization tools, task information and prior knowledge, and the role of the LLM during search. Our results show that additional numerical tools do not consistently improve performance, task semantics are broadly useful while more specific priors are less reliable, and numerical optimizers can effectively absorb gains from search trajectories established by the agent. Finally, we introduce a five-task frontier challenge within AgenticBBO-Bench and evaluate seven LLMs under the Codex agent harness, where GPT-6 Astra and DeepSeek-V4.1-Flash lie on the Pareto frontier of performance and cost among the evaluated models. Our code is available at https://github.com/lamda-bbo/agentic-bbo.

## 11. [youtube] How Expected Goals xG Actually Works
key: yt:h32AlMsWV-o
url: https://www.youtube.com/watch?v=h32AlMsWV-o
meta: {"channel": "football for everyone", "rank": 2}
query: expected goals model from scratch


[body unavailable: IpBlocked]

## 12. [awesome] a1-x-tech/mcp-google-crux (new in awesome-mcp-servers)
key: gh:a1-x-tech/mcp-google-crux
url: https://github.com/a1-x-tech/mcp-google-crux
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-08-09", "language": "TypeScript", "description": "MCP server for Google CrUX — check real-user Core Web Vitals and compare mobile, desktop and 40-week trends"}
query: awesome-mcp-servers

#   Google CrUX MCP

**English** | [Русский](./README.ru.md)

[](https://www.npmjs.com/package/mcp-google-crux)
[](https://glama.ai/mcp/servers/A1-x-Tech/mcp-google-crux)
[](https://github.com/A1-x-Tech/mcp-google-crux/actions/workflows/ci.yml)
[](./LICENSE)

**A1 Google CrUX MCP** brings real-user Core Web Vitals data into an AI app. Check whether a public site or page passes LCP, INP and CLS, compare mobile with desktop, and see how the metrics changed over time.

It reads Google’s Chrome UX Report dataset — field data collected from Chrome users, not a synthetic speed test or a way to change your site.

- **6 read-only tools.** Core Web Vitals assessment, device comparison, origin-versus-page comparison, 40-week trend and raw latest or historical records.
- **Real-user data.** It is the same CrUX field data used by PageSpeed Insights and Google’s Core Web Vitals signals.
- **Clear availability boundary.** Only public origins and URLs with enough real-user traffic have data; `no_data` is a valid result.
- **Known quota cost.** CrUX allows 150 queries per minute per project. Device comparison makes four API calls; origin-versus-page makes two.

Start with a read-only question:

> Does `https://example.com` pass Core Web Vitals on mobile?

[Connect the server](#quick-start) · [Explore use cases](#what-you-can-ask-it-to-do) · [Open technical documentation](#technical-documentation)

---

## See it work in a minute

> **You:** Does `https://example.com/pricing` pass Core Web Vitals on mobile?
>
> **Assistant:** Shows p75 LCP, INP and CLS, their good/needs-improvement/poor ratings and the overall result. Nothing changes.
>
> **You:** Compare this page with the site average and show how mobile differs from desktop.
>
> **Assistant:** Compares the origin and URL, then device groups and their traffic shares. All six tools read the public CrUX dataset only.

## Contents

- [Quick start](#quick-start)
- [What you can ask it to do](#what-you-can-ask-it-to-do)
- [How to read CrUX data](#how-to-read-crux-data)
- [Getting access](#getting-access)
- [Configuration](#configuration)
- [Data, limits and background work](#data-limits-and-background-work)
- [Technical documentation](#technical-documentation)
- [Support](#support)

## Quick start

You need Node.js 20+ and a Google Cloud API key with Chrome UX Report API enabled.

1. [Create a restricted API key](#getting-access).
2. Add the server to your AI app.
3. Ask the read-only question above.

   Codex  

 

In **Settings → MCP servers**, select **Add server**, choose **STDIO**, enter the command `npx -y mcp-google-crux@latest` and environment variables `CRUX_API_KEY`, then select **Save** and **Restart**.

```bash
codex mcp add google-crux --env CRUX_API_KEY=your_key -- npx -y mcp-google-crux@latest
codex mcp list
```

[Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

 

   Claude Code  

 

```bash
claude mcp add --env CRUX_API_KEY=your_key --transport stdio --scope user google-crux -- npx -y mcp-google-crux@latest
claude mcp list
```

[Claude Code MCP documentation](https://code.claude.com/docs/en/mcp)

 

   Claude Desktop  

 

The current official path is **Settings → Extensions**. For a custom desktop extension, open **Advanced settings → Extension Developer → Install Extension…**, select a `.mcpb` file and follow the prompts.

This repository currently publishes an npm stdio package and does not contain a `.mcpb` bundle. For Claude Desktop builds that still s

## 13. [vault] x402 per-call payment rails for agents, Coinbase-originated, now under Linux Foundation governance
key: vault:2026-09-20:x402-per-call-payment-rails-for-agents-coinbase-originated-n
url: https://docs.google.com/document/d/1_KvqUJXH1z7RUjrnbal0JVgGcJyP4yFfOdyZ1PRWbQs/edit?usp=drivesdk
meta: {"vault_status": "open", "kind": "tool", "subject": "Agent402 (agent402-mcp on npm, plus the @seb.ai setup guide)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-agent402.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Legitimises the rails, not any operator; Agent402 uses the official packages

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Guide and package both read clean, source audited offline. A three-month-old solo project (nine stars, no independent review) whose guide gets its own spending-limit claim backwards. Not installed on the main machine. If ever tried: pin the version and run it in a sandbox. Job: Give an agent hundreds of paid tools with per-call billing and no per-service signup (solved) Write-up: `TRITON-CORE/Research/links/2026-09-20-agent402.md` Link: https://docs.google.com/document/d/1_KvqUJXH1z7RUjrnbal0JVgGcJyP4yFfOdyZ1PRWbQs/edit?usp=drivesdk

## 14. [hn] Show HN: Apogee: Rebuilding Mozilla's Orbit, fully local and private
key: hn:50017301
url: https://github.com/darshi1337/apogee
discussion: https://news.ycombinator.com/item?id=50017301
meta: {"points": 52, "comments": 2, "created": "2026-10-09T07:36:19Z"}
query: mcp server

Hey everyone! Last year, Mozilla released Orbit, an AI-powered browser summarizer hosted on a GCP server. After people started digging into the extension, they discovered things like backend endpoints such as store_result. Eventually, Mozilla discontinued the project. For the past month, I’ve been trying to rebuild Orbit from scratch, but with one major difference: Apogee is fully local and privacy-focused. Apogee doesn’t send or store your data. It can directly connect to your local Ollama instance for inference. I’ve also added WebGPU integration for Chrome and Transformers.js for Firefox to provide faster, local responses. It can summarize: Articles and websites, YouTube and Billie videos, Wikipedia articles ,Hacker News and Reddit threads. Install Apogee: Chrome: https://chromewebstore.google.com/detail/apogee/pgemlpomhkdc ... Firefox: https://addons.mozilla.org/en-US/firefox/addon/apogeeext/ Obviously it is far from complete. Would love to hear your feedback and suggestions!
comment (genpfault): > https://github.com/darshi1337/apogee/blob/main/MODELS.md#loc... > Unlike Ollama, [llama.cpp] serves one model at a time: the GGUF you launched it with. FWIW: llama-server's supported multiple models for a while now: https://github.com/ggml-org/llama.cpp/tree/master/tools/serv...
