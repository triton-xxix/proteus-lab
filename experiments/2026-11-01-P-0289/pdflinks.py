"""P-0289: P-0276's second pass. For the kept arXiv papers whose abstract linked no code, fetch the
PDF (export.arxiv.org, 3 s apart, browser user agent), pdftotext it, pull github.com/owner/repo
links and code-availability phrases, then ask the keyless GitHub API about each distinct repo.
Writes results.json beside this script. Run with python3 -I."""
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = Path("/Users/triton/PROTEUS/sandbox/arxiv-pdf")
SB.mkdir(parents=True, exist_ok=True)
P276 = json.loads(Path("/Users/triton/PROTEUS/experiments/2026-10-31-P-0276/results.json").read_text())
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) proteus-p0289"}
GH = re.compile(r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", re.I)
PROMISE = re.compile(r"(code|data|implementation)[^.]{0,40}(is|are|will be)\s+(publicly\s+)?(available|released)", re.I)
SKIP_OWNERS = {"features", "orgs", "topics", "sponsors", "about"}

rows = [r for r in P276["rows"] if not r.get("github_links")]
out = []
for r in rows:
    pdf = SB / f"{r['arxiv']}.pdf"
    txt = SB / f"{r['arxiv']}.txt"
    rec = {"id": r["id"], "arxiv": r["arxiv"], "title": r["title"][:90]}
    if not pdf.exists() or pdf.stat().st_size < 1000:
        try:
            req = urllib.request.Request(f"https://export.arxiv.org/pdf/{r['arxiv']}", headers=UA)
            pdf.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        except Exception as e:  # noqa: BLE001
            rec["fetch_error"] = str(e)[:80]
            out.append(rec)
            continue
        time.sleep(3)
    rec["pdf_bytes"] = pdf.stat().st_size
    p = subprocess.run(["/usr/local/bin/pdftotext", str(pdf), str(txt)], capture_output=True, text=True)
    if p.returncode != 0 or not txt.exists():
        rec["pdftotext_error"] = p.stderr[:80]
        out.append(rec)
        continue
    # undo line-break hyphenation so a URL split over two lines is caught
    text = re.sub(r"-\n", "", txt.read_text(errors="replace"))
    rec["text_chars"] = len(text)
    repos = []
    for o, n in GH.findall(text):
        n = re.sub(r"(\.git|[.,;:)\]]+)$", "", n)
        key = f"{o}/{n}"
        if o.lower() not in SKIP_OWNERS and key.lower() not in (x.lower() for x in repos):
            repos.append(key)
    rec["repos"] = repos
    rec["promise_phrases"] = len(PROMISE.findall(text))
    out.append(rec)

distinct = sorted({x for rec in out for x in rec.get("repos", [])}, key=str.lower)
status = {}
for full in distinct:
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{full}", headers=UA)
        j = json.loads(urllib.request.urlopen(req, timeout=30).read())
        status[full] = {"code": 200, "stars": j.get("stargazers_count"), "pushed": (j.get("pushed_at") or "")[:10],
                        "archived": j.get("archived"), "renamed_to": j.get("full_name") if j.get("full_name", "").lower() != full.lower() else None}
    except urllib.error.HTTPError as e:
        status[full] = {"code": e.code}
    except Exception as e:  # noqa: BLE001
        status[full] = {"code": None, "error": str(e)[:60]}
    time.sleep(1)

papers_with = [rec for rec in out if rec.get("repos")]
summary = {
    "papers": len(rows),
    "pdfs_read": sum(1 for rec in out if "text_chars" in rec),
    "papers_with_github_in_pdf": len(papers_with),
    "papers_with_promise_but_no_link": sum(1 for rec in out if not rec.get("repos") and rec.get("promise_phrases")),
    "distinct_repos": len(distinct),
    "repos_200": sum(1 for s in status.values() if s.get("code") == 200),
    "repos_404": sum(1 for s in status.values() if s.get("code") == 404),
    "repos_other": sum(1 for s in status.values() if s.get("code") not in (200, 404)),
    "stars_of_200": sorted(s["stars"] for s in status.values() if s.get("code") == 200),
}
(HERE / "results.json").write_text(json.dumps({"summary": summary, "status": status, "papers": out}, indent=1))
print(json.dumps(summary, indent=1))
for rec in papers_with:
    print(rec["arxiv"], rec["repos"][:4])
