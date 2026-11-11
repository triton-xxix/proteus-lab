"""P-0412: how old was harvested code on the night it was queued as a probe?

Reads field-notes/harvest.jsonl (rows with a probe_id) and state/probes.json (the verdicts). GitHub rows
carry meta.created; a row from another source whose url is a GitHub repo is looked up keyless on the
GitHub API. Nothing is fetched but those repo records.
"""
import json
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import date

ROOT = "/Users/triton/PROTEUS"
REPO = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


def created_from_api(owner, repo):
    req = urllib.request.Request("https://api.github.com/repos/%s/%s" % (owner, repo), headers={"User-Agent": "repo-age-check"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=30)).get("created_at", "")[:10], ""
    except urllib.error.HTTPError as e:
        return "", "HTTP %d" % e.code
    except Exception as e:  # noqa: BLE001
        return "", type(e).__name__


def main(out_path):
    probes = {p["id"]: p for p in json.load(open(ROOT + "/state/probes.json"))["items"]}
    rows = [json.loads(line) for line in open(ROOT + "/field-notes/harvest.jsonl") if line.strip()]
    queued = [r for r in rows if r.get("probe_id")]
    out_rows, api_calls, api_errors = [], 0, []
    for r in queued:
        meta = r.get("meta") or {}
        created, how, repo = "", "", ""
        if r.get("source") == "github":
            created, how, repo = (meta.get("created") or "")[:10], "register", r["key"][3:]
        else:
            m = REPO.search(r.get("url") or "")
            if m:
                repo = "%s/%s" % (m.group(1), m.group(2).removesuffix(".git"))
                created, err = created_from_api(*repo.split("/"))
                api_calls += 1
                how = "api" if created else "api failed: " + err
                if err:
                    api_errors.append(repo + " " + err)
                time.sleep(1)
        age = (date.fromisoformat(r["date"]) - date.fromisoformat(created)).days if created else None
        p = probes.get(r["probe_id"], {})
        out_rows.append({"h": r["id"], "probe": r["probe_id"], "queued": r["date"], "source": r.get("source"), "repo": repo,
                         "created": created, "how": how, "age_days": age, "stars": meta.get("stars"),
                         "status": p.get("status"), "verdict": p.get("verdict"), "needs": p.get("needs", "")})

    dated = [x for x in out_rows if x["age_days"] is not None]

    def split(rs):
        v = {}
        for x in rs:
            k = x["verdict"] or ("open:" + str(x["status"]))
            v[k] = v.get(k, 0) + 1
        return dict(sorted(v.items()))

    young = [x for x in dated if x["age_days"] < 14]
    old = [x for x in dated if x["age_days"] >= 14]
    week = [x for x in dated if x["age_days"] < 7]
    by_source = {}
    for x in out_rows:
        s = by_source.setdefault(x["source"], {"queued": 0, "with_repo_age": 0, "under_14": 0})
        s["queued"] += 1
        if x["age_days"] is not None:
            s["with_repo_age"] += 1
            s["under_14"] += x["age_days"] < 14
    ages = sorted(x["age_days"] for x in dated)
    summary = {
        "register_rows": len(rows), "queued_as_probe": len(queued), "first_queued": min(r["date"] for r in queued),
        "last_queued": max(r["date"] for r in queued), "with_a_repo_age": len(dated), "no_repo": len(out_rows) - len(dated),
        "under_7_days": len(week), "under_14_days": len(young), "share_under_14_of_dated": round(len(young) / len(dated), 3),
        "share_under_14_of_all_queued": round(len(young) / len(queued), 3),
        "median_age_days": statistics.median(ages), "quartiles": [ages[len(ages) // 4], ages[len(ages) // 2], ages[3 * len(ages) // 4]],
        "verdicts_under_14": split(young), "verdicts_14_plus": split(old), "verdicts_no_repo": split([x for x in out_rows if x["age_days"] is None]),
        "by_source": by_source, "api_calls": api_calls, "api_errors": api_errors,
    }
    json.dump({"summary": summary, "rows": out_rows}, open(out_path, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
