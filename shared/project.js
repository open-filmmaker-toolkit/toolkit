// Shared by the home page and the tools: what needs you across the project,
// every date in it as one calendar file, and read-only summaries to share.
// Pure functions of the project data; nothing here reads or writes files.
const oftProject = (() => {
  const arr = v => (Array.isArray(v) ? v : []);
  const str = v => (v == null ? '' : String(v));
  const isDay = v => /^\d{4}-\d{2}-\d{2}$/.test(str(v));
  const num = v => (v == null || v === '' || !isFinite(Number(v)) ? 0 : Number(v));
  const same = (a, b) => !!str(a).trim() && str(a).trim().toLowerCase() === str(b).trim().toLowerCase();
  const esc = s => str(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  function today() { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; }
  function addDays(iso, n) { const [y, m, d] = iso.split('-').map(Number); const t = new Date(Date.UTC(y, m - 1, d + n)); return t.toISOString().slice(0, 10); }
  function fmt(iso) { if (!isDay(iso)) return str(iso); const [y, m, d] = iso.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString(undefined, { timeZone: 'UTC', month: 'short', day: 'numeric', year: iso.slice(0, 4) === today().slice(0, 4) ? undefined : 'numeric' }); }
  function money(n, cur) { try { return Number(n).toLocaleString(undefined, { style: 'currency', currency: cur || 'USD', maximumFractionDigits: Number(n) % 1 ? 2 : 0 }); } catch { return `${cur || ''} ${Number(n).toLocaleString()}`.trim(); } }

  const TOOLS = {
    'release-tracker': 'Release tracker', 'festival-strategy': 'Festival strategy map', 'festival-submissions': 'Festival submission tracker', 'qc-tracker': 'QC tracker',
    'contract-archive': 'Contract and release archive', bookings: 'Booking trackers', 'grant-reports': 'Grant final reports', 'grant-calendar': 'Grant calendar',
    'coi-permit-tracker': 'COI and permit tracker', 'license-tracker': 'License tracker', deliverables: 'Deliverables checklist', 'funder-crm': 'Funder CRM',
    'partner-crm': 'Partner CRM', 'subject-tracker': 'Subject tracker', 'rights-matrix': 'Rights availability matrix', 'name-supers': 'Name supers list',
    'awards-social': 'Awards and social calendars', 'shooting-calendar': 'Shooting calendar', 'call-sheet': 'Call sheet', 'travel-sheet': 'Travel sheet',
    'location-scout': 'Location scout sheet', 'interview-prep': 'Interview prep', 'finance-plan': 'Finance plan', 'cut-tracker': 'Cut version tracker',
    'press-list': 'Press list', 'revenue-tracker': 'Revenue tracker', 'impact-report': 'Impact report', 'clearance-log': 'Clearance log', budget: 'Budget',
    'final-cost-report': 'Final cost report', 'deal-memos': 'Deal memos', 'risk-plan': 'Risk plans', 'theory-of-change': 'Theory of change builder',
  };

  // ---------- What needs you ----------
  // Each rule is the same one the tool itself uses to flag a record.
  function flags(d, asOf) {
    const t = asOf || today(), out = [];
    const add = (slug, id, title, date, detail, level) => out.push({ slug, tool: TOOLS[slug], id, title, date: date || '', detail: detail || '', level: level || (date ? (date < t ? 'overdue' : date <= addDays(t, 7) ? 'week' : 'soon') : 'fix') });
    const contracts = arr(d.contracts).filter(c => c && typeof c === 'object');
    const people = arr(d.people).filter(Boolean), locations = arr(d.locations).filter(Boolean);
    const roleOf = p => (Array.isArray(p.roles) ? p.roles.join(', ') : str(p.roles));

    // Release tracker: anyone or anywhere on camera without a signed release
    const isRelease = c => /release/i.test(str(c.type)) && !/material/i.test(str(c.type));
    const stateOf = c => c.status === 'signed' ? (isDay(c.expirationDate) && c.expirationDate < t ? 'expired' : 'signed') : (c.status === 'pending' || c.status === 'declined') ? c.status : c.status ? 'other' : 'pending';
    const RANK = { signed: 0, pending: 1, expired: 2, declined: 3, other: 4 };
    const releasesFor = (field, id) => contracts.filter(c => isRelease(c) && arr(c[field]).includes(id));
    const coverage = (field, id) => { const l = releasesFor(field, id).sort((a, b) => RANK[stateOf(a)] - RANK[stateOf(b)] || str(b.signedDate).localeCompare(str(a.signedDate))); return l.length ? stateOf(l[0]) : 'missing'; };
    const onSheets = new Set(arr(d.callSheets).map(s => s && s.locationId).filter(Boolean));
    const filmed = [
      ...people.filter(p => p.onCamera === true || (p.onCamera !== false && releasesFor('personIds', p.id).length)).map(p => ['personIds', p]),
      ...locations.filter(l => l.onCamera === true || (l.onCamera !== false && (onSheets.has(l.id) || releasesFor('locationIds', l.id).length))).map(l => ['locationIds', l]),
    ];
    for (const [field, x] of filmed) {
      const s = coverage(field, x.id);
      if (s === 'missing') add('release-tracker', x.id, `${x.name || 'Someone'} is on camera with no release`);
      else if (s === 'declined') add('release-tracker', x.id, `${x.name || 'Someone'} declined the release`, '', "Don't use the footage");
      else if (s === 'expired') add('release-tracker', x.id, `The release for ${x.name || 'someone'} has expired`);
    }

    // Festival strategy map: an earlier festival that ends a premiere
    const fs = d.festivalStrategy || {}, fests = arr(d.festivals).filter(Boolean);
    const firstDay = f => [f.startDate, ...arr(f.screenings).map(s => s && s.date)].filter(isDay).sort()[0] || '';
    const breaks = (e, f) => { const p = f.premiere; if (p === 'world') return true; if (p === 'international') return !!str(e.country).trim() && !!str(fs.homeCountry).trim() && !same(e.country, fs.homeCountry); if (p === 'regional') return same(e.region, f.region); if (p === 'national') return same(e.country, f.country); if (p === 'city') return same(e.city, f.city); return false; };
    const live = fests.filter(f => f.status !== 'declined' && firstDay(f));
    for (const f of live) {
      if (!f.premiere || f.premiere === 'none') continue;
      for (const e of live) if (e !== f && firstDay(e) < firstDay(f) && breaks(e, f)) add('festival-strategy', f.id, e.status === 'accepted' ? `${e.name || 'An earlier festival'} ends your premiere at ${f.name || 'a later festival'}` : `${e.name || 'An earlier festival'} could cost your premiere at ${f.name || 'a later festival'}`, '', `${f.name || 'It'} starts ${fmt(firstDay(f))}`);
    }
    // Festival submission tracker: entry deadlines
    for (const f of fests) if (f.status === 'planned' && isDay(f.deadline) && f.deadline <= addDays(t, 60)) add('festival-submissions', f.id, f.deadline < t ? `The deadline for ${f.name || 'a festival'} passed` : `Submit to ${f.name || 'a festival'}`, f.deadline);

    // QC tracker: open fixes
    for (const r of arr((d.qc || {}).reports)) for (const i of arr(r && r.issues)) if (i && (!i.fix || i.fix === 'open' || i.fix === 'disputed')) add('qc-tracker', i.id, `${i.description || 'A QC issue'}${i.tc ? ` at ${i.tc}` : ''}`, '', `${i.fix === 'disputed' ? 'Disputed' : 'Open'}${i.owner ? `. For the ${i.owner}` : ''}`);

    // Contract and release archive: signed with no copy linked
    const assets = new Map(arr(d.assets).filter(Boolean).map(a => [a.id, a]));
    const noCopy = contracts.filter(c => ['signed', 'received', 'issued'].includes(c.status) && !arr(c.assetIds).map(id => assets.get(id)).some(a => a && (str(a.relativePath).trim() || /^data:/.test(str(a.data)))));
    if (noCopy.length) add('contract-archive', noCopy[0].id, `${noCopy.length} signed agreement${noCopy.length === 1 ? ' has' : 's have'} no copy linked`);

    // Booking trackers: invoices over 30 days old
    for (const b of arr(d.bookings).filter(Boolean)) if (b.payment === 'invoiced' && isDay(b.invoicedDate) && addDays(b.invoicedDate, 30) < t) add('bookings', b.id, `${b.venue || 'A booking'} hasn't paid`, addDays(b.invoicedDate, 30), `${b.fee ? `${money(b.fee, (d.project || {}).currency)} ` : ''}invoiced ${fmt(b.invoicedDate)}`);

    // Grant final reports and the grant calendar
    const grants = arr(d.grants).filter(Boolean);
    for (const r of arr(d.grantReports).filter(Boolean)) {
      const g = grants.find(x => x.id === r.grantId);
      if (g && g.status === 'awarded' && r.status !== 'submitted' && isDay(r.dueDate) && r.dueDate <= addDays(t, 60)) add('grant-reports', g.id, `${g.funder || g.name || 'Grant'} final report`, r.dueDate);
    }
    for (const g of grants) if (['researching', 'drafting'].includes(g.status) && isDay(g.deadline) && g.deadline >= t && g.deadline <= addDays(t, 60)) add('grant-calendar', g.id, `Apply to ${g.name || g.funder || 'a grant'}`, g.deadline);

    // COI and permit tracker, license tracker, rights matrix
    for (const c of contracts) {
      if ((c.type === 'certificate of insurance' || c.type === 'permit') && ['received', 'issued'].includes(c.status) && isDay(c.expirationDate) && c.expirationDate <= addDays(t, 30)) add('coi-permit-tracker', c.id, `${c.title || (c.type === 'permit' ? 'A permit' : 'A certificate')} ${c.expirationDate < t ? 'has expired' : 'expires'}`, c.expirationDate);
      if (c.type === 'license') {
        if (isDay(c.expirationDate) && c.expirationDate <= addDays(t, 90)) add('license-tracker', c.id, `${c.title || 'A license'} ${c.expirationDate < t ? 'has expired' : 'expires'}`, c.expirationDate);
        for (const o of arr(c.options)) if (o && !o.exercised && isDay(o.deadline) && o.deadline <= addDays(t, 60)) add('license-tracker', c.id, `${o.deadline < t ? 'Option lapsed' : 'Exercise the option'}: ${o.what || c.title || 'option'}`, o.deadline);
        for (const p of arr(c.payments)) if (p && !p.paid && isDay(p.due) && p.due <= addDays(t, 30)) add('license-tracker', c.id, `Pay ${money(num(p.amount), (d.project || {}).currency)} for ${c.title || 'a license'}`, p.due);
      }
      if (c.type === 'distribution' && c.status === 'signed' && isDay(c.expirationDate) && c.expirationDate >= t && c.expirationDate <= addDays(t, 183)) add('rights-matrix', c.id, `Rights from ${c.licensee || c.title || 'a deal'} revert`, c.expirationDate, arr(c.territories).join(', '));
    }

    // Deliverables checklist
    const del = d.deliverables || {};
    for (const i of deliverables(d)) {
      const due = isDay(i.due) ? i.due : isDay(del.dueDate) ? del.dueDate : '';
      if (!['delivered', 'accepted', 'na'].includes(i.status) && due && due <= addDays(t, 14)) add('deliverables', i.id, `Deliver ${i.title || i.key || 'an item'}`, due, i.owner || '');
    }

    // Funder CRM and partner CRM next steps, subject tracker follow-ups
    for (const f of arr(d.funders).filter(Boolean)) for (const s of arr(f.nextSteps)) if (s && !s.done && isDay(s.due) && s.due <= addDays(t, 7)) add('funder-crm', f.id, `${s.text || 'Next step'} (${f.name || 'funder'})`, s.due);
    for (const p of arr(d.partners).filter(Boolean)) for (const s of arr(p.commitments)) if (s && !s.done && isDay(s.due) && s.due <= addDays(t, 7)) add('partner-crm', p.id, `${s.text || 'Commitment'} (${p.name || 'partner'})`, s.due);
    for (const s of arr(d.subjects).filter(Boolean)) if (isDay(s.nextFollowUp) && s.status !== 'declined' && s.nextFollowUp <= addDays(t, 7)) add('subject-tracker', s.id, `Follow up with ${s.name || 'a subject'}`, s.nextFollowUp);

    // Name supers list: people on camera with no super
    const supers = arr((d.supers || {}).entries).filter(Boolean);
    const onCam = p => p.onCamera === true || (p.onCamera !== false && /subject|interview|featur|contributor/i.test(roleOf(p)));
    for (const p of people) if (onCam(p) && str(p.name).trim() && !supers.some(e => e.personId === p.id)) add('name-supers', p.id, `${p.name} is on camera with no super`);

    // Awards: entry deadlines
    for (const a of arr(d.awards).filter(Boolean)) if (!['entered', 'declined', 'skipped'].includes(a.status) && isDay(a.deadline) && a.deadline >= t && a.deadline <= addDays(t, 60)) add('awards-social', a.id, `Enter ${a.name || 'an award'}`, a.deadline);

    const ORDER = { overdue: 0, week: 1, fix: 2, soon: 3 };
    return out.sort((a, b) => ORDER[a.level] - ORDER[b.level] || (a.date || '9999').localeCompare(b.date || '9999') || a.title.localeCompare(b.title));
  }

  // The deliverables checklist's usual list, merged with the items the project changed or added.
  const BUILT = { dcp: 'Digital cinema package (DCP)', master: 'Master with titles (ProRes)', textless: 'Textless master and textless elements', hd: 'Broadcast master', trailer: 'Trailer', mix51: '5.1 mix', stereo: 'Stereo mix', me: 'Music and effects (M&E) mix', stems: 'Dialogue, music and effects stems', cc: 'Closed captions', sdh: 'Subtitles for the deaf and hard of hearing (SDH)', dcl: 'Dialogue and continuity list', subs: 'Subtitles in other languages', keyart: 'Key art', stills: 'Production stills', epk: 'Press notes and EPK', chain: 'Chain-of-title documents', eo: 'Errors and omissions (E&O) insurance certificate', cue: 'Music cue sheet', credits: 'Final credits list', licenses: 'Music and archival licenses', releases: 'Appearance and location releases', qc: 'Quality control (QC) report' };
  function deliverables(d) {
    const saved = arr((d.deliverables || {}).items).filter(x => x && (x.key || x.id));
    return Object.entries(BUILT).map(([key, title]) => Object.assign({ id: `deliverable-${key}`, key, title, status: 'todo' }, saved.find(s => s.key === key) || {}, { title: (saved.find(s => s.key === key) || {}).title || title }))
      .concat(saved.filter(s => !s.key || !BUILT[s.key]));
  }

  // ---------- At a glance ----------
  function glance(d) {
    const cur = (d.project || {}).currency || 'USD';
    const statements = arr(d.revenueStatements).filter(Boolean);
    const net = s => (s.net != null && s.net !== '' ? num(s.net) : num(s.gross) - num(s.fees) - num(s.expenses));
    const due = statements.reduce((a, s) => a + net(s), 0), paid = statements.filter(s => isDay(s.paidDate)).reduce((a, s) => a + net(s), 0);
    const toc = d.theoryOfChange || {}, results = (d.impactReport || {}).results || {};
    const ind = arr(toc.indicators).find(i => i && num(i.target) > 0 && results[i.id] && results[i.id].value != null) || arr(toc.indicators).find(i => i && num(i.target) > 0);
    return {
      revenue: statements.length ? { due: money(due, cur), paid: money(paid, cur), allPaid: Math.abs(due - paid) < 0.005 } : null,
      impact: ind ? { value: num((results[ind.id] || {}).value), target: num(ind.target), unit: ind.unit || '', text: ind.text || '' } : null,
    };
  }

  // ---------- Every date ----------
  const KINDS = [
    ['grants', 'Grant deadlines and reports'], ['shoot', 'Shoot days, scouts, interviews and travel'], ['paperwork', 'Certificates, permits, licenses and payments'],
    ['festivals', 'Festivals and awards'], ['release', 'Screenings, bookings and posts'], ['delivery', 'Delivery and QC'],
    ['contacts', 'Follow-ups and next steps'], ['money', 'Money coming in'],
  ];
  function dates(d) {
    const out = [];
    const add = (kind, slug, id, field, date, title, end) => { if (isDay(date)) out.push({ kind, slug, tool: TOOLS[slug], id, uid: `${id}-${field}`, date, end: isDay(end) && end > date ? end : '', title }); };
    for (const g of arr(d.grants).filter(Boolean)) { add('grants', 'grant-calendar', g.id, 'deadline', g.deadline, `Deadline: ${g.name || g.funder || 'grant'}`); add('grants', 'grant-calendar', g.id, 'decision', g.decisionOn, `Decision expected: ${g.name || g.funder || 'grant'}`); }
    for (const r of arr(d.grantReports).filter(Boolean)) { const g = arr(d.grants).find(x => x && x.id === r.grantId) || {}; add('grants', 'grant-reports', r.id, 'due', r.dueDate, `Final report due: ${g.funder || g.name || 'grant'}`); }
    for (const s of arr(d.shootDays).filter(Boolean)) add('shoot', 'shooting-calendar', s.id, 'date', s.date, `${s.kind === 'travel' ? 'Travel day' : s.kind === 'hold' ? 'Hold' : 'Shoot day'}${s.title || s.label ? `: ${s.title || s.label}` : ''}`);
    const shootDates = new Set(arr(d.shootDays).map(s => s && s.date));
    for (const c of arr(d.callSheets).filter(Boolean)) if (!shootDates.has(c.date)) add('shoot', 'call-sheet', c.id, 'date', c.date, `Call sheet${c.title ? `: ${c.title}` : ''}`);
    for (const s of arr(d.scouts).filter(Boolean)) { const l = arr(d.locations).find(x => x && x.id === s.locationId); add('shoot', 'location-scout', s.id, 'date', s.date, `Scout${l ? `: ${l.name}` : ''}`); }
    for (const i of arr(d.interviews).filter(Boolean)) { const p = arr(d.people).find(x => x && x.id === i.personId); add('shoot', 'interview-prep', i.id, 'date', i.date, `Interview${p ? `: ${p.name}` : i.title ? `: ${i.title}` : ''}`); }
    for (const t of arr(d.trips).filter(Boolean)) add('shoot', 'travel-sheet', t.id, 'trip', t.startDate, `Trip${t.name ? `: ${t.name}` : t.destination ? ` to ${t.destination}` : ''}`, t.endDate);
    for (const c of arr(d.contracts).filter(Boolean)) {
      const name = c.title || c.type || 'Agreement';
      if (c.type === 'certificate of insurance' || c.type === 'permit') add('paperwork', 'coi-permit-tracker', c.id, 'expires', c.expirationDate, `Expires: ${name}`);
      else if (c.type === 'license') {
        add('paperwork', 'license-tracker', c.id, 'expires', c.expirationDate, `License expires: ${name}`);
        arr(c.options).forEach((o, i) => o && !o.exercised && add('paperwork', 'license-tracker', c.id, `option-${o.id || i}`, o.deadline, `Option deadline: ${o.what || name}`));
        arr(c.payments).forEach((p, i) => p && !p.paid && add('paperwork', 'license-tracker', c.id, `payment-${p.id || i}`, p.due, `Payment due: ${name}`));
      } else if (c.type === 'distribution') add('paperwork', 'rights-matrix', c.id, 'expires', c.expirationDate, `Rights revert: ${c.licensee || name}`);
    }
    for (const f of arr(d.festivals).filter(Boolean)) {
      if (f.status === 'planned') add('festivals', 'festival-submissions', f.id, 'deadline', f.deadline, `Entry deadline: ${f.name || 'festival'}`);
      if (f.status !== 'declined') { add('festivals', 'festival-submissions', f.id, 'notify', f.notifyDate, `Decision: ${f.name || 'festival'}`); add('festivals', 'festival-submissions', f.id, 'festival', f.startDate, f.name || 'Festival', f.endDate); }
      arr(f.screenings).forEach((s, i) => s && add('festivals', 'festival-submissions', f.id, `screening-${s.id || i}`, s.date, `Screening at ${f.name || 'a festival'}`));
    }
    for (const a of arr(d.awards).filter(Boolean)) { add('festivals', 'awards-social', a.id, 'deadline', a.deadline, `Award entry deadline: ${a.name || 'award'}`); add('festivals', 'awards-social', a.id, 'nominations', a.nominationsDate, `Nominations: ${a.name || 'award'}`); add('festivals', 'awards-social', a.id, 'ceremony', a.ceremonyDate, `Ceremony: ${a.name || 'award'}`); }
    for (const s of arr(d.screenings).filter(Boolean)) add('release', 'press-list', s.id, 'date', s.date, s.title || s.name || 'Screening');
    for (const b of arr(d.bookings).filter(Boolean)) if (b.status !== 'declined' && b.status !== 'cancelled') add('release', 'bookings', b.id, 'start', b.startDate, `${b.kind === 'educational' ? 'License starts' : 'Booking'}: ${b.venue || 'venue'}`, b.kind === 'educational' ? '' : b.endDate);
    for (const p of arr(d.socialPosts).filter(Boolean)) add('release', 'awards-social', p.id, 'date', p.date, `Post${p.platform ? ` on ${p.platform}` : ''}${p.text ? `: ${str(p.text).slice(0, 60)}` : ''}`);
    const del = d.deliverables || {};
    add('delivery', 'deliverables', 'deliverables', 'due', del.dueDate, `Delivery due${del.deliverTo ? `: ${del.deliverTo}` : ''}`);
    for (const i of deliverables(d)) if (!['delivered', 'accepted', 'na'].includes(i.status) && isDay(i.due) && i.due !== del.dueDate) add('delivery', 'deliverables', i.id, 'due', i.due, `Deliver: ${i.title}`);
    for (const c of arr(d.cuts).filter(Boolean)) arr(c.screenings).forEach((s, i) => s && add('delivery', 'cut-tracker', c.id, `screening-${s.id || i}`, s.date, `Feedback screening: ${c.name || c.title || 'cut'}`));
    for (const f of arr(d.funders).filter(Boolean)) arr(f.nextSteps).forEach((s, i) => s && !s.done && add('contacts', 'funder-crm', f.id, `step-${s.id || i}`, s.due, `${s.text || 'Next step'} (${f.name || 'funder'})`));
    for (const p of arr(d.partners).filter(Boolean)) arr(p.commitments).forEach((s, i) => s && !s.done && add('contacts', 'partner-crm', p.id, `step-${s.id || i}`, s.due, `${s.text || 'Commitment'} (${p.name || 'partner'})`));
    for (const s of arr(d.subjects).filter(Boolean)) if (s.status !== 'declined') add('contacts', 'subject-tracker', s.id, 'followup', s.nextFollowUp, `Follow up with ${s.name || 'a subject'}`);
    for (const s of arr((d.financePlan || {}).sources).filter(Boolean)) {
      const g = arr(d.grants).find(x => x && x.id === s.grantId);
      arr(s.payments).forEach((p, i) => p && add('money', 'finance-plan', s.id, `payment-${i}`, p.date, `Expected: ${money(num(p.amount), (d.project || {}).currency)} from ${s.name || (g && (g.funder || g.name)) || 'a source'}`));
    }
    return out.sort((a, b) => a.date.localeCompare(b.date) || a.title.localeCompare(b.title));
  }
  function ics(d, kinds) {
    const keep = new Set(kinds || KINDS.map(k => k[0]));
    const text = s => str(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
    const fold = line => { const out = []; let cur = ''; for (const ch of line) { if (new TextEncoder().encode(cur + ch).length > 74) { out.push(cur); cur = ' ' + ch; } else cur += ch; } out.push(cur); return out.join('\r\n'); };
    const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    const title = (d.project || {}).title || 'Film project';
    const lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Open Filmmaker Toolkit//Project dates//EN', 'CALSCALE:GREGORIAN', `X-WR-CALNAME:${text(title)}`];
    const events = dates(d).filter(e => keep.has(e.kind));
    for (const e of events) {
      const end = addDays(e.end || e.date, 1).replace(/-/g, '');
      lines.push('BEGIN:VEVENT', `UID:${text(e.uid)}@open-filmmaker-toolkit`, `DTSTAMP:${stamp}`, `DTSTART;VALUE=DATE:${e.date.replace(/-/g, '')}`, `DTEND;VALUE=DATE:${end}`, `SUMMARY:${text(`${e.title} (${title})`)}`, `DESCRIPTION:${text(`From the ${e.tool}`)}`, 'TRANSP:TRANSPARENT', 'END:VEVENT');
    }
    lines.push('END:VCALENDAR');
    return { text: lines.map(fold).join('\r\n') + '\r\n', count: events.length };
  }

  // ---------- Read-only summaries ----------
  const PARTS = [
    ['clearances', 'Clearance status', 'Every third-party element and its license status, for an E&O lawyer'],
    ['releases', 'Releases', 'Who and where is on camera, and whether each has a signed release'],
    ['budget', 'Budget and costs', 'The budget by account, and what has been spent against it'],
    ['finance', 'Finance plan', 'Where the money is coming from'],
    ['schedule', 'Shoot days', 'The shooting schedule'],
    ['festivals', 'Festival plan', 'Festivals, dates and status'],
    ['delivery', 'Deliverables', 'What is due to whom, and what is done'],
    ['impact', 'Impact', 'Results against the campaign\'s targets'],
  ];
  const CONTACT = ['email', 'phone', 'address', 'contact', 'contacts', 'website'];
  function table(head, rows) {
    if (!rows.length) return '<p>Nothing here yet.</p>';
    return `<table><thead><tr>${head.map(h => `<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
  }
  // The project's own exchange rates (see shared/money.js): a dated rate applies from its date.
  function conv(d, amount, cur, date) {
    const home = str((d.project || {}).currency || 'USD').toUpperCase(); cur = str(cur).toUpperCase();
    if (!cur || cur === home) return amount;
    const rs = arr((d.project || {}).exchangeRates).filter(r => r && str(r.currency).toUpperCase() === cur && num(r.rate) > 0);
    const dated = rs.filter(r => isDay(r.date)).sort((a, b) => a.date.localeCompare(b.date));
    const hit = (isDay(date) && [...dated].reverse().find(r => r.date <= date)) || rs.find(r => !isDay(r.date)) || dated[dated.length - 1];
    return hit ? amount * num(hit.rate) : amount;
  }
  function budgetRows(d) {
    const b = d.budget || {}, fringes = arr(b.fringes).filter(Boolean);
    const spent = {};
    for (const e of arr(d.expenses).filter(Boolean)) spent[e.accountId] = (spent[e.accountId] || 0) + conv(d, num(e.amount), e.currency, e.date);
    let total = 0, totalSpent = 0;
    const rows = arr(b.accounts).filter(Boolean).map(a => {
      const sum = arr(b.lines).filter(l => l && l.accountId === a.id).reduce((s, l) => {
        const people = l.multiplier === '' || l.multiplier == null ? 1 : num(l.multiplier), base = conv(d, num(l.quantity) * people * num(l.rate), l.currency);
        const ids = Array.isArray(l.fringeIds) && l.fringeIds.length ? l.fringeIds : l.fringeId ? [l.fringeId] : [];
        return s + base + ids.map(id => fringes.find(f => f.id === id)).filter(Boolean).reduce((t, f) => t + (num(f.cap) > 0 ? Math.min(base, num(f.cap) * Math.max(people, 1)) : base) * num(f.percent) / 100, 0);
      }, 0);
      total += sum; totalSpent += spent[a.id] || 0;
      return { a, sum, spent: spent[a.id] || 0 };
    }).filter(r => r.sum || r.spent);
    const markups = arr(b.markups).filter(Boolean).map(m => ({ name: m.name, amount: total * num(m.percent) / 100 }));
    return { rows, markups, total: total + markups.reduce((s, m) => s + m.amount, 0), spent: totalSpent };
  }
  function summary(d, parts, opts) {
    const o = opts || {}, cur = (d.project || {}).currency || 'USD', p = d.project || {};
    const want = new Set(parts);
    const sections = [];
    const note = (r, extra) => [extra, o.notes ? r.notes : ''].filter(Boolean).join('. ');
    if (want.has('clearances')) {
      const head = ['Element', 'Type', 'Source', 'Rights holder', 'Status', 'Rights'].concat(o.fees ? ['Cost'] : [], o.contacts ? ['Contact'] : [], o.notes ? ['Notes'] : []);
      const rows = arr(d.thirdPartyElements).filter(Boolean).map(e => [e.description || e.name, e.type, e.source, e.rightsHolder, e.status, e.rights].concat(o.fees ? [e.cost != null && e.cost !== '' ? money(num(e.cost), cur) : ''] : [], o.contacts ? [e.contact] : [], o.notes ? [e.notes] : []));
      sections.push(['Clearance status', table(head, rows)]);
    }
    if (want.has('releases')) {
      const rel = arr(d.contracts).filter(c => c && /release/i.test(str(c.type)));
      const who = (c) => [...arr(c.personIds).map(id => (arr(d.people).find(x => x && x.id === id) || {}).name), ...arr(c.locationIds).map(id => (arr(d.locations).find(x => x && x.id === id) || {}).name)].filter(Boolean).join(', ');
      sections.push(['Releases', table(['Release', 'Covers', 'Type', 'Status', 'Signed'].concat(o.notes ? ['Notes'] : []), rel.map(c => [c.title, who(c), c.type, c.status, c.signedDate ? fmt(c.signedDate) : ''].concat(o.notes ? [c.notes] : [])))]);
    }
    if (want.has('budget')) {
      const r = budgetRows(d);
      const rows = r.rows.map(x => [`${x.a.code ? `${x.a.code} ` : ''}${x.a.name}`, money(x.sum, cur), money(x.spent, cur)]).concat(r.markups.map(m => [m.name, money(m.amount, cur), '']), [['Total', money(r.total, cur), money(r.spent, cur)]]);
      sections.push(['Budget and costs', table(['Account', 'Budget', 'Spent'], rows) + ((d.finalCostReport || {}).closeDate ? `<p>Costs run to ${esc(fmt(d.finalCostReport.closeDate))}${d.finalCostReport.final ? ', final' : ''}.</p>` : '')]);
    }
    if (want.has('finance')) {
      const rows = arr((d.financePlan || {}).sources).filter(Boolean).map(s => { const g = arr(d.grants).find(x => x && x.id === s.grantId) || {}; return [s.name || g.name || g.funder || s.kind, s.kind, s.status, money(arr(s.payments).reduce((a, x) => a + num(x && x.amount), 0), cur)].concat(o.notes ? [s.notes] : []); });
      sections.push(['Finance plan', table(['Source', 'Kind', 'Status', 'Amount'].concat(o.notes ? ['Notes'] : []), rows)]);
    }
    if (want.has('schedule')) {
      const rows = arr(d.shootDays).filter(Boolean).sort((a, b) => str(a.date).localeCompare(str(b.date))).map(s => [fmt(s.date), s.kind || 'shoot', s.title || s.label || '', arr(s.locationIds || (s.locationId ? [s.locationId] : [])).map(id => (arr(d.locations).find(x => x && x.id === id) || {}).name).filter(Boolean).join(', ')].concat(o.notes ? [s.notes] : []));
      sections.push(['Shoot days', table(['Date', 'Kind', 'Day', 'Locations'].concat(o.notes ? ['Notes'] : []), rows)]);
    }
    if (want.has('festivals')) {
      const rows = arr(d.festivals).filter(Boolean).map(f => [f.name, [f.city, f.country].filter(Boolean).join(', '), f.startDate ? fmt(f.startDate) : '', f.deadline ? fmt(f.deadline) : '', f.status].concat(o.fees ? [f.fee != null && f.fee !== '' ? money(num(f.fee), cur) : ''] : [], o.notes ? [f.notes] : []));
      sections.push(['Festival plan', table(['Festival', 'Place', 'Starts', 'Deadline', 'Status'].concat(o.fees ? ['Fee'] : [], o.notes ? ['Notes'] : []), rows)]);
    }
    if (want.has('delivery')) {
      const del = d.deliverables || {};
      const STATUS = { todo: 'To do', progress: 'In progress', delivered: 'Delivered', accepted: 'Accepted', na: 'Not needed' };
      const rows = deliverables(d).filter(i => i.status !== 'na').map(i => [i.title, STATUS[i.status] || i.status || '', i.due ? fmt(i.due) : del.dueDate ? fmt(del.dueDate) : '', i.spec || '']);
      sections.push(['Deliverables', `${del.deliverTo ? `<p>To ${esc(del.deliverTo)}${del.dueDate ? `, due ${esc(fmt(del.dueDate))}` : ''}.</p>` : ''}${table(['Item', 'Status', 'Due', 'Spec'], rows)}`]);
    }
    if (want.has('impact')) {
      const toc = d.theoryOfChange || {}, res = (d.impactReport || {}).results || {};
      const rows = arr(toc.indicators).filter(Boolean).map(i => [i.text, i.target != null ? `${i.target} ${i.unit || ''}`.trim() : '', res[i.id] && res[i.id].value != null ? `${res[i.id].value} ${i.unit || ''}`.trim() : 'Not measured yet', i.source || '']);
      sections.push(['Impact', `${toc.goal ? `<p>${esc(toc.goal)}</p>` : ''}${table(['Indicator', 'Target', 'So far', 'Measured by'], rows)}`]);
    }
    const made = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
    const css = 'body{margin:0;background:#fff;color:#1a2130;font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}main{max-width:960px;margin:0 auto;padding:24px 16px 48px}h1{font-size:26px;margin:0 0 4px}h2{font-size:19px;margin:28px 0 8px;padding-bottom:4px;border-bottom:2px solid #1a2130}.meta{color:#4b556a;margin:0 0 4px}.wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font-size:14px}th,td{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid #d4dad8}th{background:#f1f3f2}footer{margin-top:32px;color:#4b556a;font-size:13px}@media (prefers-color-scheme: dark){body{background:#141922;color:#e6e9ee}.meta,footer{color:#a6afbd}h2{border-color:#e6e9ee}th{background:#1b212b}th,td{border-color:#2f3744}}@media print{body{background:#fff;color:#000}.wrap{overflow:visible}}';
    const body = sections.map(([h, html]) => `<section><h2>${esc(h)}</h2><div class="wrap">${html}</div></section>`).join('');
    return `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">\n<title>${esc(p.title || 'Film project')}: summary</title>\n<style>${css}</style>\n</head>\n<body>\n<main>\n<h1>${esc(p.title || 'Film project')}</h1>\n<p class="meta">${esc([p.company, p.producer && `produced by ${p.producer}`].filter(Boolean).join(', '))}</p>\n<p class="meta">Summary made ${esc(made)}. Read-only: this page doesn't change the project.</p>\n${body}\n<footer>Made with the Open Filmmaker Toolkit. ${o.contacts || o.notes || o.fees ? `Includes ${[o.contacts && 'contact details', o.notes && 'notes', o.fees && 'fees'].filter(Boolean).join(', ')}.` : 'Contact details, notes and fees are left out.'}</footer>\n</main>\n</body>\n</html>\n`;
  }
  // ---------- The calendar dialog, used by the home page and the tools ----------
  function saveText(text, name, type) {
    const url = URL.createObjectURL(new Blob([text], { type }));
    const a = document.createElement('a'); a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  const stem = d => (str((d.project || {}).title).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'project');
  function calendarDialog(getData) {
    let dlg = document.getElementById('oftCalDialog');
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.id = 'oftCalDialog'; dlg.className = 'oft-dialog'; dlg.setAttribute('aria-labelledby', 'oftCalTitle');
      dlg.innerHTML = `<form method="dialog" id="oftCalForm"><h2 id="oftCalTitle">Add every date to your calendar</h2>
        <p>One calendar file with the dates from every tool. Import it into Google Calendar, Apple Calendar or Outlook. Importing a newer file updates the same events instead of adding them twice.</p>
        <fieldset class="oft-kinds"><legend>Dates to include</legend>${KINDS.map(([k, label]) => `<label><input type="checkbox" name="kind" value="${k}" checked> <span>${esc(label)} <small data-count="${k}"></small></span></label>`).join('')}</fieldset>
        <p id="oftCalNote" class="oft-changed" aria-live="polite"></p>
        <div class="oft-actions"><button type="button" class="btn" id="oftCalCancel">Cancel</button><button type="submit" class="btn primary" id="oftCalSave">Download the calendar file</button></div></form>`;
      document.body.append(dlg);
      dlg.querySelector('#oftCalCancel').onclick = () => dlg.close();
      dlg.querySelector('#oftCalForm').addEventListener('submit', ev => {
        const d = getData(), kinds = [...dlg.querySelectorAll('input[name="kind"]:checked')].map(x => x.value);
        if (!kinds.length) { ev.preventDefault(); dlg.querySelector('#oftCalNote').textContent = 'Choose at least one kind of date.'; return; }
        const out = ics(d, kinds);
        saveText(out.text, `${stem(d)}-dates.ics`, 'text/calendar');
      });
    }
    const d = getData(), all = dates(d);
    for (const [k] of KINDS) { const n = all.filter(e => e.kind === k).length; dlg.querySelector(`[data-count="${k}"]`).textContent = `(${n})`; }
    dlg.querySelector('#oftCalNote').textContent = all.length ? '' : 'There are no dates in this project yet.';
    dlg.showModal();
  }
  return { TOOLS, KINDS, PARTS, CONTACT, flags, glance, dates, ics, summary, today, addDays, fmt, calendarDialog, saveText, stem };
})();
