#!/Users/triton/PROTEUS/sandbox/skool-venv/bin/python
"""Run skool_transcript.py over a list of (slug, url) pairs, skipping ones already done.
Writes field-notes/skool/transcripts/<slug>.txt and a progress line per video to
field-notes/skool/transcripts/_progress.log. Captions first; whisper fallback is slow (about a
third of real time on this Intel Mac) so the list is ordered by value, not length."""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/Users/triton/PROTEUS/field-notes/skool/transcripts"
TP = os.path.join(HERE, "skool_transcript.py")

VIDEOS = [
    ("ais-master-95-of-claude-code", "https://youtu.be/saggDHHnmtQ"),
    ("ais-claude-code-skills-beginner-to-pro", "https://youtu.be/zKBPwDpBfhs"),
    ("ais-skill-creator-update", "https://youtu.be/RAZVk5NPNtE"),
    ("ais-executive-assistant-27-mins", "https://youtu.be/mi4hcipESKQ"),
    ("ais-loop-feature", "https://youtu.be/OUyfxhFtGCo"),
    ("ais-scheduled-tasks", "https://youtu.be/BlNJFa3Btm8"),
    ("ais-auto-mode-not-bypass", "https://youtu.be/pkSxISewcw8"),
    ("ais-memory-2-auto-dream", "https://youtu.be/LrgfmZkl3nc"),
    ("ais-firecrawl-mcp", "https://youtu.be/4efAzBiTeVo"),
    ("ais-trigger-dev", "https://youtu.be/UGIZnh6HNLc"),
    ("ais-n8n-self-healing", "https://youtu.be/uUEa6K-FLB8"),
    ("ais-paperclip", "https://youtu.be/HJ-dwefABss"),
]

os.makedirs(OUT, exist_ok=True)
log = open(os.path.join(OUT, "_progress.log"), "a")
for slug, url in VIDEOS:
    dest = os.path.join(OUT, slug + ".txt")
    if os.path.exists(dest):
        continue
    t0 = time.time()
    r = subprocess.run([TP, url, "--out", dest], capture_output=True, text=True)
    how = "ok" if r.returncode == 0 else "FAIL"
    line = "%s %s %s %.0fs %s\n" % (time.strftime("%H:%M"), how, slug, time.time() - t0,
                                   (r.stdout.strip() or r.stderr.strip())[-200:].replace("\n", " | "))
    log.write(line); log.flush()
    sys.stdout.write(line)
log.write("batch done %s\n" % time.strftime("%H:%M"))
