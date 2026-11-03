"""P-0316: native npm packages (binding.gyp) in sandbox node_modules trees, and whether their newest GitHub release
carries a prebuilt for this Mac (Node ABI 141, darwin x64). Keyless GitHub API, one call per unique repo (60/h limit)."""
import json, os, re, urllib.request, urllib.error, pathlib

SANDBOX = "/Users/triton/PROTEUS/sandbox"
OUT = pathlib.Path(__file__).parent
pkgs = {}
for root, dirs, files in os.walk(SANDBOX):
    if ".npm-cache" in root or "/.git" in root:
        dirs[:] = []
        continue
    if "binding.gyp" in files and os.path.exists(os.path.join(root, "package.json")):
        try:
            pj = json.load(open(os.path.join(root, "package.json")))
        except Exception:
            continue
        name = pj.get("name")
        repo = pj.get("repository")
        repo = repo.get("url") if isinstance(repo, dict) else repo
        m = re.search(r"github\.com[/:]([^/]+/[^/#.]+)", repo or "")
        has_build = os.path.isdir(os.path.join(root, "build", "Release")) or os.path.isdir(os.path.join(root, "prebuilds"))
        pkgs.setdefault(name, {"name": name, "versions": set(), "repo": m.group(1) if m else None, "where": [], "binary_on_disk": False})
        pkgs[name]["versions"].add(pj.get("version"))
        pkgs[name]["where"].append(root.replace(SANDBOX + "/", ""))
        pkgs[name]["binary_on_disk"] |= has_build

print(f"native packages: {len(pkgs)}")
rows = []
for p in pkgs.values():
    row = {k: (sorted(v) if isinstance(v, set) else v) for k, v in p.items()}
    row["where"] = row["where"][:3]
    if p["repo"]:
        try:
            req = urllib.request.Request(f"https://api.github.com/repos/{p['repo']}/releases?per_page=1",
                                         headers={"User-Agent": "proteus-research", "Accept": "application/vnd.github+json"})
            rel = json.load(urllib.request.urlopen(req, timeout=20))
            if rel:
                names = [a["name"] for a in rel[0]["assets"]]
                row["newest_release"] = rel[0]["tag_name"]
                row["assets"] = len(names)
                row["darwin_x64_any"] = any("darwin" in n and "x64" in n for n in names)
                row["node_v141_darwin_x64"] = any("darwin" in n and "x64" in n and ("v141" in n or "napi" in n) for n in names)
            else:
                row["newest_release"] = None
        except urllib.error.HTTPError as e:
            row["error"] = e.code
    rows.append(row)
    print(row)
summ = {"native": len(rows), "with_repo": sum(1 for r in rows if r["repo"]),
        "binary_on_disk": sum(r["binary_on_disk"] for r in rows),
        "release_has_this_mac": sum(1 for r in rows if r.get("node_v141_darwin_x64")),
        "release_has_no_assets": sum(1 for r in rows if r.get("assets") == 0),
        "no_releases": sum(1 for r in rows if r.get("newest_release", 1) is None)}
print(json.dumps(summ))
(OUT / "results.json").write_text(json.dumps({"summary": summ, "rows": rows}, indent=1))
