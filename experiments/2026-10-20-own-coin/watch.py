#!/usr/bin/env python3
"""Our own coin: read one pump.fun mint's first hour from the chain, keyless, and score the called shots.

Reuses P-0042's observer (same RPC pacing, same buy and sell reading) on a single mint instead of 50
heard on the websocket. Finds the creation transaction as the mint's oldest signature, waits until the
token is an hour old, reads up to 300 transactions, writes result.json and RESULT.md.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-20-own-coin/watch.py MINT [now]

`now` skips the wait and writes dryrun-result.json and dryrun-RESULT.md (for a dry run on any old mint).
"""
import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "2026-09-30-P-0042", "observe.py")
spec = importlib.util.spec_from_file_location("observe", SRC)
obs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(obs)
obs.MAX_TX = 300
HOUR = 3600
OUT = "dryrun-" if "now" in sys.argv else ""

SHOTS = [  # id, p, test on the analyse() row; copied from PLAN.md, committed 2026-10-19
    ("S1", 0.55, lambda r: r["first_block_buyers"] >= 1),
    ("S2", 0.40, lambda r: r["buyers_first_60s"] >= 3),
    ("S3", 0.60, lambda r: r["first_sell_s"] is not None and r["first_sell_s"] <= 60),
    ("S4", 0.15, lambda r: r["traded_after_10m"]),
    ("S5", 0.60, lambda r: r["last_trade_s"] <= 300),
    ("S6", 0.15, lambda r: r["buyers_total"] >= 10),
    ("S7", 0.01, lambda r: r.get("graduated", False)),
]


def oldest_sig(mint):
    sigs, before = [], None
    for _ in range(20):
        opt = {"limit": 1000}
        if before:
            opt["before"] = before
        page = obs.rpc("getSignaturesForAddress", [mint, opt]) or []
        sigs += page
        if len(page) < 1000:
            break
        before = page[-1]["signature"]
    ok = [s for s in sigs if not s.get("err")]
    return min(ok, key=lambda s: (s["slot"], s.get("blockTime") or 0)) if ok else None


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: watch.py MINT [now]")
    mint = sys.argv[1]
    first = oldest_sig(mint)
    if not first:
        sys.exit("no transactions found for %s" % mint)
    born = first.get("blockTime") or time.time()
    wait = born + HOUR - time.time()
    if wait > 0 and "now" not in sys.argv:
        print("created %s, reading at +1h, %.0f s from now" % (time.strftime("%H:%M:%SZ", time.gmtime(born)), wait), flush=True)
        time.sleep(wait)
    r = obs.analyse({"sig": first["signature"]})
    r["sig"], r["read_at"] = first["signature"], time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if r.get("status") != "ok":
        json.dump(r, open(HERE + "/" + OUT + "result.json", "w"), indent=1)
        sys.exit("analyse failed: %s" % r.get("status"))
    scored = []
    for sid, p, test in SHOTS:
        hit = bool(test(r))
        scored.append({"shot": sid, "p": p, "happened": hit, "brier": round((p - (1 if hit else 0)) ** 2, 4)})
    r["shots"] = scored
    json.dump(r, open(HERE + "/" + OUT + "result.json", "w"), indent=1)
    brier = sum(s["brier"] for s in scored) / len(scored)
    L = ["# Our own coin: the first hour", "",
         "Mint `%s`, creation tx `%s`, read %s from the public RPC (%d transactions)." % (mint, first["signature"], r["read_at"], r["txs_read"]), "",
         "| Measure | Ours | P-0042 median or share |", "|---|---|---|",
         "| Creator buy (tokens) | %s | 83%% bought |" % r["creator_buy_tokens"],
         "| Outside buyers in the creation slot | %s | 1.0, 70%% had any |" % r["first_block_buyers"],
         "| Buyers in the first 60 s | %s | 3.0 |" % r["buyers_first_60s"],
         "| Buyers in the first hour | %s | 4.0 (first 40 tx) |" % r["buyers_total"],
         "| Seconds to the first sell | %s | 2.0 |" % r["first_sell_s"],
         "| Still trading after 10 min | %s | 27%% |" % r["traded_after_10m"],
         "| Seconds to the last trade seen | %s | 39.5 |" % r["last_trade_s"], "",
         "| Shot | p | Happened | Brier |", "|---|---|---|---|"]
    L += ["| %s | %.2f | %s | %.4f |" % (s["shot"], s["p"], "yes" if s["happened"] else "no", s["brier"]) for s in scored]
    L += ["", "Mean Brier %.4f (always 0.5 scores 0.250). S7, graduation, is not read from the chain here: "
          "check pump.fun by hand and correct the row if it graduated." % brier]
    open(HERE + "/" + OUT + "RESULT.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
