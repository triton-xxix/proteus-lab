"""P-0272: fetch patch-gg/pixelfx as a tarball (no git clone in a scheduled run) into the sandbox."""
import io
import sys
import tarfile
import urllib.request

DEST = "/Users/triton/PROTEUS/sandbox/pixelfx-src"
for branch in ("main", "master"):
    url = f"https://codeload.github.com/patch-gg/pixelfx/tar.gz/refs/heads/{branch}"
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "proteus-probe"}), timeout=60).read()
    except Exception as e:  # noqa: BLE001
        print("fetch", branch, "failed:", e)
        continue
    print("fetched", branch, len(data), "bytes")
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        names = tf.getnames()
        tf.extractall(DEST, filter="data")
    print("extracted", len(names), "entries to", DEST)
    print("top:", sorted({n.split("/")[1] for n in names if "/" in n})[:40])
    sys.exit(0)
sys.exit(1)
