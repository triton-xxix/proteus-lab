"""P-0436: FPES (voided G-0075) from every pool GeckoTerminal lists for the mint.

Keyless. For each pool: daily candles (whole life), hourly candles ending 14 Oct 00:00Z, and minute
candles for the 24 h after the 12 Oct 22:54:22Z entry. Read only; the ledger and VOIDED.csv are not
touched. Six requests, two seconds apart, no retry.
"""
import csv, json, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
GT = "https://api.geckoterminal.com/api/v2/networks/solana/"
UA = {"User-Agent": "proteus-lab/0.2", "Accept": "application/json"}
MINT = "AMnU8vAQvDkayAcyutBL8eyxCoSHUV4CcHUQwuePpump"
ENTRY_ISO, STALE = "2026-10-12T22:54:22Z", 0.4202
T0 = int(datetime(2026, 10, 12, 22, 54, 22, tzinfo=timezone.utc).timestamp())
SNAP = int(datetime(2026, 10, 11, 22, 23, 0, tzinfo=timezone.utc).timestamp())


def get(path):
    time.sleep(2.0)
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(GT + path, headers=UA), timeout=30).read())
    except Exception as e:  # a refusal is a result
        return {"error": type(e).__name__ + ": " + str(e)[:120]}


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def ohlcv(pool, frame, before=None, limit=1000):
    q = "pools/%s/ohlcv/%s?limit=%d&currency=usd" % (pool, frame, limit)
    if before:
        q += "&before_timestamp=%d" % before
    j = get(q)
    if "error" in j:
        return None, j["error"]
    rows = j.get("data", {}).get("attributes", {}).get("ohlcv_list", [])
    return sorted(rows), None


def main():
    out = {"mint": MINT, "entry": ENTRY_ISO, "stale_entry": STALE, "pools": []}
    pl = get("tokens/%s/pools" % MINT)
    for p in pl.get("data", []):
        a = p["attributes"]
        row = {"pool": a["address"], "dex": p["relationships"]["dex"]["data"]["id"], "created": a["pool_created_at"],
               "price_now": float(a["base_token_price_usd"]), "reserve_now_usd": float(a["reserve_in_usd"]),
               "tx_24h": a["transactions"]["h24"]["buys"] + a["transactions"]["h24"]["sells"]}
        day, err = ohlcv(a["address"], "day", limit=120)
        row["day_error"] = err
        if day:
            row["day_candles"] = len(day)
            row["first_day"], row["last_day"] = iso(day[0][0]), iso(day[-1][0])
            row["days"] = [{"day": iso(d[0])[:10], "o": d[1], "h": d[2], "l": d[3], "c": d[4], "vol_usd": round(d[5], 0)} for d in day]
            with open(HERE / (a["address"][:8] + "-day.csv"), "w", newline="") as fh:
                w = csv.writer(fh); w.writerow(["ts", "o", "h", "l", "c", "v"]); w.writerows(day)
        hour, err = ohlcv(a["address"], "hour", before=T0 + 26 * 3600, limit=1000)
        row["hour_error"] = err
        if hour:
            with open(HERE / (a["address"][:8] + "-hour.csv"), "w", newline="") as fh:
                w = csv.writer(fh); w.writerow(["ts", "o", "h", "l", "c", "v"]); w.writerows(hour)
            row["hour_candles"] = len(hour)
            row["first_hour"], row["last_hour"] = iso(hour[0][0]), iso(hour[-1][0])
            peak = max(hour, key=lambda x: x[2])
            row["peak_hour"], row["peak_high"] = iso(peak[0]), peak[2]
            at_snap = [h for h in hour if h[0] <= SNAP]
            row["close_at_snapshot_hour"] = at_snap[-1][4] if at_snap else None
            row["snapshot_hour"] = iso(at_snap[-1][0]) if at_snap else None
            before = [h for h in hour if h[0] <= T0]
            row["last_hour_before_entry"] = iso(before[-1][0]) if before else None
            row["close_before_entry"] = before[-1][4] if before else None
            row["hours_with_trades_after_entry"] = len([h for h in hour if h[0] > T0])
            # first hour whose close is 90% and 99% under the stale price
            for cut, key in ((0.10, "first_hour_90pct_under_stale"), (0.01, "first_hour_99pct_under_stale")):
                hit = next((h for h in hour if h[4] <= STALE * cut), None)
                row[key] = iso(hit[0]) if hit else None
            row["hours_around"] = [{"hour": iso(h[0]), "o": h[1], "h": h[2], "l": h[3], "c": h[4], "vol_usd": round(h[5], 0)}
                                   for h in hour if SNAP - 6 * 3600 <= h[0] <= T0 + 26 * 3600]
        minute, err = ohlcv(a["address"], "minute", before=T0 + 24 * 3600, limit=1000)
        row["minute_error"] = err
        if minute is not None:
            win = [m for m in minute if T0 <= m[0] <= T0 + 24 * 3600]
            row["minute_candles_returned"], row["minute_candles_in_24h_after_entry"] = len(minute), len(win)
            if minute:
                row["minute_first"], row["minute_last"] = iso(minute[0][0]), iso(minute[-1][0])
        out["pools"].append(row)
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    for r in out["pools"]:
        short = {k: v for k, v in r.items() if k not in ("days", "hours_around")}
        print(json.dumps(short))
        for d in r.get("days", []):
            print("   day", d)
        for h in r.get("hours_around", [])[:60]:
            print("   hour", h)


if __name__ == "__main__":
    main()
