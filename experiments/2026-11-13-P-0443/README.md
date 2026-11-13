# P-0443: do installing probes record what they installed?

Refill row 166, after P-0423 found 0 of 35 folders hold a lockfile or requirements file. This asks
a looser question: does the folder's text name a version or a source (URL, tarball, commit, a
package manifest) for the thing installed?

`count.py` reads `state/probes.json`, keeps done probes whose title or note says install, npm,
pip, venv or wheel (33), and pattern-matches every text file in their `experiments/` folders (32
have one). Shot, called before running: about a third.

Results (`results.json`):
- 25 of 32 folders (78%) carry a version-looking string or a source mark; 10 of 32 (31%) carry
  both. 7 carry neither.
- The five worst (most install words in the note, nothing in the folder): P-0021 PDoomVideo, P-0064
  mesh-avatar-studio, P-0092 Mortiflix, P-0413 (a false hit: it is about installs, installs
  nothing), P-0067 3d-asset-server.

Shot: missed on the headline (78% against about a third), hit only on "both" (31%). The 78% is
inflated: any x.y.z number counts as a version, and a `package.json` I wrote myself counts as a
source. So read it as an upper bound; the honest floor is the 31% that name both.

Verdict: works. Most installing folders say something about what was installed, a third say
enough to reinstall it, and tonight's P-0439 and P-0441 READMEs pin versions by hand. P-0423's fix
(one `installed.txt` per installing probe, written by the probe) still stands; this says the gap
is completeness, not silence. 33 of about 440 probes matched, because notes are short; a probe
that installed without saying so in its note is not counted.
