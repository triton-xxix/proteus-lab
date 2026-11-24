// P-0557: does Zpup paint a three-way cyclic overlap right (A over B over C over A, no shapes touching)?
// Three flat filled bars (4-point paths) along the sides of a triangle, each rising 30 units from its
// start to its end, extended past the corners so each corner is a crossing where the arriving bar is
// 30 units above the leaving one. Truth per pair: sample points on one bar, project with my own copy
// of Zpup's rotation (z, then y, then x; checked against the SVG), and where they land inside the
// other bar's projected quad, compare depths. A render is wrong if the SVG paint order disagrees with
// the truth for any overlapping pair. Also: 30 separated boxes, checkSceneWarnings only.
import { writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
const require = createRequire('/Users/triton/PROTEUS/sandbox/p0524/inst/');
const core = await import(require.resolve('@zpup/core'));
const { renderSvg, checkSceneWarnings, checkScene, path, box } = core;
const OUT = '/Users/triton/PROTEUS/experiments/2026-11-24-P-0557/';
const COLORS = ['#d22a2a', '#2a8fd2', '#2ad25a'];
const W = 420, H = 420;

const P = [[0, -100], [86.6, 50], [-86.6, 50]]; // x, z
const RISE = 30, HALF = 8, EXT = 0.3;
function barQuad(i) {
  const [ax, az] = P[i], [bx, bz] = P[(i + 1) % 3];
  const dx = bx - ax, dz = bz - az, L = Math.hypot(dx, dz);
  const nx = -dz / L * HALF, nz = dx / L * HALF;
  const at = (t) => [ax + dx * t, -RISE * t, az + dz * t]; // y is down, so up is -y
  const s = at(-EXT), e = at(1 + EXT);
  return [[s[0] + nx, s[1], s[2] + nz], [e[0] + nx, e[1], e[2] + nz], [e[0] - nx, e[1], e[2] - nz], [s[0] - nx, s[1], s[2] - nz]];
}
const QUADS = [0, 1, 2].map(barQuad);
const bars = QUADS.map((q, i) => path({ id: 'bar' + i, path: q.map(([x, y, z]) => ({ x, y, z })), closed: true, fill: true, stroke: 0, color: COLORS[i] }));

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
function depthAt(q3, x, y) { // plane through the projected quad's first three points, solve z at (x, y)
  const [a, b, c] = q3;
  const u = [b[0] - a[0], b[1] - a[1], b[2] - a[2]], v = [c[0] - a[0], c[1] - a[1], c[2] - a[2]];
  const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
  if (Math.abs(n[2]) < 1e-9) return null;
  return a[2] - (n[0] * (x - a[0]) + n[1] * (y - a[1])) / n[2];
}
function truth(r) { // for each pair i<j: 'i' if i nearer where they overlap, 'j', 'mixed' or null (no overlap)
  const pq = QUADS.map((q) => q.map((p) => project(p, r)));
  const out = {};
  for (let i = 0; i < 3; i++) for (let j = i + 1; j < 3; j++) {
    let iNear = 0, jNear = 0;
    for (let a = 0; a <= 40; a++) for (let b = 0; b <= 8; b++) {
      const t = a / 40, w = b / 8; // bilinear sample on bar i
      const q = pq[i];
      const p = [0, 1, 2].map((k) => (1 - w) * ((1 - t) * q[0][k] + t * q[1][k]) + w * ((1 - t) * q[3][k] + t * q[2][k]));
      if (!inside(p, pq[j].map((x) => [x[0], x[1]]))) continue;
      const dj = depthAt(pq[j], p[0], p[1]);
      if (dj === null) continue;
      if (p[2] > dj + 1e-6) iNear++; else if (dj > p[2] + 1e-6) jNear++;
    }
    out[`${i}${j}`] = iNear + jNear === 0 ? null : iNear && jNear ? 'mixed' : iNear ? 'i' : 'j';
  }
  return { out, pq };
}
function paintOrder(svg) {
  const pieces = [...svg.matchAll(/<(path|polygon)\b[^>]*>/g)].map((m) => m[0].toLowerCase());
  const idx = COLORS.map((c) => pieces.map((p, k) => (p.includes(c) ? k : -1)).filter((k) => k >= 0));
  return { pieces: pieces.length, idx, first: pieces[0] };
}

const results = [];
let projCheck = null;
for (const tilt of [-90, -60, -35]) {
  for (let k = 0; k < 36; k++) {
    const r = { x: tilt, y: k * 10 };
    const scene = { width: W, height: H, rotate: r, children: bars };
    const svg = renderSvg(scene);
    const { out, pq } = truth(r);
    const po = paintOrder(svg);
    if (!projCheck) projCheck = { mine_first_corner_screen: [pq[0][0][0] + W / 2, pq[0][0][1] + H / 2], svg_first_piece: po.first.slice(0, 160) };
    let wrong = 0, overlaps = 0, mixed = 0;
    const pairs = {};
    for (const key of Object.keys(out)) {
      const t = out[key]; if (!t) continue; overlaps++;
      if (t === 'mixed') { mixed++; pairs[key] = 'mixed'; continue; }
      const [i, j] = [+key[0], +key[1]];
      const nearer = t === 'i' ? i : j, farther = t === 'i' ? j : i;
      const ok = Math.min(...po.idx[nearer]) > Math.max(...po.idx[farther]); // nearer painted after
      pairs[key] = ok ? 'ok' : 'WRONG'; if (!ok) wrong++;
    }
    results.push({ tilt, turn: r.y, pieces: po.pieces, perBar: po.idx.map((a) => a.length), overlaps, mixed, wrong, pairs });
    if (tilt === -90 && k === 0) writeFileSync(OUT + 'top_y0.svg', svg);
    if (tilt === -35 && k === 0) writeFileSync(OUT + 'tilt35_y0.svg', svg);
  }
}
const cycleScene = { width: W, height: H, rotate: { x: -90 }, children: bars };
const cycleWarnings = checkSceneWarnings(cycleScene);

// 30 separated boxes on a 6x5 grid with jittered sizes and heights, no two touching
const boxes = [];
let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
for (let gx = 0; gx < 6; gx++) for (let gz = 0; gz < 5; gz++) {
  const w = 14 + rnd() * 16, h = 10 + rnd() * 50, d = 14 + rnd() * 16;
  boxes.push(box({ width: w, height: h, depth: d, color: `rgb(${40 + gx * 30},${60 + gz * 30},120)`, translate: { x: (gx - 2.5) * 40, y: -h / 2, z: (gz - 2) * 40 } }));
}
const clutterWarnings = [];
for (let k = 0; k < 36; k++) {
  const sc = { width: W, height: H, rotate: { x: -30, y: k * 10 }, children: boxes };
  const v = checkScene(sc); if (v.length) clutterWarnings.push({ turn: k * 10, invalid: v.length });
  const ws = checkSceneWarnings(sc); if (ws.length) clutterWarnings.push({ turn: k * 10, warnings: ws.map((x) => x.message) });
  renderSvg(sc);
}
writeFileSync(OUT + 'clutter_y0.svg', renderSvg({ width: W, height: H, rotate: { x: -30, y: 0 }, children: boxes }));

const by = (t) => results.filter((r) => r.tilt === t);
const summary = {
  version: (await import(require.resolve('@zpup/core/package.json'), { with: { type: 'json' } })).default.version,
  projCheck,
  cycle: Object.fromEntries([-90, -60, -35].map((t) => [t, {
    renders: by(t).length,
    renders_with_all3_overlaps: by(t).filter((r) => r.overlaps === 3).length,
    renders_wrong: by(t).filter((r) => r.wrong > 0).length,
    wrong_pairs_total: by(t).reduce((a, r) => a + r.wrong, 0),
    mixed_pairs_total: by(t).reduce((a, r) => a + r.mixed, 0),
    max_pieces_per_bar: Math.max(...by(t).flatMap((r) => r.perBar)),
  }])),
  cycleWarnings: cycleWarnings.map((x) => x.message),
  clutter: { boxes: boxes.length, renders: 36, warnings_or_invalid: clutterWarnings },
};
writeFileSync(OUT + 'results.json', JSON.stringify({ summary, results }, null, 1));
console.log(JSON.stringify(summary, null, 1));
