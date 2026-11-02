"""Write bootgpt-teardown/weights.js: weights.bin as a base64 string the bundle can import."""
import base64

blob = open("/Users/triton/PROTEUS/sandbox/bootgpt/weights.bin", "rb").read()
out = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0295/bootgpt-teardown/weights.js"
with open(out, "w") as f:
    f.write("// weights.bin of sandbox/bootgpt, base64 (written by make_weights.py)\n")
    f.write("export default '%s';\n" % base64.b64encode(blob).decode())
print(len(blob), "bytes ->", out)
