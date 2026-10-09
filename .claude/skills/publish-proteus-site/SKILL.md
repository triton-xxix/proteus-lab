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

Pages takes a minute or two after the push. Then with the browser pane tools (allowed unattended):

1. `navigate` to `https://triton-xxix.github.io/proteus-lab/<name>/`; `get_page_text` and confirm the
   headline numbers are the ones you meant to publish.
2. `resize_window` preset `mobile`, reload, screenshot: nothing cut off, no horizontal scroll. Then
   preset `desktop` to reset.
3. `read_console_messages` with `onlyErrors`: none.

Record it in `ARTEFACTS.md`: date, what, the live link, who would care, and how it was checked.

## Never

- Publish on a Salvio's, LBB or Neptune domain, name the employer, or use Luke's name on the page.
- Commit a render over about 50 MB (a 301 MB film was rejected on 7 Oct); publish a 720p copy.
- Put the dashboard key (`state/dash.key`) anywhere near `docs/`.
