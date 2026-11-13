"""P-0437: is a flat pre-entry tape a rug tell? Six hourly volumes before each Grinder entry.

Losers: ledger rows that exited stop_loss or rug, or carry rugged=1. Winners: take_profit rows.
The most recent N of each (older pools are less likely to be served). For each, the pool the scan
saw (grinder/SNAPSHOTS.csv), then one keyless GeckoTerminal call for the hourly candles ending at the
entry hour. Window: the six whole hours before the entry hour; an hour with no candle counts as zero
volume. One call a trade, 4 s apart, one 20 s wait on a 429 and then skip. Stops at the wall-clock cap.
Read only: nothing in grinder/ is written.
"""
import csv, json, statistics, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
G = Path("/Users/triton/PROTEUS/grinder")
GT = "https://api.geckoterminal.com/api/v2/networks/solana/pools/"
UA = {"User-Agent": "proteus-lab/0.2", "Accept": "application/json"}
N, CAP_S, GAP_S = 18, 300, 4.0
FPES = [21657.0, 19585.0, 19668.0, 19596.0, 18908.0, 19463.0]   # P-0436, 11 Oct 17:00 to 22:00Z


def ts(s):
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())


def stats(vols):
    m = statistics.mean(vols)
    nz = [v for v in vols if v > 0]
    return {"vols": [round(v) for v in vols], "hours_with_trades": len(nz), "mean_usd": round(m),
            "cv": round(statistics.pstdev(vols) / m, 3) if m > 0 else None,
            "max_over_min": round(max(nz) / min(nz), 2) if len(nz) >= 2 else None}


def hourly(pool, end_hour):
    url = GT + pool + "/ohlcv/hour?aggregate=1&limit=12&currency=usd&before_timestamp=%d" % end_hour
    for attempt in (1, 2):
        try:
            j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
            return j["data"]["attributes"]["ohlcv_list"], None
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt == 1:
                time.sleep(20)
                continue
            return None, "HTTP %d" % e.code
        except Exception as e:  # noqa: BLE001
            return None, type(e).__name__
    return None, "429 twice"


def main():
    snaps = {}
    for s in csv.DictReader(open(G / "SNAPSHOTS.csv")):
        snaps.setdefault(s["mint"], []).append((s["ts"], s["pair"]))
    led = list(csv.DictReader(open(G / "LEDGER.csv")))
    losers = [r for r in led if r["exit_reason"] in ("stop_loss", "rug") or r.get("rugged") == "1"]
    winners = [r for r in led if r["exit_reason"] == "take_profit" and r.get("rugged") != "1"]
    picks = []
    for a, b in zip(reversed(losers[-N:]), reversed(winners[-N:])):   # interleave so a cut-off run stays balanced
        picks.append(("loser", a)); picks.append(("winner", b))
    t_start, rows = time.time(), []
    for kind, r in picks:
        if time.time() - t_start > CAP_S:
            print("wall-clock cap reached at", len(rows), "rows")
            break
        seen = [p for t, p in sorted(snaps.get(r["mint"], [])) if t <= r["entered_at"]]
        row = {"id": r["id"], "kind": kind, "token": r["token"], "exit_reason": r["exit_reason"], "rugged": r.get("rugged"),
               "pnl_gbp": r["pnl_gbp"], "entered_at": r["entered_at"], "entry_liq_usd": r["entry_liq_usd"]}
        if not seen:
            row["status"] = "no pool in snapshots"
            rows.append(row); continue
        end_hour = ts(r["entered_at"]) // 3600 * 3600
        data, err = hourly(seen[-1], end_hour)
        time.sleep(GAP_S)
        if data is None:
            row["status"] = "fetch failed: " + err
            rows.append(row); print(row["id"], kind, row["status"]); continue
        by = {int(x[0]): float(x[5]) for x in data}
        vols = [by.get(end_hour - k * 3600, 0.0) for k in range(6, 0, -1)]
        if sum(vols) <= 0:
            row["status"] = "no trades in the six hours"
            rows.append(row); print(row["id"], kind, row["status"]); continue
        row.update(stats(vols)); row["status"] = "ok"
        rows.append(row)
        print(row["id"], kind, r["exit_reason"], "cv", row["cv"], "max/min", row["max_over_min"], "hours", row["hours_with_trades"], "mean", row["mean_usd"])
    ok = [r for r in rows if r["status"] == "ok"]
    out = {"fpes": stats(FPES), "picked": len(picks), "tried": len(rows), "ok": len(ok),
           "ledger": {"rows": len(led), "losers": len(losers), "winners": len(winners)}}
    for kind in ("loser", "winner"):
        k = [r for r in ok if r["kind"] == kind]
        full = [r for r in k if r["hours_with_trades"] == 6]
        out[kind] = {"n": len(k), "median_cv": round(statistics.median([r["cv"] for r in k]), 3) if k else None,
                     "min_cv": min((r["cv"] for r in k), default=None),
                     "six_full_hours": len(full),
                     "median_cv_six_full": round(statistics.median([r["cv"] for r in full]), 3) if full else None,
                     "median_max_over_min_six_full": round(statistics.median([r["max_over_min"] for r in full]), 2) if full else None,
                     "cv_under_0.3": sum(1 for r in k if r["cv"] < 0.3), "cv_under_0.5": sum(1 for r in k if r["cv"] < 0.5)}
    out["rugged_flag_ok"] = [{"id": r["id"], "cv": r["cv"]} for r in ok if r["rugged"] == "1"]
    out["flattest_five"] = [{"id": r["id"], "kind": r["kind"], "exit": r["exit_reason"], "cv": r["cv"], "vols": r["vols"]}
                            for r in sorted(ok, key=lambda r: r["cv"])[:5]]
    (HERE / "results.json").write_text(json.dumps({"summary": out, "rows": rows}, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    sys.exit(main())
