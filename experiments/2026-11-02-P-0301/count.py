"""P-0301: check episode 1 against the template's own measurable rules (section 4 of xingji-manju SKILL.md):
4 to 7 scenes, 250 to 400 dialogue characters including inner voice and voice-over, spoken lines at least two
thirds of the total, and names in dialogue present in the character table."""
import json
import re

EXP = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0301"
script = open(EXP + "/逆行者/03-分集剧本-第01集.md", encoding="utf-8").read()
bible = open(EXP + "/逆行者/01-企划案.md", encoding="utf-8").read()

scenes = re.findall(r"^场\d+｜", script, flags=re.M)
line_re = re.compile(r"^([一-鿿]{2,4})(（(内心|画外)）)?：(.+)$", re.M)
SKIP = {"结尾钩子", "本集进度", "本集对白", "本集卡点", "冷开场"}


def chars(s):
    # count Han characters, letters and digits; punctuation and spaces do not count
    return len(re.findall(r"[一-鿿A-Za-z0-9]", s))


total = spoken = 0
speakers = set()
lines = []
for m in line_re.finditer(script):
    who, _, kind, text = m.groups()
    if who in SKIP:
        continue
    n = chars(text)
    total += n
    if kind is None:
        spoken += n
    speakers.add(who)
    lines.append({"who": who, "kind": kind or "spoken", "chars": n})

missing = sorted(w for w in speakers if w not in bible)
res = {
    "scenes": len(scenes), "scenes_ok": 4 <= len(scenes) <= 7,
    "dialogue_lines": len(lines), "dialogue_chars": total, "dialogue_ok": 250 <= total <= 400,
    "spoken_chars": spoken, "spoken_share": round(spoken / total, 3) if total else 0,
    "spoken_ok": total and spoken / total >= 2 / 3,
    "speakers": sorted(speakers), "speakers_missing_from_bible": missing,
}
json.dump(res, open(EXP + "/count.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(json.dumps(res, ensure_ascii=False))
