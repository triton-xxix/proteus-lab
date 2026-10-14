"""Sales call funnel and opener-consistency check (P-0157, from Skool S-21).

Reads a CSV of calls: timestamp, rep, opener, picked_up, talk_seconds, booked, showed.
Prints pickup by hour, the funnel (dial > pickup > 60 s conversation > booked > showed), and how many
distinct openers the team uses, clustering openers whose difflib ratio is >= THRESH to a cluster's first.

    python3 funnel.py calls.csv          report
    python3 funnel.py --synth out.csv    write 200 synthetic calls with planted truth
"""
import csv
import difflib
import json
import random
import sys
from collections import Counter, defaultdict

THRESH = 0.75

PLANTED = [
    "Hi {n}, it's Sam from Brightline, I know I'm calling out of the blue, have you got thirty seconds?",
    "Morning {n}, this is a cold call, do you want to hang up or give me a minute to say why I rang?",
    "Hello {n}, I was looking at your website and noticed you don't take bookings online, is that on purpose?",
    "Hi {n}, quick one, who looks after the boiler servicing contracts at your place?",
]
NAMES = ["Alex", "Priya", "Tom", "Grace", "Liam", "Fatima", "Owen", "Chloe"]


def synth(path, n=200, seed=14):
    rng = random.Random(seed)
    # planted truth: 10:00 is the best hour (pickup 0.35), others 0.12 to 0.20; script 2 converts best
    hour_p = {9: 0.15, 10: 0.35, 11: 0.20, 12: 0.12, 13: 0.14, 14: 0.18, 15: 0.16, 16: 0.13}
    rows = []
    for i in range(n):
        h = rng.choice(list(hour_p))
        k = rng.randrange(4)
        text = PLANTED[k].format(n=rng.choice(NAMES))
        if rng.random() < 0.4:  # reps paraphrase: drop or swap a few words
            w = text.split()
            j = rng.randrange(len(w))
            w[j] = rng.choice(["just", "really", "so", w[j]])
            text = " ".join(w)
        up = rng.random() < hour_p[h]
        talk = int(rng.expovariate(1 / (80 if k == 2 else 45))) if up else 0
        booked = up and talk >= 60 and rng.random() < (0.5 if k == 2 else 0.25)
        showed = booked and rng.random() < 0.7
        rows.append({"timestamp": f"2026-10-{1 + i % 10:02d}T{h:02d}:{rng.randrange(60):02d}:00", "rep": f"R{rng.randrange(1, 5)}",
                     "opener": text, "picked_up": int(up), "talk_seconds": talk, "booked": int(booked), "showed": int(showed)})
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def report(path):
    rows = list(csv.DictReader(open(path)))
    by_hour = defaultdict(lambda: [0, 0])
    for r in rows:
        h = int(r["timestamp"][11:13])
        by_hour[h][0] += 1
        by_hour[h][1] += int(r["picked_up"])
    dials = len(rows)
    up = sum(int(r["picked_up"]) for r in rows)
    conv = sum(int(r["talk_seconds"]) >= 60 for r in rows)
    booked = sum(int(r["booked"]) for r in rows)
    showed = sum(int(r["showed"]) for r in rows)
    clusters = []  # [representative, count, conversations, bookings]
    for r in rows:
        t = r["opener"].lower()
        for c in clusters:
            if difflib.SequenceMatcher(None, c[0], t).ratio() >= THRESH:
                break
        else:
            c = [t, 0, 0, 0]
            clusters.append(c)
        c[1] += 1
        c[2] += int(r["talk_seconds"]) >= 60
        c[3] += int(r["booked"])
    hours = {h: (v[0], round(v[1] / v[0], 3)) for h, v in sorted(by_hour.items())}
    best = max(hours, key=lambda h: hours[h][1])
    out = {
        "dials": dials, "pickup_rate": round(up / dials, 3),
        "pickup_to_60s": round(conv / up, 3) if up else None,
        "conv_to_booked": round(booked / conv, 3) if conv else None,
        "show_rate": round(showed / booked, 3) if booked else None,
        "pickup_by_hour": hours, "best_hour": best,
        "distinct_openers": len(clusters),
        "openers": [{"text": c[0][:70], "uses": c[1], "conversations": c[2], "booked": c[3]} for c in sorted(clusters, key=lambda c: -c[1])],
    }
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--synth":
        synth(sys.argv[2])
    else:
        report(sys.argv[1])
