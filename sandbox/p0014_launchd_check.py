"""P-0014 hygiene: is the poller's launchd job still loaded? Read-only (launchctl print)."""
import os
import subprocess

label = "com.proteus.p0014"
r = subprocess.run(["/bin/launchctl", "print", "gui/%d/%s" % (os.getuid(), label)], capture_output=True, text=True)
print("rc", r.returncode)
print((r.stdout or r.stderr).strip()[:400])
print("loaded" if r.returncode == 0 else "not loaded")
