"""P-0299: fetch caru-ini/stack-diagram as a tarball into sandbox/stack-diagram (no git clone)."""
import io
import os
import tarfile
import urllib.request

DEST = "/Users/triton/PROTEUS/sandbox/stack-diagram"
URL = "https://codeload.github.com/caru-ini/stack-diagram/tar.gz/refs/heads/main"

os.makedirs(DEST, exist_ok=True)
data = urllib.request.urlopen(URL, timeout=60).read()
print("bytes", len(data))
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    tf.extractall(DEST, filter="data")
for root, dirs, files in os.walk(DEST):
    depth = root[len(DEST):].count(os.sep)
    if depth > 3:
        continue
    for f in files:
        p = os.path.join(root, f)
        print(os.path.getsize(p), p[len(DEST) + 1:])
