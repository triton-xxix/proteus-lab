"""Fetch a GitHub repo as a tarball into the sandbox (git clone is not on the safe list)."""
import io
import sys
import tarfile
import urllib.request

repo = sys.argv[1]
dest = sys.argv[2]
url = f"https://codeload.github.com/{repo}/tar.gz/HEAD"
req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe"})
data = urllib.request.urlopen(req, timeout=60).read()
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    tf.extractall(dest, filter="data")
    names = tf.getnames()
print(f"fetched {repo}: {len(data)} bytes, {len(names)} entries, root {names[0]}")
