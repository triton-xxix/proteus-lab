#!/usr/bin/env python3
"""Data for the Skool Courses dashboard (claude.ai/artifact/XZM9j9HKgeBwWu19PJFAbi), built 14 Oct 2026.

    python3 /Users/triton/PROTEUS/bin/skool-dash.py      # writes state/skool-dash/*.json

Reads, never writes, outside this folder:
  - Luke's extractor log  OBSIDIAN/TRITON-CORE/Education/Courses/SKOOL-LOG.md (23 rooms, per course)
  - the frameworks index  OBSIDIAN/TRITON-CORE/Systems/frameworks/INDEX.md (what was built from them)
and from here field-notes/SKOOL-QUEUE.json (the nightly reading) plus my own pulls, listed below
because they are not in Luke's log. Re-run, then re-upload the five files to the dashboard.
"""
import json, os, re
from datetime import datetime, timezone

ROOT = "/Users/triton/PROTEUS/"
VAULT = "/Users/triton/OBSIDIAN/TRITON-CORE/"
OUT = ROOT + "state/skool-dash/"

# Theme per room, by slug. Rooms not named here fall back to "Other".
THEME = {
    "ai-automation-society": "AI and automation", "automatable-free": "AI and automation", "brendan": "AI and automation",
    "agent-j": "AI and automation", "ai-automation-agency": "AI agency and sales", "join-dlag": "AI and automation",
    "viral-ads": "Marketing", "aivideobootcamp": "AI video", "ai-for-brands-6110": "Fashion",
    "3-hour-youtube-leads-2772": "Marketing", "theadsclinic": "Marketing", "google-biz-profile-domination-6420": "Marketing",
    "stevekeen-free": "Economics", "bettrnation-3016": "Betting", "the-analytics-club-9973": "Data",
    "ofmconquest": "Agency (OnlyFans)", "rich-off-clothes-9474": "Fashion", "design-to-production-club-8824": "Fashion",
    "clothingmethod": "Fashion", "launch-program-7650": "Fashion", "clothing-brand-accelerator": "Fashion",
    "efd": "Fashion", "risewise-9746": "Fashion",
    "mattryder": "Sales", "lead-gen": "Cold email", "free-email-marketing-community": "Email marketing",
}

# Cost on file, by slug (the log's notes and my run logs). Blank means free.
COST = {
    "ai-for-brands-6110": "$15/mo trial, cancelled", "clothingmethod": "$12/mo, renewal cancelled",
    "mattryder": "$69/mo trial, cancelled",
}

# What the nightly reading groups were drawn from.
READ_ROOM = {**{s: "ai-automation-society" for s in ("S-01", "S-02", "S-03", "S-04", "S-05", "S-14", "S-15", "S-17")},
             **{s: "agent-j" for s in ("S-06", "S-16", "S-18", "S-19")},
             **{s: "automatable-free" for s in ("S-07", "S-09", "S-10", "S-20")},
             **{s: "brendan" for s in ("S-08", "S-11", "S-12", "S-13")},
             **{s: "mattryder" for s in ("S-21", "S-22", "S-23")},
             **{s: "lead-gen" for s in ("S-24", "S-25", "S-26", "S-27")},
             **{s: "free-email-marketing-community" for s in ("S-28", "S-29")}}

# My own pulls on 14 Oct, not in Luke's log: (room, slug, extracted, courses as (name, lessons, status)).
MINE = [
    ("Matt Ryder F The GuRUs", "mattryder", "2026-10-14", [
        ("1. Start your education here", 37, "done"), ("2. Sales Fundamentals", 29, "done"),
        ("3. Objection Handling", 37, "done"), ("4. Scripting", 26, "done"), ("5. Mastering Tonality", 9, "locked"),
        ("6. Follow ups, referrals, CRM farming", 9, "locked"), ("7. Outbound dialing", 11, "locked"),
        ("8. B2B and Complex B2C", 21, "locked"), ("9. Selling with stories", 14, "done"), ("10. The Dark Arts", 8, "locked"),
        ("11. Sales Management", 18, "done"), ("12. Business Mastery", 25, "done"), ("13. Downloadable resources", 4, "locked")]),
    ("Lead Gen Secrets (Lead Gen Jay)", "lead-gen", "2026-10-14", [
        ("The Insider Method - Free", 43, "done"), ("Work With Lead Gen Jay", 2, "done"),
        ("Copywriting - Jay's 1on1 Trainings", 9, "locked")]),
    ("Free Email Marketing Community", "free-email-marketing-community", "2026-10-14", [
        ("0.0 Agency Tips and how to get clients", 7, "done"), ("Full Email Marketing Master Class", 1, "done"),
        ("1. Klaviyo Account Set-Up Master Class", 9, "done"), ("2. Pop-up form masterclass", 13, "done"),
        ("Omnisend Masterclass", 8, "done"), ("Using Claude to run campaign reports", 1, "done"),
        ("One-on-one call", 1, "locked"), ("Editable email designs", 1, "locked"), ("Asana board for planning campaigns", 1, "locked"),
        ("My process for hiring designers", 1, "locked"), ("My process for hiring builders/technicians", 1, "locked"),
        ("Over 639 email designs", 1, "locked"), ("Steal my Klaviyo audit process", 1, "locked")]),
]

