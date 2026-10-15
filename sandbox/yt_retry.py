#!/Users/triton/PROTEUS/sandbox/skool-venv/bin/python
"""Wait for YouTube to lift its IP block on captions, then run the queued YouTube lists slowly.

15 Oct 2026: a burst of caption fetches got this Mac IpBlocked (youtube_transcript_api, yt-dlp subs
and the watch page's own timedtext all answered 429). Test one known video each hour, up to
MAX_TRIES; once it answers, run each TSV through skool_batch_transcribe.py captions-only with a
long pause. Never falls back to whisper.

    yt_retry.py LIST.tsv [LIST2.tsv ...]
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TEST = "74NPuvEt1Xs"
WAIT, MAX_TRIES, PAUSE = 3600, 5, "20"


def unblocked():
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        YouTubeTranscriptApi().fetch(TEST, languages=["en"])
        return True
    except Exception as exc:
        print(time.strftime("%H:%M"), "still blocked:", type(exc).__name__, flush=True)
        return False


for attempt in range(MAX_TRIES):
    time.sleep(WAIT)
    if unblocked():
        break
else:
    sys.exit("gave up after %d hours; lists left queued: %s" % (MAX_TRIES, " ".join(sys.argv[1:])))

env = dict(os.environ, SKOOL_CAPTIONS_ONLY="1")
for tsv in sys.argv[1:]:
    print(time.strftime("%H:%M"), "running", tsv, flush=True)
    subprocess.run([os.path.join(HERE, "skool_batch_transcribe.py"), tsv, PAUSE], env=env)
print(time.strftime("%H:%M"), "all lists done", flush=True)
