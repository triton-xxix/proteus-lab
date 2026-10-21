---
name: publish-proteus-site
description: Publish or republish a Proteus web artefact (the lab page, the record page, the Nolan site, a new page under docs/) to GitHub Pages and check it actually renders on desktop and phone. Use in the Workshop slot or any time a built page should go live.
---

# Publish a Proteus site

Proteus publishes only under its own repositories with the `proteus-` prefix (CHARTER.md). Creating a
new repository is an interactive-session job (`gh repo create` is denied unattended), so a new page in
a scheduled run goes under `docs/` in proteus-lab, which Pages serves from main.

## Which path

| What | Build | Publish |
|---|---|---|
| Lab page (`docs/index.html`, `docs/data.json`) | `node /Users/triton/PROTEUS/bin/build-lab.cjs` (after `python3 /Users/triton/PROTEUS/bin/score.py --write`) | commit `docs/` with `bin/commit.py`; Pages updates on push |
| A new page | write it under `/Users/triton/PROTEUS/docs/<name>/index.html`, self-contained | same; link it from the lab page |
| Sixteen Nights record | `sites/builds/sixteen-nights` scripts | `bash /Users/triton/PROTEUS/bin/record-publish.sh`, then commit `docs/record` |
| Nolan site | `node /Users/triton/PROTEUS/sites/nolan/build.cjs` | `bash /Users/triton/PROTEUS/bin/publish-nolan.sh "message"` (deploy clone in `sandbox/proteus-nolan`) |

Commit with named paths only:
`python3 /Users/triton/PROTEUS/bin/commit.py -m "workshop: <what>" /Users/triton/PROTEUS/docs/<name>`

## Check it renders (not optional)

Pages takes a minute or two after the push. **The browser pane is denied in scheduled runs since
21 Oct 2026** (hook): a navigate hung the nightly 28 h on 17 Oct and the Trials slot on 21 Oct, and a
hung session blocks every later run of that slot. In a scheduled run:

1. `curl -s -o /dev/null -w "%{http_code} %{size_download}" https://triton-xxix.github.io/proteus-lab/<name>/`
   until it answers 200 with the size you built (retry a few times a minute apart, not in a loop).
2. `curl -s https://triton-xxix.github.io/proteus-lab/<name>/ | grep -c "<a headline number>"`: the numbers you
   meant to publish are in the live body.
3. Lint the HTML with a script under the folder (`node` or `python3`), never by eye alone.

In an interactive session the pane is allowed: `navigate`, `get_page_text` for the numbers, `resize_window`
preset `mobile` then `desktop` for cut-offs and horizontal scroll, `read_console_messages` with `onlyErrors`.

Record it in `ARTEFACTS.md`: date, what, the live link, who would care, and how it was checked (say
"curl only" when the pane check has not happened).

## Never

- Publish on a Salvio's, LBB or Neptune domain, name the employer, or use Luke's name on the page.
- Commit a render over about 50 MB (a 301 MB film was rejected on 7 Oct); publish a 720p copy.
- Put the dashboard key (`state/dash.key`) anywhere near `docs/`.
