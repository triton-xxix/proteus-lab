"""P-0489: do a manager's Wikipedia views climb in the week before he goes?

Exits: the 11 in-season rows of the Managerial changes table in the 2025-26 Premier League article
(changes-section.txt, pulled by changes.py on 19 Nov 2026). Controls: the 13 managers whose clubs
have no row in that table after pre-season, each scored on the same 11 dates.

Ratio = mean daily views on days D-7..D-1 over the median daily views on days D-37..D-8, where D is
the date of vacancy. The exit day itself is not in either window.

    python3 sackings.py

Keyless, read only, standard library. Caches each article's series in views-cache.json.
"""
import json, statistics, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / "views-cache.json"
HALT = Path("/Users/triton/PROTEUS/HALT")
UA = "proteus-probe/0.1 (keyless research script)"
API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/"
START, END = "20250701", "20260510"

EXITS = [
    ("Nuno_Espírito_Santo", "Nottingham Forest", "2025-09-08", "Sacked"),
    ("Graham_Potter", "West Ham United", "2025-09-27", "Sacked"),
    ("Ange_Postecoglou", "Nottingham Forest", "2025-10-18", "Sacked"),
    ("Vítor_Pereira_(footballer,_born_1968)", "Wolverhampton Wanderers", "2025-11-02", "Sacked"),
    ("Enzo_Maresca", "Chelsea", "2026-01-01", "Resigned"),
    ("Ruben_Amorim", "Manchester United", "2026-01-05", "Sacked"),
    ("Thomas_Frank_(football_manager)", "Tottenham Hotspur", "2026-02-11", "Sacked"),
    ("Sean_Dyche", "Nottingham Forest", "2026-02-12", "Sacked"),
    ("Igor_Tudor", "Tottenham Hotspur", "2026-03-29", "Mutual consent"),
    ("Liam_Rosenior", "Chelsea", "2026-04-22", "Sacked"),
    ("Scott_Parker", "Burnley", "2026-04-30", "Mutual consent"),
]
CONTROLS = [
    "Mikel_Arteta", "Pep_Guardiola", "Arne_Slot", "Unai_Emery", "Eddie_Howe", "Oliver_Glasner",
    "Andoni_Iraola", "Marco_Silva", "Fabian_Hürzeler", "David_Moyes", "Keith_Andrews_(footballer)",
    "Daniel_Farke", "Régis_Le_Bris",
]
THRESHOLDS = [1.5, 2.0, 3.0]


def fetch(title):
    url = API + urllib.parse.quote(title, safe="") + "/daily/" + START + "/" + END
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                items = json.loads(r.read())["items"]
            return {i["timestamp"][:8]: i["views"] for i in items}
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {"error": "404"}
            time.sleep(4 * (attempt + 1))
        except Exception:
            time.sleep(4 * (attempt + 1))
    return {"error": "gave up after 5 tries"}


def ratio(series, d):
    """mean of D-7..D-1 over median of D-37..D-8; None if either window is short."""
    week = [series.get((d - timedelta(days=k)).strftime("%Y%m%d")) for k in range(1, 8)]
    base = [series.get((d - timedelta(days=k)).strftime("%Y%m%d")) for k in range(8, 38)]
    week = [x for x in week if x is not None]
    base = [x for x in base if x is not None]
    if len(week) < 7 or len(base) < 25:
        return None
    med = statistics.median(base)
    if med <= 0:
        return None
    return {"week_mean": round(statistics.mean(week), 1), "base_median": med,
            "ratio": round(statistics.mean(week) / med, 3), "week_max": max(week),
            "exit_day": series.get(d.strftime("%Y%m%d")),
            # the same ratio with the week's biggest day dropped: is it one match day or a climb?
            "ratio_ex_max": round(statistics.mean(sorted(week)[:-1]) / med, 3)}


def main():
    if HALT.exists():
        print("HALT")
        return 1
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    titles = [e[0] for e in EXITS] + CONTROLS
    for t in titles:
        if t in cache and "error" not in cache[t]:
            continue
        cache[t] = fetch(t)
        print(t, len(cache[t]), "days" if "error" not in cache[t] else cache[t], flush=True)
        CACHE.write_text(json.dumps(cache))
        time.sleep(1.5)

    exits = []
    for title, club, day, manner in EXITS:
        s = cache.get(title, {})
        d = date.fromisoformat(day)
        row = {"manager": title, "club": club, "date": day, "manner": manner}
        r = ratio(s, d) if "error" not in s else None
        if r:
            row.update(r)
        else:
            row["skipped"] = s.get("error", "window short")
        exits.append(row)
        print(json.dumps(row, ensure_ascii=False))

    controls = []
    for title in CONTROLS:
        s = cache.get(title, {})
        if "error" in s:
            print("control missing:", title, s)
            continue
        for _, _, day, _ in EXITS:
            r = ratio(s, date.fromisoformat(day))
            if r:
                controls.append({"manager": title, "date": day, **r})

    scored = [e for e in exits if "ratio" in e]
    rs = [e["ratio"] for e in scored]
    cr = [c["ratio"] for c in controls]
    summary = {
        "exits": len(exits), "exits_scored": len(scored),
        "median_ratio": statistics.median(rs) if rs else None,
        "min_ratio": min(rs) if rs else None, "max_ratio": max(rs) if rs else None,
        "median_ratio_ex_max": statistics.median([e["ratio_ex_max"] for e in scored]) if scored else None,
        "control_managers": len({c["manager"] for c in controls}),
        "control_windows": len(controls),
        "control_median_ratio": statistics.median(cr) if cr else None,
        "flags": {},
    }
    for th in THRESHOLDS:
        hit = sum(1 for x in rs if x > th)
        fa = sum(1 for x in cr if x > th)
        prec = hit / (hit + fa) if hit + fa else None
        summary["flags"][str(th)] = {
            "caught": hit, "of": len(rs), "false_alarms": fa, "control_windows": len(cr),
            "false_alarm_rate": round(fa / len(cr), 3) if cr else None,
            "share_of_flags_that_were_exits": round(prec, 3) if prec is not None else None,
        }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "exits": exits, "controls": controls}, indent=1, ensure_ascii=False))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
