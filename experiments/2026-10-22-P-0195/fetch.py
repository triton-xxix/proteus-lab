"""P-0195: fetch Molecular_Animation's main tarball into sandbox/p0195/repo (no git clone)."""
import io
import json
import os
import tarfile
import urllib.request

DEST = "/Users/triton/PROTEUS/sandbox/p0195/repo"
URL = "https://codeload.github.com/AmadeusBio-ai/Molecular_Animation/tar.gz/refs/heads/main"
data = urllib.request.urlopen(URL, timeout=120).read()
os.makedirs(DEST, exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
    ms = []
    for m in tf.getmembers():
        parts = m.name.split("/", 1)
        if len(parts) < 2 or not parts[1] or ".." in parts[1].split("/"):
            continue
        m.name = parts[1]
        ms.append(m)
    tf.extractall(DEST, members=ms, filter="data")
print(json.dumps({"bytes": len(data), "members": len(ms)}))
