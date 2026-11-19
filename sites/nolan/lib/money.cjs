// The career page "The money and the minutes": every film's budget against its worldwide gross on one
// log axis, and its runtime, across the filmography. Every figure is read from films/<slug>.json (the
// research child's sourced facts); multiples, totals, medians and ranks are computed here, never typed.
// Built 19 Nov 2026 Workshop. Charts are HTML grids, not SVG, so labels keep their size on a phone.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const LOG_MIN = 3, LOG_MAX = 10; // $1,000 to $10bn

function model() {
  const reg = readJSON('films.json');
  const rows = reg.films.map(f => {
    const d = readJSON(`films/${f.slug}.json`);
    const F = d.facts || {}, R = (d.reception || {}).at_release || {};
    const need = { runtime: F.runtime_min, budget: F.budget_usd, gross: F.gross_usd };
    for (const [k, v] of Object.entries(need)) {
      if (!v || typeof v.value !== 'number' || !(v.value > 0)) throw new Error(`${f.slug}: no numeric ${k}`);
    }
    return {
      slug: f.slug, title: d.title || f.title, year: d.year || f.year, deep: f.deep_page,
      runtime: F.runtime_min.value, budget: F.budget_usd.value, gross: F.gross_usd.value,
      multiple: F.gross_usd.value / F.budget_usd.value,
      mc: R.metacritic && R.metacritic.value, rt: R.rt && R.rt.value,
      budgetNote: F.budget_usd.note || '', grossNote: F.gross_usd.note || '', grossAsOf: F.gross_usd.as_of || '',
      budgetSrc: F.budget_usd.source, grossSrc: F.gross_usd.source,
      unverified: ['budget_usd', 'gross_usd'].filter(k => F[k].unverified).concat(
        ['metacritic', 'rt'].filter(k => R[k] && R[k].unverified)),
    };
  }).sort((a, b) => a.year - b.year);
  const by = (k, dir = 1) => rows.slice().sort((a, b) => dir * (a[k] - b[k]));
  const median = xs => { const s = xs.slice().sort((a, b) => a - b), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
  const sum = k => rows.reduce((t, r) => t + r[k], 0);
  const first3 = rows.slice(0, 3);
  const disputed = rows.filter(r => /disagree|range|differ/i.test(r.budgetNote + ' ' + r.grossNote));
  const mcRank = by('mc', -1);
  return {
    rows, n: rows.length,
    best: by('multiple', -1)[0], worst: by('multiple')[0],
    medianMultiple: median(rows.map(r => r.multiple)),
    totalBudget: sum('budget'), totalGross: sum('gross'),
    totalMinutes: sum('runtime'), cheapest: by('budget')[0],
    shortest: by('runtime')[0], longest: by('runtime', -1)[0],
    first3, first3Budget: first3.reduce((t, r) => t + r.budget, 0),
    biggestGross: by('gross', -1)[0], topBudget: rows.filter(r => r.budget === by('budget', -1)[0].budget),
    under2: rows.filter(r => r.multiple < 2),
    over5: rows.filter(r => r.multiple >= 5),
    disputed,
    mcTop: mcRank[0], mcTopMultipleRank: by('multiple', -1).indexOf(mcRank[0]) + 1,
  };
}

function money(v) {
  if (v >= 1e9) return `$${(v / 1e9).toFixed(2).replace(/0$/, '')}bn`;
  if (v >= 1e6) { const m = v / 1e6; return `$${m >= 100 ? Math.round(m) : m.toFixed(1).replace(/\.0$/, '')}m`; }
  return `$${Math.round(v).toLocaleString('en-GB')}`;
}
const times = x => `${x >= 10 ? x.toFixed(0) : x.toFixed(1)}×`;
const pos = v => (100 * (Math.log10(v) - LOG_MIN) / (LOG_MAX - LOG_MIN)).toFixed(2);

function moneyChart(m) {
  const ticks = [];
  for (let e = LOG_MIN; e <= LOG_MAX; e++) ticks.push(e);
  const tickLabel = e => e >= 9 ? `$${10 ** (e - 9)}bn` : e >= 6 ? `$${10 ** (e - 6)}m` : `$${(10 ** e).toLocaleString('en-GB')}`;
  const grid = ticks.map(e => `<span class="mn-tick" style="left:${pos(10 ** e)}%"></span>`).join('');
  const axis = ticks.filter(e => e % 2 === 1 || e === LOG_MAX).map(e => `<span class="mn-ax" style="left:${pos(10 ** e)}%">${tickLabel(e)}</span>`).join('');
  const rows = m.rows.map(r => `<li class="mn-row${r === m.best ? ' mn-row--best' : ''}${r === m.worst ? ' mn-row--worst' : ''}">
      <span class="mn-name">${esc(r.title)} <i>${r.year}</i></span>
      <span class="mn-track">${grid}<span class="mn-line" style="left:${pos(r.budget)}%;width:${(pos(r.gross) - pos(r.budget)).toFixed(2)}%"></span><span class="mn-dot mn-dot--b" style="left:${pos(r.budget)}%" title="budget ${money(r.budget)}"></span><span class="mn-dot mn-dot--g" style="left:${pos(r.gross)}%" title="gross ${money(r.gross)}"></span></span>
      <span class="mn-x">${times(r.multiple)}</span>
    </li>`).join('\n');
  return `<ol class="mn-chart" aria-label="Budget to worldwide gross for ${m.n} films on a log scale">
${rows}
    <li class="mn-row mn-row--axis" aria-hidden="true"><span></span><span class="mn-track mn-track--axis">${axis}</span><span></span></li>
  </ol>`;
}

function runtimeChart(m) {
  const max = Math.ceil(m.longest.runtime / 30) * 30;
  const rows = m.rows.map(r => `<li class="rt-row"><span class="mn-name">${esc(r.title)} <i>${r.year}</i></span><span class="rt-track"><span class="rt-bar${r === m.longest || r === m.shortest ? ' rt-bar--end' : ''}" style="width:${(100 * r.runtime / max).toFixed(2)}%"></span></span><span class="mn-x">${r.runtime}</span></li>`).join('\n');
  return `<ol class="rt-chart" aria-label="Runtime in minutes for ${m.n} films, scale 0 to ${max}">
${rows}
  </ol>`;
}

function renderMoney(prefix) {
  const m = model();
  const table = m.rows.map(r => {
    const notes = [r.budgetNote && `Budget: ${r.budgetNote}`, r.grossNote && `Gross: ${r.grossNote}`].filter(Boolean).join(' ');
    const flag = r.unverified.length ? ` <span class="mn-flag" title="marked unverified by the research: ${esc(r.unverified.join(', '))}">unverified ${esc(r.unverified.join(', ').replace(/_usd/g, ''))}</span>` : '';
    return `<tr class="mn-tr"><th scope="row">${r.deep ? `<a href="${prefix}${esc(r.deep)}">${esc(r.title)}</a>` : `<a href="${prefix}films/${esc(r.slug)}/">${esc(r.title)}</a>`}${flag}</th><td>${r.year}</td><td>${r.runtime}</td><td><a href="${esc(r.budgetSrc)}">${money(r.budget)}</a></td><td><a href="${esc(r.grossSrc)}">${money(r.gross)}</a></td><td>${times(r.multiple)}</td><td>${r.mc == null ? '' : r.mc}</td><td>${r.rt == null ? '' : r.rt + '%'}</td><td class="mn-note">${esc(notes)}${r.grossAsOf ? ` <i>Gross read ${esc(r.grossAsOf)}.</i>` : ''}</td></tr>`;
  }).join('\n');
  const asOf = m.rows.map(r => r.grossAsOf).filter(Boolean).sort();
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>The money and the minutes</title>
<meta name="description" content="${m.n} Christopher Nolan films, budget against worldwide gross and runtime: ${esc(m.best.title)} made ${times(m.best.multiple)} its budget, ${esc(m.worst.title)} ${times(m.worst.multiple)}; ${m.shortest.runtime} minutes to ${m.longest.runtime}. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<style>
.mn-big{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,12rem),1fr));gap:1rem;margin:2rem 0;padding:0;list-style:none}
.mn-big li{border-top:2px solid #2A313B;padding-top:.6rem}
.mn-big b{display:block;font:700 2.4rem/1 Archivo,sans-serif;color:#F2EFE8}
.mn-big span{color:#8A93A0;font-size:.95rem}
.mn-chart,.rt-chart{list-style:none;padding:0;margin:1.5rem 0}
.mn-row,.rt-row{display:grid;grid-template-columns:minmax(6rem,11rem) 1fr 3.4rem;gap:.7rem;align-items:center;min-height:2rem}
.mn-name{font-size:.95rem;line-height:1.2}.mn-name i{color:#8A93A0;font-style:normal;font-size:.85rem}
.mn-x{font:600 1rem Archivo,sans-serif;text-align:right;font-variant-numeric:tabular-nums}
.mn-track{position:relative;height:1.6rem}
.mn-tick{position:absolute;top:0;bottom:0;width:1px;background:#1C2129}
.mn-line{position:absolute;top:50%;height:3px;margin-top:-1.5px;background:linear-gradient(90deg,#3C9AB4,#E0A04A)}
.mn-dot{position:absolute;top:50%;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%}
.mn-dot--b{border:2px solid #3C9AB4;background:#0B0D11}.mn-dot--g{background:#E0A04A}
.mn-row--best .mn-x{color:#E0A04A}.mn-row--worst .mn-x{color:#C8463A}
.mn-track--axis{height:1.2rem}.mn-ax{position:absolute;transform:translateX(-50%);color:#8A93A0;font-size:.8rem;white-space:nowrap}
.mn-key{color:#8A93A0;font-size:.95rem}.mn-key b{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:-1px;margin-right:.3rem}
.rt-track{height:.9rem;background:#151A21;border-radius:2px}.rt-bar{display:block;height:100%;background:#C9D2DC;border-radius:2px}.rt-bar--end{background:#E0A04A}
.mn-fig{margin:2rem 0}.mn-fig figcaption,.mn-note-p{color:#8A93A0;font-size:.95rem;line-height:1.5;max-width:62ch}
.mn-wrap{overflow-x:auto;margin:1rem 0}
.mn-table{border-collapse:collapse;font-size:.9rem;min-width:44rem}
.mn-table th,.mn-table td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid #1C2129;vertical-align:top}
.mn-table td:nth-child(n+2):nth-child(-n+8){font-variant-numeric:tabular-nums;white-space:nowrap}
.mn-note{color:#8A93A0;font-size:.82rem;min-width:16rem}
.mn-flag{display:inline-block;font-size:.72rem;color:#C8463A;border:1px solid #C8463A;border-radius:3px;padding:0 .3rem;margin-left:.3rem;font-weight:500}
@media (max-width:560px){.mn-row,.rt-row{grid-template-columns:5.6rem 1fr 2.8rem;gap:.45rem}.mn-name{font-size:.8rem}.mn-ax{font-size:.68rem}.mn-big b{font-size:2rem}}
</style>
</head>
<body>
<main class="site mn">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · the whole career</p>
    <h1 class="site__h1">The money and the minutes.</h1>
    <p class="site__lede">${m.n} films, from ${esc(m.rows[0].title)} in ${m.rows[0].year} to ${esc(m.rows[m.n - 1].title)} in ${m.rows[m.n - 1].year}. ${m.best === m.cheapest ? 'The cheapest, ' : ''}${esc(m.best.title)}${m.best === m.cheapest ? ',' : ''} took ${times(m.best.multiple)} its budget at the box office, more than any film since. The weakest return is ${esc(m.worst.title)} at ${times(m.worst.multiple)}. The median film took ${times(m.medianMultiple)}. In between, the films got ${(m.longest.runtime / m.shortest.runtime).toFixed(1)} times longer: ${m.shortest.runtime} minutes to ${m.longest.runtime}.</p>
  </header>
  <ul class="mn-big" aria-label="The numbers">
    <li><b>${times(m.best.multiple)}</b><span>${esc(m.best.title)}'s gross over its budget, the best return of the ${m.n}</span></li>
    <li><b>${times(m.medianMultiple)}</b><span>the median film's gross over its budget</span></li>
    <li><b>${money(m.totalGross)}</b><span>worldwide gross of all ${m.n}, on ${money(m.totalBudget)} of budgets</span></li>
    <li><b>${m.totalMinutes.toLocaleString('en-GB')}</b><span>minutes to watch them all, about ${Math.round(m.totalMinutes / 60)} hours</span></li>
  </ul>
  <figure class="mn-fig">
    <p class="mn-key"><b style="border:2px solid #3C9AB4"></b>budget <b style="background:#E0A04A;margin-left:1rem"></b>worldwide gross · the number is gross over budget</p>
    ${moneyChart(m)}
    <figcaption>Log scale: each gridline is ten times the last, so a line's length shows the multiple, not the dollars. ${esc(m.best.title)} sits alone on the left at ${money(m.best.budget)}; the first ${m.first3.length} films together cost ${money(m.first3Budget)}, and ${m.topBudget.map(r => esc(r.title)).join(' and ')} cost ${(m.topBudget[0].budget / m.first3Budget).toFixed(1)} times that${m.topBudget.length > 1 ? ' each' : ''} (${money(m.topBudget[0].budget)}). ${m.over5.length} of ${m.n} took five times their budget or more; ${m.under2.length} took under two (${m.under2.map(r => esc(r.title)).join(', ')}).</figcaption>
  </figure>
  <figure class="mn-fig">
    <h2 class="site__kicker">Runtime, in minutes</h2>
    ${runtimeChart(m)}
    <figcaption>${esc(m.shortest.title)} is the shortest at ${m.shortest.runtime} minutes, ${esc(m.longest.title)} the longest at ${m.longest.runtime}. The critics' top score here, Metacritic ${m.mcTop.mc} for ${esc(m.mcTop.title)}, belongs to the ${m.mcTopMultipleRank === 1 ? 'best' : `number ${m.mcTopMultipleRank}`} return of the ${m.n}.</figcaption>
  </figure>
  <section aria-label="Every film">
    <h2 class="site__kicker">Every film, with where each number came from</h2>
    <div class="mn-wrap"><table class="mn-table">
      <thead><tr><th scope="col">Film</th><th scope="col">Year</th><th scope="col">Min</th><th scope="col">Budget</th><th scope="col">Gross</th><th scope="col">×</th><th scope="col">Metacritic</th><th scope="col">RT</th><th scope="col">What the sources said</th></tr></thead>
      <tbody>
${table}
      </tbody>
    </table></div>
    <p class="mn-note-p">What this is not. Gross is worldwide ticket sales, not profit: cinemas keep a share and budgets leave out marketing, so a ${times(m.worst.multiple)} film may well have lost money. Nothing is adjusted for inflation. Budgets are reported estimates, and on ${m.disputed.length} of ${m.n} films the fetched sources gave a range or disagreed (the note says which). Grosses were read between ${esc(asOf[0])} and ${esc(asOf[asOf.length - 1])}; ${esc(m.rows[m.n - 1].title)}'s may still be rising. Scores are current, not from release week.</p>
  </section>
  <footer class="site__foot">
    <p>Built ${new Date().toISOString().slice(0, 10)} by Proteus, an AI explorer, from the research on each film page. <a href="${prefix}data/money.json">The data</a>.</p>
    <p>Not affiliated with Christopher Nolan, Syncopy or any studio.</p>
  </footer>
</main>
</body>
</html>`;
}

function data() {
  const m = model();
  return { built_from: 'sites/nolan/films/*.json', films: m.rows.map(r => ({ slug: r.slug, title: r.title, year: r.year, runtime_min: r.runtime, budget_usd: r.budget, gross_usd: r.gross, multiple: +r.multiple.toFixed(3), metacritic: r.mc, rt: r.rt, gross_as_of: r.grossAsOf, unverified: r.unverified, budget_source: r.budgetSrc, gross_source: r.grossSrc })) };
}

module.exports = { renderMoney, model, data, money, times };
