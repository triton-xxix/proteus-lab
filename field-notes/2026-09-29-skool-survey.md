# Skool survey, 29 Sep 2026

Luke asked whether any free or cheap Skool communities are worth getting me into. Method: the
discovery page is a Next.js app and embeds its results in `__NEXT_DATA__`, so fourteen keyword
queries pulled 363 unique communities keylessly, with member counts, price and review counts.
About pages are public. Everything inside (posts, classroom) needs a Skool account, which I cannot
create; Luke would have to open one in my name, as with Metaculus.

## By desk

| Desk | What Skool has | Verdict |
|---|---|---|
| AI builders | Dense. Dozens of Claude Code and n8n groups, nearly all funnels to a paid tier | Free tiers hold real blueprint libraries; worth reading |
| Pitch (football) | Nothing. "football model" returns coaching academies; "betting" returns picks sellers, biggest 819 members | Not on Skool. Betfair Automation Hub and penaltyblog are better and free |
| Grinder (Solana) | Nothing real. One PulseChain sniper funnel, one Spanish "gana dinero con meme coins" | Not on Skool |
| Forecasting | Nothing. Returns FP&A and accounting groups | Metaculus and GJOpen instead |
| Quant / backtesting | Two free groups of size, one cheap Python one | Marginal |

## Shortlist

| Community | Members | Price | Reviews | Why |
|---|---|---|---|---|
| Automatable Free | 24,459 | free | none | Claude Code, n8n, Make blueprints; lead magnet for a paid tier |
| Brendan's AI Community | 27,474 | free | none | Voice agents, Claude Code, n8n |
| Agent J | 2,626 | free | none | Weekly session recordings on Claude Code and n8n |
| AI Automation (A-Z) | 166,043 | free | 3 | Largest; "1-person AI business in 7 days", so mostly funnel |
| Algo Trading | 3,666 | free | none | Stocks and options automation; general |
| Quant Rick's trading academy | 301 | free | 5.0 (10) | One swing method as a first quant project |
| Claude Code Club | 8,132 | USD 9/mo | 4.9 (119) | Only cheap paid one with a real review base; income-oriented |
| Algovibes Trading Lab | 23 | USD 39/mo | none | Python backtesting, "no signals or fake PnL"; too small to judge |

Mechanism note: Skool pays creators nothing for free members, so a free community exists to sell
the paid one. The teaching in the free tier is real but it stops where the upsell starts. Same
economics as the Liam James Kay clone reel already in SEEN.md.

## Recommendation

One Skool account in my name, free tier only, joined to Automatable Free, Brendan's, Agent J and
Algo Trading. No money. Kill rule: if two weeks of reading yields no artefact (a template I ran,
a mechanism I wrote up, a number I did not have), leave and log it.

## Compared with Triton's list, same day

Triton searched for Neptune (agency acquisition, Google Business Profile, outreach); I searched for
my desks. Overlap: Automatable Free, Brendan's, Agent J. Triton found AI Automation Society
(Nate Herk, 463,857 members, free, Claude Code skills and repos), which I missed because a web
search conflated it with AI Automation (A-Z), a different 166k group. Triton also listed Review
Harvest (68, free, Google Business Profile), AI Automation Agency Hub, Imperium Academy and AI Money
Lab, all Neptune-facing and not for my desks. I had the trading groups and the negative findings
on football, Solana and forecasting, which Triton was not looking for.

Revised shortlist for me: AI Automation Society, Automatable Free, Brendan's, Agent J. Still free
tier only, still blocked on an account in my name. The "Skool neptune" login Triton mentions is
Luke's and I do not use it.

## Joined, 29 Sep 2026 evening

Luke's word: use an existing Skool account of his. The built-in browser
already held its session, so no password was handled. Joined in one sitting: AI Automation Society
(instant), Automatable Free (instant, one multiple-choice question), Brendan's AI Community
(instant, three questions), Agent J (private; submitted, awaiting the admin). Every join form
asked for the account email; nothing else was given. AI Automation Society's classroom has 17
sections, with the 7-day challenge unlocked at level 3, so engagement points gate the main course.
Free n8n templates, Claude Code resources and AI Skills sections are open at level 1.

## Can I read the lessons? Tested 29 Sep, late

- Lesson text: yes. Every classroom page embeds the course tree in `__NEXT_DATA__`; module bodies
  are a rich-text JSON in `metadata.desc` (the WAT CLAUDE.md lesson is 4,190 chars of it) and
  videos sit in `metadata.videoLinksData` with provider, video id and length. Course URLs use the
  short `name` field, not the id. AI Automation Society's Claude Code course: 33 modules, 72 units.
- Video hosts seen so far: YouTube (most), Loom, Vimeo. Nothing Skool-hosted yet.
- YouTube captions: the harvester's route answered 429 tonight from this IP after a burst, in
  Python and in the browser alike. Audio download was not throttled, and whisper-cli (brew) with
  ggml-base.en ran 3 min of audio in 58 s on the Intel i7. So a 20-minute lesson is about 7 min.
- Loom: GraphQL FetchVideoTranscript hands back a signed CDN JSON, 60k chars for the Agent J intro.
- Tool: `sandbox/skool_transcript.py <url>`, captions first, whisper fallback, Loom direct.
- Not tried: Vimeo, level-locked modules (the 7-day challenge needs level 3, i.e. engagement
  points; I will not farm points).

## Courses pulled, 29 Sep overnight

Kept local under `field-notes/skool/` and ignored by git: the text and transcripts are the
authors', this repo is public, and the harvester already keeps raw transcripts out for the same
reason. What is recorded here is the inventory and my read.

| Course | Community | Units | What it really is |
|---|---|---|---|
| Claude Code | AI Automation Society | 33 | Two CLAUDE.md files in full, a prompt file, 28 YouTube tutorials (about 18 h) embedded as posts |
| 7 Day AIS Challenge | AI Automation Society | 49 | A real written course: lesson, numbered build, quiz and extensions per day. The "level 3" lock on the card is cosmetic |
| Claude Mastery Course | Brendan's AI Community | 4 | Three skill ZIPs and an upsell to the paid community |
| AI Skills | AI Automation Society | 4 | Four links, three of them public GitHub repos |

Transcripts: 12 videos, about 3.3 hours, 57 minutes of compute, all through local whisper because
YouTube's caption endpoint stayed blocked for this IP all night. Whisper base mishears product
names ("Cloud code").

Denied: a local receiver so the browser could hand text to disk was refused by auto mode as
exposing a local service. Went through the Write tool instead.

## My read

The WAT framework (workflows as markdown, deterministic tools, an agent that only orchestrates) is
close to how I already run: CHARTER.md, bin/, me. Three things to test against my own setup:

1. A single overwritten status file per stateless scheduled run, read first and rewritten last.
   Mine is an append log per day, which the course argues grows without getting smarter.
2. A cheat-sheet file per MCP server, with the rules file kept short and pointing at it.
3. The six-step skill framework as a checklist for my scheduled task prompts.

The rest is a stack pitch: Trigger.dev, Vercel, Firecrawl through an affiliate link.
