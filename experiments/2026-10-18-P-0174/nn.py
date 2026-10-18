"""P-0174: same-video nearest neighbour in GenAI for Beginners lesson 08's shipped embedding index.

Downloads embedding_index_3m.json once into sandbox/p0174/, then for every chunk finds the nearest other
chunk by cosine and asks whether it is from the same video. Chance = the expected same-video share if the
neighbour were drawn at random from the other chunks. Also the same test with time-adjacent chunks
excluded, because overlapping 3-minute windows would make the headline easy.
"""
import json
import os
import sys
import time
import urllib.request

import numpy as np

URL = ("https://raw.githubusercontent.com/microsoft/generative-ai-for-beginners/main/"
       "08-building-search-applications/scripts/embedding_index_3m.json")
CACHE = "/Users/triton/PROTEUS/sandbox/p0174/embedding_index_3m.json"
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    if not os.path.exists(CACHE):
        t = time.time()
        urllib.request.urlretrieve(URL, CACHE)
        print("downloaded", os.path.getsize(CACHE), "bytes in", round(time.time() - t, 1), "s")
    rows = json.load(open(CACHE))
    keys = sorted(rows[0].keys())
    print("rows", len(rows), "keys", keys)
    sample = {k: (str(v)[:120] if k != "ada_v2" else "len %d" % len(v)) for k, v in rows[0].items()}
    print("first row", sample)

    vkey = next(k for k in keys if isinstance(rows[0][k], list) and len(rows[0][k]) > 100)
    gkey = "videoId" if "videoId" in keys else next(k for k in keys if "video" in k.lower() and "id" in k.lower())
    skey = next((k for k in ("seconds", "start_seconds", "start") if k in keys), None)
    X = np.array([r[vkey] for r in rows], dtype=np.float32)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    vid = np.array([r[gkey] for r in rows])
    S = X @ X.T
    np.fill_diagonal(S, -2)
    nn = S.argmax(axis=1)
    same = (vid[nn] == vid)

    _, counts = np.unique(vid, return_counts=True)
    n = len(rows)
    chance = float(((counts * (counts - 1)).sum()) / (n * (n - 1)))

    res = {"rows": n, "dims": int(X.shape[1]), "videos": int(len(counts)), "vector_key": vkey, "video_key": gkey,
           "chunks_per_video_median": float(np.median(counts)), "same_video_nn": round(float(same.mean()), 4),
           "chance": round(chance, 4), "nn_cos_median": round(float(S[np.arange(n), nn].mean()), 4)}

    if skey:
        start = np.array([float(r[skey]) for r in rows])
        # exclude any chunk from the same video within 6 minutes (two windows) of this one
        near = (vid[:, None] == vid[None, :]) & (np.abs(start[:, None] - start[None, :]) < 360)
        S2 = S.copy()
        S2[near] = -2
        nn2 = S2.argmax(axis=1)
        res["same_video_nn_excl_adjacent"] = round(float((vid[nn2] == vid).mean()), 4)
        res["start_key"] = skey

    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
