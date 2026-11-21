"""P-0512: replay games/lichess/CHALLENGES.csv under "drop a bot after N refusals with no acceptance".

A refusal here is `declined` or `no answer`. `refused 400` (mostly the bot's 100-games-a-day cap) and
`refused 429` (my rate limit) are neutral: they neither count toward N nor reset it. Once a bot has N
refusals and no acceptance, every later ask to it is dropped: saved if it would have been refused,
lost if it would have been accepted. Rows are in log order. Writes results.json.
"""
import csv
import json
import sys
from collections import defaultdict

SRC, OUT = sys.argv[1], sys.argv[2]
rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
total_acc = sum(1 for r in rows if r["verdict"] == "accepted")
res = {"rows": len(rows), "accepted": total_acc, "by_N": {}}
for N in (1, 2, 3, 5, 8):
    ref = defaultdict(int)
    acc = defaultdict(bool)
    dropped = saved = lost = 0
    lost_bots = set()
    dropped_bots = set()
    for r in rows:
        b, v = r["opponent"].lower(), r["verdict"]
        if not acc[b] and ref[b] >= N:
            dropped += 1
            dropped_bots.add(b)
            if v == "accepted":
                lost += 1
                lost_bots.add(b)
            else:
                saved += 1
            continue
        if v == "accepted":
            acc[b] = True
        elif v in ("declined", "no answer"):
            ref[b] += 1
    res["by_N"][N] = {"asks_dropped": dropped, "refusals_saved": saved, "acceptances_lost": lost,
                      "bots_dropped": len(dropped_bots), "bots_lost": sorted(lost_bots)}
print(json.dumps(res, indent=1))
json.dump(res, open(OUT, "w"), indent=1)
