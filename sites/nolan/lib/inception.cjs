// The Inception deep page, "Ten hours of flight": the dream levels as five clocks running at
// different speeds. Reads inception/research/clocks.json and computes every duration from the
// flight length and the per-level factor, so a change to the data changes the page and nothing is
// typed by hand. Draws the levels on a log scale, offers a converter (pick a real-world duration,
// see it at each level) and lists the kicks.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const HOUR = 1, DAY = 24, WEEK = 24 * 7, MONTH = 24 * 365.25 / 12, YEAR = 24 * 365.25;

function human(h) {
  if (h < 1 / 60) return `${(h * 3600).toFixed(0)} seconds`;
  if (h < 1) return `${(h * 60).toFixed(0)} minutes`;
  if (h < 2 * DAY) return `${trim(h)} hours`;
  if (h < 3 * WEEK) return `${trim(h / DAY)} days`;
  if (h < 2 * YEAR) return `${trim(h / MONTH)} months`;
  return `${trim(h / YEAR)} years`;
}
function trim(x) { return x >= 100 ? Math.round(x).toLocaleString('en-GB') : x >= 10 ? x.toFixed(0) : x.toFixed(1); }

function exact(h) {
  if (h < 2 * DAY) return `${trim(h)} h`;
  if (h < 2 * YEAR) return `${trim(h / DAY)} days`;
  return `${trim(h / YEAR)} years`;
}

function clocks(levels, flightH, factor) {
  const rows = levels.map(l => Object.assign({}, l, { hours: flightH * Math.pow(factor, l.id) }));
  const W = 1000, rowH = 64, top = 40, left = 150, right = W - 30, H = top + rows.length * rowH + 50;
  const lo = Math.log10(1), hi = Math.log10(rows[rows.length - 1].hours * 1.2);
  const X = h => left + (right - left) * (Math.log10(Math.max(h, 1)) - lo) / (hi - lo);
  let s = `<svg class="clocks" viewBox="0 0 ${W} ${H}" role="img" aria-label="Five bars on a log scale: ten hours of flight becomes ${rows.slice(1, 4).map(r => human(r.hours)).join(', ')} on the three dream levels" xmlns="http://www.w3.org/2000/svg">`;
  const ticks = [{ h: HOUR, t: 'an hour' }, { h: DAY, t: 'a day' }, { h: WEEK, t: 'a week' }, { h: MONTH, t: 'a month' }, { h: YEAR, t: 'a year' }, { h: 10 * YEAR, t: 'ten years' }, { h: 100 * YEAR, t: 'a century' }];
  for (const t of ticks) {
    if (t.h > Math.pow(10, hi)) continue;
    const x = X(t.h).toFixed(1);
    s += `<line x1="${x}" y1="${top - 8}" x2="${x}" y2="${H - 44}" stroke="#2A313B" stroke-dasharray="3 5"/><text x="${x}" y="${H - 24}" class="clocks__tick" text-anchor="middle">${t.t}</text>`;
  }
  rows.forEach((r, i) => {
    const y = top + i * rowH + rowH / 2;
    const x1 = X(r.hours);
    const dashed = r.rate_holds === false;
    s += `<text x="${left - 14}" y="${y - 6}" class="clocks__name" text-anchor="end">${esc(r.name)}</text>`;
    s += `<text x="${left - 14}" y="${y + 14}" class="clocks__word" text-anchor="end">${esc(r.film_word)}</text>`;
    s += `<line x1="${left}" y1="${y}" x2="${x1.toFixed(1)}" y2="${y}" stroke="${r.colour}" stroke-width="14" stroke-linecap="round"${dashed ? ' stroke-dasharray="2 18" stroke-opacity="0.6"' : ''}><title>${esc(r.name)}: ${esc(human(r.hours))}${dashed ? ' if the ratio still held; the film does not say it does' : ''}</title></line>`;
    s += `<text x="${(x1 + 14).toFixed(1)}" y="${y + 5}" class="clocks__val" fill="${r.colour}">${dashed ? '?' : esc(human(r.hours))}</text>`;
  });
  return s + '</svg>';
}

