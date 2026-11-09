// Reminders shown when you open a tool: what's coming up or overdue. A tool lists them in
// OFT_REMINDERS = { records: () => [...], items: () => [{ id, key, text, when?, late? }], open: id => ..., what? },
// puts <section id="oftReminders" hidden></section> where they should show, and calls
// oftReminders.render() whenever it renders. Each reminder has a key that changes when its
// date does; dismissing one keeps its key in the record's dismissedReminders, so a reminder
// comes back if the date moves.
const oftReminders = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const R = () => (typeof OFT_REMINDERS !== 'undefined' ? OFT_REMINDERS : null);
  const rec = id => (R() ? R().records().find(r => r && r.id === id) : null);
  const dismissed = (r, key) => !!r && Array.isArray(r.dismissedReminders) && r.dismissedReminders.includes(key);
  function due() {
    if (!R()) return [];
    return R().items().filter(i => i && i.id && i.key && !dismissed(rec(i.id), i.key))
      .sort((a, b) => (b.late ? 1 : 0) - (a.late ? 1 : 0) || str(a.when).localeCompare(str(b.when)));
  }
  function dismiss(id, key) {
    const r = rec(id);
    if (!r) return;
    // Only the reminders still showing are kept, so the list doesn't grow forever.
    const live = new Set(R().items().filter(i => i.id === id).map(i => i.key));
    r.dismissedReminders = [...new Set([...(Array.isArray(r.dismissedReminders) ? r.dismissedReminders : []).filter(k => live.has(k)), key])];
    changed();
  }
  function render() {
    const box = document.getElementById('oftReminders');
    if (!box || !R()) return;
    const list = due();
    box.hidden = !list.length;
    if (!list.length) { box.innerHTML = ''; return; }
    box.innerHTML = `<div class="oft-rem-head"><h2 id="oftRemHead">Reminders</h2><span class="oft-rem-n">${list.length}</span></div>
      <ul class="oft-rem-list" aria-labelledby="oftRemHead">${list.map(i => `<li class="${i.late ? 'late' : ''}"><span class="oft-rem-text">${e(i.text)}</span>
        <span class="oft-rem-acts"><button type="button" class="btn small" data-rem-open="${e(i.id)}">Open</button><button type="button" class="btn small" data-rem-dismiss="${e(i.id)}" data-rem-key="${e(i.key)}" aria-label="Dismiss: ${e(i.text)}">Dismiss</button></span></li>`).join('')}</ul>
      <p class="oft-rem-note">${e(R().what || 'Reminders show here when you open this tool. Dismiss one and it comes back only if its date changes.')}</p>`;
  }
  document.addEventListener('click', ev => {
    const o = ev.target.closest('[data-rem-open]');
    if (o) { R().open(o.dataset.remOpen); return; }
    const d = ev.target.closest('[data-rem-dismiss]');
    if (d) { const box = document.getElementById('oftReminders'); dismiss(d.dataset.remDismiss, d.dataset.remKey); const next = box && box.querySelector('[data-rem-dismiss]'); if (next) next.focus(); }
  });
  const css = document.createElement('style');
  css.textContent = '#oftReminders { margin: 0 0 16px; padding: 12px 14px; border: 1px solid var(--rule); border-left: 4px solid var(--warn, #9a6700); border-radius: 8px; background: var(--sheet); }\n.oft-rem-head { display: flex; align-items: center; gap: 8px; }\n.oft-rem-head h2 { margin: 0; font-size: 16px; }\n.oft-rem-n { font-size: 13px; color: var(--ink-2); }\n.oft-rem-list { list-style: none; margin: 8px 0 0; padding: 0; display: grid; gap: 6px; }\n.oft-rem-list li { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; font-size: 14px; }\n.oft-rem-list li.late .oft-rem-text { font-weight: 600; }\n.oft-rem-text { flex: 1 1 240px; min-width: 0; overflow-wrap: anywhere; }\n.oft-rem-acts { display: flex; gap: 6px; }\n.oft-rem-note { margin: 8px 0 0; font-size: 13px; color: var(--ink-2); }\n@media print { #oftReminders { display: none !important; } }';
  document.head.append(css);
  return { render, due, dismiss };
})();
