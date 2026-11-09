// Runs before every toolkit page in the desktop app. The tools already save through the browser's file picker
// (showOpenFilePicker and showSaveFilePicker), which Chrome and Edge have and Safari and Firefox don't. This gives
// them that picker, backed by the app's own file access, so the tools work unchanged and save back to your file.
// It also turns downloads into a save dialog, and opens web links in your browser instead of in the app.
(() => {
  if (window.__oftDesktop) return;
  window.__oftDesktop = true;
  const T = () => window.__TAURI__;
  const baseName = p => String(p).split(/[\\/]/).pop();
  const aborted = () => new DOMException('The user aborted a request.', 'AbortError');
  // The picker's file types, in the form the app's dialogs take.
  const filters = types => (types || []).map(t => ({
    name: t.description || 'Files',
    extensions: Object.values(t.accept || {}).flat().map(e => String(e).replace(/^\./, '')).filter(Boolean)
  })).filter(f => f.extensions.length);

  // A file you picked. Like the browser's own file handles, it can be kept in IndexedDB; the tools turn it back
  // into a handle with window.oftDesktopHandle (see oftIdb in shared/tool.js).
  class DesktopFileHandle {
    constructor(path) { this.kind = 'file'; this.name = baseName(path); this.oftPath = path; }
    async getFile() {
      const bytes = await T().fs.readFile(this.oftPath);
      let modified = Date.now();
      try { const s = await T().fs.stat(this.oftPath); if (s && s.mtime) modified = new Date(s.mtime).getTime(); } catch { /* use now */ }
      return new File([bytes], this.name, { lastModified: modified });
    }
    async createWritable() {
      const parts = [];
      const path = this.oftPath;
      return {
        async write(data) {
          if (data && typeof data === 'object' && data.type === 'write' && 'data' in data) data = data.data;
          parts.push(data);
        },
        async close() { await T().fs.writeFile(path, new Uint8Array(await new Blob(parts).arrayBuffer())); },
        async abort() { parts.length = 0; }
      };
    }
    async queryPermission() { return 'granted'; }
    async requestPermission() { return 'granted'; }
    async isSameEntry(other) { return !!other && other.oftPath === this.oftPath; }
  }
  window.oftDesktopHandle = path => new DesktopFileHandle(path);

  window.showOpenFilePicker = async (opts = {}) => {
    const picked = await T().dialog.open({ multiple: !!opts.multiple, directory: false, filters: filters(opts.types) });
    if (!picked) throw aborted();
    return [].concat(picked).map(p => new DesktopFileHandle(typeof p === 'string' ? p : p.path));
  };
  window.showSaveFilePicker = async (opts = {}) => {
    const path = await T().dialog.save({ defaultPath: opts.suggestedName, filters: filters(opts.types) });
    if (!path) throw aborted();
    return new DesktopFileHandle(path);
  };

  // Downloads: exports, printouts saved as files and the like. The app asks where to save each one.
  const pending = new Set();
  const revoke = URL.revokeObjectURL.bind(URL);
  URL.revokeObjectURL = url => { if (pending.has(url)) setTimeout(() => URL.revokeObjectURL(url), 1000); else revoke(url); };
  async function saveDownload(href, name) {
    pending.add(href);
    let bytes;
    try { bytes = new Uint8Array(await (await fetch(href)).arrayBuffer()); } finally { pending.delete(href); }
    const ext = (name.match(/\.([a-z0-9]+)$/i) || [])[1];
    const path = await T().dialog.save({ defaultPath: name, filters: ext ? [{ name: ext.toUpperCase(), extensions: [ext] }] : [] });
    if (path) await T().fs.writeFile(path, bytes);
  }
  const isDownload = a => a && a.hasAttribute('download') && /^(blob|data):/.test(a.href);
  const click = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (isDownload(this)) { saveDownload(this.href, this.getAttribute('download') || 'download').catch(e => console.error(e)); return; }
    return click.call(this);
  };

  // Printing. On a Mac the app's browser engine has no window.print of its own; Tauri supplies one that opens the
  // print dialog, but the page isn't told it's about to print. Most tools build their printout when told
  // (the beforeprint event), so tell them first. Linux and Windows print the usual way.
  if (/Macintosh/.test(navigator.userAgent)) {
    const print = () => {
      window.dispatchEvent(new Event('beforeprint'));
      return window.__TAURI_INTERNALS__.invoke('plugin:webview|print').catch(e => console.error(e));
    };
    Object.defineProperty(window, 'print', { configurable: true, get: () => print, set: () => {} });
  }

  // Links: web addresses open in your browser. Pages of the toolkit open in this window.
  const openOutside = url => T().opener.openUrl(url).catch(e => console.error(e));
  document.addEventListener('click', ev => {
    if (ev.defaultPrevented || ev.button !== 0) return;
    const a = ev.target.closest && ev.target.closest('a[href]');
    if (!a) return;
    if (isDownload(a)) { ev.preventDefault(); saveDownload(a.href, a.getAttribute('download') || 'download').catch(e => console.error(e)); return; }
    if (/^(https?|mailto):/.test(a.href) && new URL(a.href).origin !== window.location.origin) { ev.preventDefault(); openOutside(a.href); }
  }, true);
  const open = window.open.bind(window);
  window.open = (url, target, features) => {
    let u;
    try { u = new URL(url, window.location.href); } catch { return open(url, target, features); }
    if (/^(https?|mailto):$/.test(u.protocol) && u.origin !== window.location.origin) { openOutside(u.href); return null; }
    // A scan or other file the page made: save it, since the app has no second browser tab to show it in.
    if (u.protocol === 'blob:' || u.protocol === 'data:') { saveDownload(u.href, 'file').catch(e => console.error(e)); return null; }
    window.location.href = u.href;
    return null;
  };
})();
