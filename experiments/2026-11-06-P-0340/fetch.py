#!/usr/bin/env python3
"""Fetch a GitHub repo tarball into sandbox/<name>/ without git clone. Args: owner/repo name."""
import io
import os
import sys
import tarfile
import urllib.request

repo, name = sys.argv[1], sys.argv[2]
dest = os.path.join("/Users/triton/PROTEUS/sandbox", name)
os.makedirs(dest, exist_ok=True)
url = f"https://codeload.github.com/{repo}/tar.gz/HEAD"
data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-probe"}), timeout=120).read()
with tarfile.open(fileobj=io.BytesIO(data)) as t:
    names = []
    for m in t.getmembers():
        parts = m.name.split("/", 1)
        if len(parts) < 2 or not parts[1] or m.issym() or m.islnk():
            continue
        if ".." in parts[1].split("/"):
            continue
        m.name = parts[1]
        t.extract(m, dest, filter="data")
        names.append(m.name)
print(len(data), "bytes", len(names), "entries ->", dest)
for n in sorted(names):
    if n.count("/") <= 2:
        print(n)
