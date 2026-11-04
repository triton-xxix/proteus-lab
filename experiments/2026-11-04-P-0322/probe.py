"""P-0322 driver: make a known-text captionless clip with macOS say(1) and ffmpeg, run mcp-video-analyzer
on it through run.mjs (OPENAI_API_KEY removed, WHISPER_BIN = whisper_shim.py), score word match to the script.

    python3 -I experiments/2026-11-04-P-0322/probe.py
"""
import difflib
import json
import os
import re
import subprocess

EXP = "/Users/triton/PROTEUS/experiments/2026-11-04-P-0322"
SB = "/Users/triton/PROTEUS/sandbox/mcpva"
SCRIPT = ("The forecast for Paris says the high will be fourteen degrees on Thursday. Meteo France runs a little "
          "warm, and the German model runs a little cold. Links to old videos on Hacker News die at about two and "
          "a half points a year.")
aiff, mp4 = SB + "/p0322-clip.aiff", SB + "/p0322-clip.mp4"
os.chmod(EXP + "/whisper_shim.py", 0o755)
subprocess.run(["/usr/bin/say", "-o", aiff, SCRIPT], check=True)
subprocess.run(["/usr/local/bin/ffmpeg", "-loglevel", "error", "-y", "-i", aiff, "-f", "lavfi", "-i",
                "color=c=black:s=320x240:r=10", "-shortest", "-c:v", "libx264", "-c:a", "aac", mp4], check=True)
p = subprocess.run(["node", EXP + "/run.mjs", mp4, "--detail", "brief", "--fields",
                    "transcript,metadata", "--force-refresh"], capture_output=True, text=True, timeout=400)
open(EXP + "/stderr.txt", "w").write(p.stderr[-4000:])
try:
    out = json.loads(p.stdout)
except json.JSONDecodeError:
    out = {"raw_stdout": p.stdout[-2000:]}
json.dump(out, open(EXP + "/output.json", "w"), indent=1)
tr = out.get("transcript") or []
text = " ".join(e.get("text", "") for e in tr) if isinstance(tr, list) else str(tr)


def words(s):
    return re.findall(r"[a-z]+", s.lower())


ref, hyp = words(SCRIPT), words(text)
sm = difflib.SequenceMatcher(a=ref, b=hyp)
match = sum(b.size for b in sm.get_matching_blocks()) / len(ref)
fetches = json.load(open(EXP + "/fetches.json")) if os.path.exists(EXP + "/fetches.json") else None
res = {"exit": p.returncode, "transcript_entries": len(tr) if isinstance(tr, list) else None,
       "transcript": text, "ref_words": len(ref), "hyp_words": len(hyp), "word_match": round(match, 3),
       "fetches": fetches, "warnings": out.get("warnings")}
print(json.dumps(res, indent=1))
json.dump(res, open(EXP + "/results.json", "w"), indent=1)
