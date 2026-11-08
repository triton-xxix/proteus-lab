"""P-0370: does kubai087/kubai-icons really hold 2,600+ icons under an MIT licence?

Keyless. Reads the git tree and the licence files from GitHub, counts icon-shaped
paths by top folder and extension, and saves what it found beside this script.
"""
import collections
import json
import pathlib
import re
import urllib.request

HERE = pathlib.Path(__file__).parent
REPO = "kubai087/kubai-icons"
BRANCH = "master"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


tree = json.loads(get(f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"))
blobs = [t for t in tree["tree"] if t["type"] == "blob"]
paths = [b["path"] for b in blobs]

by_ext = collections.Counter(pathlib.PurePath(p).suffix.lower() for p in paths)
by_top = collections.Counter(p.split("/")[0] for p in paths)
svgs = [p for p in paths if p.lower().endswith(".svg")]
svg_stems = {pathlib.PurePath(p).stem.lower() for p in svgs}
svg_by_dir = collections.Counter(str(pathlib.PurePath(p).parent) for p in svgs)
licences = [p for p in paths if re.search(r"(^|/)(licen[cs]e|copying|notice)", p, re.I)]

texts = {}
for p in licences[:10]:
    try:
        texts[p] = get(f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{p}")
    except Exception as e:
        texts[p] = f"ERROR {e}"

try:
    readme = get(f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/README.md")
except Exception as e:
    readme = f"ERROR {e}"
readme_lines = [l for l in readme.splitlines() if re.search(r"licen[cs]e|MIT|2,?600|icons", l, re.I)]

out = {
    "truncated": tree.get("truncated"),
    "files": len(paths),
    "by_ext": by_ext.most_common(12),
    "by_top": by_top.most_common(15),
    "svg_files": len(svgs),
    "svg_distinct_stems": len(svg_stems),
    "svg_top_dirs": svg_by_dir.most_common(12),
    "licence_files": licences,
    "readme_lines": readme_lines[:30],
}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
for p, t in texts.items():
    (HERE / ("licence-" + p.replace("/", "_") + ".txt")).write_text(t)
print(json.dumps(out, indent=1))
for p, t in texts.items():
    print("=====", p, len(t))
    print(t[:900])
