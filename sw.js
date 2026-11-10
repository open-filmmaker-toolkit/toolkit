// Keeps the toolkit working without an internet connection once it has been opened from the web.
// It only handles the toolkit's own pages: each one is fetched fresh while you're online and a copy is
// kept, and the kept copy is used when you're offline. Your project file is never sent anywhere.
// The list of pages is kept up to date by .github/scripts/sync_shared.py.
const CACHE = 'oft-pages-v1';
const PAGES = [
  // oft-pages begin
  './',
  'index.html',
  'manifest.webmanifest',
  'docs/assets/icon.svg',
  'docs/assets/icon-192.png',
  'docs/assets/icon-512.png',
  'tools/archive-log/index.html',
  'tools/awards-social/index.html',
  'tools/bookings/index.html',
  'tools/budget/index.html',
  'tools/budget-converter/index.html',
  'tools/budget-to-actuals/index.html',
  'tools/call-sheet/index.html',
  'tools/camera-sound-reports/index.html',
  'tools/cash-flow/index.html',
  'tools/chain-of-title/index.html',
  'tools/clearance-log/index.html',
  'tools/clearance-report/index.html',
  'tools/coi-permit-tracker/index.html',
  'tools/comps-tracker/index.html',
  'tools/contract-archive/index.html',
  'tools/credits-builder/index.html',
  'tools/cut-tracker/index.html',
  'tools/daily-production-report/index.html',
  'tools/day-out-of-days/index.html',
  'tools/deal-memos/index.html',
  'tools/deliverables/index.html',
  'tools/discussion-guide/index.html',
  'tools/expense-log/index.html',
  'tools/fair-use-log/index.html',
  'tools/festival-strategy/index.html',
  'tools/festival-submissions/index.html',
  'tools/field-journal/index.html',
  'tools/final-cost-report/index.html',
  'tools/finance-plan/index.html',
  'tools/footage-log/index.html',
  'tools/funder-crm/index.html',
  'tools/gear-list/index.html',
  'tools/grant-calendar/index.html',
  'tools/grant-reports/index.html',
  'tools/impact-report/index.html',
  'tools/interview-log/index.html',
  'tools/interview-prep/index.html',
  'tools/license-tracker/index.html',
  'tools/location-scout/index.html',
  'tools/music-cue-sheet/index.html',
  'tools/name-supers/index.html',
  'tools/narrative-library/index.html',
  'tools/paper-edit/index.html',
  'tools/partner-crm/index.html',
  'tools/people/index.html',
  'tools/pitch-deck/index.html',
  'tools/press-list/index.html',
  'tools/press-notes/index.html',
  'tools/qc-tracker/index.html',
  'tools/release-tracker/index.html',
  'tools/research-log/index.html',
  'tools/revenue-tracker/index.html',
  'tools/rights-matrix/index.html',
  'tools/risk-plan/index.html',
  'tools/screening-kit/index.html',
  'tools/script-breakdown/index.html',
  'tools/security-checklist/index.html',
  'tools/shooting-calendar/index.html',
  'tools/shot-list/index.html',
  'tools/sides/index.html',
  'tools/stills-library/index.html',
  'tools/stripboard/index.html',
  'tools/structure-board/index.html',
  'tools/subject-tracker/index.html',
  'tools/theory-of-change/index.html',
  'tools/travel-sheet/index.html',
  'tools/treatment-builder/index.html',
  'tools/waterfall/index.html',
  'samples/shared-festival-list.json',
  'samples/shared-funder-list.json',
  'samples/the-river-keeps-reenactments.fountain',
  'samples/the-river-keeps.oft.json',
  // oft-pages end
];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(PAGES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith('oft-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// The newest copy when online; the kept copy when the network can't be reached or takes too long.
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const kept = () => cache.match(req, { ignoreSearch: true });
    try {
      const fresh = await Promise.race([fetch(req), new Promise((_, no) => setTimeout(() => no(new Error('slow')), 6000))]);
      if (fresh && fresh.ok && fresh.type === 'basic') cache.put(req, fresh.clone());
      return fresh;
    } catch (err) {
      const copy = await kept();
      if (copy) return copy;
      if (req.mode === 'navigate') { const home = await cache.match(new URL('index.html', self.registration.scope).href); if (home) return home; }
      throw err;
    }
  })());
});
