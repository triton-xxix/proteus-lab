// A standard film page from films/<slug>.json (the checked digest a research child wrote).
'use strict';
const fs = require('fs');
const path = require('path');
const { ROOT, esc, readJSON, jpegSize } = require('./render.cjs');
const { diagram } = require('./structure.cjs');

function money(n) {
  if (n == null || isNaN(n)) return 'unverified';
  if (n >= 1e9) return '$' + (n / 1e9).toFixed(2).replace(/\.?0+$/, '') + ' billion';
  if (n >= 1e6) return '$' + Math.round(n / 1e6) + ' million';
  return '$' + Number(n).toLocaleString('en-GB');
}

function cell(label, f, fmt) {
  if (!f) return `<div class="fact fact--missing"><span class="fact__l">${esc(label)}</span><span class="fact__v">unverified</span></div>`;
  const v = fmt ? fmt(f.value) : (Array.isArray(f.value) ? f.value.join(', ') : f.value);
  const src = f.source && String(f.source).startsWith('http') ? ` <a class="fact__src" href="${esc(f.source)}" rel="noopener" aria-label="Source for ${esc(label)}">source</a>` : '';
  return `<div class="fact${f.unverified ? ' fact--unverified' : ''}"><span class="fact__l">${esc(label)}</span><span class="fact__v">${esc(v)}${f.note ? ` <em>(${esc(f.note)})</em>` : ''}${f.unverified ? ' <em>unverified</em>' : ''}</span>${src}</div>`;
}

function src(s) {
  return s && String(s).startsWith('http') ? ` <a class="src" href="${esc(s)}" rel="noopener">source</a>` : '';
}

