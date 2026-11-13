"""P-0439: unpack the guizang-game-skill tarball safely and list what the packager is."""
import sys, tarfile, os

src = "/Users/triton/PROTEUS/sandbox/p0439/repo.tar.gz"
dst = "/Users/triton/PROTEUS/sandbox/p0439/src"
os.makedirs(dst, exist_ok=True)
with tarfile.open(src) as t:
    t.extractall(dst, filter="data")
for root, dirs, files in os.walk(dst):
    for f in files:
        p = os.path.join(root, f)
        print(os.path.getsize(p), p[len(dst) + 1:])
