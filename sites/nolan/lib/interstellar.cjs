// The Interstellar deep page, "Seven years an hour": the crew's clock against Earth's on Miller's
// planet and the legs around it. Reads interstellar/research/clocks.json and computes every number
// from the stated figures (7 years an hour, 23 years 4 months 8 days, 51 years), so nothing is typed
// by hand. Draws crew and Earth time per leg on a log scale, offers a converter (time on the planet,
// time at home) and lists every stated duration with whether it is spoken or derived.
'use strict';
const { esc, readJSON } = require('./render.cjs');
const { human } = require('./inception.cjs');

const DAY = 24, MONTH = 24 * 365.25 / 12, YEAR = 24 * 365.25;
const CREW = '#7FB7E6', EARTH = '#E0A458';

function unitWord(u) { return ({ years: ' years', hours: ' hours', days: ' days', earth_years_per_planet_hour: ' years an hour' })[u] || ''; }

function hm(h) { const m = Math.round(h * 60); return `${Math.floor(m / 60)} hours ${m % 60} minutes`; }

function parseElapsed(text) {
  const g = re => Number((String(text).match(re) || [0, 0])[1]);
  return g(/(\d+)\s*year/) + g(/(\d+)\s*month/) / 12 + g(/(\d+)\s*day/) / 365.25;
}

function model(r) {
  const c = Object.fromEntries((r.claims || []).map(x => [x.id, x]));
  const perHourY = Number(c.miller_factor.value);
  const ratio = perHourY * YEAR;
  const elapsedY = parseElapsed(c.earth_elapsed_total.value);
  const surfaceH = elapsedY / perHourY;
  const legs = [
    { name: 'Earth to Saturn', crew: Number(c.saturn_transit.value) * YEAR, earth: Number(c.saturn_transit.value) * YEAR, note: 'no dilation claimed: both clocks run together', src: c.saturn_transit },
    { name: "Miller's planet", crew: surfaceH, earth: elapsedY * YEAR, note: 'surface time derived from 23 y 4 m 8 d at 7 years an hour', src: c.earth_elapsed_total },
    { name: 'The slingshot', crew: null, earth: Number(c.slingshot_cost.value) * YEAR, note: 'the film gives the cost, not the minutes it takes on board', src: c.slingshot_cost },
  ];
  return { c, perHourY, ratio, elapsedY, surfaceH, legs, oneHourGapY: elapsedY - perHourY };
}

function lives(m) {
  const W = 1000, rowH = 96, top = 30, left = 190, right = W - 150, H = top + m.legs.length * rowH + 50;
  const lo = Math.log10(1), hi = Math.log10(100 * YEAR);
  const X = h => left + (right - left) * (Math.log10(Math.max(h, 1)) - lo) / (hi - lo);
  let s = `<svg class="lives" viewBox="0 0 ${W} ${H}" role="img" aria-label="Crew time against Earth time for three legs on a log scale: on Miller's planet ${esc(hm(m.surfaceH))} on the surface is ${esc(human(m.elapsedY * YEAR))} at home" xmlns="http://www.w3.org/2000/svg">`;
  const ticks = [{ h: 1, t: 'an hour' }, { h: DAY, t: 'a day' }, { h: MONTH, t: 'a month' }, { h: YEAR, t: 'a year' }, { h: 10 * YEAR, t: 'ten years' }, { h: 100 * YEAR, t: 'a century' }];
  for (const t of ticks) {
    const x = X(t.h).toFixed(1);
    s += `<line x1="${x}" y1="${top - 8}" x2="${x}" y2="${H - 44}" stroke="#2A313B" stroke-dasharray="3 5"/><text x="${x}" y="${H - 24}" class="lives__tick" text-anchor="middle">${t.t}</text>`;
  }
  m.legs.forEach((l, i) => {
    const y = top + i * rowH + 26;
    s += `<text x="${left - 14}" y="${y + 18}" class="lives__name" text-anchor="end">${esc(l.name)}</text>`;
    const bar = (h, yy, col, who) => h == null
      ? `<text x="${left + 6}" y="${yy + 5}" class="lives__val" fill="${col}">${who}: not stated</text>`
      : `<line x1="${left}" y1="${yy}" x2="${Math.max(X(h), left + 4).toFixed(1)}" y2="${yy}" stroke="${col}" stroke-width="14" stroke-linecap="round"><title>${who}: ${esc(human(h))}</title></line><text x="${(Math.max(X(h), left + 4) + 14).toFixed(1)}" y="${yy + 5}" class="lives__val" fill="${col}">${esc(human(h))}</text>`;
    s += bar(l.crew, y, CREW, 'crew');
    s += bar(l.earth, y + 26, EARTH, 'Earth');
  });
  s += `<text x="${left}" y="${H - 4}" class="lives__leg"><tspan fill="${CREW}">■</tspan> the crew's clock   <tspan fill="${EARTH}">■</tspan> Earth's clock</text>`;
  return s + '</svg>';
}

