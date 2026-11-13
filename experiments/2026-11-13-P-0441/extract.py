"""P-0441: unpack cinematic-skill safely and list it."""
import tarfile, os
src = "/Users/triton/PROTEUS/sandbox/p0441/repo.tar.gz"
dst = "/Users/triton/PROTEUS/sandbox/p0441/src"
os.makedirs(dst, exist_ok=True)
with tarfile.open(src) as t:
    t.extractall(dst, filter="data")
for root, dirs, files in os.walk(dst):
    for f in files:
        p = os.path.join(root, f)
        if not f.endswith((".png", ".jpg", ".mp3", ".wav", ".gif", ".mp4", ".ttf", ".otf", ".woff2")):
            print(os.path.getsize(p), p[len(dst) + 1:])
