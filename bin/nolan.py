#!/usr/bin/env python3
"""One Nolan film a night: the research step for the fan site (Luke, 7 Oct 2026).

    python3 /Users/triton/PROTEUS/bin/nolan.py next       # pick the next queued film, write the child prompt, print GO or STOP
    python3 /Users/triton/PROTEUS/bin/nolan.py ingest     # check the child's digest, fetch stills, build, commit, publish
    python3 /Users/triton/PROTEUS/bin/nolan.py build      # rebuild the site from what is on disk
    python3 /Users/triton/PROTEUS/bin/nolan.py status

Register: sites/nolan/films.json. The child (one Sonnet spawn, counted against the four) writes exactly one
file, state/agents/nolan/YYYY-MM-DD-<slug>.json, from pages it fetched that night. The parent does
everything else through this script: validation (sites/nolan/check.py), stills fetched and resized here,
the page built by sites/nolan/build.cjs, a commit by named path, and bin/publish-nolan.sh. A failed check
requeues the film once with the reasons in the next prompt, then parks it. Under HALT: written, not
committed, not published. Standard library only.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime

ROOT = "/Users/triton/PROTEUS/"
SITE = ROOT + "sites/nolan/"
REG = SITE + "films.json"
THEMES = SITE + "themes.json"
OUT = ROOT + "state/agents/nolan/"
MARKER = ROOT + "state/unattended-session.json"
DECISIONS = ROOT + "state/unattended-decisions-%s.jsonl"
FFMPEG = "/usr/local/bin/ffmpeg"
NODE = "/usr/local/bin/node"
MAX_TRIES = 2
SPAWN_CAP = 4
UA = "ProteusFanSite/0.1 (https://github.com/triton-xxix/proteus-nolan; stills for a fan page, credited)"

TEMPLATE = {
    "slug": "", "title": "", "year": 0,
    "one_line": "own words, under 30 words",
    "facts": {
        "release": {"value": "YYYY-MM-DD (country)", "source": "url"},
        "runtime_min": {"value": 0, "source": "url"},
        "writers": {"value": ["..."], "source": "url"},
        "dp": {"value": "", "source": "url"}, "editor": {"value": "", "source": "url"}, "composer": {"value": "", "source": "url"},
        "budget_usd": {"value": 0, "note": "range or dispute if any", "source": "url"},
        "gross_usd": {"value": 0, "as_of": "YYYY-MM-DD", "source": "url"},
        "cast_top5": {"value": [{"name": "", "role": ""}], "source": "url"},
    },
    "time_structure": {
        "kind": "one of: linear, linear-with-flashbacks, two-threads-converging, interleaved-strands, nested-levels, parallel-timescales, dilation, inverted-crossing",
        "summary": "two or three sentences, own words",
        "sketch": {"nesting": "parallel|nested|interleaved|single",
                   "threads": [{"id": "a", "label": "", "direction": "forward|backward|static", "level": 0, "rate": 1, "span": [0, 1], "duration_label": "", "style": "colour|mono"}],
                   "joins": [{"from": "a", "to": "b", "kind": "converge|nest|cross", "at": 1.0, "label": ""}]},
        "source": "url",
    },
    "themes": [{"id": "theme-id-from-themes.json", "name": "", "scene": "20 to 80 words, own words, one scene", "source": "url or null", "new": False}],
    "inspirations": [{"claim": "own words", "who": "Nolan | Jonathan Nolan | Emma Thomas | ...", "quote": "optional, under 15 words", "source": "url"}],
    "collaborators": [{"name": "", "role": "", "also": ["other-film-slugs"]}],
    "reception": {"at_release": {"metacritic": {"value": 0, "source": ""}, "rt": {"value": 0, "count": 0, "source": ""}, "summary": "own words"},
                  "now": {"letterboxd": {"value": 0.0, "as_of": "", "source": ""}, "summary": "own words"}},
    "missed": [{"point": "own words", "source": "url"}, {"point": "", "source": ""}, {"point": "", "source": ""}],
    "images": [{"url": "https://image.tmdb.org/t/p/original/<path>.jpg", "caption": "what it shows", "source": "the page it was listed on"}],
    "sources": [{"url": "", "title": "", "fetched": True, "used_for": ["facts.runtime_min"]}],
    "_child": {"fetches": 0, "searches": 0, "fetch_failures": [], "refusals": [], "notes": "", "unverified": []},
}

BRIEF = """You are a research child for Proteus, running unattended on Sonnet. Tonight's film: {title} ({year}), slug {slug},
film {order} of 13 on a Christopher Nolan fan site Proteus is building (an unofficial site; every claim sourced).
{special}
Your job: fill the template below from pages you fetch tonight. Nothing from memory counts as a fact: a claim
whose source you did not fetch is written with "unverified": true and "source": null. Budget: at most {fetches}
WebFetch calls and {searches} WebSearch calls. Use one fetch per section with a targeted question, for example
fetch https://en.wikipedia.org/wiki/{wiki} asking only for the infobox (release, runtime, writers, DP, editor,
composer, budget, gross, top cast and the citation URLs), then again for the Production and Themes sections,
then Reception. Money from Box Office Mojo or The Numbers; release reception from Metacritic and Rotten
Tomatoes; the current rating from Letterboxd; inspirations from two to four interviews on reputable outlets
found by WebSearch ("{title} Nolan interview inspiration"). Tom Shone's book The Nolan Variations (2020) may be
cited as a book for inspirations, marked unverified unless you fetched an excerpt. If a site refuses the
fetch, record it in _child.fetch_failures and fall back to Wikipedia's citation of the same number, with the
source "via Wikipedia" and unverified true.

