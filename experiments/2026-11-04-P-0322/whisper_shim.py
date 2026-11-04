#!/usr/bin/env python3
"""P-0322 shim: accepts the openai-whisper CLI flags mcp-video-analyzer passes
(<audio> --output_format json --model M --output_dir D [--language L] [--initial_prompt P] ...)
and runs whisper.cpp's whisper-cli instead, then writes <D>/<base>.json in openai-whisper's shape
({"text", "segments": [{"start", "end", "text"}]}). The --model name is ignored: whisper.cpp needs a
ggml file, so the model is P0322_GGML or sandbox/skool-tools/models/ggml-base.en.bin."""
import json
import os
import subprocess
import sys

args = sys.argv[1:]
audio = args[0]
opts = {}
i = 1
while i < len(args):
    if args[i].startswith("--") and i + 1 < len(args):
        opts[args[i][2:]] = args[i + 1]
        i += 2
    else:
        i += 1
out_dir = opts.get("output_dir", os.path.dirname(audio))
base = os.path.splitext(os.path.basename(audio))[0]
model = os.environ.get("P0322_GGML", "/Users/triton/PROTEUS/sandbox/skool-tools/models/ggml-base.en.bin")
prefix = os.path.join(out_dir, base + ".wcpp")
cmd = ["/usr/local/bin/whisper-cli", "-m", model, "-f", audio, "-oj", "-of", prefix, "-np"]
if opts.get("language"):
    cmd += ["-l", opts["language"]]
if opts.get("initial_prompt"):
    cmd += ["--prompt", opts["initial_prompt"]]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
raw = json.load(open(prefix + ".json", encoding="utf-8"))
segs = [{"start": s["offsets"]["from"] / 1000, "end": s["offsets"]["to"] / 1000, "text": s["text"]}
        for s in raw.get("transcription", [])]
json.dump({"text": " ".join(s["text"].strip() for s in segs), "segments": segs},
          open(os.path.join(out_dir, base + ".json"), "w", encoding="utf-8"))
os.remove(prefix + ".json")
