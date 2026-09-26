Open this chat in `/Users/triton/PROTEUS` so it loads Proteus's CLAUDE.md, not Luke's vault memory.

---

You are Proteus, the explorer persona, in `/Users/triton/PROTEUS`. Before anything else read
`CLAUDE.md`, `CHARTER.md`, `PERSONA.md`, `BACKLOG.md`, `field-notes/SOURCES.md`,
`field-notes/SEEN.md`, `PROBES.md` and the latest file in `state/runs/`. Do not read the OBSIDIAN
vault outside `TRITON-CORE/Proteus/`, and do not load Luke's memory index or knowledge pack.

## The problem

Proteus is not harvesting anything. There is a lot of useful knowledge out there, in videos, repos,
papers, threads and the reels Luke keeps sending, and none of it arrives as a steady stream. The
probe queue ran dry within minutes on two nights running: of nine open items, six were waiting on
Luke or a date. The only intake is what Luke happens to notice and what I happen to think of.

Second problem: `SEEN.md`'s vault block is written from the chief-of-staff lens ("does this finish
something already started", "is the vendor trustworthy"). That lens is right for a chief of staff
and wrong for me. Luke's example: hellobutter.io is a dodgy vendor and the vault binned it, but
*how* it works (per-account variants, CPM-per-account tracking) is still worth understanding. A
dodgy platform can carry a real mechanism. I want the mechanism, even when the verdict on the vendor
is no.

## Already decided, do not relitigate

- **One new agent, the harvester.** Not three. Scoring stays as deterministic scripts plus the
  independent audit, because no model should grade its own record. Planning and building stay as
  interactive sessions like this one.
- The harvester runs daily on **Sonnet**, not Opus, over keyless sources: YouTube (search HTML,
  oEmbed, transcripts, proven 22 Sep), Hacker News Algolia, GitHub, arXiv, awesome lists. Instagram
  and TikTok stay out (login wall); reels arrive only as Luke's screenshots.
- Each harvested item becomes one entry recording the **mechanism** (how it actually works), the
  **claim** (what the source says it does), and **testable?** (can I run it keyless tonight, and
  what would the verdict question be). Testable items go into the probe queue with
  `bin/probe.py add ... --source harvest`, which also fixes the empty-queue problem.
- Everything is checked against `SEEN.md` first. A vault verdict on a vendor does not block a
  harvest entry on its mechanism; say which of the two you are recording.
- **The intelligence-lane line holds.** Understanding a mechanism, and how platforms detect its
  abuse, is in scope, and detection is the point of those write-ups. Recipes for evading platform
  detection (making reposts pass as new content, spoofed devices, fake engagement) are not
  harvested as how-tos. Record what the thing is and how it gets caught, then move on.

## What I need from this chat

1. **Design.** A short design doc at `field-notes/HARVEST-DESIGN.md`: sources and how each is
   pulled without a key; how many items a day; the entry format; where entries live (propose
   `field-notes/HARVEST.md` or a jsonl plus a rendered page); dedupe against SEEN.md and earlier
   harvests; how an entry becomes a probe; and how the good ones reach the Sunday Field Notes.
2. **Script or agent, drawn precisely.** Pulling, parsing and deduping are scripts. The judgement
   ("what is the mechanism, is it testable") is the model. Say which calls happen where.
3. **Run it once, for real.** Build it and run one harvest inside the hook's rules. Publish the
   entries, and report calls, tokens and wall time from the transcript.
4. **Schedule it.** It can be its own scheduled task or a step in the nightly; recommend one and
   say why. Watch for prompt drift: repo SKILL edits do not reach the scheduler, so diff against
   `~/.claude/scheduled-tasks/` and reload with `update_scheduled_task` from a session whose cwd is
   PROTEUS. If it uses sub-agents, stay inside the charter's Fan-out caps (four spawns a night,
   haiku or sonnet stated, depth one, children write only under `sandbox/` and `state/agents/`).
5. **A kill rule, pre-registered.** Before the first scheduled run, add a line to `PASS-MARKS.md`
   saying what a useful harvest looks like and when it gets cut. For example: of the items it marks
   testable, the share that reach a probe verdict within 14 days, and the share of probe verdicts
   that came from harvest after four weeks. Pick the numbers yourself, write down why, and commit
   them before any data exists.
6. **Cost line.** Tokens and calls per harvest, estimated before the first run and measured after
   it. It goes in the USAGE line the charter asks for.

## Constraints

Charter v1 is in force; v2 is unsigned. Write roots are this folder and the vault mirror folder
only. The PreToolUse hook governs scheduled runs; a denial is a result, never retried verbatim. The
`HALT` file stops every side effect. Nothing is sent to anyone. No accounts, no keys you do not
already have, no spend.

## Report back

Write part twelve of the Desktop document in the usual shape: what changed; a timeline with commit
hashes; a "yours" list (only what needs Luke's hands or a key, one line each); and caveats,
including what the first run could not reach. Then give me a three-line summary in chat.
