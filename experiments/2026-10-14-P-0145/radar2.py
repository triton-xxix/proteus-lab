#!/usr/bin/env python3
"""P-0145: new-term-radar night two. Re-run P-0142's GitHub rule, then apply what the first night said
the radar needs: one repo per owner, no forks, a star-farm check (stargazer account age plus the
timing of the first 100 stars) on the suspicious slice, and the Hugging Face trending diff against
13 Oct. Keyless. The core API allows 60 calls an hour unauthenticated, so the farm check is budgeted
and reads X-RateLimit-Remaining as it goes.
Usage: radar2.py OUTDIR
"""
import datetime as dt
import json
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "proteus-nightly/1.0", "Accept": "application/vnd.github+json"}
STAR_UA = {"User-Agent": "proteus-nightly/1.0", "Accept": "application/vnd.github.star+json"}
PREV = "/Users/triton/PROTEUS/experiments/2026-10-13-P-0142/results.json"
SUSPECT = re.compile(r"(pc\b|_pc|port|mobile|gta|driver|nsfw|release|bloodborne|d2r|crack|cheat|hack|free|download|apk)", re.I)
CORE_BUDGET = 44          # core calls this script may spend (60/h unauthenticated, keep a margin)
SAMPLE_USERS = 5          # stargazer accounts to age-check per repo
core = {"used": 0, "remaining": None, "stopped": False}


def get(url, headers=UA, core_call=False):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as r:
        if core_call:
            core["used"] += 1
            rem = r.headers.get("X-RateLimit-Remaining")
            core["remaining"] = int(rem) if rem is not None else None
        return json.loads(r.read().decode("utf-8"))


def parse(ts):
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def search(now):
    since = (now - dt.timedelta(days=14)).strftime("%Y-%m-%d")
    q = "created:>=%s stars:>=200" % since
    repos, total = [], None
    for page in range(1, 11):
        url = ("https://api.github.com/search/repositories?q=%s&sort=stars&order=desc&per_page=100&page=%d"
               % (urllib.parse.quote(q), page))
        try:
            data = get(url)
        except Exception as e:  # noqa: BLE001
            print("page %d failed: %s" % (page, e), flush=True)
            break
        items = data.get("items", [])
        total = data.get("total_count")
        for it in items:
            age_days = max((now - parse(it["created_at"])).total_seconds() / 86400, 1.0)
            repos.append({"full_name": it["full_name"], "owner": it["owner"]["login"], "stars": it["stargazers_count"],
                          "created_at": it["created_at"], "age_days": round(age_days, 2),
                          "stars_per_day": round(it["stargazers_count"] / age_days, 1),
                          "language": it.get("language"), "description": (it.get("description") or "")[:120],
                          "fork": it.get("fork", False)})
        if len(items) < 100:
            break
        time.sleep(7)
    return q, total, repos