# Things built from the courses that the frameworks index does not hold.
EXTRA_USES = [
    ("Video Bootcamp skills (5)", "Skill", "in use", "aivideobootcamp", "The course's method as five Claude skills, from brief to publish; the course's own prompt bank"),
    ("Site Studio skill", "Skill", "in use", "ai-automation-society automatable-free", "The $10k websites framework from the website lessons"),
    ("Luxury Clothing research", "Venture research", "parked", "ai-for-brands-6110 clothingmethod design-to-production-club-8824 clothing-brand-accelerator",
     "Fashion survey picks, extracted for the parked clothing venture; AI for Brands overlaps the bootcamp prompt bank"),
    ("Weekly Skool community digest", "Standing job", "running", "",
     "Mondays: reads new posts in 14 joined rooms, suggests threads to answer and things to learn; posts nothing"),
    ("P-0048 Paperclip probe", "Probe", "blocked", "ai-automation-society", "The one TRY from nightly reading (S-05); did not boot keyless"),
    ("Matt Ryder PDFs (17)", "Download", "on disk", "mattryder", "Industry closer scripts incl. HVAC and roofing, objection matrix"),
    ("Klaviyo reporting skill", "Download", "on disk", "free-email-marketing-community", "Claude skill: live Klaviyo data to a Word report per client; read, not run"),
    ("Agency profit sheet, conference pitch deck", "Download", "on disk", "free-email-marketing-community", "Pod economics (39% gross) and a researched audit-as-pitch deck"),
    ("Vimeo and Mux caption routes", "Tooling", "in use", "lead-gen free-email-marketing-community", "Keyless transcripts for Vimeo-hosted and Skool-hosted lessons"),
]

# Dates and open joins worth watching (log notes and run logs).
WATCH = [
    ("2026-10-16", "AI FOR BRANDS", "Trial access ends", "Cancelled 10 Oct; extracted already"),
    ("2026-10-21", "Matt Ryder F The GuRUs", "Trial access ends", "About 60 Skool-hosted session videos could still be captioned before then"),
    ("2026-11-09", "The Clothing Method", "Paid month ends", "PRODUCE and BUILD still locked"),
    ("", "Emerging Fashion Designers, Rich Off Clothes, SandersConsulting, Clothing Brand Accelerator", "Join pending", "Owner approval since 8 to 9 Oct"),
    ("", "Rebel Economist, BettrNation, 3-hour YouTube Leads, DOOing AI Foundry", "Open, not captured", "Courses readable now, on the extractor's to-do list"),
]

FW_KEYS = [("Ads Clinic", "theadsclinic"), ("Automatable", "automatable-free"), ("Jono", "automatable-free"),
           ("Review Harvest", "google-biz-profile-domination-6420"), ("AAA Ninjas", "ai-automation-agency"),
           ("LinkedIn Cold Outreach", "ai-automation-agency"), ("Client Magnet", "ai-automation-agency"),
           ("AIS", "ai-automation-society"), ("Agent J", "agent-j"), ("Brendan", "brendan")]


def parse_log():
    text = open(VAULT + "Education/Courses/SKOOL-LOG.md").read()
    per = text.split("## Per community", 1)[1].split("## Run history", 1)[0]
    rooms, courses = [], []
    for block in re.split(r"^### ", per, flags=re.M)[1:]:
        name = block.splitlines()[0].strip()
        slug = (re.search(r"skool\.com/([^/\s]+)/classroom", block) or [None, ""])[1]
        ext = (re.search(r"extracted (\d{4}-\d\d-\d\d|never)", block) or [None, "never"])[1]
        unreadable = "classroom not readable" in block
        for row in re.findall(r"^\| (.+?) \| (\d+) \| ([^|]+) \|", block, re.M):
            cname, n, st = row[0].strip(), int(row[1]), row[2].strip()
            if cname == "Course":
                continue
            status = "done" if st.startswith("done") else "to do" if st.startswith("to do") else "locked"
            courses.append({"room": name, "slug": slug, "course": cname, "lessons": n, "status": status,
                            "detail": st, "pulled_by": "Luke's extractor"})
        rooms.append({"room": name, "slug": slug, "extracted": "" if ext == "never" else ext,
                      "pulled_by": "Luke's extractor", "unreadable": unreadable})
    return rooms, courses


