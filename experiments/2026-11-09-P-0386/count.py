"""Detection-side count, read-only. Of GitHub repos created in the last 3 days with 50 or more stars, how many are tiny and have a README
that sends the reader to a paste site or a binary? Reads the search API and each README as plain text. Never fetches a linked file.
Publishes counts only: repo names stay out of the results, since a pattern match is not proof about any one repo.
"""
import json
import pathlib
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

HERE = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0", "Accept": "application/vnd.github+json"}
PASTE = re.compile(r"telegra\.ph|pastebin\.com|rentry\.co|mega\.nz|mediafire\.com|t\.me/|bit\.ly|tinyurl\.com|cutt\.ly", re.I)
BIN = re.compile(r"\.exe\b|\.msi\b|\.scr\b|\.bat\b|\bdownload\b.{0,40}\.(zip|rar|7z)\b", re.I)
RUN = re.compile(r"\brun\b.{0,40}\.exe|\binject\b|disable.{0,20}(antivirus|defender)|password\s*[:=]", re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


since = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
items = []
for page in range(1, 6):
    q = f"created:>{since}+stars:>=50"
    d = json.loads(get(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=100&page={page}"))
    if page == 1:
        total = d["total_count"]
    items += d["items"]
    if len(d["items"]) < 100:
        break
    time.sleep(7)

rows = []
readme_fail = 0
for it in items:
    try:
        t = get(f"https://raw.githubusercontent.com/{it['full_name']}/{it['default_branch']}/README.md").decode("utf-8", "replace")
    except urllib.error.HTTPError:
        readme_fail += 1
        t = ""
    rows.append({"size_kb": it["size"], "stars": it["stargazers_count"], "forks": it["forks_count"], "lang": it["language"],
                 "paste": bool(PASTE.search(t)), "binary": bool(BIN.search(t)), "run_inject": bool(RUN.search(t)), "readme_len": len(t)})
    time.sleep(0.15)


def n(f):
    return sum(1 for r in rows if f(r))


res = {"since": since, "search_total": total, "fetched": len(rows), "readme_missing": readme_fail, "under_50kb": n(lambda r: r["size_kb"] < 50),
       "paste": n(lambda r: r["paste"]), "binary": n(lambda r: r["binary"]), "run_inject": n(lambda r: r["run_inject"]),
       "tiny_and_paste": n(lambda r: r["size_kb"] < 50 and r["paste"]), "tiny_and_binary": n(lambda r: r["size_kb"] < 50 and r["binary"]),
       "tiny_paste_and_run": n(lambda r: r["size_kb"] < 50 and r["paste"] and r["run_inject"]),
       "large_and_paste": n(lambda r: r["size_kb"] >= 50 and r["paste"]),
       "forks_ge_half_stars_tiny": n(lambda r: r["size_kb"] < 50 and r["forks"] >= r["stars"] * 0.5),
       "forks_ge_half_stars_rest": n(lambda r: r["size_kb"] >= 50 and r["forks"] >= r["stars"] * 0.5)}
(HERE / "results.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))
