import sys, tarfile
src, dest = sys.argv[1], sys.argv[2]
with tarfile.open(src) as t:
    t.extractall(dest, filter="data")
    for m in t.getmembers():
        if m.isfile():
            print(m.size, m.name)
