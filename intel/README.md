# Intelligence lane

One write-up per subject, named `intel/<subject>.md`, published on the lab page and mirrored to
the vault folder. Scope and the line that does not move are in `CHARTER.md` under The intelligence
lane. This file is the template and the checklist.

## The rule before anything is run

- Isolated: a sandbox VM or a device that touches nothing of Luke's. Nothing near the employer.
- Never: buying access to a fraud service, operating one, pointing anything at a system Luke does
  not own, handling stolen data, or using Luke's identity, name, accounts or card to sign up.
- Account creation, card entry, CAPTCHAs and untrusted executables stay off limits whatever the
  charter says; they are Claude Code's own rules.
- Nothing in a write-up reads as a how-to for the abuse. Detection is the point.

## Template

```markdown
# <Subject>

Date: YYYY-MM-DD. Status: researched | taken apart | run in the sandbox.

## What it is
One paragraph, plain words.

## What it costs
Price, how it is sold, where. What I paid, if anything (SPEND.md line).

## How it works
The mechanism, at the level a defender needs. No step-by-step for the abuse.

## How it is detected
Signals, logs, rates, fingerprints, vendor controls. What works, what does not, and why.

## What I ran
Exact commands or setup, inside what isolation, with the artefact path.

## What I did not run, and why
The line, named.

## Sources
Links, with the date each was read.
```

## Register

| Date | Subject | Status | Write-up |
|---|---|---|---|
| 2026-10-03 | pump.fun sniper bots, and the fake ones | researched, own chain data | `intel/pumpfun-sniper-bots.md` |

## Feed

Added 3 Oct 2026: the lane sat empty for twelve days because nothing fed it. Now
`bin/intel.py queue` lists what the harvest flagged `intel: true` and the vault verdicts that carry
intel material, minus subjects already written up. The nightly writes one write-up a week, on
Saturday, from `bin/intel.py next`, and registers it here.
