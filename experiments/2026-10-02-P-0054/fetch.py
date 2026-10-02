"""P-0054: fetch ldraw-nova's main-branch tarball into sandbox/ and list what is in it."""
import io
import tarfile
import urllib.request
from pathlib import Path

DEST = Path("/Users/triton/PROTEUS/sandbox/ldraw-nova")
DEST.mkdir(parents=True, exist_ok=True)
url = "https://codeload.github.com/anteloc/ldraw-nova/tar.gz/refs/heads/main"
with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus"}), timeout=60) as r:
    data = r.read()
print("bytes", len(data))
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
    members = [m for m in t.getmembers() if not m.name.startswith("/") and ".." not in m.name]
    t.extractall(DEST, members=members, filter="data")
for p in sorted(DEST.rglob("*")):
    if p.is_file() and "node_modules" not in p.parts:
        print(p.relative_to(DEST), p.stat().st_size)
