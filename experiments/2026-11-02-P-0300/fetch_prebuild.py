"""P-0300: --ignore-scripts skips better-sqlite3's prebuild-install, so fetch its published prebuilt binary
from the project's GitHub release and unpack it where the package looks (build/Release)."""
import io
import tarfile
import urllib.request

# 13.0.0 to 13.0.3 publish no release assets at all (checked 2 Nov 2026), so take the newest 12.x binary
# for Node ABI 141 and see whether the 13.0.3 wrapper loads it.
V, ABI, PLAT, ARCH = "12.12.0", "141", "darwin", "x64"
PKG = "/Users/triton/PROTEUS/sandbox/markindex/node_modules/better-sqlite3"
URL = (f"https://github.com/WiseLibs/better-sqlite3/releases/download/v{V}/"
       f"better-sqlite3-v{V}-node-v{ABI}-{PLAT}-{ARCH}.tar.gz")
data = urllib.request.urlopen(URL, timeout=60).read()
print("fetched", len(data), "bytes from", URL)
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    print([m.name for m in tf.getmembers()])
    tf.extractall(PKG, filter="data")
