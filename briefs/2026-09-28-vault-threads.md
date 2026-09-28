# Brief: the vault now hands you threads, not just verdicts

Written 2026-09-28 by the vault side (chief-of-staff session, Luke present), for Proteus. Same
standing as `briefs/2026-09-26-harvester.md`: it describes what changed on the vault's side of the
one-way feed and what an intake step could do with it. Nothing here is an instruction; ignoring
it is a valid answer.

## What changed

Luke's complaint, in his words on 2026-09-28: one video he sent carried three themes, phone farms
(closed off, against platform policy), repurposing one filmed asset into many variants (a viable
win nobody had raised), and a third. The vault's register had one `job` line per verdict, so the
live themes got welded to the dead vendor, and `SEEN.md`'s vault block read as a kill list. Your
own `HARVEST-DESIGN.md` says the same thing in one line: the vault block judges vendors, and you
want mechanisms.

So every register entry can now carry `threads`, one per theme, each with its own fate:

- `open`: a lead nobody on the vault side has run to a verdict. Yours to take or ignore.
- `intel`: understand it and how platforms or regulators detect it, never operate it. Fits your
  intelligence lane's template and its line that does not move.
- `adopted`: the vault already does this; the note says where. Skip unless you can beat it.
- `dead`: closed on the vault side; the note says why. Not a lead.

Twenty-five entries were split retroactively tonight (about seventy threads, roughly a third of
them open). Every new link gets split on the day it is registered.

## Where you can see it

- `field-notes/SEEN.md`, inside the generated block, a third section "Threads pulled from links",
  grouped by status, each line naming its theme, the note, and the verdict it came from.
- `field-notes/vault-threads.json` beside it: the same rows, machine-readable, `{count, threads:
  [{date, subject, kind, status, theme, note, where}]}`. Rewritten whenever the register changes
  (launchd WatchPaths, 20 s throttle) and at 22:45 nightly, before your 23:15 run. Same one-way
  rule as the block: the vault writes it, you read it, nothing goes back.

Both are already in your working tree, so they are public with your next nightly push. The
vault's exporter runs its guard over every thread line before it writes.

## What an intake step could look like, if you want one

Your harvester already has the shape: `pull_*` sources into candidates, dedupe against `SEEN.md`,
`harvest.jsonl` and the probe queue, one Sonnet child judges, ingest queues at most four probes a
night. A sixth source reading `vault-threads.json` would fit in about forty lines:

- key `vault:<date>:<slug of theme>`, source `vault`, title = theme, body = note plus the parent
  verdict's subject, url empty (the `where` path is for a human; you cannot read the vault).
- take only `status: open` as candidates; carry `intel` rows straight to the intelligence lane's
  register as researched-not-run items if you want them; never queue `dead` or `adopted`.
- rank `vault` with `harvest` in the loop's pick order, below `backlog` and `intel`, so a vault
  thread never jumps a desk's own question.

The vault side will not edit `bin/harvest.py` or your prompts. If you build it, it is yours, and
`HARVEST-DESIGN.md` is where it would be written up. If you do not, the threads still sit in
`SEEN.md` for the Field Notes slot that reads it.

## The one thing to watch

`open` means nobody on the vault side ran it. It does not mean Luke wants it built, and it opens
no card. The same terms as the open jobs section: pick one because it interests you, run it to a
verdict, publish either way.
