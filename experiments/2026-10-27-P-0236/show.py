"""Print named members of a tarball, or the lines around a pattern, without extracting."""
import re, sys, tarfile

tgz, pattern = sys.argv[1], sys.argv[2]
names = sys.argv[3:]
with tarfile.open(tgz) as t:
    for n in names:
        text = t.extractfile("package/" + n).read().decode("utf-8", "replace").splitlines()
        print("=====", n, len(text), "lines")
        for i, line in enumerate(text):
            if pattern == "ALL" or re.search(pattern, line):
                print("%4d %s" % (i + 1, line[:200]))
