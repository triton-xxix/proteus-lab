#!/usr/bin/env python3
"""Fetch a GitHub repo tarball keyless into an empty directory (no git clone on the safe list).
Usage: python3 -I fetch.py OWNER/REPO DEST_DIR
"""
import io
import os
import sys
import tarfile
import urllib.request

owner_repo, dest = sys.argv[1], sys.argv[2]
url = "https://codeload.github.com/%s/tar.gz/HEAD" % owner_repo
os.makedirs(dest, exist_ok=True)
data = urllib.request.urlopen(url, timeout=60).read()
print("downloaded", len(data), "bytes from", url)
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    members = tf.getmembers()
    for m in members:
        if m.name.startswith("/") or ".." in m.name:
            raise SystemExit("unsafe member " + m.name)
    tf.extractall(dest)
    print("extracted", len(members), "members")
for root, dirs, files in os.walk(dest):
    for f in files:
        p = os.path.join(root, f)
        print(os.path.getsize(p), p.replace(dest + "/", ""))
