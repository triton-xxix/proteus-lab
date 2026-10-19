"""P-0179: Grinder v0.2 cost model against live Jupiter quotes.

For 10 pools from tonight's Grinder snapshot (liquidity $20k and up, spread across the range), quote a
$130 SOL buy on Jupiter's keyless lite API, then quote selling the tokens received straight back.
Quoted round-trip loss = 1 - SOL back / SOL in. Compare with the v0.2 model in grinder/RULES.md:
1% pool fee per side, $0.05 network fee per side, constant-product impact with Q = half liquidity,
no exit slippage (that is an execution allowance, not part of a quote).

Both sell quotes see the pool as it is now, not as the buy left it; the model's sell uses the same Q,
so the two are compared like for like. Nothing is signed or sent: quotes only.

    python3 costcheck.py     # writes result.json beside this file
"""
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SNAP = Path("/Users/triton/PROTEUS/grinder/SNAPSHOTS.csv")
SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
STAKE_USD = 130.0
N = 10


def quote(inp, out, amount):
    q = urllib.parse.urlencode({"inputMint": inp, "outputMint": out, "amount": int(amount), "slippageBps": 50})
    req = urllib.request.Request("https://lite-api.jup.ag/swap/v1/quote?" + q, headers={"User-Agent": "proteus-probe"})
    # first run (19 Oct 04:10) got 429 on every token quote at 1.2 s spacing: back off and retry
    for wait in (0, 6, 15, 30):
        time.sleep(wait)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            time.sleep(3)
            return d
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            QUOTA["429"] += 1
    raise RuntimeError("429 after 4 tries")


QUOTA = {"429": 0}


def model_loss(liq):
    q = liq / 2.0
    x = STAKE_USD
    after_fee = x * 0.99 - 0.05
    value_mid = after_fee / (1 + after_fee / q)       # tokens bought, valued at mid
    back = value_mid / (1 + value_mid / q) * 0.99 - 0.05
    return 1 - back / x


def main():
    rows = [r for r in csv.DictReader(SNAP.open()) if r["ts"].startswith("2026-10-19") and r["liq_usd"]]
    seen, pool = set(), []
    for r in rows:
        if r["mint"] in seen:
            continue
        seen.add(r["mint"])
        try:
            liq = float(r["liq_usd"])
        except ValueError:
            continue
        if liq >= 20000:
            pool.append((liq, r))
    pool.sort(key=lambda t: t[0])
    step = max(1, len(pool) // N)
    picks = pool[::step][:N]

    usdc = quote(SOL, USDC, 1_000_000_000)
    sol_usd = int(usdc["outAmount"]) / 1e6
    lamports = STAKE_USD / sol_usd * 1e9

    out = {"sol_usd": sol_usd, "stake_usd": STAKE_USD, "candidates": len(pool), "rows": []}
    for liq, r in picks:
        row = {"symbol": r["symbol"], "mint": r["mint"], "dex": r["dex"], "liq_usd": liq,
               "model_loss_pct": round(100 * model_loss(liq), 2)}
        try:
            buy = quote(SOL, r["mint"], lamports)
            sell = quote(r["mint"], SOL, int(buy["outAmount"]))
            back = int(sell["outAmount"])
            row.update({"quoted_loss_pct": round(100 * (1 - back / lamports), 2),
                        "buy_impact_pct": round(100 * float(buy.get("priceImpactPct") or 0), 3),
                        "sell_impact_pct": round(100 * float(sell.get("priceImpactPct") or 0), 3),
                        "buy_route": [p["swapInfo"].get("label") for p in buy.get("routePlan", [])],
                        "sell_route": [p["swapInfo"].get("label") for p in sell.get("routePlan", [])]})
            row["model_minus_quoted"] = round(row["model_loss_pct"] - row["quoted_loss_pct"], 2)
        except Exception as e:
            row["error"] = "%s: %s" % (type(e).__name__, e)
        out["rows"].append(row)
        print(json.dumps(row))
    ok = [r for r in out["rows"] if "quoted_loss_pct" in r]
    if ok:
        diffs = sorted(r["model_minus_quoted"] for r in ok)
        out["summary"] = {"quoted": len(ok), "within_2_points": sum(abs(d) <= 2 for d in diffs),
                          "median_model_minus_quoted": diffs[len(diffs) // 2],
                          "model_more_conservative": sum(d > 0 for d in diffs)}
    out["retries_after_429"] = QUOTA["429"]
    (HERE / "result.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out.get("summary"), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
