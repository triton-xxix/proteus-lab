#!/usr/bin/env python3
"""P-0146: P-0143's plur-bench BM25 port, pointed at my own text. Corpus: every run log in state/runs and
every note in the Proteus memory folder, chunked 300 words / 50 overlap like plur-bench, each unit tagged
with its source file. Twenty questions written by me (14 Oct 2026, before the run) with the file that
answers each. Hit@k = any of the top-k units comes from an answer file. No model, no network."""
import glob, json, os, sys, time

sys.path.insert(0, "/Users/triton/PROTEUS/experiments/2026-10-13-P-0143")
from bm25_r5 import chunk_text, search  # noqa: E402

RUNS = "/Users/triton/PROTEUS/state/runs"
MEM = "/Users/triton/.claude/projects/-Users-triton-PROTEUS/memory"
OUT = "/Users/triton/PROTEUS/experiments/2026-10-14-P-0146/results.json"

QUESTIONS = [
    ("Which Python can run numpy scripts on this Intel Mac without the hook denying it?", ["project_in_folder_python312.md"]),
    ("Why does the op command hang, and what do we read secrets with instead?", ["project_op_hangs_use_sdk.md"]),
    ("What car does Luke want to buy, by when, and from how much?", ["project_supercar_goal.md"]),
    ("What went wrong when probes.bak and PROBES.bak turned out to be the same file?", ["project_case_insensitive_fs.md"]),
    ("How does the nightly harvester choose candidates and which model judges them?", ["project_harvester.md"]),
    ("What did Luke say about stopping work when the probe queue runs empty?", ["feedback_empty_queue_is_not_done.md"]),
    ("Why does every pre-registration need a due date and a backstop?", ["feedback_preregistration_needs_a_due_date.md"]),
    ("At what times do the Inspector, Trials, Workshop and Smith slots run?", ["project_daytime_loop.md"]),
    ("How should I make football predictions before I have seen the odds?", ["feedback_predict_blind_then_anchor.md"]),
    ("Which trades and firms did Luke name as lead targets for Triton?", ["project_triton_lead_targets.md"]),
    ("How is token usage worked out from transcripts, and which duplicate record do we keep?", ["project_usage_from_transcripts.md"]),
    ("What rebuilds the vault front page HOME.md and when does it run?", ["project_home_page.md"]),
    ("What is still waiting on Luke for the Lichess bot?", ["project_pending_from_luke.md"]),
    ("Do child agents spawned with the Agent tool inherit the unattended hook?", ["project_subagent_hook_inheritance.md"]),
    ("Which media API keys did Luke allow outside the folder, ElevenLabs and which other?", ["project_media_keys_luke_named.md"]),
    ("When were the 85 pump.fun pools captured and how many were above 5k at capture?", ["2026-10-13.md", "2026-10-14.md"]),
    ("How did the morning chess games against caissa-x go, and what is the rating now?", ["2026-10-14.md"]),
    ("On which day did the inspector add findings F-0015 to F-0021 from the nightly log?", ["2026-10-14.md"]),
    ("When was the sub-agent hook inheritance test run and what did it show?", ["2026-09-24.md"]),
    ("Which night did the probe loop stop because the P-0140 recheck was due twelve hours later?", ["2026-10-13.md"]),
]

units, src = [], []
files = sorted(glob.glob(RUNS + "/*.md")) + sorted(glob.glob(MEM + "/*.md"))
for f in files:
    name = os.path.basename(f)
    for u in chunk_text(open(f, encoding="utf-8", errors="replace").read()):
        units.append(u + " src:" + name)
        src.append(name)
print("corpus: %d files, %d units, %d words" % (len(files), len(units), sum(len(u.split()) for u in units)), flush=True)

t0 = time.time()
rows, h1 = [], 0
h5 = h10 = 0
for q, ans in QUESTIONS:
    top = search(units, q, 10)
    ranked = [src[i] for i in top]
    hit1 = bool(ranked) and ranked[0] in ans
    hit5 = any(s in ans for s in ranked[:5])
    hit10 = any(s in ans for s in ranked[:10])
    h1 += hit1; h5 += hit5; h10 += hit10
    rank = next((k + 1 for k, s in enumerate(ranked) if s in ans), None)
    rows.append({"q": q, "answer": ans, "top5": ranked[:5], "rank": rank, "hit_1": hit1, "hit_5": hit5, "hit_10": hit10,
                 "kind": "memory" if ans[0].startswith(("project_", "feedback_", "user_")) else "runs"})
    print("%s r%-4s %s  -> %s" % ("HIT " if hit5 else "MISS", rank, q[:70], ranked[:3]), flush=True)

n = len(QUESTIONS)
by_kind = {}
for r in rows:
    k = by_kind.setdefault(r["kind"], [0, 0]); k[0] += 1; k[1] += r["hit_5"]
res = {"probe": "P-0146", "files": len(files), "units": len(units), "n": n,
       "r_at_1": round(100 * h1 / n, 1), "r_at_5": round(100 * h5 / n, 1), "r_at_10": round(100 * h10 / n, 1),
       "hits_5": h5, "published_longmemeval_r5": 92.2, "p0143_r5": 92.2, "seconds": round(time.time() - t0, 1),
       "by_kind_r5": {k: [v[0], round(100 * v[1] / v[0], 1)] for k, v in by_kind.items()}, "rows": rows}
json.dump(res, open(OUT, "w"), indent=1)
print("n %d  R@1 %.1f  R@5 %.1f (%d of %d)  R@10 %.1f  %.1fs  by kind %s" % (n, res["r_at_1"], res["r_at_5"], h5, n, res["r_at_10"], res["seconds"], res["by_kind_r5"]))
