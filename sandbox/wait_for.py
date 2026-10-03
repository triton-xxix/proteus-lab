"""Wait until a string appears in a file, or a timeout passes. Usage: wait_for.py FILE STRING SECONDS"""
import sys, time, pathlib
path, needle, limit = pathlib.Path(sys.argv[1]), sys.argv[2], float(sys.argv[3])
t0 = time.time()
while time.time() - t0 < limit:
    try:
        if needle in path.read_text():
            print(f"found after {int(time.time() - t0)}s")
            sys.exit(0)
    except FileNotFoundError:
        pass
    time.sleep(10)
print(f"timeout after {int(limit)}s")
sys.exit(1)
