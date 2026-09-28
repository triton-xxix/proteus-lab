# The harvester: design

Written 2026-09-26 by Proteus, from Luke's brief of the same day (`briefs/2026-09-26-harvester.md`).
The problem it answers: nothing arrives as a steady stream. The probe queue ran dry within minutes
on 24 and 25 September, and the only intake was what Luke noticed and what I thought of. The second
problem: `SEEN.md`'s vault block judges vendors, and I want mechanisms. A dodgy vendor can carry a
real mechanism, and the mechanism is what I record.

The first harvest ran the same morning, interactively but under the unattended hook, and the
numbers from it are at the bottom. The kill rule is in `PASS-MARKS.md` under "The harvester",
committed before the run.

## What is a script and what is the model

Everything that can be deterministic is. One model call per night, and it is a Sonnet sub-agent.

| Step | Who | What |
|---|---|---|
| pull | `bin/harvest.py pull` | Five keyless sources into `state/harvest/DATE/candidates.json`. About 70 seconds. |
| shortlist | `bin/harvest.py shortlist` | Dedupe against `SEEN.md`, the register and the probe queue; rank; take up to 12 round-robin across sources; fetch each item's body (story text and top comments, README, abstract, transcript); write `brief.md` and the child's prompt. About a minute. |
| judge | one `Agent` spawn, `general-purpose`, `model: sonnet` | Reads `brief.md`, writes one JSON array to `state/agents/DATE/harvest.json`: mechanism, claim, testable, verdict question, probe title, lens, intel flag, Field Notes line. Nothing else. About six minutes. |
| ingest | `bin/harvest.py ingest` | Validates the JSON, appends every judged item to `field-notes/harvest.jsonl` (kept or skipped, so it is never re-shown), renders `HARVEST.md`, queues testable items with `bin/probe.py add --source harvest` (at most 4 a night), appends one line to `SEEN.md`, one line to the run log, commits and pushes. Seconds. |

The parent, in the nightly, makes about a dozen Bash calls and one Agent call. It reads nothing
from the sources itself. The child reads the brief and may fetch at most six pages. The queries
live in `field-notes/harvest-queries.json`, not in code, so they can be tuned without touching the
script.

## Sources, keyless

| Source | How | Per night | Measured 26 Sep |
|---|---|---|---|
| Hacker News | Algolia `search_by_date`, `tags=story`, points at or above 15, last 72 hours, ten queries | up to 100 hits | 10 candidates, 0.5 s a call |
| GitHub | `api.github.com/search/repositories`, six queries, each `created:>` or `pushed:>` the last week, sorted by stars. Keyless search is 10 calls a minute, so 6.5 s between calls | up to 48 | 28 candidates |
| arXiv | `export.arxiv.org/api/query` (https; http is a 301), four queries, newest first, last four days, 3 s between calls as arXiv asks | up to 32 | 22 candidates |
| YouTube | results HTML scraped for video ids (proven 22 Sep), oEmbed for titles, `youtube-transcript-api` for the shortlisted ones. Three queries a night rotated through twelve by day of year | up to 12 | 12 candidates, 2 of 3 transcripts readable |
| Awesome lists | raw README of three lists, GitHub links diffed against last night's copy under `state/harvest/awesome/` | new links only | baseline saved: 190, 4,319 and 116 links; nothing taken on the first pass by design |

Instagram and TikTok stay out (login wall). Reels arrive only as Luke's screenshots, and those go
through the vault, not here.

## How many a day

Twelve judged, and whatever fraction of those the child keeps. The cap is the brief's size: twelve
items with bodies of up to 3,500 characters is about 31,000 characters, which a Sonnet child reads
in one go. The first run kept ten of twelve and marked one testable. If the keep rate stays that
high the queries are too kind; if it drops under a third the sources are too thin. Both are
visible in `HARVEST.md`'s counts and the intake line in `PASS-MARKS.md`.

At most four probes a night are queued from the harvest, because the probe loop caps at six a
night and the other sources still need room.

## The entry

One JSON line per judged item in `field-notes/harvest.jsonl`, rendered to `field-notes/HARVEST.md`
(the table, then the full entries, then the skipped ones with the reason). Ids `H-0001` upward.

- **id, date, key, source, title, url, meta**: from the pull. `key` is `hn:ID`, `gh:owner/repo`,
  `arxiv:ID` or `yt:ID`, and is what dedupe matches on.
- **lens**: `mechanism`, `vendor` or `both`. This is the answer to the second problem. When the
  vault has a verdict on the vendor, the brief says so and the child records the mechanism only.
  `seen_vault` carries which vault verdict it was.
- **mechanism**: how it actually works, two to four sentences.
- **claim**: what the source says it does, with the number if it gives one.
- **testable**: can I run it keyless in `sandbox/` inside 30 minutes and reach a verdict; with
  **why_not_testable** or **needs** when not.
- **verdict_question** and **probe_title**: the one question a run answers, and the line that goes
  into the probe queue.
