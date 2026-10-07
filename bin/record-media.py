#!/usr/bin/env python3
"""Generated media for the Sixteen Nights record, through the keys Luke named on 7 Oct 2026.

    /Users/triton/PROTEUS/.venv/bin/python3 /Users/triton/PROTEUS/bin/record-media.py <command> ...

    image  <out.png> --prompt "..." [--aspect 16:9] [--size 2K] [--model gemini-3.1-flash-image]
    video  <out.mp4> --prompt "..." --image <still.png> [--seconds 8] [--resolution 1080p] [--aspect 16:9] [--model veo-3.1-fast-generate-preview] [--negative "..."]
    tts    <out.mp3> --text "..." [--voice goT3UYdM9bhm0n2lmKQx] [--model eleven_multilingual_v2] [--speed 1.0]
    music  <out.mp3> --prompt "..." --seconds 95
    sfx    <out.mp3> --prompt "..." --seconds 2

Keys are read at run time through bin/secrets.py (1Password, service account) and never printed or
written. Every call appends one line to <build>/media-ledger.jsonl with the model, the units and an
estimated USD cost at the prices in the bootcamp config of 1 Oct 2026; the provider's bill is the truth.
Spend lands on Luke's accounts, not the Proteus card.
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/bin")
import secrets as S  # noqa: E402

BUILD = "/Users/triton/PROTEUS/sites/builds/sixteen-nights"
LEDGER = BUILD + "/media-ledger.jsonl"
GEM = "https://generativelanguage.googleapis.com/v1beta"
EL = "https://api.elevenlabs.io/v1"
PRICES = {"image": {"gemini-3.1-flash-image": {"1K": 0.067, "2K": 0.101, "4K": 0.151}, "gemini-3-pro-image": {"1K": 0.134, "2K": 0.134, "4K": 0.24}, "gemini-3.1-flash-lite-image": {"1K": 0.0336}},
          "veo_per_second": {"veo-3.1-lite-generate-preview": {"720p": 0.05, "1080p": 0.08}, "veo-3.1-fast-generate-preview": {"720p": 0.1, "1080p": 0.12}, "veo-3.1-generate-preview": {"720p": 0.4, "1080p": 0.4}},
          "tts_per_1k_chars": 0.08, "sfx_per_minute": 0.12, "music_per_minute": 0.15}
VOICE_EDWARD = "goT3UYdM9bhm0n2lmKQx"


def gemini_key():
    return S.get("Google Gemini Api Florist ", "credential", "Tritons World")


def eleven_key():
    return S.get("11 Labs Eleven Labs", "credential", "Tritons World")


def http(url, data=None, headers=None, timeout=300, method=None):
    body = json.dumps(data).encode() if isinstance(data, dict) else data
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method or ("POST" if body is not None else "GET"))
    if isinstance(data, dict):
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read(), dict(e.headers)


def ledger(**row):
    row["at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(LEDGER, "a") as fh:
        fh.write(json.dumps(row) + "\n")
    print("ledger: %s" % {k: v for k, v in row.items() if k in ("tool", "units", "unit", "est_usd", "file")})


def redact(text, key):
    return text.replace(key, "<key>") if key else text


def cmd_image(a):
    key = gemini_key()
    cfg = {"aspectRatio": a.aspect}
    if "lite" not in a.model:
        cfg["imageSize"] = a.size
    parts = []
    for ref in a.ref or []:
        raw = open(ref, "rb").read()
        mime = "image/png" if ref.lower().endswith(".png") else "image/jpeg"
        parts.append({"inlineData": {"mimeType": mime, "data": base64.b64encode(raw).decode()}})
    parts.append({"text": a.prompt})
    body = {"contents": [{"role": "user", "parts": parts}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": cfg}}
    print("Gemini image %s %s %s, %d reference(s): %s..." % (a.model, a.aspect, a.size, len(a.ref or []), a.prompt[:100]))
    status, raw, _ = http("%s/models/%s:generateContent" % (GEM, a.model), body, {"x-goog-api-key": key})
    j = json.loads(raw or b"{}")
    if status != 200:
        sys.exit("Gemini image HTTP %d: %s" % (status, redact(json.dumps(j)[:400], key)))
    cand = (j.get("candidates") or [{}])[0]
    parts = (cand.get("content") or {}).get("parts") or []
    img = next((p for p in parts if p.get("inlineData", {}).get("data")), None)
    if not img:
        said = " ".join(p.get("text", "") for p in parts)[:300]
        sys.exit("no image came back (finish %s). %s" % (cand.get("finishReason"), said))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(base64.b64decode(img["inlineData"]["data"]))
    est = PRICES["image"].get(a.model, {}).get(a.size if "lite" not in a.model else "1K")
    ledger(tool="gemini:" + a.model, units=1, unit="image", est_usd=est, file=os.path.relpath(a.out, BUILD), mime=img["inlineData"].get("mimeType"))
    print("saved %s (%d KB)" % (a.out, os.path.getsize(a.out) // 1024))


def cmd_video(a):
    key = gemini_key()
    inst = {"prompt": a.prompt}
    if a.image:
        raw = open(a.image, "rb").read()
        mime = "image/png" if a.image.lower().endswith(".png") else "image/jpeg"
        inst["image"] = {"bytesBase64Encoded": base64.b64encode(raw).decode(), "mimeType": mime}
    params = {"aspectRatio": a.aspect, "durationSeconds": a.seconds, "resolution": a.resolution, "personGeneration": "allow_adult"}
    if a.negative and "lite" not in a.model:
        params["negativePrompt"] = a.negative
    elif a.negative:
        inst["prompt"] = inst["prompt"].strip() + "\nAvoid: " + a.negative.strip() + "."
    rate = PRICES["veo_per_second"].get(a.model, {}).get(a.resolution)
    print("Veo %s %ds %s %s (est $%.2f): %s..." % (a.model, a.seconds, a.resolution, a.aspect, (rate or 0) * a.seconds, a.prompt[:100]))
    status, raw, _ = http("%s/models/%s:predictLongRunning" % (GEM, a.model), {"instances": [inst], "parameters": params}, {"x-goog-api-key": key})
    j = json.loads(raw or b"{}")
    if status != 200:
        sys.exit("Veo HTTP %d: %s" % (status, redact(json.dumps(j)[:400], key)))
    op = j["name"]
    print("started %s, waiting" % op, end="", flush=True)
    t0 = time.time()
    done = None
    while time.time() - t0 < 15 * 60:
        time.sleep(10)
        print(".", end="", flush=True)
        st, pr, _ = http("%s/%s" % (GEM, op), None, {"x-goog-api-key": key})
        pj = json.loads(pr or b"{}")
        if pj.get("error"):
            sys.exit("\nVeo failed: %s" % redact(json.dumps(pj["error"])[:400], key))
        if pj.get("done"):
            done = pj
            break
    if not done:
        sys.exit("\nstill running after 15 minutes: %s" % op)
    resp = done.get("response") or {}
    samples = (resp.get("generateVideoResponse") or {}).get("generatedSamples") or resp.get("generatedVideos") or []
    video = (samples[0] if samples else {}).get("video") or {}
    uri = video.get("uri") or video.get("downloadUri")
    if not uri:
        sys.exit("\nno video in the response: %s" % redact(json.dumps(resp)[:500], key))
    st, data, _ = http(uri, None, {"x-goog-api-key": key}, timeout=600)
    if st != 200:
        sys.exit("\ndownload HTTP %d" % st)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(data)
    ledger(tool="veo:" + a.model, units=a.seconds, unit="seconds", est_usd=(rate or 0) * a.seconds, resolution=a.resolution, file=os.path.relpath(a.out, BUILD))
    print("\nsaved %s (%d KB, %ds to render)" % (a.out, len(data) // 1024, int(time.time() - t0)))


def cmd_tts(a):
    key = eleven_key()
    body = {"text": a.text, "model_id": a.model, "voice_settings": {"stability": 0.55, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True, "speed": a.speed}}
    status, raw, _ = http("%s/text-to-speech/%s?output_format=mp3_44100_128" % (EL, a.voice), body, {"xi-api-key": key})
    if status != 200:
        sys.exit("ElevenLabs TTS HTTP %d: %s" % (status, redact(raw[:300].decode("utf8", "replace"), key)))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(raw)
    ledger(tool="elevenlabs:tts:" + a.model, units=len(a.text), unit="characters", est_usd=round(len(a.text) / 1000 * PRICES["tts_per_1k_chars"], 4), voice=a.voice, file=os.path.relpath(a.out, BUILD))
    print("saved %s (%d KB, %d chars)" % (a.out, len(raw) // 1024, len(a.text)))


def cmd_music(a):
    key = eleven_key()
    body = {"prompt": a.prompt, "music_length_ms": int(a.seconds * 1000)}
    status, raw, hdr = http("%s/music?output_format=mp3_44100_128" % EL, body, {"xi-api-key": key}, timeout=600)
    if status != 200:
        sys.exit("ElevenLabs music HTTP %d: %s" % (status, redact(raw[:300].decode("utf8", "replace"), key)))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(raw)
    ledger(tool="elevenlabs:music", units=a.seconds, unit="seconds", est_usd=round(a.seconds / 60 * PRICES["music_per_minute"], 3), file=os.path.relpath(a.out, BUILD))
    print("saved %s (%d KB)" % (a.out, len(raw) // 1024))


def cmd_sfx(a):
    key = eleven_key()
    body = {"text": a.prompt, "duration_seconds": a.seconds, "prompt_influence": 0.5}
    status, raw, _ = http("%s/sound-generation?output_format=mp3_44100_128" % EL, body, {"xi-api-key": key}, timeout=300)
    if status != 200:
        sys.exit("ElevenLabs SFX HTTP %d: %s" % (status, redact(raw[:300].decode("utf8", "replace"), key)))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "wb").write(raw)
    ledger(tool="elevenlabs:sfx", units=a.seconds, unit="seconds", est_usd=round(a.seconds / 60 * PRICES["sfx_per_minute"], 3), file=os.path.relpath(a.out, BUILD))
    print("saved %s (%d KB)" % (a.out, len(raw) // 1024))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("image"); i.add_argument("out"); i.add_argument("--prompt", required=True); i.add_argument("--aspect", default="16:9"); i.add_argument("--size", default="2K"); i.add_argument("--model", default="gemini-3.1-flash-image"); i.add_argument("--ref", action="append", help="reference image, repeatable")
    v = sub.add_parser("video"); v.add_argument("out"); v.add_argument("--prompt", required=True); v.add_argument("--image"); v.add_argument("--seconds", type=int, default=8, choices=[4, 6, 8]); v.add_argument("--resolution", default="1080p"); v.add_argument("--aspect", default="16:9"); v.add_argument("--model", default="veo-3.1-fast-generate-preview"); v.add_argument("--negative")
    t = sub.add_parser("tts"); t.add_argument("out"); t.add_argument("--text", required=True); t.add_argument("--voice", default=VOICE_EDWARD); t.add_argument("--model", default="eleven_multilingual_v2"); t.add_argument("--speed", type=float, default=1.0)
    m = sub.add_parser("music"); m.add_argument("out"); m.add_argument("--prompt", required=True); m.add_argument("--seconds", type=float, default=95)
    s = sub.add_parser("sfx"); s.add_argument("out"); s.add_argument("--prompt", required=True); s.add_argument("--seconds", type=float, default=2)
    a = p.parse_args()
    {"image": cmd_image, "video": cmd_video, "tts": cmd_tts, "music": cmd_music, "sfx": cmd_sfx}[a.cmd](a)


if __name__ == "__main__":
    main()
