"""P-0181: fetch MaryCache/imozuru as a tarball into sandbox/ (no git clone on the safe list)."""
import io
import tarfile
import urllib.request

URL = "https://codeload.github.com/MaryCache/imozuru/tar.gz/refs/heads/main"
DEST = "/Users/triton/PROTEUS/sandbox/p0181-imozuru"

data = urllib.request.urlopen(URL, timeout=60).read()
print("bytes", len(data))
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    safe = [m for m in tf.getmembers() if not m.name.startswith("/") and ".." not in m.name and (m.isfile() or m.isdir())]
    tf.extractall(DEST, members=safe)
    print("members", len(safe))
