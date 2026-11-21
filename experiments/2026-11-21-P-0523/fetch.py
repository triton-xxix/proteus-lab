"""Fetch a GitHub repo tarball and extract it safely. Usage: fetch.py OWNER/REPO DEST_DIR"""
import io
import os
import sys
import tarfile
import urllib.request

repo, dest = sys.argv[1], sys.argv[2]
url = "https://codeload.github.com/%s/tar.gz/HEAD" % repo
data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-research/1.0"}), timeout=120).read()
os.makedirs(dest, exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    tf.extractall(dest, filter="data")
print(len(data), "bytes to", dest, os.listdir(dest))