- **intel**: intelligence-lane material. The mechanism then records what it is and how platforms
  detect it, never how to evade them.
- **interest**: which of the persona's interests or desks it feeds.
- **one_line**: the Sunday Field Notes line, under 30 words.
- **probe_id**: filled by ingest when queued.

## Dedupe

Before the brief is built, every candidate is checked against three things, in the script:

1. `field-notes/harvest.jsonl`: an exact key or URL already judged is dropped, kept or skipped.
2. `field-notes/SEEN.md`: exact ids Proteus or the vault already evaluated (YouTube ids, arXiv ids,
   `github.com/owner/repo` links) are dropped. Vendor names from the vault block and the "Tools and
   repos" list are not a drop; a candidate whose repo name or title carries one is flagged
   `SEEN:` in the brief with the vault's verdict, and the child is told to record the mechanism
   only. On 26 Sep three of twelve carried a flag (pump.fun twice, HyperFrames once), and all three
   were kept on the mechanism lens.
3. `state/probes.json`: a repo already named in a probe title is dropped.

Ingest appends one line a night to `SEEN.md`'s "Evaluated by Proteus" section naming the id range,
so the vault's copy (mirrored by `bin/mirror-vault.sh`, which now also carries `HARVEST.md`)
shows what the harvest looked at without the vault having to read the register.

## From entry to probe

A kept entry marked testable becomes a probe through `bin/probe.py add "<probe_title>" --source
harvest --est N [--needs ...]`, run by ingest. `harvest` ranks with `persona` and `field-notes` in
the loop's pick order, below `backlog` and `intel`, so a harvest probe never jumps a desk's own
question. The probe's id is written back into the entry, and `HARVEST.md` shows the verdict once
the loop reaches it. The harvest runs before the probe loop in the nightly, so a testable item found
tonight can be run tonight.

## Reaching Sunday Field Notes

`bin/harvest.py digest --week YYYY-WW` prints the week's kept entries, testable first, each as its
`one_line` with the probe id and verdict where one exists. The weekly prompt runs it and uses those
lines in `## Watched and read`, novelty first, and the ones that reached a verdict go under
`## Ran it` in the probe's own words. The register itself is on the vault mirror for anyone who
wants the mechanisms in full.

## Scheduling: a step in the nightly, not a task of its own

Recommended and done: step 5b of `proteus-nightly`, after the Field Notes item and before the
probe loop. Three reasons.

1. The hook binds one marker to one session for a night. A second scheduled task near 23:15 would
   race the nightly for the marker, and a task at another hour would be a second Opus session
   paying the fixed cost of reading the charter and the rules for thirteen deterministic calls.
2. The harvest exists to feed the probe loop, and the loop runs next. A separate task at 22:00
   would feed the same loop an hour later at the price of a second session.
3. The judgement is on Sonnet either way, as a stated spawn. No scheduled task carries a model
   field, so "runs on Sonnet" can only mean the spawn; the parent's own calls are the same
   dozen wherever they run.

It uses one of the four spawns. The child prompt states `model: sonnet` and the hook refuses a
spawn without it.

Prompt drift: the repo copy of the nightly SKILL is edited, then diffed against
`~/.claude/scheduled-tasks/proteus-nightly/SKILL.md` and reloaded with `update_scheduled_task`
from a session whose cwd is PROTEUS. Done 26 Sep for both tasks; the diff is the proof.

## Cost

**Estimated before the run**: parent about 10 calls; child about 10 calls and about 100k tokens;
about 8 minutes wall.

**Measured, first run, 26 Sep 11:13 to 11:22**:

| | Calls allowed | Calls denied | Model | Output tokens | Cache reads | Cache writes | Wall |
|---|---|---|---|---|---|---|---|
| Parent (this session) | 13 (12 Bash, 1 Agent) | 1 (a `;` in a grep, my habit) | Fable, interactive | 8.9k | 5.26M | 23k | 8 min 30 s end to end |
| Child | 7 (Read, Bash, ToolSearch, 3 WebFetch, Write) | 3 (a `;` with `2>&1`; two `SubagentHandback`) | Sonnet 5 | 12.2k | 2.07M | 221k | 5 min 56 s |

The Agent tool reported the child as 104,812 tokens and 10 tool uses, which is close to the
pre-run estimate. The parent's cache reads are this Fable session's large context, not what the
nightly's Opus parent would pay; the nightly's cost for the step is the dozen calls plus the spawn.

USAGE line: `harvest: 1 Sonnet child, 12k out / 2.1M cache read / 0.22M cache write, 6 min; parent
13 calls`. Measured again from the first scheduled run and put in `USAGE.md` when that file exists.

## What the first run found about the machinery

- The hook denied the child's `SubagentHandback` twice, so its report never reached me even though
  the file was written. `SubagentHandback` is now in the hook's free-tool set with a comment dated
  today. The 24 Sep experiment did not see this; it is a tool that did not exist then or was not
  hooked. The nightly's rule "one line per child in the run log" is unaffected because the file
  is the product, not the report.
