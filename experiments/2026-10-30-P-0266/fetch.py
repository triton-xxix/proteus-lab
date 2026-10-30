"""Fetch the nirholas/pump-fun-sdk repo tarball into an empty sandbox folder and list it. Stdlib."""
import io
import os
import tarfile
import urllib.request

dest = "/Users/triton/PROTEUS/sandbox/pump-fun-sdk-src"
os.makedirs(dest, exist_ok=True)
url = "https://codeload.github.com/nirholas/pump-fun-sdk/tar.gz/HEAD"
req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/0.1"})
data = urllib.request.urlopen(req, timeout=120).read()
print("tarball bytes", len(data))
tf = tarfile.open(fileobj=io.BytesIO(data), mode="r:gz")
members = [m for m in tf.getmembers() if ".." not in m.name and not m.name.startswith("/")]
tf.extractall(dest, members=members)
names = [m.name for m in members]
print("files", len(names))
top = names[0].split("/")[0]
print("root", top)
for n in names:
    low = n.lower()
    if n.endswith("package.json") and n.count("/") == 1:
        print("package.json:", n)
    if any(k in low for k in ("bondingcurve", "bonding-curve", "bonding_curve", "curve", "quote", "progress")) and n.endswith((".ts", ".js")) and "node_modules" not in n:
        print("curve file:", n)
