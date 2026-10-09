"""Run test.html in headless Chrome twice on one profile and print the RESULT lines.
The first run sets rows per repeat to 4 and presses + five times; the second must restore row 5, repeat 1."""
import os
import re
import shutil
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = "/Users/triton/PROTEUS/sandbox/rowkeeper-profile"
shutil.rmtree(PROFILE, ignore_errors=True)
for run in (1, 2):
    p = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
                        "--user-data-dir=" + PROFILE, "--virtual-time-budget=20000", "--dump-dom",
                        "file://" + os.path.join(HERE, "test.html")], capture_output=True, text=True, timeout=120)
    m = re.search(r'id="result">(RESULT[^<]*)', p.stdout)
    print("run %d:" % run, m.group(1) if m else "no result; stderr tail: " + p.stderr[-300:])
