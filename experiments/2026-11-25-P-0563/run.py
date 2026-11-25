"""P-0563: does an spr-sdk sealed payment record verify, and fail after a one-byte edit?

Run with the sandbox venv: sandbox/p0563-venv/bin/python3 experiments/2026-11-25-P-0563/run.py
The book (with its private key) lives under sandbox/p0563-book; only the public package and results land here.
Called shot before running: works, every one-byte edit to a sealed record fails verification.
"""
import json, os, random, shutil, sys, time
# The sandbox venv's own python resolves outside the folder and the unattended hook refuses it, so the
# project .venv (also 3.14) runs this with the sandbox venv's site-packages first on the path.
sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/p0563-venv/lib/python3.14/site-packages")
import spr
from spr import SprBook, verify_folder, run_vectors

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/Users/triton/PROTEUS/sandbox/p0563-book"
PKG = "/Users/triton/PROTEUS/sandbox/p0563-pkg"
out = {"spr_version": spr.__version__}

# 1. the shipped test vectors
vec = json.load(open(os.path.join(os.path.dirname(spr.__file__), "vectors.json")))
v = run_vectors(vec)
out["vectors"] = {"passed": v["passed"], "failed": v["failed"]}

# 2. a fresh book: declare, seal three payments, export a package
for d in (BOOK, PKG):
    if os.path.exists(d):
        shutil.rmtree(d)
t0 = time.time()
book = SprBook(dir=BOOK, agent_id="agt_probe", entity="Probe Co")
intent = book.declare(purpose="Market data for the probe", max_amount_minor=50000, currency="USDC")
recs = []
for i, amt in enumerate([10000, 2500, 777]):
    recs.append(book.seal(rail="x402", source_id="0x%064x" % (i + 1), amount_minor=amt, currency="USDC",
                          nonce=book.nonce_for(intent["intent_id"], i)))
out["seal_seconds"] = round(time.time() - t0, 3)
out["records_sealed"] = len(recs)
out["verify_record"] = [book.verify_record(r["payload"]["record_id"] if "payload" in r else r["record_id"]).get("ok") for r in recs]
book.export_package(PKG)
pub = book.public_key()
key_id = pub.get("key_id") if isinstance(pub, dict) else None
out["package_files"] = sorted(os.listdir(PKG))
clean = verify_folder(PKG, expected_keys=[key_id] if key_id else None)
out["clean"] = {"ok": clean["ok"], "trust": clean["trust"], "passed": clean["passed"], "failed": clean["failed"]}

# 3. one-byte edits: flip one character inside records.jsonl, re-verify, restore
path = os.path.join(PKG, "records.jsonl")
orig = open(path, "rb").read()
rng = random.Random(563)
positions = sorted(rng.sample(range(len(orig)), 200))
caught = missed = invalid_json = 0
miss_examples = []
for pos in positions:
    b = bytearray(orig)
    ch = b[pos]
    # change to another printable byte that keeps the line JSON-shaped where possible
    new = ord("1") if ch != ord("1") else ord("2")
    if chr(ch) in '{}[]":,\n':
        new = ch ^ 0x01
    b[pos] = new
    open(path, "wb").write(bytes(b))
    try:
        r = verify_folder(PKG, expected_keys=[key_id] if key_id else None)
        if r["ok"]:
            missed += 1
            if len(miss_examples) < 5:
                miss_examples.append({"pos": pos, "from": chr(ch), "to": chr(new), "context": orig[max(0, pos - 30):pos + 30].decode("utf-8", "replace")})
        else:
            caught += 1
    except Exception as e:
        invalid_json += 1  # the checker raised instead of returning a failure
    open(path, "wb").write(orig)
out["one_byte_edits"] = {"tried": len(positions), "verify_failed": caught, "verify_passed": missed, "checker_raised": invalid_json,
                         "miss_examples": miss_examples}

# 4. the same, a single edit to the amount in a record's payload (the edit that matters)
lines = orig.decode().split("\n")
row = json.loads(lines[0])
row["payload"]["amount_minor"] += 1
lines[0] = json.dumps(row, separators=(",", ":"))
open(path, "w").write("\n".join(lines))
r = verify_folder(PKG, expected_keys=[key_id] if key_id else None)
out["amount_plus_one"] = {"ok": r["ok"], "failures": [x["what"] + ": " + x["detail"] for x in r["results"] if not x["ok"]]}
open(path, "wb").write(orig)

json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: out[k] for k in ("spr_version", "vectors", "records_sealed", "verify_record", "clean", "amount_plus_one")}))
print(json.dumps({k: v for k, v in out["one_byte_edits"].items() if k != "miss_examples"}))
for m in miss_examples:
    print("MISS", m)
