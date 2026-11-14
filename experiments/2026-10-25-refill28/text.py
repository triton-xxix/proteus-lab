import html, re, sys
raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
raw = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", raw)
txt = html.unescape(re.sub(r"<[^>]+>", " ", raw))
txt = re.sub(r"\s+", " ", txt)
for s in re.split(r"(?<=[.!?]) ", txt):
    if re.search(r"(?i)resol|dispute|bond|propos|challenge", s) and len(s) < 400:
        print("-", s.strip())
