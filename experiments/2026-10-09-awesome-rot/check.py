"""How much of a famous awesome list is dead, moved or archived? (Persona pick, 9 Oct 2026.)

Keyless. Fetches the raw README of a curated list, pulls every GitHub repo link, and GETs each repo
page without an API token: 404 = gone, a redirect to another owner/name = moved, the archived banner
in the HTML = archived. Non-GitHub links get one GET each and are classed by status.

usage: python3 check.py OWNER/REPO OUTDIR
"""
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.error
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (proteus awesome-rot check; one GET per link)"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl(), r.read(400_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, url, ""
    except Exception as e:  # DNS, TLS, timeout
        return None, url, type(e).__name__


def main():
    repo, outdir = sys.argv[1], sys.argv[2]
    readme = None
    for branch in ("master", "main"):
        st, _, body = get(f"https://raw.githubusercontent.com/{repo}/{branch}/README.md")
        if st == 200:
            readme = body
            break
    if readme is None:
        print("README not found")
        return 1
    links = re.findall(r"\]\((https?://[^)\s]+)\)", readme)
    gh, other = set(), set()
    for u in links:
        m = re.match(r"https?://github\.com/([^/#?]+)/([^/#?]+)/?$", u)
        if m and m.group(1) not in ("sponsors", "topics", "features", "orgs"):
            gh.add(f"{m.group(1)}/{m.group(2)}".removesuffix(".git"))
        elif "github.com" not in u:
            other.add(u)
    rows = []

    def check_gh(slug):
        st, final, body = get(f"https://github.com/{slug}")
        moved = st == 200 and final.rstrip("/").lower() != f"https://github.com/{slug}".lower()
        archived = "This repository was archived by the owner" in body
        return {"kind": "github", "link": slug, "status": st, "final": final,
                "moved": moved, "archived": archived}

    def check_other(u):
        st, final, err = get(u)
        return {"kind": "other", "link": u, "status": st, "final": final,
                "error": err if st is None else ""}

    t0 = time.time()
    with cf.ThreadPoolExecutor(8) as ex:
        rows += list(ex.map(check_gh, sorted(gh)))
        rows += list(ex.map(check_other, sorted(other)))
    g = [r for r in rows if r["kind"] == "github"]
    o = [r for r in rows if r["kind"] == "other"]
    summary = {
        "list": repo, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seconds": round(time.time() - t0, 1), "links_in_readme": len(links),
        "github_repos": len(g),
        "github_404": sum(r["status"] == 404 for r in g),
        "github_moved": sum(bool(r["moved"]) for r in g),
        "github_archived": sum(bool(r["archived"]) for r in g),
        "github_other_status": sum(r["status"] not in (200, 404) for r in g),
        "other_links": len(o),
        "other_ok": sum(r["status"] == 200 for r in o),
        "other_4xx": sum(r["status"] is not None and 400 <= r["status"] < 500 for r in o),
        "other_5xx": sum(r["status"] is not None and r["status"] >= 500 for r in o),
        "other_no_answer": sum(r["status"] is None for r in o),
    }
    name = repo.replace("/", "__")
    with open(f"{outdir}/{name}.rows.json", "w") as f:
        json.dump(rows, f, indent=1)
    with open(f"{outdir}/{name}.summary.json", "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
