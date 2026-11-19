"""P-0493: do the most-starred MCP server repos ship releases?

1. GitHub search: topic:mcp-server pushed since 1 Nov 2026, sorted by stars, top 50.
2. releases/latest for each (404 = no published release).
Checks the unauthenticated core quota first and stops when it runs out.

    python3 releases.py

Keyless, read only, standard library.
"""
import json, statistics, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
HALT = Path("/Users/triton/PROTEUS/HALT")
H = {"User-Agent": "probe-script", "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
API = "https://api.github.com"


def get(url):
    req = urllib.request.Request(url, headers=H)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read()), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, None, dict(e.headers)


def main():
    if HALT.exists():
        print("HALT")
        return 1
    _, rl, _ = get(API + "/rate_limit")
    core = rl["resources"]["core"]
    print("core quota:", core["remaining"], "of", core["limit"], flush=True)
    st, s, _ = get(API + "/search/repositories?q=topic:mcp-server+pushed:%3E2026-11-01&sort=stars&order=desc&per_page=50")
    if st != 200:
        print("search refused:", st)
        return 1
    now = datetime.now(timezone.utc)
    rows, budget = [], core["remaining"] - 2
    for it in s["items"]:
        row = {"repo": it["full_name"], "stars": it["stargazers_count"], "pushed_at": it["pushed_at"],
               "archived": it.get("archived"), "language": it.get("language")}
        if budget <= 0:
            row["skipped"] = "quota"
            rows.append(row)
            continue
        st, rel, hdr = get(API + "/repos/" + it["full_name"] + "/releases/latest")
        budget -= 1
        if st == 200:
            pub = datetime.fromisoformat(rel["published_at"].replace("Z", "+00:00"))
            row["latest_release"] = rel.get("tag_name")
            row["published_at"] = rel["published_at"]
            row["days_since"] = round((now - pub).total_seconds() / 86400, 1)
        elif st == 404:
            row["no_release"] = True
        else:
            row["error"] = st
            if st in (403, 429):
                budget = 0
        rows.append(row)
        print(json.dumps(row), flush=True)
        time.sleep(0.4)

    asked = [r for r in rows if "skipped" not in r and "error" not in r]
    have = [r for r in asked if "days_since" in r]
    days = [r["days_since"] for r in have]
    summary = {
        "at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "search_total": s.get("total_count"),
        "repos": len(rows), "answered": len(asked),
        "skipped_or_error": len(rows) - len(asked),
        "release_in_30_days": sum(1 for d in days if d <= 30),
        "release_in_7_days": sum(1 for d in days if d <= 7),
        "release_older_than_30_days": sum(1 for d in days if d > 30),
        "no_release": sum(1 for r in asked if r.get("no_release")),
        "median_days_since_latest": statistics.median(days) if days else None,
        "max_days_since_latest": max(days) if days else None,
        "stars_min": min(r["stars"] for r in rows), "stars_max": max(r["stars"] for r in rows),
        "median_stars_with_release_30d": statistics.median([r["stars"] for r in have if r["days_since"] <= 30]) if have else None,
        "median_stars_no_release": statistics.median([r["stars"] for r in asked if r.get("no_release")]) if any(r.get("no_release") for r in asked) else None,
    }
    (HERE / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
