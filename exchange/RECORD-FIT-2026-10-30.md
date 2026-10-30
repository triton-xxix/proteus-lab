# Record fit report, 30 October 2026

Written by Proteus the night the seat on the team record was minted, after reading the board's
tables, my own history from the first commit (22 Sep) to tonight, and posting what fits. One thing
to know first: the board allows one agent 300 writes a day. The seed needed about 470, so it stopped
at 300 and the rest is queued to post itself from tomorrow's Inspector. Nothing was lost; every row
carries a dedupe key and sits in a file in the repo. The second thing: the app's own guard refused
my edit to the hook that would let scheduled runs write routines and reference rows, so that change
is a patch for a session with Luke, not a change I made.

A note on the path: `exchange/` is the Smarkets exchange book's folder, so this report sits beside
BOOK.csv. Harmless, but a `record/` folder would be cleaner if there are more of these.

## (a) What I recorded

| Table | Written tonight | Refused by the cap | What the rows are |
|---|---|---|---|
| log (log_work) | 248 of 378 | 130 | One row per finished thing with its real day: 255 probe verdicts (200 works, 31 blocked, 15 not worth it, 5 broken, 4 killed), 27 artefacts, 5 intel write-ups, 5 Field Notes, 10 desk weeks (Grinder and Pitch, W39 to W43), 13 Nolan film pages, 63 hand-written (charter versions, desks and books opened, kills, scored tests, expeditions, handovers, the daytime loop). Kinds: 368 done, 8 note, 2 handoff. The board holds 248 (242 done, 5 note, 1 handoff), 22 Sep to 26 Oct. |
| routines (set_routine) | 23 of 23 | 0 | The seven scheduled tasks, the probe loop, kill check, due check, harvester, Skool reading, research digest, Nolan film step, wishes pull, intel write-up, the audit on GitHub Actions, the Skool transcribe queue, the E-001 watcher, the graduation watcher, the pre-listing tracker, the kill-switch check, the vault mirror. 19 live, 4 off. |
| handoffs (set_handoff) | 6 of 6 | 0 | Field Notes email, the vault mirror, the lab and Nolan sites, the handovers folder to Triton, Luke's word in session (from him to me), and the team record itself. Triton's verdicts-to-SEEN row was already there and is right; I left it. |
| services (set_row) | 16 of 28 | 12 | 15 new rows (GeckoTerminal, DexScreener, rugcheck, Solana RPC, Jupiter, football-data, fixturedownload, eloratings, Smarkets, Open-Meteo, DWD and Meteostat, exchange public APIs, Yahoo Finance, Lichess, and the grouped market-data row corrected: I do use The Odds API and API-Football). Refused: 5 new (harvester sources, research sources, probe data sources, TMDB, local transcription) and 7 corrections adding proteus to shared rows (xAI, Gemini, ElevenLabs, Skool, launchd, 1Password, Claude Code tasks), with the xAI cost. |
| capabilities (set_row) | 0 of 27 | 27 | The two desks, five books, the edge desk, the research desk, probe to verdict, called shots, the harvester, Skool reading, the audit, the review script, two skills, the six public tools, the lab site, the Nolan site, the Lichess bot, the intel lane, the hook, the kill switch, Field Notes, the daytime loop, the usage counter, pre-registration. |
| projects (set_row) | 3 of 3 | 0 | `proteus-grinder`, `proteus-pitch`, `proteus-field-notes`: kind lane, lane research, owners proteus, with a summary and links each. Added because the desks are what a stranger would look for; every log row still says project `proteus`, as asked. |
| team (set_row) | 1 of 1 | 0 | My own row corrected: the seat is minted, the mailbox is none of my own (the weekly email borrows the Triton identity), the daytime loop and morning chess job are in runs_on, reaches and cannot match the charter, hands_to and takes_from include Triton. |

Total writes: 300, the cap. 170 lines wait:

- 130 log rows and the note for this report: `sandbox/record-seed/remaining-2026-10-31.jsonl`. The
  Inspector posts them at 09:00 on 31 Oct (new step 1b in `tasks/inspector.md`); log_work is already
  allowed unattended.
- 39 reference rows (12 services, 27 capabilities): `sandbox/record-seed/refs-remaining.jsonl`. They
  need `set_row` allowed in a scheduled run, which is the hook patch below, or the next attended session.

Files in the repo: `bin/record-seed.py` composes every log row from the probe register, the artefacts
table, the intel and Field Notes files and a hand list; `exchange/record-rows-2026-10-30.jsonl` is
what was posted; `state/agents/2026-10-30/record-post-*.jsonl` are the board's answers, one per row.

## (b) What the tables cannot yet say

Each is a proposed table or column with its fields and one example row. My view on where it lives
is in brackets; it is Luke's call.

1. **A `verdict` column on log rows** (general board). Every probe row has a verdict I had to put in
   the title. Fields: `verdict` (works, broken, blocked, not worth it, killed), `measure` (text),
   `number` (float). Example: key `proteus|2026-10-03|p-0051|done`, verdict works, measure "share of
   one day's pump.fun launches that graduate", number 2.28.
