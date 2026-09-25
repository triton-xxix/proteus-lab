"""P-0018 part 2: read the access guidance and the developer page as plain text, and try the obvious
keyless API paths. Usage: python3 fuel_finder_read.py OUT_DIR
"""
import html
import json
import os
import re
import sys
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (proteus probe; keyless read)"}


def get(url, accept="*/*"):
    try:
        req = urllib.request.Request(url, headers={**UA, "Accept": accept})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.headers.get("Content-Type"), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type"), e.read()[:3000]
    except Exception as e:
        return None, None, f"{type(e).__name__}: {e}".encode()


def text_of(raw):
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    notes = []
    code, _, raw = get("https://www.gov.uk/api/content/guidance/access-the-latest-fuel-prices-and-forecourt-data-via-api-or-email", "application/json")
    doc = json.loads(raw)
    body = text_of(doc.get("details", {}).get("body", "").encode())
    notes.append("## GOV.UK guidance: access via API or email\n\n" + body)
    print("GUIDANCE", code, body[:3000])

    code, _, raw = get("https://www.developer.fuel-finder.service.gov.uk/access-latest-fuelprices")
    dev = text_of(raw)
    notes.append("## Developer portal: access-latest-fuelprices\n\n" + dev)
    print("\nDEVPAGE", code, dev[:3000])
    api_links = sorted(set(re.findall(r"https?://[A-Za-z0-9.\-]*fuel-finder[^\s\"'<>)\\]*", raw.decode("utf-8", "replace"))))
    print("\nLINKS", api_links[:30])

    tries = [
        "https://www.fuel-finder.service.gov.uk/api/v1/pfs",
        "https://www.fuel-finder.service.gov.uk/api/v1/pfs/fuel-prices",
        "https://api.fuel-finder.service.gov.uk/v1/pfs",
        "https://www.developer.fuel-finder.service.gov.uk/api",
    ] + [l for l in api_links if "api" in l.lower()][:6]
    for u in tries:
        c, ct, b = get(u, "application/json")
        line = f"TRY {u} -> {c} {ct} {b[:200].decode('utf-8', 'replace')!r}"
        print(line)
        notes.append(line)

    with open(os.path.join(out, "access-notes.md"), "w") as f:
        f.write("\n\n".join(notes))


if __name__ == "__main__":
    main()
