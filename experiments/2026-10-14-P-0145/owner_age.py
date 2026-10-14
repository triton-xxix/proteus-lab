#!/usr/bin/env python3
"""P-0145 fallback: GET /repos/{o}/{r}/stargazers returns 401 unauthenticated (both media types, tested
14 Oct 2026 12:40Z), so stargazer account age is out of reach keyless. /users/{login} still answers, so
the nearest keyless proxy is the repo OWNER's account age, followers and public repo count, for the
suspicious slice and the two controls. Flag: owner account under 60 days old. One core call per repo."""
import datetime as dt
import json
import time
import urllib.request

UA = {"User-Agent": "proteus-nightly/1.0", "Accept": "application/vnd.github+json"}
P = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0145/results.json"
R = json.load(open(P))
now = dt.datetime.now(dt.timezone.utc)
by_name = {r["full_name"]: r for r in R["flagged_tonight"]}
for c in R["farm_checks"]:
    owner = c["repo"].split("/")[0]
    req = urllib.request.Request("https://api.github.com/users/%s" % owner, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            u = json.loads(r.read().decode("utf-8")); rem = r.headers.get("X-RateLimit-Remaining")
    except Exception as e:  # noqa: BLE001
        c["owner_error"] = str(e)[:80]; continue
    created = dt.datetime.strptime(u["created_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    age = round((now - created).total_seconds() / 86400, 1)
    c["owner"] = {"login": owner, "type": u.get("type"), "account_age_days": age, "followers": u.get("followers"),
                  "public_repos": u.get("public_repos")}
    c["owner_flag"] = age < 60
    repo = by_name.get(c["repo"], {})
    print("%-40s %-12s owner %5.0f d  followers %6s  repos %4s  flag %-5s %s  (repo %s stars, %s/day)  [remaining %s]" % (
        c["repo"], u.get("type"), age, u.get("followers"), u.get("public_repos"), c["owner_flag"],
        "CONTROL" if c["control"] else "", repo.get("stars"), repo.get("stars_per_day"), rem), flush=True)
    time.sleep(0.5)
flagged = sorted(c["repo"] for c in R["farm_checks"] if c.get("owner_flag") and not c["control"])
surv = [n for n in R["of_54"]["survivors"] if n not in flagged]
R["of_54"]["owner_age_flagged"] = flagged
R["of_54"]["survive_after_owner_age"] = len(surv)
R["of_54"]["survivors_after_owner_age"] = surv
R["stargazers_endpoint"] = "401 Unauthorized keyless, both media types; owner account age used instead"
json.dump(R, open(P, "w"), indent=1)
print("of 54: after cap %d, owner-age flagged %d, survive %d" % (R["of_54"]["of_54_after_cap"], len(flagged), len(surv)))
