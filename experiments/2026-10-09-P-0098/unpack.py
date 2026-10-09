"""Unpack a downloaded tarball into its own empty folder, safely (tarfile 'data' filter).
usage: python3 unpack.py TARBALL DEST"""
import os
import sys
import tarfile

src, dest = sys.argv[1], sys.argv[2]
os.makedirs(dest, exist_ok=True)
with tarfile.open(src) as t:
    t.extractall(dest, filter="data")
    names = t.getnames()
print(len(names), "entries; top:", sorted({n.split("/")[0] for n in names}))
for n in sorted(names):
    if n.count("/") <= 2:
        print(n)
