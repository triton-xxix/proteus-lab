"""Fetch two old public front-end repos as tarballs (no git clone) into sandbox/mwg-targets/.
Extraction refuses absolute paths, parent hops and links. Nothing fetched is executed."""
import io, tarfile, urllib.request
from pathlib import Path

OUT = Path("/Users/triton/PROTEUS/sandbox/mwg-targets")
TARGETS = {
    "bootstrap-3.4.1": "https://codeload.github.com/twbs/bootstrap/tar.gz/refs/tags/v3.4.1",
    "html5-boilerplate-5.3.0": "https://codeload.github.com/h5bp/html5-boilerplate/tar.gz/refs/tags/5.3.0",
}
KEEP = (".js", ".html", ".css", ".htm")
for name, url in TARGETS.items():
    dest = OUT / name
    dest.mkdir(parents=True, exist_ok=True)
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "curl/8"}), timeout=60).read()
    n = 0
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tf:
        for m in tf:
            parts = Path(m.name).parts[1:]
            if not m.isfile() or not parts or ".." in parts or m.name.startswith("/"):
                continue
            if not m.name.endswith(KEEP) or ".min." in m.name or m.size > 400_000:
                continue
            if "dist" in parts or "vendor" in parts or "node_modules" in parts:
                continue
            p = dest.joinpath(*parts)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(tf.extractfile(m).read())
            n += 1
    print(name, len(data), "bytes,", n, "files kept")
