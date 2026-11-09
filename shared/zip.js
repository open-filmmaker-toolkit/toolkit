// Writing a .zip file in the browser, so a tool can hand over a folder of files as one download.
// Files are stored without compression: photos and PDFs are compressed already, and it keeps this small.
// oftZip.make([{ name: 'folder/file.txt', data: string | Uint8Array | ArrayBuffer, date?: Date }]) returns a Blob.
const oftZip = (() => {
  let table = null;
  function crc32(b) {
    if (!table) { table = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; table[n] = c >>> 0; } }
    let c = 0xffffffff;
    for (let i = 0; i < b.length; i++) c = table[(c ^ b[i]) & 0xff] ^ (c >>> 8);
    return (c ^ 0xffffffff) >>> 0;
  }
  const bytes = d => (typeof d === 'string' ? new TextEncoder().encode(d) : d instanceof Uint8Array ? d : new Uint8Array(d));
  function dosTime(d) {
    const t = (d.getHours() << 11) | (d.getMinutes() << 5) | Math.floor(d.getSeconds() / 2);
    const day = ((Math.max(1980, d.getFullYear()) - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
    return [t, day];
  }
  function make(files) {
    const parts = [], central = [];
    let offset = 0;
    const seen = new Set();
    for (const f of files) {
      // Two files can't share a name in a zip, so a repeat gets a number.
      let name = String(f.name).replace(/\\/g, '/').replace(/^\/+/, '');
      if (seen.has(name)) { const m = /^(.*?)(\.[^./]*)?$/.exec(name); let i = 2; while (seen.has(`${m[1]}-${i}${m[2] || ''}`)) i++; name = `${m[1]}-${i}${m[2] || ''}`; }
      seen.add(name);
      const data = bytes(f.data), nm = new TextEncoder().encode(name), crc = crc32(data), [time, day] = dosTime(f.date || new Date());
      const local = new DataView(new ArrayBuffer(30));
      [[0, 0x04034b50, 4], [4, 20, 2], [6, 0x0800, 2], [8, 0, 2], [10, time, 2], [12, day, 2], [14, crc, 4], [18, data.length, 4], [22, data.length, 4], [26, nm.length, 2], [28, 0, 2]]
        .forEach(([at, v, n]) => (n === 4 ? local.setUint32(at, v, true) : local.setUint16(at, v, true)));
      parts.push(local.buffer, nm, data);
      const c = new DataView(new ArrayBuffer(46));
      [[0, 0x02014b50, 4], [4, 20, 2], [6, 20, 2], [8, 0x0800, 2], [10, 0, 2], [12, time, 2], [14, day, 2], [16, crc, 4], [20, data.length, 4], [24, data.length, 4], [28, nm.length, 2], [30, 0, 2], [32, 0, 2], [34, 0, 2], [36, 0, 2], [38, 0, 4], [42, offset, 4]]
        .forEach(([at, v, n]) => (n === 4 ? c.setUint32(at, v, true) : c.setUint16(at, v, true)));
      central.push(c.buffer, nm);
      offset += 30 + nm.length + data.length;
    }
    const size = central.reduce((n, p) => n + p.byteLength, 0);
    const end = new DataView(new ArrayBuffer(22));
    [[0, 0x06054b50, 4], [4, 0, 2], [6, 0, 2], [8, seen.size, 2], [10, seen.size, 2], [12, size, 4], [16, offset, 4], [20, 0, 2]]
      .forEach(([at, v, n]) => (n === 4 ? end.setUint32(at, v, true) : end.setUint16(at, v, true)));
    return new Blob([...parts, ...central, end.buffer], { type: 'application/zip' });
  }
  return { make, crc32 };
})();
