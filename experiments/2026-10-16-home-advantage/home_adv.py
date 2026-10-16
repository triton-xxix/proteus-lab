"""Home advantage by season from football-data.co.uk, keyless.

Premier League (E0) every season from 1993/94, plus Germany, Spain and Italy
for the seasons around the empty-stadium year. Writes seasons.csv and prints a table.
"""
import csv
import io
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = "https://www.football-data.co.uk/mmz4281/{code}/{div}.csv"


def code(y):
    return f"{y % 100:02d}{(y + 1) % 100:02d}"


def fetch(div, y):
    url = BASE.format(code=code(y), div=div)
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-lab"})
    raw = urllib.request.urlopen(req, timeout=30).read().decode("latin-1")
    rows = []
    for r in csv.DictReader(io.StringIO(raw)):
        try:
            h, a = int(r["FTHG"]), int(r["FTAG"])
        except (KeyError, ValueError, TypeError):
            continue
        rows.append((h, a))
    return rows


def summarise(rows):
    n = len(rows)
    hw = sum(1 for h, a in rows if h > a)
    d = sum(1 for h, a in rows if h == a)
    gd = sum(h - a for h, a in rows) / n
    pts_h = (3 * hw + d) / n
    pts_a = (3 * (n - hw - d) + d) / n
    return n, hw / n, d / n, 1 - (hw + d) / n, gd, pts_h - pts_a


def main():
    jobs = [("E0", y) for y in range(1993, 2026)]
    jobs += [(div, y) for div in ("D1", "SP1", "I1") for y in range(2017, 2026)]
    out = []
    for div, y in jobs:
        try:
            rows = fetch(div, y)
        except Exception as e:  # noqa: BLE001
            print(f"{div} {y}: fetch failed {e}", file=sys.stderr)
            continue
        if len(rows) < 100:
            print(f"{div} {y}: only {len(rows)} rows, skipped", file=sys.stderr)
            continue
        n, hw, d, aw, gd, ppg = summarise(rows)
        season = f"{y}/{(y + 1) % 100:02d}"
        out.append([div, season, n, round(hw, 4), round(d, 4), round(aw, 4), round(gd, 3), round(ppg, 3)])
        print(f"{div:4} {season}  n={n:3}  home {hw:.1%}  draw {d:.1%}  away {aw:.1%}  goal diff {gd:+.2f}  pts gap {ppg:+.2f}")
        time.sleep(0.3)
    with open(OUT / "seasons.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["div", "season", "matches", "home_win", "draw", "away_win", "home_goal_diff", "home_minus_away_ppg"])
        w.writerows(out)


if __name__ == "__main__":
    main()
