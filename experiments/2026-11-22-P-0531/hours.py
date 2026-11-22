"""P-0531: Lichess challenge acceptance by UTC hour and weekday, from games/lichess/CHALLENGES.csv.

Accepted = a verdict starting 'accept' (the log's own word); every other verdict is a refusal of some
kind. Also by ISO week x hour, so an hour can be compared with 08:00 inside the same week.

    python3 hours.py
"""
import csv, json, os
from collections import Counter, defaultdict
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open("/Users/triton/PROTEUS/games/lichess/CHALLENGES.csv")))
verdicts = Counter(r["verdict"].split(" ")[0] for r in rows)
acc = lambda r: r["verdict"].lower().startswith("accept")


def table(key):
    t = defaultdict(lambda: [0, 0])
    for r in rows:
        k = key(datetime.strptime(r["utc"], "%Y-%m-%dT%H:%M:%SZ"))
        t[k][0] += 1
        t[k][1] += acc(r)
    return {str(k): {"asks": n, "accepted": a, "rate": round(100 * a / n, 1)} for k, (n, a) in sorted(t.items())}


out = {"rows": len(rows), "verdict_first_words": dict(verdicts),
       "by_hour": table(lambda d: d.hour), "by_weekday": table(lambda d: d.strftime("%a")),
       "by_week_hour": table(lambda d: "%s h%02d" % (d.strftime("%G-W%V"), d.hour)),
       "first": rows[0]["utc"], "last": rows[-1]["utc"]}
h8 = out["by_hour"].get("8")
out["hours_10_points_above_08"] = [h for h, v in out["by_hour"].items() if v["asks"] >= 50 and h8 and v["rate"] >= h8["rate"] + 10]
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("rows", "verdict_first_words", "by_hour", "by_weekday", "hours_10_points_above_08", "first", "last")}, indent=1))
for k, v in out["by_week_hour"].items():
    print(k, v)
