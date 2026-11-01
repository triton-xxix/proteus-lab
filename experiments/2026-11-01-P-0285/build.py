"""P-0285: build bootgpt in sandbox/bootgpt without build.sh (no cd allowed), report sizes.

Runs corpus_gen.py and train.py with the sandbox folder as cwd, assembles boot.asm with the
official NASM 2.16.03 macOS release, concatenates disk.img the way build.sh does, and writes
results.json beside this script.
"""
import json
import os
import runpy
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SB = Path("/Users/triton/PROTEUS/sandbox/bootgpt")
NASM = "/Users/triton/PROTEUS/sandbox/nasm/nasm-2.16.03/nasm"

os.chdir(SB)
os.chmod(NASM, 0o755)  # zipfile.extractall drops the execute bit
out = {}
if not (SB / "weights.bin").exists():
    t = time.time()
    runpy.run_path("corpus_gen.py", run_name="__main__")
    out["corpus_s"] = round(time.time() - t, 1)
    t = time.time()
    runpy.run_path("train.py", run_name="__main__")
    out["train_s"] = round(time.time() - t, 1)
out["corpus_bytes"] = (SB / "corpus.txt").stat().st_size
out["weights_bytes"] = (SB / "weights.bin").stat().st_size

r = subprocess.run([NASM, "-f", "bin", "boot.asm", "-o", "boot.bin"], capture_output=True, text=True)
out["nasm_rc"] = r.returncode
out["nasm_err"] = r.stderr[-500:]
if r.returncode == 0:
    boot = (SB / "boot.bin").read_bytes()
    out["boot_bytes"] = len(boot)
    out["boot_sig_55aa"] = boot[-2:] == b"\x55\xaa"
    # code bytes before the zero padding that runs up to the signature
    body = boot[:510].rstrip(b"\x00")
    out["boot_code_bytes_upper_bound"] = len(body)
    w = (SB / "weights.bin").read_bytes()
    (SB / "disk.img").write_bytes(boot + w)
    out["disk_img_bytes"] = len(boot) + len(w)
    out["data_sectors"] = -(-len(w) // 512)

(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
