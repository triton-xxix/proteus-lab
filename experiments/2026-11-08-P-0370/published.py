"""P-0370 part two: the repo holds about 900 icon definitions, so where do 2,600+ come from?

Reads the published npm tarball of kubai-icons-static and lists it (no extraction, nothing
from it is executed), then splits the SVGs into base icons and badged or slashed variants.
"""
import collections
import io
import json
import pathlib
import re
import tarfile
import urllib.request

HERE = pathlib.Path(__file__).parent


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


meta = json.loads(get("https://registry.npmjs.org/kubai-icons-static/latest"))
print("version", meta["version"], "licence", meta.get("license"), "fileCount", meta["dist"].get("fileCount"))
tar_bytes = get(meta["dist"]["tarball"])
with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:gz") as t:
    names = [m.name for m in t.getmembers() if m.isfile()]
    lic = [n for n in names if re.search(r"licen[cs]e", n, re.I)]
    lic_head = {}
    for n in lic:
        lic_head[n] = t.extractfile(n).read(200).decode("utf-8", "replace")

svgs = [n for n in names if n.lower().endswith(".svg")]
stems = sorted({pathlib.PurePath(n).stem for n in svgs})
dirs = collections.Counter(str(pathlib.PurePath(n).parent) for n in svgs)

# Variants: a stem that is another stem plus a suffix, e.g. folder-off, folder-check.
stem_set = set(stems)
parents = {}
for s in stems:
    parts = s.split("-")
    for i in range(len(parts) - 1, 0, -1):
        head = "-".join(parts[:i])
        if head in stem_set:
            parents[s] = (head, "-".join(parts[i:]))
            break
suffixes = collections.Counter(v[1] for v in parents.values())
off = [s for s in stems if s.endswith("-off")]

# The repo's own definition count, from the git tree saved in part one.
out = {
    "version": meta["version"],
    "licence": meta.get("license"),
    "tarball_bytes": len(tar_bytes),
    "files": len(names),
    "svg_files": len(svgs),
    "svg_distinct_stems": len(stems),
    "svg_dirs": dirs.most_common(10),
    "stems_with_a_parent_stem": len(parents),
    "stems_without_a_parent": len(stems) - len(parents),
    "off_variants": len(off),
    "top_suffixes": suffixes.most_common(25),
    "licence_files": lic_head,
    "sample": stems[:10],
}
(HERE / "published.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
