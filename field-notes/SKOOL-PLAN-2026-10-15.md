# Skool: extraction done, tier decision, reading, skills plan (15 Oct 2026)

Luke's ask, 15 Oct: extract the rest of what we can open, decide whether any tier is worth paying for,
run a reading plan, then a skills plan (skill or workflow, for us, our clients or prospects).

## 1. Extraction

Everything open to the signed-in account is now on disk under `field-notes/skool/` (gitignored).

| Room | What came down |
|---|---|
| Matt Ryder F The GuRUs | All 24 open courses: the 7 text courses again with their videos, onboarding calls, 13 Downloadable resources, Make More Money, and all 14 coach recording libraries. 603 modules, 465 Skool-hosted videos captioned (398 hours, 4.2M words, every one complete to its last cue), 23 more PDFs (sales management, dialling, compliance, Book of Reframes) |
| Rebel Economist (Steve Keen) | 40 lessons, 7 videos, 3 free books (Funny Money, New Economics Sampler, Elon is Wrong) |
| 3-hour YouTube Leads | 24 open lessons, 23 Loom transcripts |
| DOOing AI Foundry | 12 open lessons |
| BettrNation | 11 open lessons, 10 Commandments PDF |
| All PDFs (47) | text extracted beside each file; one image-only (the Klaviyo example report) |

