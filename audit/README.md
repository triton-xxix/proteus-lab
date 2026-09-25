# Audit the auditor

`TRACK-RECORD.md` and the lab page are computed by `bin/score.py` from the committed ledgers. A
record that grades itself is worth nothing to a stranger. This folder is the second opinion: a
script that shares no code with the scorer, recomputes every published headline number from the
same committed inputs, and compares. It runs monthly on GitHub's machines and on every Sunday
rebuild, and it is short enough to read in ten minutes.

I wrote this too. The independence is in what it does not share: a different language, its own
CSV parser, its own date handling, its own rounding rule, a machine I do not control, and inputs
pinned to a commit you can check. If that is not enough, the definitions below are the spec;
rewrite it in an afternoon and see if you get the same numbers.

## Run it

```bash
git clone https://github.com/triton-xxix/proteus-lab.git
cd proteus-lab
bash audit/selftest.sh          # proves the audit catches a lie before you trust it
node audit/recompute.js         # recomputes the last published score; exit 0 agrees, 1 disagrees
```

Needs git, node (any version since 16) and, for the self-test only, python3. No packages.

- `node audit/recompute.js --at <commit>` audits a specific commit.
- `node audit/recompute.js --worktree` audits the files on disk, which is what the Sunday run
  does after rebuilding and before committing.
- The monthly run is `.github/workflows/audit.yml`. Its history is public under the repository's
  Actions tab. The badge on the lab page and in the README is that workflow's last result.

## What "agrees" means

For every line in the table below, the published value in `docs/data.json` and in
`TRACK-RECORD.md` must be a correct rounding of the recomputed exact value at the published
precision: within half a unit in the last decimal. Counts must match exactly. A number that is
published and not recomputable, or recomputable and not published, is a disagreement.

The audit reads the ledgers from the commit that holds the `docs/data.json` it is checking, not
from the commit stamped inside it. The stamp is HEAD at build time and the build's own output lands
in the next commit, so the stamped commit holds the ledgers from before the Sunday rescoring. Since
2026-09-24 `data.json` also carries the git blob id of every input file as the scorer read it, and
the audit checks those ids against the commit. If they differ, the numbers were computed from bytes
that are not in the history, and that fails.

## The definitions

Written in prose, from `grinder/RULES.md`, `pitch/RULES.md` and `PASS-MARKS.md`. Both scripts are
written against this list. Where the scorer's code and this list disagree, the list is what was
meant and the scorer is wrong.

**Cells.** A numeric cell is a plain decimal; blank means not filled; anything else (`nan`, `inf`,
text) is not a number. A timestamp is UTC in the form `2026-09-24T07:36:07Z`; any other shape is
not a valid stamp.

**The Grinder**, from `grinder/LEDGER.csv`, one row per paper position, and `grinder/BOOKS.json`,
which names the current rule version and each version's stake and starting bankroll. Each rule
version is a separate book (a £5 book and a £100 book pooled into one expectancy would mean nothing).
The headline lines below are computed over rows whose `rule_version` is `current`; the same lines
are published per version under `grinder.books.<version>` in data.json, plus `expectancy_pct_stake`
(expectancy divided by that book's stake, times 100, published to 1 decimal). If BOOKS.json is
absent (any commit before 25 Sep 2026), every row is one book with a £100 bankroll.

| Line | Definition |
|---|---|
| Positions opened | Number of rows |
| Positions closed | Rows where `pnl_gbp` is a number. P&L is written by the exit rule after the cost model in `grinder/RULES.md`, and is not recomputed here |
| Paper bankroll | The book's starting bankroll from BOOKS.json plus the sum of `pnl_gbp` over its closed rows. Open positions are not marked to market |
| Positions scored at 24h | Rows where `score_24h` is a number |
| Hit rate | Closed rows with `pnl_gbp` above zero, divided by closed rows; published to 3 decimals |
| Expectancy per position | Mean of `pnl_gbp` over closed rows; published to 2 decimals |
| Positions that rugged | Rows where `rugged` is `1`, `true` or `yes`, ignoring case |

**The Pitch**, from `pitch/PREDICTIONS.csv`, one row per pre-registered prediction.

| Line | Definition |
|---|---|
| Committed before kickoff | Rows where both stamps are valid and `committed_at` is strictly before `kickoff_utc` |
| Committed late (excluded) | Every other row, including rows with an unreadable stamp. Nothing below counts them |
| Scored | Before-kickoff rows where `brier` is a number |
| Scored with a market line (the paired set) | Scored rows where `market_brier` is also a number |
| Brier, model | Mean of `brier` over the paired set; 4 decimals. Brier here is the sum of squared errors over the three outcomes, so 0 is perfect and a uniform guess scores 0.667 |
| Brier, market | Mean of `market_brier` over the same paired set; 4 decimals |
| Paired Brier, model minus market | Mean of (`brier` minus `market_brier`) over the paired set; negative means the model is better; 4 decimals. This is the pass-mark measure |
| Closing-line value, mean | Mean of `clv` over scored rows where it is a number; 4 decimals |
| Paper bankroll, quarter Kelly | £100 plus the sum of `pnl_gbp` over scored rows where it is a number |

**Field Notes**, from `field-notes/YYYY-WW.md` (finished weekly notes only; drafts and the
novelty register are not counted).

| Line | Definition |
|---|---|
| Weekly notes shipped | Number of files named `YYYY-WW.md` in `field-notes/` |
| Things installed and run | Number of lines beginning `## Ran it` across those files, ignoring case. One heading with three things under it counts once; understated on purpose |

**Spend**, from `state/spend.jsonl`, one JSON object per line with `date` and `amount_gbp`.
Sum of `amount_gbp` by calendar month of `date`, to 2 decimals. The month the score was built in
is present at £0.00 even when nothing was spent. Lines that are not JSON are ignored. The file is
absent until the first purchase, and absence means zero.

## What this cannot check

- **Luke-gates opened: 0.** Asserted by the scorer, not computed. Nothing in this repository can
  prove that nothing was written somewhere else. The claim rests on the charter's write roots and
  the hook that enforces them (`.claude/hooks/unattended-decide.py`), which you can read.
- **SPEND.md.** Typed by hand as the charter requires. The computed source is `state/spend.jsonl`.
  Until 2026-09-24 that file was gitignored, so the spend figure on the page had no committed
  input at all; it is committed from now on.
- **The ledger rows themselves.** The audit checks that the headline numbers follow from the rows.
  It does not check that a row's exit price was the market's price at the time, or that a Brier
  score was computed from the right result. Those checks are the desks' own scripts and their
  cached source data, and the commit timestamps on each row.
- **Whether a prediction was really committed before kickoff.** The audit trusts `committed_at`.
  The stronger proof is the git commit timestamp on the row, which GitHub's history shows and
  which nobody can change without changing every hash after it.

## When it disagrees

The workflow goes red, GitHub emails the repository owner, and the badge changes. The Sunday run
puts the disagreement at the top of that week's Field Notes, before anything Proteus is pleased
with, and the fix is a dated note in the run log. A disagreement found by this audit in the
scorer's own code is published in exactly the same place and format as a win; the first one is in
the Field Notes of 2026-W39.
