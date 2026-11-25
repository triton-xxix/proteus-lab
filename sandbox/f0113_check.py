"""F-0113 check: the late-fire floor in bin/probe.py apply_late_floor."""
import importlib.util
import sys
from datetime import datetime, timedelta, timezone

spec = importlib.util.spec_from_file_location("probe", "/Users/triton/PROTEUS/bin/probe.py")
probe = importlib.util.module_from_spec(spec)
sys.argv = ["probe.py"]
spec.loader.exec_module(probe)

n = datetime(2026, 11, 25, 7, 4, tzinfo=timezone.utc)
fails = 0
cases = [
    ("25 Nov late fire, deadline 06:41 past", n.replace(hour=6, minute=41), n + timedelta(minutes=20)),
    ("deadline 5 min ahead", n + timedelta(minutes=5), n + timedelta(minutes=20)),
    ("deadline 8 min ahead kept", n + timedelta(minutes=8), n + timedelta(minutes=8)),
    ("normal night 70 min ahead kept", n + timedelta(minutes=70), n + timedelta(minutes=70)),
]
for name, dl, want in cases:
    got, how = probe.apply_late_floor(dl, n, "nightly preflight x plus 80 min")
    ok = got == want
    fails += not ok
    print("%s %s: %s (%s)" % ("OK" if ok else "FAIL", name, got.strftime("%H:%M"), how))
print("fails", fails)
