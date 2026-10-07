// A film's time structure, drawn from the sketch a research child writes:
//   { nesting, threads: [{ id, label, direction, level, rate, span: [a, b], duration_label, style }],
//     joins: [{ from, to, kind: converge|nest|cross, at, label }] }
// Two renderers: diagram() for a film page, glyph() for an index card. Pure SVG strings, no deps.
'use strict';
const { esc } = require('./render.cjs');

const LANE = ['#EEF1F4', '#C8463A', '#3C9AB4', '#E8A23B', '#9AA6B2'];

function laneColour(t) {
  if (t.style === 'mono') return '#9AA6B2';
  return LANE[Math.min(t.level || 0, LANE.length - 1)];
}

function ticks(x0, x1, y, rate, colour) {
  const step = Math.max(5, 34 / Math.sqrt(Math.max(rate || 1, 0.01)));
  const out = [];
  for (let x = x0 + step; x < x1 - 2; x += step) {
    out.push(`<line x1="${x.toFixed(1)}" y1="${y - 4}" x2="${x.toFixed(1)}" y2="${y + 4}" stroke="${colour}" stroke-opacity="0.45" stroke-width="1"/>`);
  }
  return out.join('');
}

function arrow(x, y, dir, colour) {
  if (dir === 'static') return '';
  const d = dir === 'backward' ? -1 : 1;
  return `<path d="M ${x} ${y} l ${-9 * d} -6 l 0 12 z" fill="${colour}"/>`;
}

function diagram(sketch, opts) {
  const o = Object.assign({ width: 760, labelWidth: 150 }, opts || {});
  const threads = (sketch && sketch.threads || []).slice().sort((a, b) => (a.level || 0) - (b.level || 0));
  if (!threads.length) return '';
  const left = o.labelWidth + 20, right = o.width - 120, top = 30, gap = 46;
  const h = top + threads.length * gap + 30;
  const X = f => left + (right - left) * Math.max(0, Math.min(1, f));
  const Y = i => top + i * gap + 10;
  const idx = Object.fromEntries(threads.map((t, i) => [t.id, i]));
  let s = `<svg class="structure" viewBox="0 0 ${o.width} ${h}" role="img" aria-label="Time structure diagram" xmlns="http://www.w3.org/2000/svg">`;
  s += `<line x1="${left}" y1="${top - 8}" x2="${left}" y2="${h - 18}" stroke="#2A313B"/><line x1="${right}" y1="${top - 8}" x2="${right}" y2="${h - 18}" stroke="#2A313B"/>`;
  s += `<text x="${left}" y="${h - 4}" class="structure__axis">screen time, start</text><text x="${right}" y="${h - 4}" class="structure__axis" text-anchor="end">end</text>`;
  threads.forEach((t, i) => {
    const c = laneColour(t);
    const y = Y(i);
    const x0 = X(t.span ? t.span[0] : 0), x1 = X(t.span ? t.span[1] : 1);
    const dash = t.direction === 'static' ? ' stroke-dasharray="3 5"' : '';
    s += `<text x="${left - 14}" y="${y + 4}" class="structure__label" text-anchor="end" fill="${c}">${esc(t.label || t.id)}</text>`;
    s += `<line x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke="${c}" stroke-width="2.2"${dash}/>`;
    s += ticks(x0, x1, y, t.rate, c);
    s += arrow(t.direction === 'backward' ? x0 : x1, y, t.direction, c);
    if (t.duration_label) s += `<text x="${right + 10}" y="${y + 4}" class="structure__dur">${esc(t.duration_label)}</text>`;
  });
  (sketch.joins || []).forEach(j => {
    const a = idx[j.from], b = idx[j.to];
    if (a == null || b == null) return;
    const x = X(j.at == null ? 1 : j.at);
    const ya = Y(a), yb = Y(b);
    if (j.kind === 'converge') s += `<path d="M ${x} ${ya} Q ${x + 26} ${(ya + yb) / 2} ${x} ${yb}" fill="none" stroke="#E8A23B" stroke-width="1.6"/>`;
    else if (j.kind === 'nest') s += `<path d="M ${x} ${ya + 8} L ${x} ${yb - 8}" stroke="#E8A23B" stroke-width="1.4" stroke-dasharray="2 4"/>`;
    else s += `<path d="M ${x - 6} ${Math.min(ya, yb) + 8} L ${x + 6} ${Math.max(ya, yb) - 8} M ${x + 6} ${Math.min(ya, yb) + 8} L ${x - 6} ${Math.max(ya, yb) - 8}" stroke="#E8A23B" stroke-width="1.6"/>`;
    if (j.label) s += `<text x="${x + 10}" y="${(ya + yb) / 2 + 4}" class="structure__join">${esc(j.label)}</text>`;
  });
  return s + '</svg>';
}

function glyph(sketch) {
  const threads = (sketch && sketch.threads || []).slice().sort((a, b) => (a.level || 0) - (b.level || 0)).slice(0, 5);
  const w = 120, h = 12 + threads.length * 12;
  if (!threads.length) return `<svg class="glyph" viewBox="0 0 120 24" aria-hidden="true"><line x1="8" y1="12" x2="112" y2="12" stroke="#5C6773" stroke-width="2" stroke-dasharray="3 5"/></svg>`;
  let s = `<svg class="glyph" viewBox="0 0 ${w} ${h}" aria-hidden="true">`;
  threads.forEach((t, i) => {
    const c = laneColour(t), y = 8 + i * 12;
    const x0 = 8 + 104 * (t.span ? t.span[0] : 0), x1 = 8 + 104 * (t.span ? t.span[1] : 1);
    s += `<line x1="${x0.toFixed(1)}" y1="${y}" x2="${x1.toFixed(1)}" y2="${y}" stroke="${c}" stroke-width="2"${t.direction === 'static' ? ' stroke-dasharray="2 4"' : ''}/>`;
    s += arrow(t.direction === 'backward' ? x0 : x1, y, t.direction, c).replace('l -9 -6 l 0 12', 'l -6 -4 l 0 8').replace('l 9 -6 l 0 12', 'l 6 -4 l 0 8');
  });
  return s + '</svg>';
}

module.exports = { diagram, glyph };
