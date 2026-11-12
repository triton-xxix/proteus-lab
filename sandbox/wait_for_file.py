"""Blocks until a file exists (or a timeout), then prints its size. For waiting on a background job
in an unattended run without polling.
python3 /Users/triton/PROTEUS/sandbox/wait_for_file.py PATH [seconds, default 540]"""
import os
import sys
import time

path = sys.argv[1]
limit = float(sys.argv[2]) if len(sys.argv) > 2 else 540
t0 = time.time()
while not os.path.exists(path) and time.time() - t0 < limit:
    time.sleep(3)
time.sleep(1)
print("EXISTS %d bytes" % os.path.getsize(path) if os.path.exists(path) else "TIMEOUT", "after %.0f s" % (time.time() - t0))