def farm_check(full_name, now):
    """One stargazers call (first 100 stars with starred_at) plus SAMPLE_USERS profile calls."""
    rec = {"repo": full_name}
    if core["remaining"] is not None and core["remaining"] < SAMPLE_USERS + 2:
        rec["skipped"] = "rate limit"; return rec
    if core["used"] + SAMPLE_USERS + 1 > CORE_BUDGET:
        rec["skipped"] = "budget"; return rec
    try:
        stars = get("https://api.github.com/repos/%s/stargazers?per_page=100&page=1" % full_name, STAR_UA, True)
    except Exception as e:  # noqa: BLE001
        rec["error"] = str(e)[:100]; return rec
    times = sorted(parse(s["starred_at"]) for s in stars if s.get("starred_at"))
    if len(times) >= 2:
        rec["first100_span_h"] = round((times[-1] - times[0]).total_seconds() / 3600, 2)
        rec["first100_n"] = len(times)
    logins = [s["user"]["login"] for s in stars if s.get("user")]
    step = max(len(logins) // SAMPLE_USERS, 1)
    ages, sampled = [], []
    for login in logins[::step][:SAMPLE_USERS]:
        try:
            u = get("https://api.github.com/users/%s" % login, UA, True)
        except Exception as e:  # noqa: BLE001
            rec.setdefault("user_errors", []).append(str(e)[:60]); continue
        age = (now - parse(u["created_at"])).total_seconds() / 86400
        ages.append(round(age, 1))
        sampled.append({"login": login, "account_age_days": round(age, 1), "followers": u.get("followers"),
                        "public_repos": u.get("public_repos")})
        time.sleep(0.5)
    rec["sampled"] = sampled
    if ages:
        rec["median_account_age_days"] = statistics.median(ages)
        rec["under_30d"] = sum(a < 30 for a in ages)
        rec["farmed"] = rec["median_account_age_days"] < 90 or rec["under_30d"] >= 3
    return rec


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    prev = json.load(open(PREV))
    prev54 = {r["full_name"]: r for r in prev["flagged_200_per_day"]}
    q, total, repos = search(now)
    tonight = {r["full_name"]: r for r in repos}
    flagged = sorted([r for r in repos if r["stars_per_day"] >= 200], key=lambda r: -r["stars_per_day"])
    print("tonight: query %s total %s fetched %d flagged %d" % (q, total, len(repos), len(flagged)), flush=True)

    # the 54 from 13 Oct, step by step
    steps = {}
    still = [prev54[n] for n in prev54 if n in tonight and tonight[n]["stars_per_day"] >= 200]
    aged_out = [n for n in prev54 if n not in tonight]
    fell = [n for n in prev54 if n in tonight and tonight[n]["stars_per_day"] < 200]
    steps["of_54_still_200_per_day"] = len(still)
    steps["of_54_not_in_search"] = aged_out
    steps["of_54_fell_below_200"] = fell
    still_t = sorted([tonight[r["full_name"]] for r in still], key=lambda r: -r["stars_per_day"])
    nofork = [r for r in still_t if not r["fork"]]
    steps["of_54_forks_removed"] = [r["full_name"] for r in still_t if r["fork"]]
    seen, capped, dropped_cap = set(), [], []
    for r in nofork:                       # sorted by stars_per_day desc, so the first per owner is the best
        if r["owner"] in seen:
            dropped_cap.append(r["full_name"]); continue
        seen.add(r["owner"]); capped.append(r)
    steps["of_54_owner_cap_removed"] = dropped_cap
    steps["of_54_after_cap"] = len(capped)

    # farm check: the suspicious slice of the capped survivors, plus two controls from the clean top
    suspicious = [r for r in capped if SUSPECT.search(r["full_name"] + " " + r["description"]) or r["language"] is None]
    controls = [r for r in capped if r not in suspicious][:2]
    checks = []
    for r in suspicious + controls:
        c = farm_check(r["full_name"], now); c["control"] = r in controls; checks.append(c)
        print("  farm %-40s span %s h  median age %s d  under30 %s  farmed %s  %s  [core used %d, remaining %s]" % (
            r["full_name"], c.get("first100_span_h"), c.get("median_account_age_days"), c.get("under_30d"),
            c.get("farmed"), "CONTROL" if c["control"] else "", core["used"], core["remaining"]), flush=True)
    farmed = {c["repo"] for c in checks if c.get("farmed") and not c["control"]}
    survivors = [r for r in capped if r["full_name"] not in farmed]
    steps["suspicious_slice"] = [r["full_name"] for r in suspicious]
    steps["farm_flagged"] = sorted(farmed)
    steps["farm_unchecked"] = [c["repo"] for c in checks if c.get("skipped") or c.get("error")]
    steps["of_54_survive"] = len(survivors)
    steps["survivors"] = [r["full_name"] for r in survivors]

    # tonight's own set, same filters minus the farm check
    t_nofork = [r for r in flagged if not r["fork"]]
    t_seen, t_capped = set(), []
    for r in t_nofork:
        if r["owner"] in t_seen: continue
        t_seen.add(r["owner"]); t_capped.append(r)
    tonight_steps = {"flagged": len(flagged), "no_fork": len(t_nofork), "after_owner_cap": len(t_capped),
                     "new_since_13oct": [r["full_name"] for r in flagged if r["full_name"] not in prev54]}

    # Hugging Face diff
    hf_prev = {m["id"] for m in prev.get("hf_trending", [])}
    hf = []
    try:
        hf_raw = get("https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=50")
        hf = [{"id": m.get("id") or m.get("modelId"), "likes": m.get("likes"), "downloads": m.get("downloads"),
               "createdAt": m.get("createdAt")} for m in hf_raw]
    except Exception as e:  # noqa: BLE001
        print("huggingface failed: %s" % e)
    hf_now = {m["id"] for m in hf}
    hf_diff = {"prev": len(hf_prev), "now": len(hf_now), "kept": len(hf_prev & hf_now),
               "entered": sorted(hf_now - hf_prev), "left": sorted(hf_prev - hf_now)}

    print(json.dumps({"of_54": {k: (v if isinstance(v, int) else len(v)) for k, v in steps.items()},
                      "tonight": {k: (v if isinstance(v, int) else len(v)) for k, v in tonight_steps.items()},
                      "hf": {k: (v if isinstance(v, int) else len(v)) for k, v in hf_diff.items()},
                      "core_calls": core["used"], "core_remaining": core["remaining"]}), flush=True)
    json.dump({"asof": now.isoformat(), "query": q, "total_count": total, "fetched": len(repos),
               "of_54": steps, "tonight": tonight_steps, "flagged_tonight": flagged, "farm_checks": checks,
               "hf_diff": hf_diff, "hf_trending": hf, "core": core}, open(out / "results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