Stills: find the film on The Movie Database (WebSearch "themoviedb {title} {year}" or fetch
https://www.themoviedb.org/search?query={query}), then fetch its /images/backdrops page and list three to six
backdrop paths as https://image.tmdb.org/t/p/original/<path>.jpg in images[], each with a caption (say what the
page's context tells you it shows; "a still from {title}" is acceptable) and the backdrops page as source.
Do not download anything; the parent fetches and credits them.

Theme ids must come from /Users/triton/PROTEUS/sites/nolan/themes.json (Read it); add a new one only with
"new": true. Other films' finished data, for the shape, is in /Users/triton/PROTEUS/sites/nolan/films/.
{retry}
Write exactly one file with the Write tool, valid JSON, this shape and nothing else:
  {out}
{template}

Field rules:
- facts: every value has a source URL you fetched; budget_usd carries a note when sources disagree.
- time_structure: summary in your own words (two or three sentences), then the sketch: one thread per
  storyline with direction (forward, backward, static), level (0 outermost; nested levels count up), rate
  (how fast that thread's clock runs relative to level 0: 1 for ordinary, 20 for a dream level, 60480 for
  an hour that is seven years), span as fractions of screen time [start, end], duration_label (e.g. "one
  week"), style (colour or mono); joins where threads converge, nest or cross, with "at" as a screen-time
  fraction. Draw it so a reader who has not seen the film understands the device. Register prior:
  "{kind}"; correct it if the film says otherwise.
- themes: three to six, each with ONE example scene described in your own words, 20 to 80 words, no dialogue.
- inspirations: what Nolan and his collaborators have said, cited; a quote only if under 15 words.
- collaborators: recurring crew and cast on this film, with the other Nolan films they worked on (slugs:
  following, memento, insomnia, batman-begins, the-prestige, the-dark-knight, inception, the-dark-knight-rises,
  interstellar, dunkirk, tenet, oppenheimer, the-odyssey).
- reception: numbers with sources and an as_of date; two own-words summaries, at release and now.
- missed: exactly three things most viewers miss, each sourced (a commentary, an interview, a scholarly
  piece, a close reading), no fan theories presented as fact.
- sources: every URL used, once, with fetched true or false and which fields it backs.
House rules: own words; no reproduced dialogue beyond one quote under 15 words per field; no stills or image
links outside images[]; UK spelling; no em dashes; say "unverified" rather than guess; never name Luke.

Rules enforced by a hook that will refuse you: you cannot spawn agents, run git, or run scripts; Bash only
for ls, cat, head, grep on files under /Users/triton/PROTEUS, one command per call, no ; && $() or
redirection; you write only under /Users/triton/PROTEUS/state/agents/ or /Users/triton/PROTEUS/sandbox/.
A refusal is a result to report, not a problem to route around. Final message, three lines: fields filled
and how many unverified; fetches used and failures; any refusals. Do not paste the JSON into the message.
"""

WIKI = {"following": "Following_(film)", "memento": "Memento_(film)", "insomnia": "Insomnia_(2002_film)",
        "batman-begins": "Batman_Begins", "the-prestige": "The_Prestige_(film)", "the-dark-knight": "The_Dark_Knight",
        "inception": "Inception", "the-dark-knight-rises": "The_Dark_Knight_Rises", "interstellar": "Interstellar_(film)",
        "dunkirk": "Dunkirk_(2017_film)", "tenet": "Tenet_(film)", "oppenheimer": "Oppenheimer_(film)", "the-odyssey": "The_Odyssey_(2026_film)"}


def today():
    return datetime.now().strftime("%Y-%m-%d")


def load():
    return json.load(open(REG))


def save(reg):
    json.dump(reg, open(REG, "w"), indent=2, ensure_ascii=False)
    open(REG, "a").write("\n")


def session_short():
    try:
        sid = json.load(open(MARKER)).get("session_id")
    except Exception:
        return None
    return None if not sid or sid == "closed" else str(sid)[:8]


def spawns_today():
    s = session_short()
    if not s:
        return 0
    n = 0
    try:
        for line in open(DECISIONS % today()):
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("session") == s and rec.get("tool") == "Agent" and rec.get("outcome") == "allow":
                n += 1
    except FileNotFoundError:
        pass
    return n


def digest_path(f, day):
    return OUT + "%s-%s.json" % (day, f["slug"])


def cmd_next(a):
    reg = load()
    queued = sorted([f for f in reg["films"] if f["status"] == "queued"], key=lambda f: f["order"])
    if not queued:
        print("STOP: all films researched or parked"); return
    n = spawns_today()
    if n >= SPAWN_CAP:
        print("STOP: spawn cap (%d of %d used)" % (n, SPAWN_CAP)); return
    f = queued[0]
    day = today()
    os.makedirs(OUT, exist_ok=True)
    special = ""
    if f["slug"] == "the-odyssey":
        special = ("This film was released on 17 July 2026, after your training data. You know nothing reliable about it. "
                   "Every field, including the time structure kind, cast and reception, comes from fetched pages; prefer the "
                   "Wikipedia article's citations and dated reviews.")
    retry = ""
    if f.get("last_check") and f.get("last_digest"):
        retry = ("Last night's attempt at %s failed the check on: %s. Read it, keep what passed, fix those.\n"
                 % (f["last_digest"], "; ".join(f["last_check"][:6])))
    template = json.dumps(dict(TEMPLATE, slug=f["slug"], title=f["title"], year=f["year"]), indent=2, ensure_ascii=False)
    prompt = BRIEF.format(title=f["title"], year=f["year"], slug=f["slug"], order=f["order"], special=special,
                          fetches=12, searches=6, wiki=WIKI.get(f["slug"], f["title"].replace(" ", "_")),
                          query=f["title"].replace(" ", "+"), retry=retry, out=digest_path(f, day), template=template,
                          kind=f.get("time_structure_kind", "unverified"))
    pfile = OUT + "%s-%s.prompt.md" % (day, f["slug"])
    open(pfile, "w").write(prompt)
    f["status"] = "assigned"; f["assigned_on"] = day; f["tries"] = f.get("tries", 0) + 1
    save(reg)
    print("GO %s model=sonnet prompt=%s expect=%s" % (f["slug"], pfile, digest_path(f, day)))


def run_check(path):
    r = subprocess.run([sys.executable, SITE + "check.py", "film", path], capture_output=True, text=True)
    fails = [l[6:] for l in r.stdout.splitlines() if l.startswith("FAIL: ") and not re.match(r"FAIL: \d+ ", l)]
    warns = [l[6:] for l in r.stdout.splitlines() if l.startswith("WARN: ")]
    return r.returncode == 0, fails, warns


def fetch_stills(d):
    """Download up to six candidate stills, resize with ffmpeg, set `local` on each. Failures are logged, never fatal."""
    img_dir = SITE + d["slug"] + "/img/"
    raw_dir = img_dir + "raw/"
    os.makedirs(raw_dir, exist_ok=True)
    kept, failed = [], []
    for i, im in enumerate((d.get("images") or [])[:6]):
        url = im.get("url", "")
        if not url.startswith("http"):
            failed.append(url or "(no url)"); continue
        name = "still-%02d" % (i + 1)
        raw = raw_dir + name + ".bin"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read(25 * 1024 * 1024)
            if not (data[:2] == b"\xff\xd8" or data[:8] == b"\x89PNG\r\n\x1a\n" or data[:4] == b"RIFF"):
                failed.append(url + " (not an image)"); continue
            open(raw, "wb").write(data)
            for width, suffix, q in ((1600, "", "3"), (800, "-800", "4")):
                r = subprocess.run([FFMPEG, "-loglevel", "error", "-y", "-i", raw, "-vf", "scale='min(%d,iw)':-2" % width, "-q:v", q,
                                    img_dir + name + suffix + ".jpg"], capture_output=True, text=True, timeout=120)
                if r.returncode != 0:
                    raise RuntimeError(r.stderr.strip()[:120])
            im["local"] = name
            kept.append(im)
        except Exception as e:
            failed.append("%s (%s)" % (url[:80], type(e).__name__))
    d["images"] = kept
    return kept, failed


def merge_themes(d):
    th = json.load(open(THEMES))
    ids = {t["id"] for t in th["themes"]}
    added = []
    for t in d.get("themes", []):
        if t.get("id") and t["id"] not in ids:
            th["themes"].append({"id": t["id"], "name": t.get("name") or t["id"], "line": "proposed by the %s research; review" % d["slug"], "new": True})
            ids.add(t["id"]); added.append(t["id"])
    if added:
        json.dump(th, open(THEMES, "w"), indent=2, ensure_ascii=False); open(THEMES, "a").write("\n")
    return added


def build():
    r = subprocess.run([NODE, SITE + "build.cjs"], capture_output=True, text=True, timeout=300)
    return r.returncode == 0, (r.stdout + r.stderr).strip()[-300:]


def note_draft(line):
    wk = datetime.now().strftime("%G-W%V")
    draft = ROOT + "field-notes/drafts/%s.md" % wk
    if not os.path.exists(draft):
        return None
    text = open(draft).read()
    if "<!-- nolan -->" in text:
        text = re.sub(r"^.*<!-- nolan -->.*$", line, text, flags=re.M)
    else:
        if "## Built" not in text:
            text = text.rstrip("\n") + "\n\n## Built\n\n"
        text = text.rstrip("\n") + "\n" + line + "\n"
    open(draft, "w").write(text)
    return draft


def note_seen(f):
    seen = ROOT + "field-notes/SEEN.md"
    if not os.path.exists(seen):
        return None
    text = open(seen).read()
    line = "- %s: Nolan site, %s (%s) researched and built (`sites/nolan/films/%s.json`).\n" % (today(), f["title"], f["year"], f["slug"])
    if "## Rule" in text:
        text = text.replace("## Rule", line + "\n## Rule", 1)
    else:
        text = text.rstrip("\n") + "\n" + line
    open(seen, "w").write(text)
    return seen


def git(args, check=False):
    return subprocess.run(["git", "-C", ROOT] + args, capture_output=True, text=True, check=check)


def cmd_ingest(a):
    reg = load()
    day = today()
    assigned = [f for f in reg["films"] if f["status"] == "assigned"]
    if not assigned:
        print("nothing assigned"); return
    f = assigned[0]
    p = digest_path(f, f.get("assigned_on") or day)
    lines = []
    if not os.path.exists(p):
        ok, fails, warns = False, ["digest file missing"], []
    else:
        ok, fails, warns = run_check(p)
    if not ok:
        f["last_check"] = fails[:8]; f["last_digest"] = p.replace(ROOT, "")
        f["status"] = "queued" if f.get("tries", 0) < MAX_TRIES else "parked"
        save(reg)
        line = "- Nolan 5f: %s (%s, %s): check FAIL (%d: %s); digest kept %s; %s, try %d of %d; nothing built." % (
            f["slug"], f["title"], f["year"], len(fails), "; ".join(fails[:3]), f["last_digest"] if os.path.exists(p) else "none",
            "requeued" if f["status"] == "queued" else "parked", f.get("tries", 0), MAX_TRIES)
        open(ROOT + "state/runs/%s.md" % day, "a").write(line + "\n")
        print(line)
        if os.path.exists(ROOT + "HALT"):
            print("HALT set: written, not committed"); return
        git(["add", "--", REG, p] if os.path.exists(p) else ["add", "--", REG])
        git(["commit", "-q", "-m", "nolan: %s check failed, %s" % (f["slug"], f["status"])])
        git(["push", "-q", "origin", "main"])
        return
    d = json.load(open(p))
    child = d.pop("_child", {})
    d["researched_on"] = day
    d["digest"] = p.replace(ROOT, "")
    kept, failed = fetch_stills(d)
    added = merge_themes(d)
    os.makedirs(SITE + "films", exist_ok=True)
    out = SITE + "films/%s.json" % f["slug"]
    json.dump(d, open(out, "w"), indent=2, ensure_ascii=False); open(out, "a").write("\n")
    if d.get("time_structure", {}).get("kind") in ("linear", "linear-with-flashbacks", "two-threads-converging", "interleaved-strands",
                                                      "nested-levels", "parallel-timescales", "dilation", "inverted-crossing"):
        f["time_structure_kind"] = d["time_structure"]["kind"]
    f["status"] = "researched"; f["researched_on"] = day; f["research_digest"] = d["digest"]; f["page"] = "films/%s/" % f["slug"]
    f["last_check"] = warns[:8]
    save(reg)
    built, msg = build()
    f["status"] = "built" if built else "researched"
    save(reg)
    unverified = len(child.get("unverified") or [])
    live = sum(1 for x in reg["films"] if x["status"] in ("built", "live")) + 1
    line = ("- Nolan 5f: %s (%s, %s): child %d fetches (%d failed), %d searches; check PASS (%d warn, %d unverified); "
            "%d stills kept%s%s; films/%s.json written; %s. Live %d of %d." % (
                f["slug"], f["title"], f["year"], child.get("fetches", 0), len(child.get("fetch_failures") or []), child.get("searches", 0),
                len(warns), unverified, len(kept), (", %d failed" % len(failed)) if failed else "",
                (", new themes %s" % ", ".join(added)) if added else "", f["slug"],
                "built" if built else "BUILD FAILED: " + msg, live, len(reg["films"])))
    open(ROOT + "state/runs/%s.md" % day, "a").write(line + "\n")
    draft = note_draft("- Nolan site: %d of %d films live, latest %s (%s). %s <!-- nolan -->" % (live, len(reg["films"]), f["title"], f["year"], reg["site_url"]))
    seen = note_seen(f)
    print(line)
    if os.path.exists(ROOT + "HALT"):
        print("HALT set: written, not committed, not published"); return
    paths = [REG, THEMES, out, SITE + "site.json", SITE + f["slug"] + "/img", OUT, ROOT + "state/runs/%s.md" % day, ROOT + "sites/builds/nolan"]
    if draft: paths.append(draft)
    if seen: paths.append(seen)
    git(["add", "--"] + [x for x in paths if os.path.exists(x)])
    r = git(["commit", "-q", "-m", "nolan: %s researched and built (%d of %d live)" % (f["slug"], live, len(reg["films"]))])
    if r.returncode == 0:
        git(["push", "-q", "origin", "main"])
    if built:
        pub = subprocess.run(["/bin/bash", ROOT + "bin/publish-nolan.sh", "Nolan site: %s (%s)" % (f["title"], f["year"])], capture_output=True, text=True)
        print(pub.stdout.strip()[-200:])
        if "pushed" in pub.stdout:
            f["status"] = "live"; save(reg)
            git(["add", "--", REG]); git(["commit", "-q", "-m", "nolan: %s live" % f["slug"]]); git(["push", "-q", "origin", "main"])


def cmd_build(a):
    ok, msg = build()
    print(("built" if ok else "BUILD FAILED") + ": " + msg)


def cmd_status(a):
    for f in sorted(load()["films"], key=lambda x: x["order"]):
        print("%2d %-22s %-5d %-10s tries %d %s" % (f["order"], f["slug"], f["year"], f["status"], f.get("tries", 0), f.get("note", "")[:60]))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("next").set_defaults(fn=cmd_next)
    sub.add_parser("ingest").set_defaults(fn=cmd_ingest)
    sub.add_parser("build").set_defaults(fn=cmd_build)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
