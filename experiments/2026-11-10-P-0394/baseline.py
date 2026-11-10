"""P-0394: P-0386's detection-side count rerun, plus an id baseline for a 48-hour takedown recheck.

Same search, regexes and README read as experiments/2026-11-09-P-0386/count.py (read-only, never fetches a linked file).
Counts go to results.json beside this script (committed). The numeric repo ids and a README hash of every tiny
(<50 KB) repo go to /Users/triton/PROTEUS/sandbox/p0394-ids.json only (gitignored), so no name is published and the
recheck can ask the API by id whether each repo still exists and whether its README changed.
"""
import hashlib
import json
import pathlib
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

HERE = pathlib.Path(__file__).parent
IDS = pathlib.Path("/Users/triton/PROTEUS/sandbox/p0394-ids.json")
UA = {"User-Agent": "proteus-research/1.0", "Accept": "application/vnd.github+json"}
PASTE = re.compile(r"telegra\.ph|pastebin\.com|rentry\.co|mega\.nz|mediafire\.com|t\.me/|bit\.ly|tinyurl\.com|cutt\.ly", re.I)
BIN = re.compile(r"\.exe\b|\.msi\b|\.scr\b|\.bat\b|\bdownload\b.{0,40}\.(zip|rar|7z)\b", re.I)
RUN = re.compile(r"\brun\b.{0,40}\.exe|\binject\b|disable.{0,20}(antivirus|defender)|password\s*[:=]", re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


now = datetime.now(timezone.utc)
since = (now - timedelta(days=3)).strftime("%Y-%m-%d")
items = []
for page in range(1, 6):
    d = json.loads(get(f"https://api.github.com/search/repositories?q=created:>{since}+stars:>=50&sort=stars&order=desc&per_page=100&page={page}"))
    if page == 1:
        total = d["total_count"]
    items += d["items"]
    if len(d["items"]) < 100:
        break
    time.sleep(7)

rows, keep, readme_fail = [], [], 0
for it in items:
    try:
        t = get(f"https://raw.githubusercontent.com/{it['full_name']}/{it['default_branch']}/README.md").decode("utf-8", "replace")
    except urllib.error.HTTPError:
        readme_fail += 1
        t = ""
    r = {"size_kb": it["size"], "stars": it["stargazers_count"], "paste": bool(PASTE.search(t)), "binary": bool(BIN.search(t)),
         "run_inject": bool(RUN.search(t))}
    rows.append(r)
    if it["size"] < 50:
        keep.append({"id": it["id"], "created_at": it["created_at"], "readme_sha256": hashlib.sha256(t.encode()).hexdigest(),
                     "paste": r["paste"], "run_inject": r["run_inject"], "stars": it["stargazers_count"]})
    time.sleep(0.15)


def n(f):
    return sum(1 for r in rows if f(r))


res = {"run_at": now.isoformat(timespec="seconds"), "since": since, "search_total": total, "fetched": len(rows),
       "readme_missing": readme_fail, "under_50kb": n(lambda r: r["size_kb"] < 50), "paste": n(lambda r: r["paste"]),
       "tiny_and_paste": n(lambda r: r["size_kb"] < 50 and r["paste"]),
       "tiny_paste_and_run": n(lambda r: r["size_kb"] < 50 and r["paste"] and r["run_inject"]),
       "large_and_paste": n(lambda r: r["size_kb"] >= 50 and r["paste"]), "ids_saved": len(keep),
       "ids_saved_to": "sandbox/p0394-ids.json (gitignored)"}
IDS.write_text(json.dumps({"run_at": res["run_at"], "repos": keep}, indent=1))
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
