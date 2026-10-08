#!/usr/bin/env python3
"""Map fixturedownload team names to football-data names, from the data rather than by hand.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/pitch/fd_names.py

Every played match in a fixturedownload feed is paired with the football-data result in the same
league on the same day (one day either side, for UTC against London dates) with the same score. Each
pairing is a vote for home name -> home name and away name -> away name; the winner needs at least
two votes and three quarters of them. Writes pitch/fixturedownload-names.json ("DIV|fd name" ->
football-data name, the apisports-names.json format) and lists any team left unmapped. Re-run when a
promoted side's first matches are in both feeds.
"""
import json
import os
import sys
from collections import Counter, defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixturedownload-names.json")


def votes_for(div):
    p = D.CACHE + "fixturedownload-%s.json" % div
    res = D.load_results((div,))
    if not os.path.exists(p) or res.empty:
        return {}, set(), set(), set()
    res = res[res["Date"] >= res["Date"].max() - pd.Timedelta(days=400)]
    by_key = defaultdict(list)
    for _, r in res.iterrows():
        by_key[(r["Date"].normalize(), r["FTHG"], r["FTAG"])].append((r["HomeTeam"], r["AwayTeam"]))
    votes = defaultdict(Counter)
    teams = set()
    for m in json.load(open(p)):
        teams.update((m["HomeTeam"], m["AwayTeam"]))
        if m.get("HomeTeamScore") is None:
            continue
        day = pd.Timestamp(m["DateUtc"].replace("Z", "")).tz_localize("UTC").tz_convert("Europe/London").tz_localize(None).normalize()
        cands = []
        for off in (0, -1, 1):
            cands += by_key.get((day + pd.Timedelta(days=off), m["HomeTeamScore"], m["AwayTeamScore"]), [])
        if len(cands) == 1:
            votes[m["HomeTeam"]][cands[0][0]] += 1
            votes[m["AwayTeam"]][cands[0][1]] += 1
        else:
            # Several matches that day with this score: vote only where one name is already the same in both.
            for h, a in cands:
                if h == m["HomeTeam"] or a == m["AwayTeam"]:
                    votes[m["HomeTeam"]][h] += 1; votes[m["AwayTeam"]][a] += 1
    cur = res[res["Date"] >= pd.Timestamp("20%s-07-01" % D.season_codes(1)[0][:2])]
    return votes, teams, set(res["HomeTeam"]) | set(res["AwayTeam"]), set(cur["HomeTeam"]) | set(cur["AwayTeam"])


def main():
    out, missing = {}, []
    for div in D.FD_SLUGS:
        votes, teams, known, current = votes_for(div)
        left = []
        for t in sorted(teams):
            c = votes.get(t)
            if c:
                name, n = c.most_common(1)[0]
                if n >= 2 and n >= 0.75 * sum(c.values()):
                    if name != t:
                        out["%s|%s" % (div, t)] = name
                    continue
            if t in D.FD_NAMES:
                out["%s|%s" % (div, t)] = D.FD_NAMES[t]
            elif t not in known:
                left.append((t, c))
        # One side each left over this season: they are the same club, by elimination.
        got = {out.get("%s|%s" % (div, t), t) for t in teams}
        spare = sorted(current - got)
        if len(left) == 1 and len(spare) == 1:
            out["%s|%s" % (div, left[0][0])] = spare[0]
            print("by elimination", div, left[0][0], "->", spare[0])
            left = []
        missing += ["%s|%s %s" % (div, t, dict(c) if c else "no votes") for t, c in left]
        dup = [n for n, k in Counter(out.get("%s|%s" % (div, t), t) for t in teams).items() if k > 1]
        if dup or (current and current - {out.get("%s|%s" % (div, t), t) for t in teams}):
            missing.append("%s not one-to-one: duplicates %s, season teams without a calendar name %s"
                           % (div, dup, sorted(current - {out.get("%s|%s" % (div, t), t) for t in teams})))
    json.dump(dict(sorted(out.items())), open(OUT, "w"), indent=1, ensure_ascii=False)
    print("mapped", len(out), "renames; unmapped", len(missing))
    for m in missing:
        print("  unmapped", m)


if __name__ == "__main__":
    main()
