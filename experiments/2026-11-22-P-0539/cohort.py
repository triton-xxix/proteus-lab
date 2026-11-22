"""P-0539: is the Lichess acceptance fall since week 41 the same bots declining more, or new never-yes bots?

games/lichess/CHALLENGES.csv on disk. Answerable asks = accepted + declined + no answer (refused 400 and
429 are Lichess caps, not a bot's answer). Per ISO week: acceptance among veterans (first asked in week 41
or earlier) and newcomers (first asked later); share of asks going to bots that never once said yes;
and per-bot acceptance by week for bots asked in three or more weeks.
"""
import csv, json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SRC = Path("/Users/triton/PROTEUS/games/lichess/CHALLENGES.csv")
OUT = Path(__file__).with_name("results.json")
ANS = {"accepted", "declined", "no answer"}

rows = []
for r in csv.DictReader(open(SRC)):
    wk = datetime.fromisoformat(r["utc"].replace("Z", "+00:00")).isocalendar()[1]
    rows.append((wk, r["opponent"].lower(), r["verdict"]))

first = {}
ever_yes = set()
for wk, bot, v in rows:
    first[bot] = min(first.get(bot, 99), wk)
    if v == "accepted":
        ever_yes.add(bot)

weeks = sorted({w for w, _, _ in rows})
table = []
for w in weeks:
    cell = {"week": w}
    for name, sel in (("all", lambda b: True), ("veteran", lambda b: first[b] <= 41), ("newcomer", lambda b: first[b] > 41)):
        a = [v for ww, b, v in rows if ww == w and v in ANS and sel(b)]
        cell[name] = {"asks": len(a), "acc": a.count("accepted"),
                      "rate": round(100 * a.count("accepted") / len(a), 1) if a else None}
    ans = [b for ww, b, v in rows if ww == w and v in ANS]
    cell["never_yes_share"] = round(100 * sum(1 for b in ans if b not in ever_yes) / len(ans), 1) if ans else None
    cell["distinct_bots"] = len(set(ans))
    table.append(cell)

per_bot = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for wk, bot, v in rows:
    if v in ANS:
        per_bot[bot][wk][1] += 1
        per_bot[bot][wk][0] += v == "accepted"
multi = {b: d for b, d in per_bot.items() if len(d) >= 3}
# same bots: those asked in week 41 or earlier AND after; their rate before v after
early = [0, 0]; late = [0, 0]
for b, d in multi.items():
    if any(w <= 41 for w in d) and any(w > 41 for w in d):
        for w, (acc, n) in d.items():
            tgt = early if w <= 41 else late
            tgt[0] += acc; tgt[1] += n
res = {
    "rows": len(rows), "bots": len(first), "ever_yes_bots": len(ever_yes),
    "weeks": table,
    "bots_asked_3plus_weeks": len(multi),
    "same_bots_both_sides_of_wk41": {
        "n_bots": sum(1 for d in multi.values() if any(w <= 41 for w in d) and any(w > 41 for w in d)),
        "wk41_or_earlier": {"acc": early[0], "asks": early[1], "rate": round(100 * early[0] / early[1], 1) if early[1] else None},
        "after_wk41": {"acc": late[0], "asks": late[1], "rate": round(100 * late[0] / late[1], 1) if late[1] else None},
    },
}
OUT.write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
