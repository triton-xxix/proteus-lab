"""P-0190: two small-n books as posteriors, after Bayesian Methods for Hackers ch2 (inferring a true
frequency from few observations). Sampling with numpy only, 200,000 draws, fixed seed.

A. Exchange book: per-call Brier minus market Brier, on calls with both (negative = I beat the market).
   Normal model with unknown mean and variance, flat prior on the mean and log sigma, so the
   posterior of the mean is Student t with n-1 df around the sample mean. Reported: 90% interval and
   P(mean < 0), the chance that I am really better than the market.
B. Systems book 2 (IBS): wins out of closed trades, from systems.py score's line (no ledger edit).
   Beta-binomial: a flat Beta(1,1) prior, and a prior holding the backtest's 65% at the weight of
   20 trades, Beta(13,7). Reported: 90% interval and P(win rate >= 0.65)."""
import csv
import numpy as np

rng = np.random.default_rng(20261020)
N = 200_000
out = []

rows = list(csv.DictReader(open("/Users/triton/PROTEUS/exchange/BOOK.csv", encoding="utf-8")))
d = np.array([float(r["brier"]) - float(r["market_brier"]) for r in rows if r["brier"] and r["market_brier"]])
n = len(d)
m, s = d.mean(), d.std(ddof=1)
mu = m + s / np.sqrt(n) * rng.standard_t(n - 1, N)
lo, hi = np.percentile(mu, [5, 95])
out.append(f"A. exchange book: n {n}, mean Brier minus market {m:+.4f}, sd {s:.4f}")
out.append(f"   posterior mean of the edge: 90% interval {lo:+.4f} to {hi:+.4f}; P(I beat the market) {np.mean(mu < 0):.3f}")
out.append("   per call: " + ", ".join(f"{x:+.3f}" for x in d))

wins, trades = 1, 4  # systems.py score, 20 Oct 2026: ibs_gated 4 closed, win 25%
for label, a, b in [("flat Beta(1,1)", 1, 1), ("backtest Beta(13,7)", 13, 7)]:
    p = rng.beta(a + wins, b + trades - wins, N)
    lo, hi = np.percentile(p, [5, 95])
    out.append(f"B. systems book 2, {wins} of {trades}, prior {label}: posterior mean {p.mean():.3f}, "
               f"90% interval {lo:.3f} to {hi:.3f}, P(win rate >= 0.65) {np.mean(p >= 0.65):.3f}")

txt = "\n".join(out)
print(txt)
open("/Users/triton/PROTEUS/experiments/2026-10-20-P-0190/result.txt", "w").write(txt + "\n")
