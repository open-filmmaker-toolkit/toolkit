// Offline use: when a page is opened from the toolkit's web address, the browser keeps a copy of every tool
// (see sw.js at the top of the repo), so the toolkit opens without an internet connection. A page opened
// as a file on your computer already works offline and doesn't need this.
const oftOffline = (() => {
  const can = 'serviceWorker' in navigator && window.isSecureContext && /^https?:$/.test(window.location.protocol);
  const root = new URL(document.querySelector('.home-link') ? '../../' : './', window.location.href);
  const ready = can ? navigator.serviceWorker.register(new URL('sw.js', root), { scope: root.pathname }).then(() => navigator.serviceWorker.ready).catch(() => null) : Promise.resolve(null);
  return { can, ready };
})();
