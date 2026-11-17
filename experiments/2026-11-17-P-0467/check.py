"""P-0467: the half of rust-anything's Python slugify claim I can run without a Rust toolchain.

1. Replay the repo's recorded cases (demo/fixtures/python-textkit-rs/cases.jsonl) against the
   original Python (tests/fixtures/python/src/textkit/words.py, read first, copied below verbatim
   for the five plain functions). Does the recording match the original on this Python?
2. Time the original slugify over the README's own 20,000 strings (their baseline: 98 ms).

No Rust was built or run: no cargo on this Mac, and a prebuilt binary from a day-old repo is not
something an unattended run executes.
"""
import json, platform, re, statistics, sys, time, unicodedata
from pathlib import Path
from typing import Optional

HERE = Path(__file__).resolve().parent
CASES = Path("/Users/triton/PROTEUS/sandbox/p0467-cases.jsonl")
_SEPARATORS = re.compile(r"[^\w]+")


def slugify(text: str, sep: str = "-", *, max_length: Optional[int] = None) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_only = "".join(c for c in normalized if not unicodedata.combining(c))
    words = [w for w in _SEPARATORS.split(ascii_only.lower()) if w]
    slug = sep.join(words)
    if max_length is not None:
        slug = slug[:max_length].rstrip(sep)
    return slug


def word_counts(text, min_length=1):
    counts = {}
    for word in text.split():
        word = word.strip(".,;:!?\"'()").lower()
        if len(word) >= min_length:
            counts[word] = counts.get(word, 0) + 1
    return counts


def chunk(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items), size)]


def page_count(total, per_page):
    return -(-total // per_page)


def mean(values):
    return sum(values) / len(values)


FNS = {"slugify": slugify, "word_counts": word_counts, "chunk": chunk, "page_count": page_count, "mean": mean}


def special(x):
    if isinstance(x, dict):
        return any(str(k).startswith("$") for k in x) or any(special(v) for v in x.values())
    if isinstance(x, list):
        return any(special(v) for v in x)
    return False


def decode(x):
    """The recording wraps big ints and floats: {"$int": "..."} and {"$float": "..."}."""
    if isinstance(x, dict):
        if set(x) == {"$int"}:
            return int(x["$int"])
        if set(x) == {"$float"}:
            return float(x["$float"])
        return {k: decode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [decode(v) for v in x]
    return x


def same(a, b):
    if isinstance(a, float) and isinstance(b, float) and a != a and b != b:
        return True
    return a == b and type(a) is type(b)


def main():
    rows = [decode(json.loads(line)) for line in CASES.read_text().splitlines() if line.strip()]
    by_fn, keys = {}, {}
    for r in rows:
        for k in r:
            keys[k] = keys.get(k, 0) + 1
        fn = r.get("fn")
        s = by_fn.setdefault(fn, {"cases": 0, "replayed": 0, "match": 0, "mismatch": 0, "skipped_encoding": 0,
                                  "skipped_unknown_fn": 0, "error_cases": 0, "error_raised": 0, "examples": []})
        s["cases"] += 1
        if fn not in FNS:
            s["skipped_unknown_fn"] += 1
            continue
        args, kwargs = r.get("args", []), r.get("kwargs", {})
        if special(args) or special(kwargs):
            s["skipped_encoding"] += 1
            continue
        try:
            got, raised = FNS[fn](*args, **kwargs), None
        except Exception as e:
            got, raised = None, type(e).__name__
        if "ok" in r:
            s["replayed"] += 1
            if raised is None and same(got, r["ok"]):
                s["match"] += 1
            else:
                s["mismatch"] += 1
                if len(s["examples"]) < 4:
                    s["examples"].append({"args": args, "kwargs": kwargs, "recorded": r["ok"], "got": got, "raised": raised})
        else:
            s["error_cases"] += 1
            if raised is not None:
                s["error_raised"] += 1
            elif len(s["examples"]) < 4:
                s["examples"].append({"args": args, "kwargs": kwargs, "recorded": {k: v for k, v in r.items() if k not in ("fn", "args", "kwargs")}, "got": got})
    texts = [f"Hello, Wörld {i} -- Ünïcode Title_{i % 7}!" for i in range(20000)]
    times = []
    for _ in range(15):
        t = time.perf_counter()
        [slugify(x) for x in texts]
        times.append((time.perf_counter() - t) * 1e3)
    out = {
        "python": sys.version.split()[0], "machine": platform.machine(), "cases": len(rows), "row_keys": keys,
        "by_fn": by_fn,
        "slugify_20000_ms": {"median": round(statistics.median(times), 1), "min": round(min(times), 1), "max": round(max(times), 1), "runs": len(times)},
        "readme_baseline_ms": 98, "readme_speedup": 17,
    }
    (HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for fn, s in by_fn.items():
        print(fn, {k: v for k, v in s.items() if k != "examples"})
        for ex in s["examples"]:
            print("   ", json.dumps(ex, ensure_ascii=False)[:300])
    print("row keys", keys)
    print("slugify x20000", out["slugify_20000_ms"], "python", out["python"], out["machine"])


if __name__ == "__main__":
    main()