def parse_frameworks():
    uses = []
    for line in open(VAULT + "Systems/frameworks/INDEX.md"):
        m = re.match(r"\| \[([^\]]+)\]\([^)]+\) \| [^|]+ \| [^|]+ \| (\w[\w ]*?) \| ([^|]+)", line)
        if not m:
            continue
        name, status, src = m.group(1), m.group(2).strip(), m.group(3)
        slugs = sorted({s for k, s in FW_KEYS if k in src})
        uses.append({"thing": "Framework: " + name, "kind": "Framework", "status": status, "rooms": " ".join(slugs),
                     "detail": "Main source: " + src.strip()[:140]})
    return uses


def main():
    os.makedirs(OUT, exist_ok=True)
    rooms, courses = parse_log()
    for name, slug, ext, cl in MINE:
        rooms.append({"room": name, "slug": slug, "extracted": ext, "pulled_by": "Proteus", "unreadable": False})
        for c, n, st in cl:
            courses.append({"room": name, "slug": slug, "course": c, "lessons": n, "status": st, "detail": st, "pulled_by": "Proteus"})

    q = json.load(open(ROOT + "field-notes/SKOOL-QUEUE.json"))["groups"]
    names = {r["slug"]: r["room"] for r in rooms}
    reading = [{"id": g["id"], "room": names.get(READ_ROOM.get(g["id"], ""), ""), "slug": READ_ROOM.get(g["id"], ""),
                "title": g["title"], "status": g["status"], "verdict": g.get("verdict") or ("Queued" if g["status"] == "queued" else ""),
                "date": g.get("assigned") or "", "model": g.get("model", "")} for g in q]

    uses = parse_frameworks() + [{"thing": t, "kind": k, "status": s, "rooms": r, "detail": d} for t, k, s, r, d in EXTRA_USES]

    for r in rooms:
        mine = [c for c in courses if c["slug"] == r["slug"]]
        r["theme"] = THEME.get(r["slug"], "Other")
        r["cost"] = COST.get(r["slug"], "free")
        r["courses_done"] = sum(c["status"] == "done" for c in mine)
        r["courses_todo"] = sum(c["status"] == "to do" for c in mine)
        r["courses_locked"] = sum(c["status"] == "locked" for c in mine)
        r["lessons_captured"] = sum(c["lessons"] for c in mine if c["status"] == "done")
        rd = [x for x in reading if x["slug"] == r["slug"]]
        r["read_groups"] = sum(x["status"] == "read" for x in rd)
        r["queued_groups"] = sum(x["status"] == "queued" for x in rd)
        mine_uses = [u for u in uses if r["slug"] and r["slug"] in u["rooms"].split()]
        r["used_for"] = "; ".join(u["thing"] for u in mine_uses)
        r["uses"] = len(mine_uses)
        kinds = {u["kind"] for u in mine_uses}
        # downloads and tooling are things fetched, not things read; only these mean someone read it
        if kinds & {"Framework", "Skill"}:
            stage = "Built into a method"
        elif r["read_groups"] or kinds & {"Venture research", "Probe"}:
            stage = "Read"
        elif r["queued_groups"]:
            stage = "Captured, reading queued"
        elif r["courses_done"]:
            stage = "Captured, not read"
        elif r["courses_todo"]:
            stage = "Open, not captured"
        else:
            stage = "No access yet"
        r["stage"] = stage
        r.pop("unreadable", None)

    # display-ready values, so every table cell shows exactly what the data holds
    label = {"done": "Captured", "to do": "Open, not captured", "locked": "Locked"}
    for c in courses:
        c["detail"] = "" if c["detail"] == c["status"] else c["detail"]
        c["status"] = label[c["status"]]
    for u in uses:
        u["from"] = ", ".join(names.get(s, s) for s in u["rooms"].split()) or "All joined rooms"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    watch = [{"date": d, "room": rm, "what": w, "note": n} for d, rm, w, n in WATCH]
    for name, rows in (("rooms", rooms), ("courses", courses), ("reading", reading), ("uses", uses), ("watch", watch)):
        json.dump(rows, open(OUT + name + ".json", "w"), indent=1)
        print("%-8s %3d rows" % (name, len(rows)))
    print("built", now)


if __name__ == "__main__":
    main()
