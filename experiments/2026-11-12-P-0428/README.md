# P-0428: the single-degree cap fitted in sample, and the EPS band as a signal

12 Nov 2026, nightly probe loop, refill row 160, the deepen P-0422 named. `cap.py` reads
`exchange/BOOK.csv` and `exchange/icon_eps_band.jsonl` (read only). Rows: 38 settled Munich calls on a
single degree (32 of them anchored). Everything here is in sample: it describes rows already read.

**Called shot (commit 9347d121, made after seeing P-0422's 7 winners in 32, so scored as a coin).**
Best flat p within 0.05 of the 0.25 cap, and the EPS band not clearly narrower on winning nights. Both hit.

**The cap.** My degree won 8 of 38, a hit rate of 0.211. The flat p that minimises Brier is therefore
0.21, and it scores 0.1662 against my actual 0.1745. At 0.25 flat it is 0.1678; at 0.40 it is 0.2021.

| On the 32 anchored rows | Brier |
|---|---|
| Market | 0.1115 |
| Flat p at the hit rate | 0.1709 |
| Me | 0.1769 |

So I was wrong in P-0422 an hour ago to say the cap is what costs me. No flat number gets anywhere near
the market. The cap is about right on average; what the market has and I do not is knowing which nights
the favourite degree is a 0.5 and which nights it is a 0.05.

**The EPS band.** 17 of the rows fall on days with a captured ICON-EPS band.

- Width does not help. The band was wider on the nights I won (1.64 C against 1.26 C); the narrow half
  of nights hit 1 of 8, the wide half 3 of 9.
- Position might. When the degree I called sat inside the band (p10 less 0.5 to p90 plus 0.5), it won
  4 of 7. When it sat outside, it won 0 of 10.

**Caveats.** 17 rows, four winners, in sample, and found by looking. Ten of the outside-the-band calls
come from the weeks the nightly added +1 C for a station the market does not read (dropped 9 Nov), so
"outside the band" may just be another name for that mistake. The band is captured after the call each
night, so a rule built on it needs the call order changed, and any such rule is a pre-registration with
a DUE row, made in a daytime slot. Nothing in the book or the prompt was changed tonight.

**Next.** Deepen: from 11 Nov the calls carry no +1 C; after 15 settled rows under the METAR rule, count
again how often the called degree sits inside the EPS band and how those rows did.
