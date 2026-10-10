"""P-0122: fetch wheresryan22/anatomy as a tarball (no git clone) into a fresh sandbox folder."""
import io
import os
import sys
import tarfile
import urllib.request

DEST = "/Users/triton/PROTEUS/sandbox/p0122-anatomy"
os.makedirs(DEST, exist_ok=True)
url = "https://codeload.github.com/wheresryan22/anatomy/tar.gz/HEAD"
data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus"}), timeout=60).read()
print("bytes", len(data))
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
    t.extractall(DEST, filter="data")
for root, dirs, files in os.walk(DEST):
    dirs[:] = [d for d in dirs if d != "node_modules"]
    depth = root[len(DEST):].count(os.sep)
    if depth <= 3:
        for f in files:
            print(os.path.join(root, f)[len(DEST) + 1:])
sys.exit(0)
