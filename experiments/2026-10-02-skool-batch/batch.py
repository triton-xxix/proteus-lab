#!/Users/triton/PROTEUS/sandbox/skool-venv/bin/python
"""Skool transcription batch of 2 Oct 2026: S-07 to S-17 videos, in reading-queue order.
A one-shot launchd job (label com.proteus.skool-batch, plist in this folder, loaded from here,
nothing in ~/Library). Skips videos already transcribed, stops on HALT, stops itself after
10 hours, writes only field-notes/skool/transcripts/ and this folder. Same transcriber as the
29 Sep batch (sandbox/skool_transcript.py: captions first, local whisper fallback)."""
import os, subprocess, sys, time

TP = "/Users/triton/PROTEUS/sandbox/skool_transcript.py"
OUT = "/Users/triton/PROTEUS/field-notes/skool/transcripts"
HERE = os.path.dirname(os.path.abspath(__file__))
STOP_AFTER = 10 * 3600
VIDEOS = [
    ("auto-claude-code-masterclass", "Q_OJ26E5_74"), ("auto-replaced-n8n-with-claude-code", "Vmb1FtsgdjU"),
    ("auto-8-things-claude-code-app-needs", "Bs0ozi7WzR4"), ("auto-write-exactly-like-you", "aHI8OG6gODA"),
    ("brendan-agentic-workflows-claude-code", "mBFaiSoVgwk"), ("brendan-5-claude-skills", "iMWC6mdPS5g"),
    ("auto-scrape-anything-agent", "VAaFsqu5NE8"), ("auto-n8n-apify-scrape", "PxQwzoPmP3M"),
    ("auto-google-maps-contact-scraper", "pKgup8tsPv8"), ("auto-apollo-lead-scraper", "G8kSkA1pWJg"),
    ("auto-linkedin-jobs-scraper", "qNOL9-npdt4"),
    ("brendan-compared-every-ai-caller-platform", "lvS-im-KgRU"), ("brendan-which-ai-caller-platform", "8IyjiZmyh0Q"),
    ("brendan-ai-callers-quicker", "3kJoX7jFzAc"), ("brendan-ai-callers-realistic", "dDPn54zMWDw"),
    ("brendan-voice-prompt-hacks", "uUWwnS8qVQc"),
    ("brendan-livekit-voice-agent-guide", "M81cc543Tf4"), ("brendan-voice-agent-2-years", "6frVIqkaGFs"),
    ("ais-zero-to-first-cc-workflow", "tDGiWn0flK8"), ("ais-10k-agentic-workflows", "vFepZE_wrfg"),
    ("ais-watch-agents-real-time", "62Rfe1w9NBc"),
    ("ais-stop-learning-n8n", "ZeJXI2MAhj0"), ("ais-build-n8n-flows-with-cc", "B6k_vAjndMo"),
    ("ais-build-anything-n8n-cc", "OCO3aq3G0mk"),
    ("ais-imessage", "hHlpVeooPrI"), ("ais-computer", "X6EGzi9qm3E"), ("ais-remote-control", "EqhKw0Oro_k"),
    ("ais-google-cli", "Wu67lLD8bB0"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    log = open(os.path.join(OUT, "_progress.log"), "a")
    log.write("batch 2026-10-02 start %s\n" % time.strftime("%H:%M")); log.flush()
    for slug, vid in VIDEOS:
        if os.path.exists("/Users/triton/PROTEUS/HALT") or time.time() - t0 > STOP_AFTER:
            log.write("batch stopped (HALT or time) %s\n" % time.strftime("%H:%M")); break
        dest = os.path.join(OUT, slug + ".txt")
        if os.path.exists(dest):
            continue
        s = time.time()
        r = subprocess.run([TP, "https://youtu.be/" + vid, "--out", dest], capture_output=True, text=True)
        log.write("%s %s %s %.0fs %s\n" % (time.strftime("%H:%M"), "ok" if r.returncode == 0 else "FAIL", slug,
                                         time.time() - s, (r.stdout.strip() or r.stderr.strip())[-200:].replace("\n", " | ")))
        log.flush()
    log.write("batch 2026-10-02 done %s\n" % time.strftime("%H:%M")); log.close()
    open(os.path.join(HERE, "DONE"), "w").write(time.strftime("%Y-%m-%dT%H:%M:%S"))
    subprocess.run(["/bin/launchctl", "bootout", "gui/%d/com.proteus.skool-batch" % os.getuid()], capture_output=True)


if __name__ == "__main__":
    sys.exit(main())
