"""P-0248: keep each Munich daily-high market's winner before Smarkets drops it (about ten days).

Reads the Munich "Highest Temperature" markets in exchange/SNAPSHOTS.csv, asks the keyless API for any
not yet in exchange/munich_outcomes.jsonl, and appends one line per settled market. Append-only; run
nightly from step 3 so step 4 commits it. Prints one line.
"""
import csv, json, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
sys.path.insert(0, str(ROOT / "exchange"))
import exchange  # noqa: E402

LOG = ROOT / "exchange/munich_outcomes.jsonl"
have = {json.loads(l)["market_id"] for l in LOG.open()} if LOG.exists() else set()
markets = {}
for r in csv.DictReader(open(ROOT / "exchange/SNAPSHOTS.csv")):
    if r["market"] == "Highest Temperature" and r["market_id"] not in have:
        markets[r["market_id"]] = r["event"]

added, waiting, gone = 0, 0, 0
with LOG.open("a") as f:
    for mid, event in sorted(markets.items()):
        cs = exchange.get(f"/markets/{mid}/contracts/").get("contracts", [])
        if not cs:
            gone += 1
            continue
        win = [c for c in cs if c.get("state_or_outcome") == "winner"]
        if not win:
            waiting += 1
            continue
        f.write(json.dumps({"market_id": mid, "event": event, "winner": win[0]["name"],
                            "winner_id": win[0]["id"], "seen_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}) + "\n")
        added += 1
print(f"munich outcomes: {added} added, {len(have) + added} kept, {waiting} not settled, {gone} already dropped by the API")
