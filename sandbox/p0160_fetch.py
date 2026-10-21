import io, tarfile, urllib.request, os
dest = "/Users/triton/PROTEUS/sandbox/mcd-saver-strategist"
os.makedirs(dest, exist_ok=True)
for branch in ("main", "master"):
    try:
        data = urllib.request.urlopen(f"https://codeload.github.com/hujjun/mcd-saver-strategist/tar.gz/refs/heads/{branch}", timeout=60).read()
        break
    except Exception as e:
        print(branch, e)
else:
    raise SystemExit("no tarball")
tf = tarfile.open(fileobj=io.BytesIO(data))
for m in tf.getmembers():
    if m.isfile() and ".." not in m.name:
        parts = m.name.split("/", 1)
        p = os.path.join(dest, parts[1] if len(parts) > 1 else parts[0])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(tf.extractfile(m).read())
        print(p, m.size)
