"""P-0288: does huashu-bird-sticker's species data hold 11,064 records, names in 43 languages,
and a sticker file for each? Reads the GitHub tree (fetched to sandbox/birdsticker/tree.json),
downloads the species data file(s) raw, counts, and writes results.json beside this script."""
import collections
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = Path("/Users/triton/PROTEUS/sandbox/birdsticker")
RAW = "https://raw.githubusercontent.com/alchaincyf/huashu-bird-sticker/HEAD/"
tree = json.loads((SB / "tree.json").read_text())
blobs = [t for t in tree["tree"] if t["type"] == "blob"]
out = {"truncated": tree.get("truncated"), "blobs": len(blobs)}
out["top_dirs"] = collections.Counter(b["path"].split("/")[0] for b in blobs).most_common(12)
exts = collections.Counter(Path(b["path"]).suffix for b in blobs)
out["extensions"] = exts.most_common(8)
jsons = [b for b in blobs if b["path"].endswith(".json")]
out["json_files"] = [(b["path"], b.get("size")) for b in sorted(jsons, key=lambda b: -(b.get("size") or 0))[:10]]
images = [b["path"] for b in blobs if Path(b["path"]).suffix.lower() in (".png", ".webp", ".svg", ".jpg", ".avif")]
out["image_files"] = len(images)

cand = [b for b in jsons if re.search(r"species", b["path"], re.I)]
if not cand:
    print(json.dumps(out, indent=1))
    sys.exit(0)
path = max(cand, key=lambda b: b.get("size") or 0)["path"]
out["species_path"] = path
local = SB / Path(path).name
if not local.exists():
    urllib.request.urlretrieve(RAW + path, local)
data = json.loads(local.read_text())
recs = data if isinstance(data, list) else next((v for v in data.values() if isinstance(v, list)), [])
if isinstance(data, dict) and not recs:
    recs = list(data.values())
out["records"] = len(recs)
out["record_keys"] = sorted(recs[0].keys()) if recs and isinstance(recs[0], dict) else None


def name_langs(r):
    for k in ("names", "name", "i18n", "translations", "common_names"):
        v = r.get(k)
        if isinstance(v, dict):
            return set(v)
    return set()


langs = [name_langs(r) for r in recs if isinstance(r, dict)]
if langs:
    union = set().union(*langs)
    counts = collections.Counter(len(s) for s in langs)
    out["languages_union"] = len(union)
    out["languages_per_record"] = sorted(counts.items())
    out["records_with_all_union_langs"] = sum(1 for s in langs if s == union)

# a sticker per record: match any record field that looks like a file path or id against the image list
img_names = {Path(p).stem for p in images}
img_paths = set(images)
hit = 0
fields = collections.Counter()
for r in recs:
    if not isinstance(r, dict):
        continue
    found = False
    for k, v in r.items():
        if isinstance(v, str) and (v in img_paths or v.lstrip("./") in img_paths or Path(v).stem in img_names):
            if k not in ("names",):
                fields[k] += 1
                found = True
                break
    hit += found
out["records_matching_an_image"] = hit
out["matching_fields"] = fields.most_common(3)
(HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