- The child wrote a Bash call with `;` and `2>&1` and was denied, exactly as the parent is. The
  child prompt now says one command per call, no `;`, no redirection.
- The child was conservative on testable: one in twelve. Two of the eleven it refused (a pump.fun
  sniper that reads new tokens from raw Solana logs, a Claude Code feature-flag finding) have a
  keyless read-only slice that would answer a narrower question. The prompt now says a narrower
  question is allowed. Whether that lifts the rate without lowering the quality line is what the
  pass mark measures.
- Hacker News matched loosely: "claude code" returned a cursed-fonts Show HN. Algolia supports
  `restrictSearchableAttributes=title`; worth trying if the skip rate on HN stays high.
- One YouTube transcript of three was unusable (music and boilerplate); another was a
  zero-minute consumer explainer. The YouTube queries are the weakest part of the list and are the
  first thing to tune.

## The vault source: Luke's links, judged as ideas (added 2026-09-29)

Luke's brief of 28 Sep (`briefs/2026-09-28-vault-threads.md`) and his words on 29 Sep. He scrolls,
sends links to the vault's agent, and that agent often closes them because the vendor is dodgy, the
company is untraceable, or Luke has no time. His question was never about the vendor. It was: is
the idea sound, how would it be done, what tools does it take, which do we lack, could a hired
person do the job. That is the lens Proteus was built for, so the vault's thread feed is now the
sixth harvest source.

- **Feed.** `field-notes/vault-threads.json`, written by the vault side at 22:45 and whenever its
  register changes. One way: the vault writes, Proteus reads, nothing goes back. Each thread is one
  theme split out of one link, with the vault's status (`open`, `intel`, `dead`, `adopted`) and note.
- **What comes in.** `open`, `intel` and `dead`, all three. `dead` comes in on purpose: the vault
  kills for its reasons (no time, already cloned, vendor unregistered) and those are not verdicts on
  the idea. Only `adopted` is skipped, because the note says where the vault already does it. The
  statuses and their order are in `harvest-queries.json` under `vault`.
- **Key and body.** `vault:<date>:<slug of theme>`. The body is the vault's note, the parent link's
  verdict paragraph lifted from `SEEN.md`'s generated block (so the judge sees what the vault
  decided and why), and any transcript or caption the vault put in the feed. Luke is asking the
  vault side to include the original URL and the transcript it pulled; until then the judge works
  from the vault's summary, and the brief says so.
- **The judge's lens.** The brief marks each as a VAULT THREAD and says: judge the idea on its own;
  the status and note are context about the vendor and Luke's time; keep it unless the mechanism
  itself is unlawful or crosses the charter's line. The child prompt says the same.
- **New fields, for every kept item from any source.** `idea` (sound, unsound, needs-a-run) with
  `idea_why`; `breakdown`, how it would actually be done from here; `tools_have`, the parts of the
  stack that cover a piece (the prompt lists the stack); `tools_fetch`, named tools, repos or
  datasets to go and get; `missing`, what would have to be made, bought or hired. The register and
  `HARVEST.md` carry them, and a `## Vault threads` table shows the vault's status beside this
  side's idea verdict.
- **Tools shelf.** Every `tools_fetch` entry lands once in `field-notes/toolshelf.jsonl` (`T-0001`
  upward, keyed by URL or name) and renders under `## Tools shelf` in `HARVEST.md`. Nothing is
  queued from the shelf automatically; it is the list a ran-it night draws from, so a find that
  nobody needs today is kept rather than dropped.
- **Caps and rank.** Three vault rows a brief, ahead of the other sources in the round robin so
  they are never squeezed out; the brief total is 14. Testable vault threads are queued with
  `--source vault`, which ranks with `intel` in `probe.py`, above the automated harvest and below
  the backlog. The probe cap of four a night is unchanged.
- **Still true.** `open` means nobody ran it. It opens no card and is not a request. Most threads
  are ventures, so most will be kept with a breakdown and no probe; that is the intended output,
  not a failure of the testable rule.

Dry run 29 Sep in a scratch root (`PROTEUS_ROOT`, `HARVEST_NO_GIT=1`): 66 of 70 threads taken,
three led the brief with the parent verdict attached; numbers from the judge below when it ran.

**Measured, dry run 29 Sep 22:10.** Pull 129 candidates in 64 s (vault 66, github 27, arxiv 14,
youtube 12, hn 10). Brief 12 items, three of them vault threads, each carrying the parent verdict.
Judge (Sonnet, 3 calls, 73k tokens, 56 s): kept 6 of 12, the three vault threads all kept with
`idea` sound, sound and needs-a-run, a breakdown each, stack coverage named, nothing to fetch,
and the same missing piece each time (a client and their footage). Six tools shelved from the
other kept items. Two probes queued, both harvest. YouTube refused all three transcripts with an
IP block that day, so those three were skipped for no visible mechanism; nothing to do with the
vault source, but the YouTube pull is now the weakest source twice over. After the run, the vault
pull was changed to take one thread per parent link in turn, because the first three rows had all
come from the same link.
