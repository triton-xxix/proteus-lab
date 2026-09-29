"""Team briefs before a blind call: current head coach from Wikipedia, last six results and Elo
from eloratings.net. Keyless. Prints one block per team for every fixture not yet in the book,
or for the teams named on the command line. The point is to stop calling on stale memory
(Germany's coach was wrong on 2026-09-29 until a web check).
  brief.py                   teams in fixtures not yet in JUDGEMENT.csv (needs The Odds API events, no quota)
  brief.py Germany Greece    named teams
"""
import re, sys, os, json, time, urllib.request, urllib.parse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "proteus-lab (github.com/triton-xxix/proteus-lab)"}
WIKI = {"Republic of Ireland": "Republic of Ireland national football team", "Czech Republic": "Czech Republic national football team",
        "Bosnia & Herzegovina": "Bosnia and Herzegovina national football team", "United States": "United States men's national soccer team"}
ALIAS = {"Republic of Ireland": "Ireland", "Czech Republic": "Czechia", "North Macedonia": "Macedonia", "Bosnia & Herzegovina": "Bosnia and Herzegovina"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8")


def coach(team):
    page = WIKI.get(team, "%s national football team" % team)
    q = urllib.parse.urlencode({"action": "parse", "page": page, "prop": "wikitext", "format": "json", "formatversion": "2", "redirects": "1"})
    w = None
    for wait in (0, 5, 20):
        time.sleep(wait + 1.2)  # Wikipedia returns 429 after about twenty quick calls; pace and back off
        try:
            w = json.loads(get("https://en.wikipedia.org/w/api.php?" + q))["parse"]["wikitext"]
            break
        except Exception as e:
            err = e
    if w is None:
        return "coach: lookup failed (%s)" % err
    for k in ("head coach", "coach", "manager"):
        m = re.search(r"\|\s*%s\s*=\s*(.+)" % k, w, re.I)
        if m:
            v = re.sub(r"\[\[([^|\]]*\|)?([^\]]+)\]\]", r"\2", m.group(1))
            v = re.sub(r"<[^>]+>|\{\{[^}]*\}\}", "", v).strip()
            return "coach: %s (Wikipedia infobox)" % v
    return "coach: not found in infobox"


def elo_tables():
    names = {}
    for line in get("https://www.eloratings.net/en.teams.tsv").splitlines():
        p = line.split("\t")
        for n in p[1:]:
            if n:
                names.setdefault(n, p[0])
    rating = {}
    for line in get("https://www.eloratings.net/World.tsv").splitlines():
        p = line.split("\t")
        if len(p) > 3:
            rating[p[2]] = (p[0], p[3])
    results = []
    for line in get("https://www.eloratings.net/latest.tsv").splitlines():
        p = line.split("\t")
        if len(p) >= 7 and p[5].isdigit():
            results.append(("%s-%s-%s" % (p[0], p[1], p[2]), p[3], p[4], int(p[5]), int(p[6])))
    code2name = {}
    for n, c in names.items():
        code2name.setdefault(c, n)
    return names, rating, results, code2name


def brief(team, names, rating, results, code2name):
    c = names.get(ALIAS.get(team, team))
    out = ["## %s" % team, coach(team)]
    if not c:
        out.append("elo: team code not found")
        return "\n".join(out)
    rk, rt = rating.get(c, ("?", "?"))
    out.append("elo: %s, world rank %s" % (rt, rk))
    mine = [r for r in results if c in (r[1], r[2])]
    mine.sort(reverse=True)
    for d, h, a, hg, ag in mine[:6]:
        opp = code2name.get(a if h == c else h, a if h == c else h)
        gf, ga = (hg, ag) if h == c else (ag, hg)
        out.append("  %s %s %d-%d %s (%s)" % (d, "v" if h == c else "at", gf, ga, opp, "W" if gf > ga else "D" if gf == ga else "L"))
    return "\n".join(out)


def main(argv):
    teams = argv
    if not teams:
        sys.path.insert(0, HERE)
        import judgement
        rows = judgement.load()
        have = {(r["home"], r["away"], r["kickoff_utc"]) for r in rows}
        teams = []
        for ko, h, a, s in sorted(judgement.events(judgement.key())):
            if (h, a, ko) not in have:
                for t in (h, a):
                    if t not in teams:
                        teams.append(t)
    names, rating, results, code2name = elo_tables()
    print("# Team briefs, %s\n" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%MZ"))
    for t in teams:
        print(brief(t, names, rating, results, code2name))
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
