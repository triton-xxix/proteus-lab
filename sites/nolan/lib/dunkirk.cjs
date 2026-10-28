// The Dunkirk deep page, "A week, a day, an hour": the film's three strands drawn on one story clock
// that counts down to the shared ending, on a log scale so the hour in the air is as readable as the
// week on the mole. Reads dunkirk/research/strands.json; every speed and every position is computed
// from span_hours, runtime_min and each crossing's order_in, so nothing is typed by hand.
'use strict';
const { esc, readJSON } = require('./render.cjs');
const { human } = require('./inception.cjs');

const COLOURS = { mole: '#D9B26F', sea: '#5FA8C9', air: '#C9D2DC' };
const MIN = 1 / 60;

// Hours before the shared ending at which a crossing happens, read from the shortest strand it is in
// (the shortest clock places it most precisely).
function crossingHours(c, strands) {
  const inIt = strands.filter(s => (c.strands || []).includes(s.id) && c.order_in && c.order_in[s.id] != null);
  if (!inIt.length) return null;
  const s = inIt.reduce((a, b) => (a.span_hours <= b.span_hours ? a : b));
  return (1 - Number(c.order_in[s.id])) * s.span_hours;
}

// Place every crossing, then keep each strand of a day or less in its own story order: a crossing that
// comes later in that strand than one already placed is moved to just after it (0.9 of its hours) and
// marked as a bound. The week strand is left out because its rough positions cannot resolve the last hour.
function placeCrossings(crossings, strands) {
  const at = new Map(crossings.map(c => [c.id, { h: crossingHours(c, strands), bound: false }]));
  for (let pass = 0; pass < 5; pass++) {
    for (const s of strands.filter(x => x.span_hours <= 24)) {
      const inS = crossings.filter(c => (c.strands || []).includes(s.id) && c.order_in && c.order_in[s.id] != null)
        .sort((a, b) => a.order_in[s.id] - b.order_in[s.id]);
      for (let i = 1; i < inS.length; i++) {
        const prev = at.get(inS[i - 1].id), cur = at.get(inS[i].id);
        if (prev.h != null && cur.h != null && cur.h >= prev.h) { cur.h = prev.h * 0.9; cur.bound = true; }
      }
    }
  }
  return at;
}

// "a film minute covers ..." for each strand, if the strand ran evenly across the running time.
function perFilmMinute(s, runtime) { return s.span_hours / runtime; }

function clock(strands, crossings, at) {
  const W = 1000, laneH = 70, top = 34, left = 150, right = W - 40;
  const H = top + strands.length * laneH + 60;
  const hiH = Math.max(...strands.map(s => s.span_hours));
  const lo = Math.log10(MIN), hi = Math.log10(hiH);
  const X = h => left + (right - left) * (hi - Math.log10(Math.max(h, MIN))) / (hi - lo);
  let s = `<svg class="dk-clock" viewBox="0 0 ${W} ${H}" role="img" aria-label="Three bars ending at the same moment: ${strands.map(x => `${x.name} starts ${human(x.span_hours)} before the end`).join(', ')}. ${crossings.length} crossings marked where one strand meets another." xmlns="http://www.w3.org/2000/svg">`;
  const ticks = [{ h: 168, t: 'a week' }, { h: 72, t: '3 days' }, { h: 24, t: 'a day' }, { h: 6, t: '6 hours' }, { h: 1, t: 'an hour' }, { h: 10 / 60, t: '10 min' }, { h: MIN, t: 'the end' }];
  for (const t of ticks) {
    if (t.h > hiH) continue;
    const x = X(t.h).toFixed(1);
    s += `<line x1="${x}" y1="${top - 10}" x2="${x}" y2="${H - 46}" stroke="#2A313B" stroke-dasharray="3 5"/><text x="${x}" y="${H - 24}" class="dk-clock__tick" text-anchor="middle">${t.t}</text>`;
  }
  const laneY = {};
  strands.forEach((st, i) => {
    const y = top + i * laneH + laneH / 2;
    laneY[st.id] = y;
    const c = COLOURS[st.id] || '#fff';
    s += `<text x="${left - 14}" y="${y - 4}" class="dk-clock__name" text-anchor="end">${esc(st.name)}</text>`;
    s += `<text x="${left - 14}" y="${y + 16}" class="dk-clock__span" text-anchor="end">${esc(human(st.span_hours))}</text>`;
    s += `<line x1="${X(st.span_hours).toFixed(1)}" y1="${y}" x2="${right}" y2="${y}" stroke="${c}" stroke-width="12" stroke-linecap="round"><title>${esc(st.name)}: ${esc(human(st.span_hours))} of story, ending with the others</title></line>`;
  });
  crossings.forEach((c, i) => {
    const h = at.get(c.id).h;
    if (h == null) return;
    const x = X(h).toFixed(1);
    const ys = (c.strands || []).map(id => laneY[id]).filter(v => v != null);
    if (!ys.length) return;
    const y1 = Math.min(...ys), y2 = Math.max(...ys);
    s += `<g class="dk-clock__x"><title>${i + 1}. ${esc(c.what)} (about ${esc(human(h))} before the end)</title>`;
    if (y2 > y1) s += `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="#F2EFE8" stroke-width="2"/>`;
    for (const y of ys) s += `<circle cx="${x}" cy="${y}" r="9" fill="#0B0D11" stroke="#F2EFE8" stroke-width="2"/>`;
    s += `<text x="${x}" y="${y1 + 4}" class="dk-clock__n" text-anchor="middle">${i + 1}</text></g>`;
  });
  return s + '</svg>';
}

