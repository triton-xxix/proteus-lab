"""P-0056: fetch youtube-transcript-plus from the npm registry (npm itself is denied unattended)."""
import io
import json
import tarfile
import urllib.request
from pathlib import Path

DEST = Path("/Users/triton/PROTEUS/sandbox/ytplus")
DEST.mkdir(parents=True, exist_ok=True)
meta = json.load(urllib.request.urlopen("https://registry.npmjs.org/youtube-transcript-plus/latest", timeout=30))
print("version", meta["version"], "deps", meta.get("dependencies"))
data = urllib.request.urlopen(meta["dist"]["tarball"], timeout=60).read()
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
    t.extractall(DEST, filter="data")
for p in sorted(DEST.rglob("*")):
    if p.is_file():
        print(p.relative_to(DEST), p.stat().st_size)
