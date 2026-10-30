"""P-0262: star change on P-0145's 34 survivors, 14 Oct baseline v today, keyless GitHub REST."""
from __future__ import annotations

import json
import statistics
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

BASE = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0145/results.json"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-30-P-0262/results.json"
UA = {"User-Agent": "proteus-trials/1.0", "Accept": "application/vnd.github+json"}


def get(url: str):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read().decode()), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, None, dict(e.headers)


def main() -> None:
    d = json.load(open(BASE))
    survivors = d["of_54"]["survivors_after_owner_age"]
    suspicious = set(d["of_54"]["suspicious_slice"])
    baseline = {r["full_name"]: r for r in d["flagged_tonight"] if isinstance(r, dict)}
    # survivors not in the 14 Oct flagged list fall back to the 13 Oct P-0142 counts
    try:
        d13 = json.load(open("/Users/triton/PROTEUS/experiments/2026-10-13-P-0142/results.json"))
        for v in d13.values():
            if isinstance(v, list):
                for r in v:
                    if isinstance(r, dict) and "full_name" in r and "stars" in r:
                        baseline.setdefault(r["full_name"], dict(r, baseline_date="2026-10-13"))
    except Exception:  # noqa: BLE001
        pass
    rows = []
    remaining = None
    for name in survivors:
        b = baseline.get(name, {})
        status, body, hdr = get("https://api.github.com/repos/" + name)
        remaining = hdr.get("X-RateLimit-Remaining", remaining)
        now = body.get("stargazers_count") if body else None
        then = b.get("stars")
        row = {"repo": name, "suspicious": name in suspicious, "status": status, "stars_14oct": then,
               "stars_now": now, "stars_per_day_14oct": b.get("stars_per_day"),
               "created_at": body.get("created_at") if body else None,
               "pushed_at": body.get("pushed_at") if body else None,
               "archived": body.get("archived") if body else None,
               "renamed_to": body.get("full_name") if body and body.get("full_name") != name else None}
        if then and now is not None:
            row["change"] = now - then
            row["change_pct"] = round(100.0 * (now - then) / then, 1)
        rows.append(row)
        time.sleep(0.3)

    def slice_stats(flag: bool) -> dict:
        xs = [r for r in rows if r["suspicious"] == flag]
        ok = [r for r in xs if "change_pct" in r]
        return {"n": len(xs), "fetched": len(ok), "gone": sum(1 for r in xs if r["status"] == 404),
                "lost_stars": sum(1 for r in ok if r["change"] < 0),
                "median_change_pct": statistics.median([r["change_pct"] for r in ok]) if ok else None,
                "median_change_abs": statistics.median([r["change"] for r in ok]) if ok else None,
                "mean_change_pct": round(statistics.mean([r["change_pct"] for r in ok]), 1) if ok else None,
                "repos": {r["repo"]: r.get("change_pct") for r in xs}}

    out = {"asof": datetime.now(timezone.utc).isoformat(), "baseline_asof": d["asof"],
           "baseline_found_for": sum(1 for r in rows if r["stars_14oct"]),
           "rate_limit_remaining_after": remaining,
           "suspicious": slice_stats(True), "rest": slice_stats(False), "rows": rows}
    json.dump(out, open(OUT, "w"), indent=1)
    for k in ("asof", "baseline_found_for", "rate_limit_remaining_after"):
        print(k, out[k])
    for k in ("suspicious", "rest"):
        s = dict(out[k])
        s.pop("repos")
        print(k, s)
    for r in sorted(rows, key=lambda r: r.get("change_pct", -999)):
        print(r["suspicious"] and "S" or " ", r["status"], r["repo"], r["stars_14oct"], "->", r["stars_now"],
              r.get("change_pct"), r.get("renamed_to") or "")


if __name__ == "__main__":
    main()
