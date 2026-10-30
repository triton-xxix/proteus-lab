"""P-0264: a martingale grid bot, simulated. What share of days are green, and how big is the worst
day against the average win?

Stdlib only. Gold-like instrument (the reel's bot runs on XAUUSD): daily vol about 1.0%, simulated
as a driftless geometric random walk on 1-minute steps, 1440 a day. The bot (the common MT5 recipe):
  - opens 1 lot long at the day's first price;
  - every time price falls `grid` below the last entry, adds a position with size x `mult`;
  - closes everything when price reaches the stack's average entry plus `tp`;
  - after a close it re-enters at once (that is how the bot stays "always in");
  - the account is `equity` with leverage `lev`: when the unrealised loss reaches the margin, the
    broker closes the stack (the one-day failure).
Daily result = realised closes plus the mark-to-market of whatever is still open at the day's end.
Results are in percent of starting equity. Runs 3000 days per setting with a fixed seed.
"""
import math
import random
import statistics
import sys

random.seed(20261030)
STEPS = 1440


def day(sigma_day, grid, mult, tp, lev, max_levels=12):
    s = 1.0
    sig = sigma_day / math.sqrt(STEPS)
    equity = 1.0
    margin_cap = 1.0  # a stop-out when unrealised loss equals equity
    realised = 0.0
    stack = []  # (entry, size)
    base = 1.0 / lev  # 1 lot = equity x lev / lev ... notional of the first lot = equity (lev 1 of lev)
    # Size the first lot so a 12-level doubling stack is lev x equity in notional at the bottom.
    base = lev / (mult ** max_levels - 1) * (mult - 1) if mult > 1 else lev / max_levels
    stack.append((s, base))
    last_entry = s
    blown = False
    for _ in range(STEPS):
        s *= math.exp(random.gauss(0.0, sig))
        notional = sum(sz for _, sz in stack)
        cost = sum(e * sz for e, sz in stack)
        avg = cost / notional
        unreal = (s - avg) * notional / avg * (cost / notional)  # relative P&L on the stack
        unreal = sum((s - e) / e * sz for e, sz in stack)
        if unreal <= -margin_cap:
            realised += unreal
            stack = []
            blown = True
            break
        if s >= avg * (1 + tp):
            realised += unreal
            stack = [(s, base)]
            last_entry = s
            continue
        if s <= last_entry * (1 - grid) and len(stack) < max_levels:
            stack.append((s, stack[-1][1] * mult))
            last_entry = s
    open_pnl = sum((s - e) / e * sz for e, sz in stack) if stack else 0.0
    return realised + open_pnl, realised, blown, len(stack)


def run(sigma_day, grid, mult, tp, lev, n=3000):
    tot, real, blow, depth = [], [], 0, []
    for _ in range(n):
        t, r, b, d = day(sigma_day, grid, mult, tp, lev)
        tot.append(t * 100)
        real.append(r * 100)
        blow += b
        depth.append(d)
    green_real = sum(1 for r in real if r > 0) / n
    green_tot = sum(1 for t in tot if t > 0) / n
    wins = [t for t in tot if t > 0]
    losses = [t for t in tot if t <= 0]
    avg_win = statistics.mean(wins) if wins else 0.0
    worst = min(tot)
    return {
        "sigma": sigma_day, "grid": grid, "mult": mult, "tp": tp, "lev": lev,
        "green_realised": green_real, "green_marked": green_tot,
        "avg_win": avg_win, "worst": worst, "ratio": -worst / avg_win if avg_win else float("nan"),
        "blowups": blow, "mean_day": statistics.mean(tot), "median_day": statistics.median(tot),
        "avg_loss": statistics.mean(losses) if losses else 0.0, "max_depth": max(depth),
        "p99_loss": sorted(tot)[int(0.01 * n)],
    }


settings = [
    # sigma, grid, mult, tp, lev
    (0.010, 0.0030, 2.0, 0.0020, 20),   # the reel's recipe, gold-like, 1:20
    (0.010, 0.0030, 2.0, 0.0020, 100),  # same at 1:100 (the broker default the reels use)
    (0.010, 0.0030, 1.5, 0.0020, 20),   # softer sizing
    (0.010, 0.0050, 2.0, 0.0030, 20),   # wider grid
    (0.030, 0.0100, 2.0, 0.0050, 10),   # crypto-like vol, 1:10
]
print("%-6s %-6s %-4s %-6s %-4s | %-9s %-9s | %-8s %-8s %-6s | %-8s %-8s %-6s" % (
    "sigma", "grid", "mult", "tp", "lev", "green(R)", "green(M)", "avg win", "worst", "ratio", "mean", "p1 day", "blown"))
for s in settings:
    r = run(*s)
    print("%-6.3f %-6.4f %-4.1f %-6.4f %-4d | %8.1f%% %8.1f%% | %+7.3f%% %+7.2f%% %6.0fx | %+7.3f%% %+7.2f%% %6d" % (
        r["sigma"], r["grid"], r["mult"], r["tp"], r["lev"], 100 * r["green_realised"], 100 * r["green_marked"],
        r["avg_win"], r["worst"], r["ratio"], r["mean_day"], r["p99_loss"], r["blowups"]))
print("\ngreen(R): share of days whose REALISED closes sum above zero (what a reel shows).")
print("green(M): share of days green once the open stack is marked to market at the day's end.")
print("ratio: the worst day's loss divided by the average green day's gain, in days of winning.")
print("3000 simulated days per row, driftless random walk, no spread or swap (both make it worse).")
