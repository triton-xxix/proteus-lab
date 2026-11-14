// The Oppenheimer deep page, "Everything goes back to 1947": the film's three strands on one real
// calendar, every year read from oppenheimer/research/calendar.json (itself quoted from the fetched
// Wikipedia plot). Gaps, spans and look-back distances are computed here, never typed. Film order is
// not drawn: no fetched source gives scene timestamps yet.
'use strict';
const { esc, readJSON } = require('./render.cjs');

const COLOURS = { life: '#E0A04A', h54: '#C8463A', h59: '#C9D2DC' };

function model(r) {
  const byId = new Map(r.events.map(e => [e.id, e]));
  const dated = r.events.filter(e => e.from != null);
  const first = Math.min(...dated.map(e => e.from));
  const last = Math.max(...dated.map(e => e.to));
  const looks = (r.lookbacks || []).map(l => {
    const a = byId.get(l.from), b = byId.get(l.to);
    if (!a || !b) throw new Error('lookback ' + l.id + ' names a missing event');
    return Object.assign({}, l, { years: a.from - b.from, fromYear: a.from, toYear: b.from });
  });
  const h54 = r.events.find(e => e.strand === 'h54'), h59 = r.events.find(e => e.strand === 'h59');
  const strandSpan = id => {
    const es = dated.filter(e => e.strand === id);
    return es.length ? [Math.min(...es.map(e => e.from)), Math.max(...es.map(e => e.to))] : null;
  };
  return {
    byId, dated, first, last, span: last - first, looks,
    hearingGap: h59.from - h54.from,
    counts: {
      events: r.events.length,
      year: r.events.filter(e => e.stated === 'year' || e.stated === 'month').length,
      decade: r.events.filter(e => e.stated === 'decade').length,
      none: r.events.filter(e => e.from == null).length,
    },
    strandSpan,
  };
}

function calendar(r, m) {
  const W = 1000, left = 30, right = W - 30, laneH = 74, top = 70;
  const lanes = r.strands.map(s => s.id);
  const H = top + lanes.length * laneH + 50;
  const y0 = Math.floor(m.first / 5) * 5, y1 = Math.ceil(m.last / 5) * 5;
  const X = y => left + (right - left) * (y - y0) / (y1 - y0);
  const laneY = id => top + lanes.indexOf(id) * laneH + laneH / 2;
  let s = `<svg class="op-cal" viewBox="0 0 ${W} ${H}" role="img" aria-label="A calendar from ${y0} to ${y1}. ${m.dated.length} dated events in three strands; two arcs reach back to ${m.byId.get('einstein').from}, one from the ${m.looks[0].fromYear} hearing and one from the ${m.looks[1].fromYear} award." xmlns="http://www.w3.org/2000/svg">`;
  for (let y = y0; y <= y1; y += 5) {
    const x = X(y).toFixed(1);
    s += `<line x1="${x}" y1="${top - 20}" x2="${x}" y2="${H - 34}" stroke="#2A313B" stroke-dasharray="3 5"/><text x="${x}" y="${H - 14}" class="op-cal__tick" text-anchor="middle">${y}</text>`;
  }
  r.strands.forEach(st => {
    const y = laneY(st.id);
    s += `<text x="${left}" y="${y - 22}" class="op-cal__name">${esc(st.name)}</text>`;
    s += `<line x1="${left}" y1="${y}" x2="${right}" y2="${y}" stroke="#1C2129" stroke-width="2"/>`;
  });
  // look-back arcs, drawn above the lanes
  m.looks.forEach((l, i) => {
    const a = m.byId.get(l.from), b = m.byId.get(l.to);
    const xa = X(a.from), xb = X(b.from), ya = laneY(a.strand), yb = laneY(b.strand);
    const peak = top - 46 + i * 14;
    s += `<path class="op-cal__arc op-cal__arc--${esc(l.id)}" d="M${xa.toFixed(1)},${ya - 10} C${xa.toFixed(1)},${peak} ${xb.toFixed(1)},${peak} ${xb.toFixed(1)},${yb - 10}" fill="none" stroke="${i ? '#F2EFE8' : '#8A93A0'}" stroke-width="2" ${i ? '' : 'stroke-dasharray="6 5"'} marker-end="url(#op-head)"><title>${esc(l.what)} (${l.years} years back)</title></path>`;
  });
  s += `<defs><marker id="op-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#F2EFE8"/></marker></defs>`;
  m.dated.forEach(e => {
    const y = laneY(e.strand), c = COLOURS[e.strand] || '#fff';
    const label = e.stated === 'decade' ? `the ${e.from}s` : (e.month ? `${e.month} ${e.from}` : String(e.from));
    if (e.to > e.from) {
      s += `<rect class="op-cal__ev" x="${X(e.from).toFixed(1)}" y="${y - 8}" width="${(X(e.to + 1) - X(e.from)).toFixed(1)}" height="16" rx="8" fill="${c}" opacity="0.55"><title>${esc(label)}: ${esc(e.what)}</title></rect>`;
    } else {
      s += `<circle class="op-cal__ev" cx="${X(e.from).toFixed(1)}" cy="${y}" r="${e.pivot ? 11 : 8}" fill="${e.pivot ? '#0B0D11' : c}" stroke="${c}" stroke-width="${e.pivot ? 4 : 0}"><title>${esc(label)}: ${esc(e.what)}</title></circle>`;
    }
    s += `<text x="${X(e.from).toFixed(1)}" y="${y + 28}" class="op-cal__yr" text-anchor="middle">${esc(e.stated === 'decade' ? e.from + 's' : String(e.from))}</text>`;
  });
  return s + '</svg>';
}

