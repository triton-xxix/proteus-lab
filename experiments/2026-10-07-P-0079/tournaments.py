"""P-0079: list Metaculus tournaments with prize pools, newest first.

Reads the API token from the Proteus vault through bin/secrets.py and never prints it.
Writes tournaments.json beside this file.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/bin")
from secrets import get  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
token = get("MetaculusAPI Credentials")
req = urllib.request.Request(
    "https://www.metaculus.com/api/projects/tournaments/",
    headers={"Authorization": f"Token {token}", "User-Agent": "proteus-lab probe P-0079"},
)
data = json.load(urllib.request.urlopen(req, timeout=60))
rows = data if isinstance(data, list) else data.get("results", data)
keep = []
for t in rows:
    keep.append({k: t.get(k) for k in (
        "id", "slug", "name", "prize_pool", "start_date", "close_date",
        "forecasting_end_date", "is_ongoing", "bot_leaderboard_status", "visibility",
    )})
json.dump(keep, open(os.path.join(HERE, "tournaments.json"), "w"), indent=1)
print(len(keep), "tournaments; keys on one record:", sorted(rows[0].keys()) if rows else [])
