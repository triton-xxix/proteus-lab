# P-0030: hn.watch, does a fresh item reach playable video in under 10 seconds, no login?

28 Sep 2026, 23:33 to 23:46 local. Keyless, no account. Scripts in `sandbox/hnwatch/` (copies of
the two that matter are beside this file).

## Verdict: blocked, on a visible browser tab

The pre-generated path is fast and the generate-on-click path did not finish in five minutes from
the only browser I have, which reports itself hidden. Whether the player refuses to start for a
page nobody can see, or generation is just slow tonight, I cannot tell from here.

## How it works, read from the page's own JavaScript

- The list is server-rendered HTML mirroring the Hacker News front page, 30 rows a page, "synced
  N min ago". No cookies, no tracking script; one `sendBeacon` to `/api/e` for counts.
- A click asks `/api/story/<id>` (200 in 0.1 to 2.2 s) which says whether the article could be
  read and how many comments there are. Article unreadable and under ten comments: no explainer.
- Then it sets an iframe to `scrimba.com/explain?link=<hn url>&embed=1,fullwindow&play=1&via=hn_watch`
  and puts a "Making your explainer…" cover over it. The cover lifts only when the frame posts
  `scrimba:embed-watching`; at 60 s the cover says "Still working…"; `scrimba:embed-error` carries
  `throttled`, `pages` (retried after 30 s) or `ineligible` (story left the front page).
- So the video is Scrimba's, hn.watch is a front page and a gate, and "fresh" means a front-page
  story nobody has clicked yet.

## Measured

| | |
|---|---|
| Stories on pages 1 and 2 | 60 |
| Already generated (scrimba title carries "Visual Walkthrough") | 45 |
| Not generated and gate would play | 13 |
| Not generated, gate refuses (article unreadable, under 10 comments) | 2 |
| Explain page fetch, generated story | 0.07 to 0.5 s, 8.4 KB HTML |
| Explain page fetch, ungenerated story | same, 8.0 KB, title "Explain anything" |
| Story 49877678 (79 comments, article ok), play clicked, hidden tab | no `embed-watching` after 284 s, cover on "Still working…", server still ungenerated at 23:45 |
| Story 49884237 (0 comments, article ok), play clicked, hidden tab, emulated 1280x800 | no signal after 55 s, server still ungenerated |
| A plain HTTP GET of the explain URL | does not trigger generation (three stories rechecked ten minutes later, still ungenerated) |

## The confound, stated plainly

The pane in a scheduled run is hidden: `document.visibilityState` is `hidden`, the viewport was
0x0 until I emulated one, and no message ever arrived from the frame, not even an error. A player
that waits for visibility before it generates a video would look exactly like this. A person with
the page open in front of them may well see the claimed few seconds. I could not surface the pane
(the desktop app's pane list has no browser entry), so the question stays open.

## What holds regardless

- For the 45 front-page stories already generated, "click to playable" is one 8 KB page from a
  Cloudflare edge, well under a second before the player's own JavaScript runs.
- The generation is pre-warmed for most of the front page, so most clicks never hit the slow path.
  The claim "a few seconds" is only tested by the 13 that are not warmed, and those are the ones I
  could not measure.
- No login anywhere on the path, and the explain page returned the same to a script as to the
  browser.

## Rerun

Open `https://hn.watch/?item=<id>` for an id from `scan.py`'s candidates list in a visible tab,
click the poster, time until the cover lifts. `titles.py <id>` says whether the server has it.
