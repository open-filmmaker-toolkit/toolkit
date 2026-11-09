// Browsers that can't save back to the file. Chrome, Edge, Brave and Arc on a computer save straight back to the
// project file. Other browsers download a new copy each time, so the toolkit says so, with the setting that lets
// you save over the same file. The tools show it once; the home page shows it in the Start here box.
const OFT_NOTE_DONE = 'oft-browser-note-done';
function oftBrowserNote() {
  const ua = navigator.userAgent || '';
  const phone = /iPhone|iPad|iPod|Android/.test(ua) || (navigator.maxTouchPoints > 1 && /Macintosh/.test(ua));
  const tip = phone ? 'On a phone or tablet, keep the newest copy and delete the older ones.'
    : /Firefox\//.test(ua) ? 'To keep one file, turn on <b>Always ask you where to save files</b> in Firefox\'s settings, under General, then Files and Applications. Then save over the same file each time.'
    : /Safari\//.test(ua) && !/Chrome|Chromium|Edg\//.test(ua) ? 'To keep one file, set <b>File download location</b> to <b>Ask for each download</b> in Safari\'s settings, under General. Then save over the same file each time.'
    : 'To keep one file, set this browser to ask where to save each download. Then save over the same file each time.';
  return `<b>This browser saves a new copy each time.</b> Chrome, Edge, Brave and Arc on a computer save straight back to your project file. Here, each save downloads a new copy. ${tip}`;
}
