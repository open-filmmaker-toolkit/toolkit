// Bar charts drawn with the page's own HTML and CSS, so they scale to any width, print, follow dark mode
// and need no library. oftChart.bars({ title, rows: [{ label, value, target, text }], note }) returns HTML: a
// figure with the bars, which screen readers skip, and a table of the same numbers, which everyone can read.
const oftChart = (() => {
  const str = v => (v == null ? '' : String(v));
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const num = n => (Number.isFinite(Number(n)) ? Number(n).toLocaleString() : '');
  function style() {
    if (document.getElementById('oftChartCss')) return;
    const css = document.createElement('style');
    css.id = 'oftChartCss';
    css.textContent = `.oft-chart { margin: 0 0 14px; padding: 10px 12px; border: 1px solid var(--rule); border-radius: 8px; background: var(--sheet); }
.oft-chart figcaption { margin: 0 0 8px; font-weight: 600; }
.oft-chart-bars { display: grid; gap: 6px; margin: 0 0 8px; }
.oft-chart-row { display: grid; grid-template-columns: minmax(90px, 30%) minmax(0, 1fr) auto; gap: 8px; align-items: center; font-size: 13px; }
.oft-chart-row .l { overflow-wrap: anywhere; }
.oft-chart-row .t { position: relative; height: 14px; border-radius: 3px; background: var(--hover); }
.oft-chart-row .f { position: absolute; inset: 0 auto 0 0; border-radius: 3px; background: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.oft-chart-row .f.met { background: var(--good, var(--ink)); }
.oft-chart-row .m { position: absolute; top: -3px; bottom: -3px; width: 2px; background: var(--warn, #b25d00); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.oft-chart-row .v { font-variant-numeric: tabular-nums; white-space: nowrap; }
.oft-chart table { width: 100%; border-collapse: collapse; font-size: 13px; }
.oft-chart th, .oft-chart td { padding: 3px 6px; border-top: 1px solid var(--rule); text-align: left; }
.oft-chart td.n, .oft-chart th.n { text-align: right; font-variant-numeric: tabular-nums; }
.oft-chart .note { margin: 6px 0 0; font-size: 12px; color: var(--ink-2); }
@media (max-width: 560px) { .oft-chart-row { grid-template-columns: 1fr auto; } .oft-chart-row .t { grid-column: 1 / -1; grid-row: 2; } }`;
    document.head.append(css);
  }
  function bars({ title, rows, note, valueLabel = 'Value', targetLabel = 'Target' }) {
    style();
    const list = rows.filter(r => Number.isFinite(Number(r.value)));
    if (!list.length) return '';
    const max = Math.max(1, ...list.map(r => Math.max(Number(r.value), Number.isFinite(Number(r.target)) ? Number(r.target) : 0)));
    const hasTarget = list.some(r => Number.isFinite(Number(r.target)));
    const pct = v => `${Math.max(0, Math.min(100, Number(v) / max * 100)).toFixed(2)}%`;
    const shown = r => r.text != null ? r.text : num(r.value);
    return `<figure class="oft-chart"><figcaption>${e(title)}</figcaption>
      <div class="oft-chart-bars" aria-hidden="true">${list.map(r => {
        const t = Number.isFinite(Number(r.target)) ? Number(r.target) : null;
        return `<div class="oft-chart-row"><span class="l">${e(r.label)}</span><span class="t"><span class="f${t != null && Number(r.value) >= t ? ' met' : ''}" style="width:${pct(r.value)}"></span>${t != null ? `<span class="m" style="left:calc(${pct(t)} - 1px)"></span>` : ''}</span><span class="v">${e(shown(r))}${t != null ? ` of ${e(num(t))}` : ''}</span></div>`;
      }).join('')}</div>
      <table><thead><tr><th scope="col">${e(title)}</th><th scope="col" class="n">${e(valueLabel)}</th>${hasTarget ? `<th scope="col" class="n">${e(targetLabel)}</th>` : ''}</tr></thead>
      <tbody>${list.map(r => `<tr><th scope="row">${e(r.label)}</th><td class="n">${e(shown(r))}</td>${hasTarget ? `<td class="n">${Number.isFinite(Number(r.target)) ? e(num(r.target)) : ''}</td>` : ''}</tr>`).join('')}</tbody></table>
      ${note ? `<p class="note">${e(note)}</p>` : ''}</figure>`;
  }
  // A figure written as text, such as "$350,000", "1.1 million" or "40k", as a number.
  function parse(text) {
    const t = str(text).toLowerCase().replace(/,/g, '');
    const m = t.match(/-?\d+(?:\.\d+)?/);
    if (!m) return null;
    let n = Number(m[0]);
    const rest = t.slice(m.index + m[0].length).trim();
    if (/^(billion|bn|b)\b/.test(rest)) n *= 1e9; else if (/^(million|mn|m)\b/.test(rest)) n *= 1e6; else if (/^(thousand|k)\b/.test(rest)) n *= 1e3;
    return n;
  }
  return { bars, parse };
})();
