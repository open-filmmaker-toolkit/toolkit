// Links from a record in one tool to records another tool keeps: a trip, a shoot day, an interview,
// clips, subjects, a card on the structure board, a screening, gear or a source in the research log. A tool lists its links in
// OFT_LINKS, as [{ key, label, from, many?, hint? }], puts <div id="oftLinks"></div> in its editor,
// and calls oftLinks.fill(record) when the editor opens, oftLinks.save(record) when it saves, and
// oftLinks.labels(record) for what to show in the list.
const oftLinks = (() => {
  const str = v => (v == null ? '' : String(v));
  const list = v => (Array.isArray(v) ? v.filter(x => x && typeof x === 'object' && x.id) : []);
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const day = iso => { const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(str(iso)); return m ? new Date(+m[1], +m[2] - 1, +m[3]).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' }) : ''; };
  const person = id => list(doc.people).find(p => p.id === id);
  const SOURCES = {
    trips: () => list(doc.trips).map(t => ({ id: t.id, label: [t.name || 'Untitled trip', day(t.startDate)].filter(Boolean).join(', ') })),
    shootDays: () => list(doc.shootDays).slice().sort((a, b) => str(a.date).localeCompare(str(b.date))).map(d => ({ id: d.id, label: [day(d.date), d.title || (d.kind === 'travel' ? 'Travel day' : d.kind === 'hold' ? 'Hold' : 'Shoot day')].filter(Boolean).join(': ') })),
    interviews: () => list(doc.interviews).map(i => ({ id: i.id, label: [(person(i.personId) || {}).name || 'Interview', day(i.date || (list(doc.shootDays).find(d => d.id === i.shootDayId) || {}).date)].filter(Boolean).join(', ') })),
    clips: () => list(doc.assets).filter(a => a.type === 'clip').map(a => ({ id: a.id, label: a.title || a.name || str(a.relativePath).split('/').pop() || 'Clip' })),
    subjects: () => list(doc.subjects).map(s => ({ id: s.id, label: s.name || (person(s.personId) || {}).name || 'Unnamed subject' })),
    locations: () => list(doc.locations).map(l => ({ id: l.id, label: l.name || 'Unnamed location' })),
    cards: () => list(doc.structure && doc.structure.cards).map(c => ({ id: c.id, label: c.title || 'Untitled card' })),
    screenings: () => list(doc.screenings).slice().sort((a, b) => str(a.date).localeCompare(str(b.date))).map(s => ({ id: s.id, label: [s.title || 'Untitled screening', day(s.date)].filter(Boolean).join(', ') })),
    sources: () => list(doc.sources).map(s => ({ id: s.id, label: s.title || 'Untitled source' })),
    gear: () => list(doc.gear && doc.gear.items).map(g => ({ id: g.id, label: [g.name || 'Unnamed item', g.serial && `serial ${g.serial}`].filter(Boolean).join(', ') })),
  };
  const specs = () => (typeof OFT_LINKS !== 'undefined' ? OFT_LINKS : []);
  const fid = s => `oftLink-${s.key}`;
  function fill(rec) {
    const box = document.getElementById('oftLinks');
    if (!box) return;
    box.innerHTML = specs().map(s => {
      const opts = SOURCES[s.from]();
      const have = s.many ? (Array.isArray(rec[s.key]) ? rec[s.key] : []) : [rec[s.key]].filter(Boolean);
      // A link to something no longer in the project stays, so nothing is lost.
      const gone = have.filter(id => !opts.some(o => o.id === id)).map(id => ({ id, label: 'No longer in the project' }));
      const all = [...opts, ...gone];
      if (s.many) return `<fieldset class="oft-link-checks"><legend>${e(s.label)}</legend>${all.length ? all.map(o => `<label><input type="checkbox" name="${fid(s)}" value="${e(o.id)}"${have.includes(o.id) ? ' checked' : ''}> ${e(o.label)}</label>`).join('') : `<p class="oft-link-none">${e(s.none || 'None in the project yet.')}</p>`}${s.hint ? `<p class="oft-link-none">${e(s.hint)}</p>` : ''}</fieldset>`;
      return `<div class="oft-link-one"><label for="${fid(s)}">${e(s.label)}</label><select id="${fid(s)}"><option value="">None</option>${all.map(o => `<option value="${e(o.id)}"${have[0] === o.id ? ' selected' : ''}>${e(o.label)}</option>`).join('')}</select>${s.hint ? `<p class="oft-link-none">${e(s.hint)}</p>` : ''}</div>`;
    }).join('');
  }
  function save(rec) {
    if (!document.getElementById('oftLinks')) return;
    for (const s of specs()) {
      if (s.many) { const v = [...document.querySelectorAll(`input[name="${fid(s)}"]:checked`)].map(x => x.value); if (v.length) rec[s.key] = v; else delete rec[s.key]; }
      else { const el = document.getElementById(fid(s)); if (!el) continue; if (el.value) rec[s.key] = el.value; else delete rec[s.key]; }
    }
  }
  // What a record links to, for its row: "Trip: Spring flood trip".
  function labels(rec, short) {
    const out = [];
    for (const s of specs()) {
      const ids = s.many ? (Array.isArray(rec[s.key]) ? rec[s.key] : []) : [rec[s.key]].filter(Boolean);
      if (!ids.length) continue;
      const opts = SOURCES[s.from]();
      const names = ids.map(id => (opts.find(o => o.id === id) || { label: 'missing' }).label);
      out.push(`${s.short || s.label}: ${names.length > 3 && !short ? `${names.slice(0, 3).join(', ')} and ${names.length - 3} more` : names.join(', ')}`);
    }
    return out;
  }
  const css = document.createElement('style');
  css.textContent = '#oftLinks { display: grid; gap: 12px; }\n#oftLinks:empty { display: none; }\n.oft-link-one { display: grid; gap: 4px; }\n.oft-link-one label, .oft-link-checks legend { font-size: 14px; font-weight: 600; }\n.oft-link-one select { width: 100%; padding: 8px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--paper); color: var(--ink); font: inherit; }\n.oft-link-checks { border: 0; margin: 0; padding: 0; min-width: 0; display: grid; gap: 2px; max-height: 200px; overflow-y: auto; }\n.oft-link-checks legend { padding: 0; margin-bottom: 4px; }\n.oft-link-checks label { display: flex; gap: 8px; align-items: center; font-size: 14px; min-height: 24px; }\n.oft-link-none { margin: 0; font-size: 13px; color: var(--ink-2); }';
  document.head.append(css);
  return { fill, save, labels, SOURCES };
})();