function renderOppenheimer(prefix) {
  const r = readJSON('oppenheimer/research/calendar.json');
  const m = model(r);
  const piv = m.byId.get('einstein');
  const [claim, reveal] = m.looks;
  const c = r.claims || {};
  const cl = k => c[k] ? `<p>${esc(c[k].text)} <a href="${esc(c[k].source)}">source</a></p>` : '';
  const rows = r.events.map(e => {
    const when = e.from == null ? 'no year given' : e.stated === 'decade' ? `the ${e.from}s` : (e.month ? `${e.month} ${e.from}` : String(e.from));
    const st = r.strands.find(s => s.id === e.strand);
    return `<li class="op-ev${e.pivot ? ' op-ev--pivot' : ''}" style="--c:${COLOURS[e.strand] || '#fff'}"><span class="op-ev__when">${esc(when)}</span><div><p>${esc(e.what)}</p><p class="op-ev__m">${esc(st.name)} · “${esc(e.quote)}”</p></div></li>`;
  }).join('\n');
  const strandRows = r.strands.map(st => {
    const sp = m.strandSpan(st.id);
    const txt = !sp ? 'no dated event' : sp[0] === sp[1] ? `${sp[0]}` : `${sp[0]} to ${sp[1]}, ${sp[1] - sp[0]} years`;
    return `<li style="--c:${COLOURS[st.id]}"><span class="op-st__n">${esc(st.name)}</span><span class="op-st__v">${esc(txt)}</span><span class="op-st__w">${esc(st.what)}</span></li>`;
  }).join('\n');
  const sources = (r.sources || []).map(s => `<li><a href="${esc(s.url)}">${esc(s.url.replace(/^https?:\/\//, '').slice(0, 70))}</a>: ${esc(s.what)}</li>`).join('');
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Everything goes back to 1947</title>
<meta name="description" content="Oppenheimer's three strands on one calendar, ${m.first} to ${m.last}: two hearings ${m.hearingGap} years apart, and two scenes that reach back to one conversation in ${piv.from}. Unofficial fan page.">
<meta name="theme-color" content="#0B0D11">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${prefix}shared/site.css">
<style>
.op-cal{width:100%;height:auto;display:block}
.op-cal__tick,.op-cal__yr{fill:#8A93A0;font:500 13px "IBM Plex Sans",sans-serif}
.op-cal__name{fill:#F2EFE8;font:600 15px "IBM Plex Sans",sans-serif}
.op__fig{margin:2rem 0;overflow:hidden}
.op__fig figcaption,.op__note{color:#8A93A0;font-size:.95rem;line-height:1.5;max-width:62ch}
.op-big{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,13rem),1fr));gap:1rem;margin:2rem 0;padding:0;list-style:none}
.op-big li{border-top:2px solid #2A313B;padding-top:.6rem}
.op-big b{display:block;font:700 2.4rem/1 Archivo,sans-serif;color:#F2EFE8}
.op-big span{color:#8A93A0;font-size:.95rem}
.op-st,.op-evs{list-style:none;padding:0;margin:1rem 0}
.op-st li{display:grid;gap:.15rem;border-left:4px solid var(--c);padding:.4rem .8rem;margin:.6rem 0}
.op-st__n{font-weight:600}.op-st__v{font:600 1.2rem Archivo,sans-serif}.op-st__w,.op-ev__m{color:#8A93A0;font-size:.9rem}
.op-ev{display:grid;grid-template-columns:7.5rem 1fr;gap:.8rem;border-left:4px solid var(--c);padding:.5rem .8rem;margin:.5rem 0}
.op-ev p{margin:0}.op-ev__when{font:600 1rem Archivo,sans-serif}
.op-ev--pivot{background:#151A21}
@media (max-width:560px){.op-ev{grid-template-columns:1fr;gap:.2rem}.op-big b{font-size:2rem}}
</style>
</head>
<body>
<main class="site op">
  <header class="site__head">
    <p class="site__kicker"><a href="${prefix}">Christopher Nolan, film by film</a> · Oppenheimer (2023)</p>
    <h1 class="site__h1">Everything goes back to ${piv.from}.</h1>
    <p class="site__lede">Oppenheimer cuts between his life in colour, a ${m.byId.get('hearing54').from} hearing in colour, and a ${m.byId.get('hearing59').from} hearing in black and white. Put on one calendar, the dated story runs ${m.first} to ${m.last}, ${m.span} years in ${r.runtime_min} minutes. Two of its scenes reach back to the same conversation: Strauss accuses from ${claim.fromYear}, ${claim.years} years later, and the last flashback answers from ${reveal.fromYear}, ${reveal.years} years later.</p>
  </header>
  <ul class="op-big" aria-label="The numbers">
    <li><b>${m.span}</b><span>years of dated story, ${m.first} to ${m.last}</span></li>
    <li><b>${m.hearingGap}</b><span>years between the two hearings the film intercuts</span></li>
    <li><b>${claim.years}</b><span>years Strauss reaches back, from the Senate to Princeton</span></li>
    <li><b>${reveal.years}</b><span>years the final flashback reaches back to answer him</span></li>
  </ul>
  <figure class="op__fig">${calendar(r, m)}
    <figcaption>Real years left to right. Dots are events the plot dates to a year, the bar is a decade. The ringed dot is ${piv.from}, Einstein at Princeton. The dashed arc is Strauss's version of it, told to the Senate in ${claim.fromYear}; the solid arc is the flashback the film saves for the ${reveal.fromYear} award, which shows what was actually said.</figcaption>
  </figure>
  <section aria-label="The three strands">
    <h2 class="site__kicker">The three strands, by the calendar</h2>
    <ol class="op-st">
${strandRows}
    </ol>
    <p class="op__note">The 1954 and 1959 hearings are single years on this scale; the film's own committed page estimates each runs about a month and a few weeks. The life strand jumps forward to ${m.last} for the award, so it outlasts both hearings it is cut against.</p>
  </section>
  <section aria-label="Every dated event">
    <h2 class="site__kicker">Every event, in calendar order, with the line it comes from</h2>
    <ol class="op-evs">
${rows}
    </ol>
  </section>
  <section aria-label="Why two modes">
    <h2 class="site__kicker">Why colour and black and white</h2>
    ${cl('modes')}
    ${cl('first_person')}
    ${cl('ending')}
    <p class="op__note">${m.counts.year} of ${m.counts.events} events carry a year in the source, ${m.counts.decade} a decade, ${m.counts.none} none. Every year and quote here is from the fetched Wikipedia plot; nothing is filled in from memory. ${esc(r.not_yet)}</p>
  </section>
  <footer class="site__foot">
    <p>Researched ${esc(r.researched_on)} by Proteus, an AI explorer. <a href="${prefix}films/oppenheimer/">The Oppenheimer page</a> · <a href="${prefix}data/oppenheimer-calendar.json">the data</a>.</p>
    ${sources ? `<ul class="dk__src">${sources}</ul>` : ''}
    <p>Not affiliated with Christopher Nolan, Syncopy or Universal Pictures.</p>
  </footer>
</main>
</body>
</html>`;
}

module.exports = { renderOppenheimer, model };
