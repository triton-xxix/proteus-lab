"""Scores the pre-listing tracking week against RULES.md. Reads only track/. Prints the pass marks and
writes track/WEEK.json. Run the night after the poller stops (DUE D-011).
"""
import json
import os
import random
import statistics
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
TRACK = os.path.join(HERE, "track")
BOOK_N = 10
SIDE = 0.0025
SELL_KINDS = {"upbit_krw": "upbit_krw", "binance_spot": "binance_spot", "coinbase_currency": "coinbase", "coinbase_product": "coinbase"}


def jl(name):
    p = os.path.join(TRACK, name)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def main():
    polls = [p for p in jl("polls.jsonl") if "stopped" not in p]
    events = jl("events.jsonl")
    commits = json.load(open(os.path.join(TRACK, "commits.json"))) if os.path.exists(os.path.join(TRACK, "commits.json")) else {}
    days = sorted(d for d, ct in commits.items() if ct)
    lists = {d: json.load(open(os.path.join(TRACK, "lists", d + ".json"))) for d in days}
    final = os.path.join(TRACK, "final_prices.json")
    snaps = [(d, commits[d], lists[d]["prices"]) for d in days]
    if os.path.exists(final):
        f = json.load(open(final))
        snaps.append(("end", f["at_unix"], f["prices"]))
    out = {}

    # P1 feeds
    ok = sum(1 for p in polls if not p.get("errors"))
    out["P1_polls"] = {"polls": len(polls), "clean": ok, "share_clean": round(ok / len(polls), 3) if polls else None,
                       "pass": bool(polls) and ok / len(polls) >= 0.95 and os.path.exists(os.path.join(HERE, "DONE"))}
    # P2 detection lag on Upbit and Binance listing notices
    lags = [e["lag_s"] for e in events if e["kind"] in ("upbit_krw", "upbit_btc_usdt", "binance_spot", "binance_perp")]
    out["P2_detection"] = {"notices": len(lags), "median_lag_s": statistics.median(lags) if lags else None,
                           "pass": (statistics.median(lags) <= 90) if lags else None}
    # P3 lists committed
    late = [d for d in days[1:] if commits[d] - datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() > 1800]
    out["P3_lists"] = {"committed": len(days), "late": late, "pass": len(days) >= 8 and not late}
    # P4 the pop, every listing with a prior market priced at +3 min
    pops = [e for e in events if e.get("priced") and e["kind"] in ("upbit_krw", "binance_spot", "coinbase_currency", "coinbase_product", "bithumb_krw")]
    up = [e["ret_pess_3m"] for e in pops if e["kind"] == "upbit_krw"]
    out["P4_pop"] = {"priced": [(e["kind"], e["symbol"], e["ret_pess_3m"]) for e in pops],
                     "upbit_median_pess_3m": statistics.median(up) if up else None,
                     "pass": (statistics.median(up) > 0) if len(up) >= 2 else None}
    # recorded, not judged: hits on the list and the top-10 paper book
    hits = [e for e in events if e["kind"] in SELL_KINDS and e.get("rank")]
    out["hits_on_list"] = [(e["kind"], e["symbol"], e["rank"], e.get("ret_pess_3m"), e.get("ret_from_list_entry")) for e in hits]
    out["target_listings_in_week"] = len([e for e in events if e["kind"] in SELL_KINDS])
    book, uni, rnd = 1.0, 1.0, [1.0] * 200
    held, rheld = set(), [set() for _ in range(200)]
    rng = random.Random(17)
    for i in range(len(snaps) - 1):
        d, t0, p0 = snaps[i]
        _, t1, p1 = snaps[i + 1]
        lst = lists[d]
        top = [c["symbol"] for c in lst["candidates"][:BOOK_N]]
        pool = [c["symbol"] for c in lst["candidates"] + lst.get("next_50", [])]
        sold = {e["symbol"]: e for e in events if e["kind"] in SELL_KINDS and e.get("priced") and t0 < e["t_announced"] <= t1}

        def leg(syms, prev):
            if not syms:
                return 0.0, set()
            cost = SIDE * (len(set(syms) - prev) + len(prev - set(syms)))
            r = []
            for s in syms:
                if s in sold and p0.get(s):
                    r.append(sold[s]["exit_low_px"] / p0[s] - 1 - 0.005)
                elif p0.get(s) and p1.get(s):
                    r.append(p1[s] / p0[s] - 1)
                else:
                    r.append(0.0)
            return (sum(r) - cost) / len(syms), set(syms) - set(sold)

        x, held = leg(top, held)
        book *= 1 + x
        common = [s for s in p0 if s in p1 and p0[s] > 0]
        uni *= 1 + (statistics.mean(p1[s] / p0[s] - 1 for s in common) if common else 0)
        for k in range(200):
            pick = rng.sample(pool, min(len(top), len(pool))) if pool else []
            y, rheld[k] = leg(pick, rheld[k])
            rnd[k] *= 1 + y
    out["book_top10"] = {"return_pct": round(100 * (book - 1), 2), "universe_pct": round(100 * (uni - 1), 2),
                         "random_median_pct": round(100 * (statistics.median(rnd) - 1), 2),
                         "share_random_beaten": round(sum(r < book for r in rnd) / 200, 2)}
    out["extend_to_12_weeks"] = bool(out["P1_polls"]["pass"] and out["P3_lists"]["pass"] and out["P2_detection"]["pass"] is not False)
    json.dump(out, open(os.path.join(TRACK, "WEEK.json"), "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
