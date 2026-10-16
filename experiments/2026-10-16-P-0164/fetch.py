"""Fetch the pro-vi/cc-stretch tarball into sandbox/p0164/ (no git clone) and list its files."""
import io
import tarfile
import urllib.request
from pathlib import Path

DEST = Path("/Users/triton/PROTEUS/sandbox/p0164")
DEST.mkdir(parents=True, exist_ok=True)
url = "https://codeload.github.com/pro-vi/cc-stretch/tar.gz/HEAD"
raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-lab"}), timeout=60).read()
with tarfile.open(fileobj=io.BytesIO(raw)) as t:
    t.extractall(DEST, filter="data")
for p in sorted(DEST.rglob("*")):
    if p.is_file():
        print(p.relative_to(DEST), p.stat().st_size)
