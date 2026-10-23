#!/usr/bin/env python3
"""P-0201: does librosa's pYIN recover a synthetic sung melody within 50 cents on 90% of voiced frames?

Synthetic "singer": a 14-note melody in a baritone-to-tenor range, each note a harmonic series with
1/n amplitudes, 5.5 Hz vibrato of +-30 cents, a gentle onset and release, breath gaps between phrases,
plus pink-ish noise at -30 dB. Ground truth is known per sample, so per frame.
Run with the Python 3.12 sandbox venv (librosa lives there):
  /Users/triton/PROTEUS/sandbox/py312-venv/bin/python3 /Users/triton/PROTEUS/experiments/2026-10-23-P-0201/pyin_test.py
"""
import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 22050
HOP = 256
FRAME = 2048

# (midi, seconds); 0 midi = rest
MELODY = [(57, 0.5), (60, 0.4), (62, 0.4), (64, 0.6), (0, 0.3), (62, 0.4), (60, 0.4), (57, 0.7),
          (0, 0.4), (65, 0.4), (67, 0.4), (69, 0.5), (67, 0.4), (64, 0.8), (0, 0.3), (72, 0.6), (69, 0.9)]


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def synth(seed=7):
    rng = np.random.default_rng(seed)
    pieces, truth = [], []
    for midi, dur in MELODY:
        n = int(dur * SR)
        t = np.arange(n) / SR
        if midi == 0:
            pieces.append(np.zeros(n))
            truth.append(np.zeros(n))
            continue
        base = midi_hz(midi)
        cents = 30 * np.sin(2 * np.pi * 5.5 * t + rng.uniform(0, 2 * np.pi))
        f = base * 2 ** (cents / 1200)
        phase = 2 * np.pi * np.cumsum(f) / SR
        y = np.zeros(n)
        for h in range(1, 9):
            y += (1.0 / h) * np.sin(h * phase)
        env = np.ones(n)
        a = int(0.03 * SR)
        env[:a] = np.linspace(0, 1, a)
        env[-a:] = np.linspace(1, 0, a)
        pieces.append(y * env * 0.3)
        truth.append(f)
    y = np.concatenate(pieces)
    tr = np.concatenate(truth)
    noise = rng.standard_normal(len(y))
    noise = np.cumsum(noise) * 0.02  # crude pink-ish tilt
    noise -= np.convolve(noise, np.ones(64) / 64, mode="same")
    y = y + noise * (10 ** (-30 / 20))
    return y.astype(np.float32), tr


def main():
    import librosa
    y, tr = synth()
    t0 = time.time()
    f0, vflag, vprob = librosa.pyin(y, fmin=80, fmax=800, sr=SR, frame_length=FRAME, hop_length=HOP)
    elapsed = time.time() - t0
    centres = np.arange(len(f0)) * HOP  # librosa centres frames at hop*i with centre=True
    truth_frames = np.array([tr[min(i, len(tr) - 1)] for i in centres])
    # a frame is "voiced in truth" when its centre sample is inside a note and at least 40 ms from an edge
    inside = truth_frames > 0
    edge = np.zeros_like(inside)
    margin = int(0.04 * SR / HOP)
    changes = np.flatnonzero(np.diff(inside.astype(int)) != 0)
    for c in changes:
        edge[max(0, c - margin):c + margin + 1] = True
    voiced_core = inside & ~edge
    with np.errstate(divide="ignore", invalid="ignore"):
        cents_err = 1200 * np.log2(f0 / np.where(truth_frames > 0, truth_frames, np.nan))
    ok = voiced_core & vflag & (np.abs(cents_err) <= 50)
    n_core = int(voiced_core.sum())
    hit = int(ok.sum())
    missed_voicing = int((voiced_core & ~vflag).sum())
    octave = int((voiced_core & vflag & (np.abs(np.abs(cents_err) - 1200) <= 50)).sum())
    false_voiced = int((~inside & vflag).sum())
    unvoiced_frames = int((~inside).sum())
    abs_err = np.abs(cents_err[voiced_core & vflag])
    res = {
        "frames": int(len(f0)),
        "voiced_core_frames": n_core,
        "within_50_cents": hit,
        "within_50_cents_pct": round(100 * hit / n_core, 1),
        "within_50_cents_pct_all_voiced_incl_edges": round(100 * int((inside & vflag & (np.abs(cents_err) <= 50)).sum()) / int(inside.sum()), 1),
        "voicing_missed": missed_voicing,
        "octave_errors": octave,
        "false_voiced_of_unvoiced": [false_voiced, unvoiced_frames],
        "median_abs_cents": round(float(np.median(abs_err)), 2),
        "p95_abs_cents": round(float(np.percentile(abs_err, 95)), 2),
        "audio_seconds": round(len(y) / SR, 2),
        "pyin_seconds": round(elapsed, 2),
        "librosa": librosa.__version__,
        "settings": {"sr": SR, "hop": HOP, "frame": FRAME, "fmin": 80, "fmax": 800, "vibrato_cents": 30, "noise_db": -30},
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(res, fh, indent=1)
    for k, v in res.items():
        print(k, v)


if __name__ == "__main__":
    main()