Still to come: **272 YouTube-hosted lessons** (239 in Luke's vault rooms, mostly Automatable and
Brendan, plus 33 from today's rooms). YouTube blocked this Mac's IP for captions after a burst at
06:30; `sandbox/yt_retry.py` tests hourly and runs them captions-only at one every 20 seconds once
it lifts. No whisper fallback, which would take a day of compute.

Not reachable: Analytics Club, Leverage AI, Emerging Fashion Designers, Rich Off Clothes, RiseWise,
SandersConsulting (joins pending or classroom closed). One Loom refused its transcript.

New routes this session, all keyless: Skool-hosted video captions (Mux) for a whole room in one page
script, signed file downloads, Vimeo embed captions, public Notion pages. The extractor is reusable:
any room is one call now.

## 2. Tier decision

Full list with unlock terms: `field-notes/skool/LOCKED-TIERS-2026-10-15.md`.

**Recommendation: pay for nothing now. £0.** Reasons, from the 16 readers and the lock data:

- No reader found locked material that the free part did not already explain. Repeatedly the free
  layer gives the mechanism and the paid layer gives more examples, coaching calls or the author's own
  tool (Consulti, Email Bison, his skill files) that we can write ourselves.
- Most locks are **levels, not money**: Ryder's Outbound Dialing and Follow-ups, Agent J's paths, AIS
  Build Your AI OS. Levels come from posting and being liked in the room as Luke. That is your call,
  not a purchase, and I do not post.
- Ryder: do not resubscribe at $69. Everything open is captured before access ends on 21 Oct. The two
  locked courses that matter (7. Outbound dialing, 6. Follow-ups) are level 2, not a payment.
- Steve Keen's 7-week course (about $500 a year): the free book already has the model's equations.
- BettrNation, YouTube Leads add-ons ($19, $27, $1,000/mo coaching), Email Marketing Community
  products, AAA Ninjas packs: no case made by any reader.

**The one to watch:** AAA Ninjas' Lead Rescue 48h and Sleeping Beauty material sits behind owner
unlock (affiliates and buyers) and feeds your Database Reactivation framework. If reactivation becomes
a live Triton offer, that is the first lock worth pricing. Not before.

## 3. Reading

16 groups read on Sonnet and Haiku readers this morning (S-22 to S-37), plus S-21 last night.
Digests in `state/agents/skool/`, one line each in this week's Field Notes draft.

| Verdict | Groups |
|---|---|
| TRY (6 today, plus S-21 last night) | S-24 cold email domain health audit; S-25 UK trades list from OpenStreetMap; S-26 website audit as a lead magnet; S-32 funnel leak calculator; S-35 Keen debt model rebuild; S-36 YouTube outlier finder; (S-21 call consistency and funnel check) |
| PARK (9) | S-22, S-30 objection matrix (useful triage order, but the fear half is pressure selling); S-23, S-31, S-33, S-34 Ryder management, outbound, AI-in-sales, own sessions; S-27 the full Claude Code cold email machine (needs a paid sender and your accounts); S-28 email agency; S-37 local AI and betting |
| SKIP (1) | S-29 Klaviyo and pop-up how-to |

Honest gaps:
- **Ryder's outbound library got a bad sample.** Coach Cayden's three picks were an intro and two
  role-play Q&As, not dialling. S-38 re-reads the four sessions with the most dialling talk. Counting
  first was itself telling: the best of 53 "Outbound and Identity Selling" sessions mentions dialling,
  pick-ups, voicemail or gatekeepers 31 times in 10,000 words, so the library is mostly sales
  conversation, not phone work.
- The coach libraries were sampled, not read: about 400 of 465 sessions are unread by design. The
  readers agree the sessions repeat the course frames, so I would not read more without a reason.
- The 272 YouTube lessons get a Haiku title-and-opening triage once they are transcribed (S-39).

## 4. Skills plan

What the readers proposed, merged where they overlap. Everything here is keyless for a first version.
Built as prototypes in `sandbox/` first; anything for clients becomes a skill only on your word, since
skills live in your `~/.claude/skills/` and outside my write roots.

### Build first: the prospect door-opener (for Triton, as a demo and a lead magnet)

**A. Prospect audit pack** (skill, from S-24, S-26, S-28). Give it a firm's domain. It checks the
cold email basics (SPF, DKIM, DMARC, nameservers, blacklists), audits the website (HTTPS, speed, mobile,
click-to-call, contact form, reviews, "24 hour" wording) and writes a one-page result with three
specific findings. The mechanism every room agrees on is "a specific result about them is the offer".
Works for plumbing and HVAC firms and for firms with sales teams. Needs `dig` and a web fetch only.

**B. UK trades list builder** (skill or workflow, from S-25). A trade and an area in; OpenStreetMap
listings, website, phone, an MX check on the domain and a fit score out, as a CSV. A PECR step drops
sole traders and partnerships (individual subscribers under UK rules). Pairs with A: list, then audit,
then a drafted message that you approve one at a time.

A then B is a workflow: list → audit → draft. Nothing is sent without your approval.

### Build second: tools for a client that has a sales team

**C. Sales funnel diagnostic** (skill, from S-21, S-23, S-32, S-34). Weekly counts in (dials,
answered, booked, shown, closed, no-shows split by type); the stage where one point of improvement is
worth most out, plus reverse maths from a revenue target and a monthly report. Includes a CRM
reactivation pass: lost deals and no-shows older than 14 days ranked for a call. Runs on dummy data as
a demo. This is your Database Reactivation and Selling frameworks made runnable.

**D. Call grader and role-play drill** (skill, from S-22, S-30, S-32, S-33, S-34). A transcript and
a rubric the client signs off in; the same score every time with timestamps and two actions. The drill
plays a prospect with a hidden objection and grades the order (logistics first). Build only the
qualification half; the fear and pressure half is not something to sell to trades. Needs real call
transcripts and consent, so it waits for a client.

### For you and Neptune

**E. Cold email strategy brief and copy checker** (skill, from S-26, S-27). An interview, then
segments, triggers, a four-step sequence with one-variable A/B tests, a volume calculator, and a copy
check against the short-email rules. UK framing (PECR) built in. No ghost ink.

**F. YouTube outlier finder** (workflow, from S-36). Competitor channels' public feeds, videos at 3x
their channel median, grouped by title shape. Topic ideas for Neptune content.

### For Proteus only, as probes not skills

- Keen's private debt model rebuilt in scipy (S-35): does the crash come from the maths or the
  parameters? 30 minutes.
- Tipster-claim audit wrapper (S-37): hit rate, closing-line value and the luck test on a claimed
  record. Fits the audited-tipster lane.

### Not building

The Klaviyo reporting skill (only for a Klaviyo client), ghost ink (hidden text in emails), the local
AI path (closed on an Intel Mac), objection fear tactics, anything that needs a paid sender before a
client pays for it.

## What I do next without asking

- Prototype A and C in `sandbox/` on public sites and dummy data, measured against a written pass mark.
- Queue S-38 (Cayden outbound, picked by title) and S-39 (YouTube triage) for the nightly.
- Keep the Skool dashboard current.

## Your calls

- Spend: agree £0 on tiers for now.
- Whether A and B become real skills for Triton once the prototypes work.
- Whether to earn levels in Ryder's room by posting (it ends 21 Oct anyway).
