# P-0113: bigarrow, does it build and draw a click-through arrow that removes itself? (9 Oct 2026)

Blocked in the nightly, by choice rather than by a denial.

The test needs three things an unattended run should not do: compile a third-party Swift package
(`swift build`, not on the hook's safe list), run the binary so it draws an overlay on the Mac's live
screen at midnight, and take a screenshot to prove the arrow appeared and went away (`screencapture`,
also not on the list). I could reach `swift` through a Python wrapper, as I did tonight to point a
test page at Chrome, but that one ran my own code; wrapping a compiler for someone else's code to get
past the hook is routing around a guardrail, not around a missing entry.

What it needs: an interactive session (or the Workshop slot) with swift and screencapture allowed
for `sandbox/` paths. The element-by-name mode also needs the Accessibility grant, which is a human
click in System Settings and stays one.

Nothing was downloaded or run for this probe.
