"""P-0441: end the orphaned workers of the hung render (parent pid 87409 or already re-parented, py312-venv multiprocessing only)."""
import os, signal, subprocess
out = subprocess.run(["ps", "-axo", "pid=,ppid=,command="], capture_output=True, text=True).stdout
for line in out.splitlines():
    parts = line.split(None, 2)
    if len(parts) < 3:
        continue
    pid, ppid, cmd = int(parts[0]), int(parts[1]), parts[2]
    if "py312-venv" in cmd and "multiprocessing" in cmd and (ppid == 87409 or ppid == 1) and pid in range(87411, 87436):
        print("kill", pid, ppid, cmd[:80])
        os.kill(pid, signal.SIGTERM)
    elif "ffmpeg" in cmd and "rawvideo" in cmd:
        print("ffmpeg left", pid, ppid, cmd[:100])
