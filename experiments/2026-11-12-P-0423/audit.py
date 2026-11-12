"""P-0423: open the artefact folders P-0413 labelled without opening.

For every probe in experiments/2026-11-11-P-0413/labels.json, find its artefact folder(s)
(experiments/*-P-NNNN, plus the artefact path on the probe's row in state/probes.json), and look for:
  install evidence: a lockfile or requirements file in the folder, or install words in its text files
  run evidence: an output file (json, csv, log, txt, png, mp4, html) or run words in its text files
Read only. Usage: python3 audit.py /abs/path/results.json
"""
import glob
import json
import os
import re
import sys

ROOT = "/Users/triton/PROTEUS"
LABELS = ROOT + "/experiments/2026-11-11-P-0413/labels.json"
LOCK = {"package-lock.json", "requirements.txt", "go.sum", "go.mod", "pnpm-lock.yaml", "yarn.lock",
        "uv.lock", "poetry.lock", "Pipfile.lock", "Cargo.lock", "package.json", "pyproject.toml"}
INSTALL = re.compile(r"npm (ci|install)|pip install|uv (pip|sync|add)|go (build|install|mod)|cargo (build|install)|"
                     r"brew install|tarball|node_modules|site-packages|venv|wheel|fetched to sandbox|unpacked|"
                     r"downloaded|installed", re.I)
RAN = re.compile(r"\b(ran|run|executed|exit code|exit 0|passed|tests? (pass|ran)|rendered|built|output|stdout)\b", re.I)
NOTRUN = re.compile(r"(not|never|did not|didn't|without) (run|ran|execut|install)|not executed|was not run|"
                    r"did not run|read only|read, not run", re.I)
OUT_EXT = {".json", ".csv", ".log", ".txt", ".png", ".jpg", ".mp4", ".html", ".jsonl", ".svg", ".gif", ".wav"}
TEXT_EXT = {".md", ".txt", ".log", ".py", ".js", ".mjs", ".sh", ".json"}


def folders_for(pid, probes):
    out = set(glob.glob(ROOT + "/experiments/*-" + pid)) | set(glob.glob(ROOT + "/experiments/*-" + pid + "-*"))
    row = probes.get(pid) or {}
    a = row.get("artefact") or ""
    if a:
        p = a if a.startswith("/") else os.path.join(ROOT, a)
        if os.path.exists(p):
            out.add(p.rstrip("/"))
    return sorted(out)


def scan_folder(path):
    files, text = [], ""
    if os.path.isfile(path):
        walk = [(os.path.dirname(path), [], [os.path.basename(path)])]
    else:
        walk = os.walk(path)
    for d, _, fs in walk:
        if "node_modules" in d or ".venv" in d:
            continue
        for f in fs:
            full = os.path.join(d, f)
            files.append(full)
            ext = os.path.splitext(f)[1].lower()
            if ext in TEXT_EXT and os.path.getsize(full) < 400000:
                try:
                    text += "\n" + open(full, errors="replace").read()
                except OSError:
                    pass
    names = {os.path.basename(f) for f in files}
    return {"files": len(files), "lockfiles": sorted(names & LOCK),
            "outputs": sum(1 for f in files if os.path.splitext(f)[1].lower() in OUT_EXT),
            "scripts": sum(1 for f in files if os.path.splitext(f)[1].lower() in {".py", ".js", ".mjs", ".sh", ".cjs", ".ts"}),
            "install_words": sorted({m.group(0).lower() for m in INSTALL.finditer(text)})[:8],
            "run_words": len(RAN.findall(text)),
            "not_run_phrases": sorted({m.group(0).lower() for m in NOTRUN.finditer(text)})[:6]}


def main(out_path):
    lab = json.load(open(LABELS))["labels"]
    raw = json.load(open(ROOT + "/state/probes.json"))
    rows = raw["probes"] if isinstance(raw, dict) and "probes" in raw else raw
    probes = {}
    for r in (rows.values() if isinstance(rows, dict) else rows):
        if isinstance(r, dict) and r.get("id"):
            probes[r["id"]] = r
    out = {"rows": []}
    for pid, (label, why) in sorted(lab.items()):
        fs = folders_for(pid, probes)
        agg = {"files": 0, "lockfiles": [], "outputs": 0, "scripts": 0, "install_words": [], "run_words": 0, "not_run_phrases": []}
        for f in fs:
            s = scan_folder(f)
            for k in ("files", "outputs", "scripts", "run_words"):
                agg[k] += s[k]
            for k in ("lockfiles", "install_words", "not_run_phrases"):
                agg[k] = sorted(set(agg[k]) | set(s[k]))
        install = bool(agg["lockfiles"]) or bool(agg["install_words"])
        ran = agg["outputs"] > 0 or agg["run_words"] > 0
        row = {"id": pid, "label": label, "why": why, "folders": [f.replace(ROOT + "/", "") for f in fs],
               "install_evidence": install, "run_trace": ran, **agg}
        out["rows"].append(row)
        print("%s %-7s folders %d files %3d lock %-28s outputs %3d scripts %2d runwords %3d install %-5s notrun %s" % (
            pid, label, len(fs), agg["files"], ",".join(agg["lockfiles"])[:28], agg["outputs"], agg["scripts"],
            agg["run_words"], install, agg["not_run_phrases"]))
    for lb in ("ran", "outside"):
        rs = [r for r in out["rows"] if r["label"] == lb]
        out[lb] = {"n": len(rs), "with_folder": sum(1 for r in rs if r["folders"]),
                   "run_trace": sum(1 for r in rs if r["run_trace"]),
                   "install_evidence": sum(1 for r in rs if r["install_evidence"]),
                   "lockfile": sum(1 for r in rs if r["lockfiles"]),
                   "not_run_phrase": [r["id"] for r in rs if r["not_run_phrases"]],
                   "no_folder": [r["id"] for r in rs if not r["folders"]]}
        print(lb, json.dumps(out[lb]))
    json.dump(out, open(out_path, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
