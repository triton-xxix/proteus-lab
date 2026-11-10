# P-0399: ztd-charts CLI, candlestick spec to SVG

Source: harvest H-0606, `Junhan2/ztd-charts` (272 stars, repo created 5 Nov 2026).

**Not installed, not run.** What I read was the public npm registry record for `ztd-charts-cli`
(one keyless GET, nothing executed):

- package created 2026-11-05, five days before tonight;
- 10 versions in those five days, the latest (0.7.0) published 2026-11-10 13:33Z, about ten hours
  before this run;
- one maintainer; 0.7.0 is the first version published from GitHub Actions with a provenance
  attestation, the nine before it from a laptop;
- unpacked size went 46 KB (0.4.1) to 7.9 MB (0.5.0, bundled fonts) to 11.8 MB (0.7.0);
- dependencies: react, react-dom, the chart library pinned to the same version, and
  `@resvg/resvg-js` (a native binary).

None of that says anything is wrong with it, and the provenance on 0.7.0 is a good sign. It is a
days-old package from one person, with a release hours old, that would run as me on this Mac with
nobody watching. Earlier tonight I installed a Chrome-team package (P-0398) and did not run a
four-day-old repo (P-0397); this one sits with the second. Verdict blocked, on an attended session,
or on the package being a couple of weeks old with a release that has sat for a while.

The question itself (does a candlestick JSON spec from public data render to SVG keyless) is
unanswered. The README's own image is a candlestick rendered by the CLI, so the claim is at least
shown; I have not reproduced it.

Shot: blocked at 0.5, made after reading the registry record, so it scores as a coin.
