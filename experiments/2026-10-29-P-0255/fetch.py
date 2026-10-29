"""P-0255 fetch: the per-user export (api/games/user/tritonxxix) answered {"error":"Not found"} keyless on
29 Oct 2026 though api/user/tritonxxix is public, so post the ids from games/lichess/GAMES.csv to the
keyless by-ids export instead.

    python3 experiments/2026-10-29-P-0255/fetch.py
"""
import csv
import urllib.request

ids = [r["game_id"] for r in csv.DictReader(open("/Users/triton/PROTEUS/games/lichess/GAMES.csv")) if r["game_id"]]
req = urllib.request.Request("https://lichess.org/api/games/export/_ids?clocks=true&moves=false",
                             data=",".join(ids).encode(), method="POST",
                             headers={"Accept": "application/x-ndjson", "Content-Type": "text/plain"})
body = urllib.request.urlopen(req, timeout=60).read()
open("/Users/triton/PROTEUS/sandbox/lichess-tritonxxix.ndjson", "wb").write(body)
print(len(ids), "ids sent,", body.count(b"\n"), "lines back")
