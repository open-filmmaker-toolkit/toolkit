// A month grid for tools with dates. oftMonth.render(box, items, { pick }) draws the month kept on the box,
// with buttons to move between months. Each item is { date: 'YYYY-MM-DD', label, title, cls, attrs }, where
// attrs is an attribute string such as data-edit="id" that the tool's own click handler already knows.
// On a phone the grid becomes a list of the days that have something on them.
const oftMonth = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const iso = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const isDay = s => /^\d{4}-\d{2}-\d{2}$/.test(str(s));
  function style() {
    if (document.getElementById('oftMonthCss')) return;
    const css = document.createElement('style');
    css.id = 'oftMonthCss';
    css.textContent = `.oft-cal { background: var(--sheet); border: 1px solid var(--rule); border-radius: 8px; padding: 10px; }
.oft-cal-head { display: flex; align-items: center; gap: 8px; margin: 0 0 8px; }
.oft-cal-head h3 { margin: 0; flex: 1; font-size: 18px; line-height: 1.2; }
.oft-cal-grid { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 2px; margin: 0; padding: 0; list-style: none; }
.oft-cal-dow { font-size: 12px; color: var(--ink-2); text-align: center; padding: 2px 0; }
.oft-cal-day { min-height: 78px; padding: 4px; border: 1px solid var(--rule-soft, var(--rule)); border-radius: 4px; min-width: 0; }
.oft-cal-day.out { background: var(--paper); }
.oft-cal-day.out .d { font-style: italic; }
.oft-cal-day.today { box-shadow: inset 0 0 0 2px var(--ink); }
.oft-cal-day .d { display: block; font-size: 12px; color: var(--ink-2); font-variant-numeric: tabular-nums; }
.oft-cal-day .d .long { display: none; }
.oft-cal-day ul { margin: 0; padding: 0; list-style: none; }
.oft-cal-day li > * { display: block; width: 100%; margin-top: 3px; padding: 2px 4px; border: 0; border-radius: 3px; background: var(--hover); color: var(--ink); font: inherit; font-size: 12px; text-align: left; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.oft-cal-day li > button { cursor: pointer; }
.oft-cal-none { margin: 8px 0 0; font-size: 13px; color: var(--ink-2); }
@media (max-width: 560px) {
  .oft-cal-grid { grid-template-columns: 1fr; gap: 6px; }
  .oft-cal-dow, .oft-cal-day.empty, .oft-cal-day.out { display: none; }
  .oft-cal-day { min-height: 0; }
  .oft-cal-day .d .short { display: none; }
  .oft-cal-day .d .long { display: inline; font-weight: 600; color: var(--ink); }
  .oft-cal-day li > * { white-space: normal; font-size: 14px; }
}`;
    document.head.append(css);
  }
  function render(box, items, opts = {}) {
    style();
    const dated = items.filter(i => isDay(i.date)).sort((a, b) => a.date.localeCompare(b.date));
    const t = new Date(), today = iso(t);
    if (!/^\d{4}-\d{2}$/.test(box.dataset.month || '')) {
      const next = dated.find(i => i.date >= today) || dated[dated.length - 1];
      box.dataset.month = next ? next.date.slice(0, 7) : today.slice(0, 7);
    }
    const [y, m] = box.dataset.month.split('-').map(Number);
    const first = new Date(y, m - 1, 1), start = new Date(y, m - 1, 1 - first.getDay());
    const weeks = Math.ceil((first.getDay() + new Date(y, m, 0).getDate()) / 7);
    const dow = [...Array(7)].map((_, i) => new Date(2024, 0, 7 + i).toLocaleDateString(undefined, { weekday: 'short' }));
    let cells = '';
    for (let i = 0; i < weeks * 7; i++) {
      const d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i), key = iso(d), here = dated.filter(x => x.date === key);
      const long = d.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });
      cells += `<li class="oft-cal-day${d.getMonth() !== m - 1 ? ' out' : ''}${key === today ? ' today' : ''}${here.length ? '' : ' empty'}" aria-label="${e(long)}${here.length ? `, ${here.length} thing${here.length === 1 ? '' : 's'}` : ''}">
        <span class="d" aria-hidden="true"><span class="short">${d.getDate()}</span><span class="long">${e(long)}</span></span>${here.length ? `<ul>${here.map(x => `<li>${x.attrs ? `<button type="button" ${x.attrs} class="${e(x.cls || '')}" title="${e(x.title || x.label)}">` : `<span class="${e(x.cls || '')}" title="${e(x.title || x.label)}">`}${e(x.label)}${x.attrs ? '</button>' : '</span>'}</li>`).join('')}</ul>` : ''}</li>`;
    }
    const inMonth = dated.filter(x => x.date.slice(0, 7) === box.dataset.month).length;
    const name = first.toLocaleDateString(undefined, { month: 'long', year: 'numeric' });
    box.classList.add('oft-cal');
    box.innerHTML = `<div class="oft-cal-head"><button type="button" class="btn small" data-month="-1" aria-label="Previous month">&#8249;</button><h3 aria-live="polite">${e(name)}</h3>
      <button type="button" class="btn small" data-month="0">Today</button><button type="button" class="btn small" data-month="1" aria-label="Next month">&#8250;</button></div>
      <div class="oft-cal-grid" aria-hidden="true">${dow.map(d => `<div class="oft-cal-dow">${e(d)}</div>`).join('')}</div>
      <ol class="oft-cal-grid" aria-label="${e(name)}">${cells}</ol>
      ${inMonth ? '' : `<p class="oft-cal-none">Nothing in ${e(name)}.${dated.length ? ' Use the arrows to see other months.' : ''}</p>`}${opts.note ? `<p class="oft-cal-none">${e(opts.note)}</p>` : ''}`;
    // The day names sit above the days; on a phone, where the grid is a list, they're hidden.
    const [dowRow, days] = box.querySelectorAll('.oft-cal-grid');
    dowRow.style.marginBottom = '2px';
    days.style.marginTop = '0';
    box.querySelectorAll('[data-month]').forEach(b => b.addEventListener('click', () => {
      const n = Number(b.dataset.month);
      const d = n ? new Date(y, m - 1 + n, 1) : new Date();
      box.dataset.month = iso(d).slice(0, 7);
      render(box, items, opts);
      box.querySelector(`[data-month="${b.dataset.month}"]`).focus();
    }));
  }
  return { render };
})();
