# P-0185: score skip-if-graph_insiders-is-0 forward

**Question.** On the next 20 Grinder (G) and R01 shadow entries after 20 Oct, does the kept group
(graph_insiders > 0 at entry) beat the skipped group (= 0) by 20+ points mean 24h outcome?

**Method.** `forward.py` reuses P-0013's join (latest insider snapshot at or before entry, outcome from
`score_24h` else PATHS.csv `path_move_pct`, one row per token) and keeps only entries after
2026-10-20T23:59:59Z.

**Number.** 0 entries after the cut in either ledger. The last R01 entries are R-0027 to R-0029 at
2026-10-20T22:38:37Z; the G book's last trade is G-0092 on 16 Oct. Insider snapshots do keep landing
(grinder/insiders/ up to 2026-11-02.jsonl), so the filter's input exists; the trades do not.

**Called shot.** blocked at 0.60, "fewer than 20 entries after 20 Oct". Hit.

**Verdict.** blocked: needs 20 new G or R01 entries. Neither book has entered in 13 days, so the forward
test cannot start until the gates let a trade through.

**Not done.** No backfill from the insider snapshots of coins the gates skipped: that would test a
different population (unentered coins) and is a separate probe if wanted.
