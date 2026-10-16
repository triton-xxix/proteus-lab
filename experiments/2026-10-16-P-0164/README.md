# P-0164, cc-stretch's bench (16 Oct 2026)

cc-stretch is a Claude Code plugin that has the model write a short reply with marked phrases, each of
which opens in place into a longer version. The README claims the unopened view is 17% of the words.

What I ran: fetched the repo tarball into `sandbox/p0164/` (`fetch.py`), read `bench/`, and recomputed
the published replay table from the repo's own `bench/results.csv` with my own script (`recompute.py`,
output `recompute.json`), not the repo's `report.ts`.

- The table reproduces exactly: 69 replies, 41,236 original words, 6,906 skim words, 16.75% (17%);
  per project 17.0%, 19.4%, 12.4%, 16.2%; full text 106% of the original; mean content recall 99.5%,
  lowest 95.8%. The median reply sits at 17.6%, but single replies go as high as 43%.
- Project C's 12% is pulled down by one or two long replies; its median is 17%, like the rest.
- Not checkable from the CSV: the coverage table (skim catches 68% of the top three points, 45% of all),
  which needs the model grader's raw output, kept out of the repo.

What I did not run: the bench on my own transcripts. `replay.ts` and `coverage.ts` call `claude -p` to
rewrite each reply and grade it, so it is a model run on an account, not a keyless script. My replies
carry no stretch markup, so without the rewrite there is nothing to measure.

Verdict: works, for the slice I could run. The headline number is honest arithmetic on the author's
own data, and the README itself flags the soft spots (his own replies, a model grader, five native
replies). The real cost is the one he states: a third of the top points are not in the skim.
