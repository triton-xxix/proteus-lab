#!/usr/bin/env python3
"""P-0142: new-term-radar's GitHub breakout rule, keyless.

Rule (from the repo README as harvested): a repo under 14 days old averaging 200+ stars a day.
GitHub search API, unauthenticated (10 requests a minute, 1000 results a query), repos created in
the last 14 days with at least 200 stars, sorted by stars. Also pulls the Hugging Face trending top
50 (keyless) and saves both, so a later night can diff.
Usage: radar.py OUTDIR
"""
import datetime as dt
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "proteus-nightly/1.0", "Accept": "application/vnd.github+json"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    since = (now - dt.timedelta(days=14)).strftime("%Y-%m-%d")
    q = "created:>=%s stars:>=200" % since
    repos = []
    pages = 0
    for page in range(1, 11):
        url = ("https://api.github.com/search/repositories?q=%s&sort=stars&order=desc&per_page=100&page=%d"
               % (urllib.parse.quote(q), page))
        try:
            data = get(url)
        except Exception as e:  # noqa: BLE001
            print("page %d failed: %s" % (page, e))
            break
        pages += 1
        items = data.get("items", [])
        total = data.get("total_count")
        for it in items:
            created = dt.datetime.strptime(it["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            age_days = max((now - created).total_seconds() / 86400, 1.0)
            repos.append({
                "full_name": it["full_name"], "stars": it["stargazers_count"],
                "created_at": it["created_at"], "age_days": round(age_days, 2),
                "stars_per_day": round(it["stargazers_count"] / age_days, 1),
                "language": it.get("language"), "description": (it.get("description") or "")[:120],
                "fork": it.get("fork", False),
            })
        if len(items) < 100:
            break
        time.sleep(7)
    flagged = [r for r in repos if r["stars_per_day"] >= 200]
    flagged.sort(key=lambda r: -r["stars_per_day"])
    print("query: %s  total_count %s  fetched %d repos over %d pages" % (q, total, len(repos), pages))
    print("200+ stars a day: %d" % len(flagged))
    for r in flagged:
        print("  %-45s %6d stars %5.1f d  %6.1f/day  %s" % (r["full_name"], r["stars"], r["age_days"],
                                                           r["stars_per_day"], r["language"]))
    hf = []
    try:
        hf = get("https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=50")
        hf = [{"id": m.get("id") or m.get("modelId"), "likes": m.get("likes"),
               "downloads": m.get("downloads"), "createdAt": m.get("createdAt")} for m in hf]
        print("huggingface trending: %d models" % len(hf))
    except Exception as e:  # noqa: BLE001
        print("huggingface trending failed: %s" % e)
    json.dump({"asof": now.isoformat(), "query": q, "total_count": total, "fetched": len(repos),
               "flagged_200_per_day": flagged, "all": repos, "hf_trending": hf},
              open(out / "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