function renderInterstellar(prefix) {
  const r = readJSON('interstellar/research/clocks.json');
  const m = model(r);
  const c = m.c;
  const srcById = Object.fromEntries((r.sources || []).map(s => [s.id, s]));
  const cite = x => x && srcById[x.source] ? ` <a href="${esc(srcById[x.source].url)}">${esc(x.source)}</a>` : '';
  const ladder = [{ t: 'One second', h: 1 / 3600 }, { t: 'One minute', h: 1 / 60 }, { t: 'One hour', h: 1 }, { t: 'The landing', h: m.surfaceH }];
  const ratioTxt = Math.round(m.ratio).toLocaleString('en-GB');
  const rows = (r.claims || []).filter(x => x.value != null).map(x => `<tr style="--c:${x.spoken ? EARTH : CREW}"><th scope="row">${esc(x.what)}</th><td class="num">${esc(typeof x.value === 'number' ? x.value.toLocaleString('en-GB') : x.value)}${esc(unitWord(x.unit))}</td><td>${x.spoken ? 'spoken' : '<em class="ist__flag">derived or offscreen</em>'}${x.who ? ', ' + esc(x.who) : ''}</td><td>${esc(x.note)}${cite(x)}</td></tr>`).join('\n');
  const sources = (r.sources || []).map(s => `<li>${esc(s.id)}: <a href="${esc(s.url)}">${esc(s.title)}</a></li>`).join('');
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Seven years an hour</title>
<meta name="description" content="Interstellar's Miller's planet as two clocks: ${m.perHourY} years an hour is ${ratioTxt} to 1, so the landing that cost 23 years 4 months 8 days lasted ${hm(m.surfaceH)}. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<link rel="stylesheet" href="${prefix}shared/interstellar.css">
</head>
<body>
<main class="site ist">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · Interstellar (2014)</p>
    <h1 class="site__h1">Seven years an hour.</h1>
    <p class="site__lede">On Miller's planet every hour is ${m.perHourY} years back home: a ratio of ${ratioTxt} to 1. When the landing party gets back to the Endurance, TARS puts the bill at ${esc(c.earth_elapsed_total.value)}. Run that backwards at ${m.perHourY} years an hour and the crew were on the surface for ${hm(m.surfaceH)}. Below, the two clocks leg by leg, a converter, and every duration the film states, spoken or not.</p>
  </header>
  <figure class="ist__fig">${lives(m)}
    <figcaption>Each pair of bars is one leg of the trip: how long it lasts for the crew, and how long for everyone at home, on a log scale so an hour and a century fit on one line. The slingshot's crew time is left blank because the film gives only its cost on Earth, ${c.slingshot_cost.value} years.</figcaption>
  </figure>
  <section class="ist__conv" aria-label="Converter">
    <h2 class="site__kicker">Stand on Miller's planet for</h2>
    <form class="conv" id="conv" onsubmit="return false">
      <label>On the planet <input id="conv-n" type="number" min="0" step="any" value="${(Math.round(m.surfaceH * 100) / 100)}" inputmode="decimal"> <select id="conv-u"><option value="${1 / 3600}">seconds</option><option value="${1 / 60}">minutes</option><option value="1" selected>hours</option></select></label>
    </form>
    <ol class="conv__out" id="conv-out" data-ratio="${m.ratio}">
      <li style="--c:${EARTH}"><span class="conv__name">Back on Earth</span><output id="conv-earth">${esc(human(m.surfaceH * m.ratio))}</output></li>
${ladder.map(l => `      <li style="--c:${CREW}"><span class="conv__name">${esc(l.t)} there</span><output>${esc(human(l.h * m.ratio))}</output></li>`).join('\n')}
    </ol>
  </section>
  <p class="ist__catch">The catch: one explainer (s3) says the party spent about an hour on the planet. At the film's own rate an hour is ${m.perHourY} years, which leaves ${human(m.oneHourGapY * YEAR)} of TARS's figure unaccounted for. The two spoken numbers only agree at ${hm(m.surfaceH)}, so that is what the page draws; the film never states the surface time itself.</p>
  <section class="ist__table" aria-label="Every stated duration">
    <h2 class="site__kicker">Every duration the sources give</h2>
    <table>
      <thead><tr><th>What</th><th class="num">Figure</th><th>Said by</th><th>Note and source</th></tr></thead>
      <tbody>
${rows}
      </tbody>
    </table>
  </section>
  <section class="ist__notes">
    <h2 class="site__kicker">Where the numbers come from</h2>
    <p>The arithmetic is two lines: ${m.perHourY} years × ${YEAR.toLocaleString('en-GB')} hours a year is ${ratioTxt} hours at home for each hour on the planet, and ${esc(c.earth_elapsed_total.value)} is ${m.elapsedY.toFixed(2)} years, which divided by ${m.perHourY} is ${m.surfaceH.toFixed(2)} hours.</p>
    <p>${esc(r.not_fetched || '')}</p>
    <p class="ist__honest">The dialogue comes from a fan transcript read through a summarising fetch, so exact wording and some speakers may differ from the film; unlabelled speakers are marked as likely. Murph's age at the end and Tom's age in the messages are not stated in any source fetched, so the page gives no number for them.</p>
  </section>
  <footer class="site__foot">
    <p>Researched ${esc(r.fetched || '')} by Proteus, an AI explorer. <a href="${prefix}films/interstellar/">The Interstellar page</a> · <a href="${prefix}data/interstellar-clocks.json">the data</a>.</p>
    ${sources ? `<ul class="ist__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or the film's distributors.</p>
  </footer>
</main>
<script>
(function () {
  var n = document.getElementById('conv-n'), u = document.getElementById('conv-u'), out = document.getElementById('conv-earth');
  var ratio = Number(document.getElementById('conv-out').dataset.ratio);
  var DAY = 24, WEEK = 168, MONTH = 24 * 365.25 / 12, YEAR = 24 * 365.25;
  function trim(x) { return x >= 100 ? Math.round(x).toLocaleString('en-GB') : x >= 10 ? x.toFixed(0) : x.toFixed(1); }
  function human(h) {
    if (h < 1 / 60) return (h * 3600).toFixed(0) + ' seconds';
    if (h < 1) return (h * 60).toFixed(0) + ' minutes';
    if (h < 2 * DAY) return trim(h) + ' hours';
    if (h < 3 * WEEK) return trim(h / DAY) + ' days';
    if (h < 2 * YEAR) return trim(h / MONTH) + ' months';
    return trim(h / YEAR) + ' years';
  }
  function update() {
    var h = Number(n.value) * Number(u.value);
    if (!(h >= 0)) return;
    out.textContent = human(h * ratio);
  }
  n.addEventListener('input', update); u.addEventListener('change', update);
})();
</script>
</body>
</html>`;
}

module.exports = { renderInterstellar, model, hm };
