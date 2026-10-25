"""Real-browser checks for all three tools.

Run: pip install playwright pypdf && playwright install chromium firefox webkit
     python tests/browser_tools.py [chromium|firefox|webkit]   (default: chromium)

Checks, per tool: opening the sample, saving, all CSV exports, phone width, dark
mode and print layout. Chromium also covers the save-conflict warning (it has the
file picker API; its handles are faked in memory) and renders a real PDF.
Firefox and WebKit (Safari's engine) use the download/upload fallback instead.
"""
import csv, io, json, pathlib, sys
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[1]
sample = (root / 'samples/the-river-keeps.oft.json').read_text()
TOOLS = ['clearance-log', 'music-cue-sheet', 'call-sheet']
COLLECTIONS = ['project', 'people', 'locations', 'thirdPartyElements', 'contracts', 'assets', 'musicCueSheet', 'callSheets']
PRINT_BTN = {'clearance-log': '#printBtn', 'music-cue-sheet': '#printBtn', 'call-sheet': '#printAllBtn'}
PHONE = {'width': 390, 'height': 844}

STUB_PRINT = 'window.print = () => { window.__printed = true; };'
FAKE_PICKERS = """
window.__file = {name:'proj.oft.json', text: %s};
window.__writes = 0;
const mk = () => ({name: window.__file.name,
  getFile: async () => ({text: async () => window.__file.text, name: window.__file.name}),
  createWritable: async () => { let buf=''; return {write: async d => {buf += d;}, close: async () => {window.__file.text = buf; window.__writes++;}}; },
  queryPermission: async()=>'granted', requestPermission: async()=>'granted'});
window.showOpenFilePicker = async () => [mk()];
window.showSaveFilePicker = async () => mk();
""" % json.dumps(sample)

fails = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        fails.append(msg)

def luminance(rgb):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(rgb[0]) + 0.7152 * ch(rgb[1]) + 0.0722 * ch(rgb[2])

def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)

# Resolves real text and background colors, walking up through transparent layers.
COLORS_JS = """() => {
  const c = document.createElement('canvas').getContext('2d');
  const rgb = v => { c.clearRect(0,0,1,1); c.fillStyle = '#000'; c.fillStyle = v; c.fillRect(0,0,1,1); const d = c.getImageData(0,0,1,1).data; return [d[0],d[1],d[2],d[3]/255]; };
  const bg = el => { for (let e = el; e; e = e.parentElement) { const v = rgb(getComputedStyle(e).backgroundColor); if (v[3] > 0.99) return v.slice(0,3); } return [255,255,255]; };
  const pairs = {};
  for (const [k, sel] of Object.entries({page: 'body', heading: 'h1', button: '.btn:not(.primary):not(.danger)', primary: '.btn.primary'})) {
    const el = document.querySelector(sel);
    if (el && (sel === 'body' || el.offsetParent !== null)) pairs[k] = [rgb(getComputedStyle(el).color).slice(0,3), bg(el)];
  }
  return pairs;
}"""

def new_page(browser, name, fake, **ctx):
    context = browser.new_context(accept_downloads=True, **ctx)
    page = context.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.add_init_script(STUB_PRINT + (FAKE_PICKERS if fake else ''))
    page.goto('file://%s/tools/%s/index.html' % (root, name))
    page.wait_for_load_state('networkidle')
    return context, page, errs

def open_sample(page, fake):
    if fake:
        page.click('#openBtn')
    else:
        page.set_input_files('#fileInput', files=[{'name': 'proj.oft.json', 'mimeType': 'application/json', 'buffer': sample.encode()}])
    page.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")

def horizontal_overflow(page):
    return page.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')

