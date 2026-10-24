"""Check that a unified diff's context and removed lines match the working tree, since `git apply
--check` is off the unattended list. Smith 24 Oct 2026.

    python3 /Users/triton/PROTEUS/state/loop/hook-patches/check-diff.py <diff path>

Prints one line per hunk: OK at <line> (offset n) or MISMATCH with the first differing line.
Exit 1 on any mismatch. Does not apply anything.
"""
import re
import sys

ROOT = "/Users/triton/PROTEUS/"


def main(path):
    text = open(path).read().splitlines()
    files, cur = [], None
    for ln in text:
        if ln.startswith("--- a/"):
            cur = {"file": ln[6:], "hunks": []}
        elif ln.startswith("+++ b/"):
            files.append(cur)
        elif ln.startswith("@@") and cur is not None:
            m = re.match(r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", ln)
            cur["hunks"].append({"start": int(m.group(1)), "old_n": int(m.group(2) or 1), "new_n": int(m.group(4) or 1), "lines": []})
        elif cur is not None and cur["hunks"] and (ln[:1] in (" ", "+", "-") or ln == ""):
            cur["hunks"][-1]["lines"].append(ln if ln else " ")
    bad = 0
    for f in files:
        src = open(ROOT + f["file"]).read().splitlines()
        for h in f["hunks"]:
            old = [l[1:] for l in h["lines"] if l[0] in " -"]
            new = [l[1:] for l in h["lines"] if l[0] in " +"]
            counts = "counts old %d/%d new %d/%d" % (len(old), h["old_n"], len(new), h["new_n"])
            if len(old) != h["old_n"] or len(new) != h["new_n"]:
                print("MISMATCH %s @@ -%d: hunk header %s" % (f["file"], h["start"], counts))
                bad += 1
                continue
            hit = None
            for off in [0] + [d for k in range(1, 400) for d in (k, -k)]:
                s = h["start"] - 1 + off
                if s < 0 or s + len(old) > len(src):
                    continue
                if src[s:s + len(old)] == old:
                    hit = off
                    break
            if hit is None:
                s = h["start"] - 1
                for i, (a, b) in enumerate(zip(old, src[s:s + len(old)])):
                    if a != b:
                        print("MISMATCH %s @@ -%d: line %d diff is %r, tree is %r" % (f["file"], h["start"], s + i + 1, a, b))
                        break
                else:
                    print("MISMATCH %s @@ -%d: runs past end of file" % (f["file"], h["start"]))
                bad += 1
            else:
                print("OK %s @@ -%d (offset %d), %s" % (f["file"], h["start"], hit, counts))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