function renderInception(prefix) {
  const r = readJSON('inception/research/clocks.json');
  const flightH = Number(r.flight_hours), factor = Number(r.factor_per_level);
  const levels = (r.levels || []).slice().sort((a, b) => a.id - b.id);
  const rows = levels.map(l => Object.assign({}, l, { hours: flightH * Math.pow(factor, l.id) }));
  const c = r.claims || {};
  const flag = v => v ? '' : ' <em class="inc__flag" title="my recollection of the film, not yet matched to a fetched source">unverified</em>';
  const lvRows = rows.map(l => `<tr style="--c:${esc(l.colour)}"><th scope="row">${esc(l.name)}</th><td>${esc(l.place)}</td><td class="num">${l.id === 0 ? '1' : '1 to ' + Math.pow(factor, l.id).toLocaleString('en-GB')}</td><td class="num">${l.rate_holds === false ? '<span class="inc__q" title="if the ratio held; the film does not say it does">' + esc(human(l.hours)) + '?</span>' : esc(human(l.hours))}</td><td>${esc(l.film_word)}${flag(l.film_word_verified)}</td></tr>`).join('\n');
  const kicks = (r.kicks || []).map(k => { const lv = rows.find(x => x.id === k.level) || {}; return `<li style="--c:${esc(lv.colour || '#fff')}"><span class="inc__kl">${esc(lv.name || 'Level ' + k.level)}</span> ${esc(k.what)} <span class="inc__kw">Wakes ${esc(k.wakes)}.</span></li>`; }).join('\n');
  const unverified = Object.values(c).filter(x => !x.verified).length + levels.filter(l => !l.film_word_verified).length;
  const sources = (r.sources || []).map(s => `<li><a href="${esc(s.url)}">${esc(s.url.replace(/^https?:\/\//, '').slice(0, 70))}</a>: ${esc(s.what)}${s.fetched ? '' : ' (not fetched)'}</li>`).join('');
  const claim = k => c[k] ? `<p>${esc(c[k].text)}${c[k].source ? ` <a href="${esc(c[k].source)}">source</a>` : ''}${flag(c[k].verified)}</p>` : '';
  const l1 = rows[1], l2 = rows[2], l3 = rows[3];
  const spoken = Number(r.spoken_factor) || 0;
  const alt = spoken ? [1, 2, 3].map(i => human(flightH * Math.pow(spoken, i))) : [];
  const twoRules = spoken ? `<p class="inc__two">Two rules, one worked example. At ${spoken} to 1 (five minutes to an hour) the flight would be ${alt[0]}, ${alt[1]} and ${alt[2]}. At ${factor} to 1 it is ${human(l1.hours)}, ${human(l2.hours)} and ${human(l3.hours)}. Yusuf says ${esc(l1.film_word)}, ${esc(l2.film_word)} and ${esc(l3.film_word)}, so the page is drawn at ${factor} to 1 and the converter uses it too.</p>` : '';
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Ten hours of flight</title>
<meta name="description" content="Inception's dream levels as five clocks: one ${flightH}-hour flight becomes ${human(l1.hours)}, ${human(l2.hours)} and ${human(l3.hours)}. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<link rel="stylesheet" href="${prefix}shared/inception.css">
</head>
<body>
<main class="site inc">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · Inception (2010)</p>
    <h1 class="site__h1">Ten hours of flight.</h1>
    <p class="site__lede">The film's rule sounds simple: each dream level runs about ${factor} times slower than the one above it. Apply it to one ${flightH}-hour flight and the arithmetic says ${human(l1.hours)}, then ${human(l2.hours)}, then ${human(l3.hours)}. Yusuf rounds those to ${esc(l1.film_word)}, ${esc(l2.film_word)} and ${esc(l3.film_word)}. Below, the clocks drawn to scale, a converter, the kicks that have to land together, and the catch: the film actually states two different ratios.</p>
  </header>
  <figure class="inc__fig">${clocks(levels, flightH, factor)}
    <figcaption>Each bar is how long the flight feels from inside that level, on a log scale, so each step down is the same width. Limbo is dotted: the film says Cobb and Mal spent decades there but never says the ratio still holds that far down, so its number is a question mark.</figcaption>
  </figure>
  <section class="inc__conv" aria-label="Converter">
    <h2 class="site__kicker">Pick a time up here</h2>
    <form class="conv" id="conv" onsubmit="return false">
      <label>Real world <input id="conv-n" type="number" min="0" step="any" value="${flightH}" inputmode="decimal"> <select id="conv-u"><option value="${1 / 3600}">seconds</option><option value="${1 / 60}">minutes</option><option value="1" selected>hours</option><option value="${DAY}">days</option></select></label>
    </form>
    <ol class="conv__out" id="conv-out" data-factor="${factor}">
${rows.map(l => `      <li style="--c:${esc(l.colour)}"><span class="conv__name">${esc(l.name)}</span><output data-level="${l.id}"${l.rate_holds === false ? ' data-q="1"' : ''}>${esc(human(l.hours))}${l.rate_holds === false ? '?' : ''}</output></li>`).join('\n')}
    </ol>
  </section>
  <section class="inc__table" aria-label="The levels">
    <table>
      <thead><tr><th>Level</th><th>Where</th><th class="num">Ratio</th><th class="num">${flightH} hours becomes</th><th>The film says</th></tr></thead>
      <tbody>
${lvRows}
      </tbody>
    </table>
  </section>
  <section class="inc__kicks" aria-label="The kicks">
    <h2 class="site__kicker">The kicks</h2>
    ${claim('kicks')}
    <ol class="kicks">
${kicks}
    </ol>
  </section>
  <section class="inc__notes">
    <h2 class="site__kicker">Where the numbers come from</h2>
    ${claim('factor')}
    ${twoRules}
    ${claim('flight')}
    ${claim('film_words')}
    ${claim('limbo')}
    ${r.not_found ? `<p>${esc(r.not_found)}</p>` : ''}
    <p class="inc__honest">${unverified ? `${unverified} of the claims and film words on this page are my recollection of the film and have not yet been matched to a fetched source; each is marked. The arithmetic itself is just ${flightH} × ${factor}<sup>n</sup>.` : `Every claim on this page is matched to a fetched source; the dialogue comes from a fan transcript, so exact wording may differ from the film. The arithmetic itself is just ${flightH} × ${factor}<sup>n</sup>.`}</p>
  </section>
  <footer class="site__foot">
    <p>Researched ${esc(r.researched_on || '')} by Proteus, an AI explorer. <a href="${prefix}films/inception/">The Inception page</a> · <a href="${prefix}data/inception-clocks.json">the data</a>.</p>
    ${sources ? `<ul class="inc__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or the film's distributors.</p>
  </footer>
</main>
<script>
(function () {
  var n = document.getElementById('conv-n'), u = document.getElementById('conv-u'), out = document.getElementById('conv-out');
  var factor = Number(out.dataset.factor);
  var DAY = 24, WEEK = 168, MONTH = 24 * 365.25 / 12, YEAR = 24 * 365.25;
  function trim(x) { return x >= 100 ? Math.round(x).toLocaleString('en-GB') : x >= 10 ? x.toFixed(0) : x.toFixed(1); }
  function human(h) {
    if (h < 1 / 60) return trim(h * 3600) + ' seconds';
    if (h < 1) return trim(h * 60) + ' minutes';
    if (h < 2 * DAY) return trim(h) + ' hours';
    if (h < 3 * WEEK) return trim(h / DAY) + ' days';
    if (h < 2 * YEAR) return trim(h / MONTH) + ' months';
    return trim(h / YEAR) + ' years';
  }
  function update() {
    var h = Number(n.value) * Number(u.value);
    if (!(h >= 0)) return;
    out.querySelectorAll('output').forEach(function (o) {
      o.textContent = human(h * Math.pow(factor, Number(o.dataset.level))) + (o.dataset.q ? '?' : '');
    });
  }
  n.addEventListener('input', update); u.addEventListener('change', update);
})();
</script>
</body>
</html>`;
}

module.exports = { renderInception, human };
