// Release status for a person or a location, worked out the way the release tracker does it, so
// the clearance log and call sheet say the same thing. Releases are contracts whose type contains
// "release" (but not materials releases), covering people in personIds and places in locationIds.
const oftReleases = (() => {
  const str = v => (v == null ? '' : String(v));
  const list = v => (Array.isArray(v) ? v.filter(x => x && typeof x === 'object') : []);
  const day = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  const covers = c => /release/i.test(str(c.type)) && !/material/i.test(str(c.type));
  function stateOf(c) {
    if (c.status === 'signed') return /^\d{4}-\d{2}-\d{2}$/.test(str(c.expirationDate)) && c.expirationDate < day() ? 'expired' : 'signed';
    if (c.status === 'pending' || c.status === 'declined') return c.status;
    return 'pending';
  }
  const RANK = { signed: 0, pending: 1, expired: 2, declined: 3 };
  const LABEL = { signed: 'Release signed', pending: 'Release not signed yet', expired: 'Release expired', declined: 'Release declined', missing: 'No release' };
  // The best standing release: signed beats waiting, beats expired, beats declined.
  function status(kind, id) {
    const field = kind === 'person' ? 'personIds' : 'locationIds';
    const all = list(doc.contracts).filter(c => covers(c) && Array.isArray(c[field]) && c[field].includes(id))
      .sort((a, b) => RANK[stateOf(a)] - RANK[stateOf(b)] || str(b.signedDate).localeCompare(str(a.signedDate)));
    const state = all.length ? stateOf(all[0]) : 'missing';
    return { state, label: LABEL[state], ok: state === 'signed', release: all[0] || null };
  }
  return { status, LABEL };
})();
