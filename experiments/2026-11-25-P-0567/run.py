"""P-0567: does the 23 Nov lead list land cleanly in Hermit CRM?

Writes the 20 OSM rows as a CSV in the sandbox (names stay there; sandbox/ is gitignored), inits a fresh Hermit
data folder, runs import as a dry run, then with --apply, then check and report. Only counts and Hermit's
own messages (with firm names replaced by row numbers) go into results.json.
Called shot: works, 20 of 20 imported in one command, check passes with no errors.
"""
import csv, json, re, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = Path("/Users/triton/PROTEUS/sandbox/p0567")
HERMIT = "/Users/triton/PROTEUS/sandbox/hermit-venv/bin/hermitcrm"
rows = json.loads(Path("/Users/triton/PROTEUS/experiments/2026-11-23-lead-finder/run-2026-11-23.json").read_text())["rows"]
if SB.exists():
    shutil.rmtree(SB)
SB.mkdir(parents=True)
data = SB / "data"
src = SB / "leads.csv"
with open(src, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["name", "website", "phone", "postcode", "industry", "source"])
    for r in rows:
        w.writerow([r.get("name") or "", r.get("website") or "", r.get("phone") or "", r.get("postcode") or "",
                    r.get("craft") or "", "osm " + str(r.get("osm") or "")])
names = [r.get("name") or "" for r in rows]


def scrub(t):
    for i, n in enumerate(sorted(set(n for n in names if n), key=len, reverse=True)):
        t = t.replace(n, "<firm>")
    return re.sub(r"https?://\S+?(?=,|\s|$)", "<site>", t)


def run(*args):
    p = subprocess.run([HERMIT, "--data", str(data), *args], capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)
    return {"cmd": " ".join(args), "rc": p.returncode, "out": scrub(p.stdout)[-3000:], "err": scrub(p.stderr)[-1500:]}


out = {"rows_in": len(rows), "named": sum(bool(n) for n in names),
       "with_website": sum(bool(r.get("website")) for r in rows), "with_phone": sum(bool(r.get("phone")) for r in rows)}
steps = [subprocess.run([HERMIT, "init", str(data)], capture_output=True, text=True, timeout=120, stdin=subprocess.DEVNULL)]
out["init"] = {"rc": steps[0].returncode, "out": steps[0].stdout[-800:], "err": steps[0].stderr[-800:]}
out["dry_run"] = run("import", str(src))
out["apply"] = run("import", str(src), "--apply")
out["reimport_dry_run"] = run("import", str(src), "--mode", "companies")
out["mapping_line"] = next((l for l in out["reimport_dry_run"]["out"].splitlines() if l.startswith("Mode:")), None)
out["check"] = run("check")
out["report"] = run("report")
companies = data / "companies"
out["company_files"] = len(list(companies.rglob("*.md"))) if companies.exists() else 0
(HERE / "results.json").write_text(json.dumps(out, indent=1))
for k in ("init", "dry_run", "apply", "check", "report"):
    v = out[k]
    print("==", k, "rc", v["rc"])
    print((v["out"] or "")[-900:])
    if v["err"]:
        print("ERR", v["err"][-500:])
print("company files", out["company_files"], "rows in", out["rows_in"], "named", out["named"])