function renderFilm(d, reg, base, neighbours) {
  const f = d.facts || {};
  const themes = readJSON('themes.json').themes;
  const tname = id => (themes.find(t => t.id === id) || {}).name || id;
  const imgs = (d.images || []).filter(i => i.local).map(i => {
    const sz = jpegSize(path.join(ROOT, d.slug, 'img', i.local + '-800.jpg')) || { w: 800, h: 450 };
    return `<figure class="still"><img src="${base}../${d.slug}/img/${i.local}-800.jpg" srcset="${base}../${d.slug}/img/${i.local}-800.jpg 800w, ${base}../${d.slug}/img/${i.local}.jpg 1600w" sizes="(max-width: 860px) 100vw, 50vw" width="${sz.w}" height="${sz.h}" alt="${esc(i.caption)}" loading="lazy"><figcaption>${esc(i.caption)}${src(i.source)}</figcaption></figure>`;
  }).join('');
  const prev = neighbours.prev, next = neighbours.next;
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(d.title)} (${d.year}): how it plays with time</title>
<meta name="description" content="${esc(d.one_line || '')}">
<meta name="theme-color" content="#0B0D11">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230B0D11'/><rect x='4' y='4' width='12' height='24' fill='%23C8463A'/><rect x='16' y='4' width='12' height='24' fill='%233C9AB4'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${base}../shared/site.css">
<link rel="stylesheet" href="${base}../shared/film.css">
</head>
<body>
<main class="film-page">
  <nav class="film-nav"><a href="${base}../">All films</a>${prev ? ` · <a href="${base}../films/${prev.slug}/">${esc(prev.title)}</a>` : ''}${next ? ` · <a href="${base}../films/${next.slug}/">${esc(next.title)}</a>` : ''}</nav>
  <header class="film-head">
    <p class="site__kicker">${d.year}${reg && reg.deep_page ? ' · deep timeline available' : ''}</p>
    <h1 class="site__h1">${esc(d.title)}</h1>
    <p class="site__lede">${esc(d.one_line || '')}</p>
    ${reg && reg.deep_page ? `<p class="film-deep"><a href="${base}../${reg.deep_page}">Walk the full timeline</a></p>` : ''}
  </header>
  <section class="facts" aria-label="Facts">
    ${cell('Released', f.release)}${cell('Runtime', f.runtime_min, v => v + ' min')}${cell('Written by', f.writers)}${cell('Cinematography', f.dp)}${cell('Editor', f.editor)}${cell('Music', f.composer)}${cell('Budget', f.budget_usd, money)}${cell('Gross', f.gross_usd, money)}
  </section>
  <section class="block">
    <h2 class="block__h">How it plays with time</h2>
    <p class="block__p">${esc((d.time_structure || {}).summary || '')}${src((d.time_structure || {}).source)}</p>
    ${diagram((d.time_structure || {}).sketch)}
  </section>
  <section class="block">
    <h2 class="block__h">Themes</h2>
    <dl class="themes">${(d.themes || []).map(t => `<div class="theme" id="theme-${esc(t.id)}"><dt>${esc(t.name || tname(t.id))}</dt><dd>${esc(t.scene)}${src(t.source)}</dd></div>`).join('')}</dl>
  </section>
  <section class="block">
    <h2 class="block__h">Where it came from</h2>
    <ul class="list">${(d.inspirations || []).map(i => `<li>${esc(i.claim)}${i.who ? ` <span class="who">${esc(i.who)}</span>` : ''}${i.quote ? ` <q>${esc(i.quote)}</q>` : ''}${src(i.source)}${i.unverified ? ' <em>unverified</em>' : ''}</li>`).join('')}</ul>
  </section>
  ${imgs ? `<section class="block"><h2 class="block__h">Stills</h2><div class="stills">${imgs}</div><p class="credit">Stills © their studios, used here for commentary and criticism.</p></section>` : ''}
  <section class="block block--two">
    <div>
      <h2 class="block__h">People who keep coming back</h2>
      <ul class="list">${(d.collaborators || []).map(c => `<li><b>${esc(c.name)}</b>, ${esc(c.role)}${c.also && c.also.length ? `: also ${c.also.map(s => `<a href="${base}../films/${esc(s)}/">${esc(s.replace(/-/g, ' '))}</a>`).join(', ')}` : ''}</li>`).join('')}</ul>
    </div>
    <div>
      <h2 class="block__h">How it was received</h2>
      ${(() => { const r = d.reception || {}; const a = r.at_release || {}; const n = r.now || {}; return `<p class="block__p">${esc(a.summary || '')}${a.metacritic && a.metacritic.value ? ` Metacritic ${esc(a.metacritic.value)}${src(a.metacritic.source)}.` : ''}${a.rt && a.rt.value ? ` Rotten Tomatoes ${esc(a.rt.value)}%${src(a.rt.source)}.` : ''}</p><p class="block__p">${esc(n.summary || '')}${n.letterboxd && n.letterboxd.value ? ` Letterboxd ${esc(n.letterboxd.value)} as of ${esc(n.letterboxd.as_of || '')}${src(n.letterboxd.source)}.` : ''}</p>`; })()}
    </div>
  </section>
  <section class="block">
    <h2 class="block__h">Three things most people miss</h2>
    <ol class="list list--num">${(d.missed || []).map(m => `<li>${esc(m.point)}${src(m.source)}</li>`).join('')}</ol>
  </section>
  <section class="block">
    <h2 class="block__h">Cast</h2>
    <p class="block__p">${((f.cast_top5 || {}).value || []).map(c => `${esc(c.name)} as ${esc(c.role)}`).join('; ')}.</p>
  </section>
  <footer class="block block--foot">
    <h2 class="block__h">Sources</h2>
    <ol class="list list--src">${(d.sources || []).map(s => `<li><a href="${esc(s.url)}" rel="noopener">${esc(s.title || s.url)}</a>${s.fetched ? '' : ' <em>not fetched, cited only</em>'}</li>`).join('')}</ol>
    <p class="credit">Researched ${esc(d.researched_on || '')} from the pages above by Proteus, an AI explorer, for an unofficial fan site. Not affiliated with Christopher Nolan, Syncopy or any studio. The data for this page is at <a href="${base}../data/${esc(d.slug)}.json">data/${esc(d.slug)}.json</a>.</p>
  </footer>
</main>
</body>
</html>`;
}

module.exports = { renderFilm };
