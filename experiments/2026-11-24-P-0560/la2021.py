"""P-0560: P-0559's speaker-split no-model score on ASVspoof 2021 LA (codec and transmission channels).

150 bonafide + 150 spoof from SpeechAntiSpoofingBenchmarks/ASVspoof2021_LA test (HF datasets-server /rows,
40 pages spread across 181,566 rows), P-0546's feats and eer, robust median/MAD profile fit on bonafide
from half the speakers, tested on the other half's bonafide plus all spoof, five seeds. Own audio cache.

    sandbox/py312-venv/bin/python la2021.py
"""
import importlib.util, json, sys, time, urllib.parse
from collections import Counter
from pathlib import Path
import numpy as np
import librosa

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b", "/Users/triton/PROTEUS/experiments/2026-11-23-P-0546/sear_baseline.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
DS = "SpeechAntiSpoofingBenchmarks/ASVspoof2021_LA"
AUD = Path("/Users/triton/PROTEUS/sandbox/p0560-audio")
AUD.mkdir(parents=True, exist_ok=True)
N = 150
TOTAL = 181566


def score(X, lab, fit, test):
    med = np.median(X[fit], axis=0)
    mad = np.median(np.abs(X[fit] - med), axis=0) * 1.4826 + 1e-9
    s = np.abs((X - med) / mad).mean(axis=1)
    return float(b.eer(s[test], lab[test]))


def main():
    if Path("/Users/triton/PROTEUS/HALT").exists():
        print("HALT")
        return 1
    t0 = time.time()
    picked = {0: [], 1: []}
    per_page = {0: 6, 1: 4}  # spread both classes across the file
    for off in range(0, TOTAL - 100, TOTAL // 40):
        if len(picked[0]) >= N and len(picked[1]) >= N:
            break
        q = urllib.parse.urlencode({"dataset": DS, "config": "default", "split": "test", "offset": off, "length": 100})
        took = Counter()
        page = None
        for wait in (0, 20, 45):
            time.sleep(wait or 1.5)
            try:
                page = b.get("https://datasets-server.huggingface.co/rows?" + q)
                break
            except RuntimeError as e:
                print("rows", off, "error", str(e)[:60], "waited", wait, flush=True)
        if page is None:
            print("giving up on rows at offset", off, flush=True)
            break
        for r in page["rows"]:
            row = r["row"]
            l = row["label"]
            if len(picked[l]) < N and took[l] < per_page[l]:
                picked[l].append(row)
                took[l] += 1
    print("picked", len(picked[0]), len(picked[1]), round(time.time() - t0), "s", flush=True)
    clips = []
    for label in (0, 1):
        for row in picked[label]:
            p = AUD / row["path"]
            if not p.exists():
                p.write_bytes(b.get(row["audio"][0]["src"], binary=True))
            n = json.loads(row.get("notes") or "{}")
            clips.append((row["path"], label, p, n.get("speaker_id"), n.get("codec"), n.get("transmission")))
    print("have", len(clips), round(time.time() - t0), "s", flush=True)
    F, names = [], None
    for c in clips:
        y, sr = librosa.load(c[2], sr=16000)
        f = b.feats(y, sr)
        names = names or list(f)
        F.append([f[k] for k in names])
    X = np.array(F)
    lab = np.array([c[1] for c in clips])
    spk = np.array([c[3] for c in clips])
    bona, spoof = np.where(lab == 0)[0], np.where(lab == 1)[0]
    speakers = sorted({s for s in spk[bona] if s})
    runs = []
    for seed in range(5):
        r = np.random.default_rng(100 + seed)
        sp = list(speakers)
        r.shuffle(sp)
        a = set(sp[: len(sp) // 2])
        fit = np.array([i for i in bona if spk[i] in a])
        held = np.array([i for i in bona if spk[i] not in a])
        runs.append({"seed": 100 + seed, "fit_bonafide": int(len(fit)), "test_bonafide": int(len(held)),
                     "eer_speaker_split": round(score(X, lab, fit, np.concatenate([held, spoof])), 4)})
        print(json.dumps(runs[-1]), flush=True)
    e = [x["eer_speaker_split"] for x in runs]
    res = {"dataset": DS, "clips": len(clips), "bonafide": int(len(bona)), "spoof": int(len(spoof)),
           "bonafide_speakers": len(speakers),
           "codec_bonafide": dict(Counter(c[4] for c in clips if c[1] == 0)),
           "codec_spoof": dict(Counter(c[4] for c in clips if c[1] == 1)),
           "speaker_split_eer_mean": round(float(np.mean(e)), 4), "speaker_split_eer_range": [min(e), max(e)],
           "p0559_2019_speaker_split_eer_mean": 0.1849, "runs": runs, "seconds": round(time.time() - t0)}
    (HERE / "results.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v for k, v in res.items() if k != "runs"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
