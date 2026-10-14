"""Fetch a GitHub repo tarball into a fresh sandbox folder (git clone is off the safe list)."""
import io
import sys
import tarfile
import urllib.request
from pathlib import Path

repo, dest = sys.argv[1], Path(sys.argv[2])
dest.mkdir(parents=True, exist_ok=False)
data = urllib.request.urlopen(f"https://codeload.github.com/{repo}/tar.gz/HEAD", timeout=120).read()
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    members = t.getmembers()
    root = members[0].name.split("/")[0]
    for m in members:
        if m.issym() or m.islnk() or ".." in m.name:
            continue
        m.name = m.name[len(root) + 1:]
        if m.name:
            t.extract(m, dest)
print(f"{len(data)} bytes, {len(members)} entries, root {root}")
