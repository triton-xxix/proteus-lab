"""P-0268: score a Skool About page against the Magnetic Memberships 5 June 2026 audit checklist.

Stdlib only. Input: saved HTML of skool.com/<slug>/about (the page embeds its data as Next.js JSON),
or a plain-text file holding the short description on line 1 and the long copy after a blank line.
Checklist, as the transcript states it (S-58 digest, `field-notes/skool/transcripts/
magnetic-post-2026-06-05-what-the-top-45-skool-earners-are-doing.txt`):
  1 short description 150 characters or fewer
  2 a primary keyword in its first five words (here: a word from the community's own name or tags)
  3 long copy 1,000 characters or fewer
  4 a hook in the first sentence carrying a specific number
  5 five to seven outcome bullets
  6 a proof line (named results, member counts, authority markers)
  7 a guarantee or trial
  8 a price anchor (per day, worth X, or the price stated)
  9 exactly one call to action
 10 no outbound links in the copy
 11 reading level grade 5 to 6 (Flesch-Kincaid, syllables by heuristic)
Usage: python3 about_score.py FILE [FILE ...]
"""
import html
import json
import os
import re
import sys

BULLET = re.compile(r"^\s*(?:[-*•▪◦✅✔✓☑→➜➡️🔥💰📈🎯🚀]|\d+[.)])\s*\S", re.M)
CTA = re.compile(r"\b(join (?:now|us|here|today|the)|apply (?:now|here|today)|click (?:the link|below|here)|see you inside|get started|enrol+ now|sign up)\b", re.I)
PROOF = re.compile(r"\b(\d[\d,.]*\s*(?:\+\s*)?(?:members|students|clients|customers|coaches|businesses|people)|featured in|ranked|#\s?1|top 1%|\$\s?\d[\d,.]*\s*[kKmM]?\b(?! ?/mo| a month| per month| ?/month)|years? of|case stud|results?)\b", re.I)
GUARANTEE = re.compile(r"\b(guarantee|money back|money-back|refund|risk[- ]free|free trial|day trial|cancel any ?time)\b", re.I)
ANCHOR = re.compile(r"(\$\s?\d[\d,.]*\s*(?:/|per|a)\s*(?:mo|month|day|week|year)|per day|a day|worth \$?\d|valued at|\$\d[\d,]*\s*value|cents a day)", re.I)
LINK = re.compile(r"https?://|www\.", re.I)
STOP = set("the a an and or for to of in on with your you we our my how what skool community group free".split())


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


def fk_grade(text):
    # a bullet or a line break ends a sentence as a reader sees it, even without a full stop
    sents = max(1, len(re.findall(r"[.!?]+(?:\s|$)|\n", text)) or 1)
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not words:
        return None
    syl = sum(syllables(w) for w in words)
    return 0.39 * len(words) / sents + 11.8 * syl / len(words) - 15.59


def find_strings(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                out.append((k, v))
            else:
                find_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_strings(v, out)


def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', raw, re.S)
    if not m:
        parts = raw.split("\n\n", 1)
        return {"name": os.path.basename(path), "tags": [], "short": parts[0].strip(), "long": parts[1].strip() if len(parts) > 1 else ""}
    data = json.loads(m.group(1))
    pairs = []
    find_strings(data, pairs)
    name = next((v for k, v in pairs if k == "displayName"), None) or next((v for k, v in pairs if k == "name" and len(v) < 80), os.path.basename(path))
    short = next((v for k, v in pairs if k == "description" and 10 < len(v) < 400), "")
    # the long copy is the longest string that is not markup-heavy and not the description
    cands = [v for k, v in pairs if len(v) > 200 and "<" not in v[:50] and v != short and not v.startswith("http") and "{" not in v[:20]]
    # Skool stores rich text as JSON-in-a-string on some fields; unwrap plain paragraphs if so
    long = max(cands, key=len) if cands else ""
    if long.lstrip().startswith("{") or long.lstrip().startswith("["):
        try:
            inner = json.loads(long)
            texts = []
            find_strings(inner, texts)
            long = "\n".join(v for k, v in texts if k in ("text",) and v.strip())
        except Exception:  # noqa
            pass
    long = html.unescape(long)
    tags = [v for k, v in pairs if k in ("tag", "label", "keyword") and len(v) < 40]
    return {"name": name, "tags": tags, "short": html.unescape(short), "long": long}


def score(page):
    short, long = page["short"], page["long"]
    keyset = {w.lower().strip(".,") for w in re.findall(r"[A-Za-z][A-Za-z-]+", page["name"] + " " + " ".join(page["tags"]))} - STOP
    first5 = [w.lower().strip(".,&") for w in short.split()[:5]]
    first_sent = re.split(r"(?<=[.!?])\s|\n", long.strip(), maxsplit=1)[0] if long else ""
    bullets = len(BULLET.findall(long))
    ctas = len(CTA.findall(long + " " + short))
    grade = fk_grade(long) if long else None
    checks = [
        ("1 short description <= 150 chars", len(short) <= 150, "%d chars" % len(short)),
        ("2 keyword in first five words", any(w in keyset for w in first5), "first five: %s; keys: %s" % (" ".join(first5), ", ".join(sorted(keyset))[:60])),
        ("3 long copy <= 1,000 chars", 0 < len(long) <= 1000, "%d chars" % len(long)),
        ("4 number in the first sentence", bool(re.search(r"\d", first_sent)), first_sent[:80]),
        ("5 five to seven bullets", 5 <= bullets <= 7, "%d bullets" % bullets),
        ("6 proof line", bool(PROOF.search(long)), (PROOF.search(long).group(0) if PROOF.search(long) else "none")),
        ("7 guarantee or trial", bool(GUARANTEE.search(long + " " + short)), (GUARANTEE.search(long + " " + short).group(0) if GUARANTEE.search(long + " " + short) else "none")),
        ("8 price anchor", bool(ANCHOR.search(long + " " + short)), (ANCHOR.search(long + " " + short).group(0) if ANCHOR.search(long + " " + short) else "none")),
        ("9 exactly one call to action", ctas == 1, "%d found" % ctas),
        ("10 no outbound links", not LINK.search(long), "link present" if LINK.search(long) else "clean"),
        ("11 reading grade 5 to 6", grade is not None and 5 <= grade <= 6.99, "grade %.1f" % grade if grade is not None else "no copy"),
    ]
    return checks


for path in sys.argv[1:]:
    page = load(path)
    checks = score(page)
    passed = sum(1 for _, ok, _ in checks if ok)
    print("\n== %s  (%s)  %d of 11" % (page["name"], os.path.basename(path), passed))
    print("   short: %s" % page["short"][:160])
    for name, ok, why in checks:
        print("   %s %-36s %s" % ("PASS" if ok else "FAIL", name, why))
