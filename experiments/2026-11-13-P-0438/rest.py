"""P-0438: the metronome measure on the ledger rows P-0437 did not reach, pooled with its rows.

Imports P-0437's metronome.py for the fetch and the statistics (same window, same CV). The cut is
fixed before this run: only trades with volume in all six pre-entry hours count. Every ledger row
that exited (any reason) and is not in P-0437's results is tried, newest first. Winner means
take_profit; loser means stop_loss, rug or rugged=1; other exits (time_stop, trail_stop) are kept
and reported by pnl sign. 3.5 s between calls, wall-clock cap 330 s. Read only.
"""
import csv, json, statistics, sys, time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-11-13-P-0437")
import metronome as m  # noqa: E402

HERE = Path(__file__).resolve().parent
CAP_S, GAP_S = 330, 3.5


def kind_of(r):
    if r["exit_reason"] in ("stop_loss", "rug") or r.get("rugged") == "1":
        return "loser"
    if r["exit_reason"] == "take_profit":
        return "winner"
    return "other"


def main():
    first = json.loads((Path(m.__file__).resolve().parent / "results.json").read_text())["rows"]
    done = {r["id"] for r in first}
    snaps = {}
    for s in csv.DictReader(open(m.G / "SNAPSHOTS.csv")):
        snaps.setdefault(s["mint"], []).append((s["ts"], s["pair"]))
    led = [r for r in csv.DictReader(open(m.G / "LEDGER.csv")) if r["exit_reason"]]
    todo = [r for r in reversed(led) if r["id"] not in done]
    t_start, rows = time.time(), []
    for r in todo:
        if time.time() - t_start > CAP_S:
            print("wall-clock cap reached at", len(rows), "of", len(todo))
            break
        row = {"id": r["id"], "kind": kind_of(r), "token": r["token"], "exit_reason": r["exit_reason"], "rugged": r.get("rugged"),
               "pnl_gbp": r["pnl_gbp"], "entered_at": r["entered_at"], "rule_version": r["rule_version"]}
        seen = [p for t, p in sorted(snaps.get(r["mint"], [])) if t <= r["entered_at"]]
        if not seen:
            row["status"] = "no pool in snapshots"
            rows.append(row); continue
        end_hour = m.ts(r["entered_at"]) // 3600 * 3600
        data, err = m.hourly(seen[-1], end_hour)
        time.sleep(GAP_S)
        if data is None:
            row["status"] = "fetch failed: " + err
            rows.append(row); print(row["id"], row["status"]); continue
        by = {int(x[0]): float(x[5]) for x in data}
        vols = [by.get(end_hour - k * 3600, 0.0) for k in range(6, 0, -1)]
        if sum(vols) <= 0:
            row["status"] = "no trades in the six hours"
            rows.append(row); continue
        row.update(m.stats(vols)); row["status"] = "ok"
        rows.append(row)
    for r in first:
        r.setdefault("leg", "P-0437")
    for r in rows:
        r["leg"] = "P-0438"
    pooled = [r for r in first + rows if r.get("status") == "ok"]
    full = [r for r in pooled if r["hours_with_trades"] == 6]
    new_full = [r for r in rows if r.get("status") == "ok" and r["hours_with_trades"] == 6]

    def block(sel):
        out = {}
        for k in ("loser", "winner", "other"):
            s = [r["cv"] for r in sel if r["kind"] == k]
            out[k] = {"n": len(s), "median_cv": round(statistics.median(s), 3) if s else None}
        return out

    def lost(sel):
        neg = sum(1 for r in sel if float(r["pnl_gbp"] or 0) < 0)
        return {"n": len(sel), "lost_money": neg, "share": round(neg / len(sel), 3) if sel else None}

    status = {}
    for r in rows:
        status[r["status"]] = status.get(r["status"], 0) + 1
    summary = {"todo": len(todo), "tried": len(rows), "status": status,
               "pooled_ok": len(pooled), "pooled_six_full": len(full), "new_six_full": len(new_full),
               "six_full_pooled": block(full), "six_full_new_only": block(new_full),
               "base_rate_lost_money_six_full": lost(full),
               "cv_under_0.3": lost([r for r in full if r["cv"] < 0.3]),
               "cv_0.3_to_0.6": lost([r for r in full if 0.3 <= r["cv"] < 0.6]),
               "cv_0.6_plus": lost([r for r in full if r["cv"] >= 0.6]),
               "flattest_eight": [{"id": r["id"], "kind": r["kind"], "exit": r["exit_reason"], "pnl_gbp": r["pnl_gbp"], "cv": r["cv"], "leg": r["leg"]}
                                  for r in sorted(full, key=lambda r: r["cv"])[:8]]}
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
