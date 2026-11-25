// P-0568: P-0557's three-bar cycle with each bar split in two at its midpoint (the docs' fix for cycles).
// Same geometry, same 108 renders (tilts -90, -60, -35, 36 turns each), same truth method (sampled depths
// where projected quads overlap), but six pieces with six colours, and truth over every pair of pieces
// from different bars. Called shot: wrong count 0 at all 108 renders, 6 pieces in the SVG.
import { writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire('/Users/triton/PROTEUS/sandbox/p0524/inst/');
const core = await import(require.resolve('@zpup/core'));
const { renderSvg, checkSceneWarnings, path } = core;
const OUT = '/Users/triton/PROTEUS/experiments/2026-11-25-P-0568/';
const COLORS = ['#d22a2a', '#a01010', '#2a8fd2', '#105fa0', '#2ad25a', '#10a03a'];
const W = 420, H = 420;
const P = [[0, -100], [86.6, 50], [-86.6, 50]];
const RISE = 30, HALF = 8, EXT = 0.3;
function pieceQuads(i) {
  const [ax, az] = P[i], [bx, bz] = P[(i + 1) % 3];
  const dx = bx - ax, dz = bz - az, L = Math.hypot(dx, dz);
  const nx = -dz / L * HALF, nz = dx / L * HALF;
  const at = (t) => [ax + dx * t, -RISE * t, az + dz * t];
  const q = (s, e) => [[s[0] + nx, s[1], s[2] + nz], [e[0] + nx, e[1], e[2] + nz], [e[0] - nx, e[1], e[2] - nz], [s[0] - nx, s[1], s[2] - nz]];
  const s = at(-EXT), m = at(0.5), e = at(1 + EXT);
  return [q(s, m), q(m, e)];
}
const QUADS = [0, 1, 2].flatMap(pieceQuads); // piece k belongs to bar floor(k/2)
const pieces = QUADS.map((q, k) => path({ id: 'p' + k, path: q.map(([x, y, z]) => ({ x, y, z })), closed: true, fill: true, stroke: 0, color: COLORS[k] }));
const rad = (d) => d * Math.PI / 180;
function project([x, y, z], r) {
  let c = Math.cos(rad(r.z || 0)), s = Math.sin(rad(r.z || 0));
  [x, y] = [x * c - y * s, x * s + y * c];
  c = Math.cos(rad(r.y || 0)); s = Math.sin(rad(r.y || 0));
  [x, z] = [x * c + z * s, -x * s + z * c];
  c = Math.cos(rad(r.x || 0)); s = Math.sin(rad(r.x || 0));
  [y, z] = [y * c - z * s, y * s + z * c];
  return [x, y, z];
}
function inside(pt, poly) {
  let c = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > pt[1]) !== (yj > pt[1]) && pt[0] < (xj - xi) * (pt[1] - yi) / (yj - yi) + xi) c = !c;
  }
  return c;
}
function depthAt(q3, x, y) {
  const [a, b, c] = q3;
  const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
  if (Math.abs(n[2]) < 1e-9) return null;
  return a[2] - (n[0] * (x - a[0]) + n[1] * (y - a[1])) / n[2];
}
function truth(r) {
  const pq = QUADS.map((q) => q.map((p) => project(p, r)));
  const out = {};
  for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
    if (Math.floor(i / 2) === Math.floor(j / 2)) continue; // same bar: adjacent, coplanar
    let iNear = 0, jNear = 0;
    for (let a = 0; a <= 40; a++) for (let b = 0; b <= 8; b++) {
      const t = a / 40, w = b / 8, q = pq[i];
      const p = [0, 1, 2].map((k) => (1 - w) * ((1 - t) * q[0][k] + t * q[1][k]) + w * ((1 - t) * q[3][k] + t * q[2][k]));
      if (!inside(p, pq[j].map((x) => [x[0], x[1]]))) continue;
      const dj = depthAt(pq[j], p[0], p[1]);
      if (dj === null) continue;
      if (p[2] > dj + 1e-6) iNear++; else if (dj > p[2] + 1e-6) jNear++;
    }
    out[`${i}-${j}`] = iNear + jNear === 0 ? null : iNear && jNear ? 'mixed' : iNear ? 'i' : 'j';
  }
  return out;
}
function paintOrder(svg) {
  const els = [...svg.matchAll(/<(path|polygon)\b[^>]*>/g)].map((m) => m[0].toLowerCase());
  return { pieces: els.length, idx: COLORS.map((c) => els.map((p, k) => (p.includes(c) ? k : -1)).filter((k) => k >= 0)) };
}
const results = [];
for (const tilt of [-90, -60, -35]) for (let k = 0; k < 36; k++) {
  const r = { x: tilt, y: k * 10 };
  const svg = renderSvg({ width: W, height: H, rotate: r, children: pieces });
  const tr = truth(r), po = paintOrder(svg);
  let wrong = 0, overlaps = 0, mixed = 0, missing = 0;
  for (const [key, t] of Object.entries(tr)) {
    if (!t) continue; overlaps++;
    if (t === 'mixed') { mixed++; continue; }
    const [i, j] = key.split('-').map(Number);
    const nearer = t === 'i' ? i : j, farther = t === 'i' ? j : i;
    if (!po.idx[nearer].length || !po.idx[farther].length) { missing++; continue; }
    if (!(Math.min(...po.idx[nearer]) > Math.max(...po.idx[farther]))) wrong++;
  }
  results.push({ tilt, turn: r.y, pieces: po.pieces, overlaps, mixed, wrong, missing });
  if (tilt === -90 && k === 0) writeFileSync(OUT + 'top_y0.svg', svg);
}
const by = (t) => results.filter((r) => r.tilt === t);
const summary = {
  renders: results.length,
  renders_wrong: results.filter((r) => r.wrong > 0).length,
  wrong_pairs_total: results.reduce((a, r) => a + r.wrong, 0),
  mixed_pairs_total: results.reduce((a, r) => a + r.mixed, 0),
  missing_total: results.reduce((a, r) => a + r.missing, 0),
  pieces_min_max: [Math.min(...results.map((r) => r.pieces)), Math.max(...results.map((r) => r.pieces))],
  per_tilt: Object.fromEntries([-90, -60, -35].map((t) => [t, { renders_wrong: by(t).filter((r) => r.wrong > 0).length, overlapping_pairs: by(t).reduce((a, r) => a + r.overlaps, 0) }])),
  warnings: checkSceneWarnings({ width: W, height: H, rotate: { x: -90 }, children: pieces }).map((x) => x.message),
};
writeFileSync(OUT + 'results.json', JSON.stringify({ summary, results }, null, 1));
console.log(JSON.stringify(summary, null, 1));