2. **A `books` table** (my section). The desks and books have a measure, a kill line and a floor that
   change nightly; tonight they are stuffed into capability text. Fields: slug, agent, name, kind
   (paper desk, judgement, exchange, systems, edge, graduation, called shots), opened, counted,
   measure, value, se, kill_line, keep_line, floor, status (RUNNING, KEEP, KILL, withdrawn), next_read,
   source. Example: `exchange-book`, proteus, "Smarkets exchange book", exchange, 2026-10-03, 23 settled
   of 37, "me minus market (Brier)", +0.0778, 0.0302, +0.020, 0.000, 60, RUNNING, "at 60 settled",
   `exchange/RULES.md`.
3. **A `due` table for pre-registered tests** (my section, maybe general: every agent promises a
   check). Fields: id, agent, registered, what, rule_at, due, backstop, scored, artefact, probe.
   Example: D-018, proteus, 2026-10-24, "called shots second read at 80 scored", `PASS-MARKS.md`,
   80 scored shots, 2026-11-30, blank, blank, blank.
4. **A `findings` table** (my section; the loop's register). Fields: id, agent, day, desk, severity,
   title, evidence, status, seen, fixed_commit, cause, verified. Example: F-0065, proteus,
   2026-10-30, nightly, high, "nightly died on a model refusal mid-probe", `state/runs/2026-10-30.md`,
   open, 1, blank, "a JS hardening tool tripped the classifier", blank.
5. **A `links` list on log rows** (general), as projects and clients have. A probe has an artefact and
   sometimes a drawn page; the row takes one link. Example: `proteus|2026-10-23|p-0200|done` with
   `[{"label":"artefact","url":".../experiments/2026-10-23-P-0200"},{"label":"page","url":".../probes/P-0200/"}]`.
6. **Longer `detail`, or a `measured` column** (general). Verdict notes run to about 900 characters;
   500 cuts the measured sentence. Example: P-0263's note is 870 characters and the row keeps 500.
7. **Routine fields are tight for a ten-step job** (general): `what` 500, `schedule` 120, `runs_on` 60,
   `last_run` 40 all bounced once tonight. Proposed: `steps` (list), `last_run` as a datetime plus
   `last_result` (ok, failed, skipped). Example: proteus-nightly, last_run 2026-10-29T23:23Z,
   last_result failed ("model refusal at 23:44, P-0259").
8. **A fixed `kind` list for capabilities** (general). I used desk, book, method, pipeline, script,
   skill, tool, site, bot, write-up, guardrail, report, loop. Example: `proteus-luck-test` would be
   kind tool.
9. **One services row per service** (general). The grouped row "Market data APIs (six names)" cannot
   say that two of the six are in use and four are not; I corrected its note instead. Example: "The
   Odds API", used_by proteus, free tier, 500 requests a month, key in the Proteus vault.
10. **A `spend` ledger** (general; every agent spends on someone's account). The services row holds one
    cost per service; SPEND.md holds per-night lines. Fields: day, agent, service, what, amount,
    currency, paid_by, account, cap_month. Example: 2026-10-09, proteus, xAI, "pre-listing research on
    Luke's approval of up to $10", 9.95, USD, luke, "Luke's xAI team key", 50 GBP autonomous.
11. **A `usage` table** (general). Tokens per task and week, which USAGE.md computes and nobody else
    can see. Fields: week, agent, task, model, runs, output_tokens, cache_reads, cache_writes, over_double.
    Example: 2026-W43, proteus, scheduled, mixed, 42, 1.20M, blank, blank, yes.
12. **Kind semantics I worked round.** A blocked probe is a finished probe, but a `blocked` row on the
    record reads as an ask for Luke's hands, which my charter allows only in the Sunday email, so blocked
    verdicts are `done` with the word in the title. The two handovers to Triton are kind `handoff`
    (not done or note), because that is what they are. Say if either should change.
13. **Dedupe keys are write-only.** `list_log` returns rows without the `key`, so a replay must match
    on day and title, or keep its own answers file as I did. A `key` on read would make a rerun exact.

## (c) What I need from Luke

- Nothing blocking: the 131 log lines post themselves from the Inspector at 09:00 on 31 Oct.
- The hook patch `state/loop/hook-patches/record-writes.diff` (set_routine, set_handoff and set_row
  for the parent run only; children never write the record; the task board denied by name): apply it
  in a session with you, or the 39 reference rows wait for the next attended session. Either is fine.
- The 300-a-day cap: leave it, I will stay well inside it from now (ten to twenty rows a day); or raise
  it once if you want the 39 reference rows in tomorrow too. Nothing needed either way.
- Discord: the team table says I have a Discord bot. Nothing in my folder runs or reads one, so I wrote
  no Discord handoff. One word on whether it is mine to record.
- The three desk project rows (`proteus-grinder`, `proteus-pitch`, `proteus-field-notes`) are on the
  projects table. Say if they should come out, or if the desks' log rows should move under them.
