// How the budget adds up, shared by every tool that reads it.
const SECTIONS = [
  { id: 'atl', label: 'Above the line' },
  { id: 'production', label: 'Production' },
  { id: 'post', label: 'Post-production' },
  { id: 'other', label: 'Other costs' },
];
const sectionLabel = id => (SECTIONS.find(s => s.id === id) || SECTIONS[3]).label;
const num = v => (v === '' || v == null || !isFinite(Number(v)) ? 0 : Number(v));
const cents = n => Math.round(n * 100) / 100;
const objs = v => arr(v).filter(x => x && typeof x === 'object');
// How many people a line pays: its multiplier, which defaults to 1.
const linePeople = l => (l.multiplier === '' || l.multiplier == null ? 1 : num(l.multiplier));
// A line costs quantity × multiplier × rate, in the line's own currency.
const lineRaw = l => cents(num(l.quantity) * linePeople(l) * num(l.rate));
// The same, in the project currency (see the exchange rates).
function lineSubtotal(l) {
  const raw = lineRaw(l);
  return l.currency && typeof oftMoney !== 'undefined' ? cents(oftMoney.convert(raw, l.currency)) : raw;
}
// A line can have several fringes. Older files have one, in fringeId.
const lineFringeIds = l => (Array.isArray(l.fringeIds) && l.fringeIds.length ? l.fringeIds : l.fringeId ? [l.fringeId] : []);
// A fringe is a percentage of the line. With a cap, such as a payroll tax that stops at a wage limit,
// it applies only to wages up to the cap for each person on the line.
function fringeOn(f, sub, l) {
  const cap = num(f.cap);
  const base = cap > 0 ? Math.min(sub, cap * Math.max(linePeople(l), 1)) : sub;
  return cents(base * num(f.percent) / 100);
}
const accountOrder = (a, b) => SECTIONS.findIndex(s => s.id === a.section) - SECTIONS.findIndex(s => s.id === b.section) ||
  str(a.code).localeCompare(str(b.code), undefined, { numeric: true }) || str(a.name).localeCompare(str(b.name));
// Totals for a budget record: each line with its fringes, each account, each section, then fringes and percentages on the subtotal.
function budgetTotals(b) {
  b = b && typeof b === 'object' ? b : {};
  const fringes = objs(b.fringes);
  const markups = objs(b.markups);
  const accounts = objs(b.accounts).slice().sort(accountOrder);
  const lines = objs(b.lines).map(l => {
    const sub = lineSubtotal(l);
    const parts = lineFringeIds(l).map(id => fringes.find(x => x.id === id)).filter(Boolean).map(f => ({ fringe: f, amount: fringeOn(f, sub, l) }));
    const fringe = cents(parts.reduce((t, p) => t + p.amount, 0));
    return { line: l, sub, fringe, fringes: parts, total: cents(sub + fringe) };
  });
  const byAccount = accounts.map(a => {
    const ls = lines.filter(x => x.line.accountId === a.id);
    return { account: a, lines: ls, sub: cents(ls.reduce((t, x) => t + x.sub, 0)), fringe: cents(ls.reduce((t, x) => t + x.fringe, 0)), total: cents(ls.reduce((t, x) => t + x.total, 0)) };
  });
  const loose = lines.filter(x => !accounts.some(a => a.id === x.line.accountId));
  const sections = SECTIONS.map(s => {
    const as = byAccount.filter(x => (SECTIONS.some(y => y.id === x.account.section) ? x.account.section : 'other') === s.id);
    return { section: s, accounts: as, total: cents(as.reduce((t, x) => t + x.total, 0)) };
  });
  const direct = cents(lines.reduce((t, x) => t + x.sub, 0));
  const fringeTotal = cents(lines.reduce((t, x) => t + x.fringe, 0));
  const subtotal = cents(direct + fringeTotal);
  const marks = markups.map(m => ({ markup: m, amount: cents(subtotal * num(m.percent) / 100) }));
  const grand = cents(subtotal + marks.reduce((t, x) => t + x.amount, 0));
  const fringeTotals = fringes.map(f => ({ fringe: f, amount: cents(lines.reduce((t, x) => t + x.fringes.filter(p => p.fringe === f).reduce((s, p) => s + p.amount, 0), 0)) }));
  return { lines, accounts: byAccount, loose, sections, direct, fringeTotal, fringeTotals, subtotal, markups: marks, grand };
}
