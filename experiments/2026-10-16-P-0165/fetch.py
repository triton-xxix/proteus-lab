"""Fetch the Leonxlnx/earshot tarball into sandbox/p0165/ (no git clone) and list its files."""
import io
import tarfile
import urllib.request
from pathlib import Path

DEST = Path("/Users/triton/PROTEUS/sandbox/p0165")
DEST.mkdir(parents=True, exist_ok=True)
url = "https://codeload.github.com/Leonxlnx/earshot/tar.gz/HEAD"
raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-lab"}), timeout=60).read()
print("tarball bytes", len(raw))
with tarfile.open(fileobj=io.BytesIO(raw)) as t:
    t.extractall(DEST, filter="data")
for p in sorted(DEST.rglob("*")):
    if p.is_file() and p.stat().st_size > 0:
        print(p.relative_to(DEST), p.stat().st_size)
