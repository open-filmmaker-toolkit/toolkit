// Editing and removing a screening. Screenings are shared: the press list and the partner CRM
// both add them, partners link to them (screeningIds) and press RSVPs name one (screeningId).
// Editing keeps every field the dialog doesn't show. Removing one also removes the links to it,
// after saying what they are.
const oftScreenings = (() => {
  const str = v => (v == null ? '' : String(v));
  const list = v => (Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []);
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const css = document.createElement('style');
  css.textContent = '.scr-edit { display: inline-block; min-height: 24px; min-width: 24px; margin-top: 2px; }\n.oft-dialog input[type="date"] { padding: 8px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--sheet); color: var(--ink); font: inherit; }\n.oft-dialog .oft-warn { padding: 10px 12px; border-left: 4px solid var(--bad); background: var(--bad-bg, transparent); }\n.oft-dialog .oft-actions .oft-left { margin-right: auto; }';
  document.head.append(css);
  const all = () => list(doc.screenings).filter(s => s.id);
  const sorted = () => all().sort((a, b) => str(a.date || '9999').localeCompare(str(b.date || '9999')));
  // What refers to a screening: partners that link to it and press outlets with an RSVP for it.
  function refs(id) {
    const partners = list(doc.partners).filter(p => Array.isArray(p.screeningIds) && p.screeningIds.includes(id));
    const rsvps = [];
    for (const o of list(doc.pressOutlets)) for (const r of list(o.rsvps)) if (r.screeningId === id) rsvps.push({ outlet: o, rsvp: r });
    return { partners, rsvps };
  }
  function describe(id) {
    const { partners, rsvps } = refs(id);
    const bits = [];
    if (partners.length) bits.push(`${partners.length} partner${partners.length === 1 ? '' : 's'} link to it (${partners.map(p => p.name || 'unnamed partner').join(', ')})`);
    if (rsvps.length) bits.push(`${rsvps.length} press RSVP${rsvps.length === 1 ? '' : 's'} name it`);
    return bits;
  }
  function remove(id) {
    doc.screenings = list(doc.screenings).filter(s => s.id !== id).concat((Array.isArray(doc.screenings) ? doc.screenings : []).filter(s => !s || typeof s !== 'object'));
    for (const p of list(doc.partners)) if (Array.isArray(p.screeningIds) && p.screeningIds.includes(id)) {
      p.screeningIds = p.screeningIds.filter(x => x !== id);
      if (!p.screeningIds.length) delete p.screeningIds;
    }
    for (const o of list(doc.pressOutlets)) if (Array.isArray(o.rsvps) && o.rsvps.some(r => r && r.screeningId === id)) {
      o.rsvps = o.rsvps.filter(r => !r || r.screeningId !== id);
      if (!o.rsvps.length) delete o.rsvps;
    }
  }
  function dialog() {
    let dlg = document.getElementById('oftScreeningDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog'; dlg.id = 'oftScreeningDialog'; dlg.setAttribute('aria-labelledby', 'oftScreeningTitle');
    dlg.innerHTML = `<form method="dialog" id="oftScreeningForm"><h2 id="oftScreeningTitle">Edit screening</h2>
  <label class="oft-field" for="oftScrTitle">Screening</label><input type="text" id="oftScrTitle" required autocomplete="off">
  <label class="oft-field" for="oftScrDate">Date</label><input type="date" id="oftScrDate">
  <label class="oft-field" for="oftScrPlace">Venue or city</label><input type="text" id="oftScrPlace" autocomplete="off">
  <div id="oftScrConfirm" hidden><p class="oft-warn" id="oftScrWarn" role="alert"></p></div>
  <div class="oft-actions"><button type="button" class="btn oft-left" id="oftScrRemove">Remove screening</button><button type="button" class="btn" id="oftScrCancel">Cancel</button><button type="submit" class="btn primary" id="oftScrSave">Save screening</button></div></form>`;
    document.body.append(dlg);
    dlg.querySelector('#oftScrCancel').onclick = () => dlg.close();
    return dlg;
  }
  // Opens the editor for a saved screening; onDone(message) runs after a change.
  function edit(id, onDone) {
    const s = all().find(x => x.id === id);
    if (!s) return;
    const dlg = dialog();
    const $ = q => dlg.querySelector(q);
    $('#oftScrTitle').value = str(s.title || s.name);
    $('#oftScrDate').value = /^\d{4}-\d{2}-\d{2}$/.test(str(s.date)) ? s.date : '';
    $('#oftScrPlace').value = str(s.place);
    $('#oftScrConfirm').hidden = true;
    const rm = $('#oftScrRemove');
    rm.textContent = 'Remove screening';
    rm.onclick = () => {
      const bits = describe(id);
      if ($('#oftScrConfirm').hidden) {
        $('#oftScrWarn').textContent = bits.length
          ? `${bits.join(', and ')}. Removing the screening also removes ${bits.length > 1 ? 'those links' : 'that link'}. Click "Remove anyway" to go ahead.`
          : 'Nothing else in the project refers to this screening. Click "Remove anyway" to go ahead.';
        $('#oftScrConfirm').hidden = false;
        rm.textContent = 'Remove anyway';
        return;
      }
      remove(id);
      dlg.close();
      onDone(`Removed ${s.title || 'the screening'}.`);
    };
    $('#oftScreeningForm').onsubmit = ev => {
      ev.preventDefault();
      const title = $('#oftScrTitle').value.trim();
      if (!title) { $('#oftScrTitle').reportValidity(); return; }
      s.title = title;
      for (const [k, q] of [['date', '#oftScrDate'], ['place', '#oftScrPlace']]) { const v = $(q).value.trim(); if (v) s[k] = v; else delete s[k]; }
      dlg.close();
      onDone(`Saved ${title}.`);
    };
    dlg.showModal();
    $('#oftScrTitle').focus();
  }
  // A list of screenings with an Edit button for each, for a tool's side panel.
  function listHtml(fmt, extra) {
    const scr = sorted();
    return scr.length ? scr.map(s => `<li><span></span><span>${e(s.title || 'Untitled screening')}<span class="when">${e([s.date && fmt(s.date), s.place].filter(Boolean).join(' · '))}${extra ? e(extra(s)) : ''}</span><button type="button" class="link-btn scr-edit" data-edit-screening="${e(s.id)}" aria-label="Edit ${e(s.title || 'screening')}">Edit</button></span></li>`).join('') : '';
  }
  return { all, sorted, refs, describe, remove, edit, listHtml };
})();
