"""Score pitch/JUDGEMENT.csv against eloratings.net results (keyless).

Fills result, home_goals, away_goals, brier and market_brier on rows that have none yet.
Never rewrites a filled row. Prints the paired Brier difference on counted rows (PASS-MARKS.md,
"The judgement book": J-0009 onwards; J-0001 to J-0008 were seen before the lines were written).
Blind rows (blind_* columns, committed before odds_seen_at) get blind_brier and their own paired line.
Found and tested in P-0024 (experiments/2026-09-27-P-0024/).
"""
import csv, os, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "JUDGEMENT.csv")
RESULTS_URL = "https://www.eloratings.net/latest.tsv"
TEAMS_URL = "https://www.eloratings.net/en.teams.tsv"
# eloratings names that differ from the book's. Match name to code, never guess codes (NI is Nicaragua).
# "North Macedonia" needs no alias: it is NM. "Macedonia" is MK, which has no current results, and
# the old alias to it left J-0019 and J-0052 unscored for days (found 5 Oct 2026).
ALIAS = {"Republic of Ireland": "Ireland", "Czech Republic": "Czechia"}
SEEN = {f"J-{i:04d}" for i in range(1, 9)}
LEAN_MIN = 0.03


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-lab (github.com/triton-xxix/proteus-lab)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def brier(p, o):
    return sum((a - b) ** 2 for a, b in zip(p, o))


def main():
    name2code = {}
    for line in fetch(TEAMS_URL).splitlines():
        parts = line.split("\t")
        for n in parts[1:]:
            if n:
                name2code.setdefault(n, parts[0])
    results = {}
    for line in fetch(RESULTS_URL).splitlines():
        p = line.split("\t")
        if len(p) >= 7 and p[5].isdigit() and p[6].isdigit():
            results[(f"{p[0]}-{p[1]}-{p[2]}", p[3], p[4])] = (int(p[5]), int(p[6]))

    with open(BOOK, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)

    filled, unmapped = 0, []
    for r in rows:
        if r["result"] or not r["market_home"]:
            continue
        hc = name2code.get(ALIAS.get(r["home"], r["home"]))
        ac = name2code.get(ALIAS.get(r["away"], r["away"]))
        if not hc or not ac:
            unmapped.append(r["id"])
            continue
        d = r["kickoff_utc"][:10]
        if (d, hc, ac) in results:
            hg, ag = results[(d, hc, ac)]
        elif (d, ac, hc) in results:
            ag, hg = results[(d, ac, hc)]
        else:
            continue
        o = (1, 0, 0) if hg > ag else (0, 1, 0) if hg == ag else (0, 0, 1)
        me = [float(r[k]) for k in ("p_home", "p_draw", "p_away")] if r.get("p_home") else None
        mk = [float(r[k]) for k in ("market_home", "market_draw", "market_away")]
        r.update(result="HDA"[o.index(1)], home_goals=hg, away_goals=ag, market_brier=round(brier(mk, o), 4))
        if r.get("p_home"):
            r["brier"] = round(brier(me, o), 4)
        if r.get("blind_home"):
            bl = [float(r[k]) for k in ("blind_home", "blind_draw", "blind_away")]
            r["blind_brier"] = round(brier(bl, o), 4)
        filled += 1

    if filled:
        with open(BOOK, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    blind = [r for r in rows if r.get("blind_brier") and r["market_brier"]
             and r["blind_committed_at"] < r["kickoff_utc"] and r["blind_committed_at"] < r["odds_seen_at"]]
    both = [r for r in blind if r["brier"]]
    scored = [r for r in rows if r["brier"]]
    counted = [r for r in scored if r["id"] not in SEEN and r["committed_at"] < r["kickoff_utc"]]
    leaned = [r for r in counted if float(r["lean_size"] or 0) >= LEAN_MIN]

    def diff(rs):
        return round(sum(float(r["brier"]) - float(r["market_brier"]) for r in rs) / len(rs), 4) if rs else None

    print(f"filled {filled}, scored {len(scored)}, seen {len(scored) - len([r for r in scored if r['id'] not in SEEN])}, "
          f"counted {len(counted)}, unmapped {len(unmapped)}")
    print(f"blind rows counted {len(blind)}: blind minus market "
          f"{round(sum(float(r['blind_brier']) - float(r['market_brier']) for r in blind) / len(blind), 4) if blind else None}; "
          f"on {len(both)} rows with both columns, blind minus anchored "
          f"{round(sum(float(r['blind_brier']) - float(r['brier']) for r in both) / len(both), 4) if both else None}")
    print(f"paired Brier diff (me minus market): seen {diff([r for r in scored if r['id'] in SEEN])}, "
          f"counted {diff(counted)}, counted leaned {diff(leaned)} over {len(leaned)}")


if __name__ == "__main__":
    main()
