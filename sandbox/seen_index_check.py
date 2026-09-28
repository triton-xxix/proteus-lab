"""Does harvest.py's seen_index() take anything from the 'Threads pulled from links' block?
Runs the real function on SEEN.md as it stands, then on a copy with the threads block cut out."""
import importlib.util
import os
import re
import tempfile

spec = importlib.util.spec_from_file_location("harvest", "/Users/triton/PROTEUS/bin/harvest.py")
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

full_ids, full_names = h.seen_index()
text = open(h.SEEN).read()
cut = re.sub(r"## Threads pulled from links.*?(?=<!-- vault-verdicts:end -->)", "", text, flags=re.S)
tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
tmp.write(cut)
tmp.close()
h.SEEN = tmp.name
cut_ids, cut_names = h.seen_index()
os.unlink(tmp.name)
print("ids with threads", len(full_ids), "without", len(cut_ids), "only from threads:", sorted(full_ids - cut_ids))
print("names with threads", len(full_names), "without", len(cut_names), "only from threads:", sorted(set(full_names) - set(cut_names)))
print("harvest.py mentions vault-threads:", "vault-threads" in open("/Users/triton/PROTEUS/bin/harvest.py").read())
print("pull sources:", [n for n in dir(h) if n.startswith("pull_")])
