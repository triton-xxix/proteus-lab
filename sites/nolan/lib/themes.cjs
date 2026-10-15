'use strict';
// The themes page: one section per theme in themes.json, the films it runs through in year order,
// each with the scene the research child wrote and whether that scene carries a source.
// Everything is drawn from films/<slug>.json; nothing is typed here.
const { esc } = require('./render.cjs');

function renderThemes(films, themes, data, rel) {
  const sorted = films.films.slice().sort((a, b) => a.year - b.year);
  const live = sorted.filter(f => data[f.slug]);
  const known = new Set(themes.themes.map(t => t.id));
  let sourced = 0, unverified = 0;
  const sections = themes.themes.map(t => {
    const hits = live.map(f => ({ f, th: (data[f.slug].themes || []).find(x => x.id === t.id) })).filter(h => h.th);
    return { t, hits };
  });
  for (const s of sections) for (const h of s.hits) (h.th.source ? sourced++ : unverified++);
  const seen = sections.filter(s => s.hits.length).sort((a, b) => b.hits.length - a.hits.length || a.hits[0].f.year - b.hits[0].f.year);
  const unseen = sections.filter(s => !s.hits.length);
  const proposed = [];
  for (const f of live) for (const x of data[f.slug].themes || []) if (!known.has(x.id)) proposed.push({ f, x });
  const top = seen[0];

  const strand = s => `<div class="th-strand" aria-hidden="true">${sorted.map(f => {
    const on = s.hits.some(h => h.f.slug === f.slug);
    const cls = on ? 'th-strand__dot th-strand__dot--on' : (data[f.slug] ? 'th-strand__dot th-strand__dot--live' : 'th-strand__dot');
    return `<span class="th-strand__cell"><span class="${cls}"></span><span class="th-strand__yr">${String(f.year).slice(2)}</span></span>`;
  }).join('')}</div>`;

  const card = h => `<li class="th-card">
        <p class="th-card__meta"><span class="th-card__year">${h.f.year}</span> <a href="${rel}films/${h.f.slug}/#theme-${h.th.id}">${esc(h.f.title)}</a></p>
        <p class="th-card__scene">${esc(h.th.scene || '')}</p>
        <p class="th-card__src">${h.th.source ? `<a href="${esc(h.th.source)}" rel="noopener">source</a>` : `<span class="th-card__flag">reading, no source</span>`}</p>
      </li>`;

  const section = s => `<section class="th" id="${s.t.id}">
    <header class="th__head">
      <h2 class="th__name">${esc(s.t.name)}</h2>
      <p class="th__count">${s.hits.length} of ${live.length} films</p>
    </header>
    <p class="th__line">${esc(s.t.line)}</p>
    ${strand(s)}
    <ol class="th-cards">
      ${s.hits.map(card).join('\n      ')}
    </ol>
  </section>`;

  const nav = seen.map(s => `<a class="th-nav__a" href="#${s.t.id}">${esc(s.t.name)} <span>${s.hits.length}</span></a>`).join('');

  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Nolan's themes, film by film</title>
<meta name="description" content="Fifteen themes traced through Christopher Nolan's films, one scene per film, with which readings carry a source.">
<meta name="theme-color" content="#0B0D11">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230B0D11'/><rect x='4' y='4' width='12' height='24' fill='%23C8463A'/><rect x='16' y='4' width='12' height='24' fill='%233C9AB4'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${rel}shared/site.css">
<link rel="stylesheet" href="${rel}shared/film.css">
<link rel="stylesheet" href="${rel}shared/themes.css">
</head>
<body>
<main class="site">
  <header class="site__head">
    <p class="site__kicker"><a href="${rel}">Christopher Nolan, film by film</a> / Themes</p>
    <h1 class="site__h1">The threads that keep coming back.</h1>
    <p class="site__lede">${themes.themes.length} themes, traced through the ${live.length} films researched so far, one scene per film. ${top ? `${esc(top.t.name)} runs through the most: ${top.hits.length} of ${live.length}.` : ''} Of ${sourced + unverified} readings, ${sourced} cite a source and ${unverified} are the researcher's own reading of the film, marked as such.</p>
  </header>
  <nav class="th-nav" aria-label="Themes">${nav}</nav>
  ${seen.map(section).join('\n  ')}
  ${unseen.length ? `<section class="th th--quiet"><h2 class="site__kicker">Not found yet in the films researched</h2><p class="th__line">${unseen.map(s => esc(s.t.name)).join(', ')}. These fill in as the remaining ${films.films.length - live.length} films land.</p></section>` : ''}
  ${proposed.length ? `<section class="th th--quiet"><h2 class="site__kicker">Proposed, not yet in the vocabulary</h2><p class="th__line">${proposed.map(p => `${esc(p.x.name || p.x.id)} (${esc(p.f.title)})`).join(', ')}.</p></section>` : ''}
  <footer class="site__foot">
    <p>Each scene is written by Proteus's research step from the sources on that film's page. A reading without a source is an interpretation, not a quoted claim. The vocabulary is fixed in <a href="https://github.com/triton-xxix/proteus-lab/blob/main/sites/nolan/themes.json">themes.json</a> so the same idea gets the same name across films.</p>
    <p>Not affiliated with Christopher Nolan, Syncopy or Warner Bros.</p>
  </footer>
</main>
</body>
</html>`;
}

module.exports = { renderThemes };
