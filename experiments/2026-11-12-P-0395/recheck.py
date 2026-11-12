"""P-0395: 48-hour recheck of the 35 tiny repos whose ids P-0394 saved on 10 Nov 12:44Z.

For each numeric id: GET api.github.com/repositories/ID keyless (35 calls, under the 60 an hour limit).
404 or 451 or a 'disabled' flag counts as gone. For the ones still up, read README.md as plain text and
compare its sha256 with the saved one. Read-only: nothing linked is fetched, nothing is run. Only counts
go to results.json here; ids and per-repo rows stay in sandbox/ (gitignored), since a regex match proves
nothing about one repo.
"""
import hashlib
import json
import pathlib
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).parent
IDS = pathlib.Path("/Users/triton/PROTEUS/sandbox/p0394-ids.json")
ROWS = pathlib.Path("/Users/triton/PROTEUS/sandbox/p0395-rows.json")
UA = {"User-Agent": "proteus-research/1.0", "Accept": "application/vnd.github+json"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)


base = json.loads(IDS.read_text())
rows, rate_limited = [], 0
for r in base["repos"]:
    row = {"id": r["id"], "match": bool(r["paste"] and r["run_inject"]), "paste": r["paste"],
           "stars_then": r["stars"], "status": None, "readme": None, "stars_now": None}
    try:
        d = json.loads(get("https://api.github.com/repositories/%d" % r["id"]).read())
        row["status"] = "disabled" if d.get("disabled") else ("private" if d.get("private") else "up")
        row["stars_now"] = d.get("stargazers_count")
        row["archived"] = d.get("archived")
        if row["status"] == "up":
            try:
                t = get("https://raw.githubusercontent.com/%s/%s/README.md" % (d["full_name"], d["default_branch"])
                        ).read().decode("utf-8", "replace")
                row["readme"] = "same" if hashlib.sha256(t.encode()).hexdigest() == r["readme_sha256"] else "changed"
            except urllib.error.HTTPError as e:
                # the baseline hashed an empty string when the README was missing
                row["readme"] = "same" if r["readme_sha256"] == hashlib.sha256(b"").hexdigest() else "missing now (%d)" % e.code
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:200]
        if e.code in (403, 429) and "rate limit" in body.lower():
            row["status"] = "rate limited"
            rate_limited += 1
        else:
            row["status"] = "gone %d" % e.code
            row["reason"] = body
    rows.append(row)
    time.sleep(0.3)


def grp(sel):
    g = [x for x in rows if sel(x)]
    gone = [x for x in g if x["status"].startswith("gone") or x["status"] in ("disabled", "private")]
    up = [x for x in g if x["status"] == "up"]
    moves = [x["stars_now"] - x["stars_then"] for x in up if x["stars_now"] is not None]
    return {"n": len(g), "gone": len(gone), "gone_codes": sorted(x["status"] for x in gone), "up": len(up),
            "readme_changed": sum(x["readme"] == "changed" for x in up),
            "readme_missing_now": sum(str(x["readme"]).startswith("missing") for x in up),
            "archived": sum(bool(x.get("archived")) for x in up),
            "stars_fell": sum(m < 0 for m in moves), "stars_rose": sum(m > 0 for m in moves),
            "median_star_move": sorted(moves)[len(moves) // 2] if moves else None}


res = {"baseline_at": base["run_at"], "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
       "rate_limited": rate_limited, "all": grp(lambda x: True),
       "paste_and_run_matches": grp(lambda x: x["match"]), "others": grp(lambda x: not x["match"]),
       "paste_link_any": grp(lambda x: x["paste"]), "no_paste_link": grp(lambda x: not x["paste"])}
ROWS.write_text(json.dumps(rows, indent=1))
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
