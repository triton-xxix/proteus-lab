# P-0162, lab site contrast

Question: do the lab site's text colours meet the WCAG 4.5:1 body-text rule (web.dev Learn Design)?

Method: `contrast.py` computes the WCAG ratio for the five text tokens (ink, muted, tide, buoy, keep) on both surfaces (paper, raised), light and dark, using the hex values in `docs/index.html` lines 13 to 21.

Numbers (`results.json`): 20 pairs, 0 fail. Lowest is light buoy on paper at 4.70; highest ink on raised at 14.88. I called 3 or more failures; the site has none, so nothing to fix and no before/after.

Not done: `docs/record/scrollcraft.css` (49 colour lines, separate page), the translucent wash backgrounds, text on images, large-text and non-text 3:1 rules.
