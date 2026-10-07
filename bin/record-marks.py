#!/usr/bin/env python3
"""Data marks for the Sixteen Nights film: short sounds made from the record, not downloaded.

    /Users/triton/PROTEUS/sandbox/py312-venv/bin/python /Users/triton/PROTEUS/bin/record-marks.py [outdir]

Writes, at 48 kHz mono, into <outdir> (default sites/builds/sixteen-nights/film/media/marks):
  tick.wav     one soft wooden tick (one per nightly run and per clock second)
  thud.wav     one low thud (one per killed probe)
  cross.wav    one brighter tone (where the Grinder crosses back above £1,000)
  resolve.wav  a low chord that settles (the last frame)
  marks.json   where each mark lands in film time, derived from STORYBOARD frame times and record.json
Pure numpy synthesis; every parameter is fixed, so the files are reproducible byte for byte.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "sites/builds/sixteen-nights/film/media/marks"
SR = 48000


def noise(n, seed):
    """Deterministic white noise without numpy.random (its C extension is broken in this venv)."""
    i = np.arange(n, dtype=np.float64) + seed * 1000.0
    return (np.sin(i * 12.9898 + seed) * 43758.5453) % 1.0 * 2.0 - 1.0


def env(n, attack, decay, curve=4.0):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    d = np.exp(-t / max(decay, 1e-4) * curve)
    return a * d


def tick():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 1850 * t) * 0.6 + np.sin(2 * np.pi * 3700 * t) * 0.2
    hiss = noise(n, 7) * 0.25
    return (body + hiss) * env(n, 0.001, 0.03) * 0.5


def thud():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 110 * np.exp(-t * 6) + 48
    phase = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(phase) * 0.9 + np.sin(phase * 0.5) * 0.3
    knock = noise(n, 11) * 0.15 * env(n, 0.0005, 0.02)
    return (body * env(n, 0.002, 0.35, 3.0) + knock) * 0.8


def cross():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    tone = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((440, 0.5), (660, 0.3), (880, 0.18), (1320, 0.08)))
    shimmer = np.sin(2 * np.pi * 5.5 * t) * 0.08 + 1
    return tone * shimmer * env(n, 0.01, 0.6, 3.0) * 0.5


def resolve():
    n = int(4.0 * SR)
    t = np.arange(n) / SR
    chord = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((55, 0.5), (110, 0.4), (164.8, 0.25), (220, 0.2), (329.6, 0.1)))
    slow = 1 - np.exp(-t * 1.2)
    tail = np.exp(-np.clip(t - 2.4, 0, None) * 1.6)
    return chord * slow * tail * 0.45


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else OUT
    os.makedirs(out, exist_ok=True)
    for name, fn in (("tick", tick), ("thud", thud), ("cross", cross), ("resolve", resolve)):
        y = fn().astype(np.float32)
        y = y / max(1e-6, np.abs(y).max()) * 0.8
        sf.write(os.path.join(out, name + ".wav"), y, SR, subtype="PCM_16")
    rec = json.load(open(ROOT + "sites/builds/sixteen-nights/record.json"))
    # Film-time placement, from the storyboard: clock ticks in frame 01 (0-4s); the field (48-58s) gets one
    # tick per nightly run spread over its 8s fill; thuds on the four falls (58-62s); cross where the Grinder
    # climbs past £1,000 inside frame 06 (27-33s); resolve at the start of frame 15 (87s).
    nights = rec["nights"]
    marks = {"tick": [0.2, 1.2, 2.2, 3.2] + [round(48.6 + 8.0 * i / max(nights - 1, 1), 2) for i in range(nights)],
             "thud": [58.4, 58.9, 59.5, 60.2][: rec["probes"]["killed"]],
             "cross": [], "resolve": [87.0]}
    path = rec["grinder"]["path"]
    start = rec["grinder"]["stats"]["start"]
    low_i = min(range(len(path)), key=lambda i: path[i]["bankroll"])
    # frame 05 covers path[0..low_i] over 5.5s from 20.5s; frame 06 covers path[low_i..end] over 5.0s from 27.3s
    for i in range(low_i + 1, len(path)):
        if path[i - 1]["bankroll"] < start <= path[i]["bankroll"]:
            frac = (i - low_i) / max(len(path) - 1 - low_i, 1)
            marks["cross"].append(round(27.3 + 5.0 * frac, 2))
            break
    json.dump(marks, open(os.path.join(out, "marks.json"), "w"), indent=1)
    print("marks written to %s: %s" % (out, {k: len(v) for k, v in marks.items()}))


if __name__ == "__main__":
    main()
