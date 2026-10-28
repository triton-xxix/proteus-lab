"""P-0249: the ECMWF IFS ensemble's band for Munich's daily high, beside ICON-EPS (P-0232).

Same capture and score as experiments/2026-10-27-P-0232/capture.py, with the model and the log swapped:
models=ecmwf_ifs025 (51 members), rows to exchange/ecmwf_ens_band.jsonl so step 4 commits them.

  python3 capture.py          append tomorrow's row
  python3 capture.py score    print coverage so far
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("icon", "/Users/triton/PROTEUS/experiments/2026-10-27-P-0232/capture.py")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.LOG = base.ROOT + "/exchange/ecmwf_ens_band.jsonl"
base.URL = base.URL.replace("models=icon_seamless", "models=ecmwf_ifs025")

if __name__ == "__main__":
    base.score() if sys.argv[1:] == ["score"] else base.capture()