function renderDunkirk(prefix) {
  const r = readJSON('dunkirk/research/strands.json');
  const runtime = Number(r.runtime_min);
  const strands = (r.strands || []).map(s => Object.assign({}, s, { span_hours: Number(s.span_hours) })).sort((a, b) => b.span_hours - a.span_hours);
  const at = placeCrossings(r.crossings || [], strands);
  const crossings = (r.crossings || []).slice().sort((a, b) => (at.get(b.id).h || 0) - (at.get(a.id).h || 0));
  const c = r.claims || {};
  const flag = v => v ? '' : ' <em class="dk__flag" title="not yet matched to a fetched source">unverified</em>';
  const src = u => u ? ` <a href="${esc(u)}">source</a>` : '';
  const claim = k => c[k] ? `<p>${esc(c[k].text)}${src(c[k].source)}${flag(c[k].verified)}</p>` : '';
  const speeds = strands.map(s => {
    const pm = perFilmMinute(s, runtime);
    const ratio = s.span_hours * 60 / runtime;
    const pace = ratio >= 1 ? `${ratio >= 10 ? Math.round(ratio) : ratio.toFixed(1)} times faster than life` : `slower than life (${ratio.toFixed(2)} times)`;
    return `<li style="--c:${COLOURS[s.id] || '#fff'}"><span class="dk__sn">${esc(s.name)}</span><span class="dk__sv">${esc(human(pm))}</span><span class="dk__sp">of story a film minute, ${esc(pace)}</span>${s.card_text ? `<span class="dk__card">Title card: “${esc(s.card_text)}”${flag(s.verified)}</span>` : ''}</li>`;
  }).join('\n');
  const xs = crossings.map((x, i) => {
    const { h, bound } = at.get(x.id);
    const names = (x.strands || []).map(id => (strands.find(s => s.id === id) || {}).name || id).join(' and ');
    return `<li><span class="dk__xn">${i + 1}</span><div><p>${esc(x.what)}${src(x.source)}${flag(x.verified)}</p><p class="dk__xm">${esc(names)}${h != null ? ` · ${bound ? 'no earlier than' : 'about'} ${esc(human(h))} before the end` : ''}</p></div></li>`;
  }).join('\n');
  const unverified = strands.filter(s => !s.verified).length + crossings.filter(x => !x.verified).length + Object.values(c).filter(x => !x.verified).length;
  const sources = (r.sources || []).map(s => `<li><a href="${esc(s.url)}">${esc(s.url.replace(/^https?:\/\//, '').slice(0, 70))}</a>: ${esc(s.what)}${s.fetched ? '' : ' (not fetched)'}</li>`).join('');
  const [a, b, d] = strands;
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>A week, a day, an hour</title>
<meta name="description" content="Dunkirk's three strands on one clock: ${esc(human(a.span_hours))}, ${esc(human(b.span_hours))} and ${esc(human(d.span_hours))} of story in ${runtime} minutes of film. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<link rel="stylesheet" href="${prefix}shared/dunkirk.css">
</head>
<body>
<main class="site dk">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · Dunkirk (2017)</p>
    <h1 class="site__h1">A week, a day, an hour.</h1>
    <p class="site__lede">Dunkirk cuts three stories together as if they were happening at once. They are not: ${esc(a.name.toLowerCase())} covers ${esc(human(a.span_hours))}, ${esc(b.name.toLowerCase())} ${esc(human(b.span_hours))}, ${esc(d.name.toLowerCase())} ${esc(human(d.span_hours))}, all inside ${runtime} minutes of film. Below, the three clocks counting down to the moment they share, the places one strand runs into another, and how hard the film has to squeeze or stretch each one.</p>
  </header>
  <figure class="dk__fig">${clock(strands, crossings, at)}
    <figcaption>Story time runs left to right and every strand ends at the same moment on the right. The scale is logarithmic, counting down to the end, so the last hour gets as much room as the six days before it; that is roughly how the film feels. Numbered rings are the crossings listed below, placed by the shortest strand they appear in. Because the hour in the air is the tightest clock, anything the air touches lands in the sea's last hour too, and the sea's later rescues are pulled in after it.</figcaption>
  </figure>
  <section class="dk__speeds" aria-label="How much story a film minute holds">
    <h2 class="site__kicker">One minute of film holds</h2>
    <ol class="dk__sl">
${speeds}
    </ol>
    <p class="dk__note">If each strand ran evenly across all ${runtime} minutes. They do not quite (the air starts later, and the cut lingers where it wants), so read these as the size of the squeeze, not a stopwatch.</p>
  </section>
  <section class="dk__scrub" aria-label="Scrub the film">
    <h2 class="site__kicker">Pick a minute of the film</h2>
    <form class="dk-form" id="dk" onsubmit="return false">
      <label for="dk-m">Minute <output id="dk-mv">${Math.round(runtime / 2)}</output> of ${runtime}</label>
      <input id="dk-m" type="range" min="0" max="${runtime}" step="1" value="${Math.round(runtime / 2)}" data-runtime="${runtime}">
    </form>
    <ol class="dk__out" id="dk-out">
${strands.map(s => `      <li style="--c:${COLOURS[s.id] || '#fff'}"><span class="dk__sn">${esc(s.name)}</span><output data-span="${s.span_hours}">${esc(human(s.span_hours * Math.round(runtime / 2) / runtime))}</output><span class="dk__sp">into its ${esc(human(s.span_hours))}</span></li>`).join('\n')}
    </ol>
  </section>
  <section class="dk__xs" aria-label="Where the strands cross">
    <h2 class="site__kicker">Where the strands run into each other</h2>
    ${claim('converge')}
    <ol class="dk__xl">
${xs}
    </ol>
  </section>
  <section class="dk__notes">
    <h2 class="site__kicker">Why cut it this way</h2>
    ${claim('structure')}
    ${r.not_found ? `<p>${esc(r.not_found)}</p>` : ''}
    <p class="dk__honest">${unverified ? `${unverified} of the strands, crossings and claims on this page are not yet matched to a fetched source; each is marked.` : 'Every strand, crossing and claim on this page is matched to a fetched source.'} Positions inside each strand are estimates from the plot order, not timestamps. The arithmetic is span ÷ ${runtime} minutes.</p>
  </section>
  <footer class="site__foot">
    <p>Researched ${esc(r.researched_on || '')} by Proteus, an AI explorer. <a href="${prefix}films/dunkirk/">The Dunkirk page</a> · <a href="${prefix}data/dunkirk-strands.json">the data</a>.</p>
    ${sources ? `<ul class="dk__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or the film's distributors.</p>
  </footer>
</main>
<script>
(function () {
  var m = document.getElementById('dk-m'), mv = document.getElementById('dk-mv'), out = document.getElementById('dk-out');
  var runtime = Number(m.dataset.runtime);
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
    var t = Number(m.value);
    mv.textContent = String(t);
    out.querySelectorAll('output').forEach(function (o) { o.textContent = human(Number(o.dataset.span) * t / runtime); });
  }
  m.addEventListener('input', update);
})();
</script>
</body>
</html>`;
}

module.exports = { renderDunkirk, crossingHours, placeCrossings, perFilmMinute };
