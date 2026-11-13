"""P-0443: of done probes whose note says install, npm or pip, how many artefact folders name a version
or a source URL for what was installed? Word and pattern matching over every text file in each folder.
Shot (called before running): about a third."""
import json, os, re

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "experiments/2026-11-13-P-0443/"
INSTALL = re.compile(r"\b(install(ed|s|ing)?|npm ci|npm|pip|pip3|venv|wheel)\b", re.I)
VERSION = re.compile(r"(==\s?\d+\.\d+|@\d+\.\d+\.\d+|\b\d+\.\d+\.\d+\b|\bv\d+\.\d+\b|\bversion\s+\d)", re.I)
SOURCE = re.compile(r"(github\.com/[\w.-]+/[\w.-]+|codeload\.github\.com|pypi\.org/project|npmjs\.com/package|tar\.gz|\bcommit [0-9a-f]{7,}|\b[0-9a-f]{40}\b|requirements\.txt|package-lock\.json|package\.json|uv\.lock|poetry\.lock)", re.I)
TEXT = (".md", ".txt", ".json", ".py", ".mjs", ".js", ".sh", ".toml", ".cfg", ".yaml", ".yml")

items = json.load(open(ROOT + "state/probes.json"))["items"]
rows = []
for it in items:
    if it.get("status") != "done" or it.get("verdict") not in ("works", "broken", "not-worth-it", "blocked"):
        continue
    note = (it.get("note") or "") + " " + (it.get("title") or "")
    hits = INSTALL.findall(note)
    if not hits:
        continue
    folders = [a for a in it.get("artefacts") or [] if a.startswith("experiments/")]
    folders = [ROOT + f.rstrip("/") for f in folders if os.path.isdir(ROOT + f.rstrip("/"))]
    v = s = 0; files = 0
    for f in folders:
        for root, _, fs in os.walk(f):
            for name in fs:
                if not name.endswith(TEXT):
                    continue
                p = os.path.join(root, name)
                if os.path.getsize(p) > 2_000_000:
                    continue
                files += 1
                if name in ("requirements.txt", "package.json", "package-lock.json", "uv.lock"):
                    s += 1
                try:
                    t = open(p, errors="ignore").read()
                except Exception:
                    continue
                v += len(VERSION.findall(t)); s += len(SOURCE.findall(t))
    rows.append({"id": it["id"], "verdict": it["verdict"], "install_words": len(hits), "folders": len(folders), "files": files,
                 "version_marks": v, "source_marks": s, "title": it["title"][:90]})

with_folder = [r for r in rows if r["folders"]]
named = [r for r in with_folder if r["version_marks"] or r["source_marks"]]
both = [r for r in with_folder if r["version_marks"] and r["source_marks"]]
neither = sorted([r for r in with_folder if not r["version_marks"] and not r["source_marks"]], key=lambda r: -r["install_words"])
res = {"probes_with_install_words": len(rows), "with_artefact_folder": len(with_folder),
       "name_version_or_source": len(named), "name_both": len(both), "neither": len(neither),
       "share_named": round(len(named) / len(with_folder), 3) if with_folder else None,
       "worst_five": neither[:5], "rows": rows}
json.dump(res, open(OUT + "results.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "rows"}, indent=1))
