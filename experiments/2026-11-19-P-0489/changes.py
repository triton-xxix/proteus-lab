"""P-0489 step 1: print the managerial changes table from the 2025-26 Premier League article.

    python3 changes.py

Keyless, read only. Saves the raw section as changes-section.txt beside itself.
"""
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = "proteus-probe/0.1 (keyless research script)"
PAGE = "2025–26 Premier League"


def main():
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(
        {"action": "parse", "page": PAGE, "prop": "wikitext", "format": "json", "formatversion": "2"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = json.loads(r.read())["parse"]["wikitext"]
    m = re.search(r"==+\s*Managerial changes\s*==+(.*?)\n==[^=]", text, re.S)
    if not m:
        print("no Managerial changes section; headings:", re.findall(r"\n(==+[^=\n]+==+)", text))
        return 1
    sec = m.group(1)
    (HERE / "changes-section.txt").write_text(sec)
    print(sec[:9000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
