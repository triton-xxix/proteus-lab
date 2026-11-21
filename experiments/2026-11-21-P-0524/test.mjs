// P-0524: does Zpup keep a small object visible on a big floor at four angles, with no script in
// the SVG? A 300x300 floor lying flat, a 20 px box near one far corner (the case the Show HN says
// one-point sorting gets wrong). Paint order is read from the SVG: the box is visible if every
// box piece is painted after the floor. Writes one SVG per angle and results.json.
import { writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire('/Users/triton/PROTEUS/sandbox/p0524/inst/');
const core = await import(require.resolve('@zpup/core'));
const { renderSvg, renderSpinSvg, rect, box } = core;
const OUT = '/Users/triton/PROTEUS/experiments/2026-11-21-P-0524/';
const FLOOR = '#6a8f4e';

const results = [];
for (const corner of [[120, 120], [-120, 120], [120, -120], [-120, -120]]) {
  for (const y of [0, 90, 180, 270]) {
    const scene = {
      width: 420, height: 320, rotate: { x: -30, y },
      children: [
        rect({ width: 300, height: 300, fill: true, stroke: 0, color: FLOOR, rotate: { x: 90 } }),
        box({ width: 20, height: 20, depth: 20, color: '#d23', translate: { x: corner[0], y: -10, z: corner[1] } }),
      ],
    };
    const svg = renderSvg(scene);
    const pieces = [...svg.matchAll(/<(path|polygon|ellipse|circle|rect)\b[^>]*>/g)].map((m) => m[0]);
    const floorIdx = pieces.map((p, i) => (p.toLowerCase().includes(FLOOR) ? i : -1)).filter((i) => i >= 0);
    const other = pieces.map((p, i) => (p.toLowerCase().includes(FLOOR) ? -1 : i)).filter((i) => i >= 0);
    const ok = floorIdx.length > 0 && other.length > 0 && Math.max(...floorIdx) < Math.min(...other);
    const name = `c${corner[0]}_${corner[1]}_y${y}.svg`;
    if (corner[0] === 120 && corner[1] === 120) writeFileSync(OUT + name, svg);
    results.push({ corner, y, pieces: pieces.length, floorPieces: floorIdx.length, boxPieces: other.length,
      boxAfterFloor: ok, hasScript: /<script/i.test(svg), bytes: svg.length });
  }
}
const spin = renderSpinSvg({ width: 420, height: 320, rotate: { x: -30, y: 0 }, children: [
  rect({ width: 300, height: 300, fill: true, stroke: 0, color: FLOOR, rotate: { x: 90 } }),
  box({ width: 20, height: 20, depth: 20, color: '#d23', translate: { x: 120, y: -10, z: 120 } }),
] });
writeFileSync(OUT + 'spin.svg', spin);
const summary = { version: (await import(require.resolve('@zpup/core/package.json'), { with: { type: 'json' } })).default.version,
  renders: results.length, boxAfterFloor: results.filter((r) => r.boxAfterFloor).length,
  anyScript: results.some((r) => r.hasScript) || /<script/i.test(spin), spinBytes: spin.length,
  spinHasSmil: /<animate|<set/.test(spin) };
writeFileSync(OUT + 'results.json', JSON.stringify({ summary, results }, null, 1));
console.log(JSON.stringify(summary));
for (const r of results) if (!r.boxAfterFloor) console.log('FAIL', JSON.stringify(r));
