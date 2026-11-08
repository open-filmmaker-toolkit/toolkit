// Sending a tool's costs to the budget, the way deal memos do. A tool lists its costs in
// OFT_COSTS = { label, noun, items: () => [{ id, description, quantity, unit, rate, multiplier? }] }.
// Once you pick an account, each cost gets a budget line there, tagged with where it came from
// (line.source = { tool, id }), and the lines follow the tool from then on: their numbers change
// when the costs do, and a cost that's gone takes its line with it. Names and accounts you change
// in the budget are kept. The choice is kept in budgetLinks[tool].accountId.
const oftCosts = (() => {
  const str = v => (v == null ? '' : String(v));
  const list = v => (Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []);
  const e = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  const n = v => (v === '' || v == null || !isFinite(Number(v)) ? 0 : Number(v));
  const budget = () => (doc.budget && typeof doc.budget === 'object' && !Array.isArray(doc.budget) ? doc.budget : null);
  const accounts = () => list(budget() && budget().accounts).filter(a => a.id);
  const link = () => { const l = doc.budgetLinks && doc.budgetLinks[OFT_SLUG]; return l && typeof l === 'object' && accounts().some(a => a.id === l.accountId) ? l : null; };
  const money = v => { try { return Number(v).toLocaleString(undefined, { style: 'currency', currency: (doc.project && doc.project.currency) || 'USD' }); } catch { return `${Number(v).toFixed(2)}`; } };
  const items = () => (typeof OFT_COSTS !== 'undefined' ? OFT_COSTS.items() : []).filter(i => i && i.id && n(i.rate) && n(i.quantity));
  const amount = i => n(i.quantity) * (i.multiplier == null ? 1 : n(i.multiplier)) * n(i.rate);
  const mine = l => l.source && l.source.tool === OFT_SLUG;
  // Brings the budget lines up to date with the tool's costs. Returns how many lines were added, changed and removed.
  function sync() {
    const l = link(), b = budget();
    if (!l || !b) return null;
    if (!Array.isArray(b.lines)) b.lines = [];
    const want = items(), out = { added: 0, changed: 0, removed: 0 };
    for (const i of want) {
      const nums = { quantity: n(i.quantity), unit: i.unit || 'Flat', rate: n(i.rate) };
      if (i.multiplier != null && n(i.multiplier) !== 1) nums.multiplier = n(i.multiplier);
      const line = b.lines.find(x => x && mine(x) && x.source.id === i.id);
      if (line) {
        const before = JSON.stringify([line.quantity, line.unit, line.rate, line.multiplier]);
        Object.assign(line, nums); if (nums.multiplier == null) delete line.multiplier;
        if (JSON.stringify([line.quantity, line.unit, line.rate, line.multiplier]) !== before) out.changed++;
      } else {
        b.lines.push(Object.assign({ id: newId('line'), accountId: l.accountId, description: i.description || 'Cost' }, nums, { source: { tool: OFT_SLUG, id: i.id } }));
        out.added++;
      }
    }
    const keep = new Set(want.map(i => i.id));
    const before = b.lines.length;
    b.lines = b.lines.filter(x => !(x && mine(x) && !keep.has(x.source.id)));
    out.removed = before - b.lines.length;
    return out;
  }
  function dialog() {
    let dlg = document.getElementById('oftCostsDialog');
    if (dlg) return dlg;
    dlg = document.createElement('dialog');
    dlg.className = 'oft-dialog'; dlg.id = 'oftCostsDialog'; dlg.setAttribute('aria-labelledby', 'oftCostsTitle');
    dlg.innerHTML = `<h2 id="oftCostsTitle">Send costs to the budget</h2><p id="oftCostsIntro"></p><div id="oftCostsList"></div>
  <div id="oftCostsPick"><label class="oft-field" for="oftCostsAccount">Budget account</label><select id="oftCostsAccount"></select></div>
  <div class="oft-actions"><button type="button" class="btn" id="oftCostsStop" hidden>Stop sending</button><button type="button" class="btn" id="oftCostsCancel">Cancel</button><button type="button" class="btn primary" id="oftCostsSend">Send to the budget</button></div>`;
    document.body.append(dlg);
    const css = document.createElement('style');
    css.textContent = '#oftCostsAccount { width: 100%; padding: 8px 10px; border: 1px solid var(--rule); border-radius: 6px; background: var(--sheet); color: var(--ink); font: inherit; }\n.oft-costs { width: 100%; border-collapse: collapse; font-size: 14px; margin: 6px 0 10px; }\n.oft-costs td, .oft-costs th { padding: 4px 6px; border-bottom: 1px solid var(--rule); text-align: left; }\n.oft-costs td.r, .oft-costs th.r { text-align: right; white-space: nowrap; }';
    document.head.append(css);
    dlg.querySelector('#oftCostsCancel').onclick = () => dlg.close();
    return dlg;
  }
  function open() {
    const dlg = dialog(), $ = q => dlg.querySelector(q);
    const all = items(), b = budget(), l = link(), C = typeof OFT_COSTS !== 'undefined' ? OFT_COSTS : { label: 'costs', noun: 'cost' };
    const total = all.reduce((t, i) => t + amount(i), 0);
    $('#oftCostsList').innerHTML = all.length ? `<table class="oft-costs"><thead><tr><th>${e(C.noun ? C.noun[0].toUpperCase() + C.noun.slice(1) : 'Cost')}</th><th class="r">Amount</th></tr></thead><tbody>${all.map(i => `<tr><td>${e(i.description)}<br><small>${e(`${n(i.quantity)} ${str(i.unit || 'flat').toLowerCase()}${i.multiplier != null && n(i.multiplier) !== 1 ? ` × ${n(i.multiplier)}` : ''} at ${money(n(i.rate))}`)}</small></td><td class="r">${e(money(amount(i)))}</td></tr>`).join('')}<tr><th>Total</th><th class="r">${e(money(total))}</th></tr></tbody></table>` : `<p>${e(C.none || 'There are no costs to send yet.')}</p>`;
    $('#oftCostsPick').hidden = !b || !accounts().length;
    $('#oftCostsAccount').innerHTML = accounts().map(a => `<option value="${e(a.id)}">${e([a.code, a.name].filter(Boolean).join(' '))}</option>`).join('');
    if (l) $('#oftCostsAccount').value = l.accountId;
    else { const guess = accounts().find(a => C.account && C.account.test([a.code, a.name].join(' '))); if (guess) $('#oftCostsAccount').value = guess.id; }
    $('#oftCostsIntro').textContent = !b || !accounts().length ? 'The project has no budget accounts yet. Start the budget in the budget tool, then send these costs to it.'
      : l ? `These ${C.label} are in the budget, and their lines follow this tool: when a cost changes here, its line changes too. Lines you rename or move to another account stay where you put them.` : `Each cost gets a line in the account you choose, marked as coming from here. From then on the lines follow this tool: when a cost changes here, its line changes too.`;
    $('#oftCostsSend').disabled = !b || !accounts().length;
    $('#oftCostsSend').textContent = l ? 'Update the budget' : 'Send to the budget';
    $('#oftCostsStop').hidden = !l;
    $('#oftCostsSend').onclick = () => {
      doc.budgetLinks = doc.budgetLinks && typeof doc.budgetLinks === 'object' && !Array.isArray(doc.budgetLinks) ? doc.budgetLinks : {};
      const acc = $('#oftCostsAccount').value, was = link();
      doc.budgetLinks[OFT_SLUG] = Object.assign({}, doc.budgetLinks[OFT_SLUG], { accountId: acc });
      // Lines already sent move to a newly chosen account.
      if (was && was.accountId !== acc) for (const x of list(budget().lines)) if (mine(x) && x.accountId === was.accountId) x.accountId = acc;
      const r = sync();
      dlg.close();
      changed();
      toast(`Sent to the budget: ${r.added} line${r.added === 1 ? '' : 's'} added${r.changed ? `, ${r.changed} changed` : ''}${r.removed ? `, ${r.removed} removed` : ''}.`);
    };
    $('#oftCostsStop').onclick = () => {
      delete doc.budgetLinks[OFT_SLUG];
      if (!Object.keys(doc.budgetLinks).length) delete doc.budgetLinks;
      let k = 0;
      for (const x of list(budget() && budget().lines)) if (mine(x)) { delete x.source; k++; }
      dlg.close();
      changed();
      toast(`Stopped sending. The ${k} line${k === 1 ? '' : 's'} already in the budget stay${k === 1 ? 's' : ''} as ${k === 1 ? 'it is' : 'they are'}.`);
    };
    dlg.showModal();
  }
  return { sync, open, items, amount, link };
})();
// Keeps the budget lines in step with every change, once a budget account is chosen.
if (typeof OFT_COSTS !== 'undefined') {
  const oftCostsChanged = changed;
  changed = function () { oftCosts.sync(); return oftCostsChanged.apply(this, arguments); };
}
