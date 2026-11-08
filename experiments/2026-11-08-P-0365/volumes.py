"""P-0365: how much has traded on each Munich daily-high market on Smarkets, ten days back?

Reads market ids from exchange/BOOK.csv, calls /v3/markets/{id}/volumes/ (keyless, one call a market).
Writes the raw responses and a summary into this folder.
"""
import csv, json, pathlib, statistics, time, urllib.error, urllib.request
from datetime import datetime, timedelta, timezone

HERE = pathlib.Path("/Users/triton/PROTEUS/experiments/2026-11-08-P-0365")
BOOK = pathlib.Path("/Users/triton/PROTEUS/exchange/BOOK.csv")
API = "https://api.smarkets.com/v3"
TODAY = datetime(2026, 11, 8, tzinfo=timezone.utc)
FROM = TODAY - timedelta(days=10)


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "proteus-exchange/0.1", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


rows = [r for r in csv.DictReader(open(BOOK)) if "munich" in (r["event"] + r["market"]).lower() or "highest temperature" in (r["event"] + r["market"]).lower()]
recent = [r for r in rows if datetime.fromisoformat(r["event_start"].replace("Z", "+00:00")) >= FROM]
ids = sorted({r["market_id"] for r in recent})
print("book rows on Munich", len(rows), "in last ten days", len(recent), "distinct markets", len(ids))

raw, errors = {}, {}
for m in ids:
    try:
        raw[m] = get(f"/markets/{m}/volumes/")
    except urllib.error.HTTPError as e:
        errors[m] = e.code
    except Exception as e:
        errors[m] = str(e)[:80]
    time.sleep(0.3)
(HERE / "raw.json").write_text(json.dumps(raw, indent=1))
if raw:
    first = next(iter(raw))
    print("first raw response:", json.dumps(raw[first])[:600])
print("errors", errors)
print(json.dumps({"n_ok": len(raw), "n_err": len(errors)}))
_ = statistics
