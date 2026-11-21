"""P-0519: what changed in alphagov/e-petitions around Jan to Feb 2022?

Keyless GitHub REST API: commits between SINCE and UNTIL (all pages, 100 per page), each message's
first line, flagged when it names constituencies, postcodes, ONS, geography or signature counting.

    python3 commits.py
"""
import json, re, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SINCE, UNTIL = "2021-11-01T00:00:00Z", "2022-04-01T00:00:00Z"
UA = {"User-Agent": "proteus-lab-check/1.0", "Accept": "application/vnd.github+json"}
PAT = re.compile(r"constituen|postcode|ons\b|geograph|mapit|boundar|signature.?count|count|backfill|location|region", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r), r.headers.get("X-RateLimit-Remaining")


def main():
    rows, page, left = [], 1, None
    while page <= 5:
        data, left = get("https://api.github.com/repos/alphagov/e-petitions/commits?since=%s&until=%s&per_page=100&page=%d" % (SINCE, UNTIL, page))
        if not data:
            break
        for c in data:
            msg = c["commit"]["message"]
            rows.append({"sha": c["sha"][:10], "date": c["commit"]["author"]["date"][:10],
                         "first": msg.splitlines()[0][:120], "flag": bool(PAT.search(msg))})
        page += 1
        time.sleep(0.5)
    flagged = [r for r in rows if r["flag"]]
    out = {"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "window": [SINCE, UNTIL],
           "commits": len(rows), "flagged": len(flagged), "ratelimit_left": left, "rows": rows}
    (HERE / "results.json").write_text(json.dumps(out, indent=1))
    print("commits", len(rows), "flagged", len(flagged), "ratelimit left", left)
    for r in rows:
        print(("*" if r["flag"] else " "), r["date"], r["sha"], r["first"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
