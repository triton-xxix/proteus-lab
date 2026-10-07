// The career timeline for the index hero: thirteen films on a line from 1998 to 2026.
// Bar height is runtime where a researched page has it; queued films are outlines.
'use strict';
const { esc } = require('./render.cjs');

function timeline(films, data) {
  const W = 1200, H = 300, left = 40, right = W - 40, base = H - 50;
  const y0 = 1997.5, y1 = 2026.8;
  const X = y => left + (right - left) * (y - y0) / (y1 - y0);
  let s = `<svg class="career" viewBox="0 0 ${W} ${H}" role="img" aria-label="Christopher Nolan's thirteen features from 1998 to 2026, bar height is runtime" xmlns="http://www.w3.org/2000/svg">`;
  s += `<line x1="${left}" y1="${base}" x2="${right}" y2="${base}" stroke="#2A313B" stroke-width="1.5"/>`;
  for (let y = 1998; y <= 2026; y += 2) s += `<text x="${X(y)}" y="${base + 22}" class="career__year" text-anchor="middle">${y}</text>`;
  films.slice().sort((a, b) => a.year - b.year).forEach(f => {
    const d = data[f.slug];
    const runtime = d && d.facts && d.facts.runtime_min && d.facts.runtime_min.value;
    const h = runtime ? Math.round((runtime / 190) * 200) : 70;
    const x = X(f.year + 0.5);
    const live = !!d || !!f.deep_page;
    const fill = live ? (f.time_structure_kind === 'linear' || f.time_structure_kind === 'linear-with-flashbacks' ? '#9AA6B2' : '#E8A23B') : 'none';
    const href = f.deep_page ? f.deep_page : (d ? `films/${f.slug}/` : null);
    const bar = `<rect x="${x - 14}" y="${base - h}" width="28" height="${h}" rx="2" fill="${fill}" stroke="${live ? 'none' : '#3A434E'}" stroke-dasharray="${live ? '0' : '3 3'}"><title>${esc(f.title)} (${f.year})${runtime ? ', ' + runtime + ' min' : ', coming'}</title></rect>`;
    const label = `<text x="${x}" y="${base - h - 8}" class="career__title" text-anchor="middle">${esc(f.title.length > 14 ? f.title.replace('The Dark Knight Rises', 'TDK Rises').replace('Batman Begins', 'Batman B.').replace('The Dark Knight', 'TDK') : f.title)}</text>`;
    s += href ? `<a href="${href}">${bar}${label}</a>` : bar + label;
  });
  s += `<text x="${left}" y="22" class="career__key">Filled bars are researched pages. Height is runtime. Amber bars play with time; grey ones run straight.</text>`;
  return s + '</svg>';
}

module.exports = { timeline };
