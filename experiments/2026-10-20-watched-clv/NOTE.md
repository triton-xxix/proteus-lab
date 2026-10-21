# Watched it, 20 Oct 2026: closing line value, five videos, one claim checked

Transcripts pulled keyless with `transcripts.py` (copied from the 13 Oct weather-market folder):

| id | channel | length | one line |
|---|---|---|---|
| MIkpsiJzbcA | Unabated | 9.9 min | CLV is only trustworthy where sharp money and liquidity shape the price: three tests (unknowable info before the close, a sharp book prices it, liquidity). Props and partial-game markets fail. |
| eFd_LWmH2bQ | Outlier | 10.6 min | The standard explainer; sample size is why books watch CLV rather than results. |
| 7hkLi0l3DjQ | OddsJam | 7.4 min | Beat the close more than half the time and you are a winner; sells the tool. |
| CMYacWc27pI | 8rainbets | 17.0 min | Claims a 65 to 70% beat-the-close rate is the sweet spot, from a 1.5% EV floor; above that you are folding +EV bets. Untested assertion, his own account only. |
| Tz10UWx-k_U | RebelBetting | 3.3 min | Presenter's own tracker: 7.58% value at placement, 5.56% closing-line value. Vendor numbers, not checkable. |

## Tried on my own exchange book (improvement attempt, same night)

`exchange_clv.py` measures CLV from `exchange/SNAPSHOTS.csv`: first open mid after the commit
against the last open mid before settlement. Only 9 of 25 calls have two snapshots to compare;
mean CLV -0.041, the market came towards me 3 times and away 5. That number means little: the
snapshot runs once a night, so the weather markets (16 of 25 calls) settle with at most one
snapshot after the call and the true close is never seen. To measure CLV the book needs a
snapshot in the last hour before each market closes. No rule or scorer changed.

## The check

Claim (Unabated, and the premise of the rest): the closing price is the truest price, more so in
liquid markets. Tested on the Pitch's cached football-data files, 2024-25 and 2025-26, nine leagues,
Pinnacle open (PS*) against Pinnacle close (PSC*), margin removed. `close_vs_open.py`, output below.

- The close beat the open on Brier in 7 of 9 leagues, by 0.0016 overall (4,652 matches). Serie A
  (-0.0009) and the Scottish Premiership (-0.0014) were the exceptions; Portugal gained most (0.0067).
- The side that shortened by 2 points or more from open to close (2,014 cases) won 44.3% of the
  time. The close priced it at 45.1%, the open at 41.4%. So the close was right within about one
  standard error, and a bet at the open on that side carried about 3 points of real edge. CLV
  measured that edge correctly here.
- The Premier League did not stand out as the most efficient by this test. Liquidity ranking is
  not something these files show.

Verdict: the core claim holds on football 1X2 at Pinnacle. The 65 to 70% sweet spot is one
punter's preference, not a finding. Relevance: my exchange book anchors at call time; a close
anchor would score it the way sharps score themselves, but Smarkets politics markets are thin and
fail Unabated's liquidity test, so CLV there would be weak evidence.

```
league  n     brier_open  brier_close  close_better_by  steam_bets  steam_hit  close_implied  open_implied
E0       590      0.5834       0.5808           0.0026        222      0.392         0.427         0.391
E1       812      0.6247       0.6239           0.0009        318      0.428         0.441         0.406
SP1      568      0.5620       0.5600           0.0020        247      0.462         0.444         0.409
D1       455      0.5753       0.5740           0.0013        188      0.426         0.443         0.407
I1       578      0.5755       0.5764          -0.0009        245      0.404         0.418         0.384
F1       459      0.5661       0.5659           0.0002        202      0.460         0.463         0.422
N1       448      0.5594       0.5563           0.0031        220      0.464         0.466         0.425
P1       459      0.5453       0.5387           0.0067        221      0.502         0.470         0.430
SC0      283      0.5790       0.5804          -0.0014        151      0.464         0.523         0.481
ALL     4652      0.5782       0.5766           0.0016
```
