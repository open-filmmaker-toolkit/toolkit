// Several currencies. Any amount can carry its own currency (a `currency` field on
// its record); the project currency is the default. Exchange rates are typed in by
// hand, never fetched: project.exchangeRates, each { currency, rate, date? }, where
// rate is what one unit of that currency is worth in the project currency. A rate
// with a date applies from that date; one without a date applies to everything else.
const oftMoney = (() => {
  const up = s => String(s == null ? '' : s).trim().toUpperCase();
  const isDay = v => /^\d{4}-\d{2}-\d{2}$/.test(String(v || ''));
  const list = v => (Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []);
  const home = () => up(doc.project && doc.project.currency) || 'USD';
  const rates = () => list(doc.project && doc.project.exchangeRates).filter(r => /^[A-Z]{3}$/.test(up(r.currency)) && Number(r.rate) > 0);
  function rateFor(cur, date) {
    cur = up(cur);
    if (!cur || cur === home()) return { rate: 1 };
    const all = rates().filter(r => up(r.currency) === cur);
    const dated = all.filter(r => isDay(r.date)).sort((a, b) => a.date.localeCompare(b.date));
    const fixed = all.find(r => !isDay(r.date));
    const onDate = isDay(date) ? [...dated].reverse().find(r => r.date <= date) : null;
    const hit = onDate || fixed || dated[dated.length - 1];
    return hit ? { rate: Number(hit.rate), from: hit } : null;
  }
  // Converts an amount to the project currency. With no rate for its currency, the amount is counted as it is.
  function convert(amount, cur, date) { const r = rateFor(cur, date); return r ? Number(amount) * r.rate : Number(amount); }
  // A record's amount in the project currency, at the rate for its date.
  const amountOf = (r, field = 'amount', dateField = 'date') => (r.currency ? convert(Number(r[field]) || 0, r.currency, r[dateField]) : Number(r[field]) || 0);
  // Currencies other than the project's that money records use.
  function inUse() {
    const b = doc.budget || {}, f = doc.financePlan || {};
    const recs = [...list(b.lines), ...list(f.sources), ...list(doc.contracts), ...list(doc.expenses)];
    return [...new Set(recs.map(r => up(r.currency)).filter(c => c && c !== home()))].sort();
  }
  const show = n => Number(n).toLocaleString(undefined, { maximumFractionDigits: 6 });
  function note() {
    const cs = inUse();
    if (!cs.length) return '';
    const parts = cs.map(c => {
      const all = rates().filter(r => up(r.currency) === c), dated = all.filter(r => isDay(r.date)), fixed = all.find(r => !isDay(r.date));
      if (!all.length) return `there's no exchange rate for ${c} yet, so ${c} amounts are counted as ${home()}`;
      if (!dated.length) return `1 ${c} = ${show(fixed.rate)} ${home()}`;
      const last = dated.sort((a, b) => a.date.localeCompare(b.date))[dated.length - 1];
      return `${c} at the rate for each date (latest: 1 ${c} = ${show(last.rate)} ${home()} from ${last.date})${fixed ? `, otherwise 1 ${c} = ${show(fixed.rate)} ${home()}` : ''}`;
    });
    return `Totals are in ${home()}: ${parts.join('; ')}.`;
  }
  function fmt(n, cur) {
    try { return new Intl.NumberFormat(undefined, { style: 'currency', currency: up(cur) || home() }).format(Number(n)); }
    catch { return `${up(cur) || home()} ${Number(n).toLocaleString()}`; }
  }
  // The rates dialog, opened from "Exchange rates" under the file buttons.
  function rowHtml(r) {
    const e = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
    return `<div class="oft-rate"><input type="text" class="oft-rate-cur" maxlength="3" value="${e(r.currency)}" placeholder="EUR" aria-label="Currency" autocomplete="off">
      <input type="number" class="oft-rate-val" step="any" min="0" value="${e(r.rate)}" placeholder="Rate" aria-label="What 1 of it is worth in ${e(home())}">
      <input type="date" class="oft-rate-date" value="${e(r.date)}" aria-label="From this date (leave blank for one rate)">
      <button type="button" class="btn small" data-oft-del aria-label="Remove this rate">Remove</button></div>`;
  }
  function dialog() {
    let dlg = document.getElementById('oftRatesDialog');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'oftRatesDialog'; dlg.className = 'oft-dialog'; dlg.setAttribute('aria-labelledby', 'oftRatesTitle');
      dlg.innerHTML = `<form method="dialog" id="oftRatesForm"><h2 id="oftRatesTitle">Exchange rates</h2>
        <p id="oftRatesIntro"></p>
        <div id="oftRateRows" role="group" aria-label="Rates"></div>
        <p><button type="button" class="btn small" id="oftRateAdd">Add a rate</button></p>
        <p id="oftRatesErr" class="oft-unmatched" aria-live="polite"></p>
        <div class="oft-actions"><button type="button" class="btn" id="oftRatesCancel">Cancel</button><button type="submit" class="btn primary">Save rates</button></div></form>`;
      document.body.append(dlg);
      dlg.querySelector('#oftRateAdd').onclick = () => { dlg.querySelector('#oftRateRows').insertAdjacentHTML('beforeend', rowHtml({})); dlg.querySelector('#oftRateRows .oft-rate:last-child input').focus(); };
      dlg.querySelector('#oftRateRows').addEventListener('click', ev => { const b = ev.target.closest('[data-oft-del]'); if (b) b.closest('.oft-rate').remove(); });
      dlg.querySelector('#oftRatesCancel').onclick = () => dlg.close();
      dlg.querySelector('#oftRatesForm').addEventListener('submit', ev => {
        const out = [];
        for (const row of dlg.querySelectorAll('.oft-rate')) {
          const c = up(row.querySelector('.oft-rate-cur').value), v = row.querySelector('.oft-rate-val').value, d = row.querySelector('.oft-rate-date').value;
          if (!c && !v) continue;
          if (!/^[A-Z]{3}$/.test(c) || !(Number(v) > 0)) { ev.preventDefault(); dlg.querySelector('#oftRatesErr').textContent = 'Each rate needs a three-letter currency code, such as EUR, and a number above zero.'; return; }
          out.push(Object.assign({ currency: c, rate: Number(v) }, d ? { date: d } : {}));
        }
        if (out.length) doc.project.exchangeRates = out; else delete doc.project.exchangeRates;
        if (typeof changed === 'function') changed(); else { dirty = true; render(); }
      });
    }
    dlg.querySelector('#oftRatesIntro').textContent = `Type in what one unit of each currency is worth in ${home()}, the project currency. Nothing is looked up online. Add a date to use a rate from that date on, or leave it blank for one rate throughout.`;
    dlg.querySelector('#oftRatesErr').textContent = '';
    const rs = list(doc.project && doc.project.exchangeRates);
    dlg.querySelector('#oftRateRows').innerHTML = (rs.length ? rs : inUse().map(c => ({ currency: c }))).map(rowHtml).join('') || rowHtml({});
    dlg.showModal();
  }
  // A field for an amount's currency, for the tools' editors.
  function currencies() { return [...new Set([home(), ...rates().map(r => up(r.currency)), ...inUse()])]; }
  return { home, rateFor, convert, amountOf, inUse, note, fmt, dialog, currencies, up };
})();
// Shows which rates the totals use, under the file buttons and on the printed report.
const oftMoneyRender = render;
render = function () {
  const out = oftMoneyRender.apply(this, arguments);
  let p = document.getElementById('oftRatesNote');
  const text = oftMoney.note();
  if (!p && text) { p = document.createElement('p'); p.id = 'oftRatesNote'; p.className = 'oft-rates-note'; const main = document.querySelector('main#main') || document.querySelector('main'); if (main) main.prepend(p); }
  if (p) { p.textContent = text; p.hidden = !text; }
  return out;
};
if (typeof renderReport === 'function') {
  const oftMoneyReport = renderReport;
  renderReport = function () {
    const out = oftMoneyReport.apply(this, arguments);
    const r = document.getElementById('report'), text = oftMoney.note();
    if (r && text) { const p = document.createElement('p'); p.className = 'oft-rates-note'; p.textContent = text; r.append(p); }
    return out;
  };
}
