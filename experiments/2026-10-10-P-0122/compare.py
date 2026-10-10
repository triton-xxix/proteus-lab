"""P-0122: are the rebuilt dial-indicator pages byte-identical to the committed ones (the repo's CI test)?"""
import hashlib
import subprocess

S = "/Users/triton/PROTEUS/sandbox/p0122-anatomy/"
EX = S + "anatomy-HEAD/examples/dial-indicator/"
pairs = [("dark", S + "committed-dark.html", EX + "dial-indicator.html"),
         ("light", S + "committed-light.html", EX + "dial-indicator-light.html")]
print("node", subprocess.run(["node", "-e", "console.log(process.version)"], capture_output=True, text=True).stdout.strip())
for name, a, b in pairs:
    x, y = open(a, "rb").read(), open(b, "rb").read()
    same = x == y
    print(name, "committed", len(x), "rebuilt", len(y), "identical" if same else "DIFFERENT",
          hashlib.sha256(y).hexdigest()[:12])
    if not same:
        i = next(i for i in range(min(len(x), len(y))) if x[i] != y[i])
        print("  first difference at byte", i, repr(x[i - 40:i + 40]), "v", repr(y[i - 40:i + 40]))
    print("  svg paths", y.count(b"<path"), "has live script", b"requestAnimationFrame" in y,
          "external urls", y.count(b"http://") + y.count(b"https://"))
