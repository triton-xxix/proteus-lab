"""P-0441: end the hung parallel render (my own processes only: command line must name the cherry project or its chunks)."""
import os, signal, subprocess
out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
me = os.getpid()
for line in out.splitlines():
    pid, _, cmd = line.strip().partition(" ")
    if int(pid) == me:
        continue
    if "/sandbox/p0441/cherry" in cmd and ("render.py" in cmd or "ffmpeg" in cmd or "timed_render.py" in cmd or "multiprocessing" in cmd):
        print("kill", pid, cmd[:120])
        os.kill(int(pid), signal.SIGTERM)
for line in out.splitlines():
    pid, _, cmd = line.strip().partition(" ")
    if "multiprocessing" in cmd and "py312-venv" in cmd:
        print("worker", pid, cmd[:120])
