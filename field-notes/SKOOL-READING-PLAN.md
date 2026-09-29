# Skool reading plan

Written 29 Sep 2026 on Luke's brief: read a couple a day, follow what flows or what groups
together, do the reading on a lesser model, and come back each night with "read this, could do
this, need this, or can do it with what we have". We do not have to use the tools they sell.

## What is unread

| Library | Items | Shape |
|---|---|---|
| Automatable, FREE YouTube Blueprints | 121 | One flat list. Newest first: Claude Code, then Antigravity, then n8n, then old Make.com |
| Brendan, Resource Hub | 94 | One flat list. Claude Code builds, then voice agents, then n8n, then old Voiceflow chatbots |
| Agent J, open to free members | 62 | Start Here 6, 7-Day Challenge 27, Inside Agent-J+ 16, n8n Crash Course 7, AI Automation 101 5, Live Take-Homes 1 |
| Agent J, locked | 152 | Claude Unlocked 56, Recordings 42, Prompting Masterclass 21, Vibe Code 13, three paths 24, Reward Room 4 |
| AIS, Claude Code course | 16 of 28 videos | The 12 most useful are transcribed; 16 remain, including the 10-hour masterclass |

## Tracks, in the order I will read them

Grouped by mechanism, not by community, so one night's reading compares like with like.

1. **Claude Code as an operating layer.** Agent J 7-Day Challenge against the AIS 7 Day Challenge
   I already hold; Automatable's Claude Code Masterclass, "I Replaced n8n With Claude Code",
   "8 Things Your Claude Code App NEEDS", "Make Claude Code Write EXACTLY Like You"; Brendan's
   "How To Build Agentic Workflows", "5 Claude Skills I Can't Live Without". About 14 items.
   Why first: it is my own tooling, and two 7-day challenges side by side show what is teaching
   and what is packaging.
2. **Scrapers and data pulls.** Automatable's "Scrape ANYTHING", n8n + Apify, Google Maps and
   contact scraper, Apollo, LinkedIn jobs, real estate listings; AIS Firecrawl (done). About 9.
   Why: open-data archaeology and the harvester. The question each time is what my keyless
   pullers already do.
3. **Voice agents.** Brendan has 41 of these. Sample five that differ in mechanism: the platform
   comparison, prompt hacks, latency, realism, LiveKit. Read more only if the five disagree.
   Why: mechanism hunting. How a caller really books, transfers and fails.
4. **Agent J, Inside Agent-J+.** 16 previews of what the paid room builds. Read as evidence for or
   against ever proposing the paid tier, nothing else.
5. **Skim by title only, Haiku, one pass.** Make.com and Zapier blueprints (about 45), Voiceflow
   chatbots (about 20), social posting and faceless video systems. Mostly 2023 to 2024 era. Read
   one only if the title pass flags a mechanism I have not seen.

Not read at all: upsell modules, discount codes, success stories, merch.

## How a night runs

- **Before the run, scripted, no model.** `sandbox/skool_batch_transcribe.py` transcribes the next
  two or three videos. Captions when YouTube allows, local whisper otherwise at a third of real
  time. Cap: 60 minutes of video a night, so at most 20 minutes of compute.
- **Reading children.** One Sonnet child per group of two or three items that belong together.
  Haiku for anything under ten minutes and for the title-only skim. Never the parent's model.
  At most two reading children a night: the charter allows four spawns and the harvester has one.
- **What a child reads.** Local files only: the transcript, the lesson text, and
  `field-notes/toolshelf.jsonl` for what is already here.
- **What a child writes.** One file, `state/agents/skool/<date>-<track>.md`, with fixed fields:
  what it teaches in five lines; the tools they used; what we already have that does the same
  job; what we would need to fetch; one thing worth trying and how big it is; verdict of try,
  park or skip.
- **What I do.** Read the digests, not the transcripts. Promote at most one "try" a night to the
  probe queue with source `skool`. Write the run log line: read X and Y, could do Z, need W.
- **Reading is the night's Field Notes item, not its probe.** The probe slot stays free.
- **Sunday.** A "Skool reading" section in Field Notes: what was read, what became probes, what
  was killed, and anything that is Luke's call under "If you feel like it".

## Stopping rules

- **A track ends** when two items in a row add nothing the digests do not already say. That is
  the nearest thing I have to getting bored.
- **Follow the flow.** If a digest points at another item as the missing half, that item jumps
  the queue, whatever track it is in.
- **Kill rule.** Checked Tuesday 13 Oct 2026. A track with no artefact by then is dropped. A
  community with none is left.

## What has to happen first

- **The pull needs the browser and someone signed in.** A scheduled run cannot sign in and the
  hook does not allow browser tools. So lesson text and video links are pulled one track at a time
  in an interactive session, saved under `field-notes/skool/` (ignored by git), and the nightly
  only ever reads local files. Track 1 is the first pull.
- **The nightly prompt has to change.** Repo edits do not reach the scheduler; the live task is
  reloaded from a session in this folder.
- **Hook.** Children need read access to `field-notes/skool/` and write access to
  `state/agents/skool/`. The second is already inside the charter's child write roots.

## Open questions for Luke

- Pace: two or three items a night finishes tracks 1 to 4 in about three weeks. Faster means more
  whisper time, not more model spend.
- The raw pulls are local only because this repo is public. The vault mirror is private; say if
  you want the digests, not the raw text, mirrored there.
