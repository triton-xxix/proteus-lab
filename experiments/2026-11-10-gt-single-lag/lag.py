"""How stale is GeckoTerminal's single-pool endpoint against its own trades list?

Takes the new_pools page already saved (argv[1]), picks the pool with the most h1 transactions among
those created in the last 3 hours (a busy young pool, so the counts move inside two minutes), then at
0, 10, 30, 60 and 120 s reads /pools/ADDR and /pools/ADDR/trades and writes both side by side.
Keyless, 10 calls, read-only.
"""
import json, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://api.geckoterminal.com/api/v2/networks/solana/pools/"
HDR = {"Accept": "application/json;version=20230302", "User-Agent": "curl/8"}


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=20) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": repr(e)[:160]}


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


page = json.loads(Path(sys.argv[1]).read_text())["data"]
now = datetime.now(timezone.utc)
cands = []
for p in page:
    a = p["attributes"]
    age_min = (now - ts(a["pool_created_at"])).total_seconds() / 60
    h1 = a["transactions"]["h1"]
    cands.append((h1["buys"] + h1["sells"], age_min, a["address"], a["name"]))
cands.sort(reverse=True)
tx, age, addr, name = cands[0]
print("picked", name, addr, "page h1 tx", tx, "age min at page read", round(age, 1))

reads, t0 = [], time.time()
for wait in (0, 10, 30, 60, 120):
    while time.time() - t0 < wait:
        time.sleep(0.5)
    at = datetime.now(timezone.utc)
    single = get(BASE + addr)
    trades = get(BASE + addr + "/trades")
    row = {"t": wait, "at": at.isoformat(timespec="seconds")}
    if "data" in single:
        a = single["data"]["attributes"]
        h1 = a["transactions"]["h1"]
        m5 = a["transactions"]["m5"]
        row.update(single_h1_tx=h1["buys"] + h1["sells"], single_m5_tx=m5["buys"] + m5["sells"],
                   single_h1_vol=a["volume_usd"]["h1"], single_price=a["base_token_price_usd"])
    else:
        row["single_error"] = single.get("error") or str(single)[:120]
    if "data" in trades:
        stamps = sorted(ts(t["attributes"]["block_timestamp"]) for t in trades["data"])
        row.update(trades_listed=len(stamps),
                   trades_last_hour=sum(1 for s in stamps if (at - s).total_seconds() <= 3600),
                   trades_last_5m=sum(1 for s in stamps if (at - s).total_seconds() <= 300),
                   newest_trade_age_s=round((at - stamps[-1]).total_seconds(), 1) if stamps else None,
                   oldest_listed_age_s=round((at - stamps[0]).total_seconds(), 1) if stamps else None)
    else:
        row["trades_error"] = trades.get("error") or str(trades)[:120]
    reads.append(row)
    print(json.dumps(row))

out = {"pool": addr, "name": name, "page_h1_tx": tx, "age_min_at_page_read": round(age, 1), "reads": reads}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
