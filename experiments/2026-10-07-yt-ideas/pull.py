"""Keyless: latest uploads per channel -> transcripts in sandbox/yt_ideas/transcripts/<group>/.

    /Users/triton/PROTEUS/sandbox/skool-venv/bin/python /Users/triton/PROTEUS/sandbox/yt_ideas/pull.py

Run with the skool venv (youtube_transcript_api). Transcripts stay in the sandbox (gitignored):
other people's words, read by child agents, never committed.
"""
import json, os, re, time, urllib.request
from youtube_transcript_api import YouTubeTranscriptApi

HERE = "/Users/triton/PROTEUS/sandbox/yt_ideas"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36",
      "Accept-Language": "en-GB,en;q=0.9"}
SKIP = re.compile(r"masterclass|zoom event|live event|q&a|shorts|giveaway|update|subscribe|announc", re.I)
DONE = {"vSP9pRiRoNY", "8WvaoS5AyAU", "izChxo_4ZPs", "5bVFcDkciTA", "86M1nLZBqOo", "53oiIN5VxoE"}
GROUPS = {
    "A-quantified-strategies": [("@QuantifiedStrategies", 16)],
    "B-kevin-davey": [("@AlgoTradingWithKevinDavey", 12)],
    "C-testers": [("@Algovibes", 6), ("@StatOasis", 6), ("@deltatrendtrading", 4)],
    "D-systematic-pros": [("@TopTradersUnplugged", 4), ("@neurotrader888", 4), ("@memlabs-research", 4)],
}


def walk(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                yield v
            yield from walk(v, key)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)


def uploads(handle):
    html = urllib.request.urlopen(urllib.request.Request("https://www.youtube.com/%s/videos" % handle, headers=UA), timeout=30).read().decode("utf-8", "replace")
    d = json.loads(re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S).group(1))
    out = []
    for lv in walk(d.get("contents", {}), "lockupViewModel"):
        md = lv.get("metadata", {}).get("lockupMetadataViewModel", {})
        meta = [p.get("text", {}).get("content", "") for mp in walk(md, "metadataParts") for p in mp]
        out.append({"id": lv.get("contentId"), "title": md.get("title", {}).get("content", ""), "meta": " / ".join(meta[-2:])})
    return out


def main():
    api = YouTubeTranscriptApi()
    index = {}
    for group, chans in GROUPS.items():
        os.makedirs(os.path.join(HERE, "transcripts", group), exist_ok=True)
        index[group] = []
        for handle, n in chans:
            try:
                vids = uploads(handle)
            except Exception as e:
                print("ERR list", handle, e)
                continue
            # Top Traders Unplugged: the Systematic Investor series only (trend followers talking shop)
            if handle == "@TopTradersUnplugged":
                vids = [v for v in vids if "Systematic Investor" in v["title"]]
            picked = [v for v in vids if v["id"] not in DONE and not SKIP.search(v["title"])][:n]
            for v in picked:
                path = os.path.join(HERE, "transcripts", group, v["id"] + ".txt")
                if not os.path.exists(path):
                    try:
                        segs = api.fetch(v["id"], languages=["en", "en-GB", "en-US"])
                        rows = [(s.start, s.text) for s in segs]
                        with open(path, "w") as fh:
                            fh.write("# %s\n# channel %s | video %s | https://www.youtube.com/watch?v=%s | %s\n\n" % (v["title"], handle, v["id"], v["id"], v["meta"]))
                            fh.write("\n".join("[%02d:%02d] %s" % (int(t) // 60, int(t) % 60, x) for t, x in rows))
                        v["words"] = sum(len(x.split()) for _, x in rows)
                    except Exception as e:
                        v["error"] = type(e).__name__
                        print("  no transcript", v["id"], type(e).__name__)
                    time.sleep(1.5)
                v["channel"] = handle
                index[group].append(v)
                print(group, handle, v["id"], v.get("words", v.get("error", "cached")), v["title"][:70], flush=True)
    json.dump(index, open(os.path.join(HERE, "index.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
