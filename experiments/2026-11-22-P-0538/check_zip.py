"""P-0538: what does the ungated ASVspoof 2019 mirror's dummy zip hold, and does any of it match SEAR?

Fetches LanceaKing/asvspoof2019 dummy/LA/1.0.0/dummy_data.zip (3.7 MB) and SEAR t1/19LA_*.jsonl
(dev 16 MB, train 17 MB) into sandbox/p0538/, lists the zip's flac and protocol files, and intersects
the flac ids with SEAR's audio_path ids. Data only: the zip is listed with zipfile, nothing executed.
"""
import io, json, re, urllib.request, zipfile
from pathlib import Path

SB = Path("/Users/triton/PROTEUS/sandbox/p0538")
SB.mkdir(parents=True, exist_ok=True)
OUT = Path(__file__).with_name("results.json")
HF = "https://huggingface.co/datasets"


def get(url, dest):
    if not dest.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe"})
        dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return dest


z = get(f"{HF}/LanceaKing/asvspoof2019/resolve/main/dummy/LA/1.0.0/dummy_data.zip", SB / "dummy_LA.zip")
zf = zipfile.ZipFile(z)
names = zf.namelist()
flacs = [n for n in names if n.endswith(".flac")]
protos = [n for n in names if n.endswith(".txt")]
ids = lambda ns: {re.search(r"(LA_[TDE]_\d+)", n).group(1) for n in ns if re.search(r"(LA_[TDE]_\d+)", n)}
zip_ids = ids(flacs)
by_split = {s: sorted(i for i in zip_ids if i.startswith(f"LA_{s}_")) for s in "TDE"}
proto_lines = {}
for p in protos:
    lines = zf.read(p).decode("utf-8", "replace").strip().splitlines()
    proto_lines[p] = {"lines": len(lines), "first": lines[:2]}
sizes = sorted(zf.getinfo(n).file_size for n in flacs)

res = {"zip_bytes": z.stat().st_size, "entries": len(names), "flacs": len(flacs),
       "flac_ids_by_split": {k: len(v) for k, v in by_split.items()},
       "flac_bytes_min_median_max": [sizes[0], sizes[len(sizes) // 2], sizes[-1]] if sizes else None,
       "protocol_files": proto_lines, "sear": {}}

for split in ("dev", "train"):
    j = get(f"{HF}/SEAR-benchmark/SEAR/resolve/main/t1/19LA_{split}.jsonl", SB / f"sear_t1_19LA_{split}.jsonl")
    sear_ids = set()
    for line in open(j, encoding="utf-8"):
        m = re.search(r"(LA_[TDE]_\d+)", line)
        if m:
            sear_ids.add(m.group(1))
    res["sear"][split] = {"sear_ids": len(sear_ids), "in_zip": len(sear_ids & zip_ids),
                          "matched": sorted(sear_ids & zip_ids)[:20]}

OUT.write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