def test_core(browser, name, fake):
    ctx, pg, errs = new_page(browser, name, fake)
    open_sample(pg, fake)
    check('River' in pg.inner_text('#filmTitle'), 'sample opens')
    for col in COLLECTIONS:
        pg.click('#projectCsvBtn')
        pg.select_option('#projectCsvCollection', col)
        with pg.expect_download() as d:
            pg.click('#projectCsvForm button[type=submit]')
        text = open(d.value.path(), encoding='utf-8-sig').read()
        check(d.value.suggested_filename.endswith('-%s.csv' % col) and len(list(csv.reader(io.StringIO(text)))) >= 1, 'csv export %s' % col)
    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == 1 and not pg.is_visible('#conflictDialog'), 'clean save writes, no conflict')
        ext = json.loads(pg.evaluate('window.__file.text')); ext['project']['title'] = 'CHANGED EXTERNALLY'
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        check(pg.is_visible('#conflictDialog') and 'CHANGED EXTERNALLY' in pg.evaluate('window.__file.text'), 'conflict warns and leaves the file alone')
        pg.click('#conflictCancelBtn')
        check(not pg.is_visible('#conflictDialog'), 'keep editing closes the dialog')
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        writes = pg.evaluate('window.__writes')
        pg.click('#conflictOverwriteBtn'); pg.wait_for_timeout(300)
        check(pg.evaluate('window.__writes') == writes + 1 and 'CHANGED EXTERNALLY' not in pg.evaluate('window.__file.text'), 'overwrite replaces the file')
        pg.evaluate('t => window.__file.text = t', json.dumps(ext))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        pg.click('#conflictReloadBtn'); pg.wait_for_timeout(300)
        check('CHANGED EXTERNALLY' in pg.content(), 'reload latest shows the newer file')
        pg.evaluate('t => window.__file.text = t', json.dumps(dict(ext, project=dict(ext['project'], title='AGAIN'))))
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        with pg.expect_download() as d:
            pg.click('#conflictCopyBtn')
        check(d.value.suggested_filename.endswith('.json'), 'save a copy downloads')
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        saved = json.loads(open(d.value.path(), encoding='utf-8').read())
        check(saved.get('project', {}).get('title') == 'The River Keeps', 'save downloads the project file')
        pg.set_input_files('#fileInput', files=[{'name': 'again.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(saved).encode()}])
        pg.wait_for_timeout(300)
        check('River' in pg.inner_text('#filmTitle'), 'saved file reopens')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_phone(browser, name, fake):
    ctx, pg, errs = new_page(browser, name, fake, viewport=PHONE)
    check(horizontal_overflow(pg) <= 1, 'phone: empty state does not scroll sideways')
    open_sample(pg, fake)
    check(horizontal_overflow(pg) <= 1, 'phone: loaded project does not scroll sideways (%spx over)' % horizontal_overflow(pg))
    for sel in ['#saveBtn', '#openBtn']:
        box = pg.locator(sel).bounding_box()
        check(box is not None and box['x'] >= 0 and box['x'] + box['width'] <= PHONE['width'] + 1, 'phone: %s fits on screen' % sel)
    pg.click('#addBtn'); pg.wait_for_timeout(300)
    box = pg.locator('dialog[open]').first.bounding_box()
    check(box is not None and box['x'] >= 0 and box['x'] + box['width'] <= PHONE['width'] + 1, 'phone: editor fits on screen')
    check(horizontal_overflow(pg) <= 1, 'phone: editor does not scroll the page sideways')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_dark(browser, name, fake):
    for scheme in ['light', 'dark']:
        ctx, pg, errs = new_page(browser, name, fake, color_scheme=scheme)
        open_sample(pg, fake)
        pairs = pg.evaluate(COLORS_JS)
        page_bg = pairs['page'][1]
        if scheme == 'dark':
            check(luminance(page_bg) < 0.2, 'dark mode: page background is dark %s' % page_bg)
        else:
            check(luminance(page_bg) > 0.6, 'light mode: page background is light %s' % page_bg)
        for k, (fg, bg) in pairs.items():
            ratio = contrast(fg, bg)
            check(ratio >= 4.5, '%s mode: %s text contrast %.1f:1' % (scheme, k, ratio))
        ctx.close()

def test_print(browser, name, fake, can_pdf):
    ctx, pg, errs = new_page(browser, name, fake)
    open_sample(pg, fake)
    pg.click(PRINT_BTN[name]); pg.wait_for_timeout(300)
    check(pg.evaluate('window.__printed === true'), 'print dialog is requested')
    pg.emulate_media(media='print')
    check(pg.is_visible('#report') and not pg.is_visible('.page'), 'print view shows only the report')
    check('The River Keeps' in pg.inner_text('#report'), 'report names the film')
    if can_pdf:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(pg.pdf(prefer_css_page_size=True)))
        pdf_text = ' '.join(p.extract_text() or '' for p in reader.pages)
        check(len(reader.pages) >= 1 and 'The River Keeps' in pdf_text, 'PDF renders %d page(s) with the film title' % len(reader.pages))
        if name == 'call-sheet':
            days = len(json.loads(sample)['callSheets'])
            check(len(reader.pages) == days, 'PDF has one page per shoot day (%d)' % days)
            check('General call' in pdf_text and '7:00' in pdf_text, 'PDF has the call time')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_call_sheet_export(browser, fake):
    ctx, pg, errs = new_page(browser, 'call-sheet', fake)
    open_sample(pg, fake)
    with pg.expect_download() as d:
        pg.click('#sheetCsvBtn')
    txt = open(d.value.path(), encoding='utf-8-sig').read()
    check(txt.startswith('CALL SHEET') and 'CREW AND CAST' in txt, 'all-days spreadsheet export')
    template = (root / 'templates/call-sheet-template.csv').read_text()
    keep = ('CALL SHEET', 'SCHEDULE', 'CREW AND CAST', 'NOTES', 'Film', 'General call', 'Nearest hospital', 'Time', 'Name', 'Prepared by')
    skeleton = lambda t: [r[0] for r in csv.reader(io.StringIO(t)) if r and r[0] in keep]
    check(skeleton(template) == skeleton(txt), 'export layout matches the blank template')
    pg.locator('[data-id]').first.click(); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#sheetCsvDayBtn')
    check('-call-sheet-' in d.value.suggested_filename, 'single-day spreadsheet export')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def main():
    engine = sys.argv[1] if len(sys.argv) > 1 else 'chromium'
    fake = engine == 'chromium'
    with sync_playwright() as p:
        browser = getattr(p, engine).launch(headless=True)
        print('#### %s %s' % (engine, browser.version))
        for name in TOOLS:
            for label, fn in [('core', lambda: test_core(browser, name, fake)), ('phone', lambda: test_phone(browser, name, fake)),
                              ('dark mode', lambda: test_dark(browser, name, fake)), ('print', lambda: test_print(browser, name, fake, fake))]:
                print('== %s / %s' % (name, label))
                fn()
        print('== call-sheet / spreadsheet export')
        test_call_sheet_export(browser, fake)
        browser.close()
    print('FAILS', fails)
    sys.exit(1 if fails else 0)

main()
