"""P-0276: code-link rot on the arXiv papers the harvester kept since 1 Oct 2026.

Fetches each abstract page (3 s apart, arXiv's asked-for pace), pulls github.com links from the
abstract and comments, then asks the GitHub API (keyless, 60 an hour) whether each repo answers.
Writes results.json. Run with python3 -I.
"""
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request

HARVEST = "/Users/triton/PROTEUS/field-notes/harvest.jsonl"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-31-P-0276/results.json"
UA = {"User-Agent": "proteus-probe (research, 1 req / 3 s)"}

papers = []
for line in open(HARVEST, encoding="utf-8"):
    r = json.loads(line)
    if r.get("source") == "arxiv" and r.get("keep") and r.get("date", "") >= "2026-10-01":
        papers.append((r["id"], r["key"].split(":", 1)[1], r["url"], r.get("title", "")))
print("papers", len(papers), flush=True)


def get(url, headers=UA, timeout=30):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


link_re = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
rows = []
for hid, aid, url, title in papers:
    rec = {"id": hid, "arxiv": aid, "title": title[:90], "abs_status": None, "github_links": [], "comments_hint": ""}
    try:
        st, body = get(url)
        rec["abs_status"] = st
        # abstract block and comments line only, not the page chrome
        m = re.search(r'<blockquote class="abstract[^"]*">(.*?)</blockquote>', body, re.S)
        abstract = html.unescape(m.group(1)) if m else ""
        c = re.search(r'<td class="tablecell comments[^"]*">(.*?)</td>', body, re.S)
        comments = html.unescape(c.group(1)) if c else ""
        rec["comments_hint"] = re.sub(r"<[^>]+>", "", comments)[:120]
        found = []
        for mm in link_re.finditer(abstract + " " + comments):
            owner, repo = mm.group(1), mm.group(2).rstrip(".,);")
            repo = re.sub(r"\.git$", "", repo)
            key = f"{owner}/{repo}"
            if key not in found:
                found.append(key)
        rec["github_links"] = found
    except Exception as e:  # noqa: BLE001
        rec["abs_error"] = f"{type(e).__name__}: {e}"[:120]
    rows.append(rec)
    print(hid, aid, rec["abs_status"], rec["github_links"], flush=True)
    time.sleep(3)

repos = {}
for rec in rows:
    for key in rec["github_links"]:
        if key in repos:
            continue
        try:
            st, body = get("https://api.github.com/repos/" + key, headers={**UA, "Accept": "application/vnd.github+json"})
            d = json.loads(body)
            repos[key] = {"status": st, "stars": d.get("stargazers_count"), "pushed_at": d.get("pushed_at"),
                          "archived": d.get("archived"), "redirected_to": d.get("full_name") if d.get("full_name", "").lower() != key.lower() else None}
        except urllib.error.HTTPError as e:
            repos[key] = {"status": e.code}
        except Exception as e:  # noqa: BLE001
            repos[key] = {"status": None, "error": f"{type(e).__name__}"}
        print(key, repos[key], flush=True)
        time.sleep(1)

with_code = [r for r in rows if r["github_links"]]
all_links = [k for r in rows for k in r["github_links"]]
dead = [k for k, v in repos.items() if v.get("status") != 200]
res = {"papers": len(rows), "abs_fetched": sum(1 for r in rows if r["abs_status"] == 200),
       "papers_with_github_link": len(with_code), "distinct_repos": len(repos),
       "repos_200": sum(1 for v in repos.values() if v.get("status") == 200), "repos_dead": dead,
       "repos_archived": [k for k, v in repos.items() if v.get("archived")],
       "stars": {k: v.get("stars") for k, v in repos.items() if v.get("status") == 200},
       "rows": rows, "repos": repos}
json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("rows", "repos", "stars")}, indent=1))
sys.exit(0)
