"""Real-browser checks for every tool.

Run: pip install playwright pypdf && playwright install chromium
     python tests/browser_tools.py [chromium|chromium-fallback|firefox|webkit]   (default: chromium)

CI runs chromium and chromium-fallback. chromium-fallback is Chromium with the file
picker API removed, so it takes the download/upload path Firefox and Safari use.
Firefox and WebKit still work locally (playwright install firefox webkit).

Checks, per tool: opening the sample, saving, all CSV exports, phone width, dark
mode and print layout. Chromium also covers the save-conflict warning (it has the
file picker API; its handles are faked in memory) and renders a real PDF.
chromium-fallback, Firefox and WebKit (Safari's engine) use the download/upload fallback instead.
The call sheet, release tracker, credits builder, name supers list, subject tracker, research and archival log, comps tracker, treatment builder, pitch deck builder and archive log also get end-to-end checks
of their own, and the spreadsheet templates are checked against the tools' exports.
"""
import base64, datetime, csv, io, json, os, pathlib, re, sys, tempfile
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parents[1]
sample = (root / 'samples/the-river-keeps.oft.json').read_text()
TOOLS = ['clearance-log', 'music-cue-sheet', 'call-sheet', 'release-tracker', 'credits-builder', 'name-supers', 'subject-tracker', 'research-log', 'comps-tracker', 'treatment-builder', 'pitch-deck', 'grant-calendar', 'narrative-library', 'budget', 'budget-converter', 'finance-plan', 'funder-crm', 'cash-flow', 'shooting-calendar', 'interview-prep', 'field-journal', 'location-scout', 'deal-memos', 'gear-list', 'coi-permit-tracker', 'travel-sheet', 'risk-plan', 'security-checklist', 'camera-sound-reports', 'interview-log', 'daily-production-report', 'expense-log', 'festival-submissions', 'press-list', 'partner-crm', 'discussion-guide', 'archive-log', 'footage-log', 'paper-edit', 'structure-board', 'cut-tracker', 'budget-to-actuals', 'fair-use-log', 'license-tracker', 'clearance-report', 'chain-of-title', 'festival-strategy', 'press-notes', 'stills-library', 'awards-social', 'rights-matrix', 'deliverables', 'qc-tracker', 'waterfall', 'revenue-tracker', 'bookings']
COLLECTIONS = ['project', 'people', 'locations', 'thirdPartyElements', 'contracts', 'assets', 'musicCueSheet', 'callSheets']
PRINT_BTN = {'bookings': '#printBtn', 'revenue-tracker': '#printBtn', 'waterfall': '#printBtn', 'qc-tracker': '#printBtn', 'deliverables': '#printBtn', 'rights-matrix': '#printBtn', 'awards-social': '#printBtn', 'stills-library': '#printBtn', 'press-notes': '#printBtn', 'festival-strategy': '#printBtn', 'clearance-log': '#printBtn', 'music-cue-sheet': '#printBtn', 'call-sheet': '#printAllBtn', 'release-tracker': '#printBtn',
             'credits-builder': '#printBtn', 'name-supers': '#printBtn', 'subject-tracker': '#printBtn', 'research-log': '#printBtn', 'comps-tracker': '#printBtn', 'treatment-builder': '#printBtn', 'pitch-deck': '#printBtn', 'grant-calendar': '#printBtn', 'narrative-library': '#printBtn', 'budget': '#printBtn', 'budget-converter': '#printBtn', 'finance-plan': '#printBtn', 'funder-crm': '#printBtn', 'cash-flow': '#printBtn', 'shooting-calendar': '#printBtn', 'interview-prep': '#printBtn', 'field-journal': '#printBtn', 'location-scout': '#printBtn', 'deal-memos': '#printBtn', 'gear-list': '#printBtn', 'coi-permit-tracker': '#printBtn', 'travel-sheet': '#printBtn', 'risk-plan': '#printBtn', 'security-checklist': '#printBtn', 'camera-sound-reports': '#printBtn', 'interview-log': '#printBtn', 'daily-production-report': '#printBtn', 'expense-log': '#printBtn', 'festival-submissions': '#printBtn', 'press-list': '#printBtn', 'partner-crm': '#printBtn', 'discussion-guide': '#printBtn', 'archive-log': '#printBtn', 'footage-log': '#printBtn', 'paper-edit': '#printBtn', 'structure-board': '#printBtn', 'cut-tracker': '#printBtn', 'budget-to-actuals': '#printBtn', 'fair-use-log': '#printBtn', 'license-tracker': '#printBtn', 'clearance-report': '#printBtn', 'chain-of-title': '#printBtn'}
PHONE = {'width': 390, 'height': 844}
# The button that opens each tool's main dialog, for the phone-width check. Most tools use #addBtn.
DIALOG_BTN = {'stills-library': '[data-edit]', 'treatment-builder': '[data-compare]', 'cash-flow': '#settingsBtn', 'discussion-guide': '#projectCsvBtn'}

STUB_PRINT = 'window.print = () => { window.__printed = true; };'
NO_PICKERS = 'delete window.showOpenFilePicker; delete window.showSaveFilePicker; delete window.showDirectoryPicker;'
FALLBACK = False
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

def new_page(browser, name, fake, extra='', **ctx):
    context = browser.new_context(accept_downloads=True, **ctx)
    page = context.new_page()
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)))
    page.add_init_script(STUB_PRINT + (NO_PICKERS if FALLBACK else '') + (FAKE_PICKERS if fake else '') + extra)
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
    pg.locator(DIALOG_BTN.get(name, '#addBtn')).first.click(); pg.wait_for_timeout(300)
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

# A project folder in memory, for the release tracker's "Connect project folder" (Chromium only).
FAKE_DIR = """
window.__dir = {'proj.oft.json': ''};
const fsFile = path => ({name: path.split('/').pop(), isSameEntry: async () => true,
  getFile: async () => new File([window.__dir[path]], path.split('/').pop()),
  createWritable: async () => { const parts = []; return {write: async d => { parts.push(d); }, close: async () => { window.__dir[path] = await new Blob(parts).text(); }}; }});
const fsDir = (prefix, name) => ({name,
  getDirectoryHandle: async n => fsDir(prefix + n + '/', n),
  getFileHandle: async (n, o) => { const path = prefix + n; if (!(path in window.__dir)) { if (o && o.create) window.__dir[path] = ''; else throw new DOMException('Not found', 'NotFoundError'); } return fsFile(path); }});
window.showDirectoryPicker = async () => fsDir('', 'River Keeps');
"""

def test_release_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'release-tracker', fake, extra=FAKE_DIR if fake else '')
    open_sample(pg, fake)
    check(pg.inner_text('#covHeadline') == '2 of 7 covered', 'coverage counts the sample (%s)' % pg.inner_text('#covHeadline'))
    missing = pg.locator('.cov-line.is-missing').all_inner_texts()
    check(any('Marcus Bell' in t for t in missing) and any('Riverside levee' in t for t in missing), 'flags a person and a location with no release on file')
    check('Riverside levee' in pg.inner_text('#placesCov'), 'a location on a call sheet counts as filmed')

    # Start a release from a flagged person, sign it and attach a scan.
    pg.click('#peopleCov .is-missing:has-text("Marcus Bell") .cov-sig')
    check(pg.is_visible('#editor') and pg.input_value('#f-type') == 'appearance release', 'flagged person opens a new appearance release')
    check(pg.eval_on_selector_all('#peopleList input:checked', 'els => els.map(e => e.value)') == ['person-marcus-bell'], 'the flagged person is already checked')
    pg.select_option('#f-status', 'signed')
    check(len(pg.input_value('#f-signedDate')) == 10, 'marking it signed fills in today')
    if fake:
        pg.click('#connectFolderBtn'); pg.wait_for_timeout(200)
        check('River Keeps' in pg.inner_text('#folderNote'), 'project folder connects')
    pg.set_input_files('#scanInput', files=[{'name': 'marcus-release.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 fake'}])
    check('marcus-release.pdf' in pg.inner_text('#scanList'), 'attached scan is listed')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)
    check(not pg.is_visible('#editor'), 'saving closes the editor')
    check('is-covered' in pg.get_attribute('#peopleCov .cov-line:has-text("Marcus Bell")', 'class'), 'person is now covered')
    if fake:
        check(pg.evaluate("window.__dir['releases/marcus-release.pdf']") == '%PDF-1.4 fake', 'scan is copied into the releases folder')

    # Decline a pending release.
    pg.click('#peopleCov .cov-line:has-text("Leon Pryor") .cov-sig')
    pg.select_option('#f-status', 'declined')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('is-declined' in pg.get_attribute('#peopleCov .cov-line:has-text("Leon Pryor")', 'class'), 'declined release is flagged')

    # Take someone off camera.
    pg.click('#onCameraBtn')
    pg.uncheck('#ocPeople input[value="person-daniel-okafor"]')
    pg.click('#onCameraForm button[type=submit]'); pg.wait_for_timeout(200)
    check('Daniel Okafor' not in pg.inner_text('#peopleCov'), 'unchecked person leaves the on-camera list')

    # A materials release links to clearance log items, and deleting it unlinks them.
    pg.click('#addBtn')
    pg.select_option('#f-type', 'materials release')
    pg.fill('#f-title', 'Temporary materials release')
    pg.check('#elementsList input[value="sample-01"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.select_option('#statusFilter', 'pending')
    check(pg.locator('#rows tr[data-id]').count() >= 1, 'status filter shows matching releases')
    pg.select_option('#statusFilter', 'all')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rel_csv = open(d.value.path(), encoding='utf-8-sig').read()
    check('Marcus Bell' in rel_csv and 'Temporary materials release' in rel_csv, 'releases CSV lists the new releases')

    def saved_project():
        if fake:
            pg.click('#saveBtn'); pg.wait_for_timeout(300)
            return json.loads(pg.evaluate('window.__file.text'))
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        return json.loads(open(d.value.path(), encoding='utf-8').read())

    data = saved_project()
    temp = next(c for c in data['contracts'] if c['title'] == 'Temporary materials release')
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-01')
    check(temp['id'] in el.get('contractIds', []), 'materials release is recorded on the clearance log item')
    marcus = next(c for c in data['contracts'] if 'person-marcus-bell' in c.get('personIds', []))
    scan = next(a for a in data['assets'] if a['id'] in marcus.get('assetIds', []))
    check(marcus['status'] == 'signed' and scan['type'] == 'release scan' and scan['relativePath'] == 'releases/marcus-release.pdf', 'saved release has its scan as an asset')
    people = {p['id']: p for p in data['people']}
    check(people['person-daniel-okafor'].get('onCamera') is False and people['person-marcus-bell'].get('onCamera') is True, 'on-camera choices are saved')
    original = json.loads(sample)
    music = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-03')
    check(music.get('music') == next(e for e in original['thirdPartyElements'] if e['id'] == 'sample-03')['music']
          and data.get('callSheets') == original['callSheets'] and data.get('musicCueSheet') == original['musicCueSheet'], 'other tools\' data is unchanged')

    pg.click('#rows tr:has-text("Temporary materials release") .el-name')
    pg.once('dialog', lambda dlg: dlg.accept())
    pg.click('#deleteBtn'); pg.wait_for_timeout(300)
    data = saved_project()
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-01')
    before = next(e for e in original['thirdPartyElements'] if e['id'] == 'sample-01')
    check(not any(c['title'] == 'Temporary materials release' for c in data['contracts']) and el.get('contractIds') == before.get('contractIds'),
          'deleting a release unlinks its clearance log items and keeps their other contracts')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_credits_builder(browser, fake):
    ctx, pg, errs = new_page(browser, 'credits-builder', fake)
    open_sample(pg, fake)
    check(pg.inner_text('#reqCount') == '2 of 4 in the credits', 'flags the required credits that are missing, including deal memos (%s)' % pg.inner_text('#reqCount'))
    crawl = pg.inner_text('#crawl')
    check('Lena Ward' in crawl and 'Muddy Water Hymn' in crawl and 'levee at night' not in crawl.lower(), 'crawl shows people and songs, without excluded score cues')

    pg.click('#reqs [data-addreq="contract-rchs-license"]'); pg.wait_for_timeout(200)
    check(pg.inner_text('#reqCount') == '3 of 4 in the credits', 'adding the required wording meets it (%s)' % pg.inner_text('#reqCount'))

    pg.click('#exportBtn')
    text = pg.inner_text('#exportPreview')
    check('Directed by\nLena Ward' in text and 'Written by Earl Whitaker and June Whitaker' in text and 'Published by Delta Song Publishing (BMI)' in text,
          'text export has credits and music lines')
    check('Riverside County Historical Society' in text and 'Riverside Courier' not in text, 'text export lists archival sources, without excluded ones')
    pg.check('input[name=layout][value=columns]')
    check('Directed by\tLena Ward' in pg.inner_text('#exportPreview'), 'two-column layout uses a tab')
    with pg.expect_download() as d:
        pg.click('#downloadTxtBtn')
    check(d.value.suggested_filename.endswith('-end-credits-two-columns.txt') and 'Directed by\tLena Ward' in open(d.value.path(), encoding='utf-8').read(),
          'text file downloads')
    check(not pg.is_visible('#exportDialog'), 'export dialog closes after download')

    pg.click('#addBtn'); pg.fill('#f-role', 'Gaffer'); pg.fill('#f-names', 'Jo Park')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Jo Park' in pg.inner_text('#crawl'), 'new credit shows in the crawl')
    rows = pg.locator('#entries .entry')
    last = rows.count() - 1
    pg.click('[data-up="%d"]' % last); pg.wait_for_timeout(100)
    check('Gaffer' in rows.nth(last - 1).inner_text(), 'moving a credit up reorders it')

    pg.click('[data-edit="credit-post-supervisor"]')
    pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    check('Sam Okafor' in pg.inner_text('#uncredited'), 'removing a credit lists the person as not credited')
    pg.click('#uncredited [data-skip="person-sam-okafor"]'); pg.wait_for_timeout(200)
    check('Sam Okafor' not in pg.inner_text('#uncredited'), 'marking someone not credited takes them off the list')

    pg.click('#addReqBtn')
    pg.select_option('#r-contract', '')
    pg.fill('#r-title', 'Test archive license')
    pg.select_option('#r-element', 'sample-07')
    pg.fill('#r-text', 'Courtesy of the Test Archive')
    pg.click('#reqForm button[type=submit]'); pg.wait_for_timeout(200)
    check(pg.inner_text('#reqCount') == '3 of 5 in the credits', 'a new requirement is flagged until the credits include it (%s)' % pg.inner_text('#reqCount'))

    pg.click('#playBtn')
    check('is-playing' in pg.get_attribute('#screen', 'class'), 'play crawl starts the roll')
    pg.click('#playBtn')
    check('is-playing' not in pg.get_attribute('#screen', 'class'), 'stop crawl ends it')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    entries = data['credits']['entries']
    check(any(e.get('role') == 'Gaffer' and e.get('names') == ['Jo Park'] for e in entries) and data['credits'].get('notCredited') == ['person-sam-okafor'],
          'credits and not-credited choices are saved')
    lic = next((c for c in data['contracts'] if c.get('title') == 'Test archive license'), {})
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-07')
    check(lic.get('requiredCredit') == 'Courtesy of the Test Archive' and lic.get('thirdPartyElementIds') == ['sample-07'] and lic.get('id') in el.get('contractIds', []),
          'new license is saved and linked to its clearance log item')
    original = json.loads(sample)
    song = lambda d: next(e for e in d['thirdPartyElements'] if e['id'] == 'sample-03').get('music')
    check(data['people'] == original['people'] and data.get('callSheets') == original['callSheets'] and data.get('musicCueSheet') == original['musicCueSheet']
          and song(data) == song(original), "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

    # Drafting from the project, on the sample with its credits taken out.
    ctx, pg, errs = new_page(browser, 'credits-builder', False)
    bare = json.loads(sample); bare.pop('credits')
    pg.set_input_files('#fileInput', files=[{'name': 'bare.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(bare).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    check(pg.is_visible('#fillBtn'), 'a project without credits offers a draft')
    pg.click('#fillBtn'); pg.wait_for_timeout(200)
    roles = [t.split('\n')[0] for t in pg.locator('#entries .entry .what').all_inner_texts()]
    check(roles[:6] == ['Director', 'Producer', 'Editor', 'Director of photography', 'Composer', 'Featuring'], 'draft puts key creatives first, then featuring %s' % roles[:6])
    crawl = pg.inner_text('#crawl')
    check('Daniel Okafor' in crawl and 'Muddy Water Hymn' in crawl and 'All rights reserved' in crawl, 'draft has people, music and a copyright line')
    check(pg.inner_text('#reqCount') == '4 of 4 in the credits', 'draft includes the required wording, deal memo credits too (%s)' % pg.inner_text('#reqCount'))
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

# Each spreadsheet template's columns must appear in its tool's CSV export, in the same order.
TEMPLATE_EXPORTS = [('bookings', 'bookings-template.csv'), ('revenue-tracker', 'revenue-template.csv'), ('waterfall', 'waterfall-template.csv'), ('qc-tracker', 'qc-issues-template.csv'), ('deliverables', 'deliverables-template.csv'), ('rights-matrix', 'rights-matrix-template.csv'), ('stills-library', 'stills-caption-sheet-template.csv'), ('festival-strategy', 'festival-strategy-template.csv'), ('fair-use-log', 'fair-use-template.csv'), ('license-tracker', 'licenses-template.csv'), ('clearance-report', 'clearance-report-template.csv'), ('chain-of-title', 'chain-of-title-template.csv'), ('structure-board', 'structure-board-template.csv'), ('cut-tracker', 'cut-notes-template.csv'), ('budget-to-actuals', 'cost-report-template.csv'), ('footage-log', 'footage-log-template.csv'), ('paper-edit', 'paper-edit-template.csv'), ('press-list', 'press-list-template.csv'), ('partner-crm', 'partner-crm-template.csv'), ('camera-sound-reports', 'camera-and-sound-reports-template.csv'), ('interview-log', 'interview-moments-template.csv'), ('travel-sheet', 'travel-sheet-template.csv'), ('risk-plan', 'risk-assessment-template.csv'), ('security-checklist', 'security-checklist-template.csv'), ('gear-list', 'gear-list-template.csv'), ('coi-permit-tracker', 'certificates-and-permits-template.csv'), ('location-scout', 'location-scout-template.csv'), ('deal-memos', 'deal-memos-template.csv'), ('shooting-calendar', 'shooting-calendar-template.csv'), ('interview-prep', 'interview-questions-template.csv'), ('funder-crm', 'funder-crm-template.csv'), ('cash-flow', 'cash-flow-template.csv'), ('budget', 'budget-template.csv'), ('finance-plan', 'finance-plan-template.csv'), ('grant-calendar', 'grant-calendar-template.csv'), ('clearance-log', 'clearance-log-template.csv'), ('release-tracker', 'release-log-template.csv'),
                    ('music-cue-sheet', 'music-cue-sheet-template.csv'), ('name-supers', 'name-supers-template.csv'),
                    ('subject-tracker', 'subject-tracker-template.csv'), ('research-log', 'research-log-template.csv'),
                    ('comps-tracker', 'comps-tracker-template.csv')]

def test_name_supers(browser, fake):
    ctx, pg, errs = new_page(browser, 'name-supers', fake)
    open_sample(pg, fake)
    rows = pg.inner_text('#rows')
    check('Close to Marcus Bell in the project' in rows, 'flags a typed name close to someone in the project')
    check('Changed: title was "Levee board member"' in rows and 'New since export' in rows, 'flags changes since the last export')
    check('Marcus Bell' in pg.inner_text('#missing'), 'lists people on camera without a super')
    pg.click('[data-link="super-foreman"]'); pg.wait_for_timeout(200)
    check('Close to Marcus Bell' not in pg.inner_text('#rows') and 'Everyone on camera has a super' in pg.inner_text('#missing'), 'using the project spelling links the super')

    pg.click('[data-edit="super-ruth"]')
    pg.fill('#f-name', 'Ruth A. Hammond'); pg.fill('#f-tc', '1:02'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a badly formed timecode is refused')
    pg.fill('#f-tc', '01:00:30:00'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .nm').first.inner_text() == 'Ruth A. Hammond', 'supers sort by timecode, with the fixed spelling')

    pg.click('#addBtn'); pg.select_option('#f-person', ''); pg.fill('#f-name', 'Archival narrator'); pg.fill('#f-title', 'Voice, 1965 newsreel')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Archival narrator' in pg.inner_text('#rows'), 'adds a super for someone not in the project')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[0] == ['First appears', 'Name', 'Title', 'Notes', 'Since last export'] and lines[1][:2] == ['01:00:30:00', 'Ruth A. Hammond'] and lines[1][4].startswith('Changed'),
          'export lists supers in order with what changed')
    check('No changes since then' in pg.inner_text('#since') and 'New since export' not in pg.inner_text('#rows'), 'export resets the change flags')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    people = {p['id']: p for p in data['people']}
    foreman = next(e for e in data['supers']['entries'] if e['id'] == 'super-foreman')
    check(people['person-ruth-hammond']['name'] == 'Ruth A. Hammond' and foreman.get('personId') == 'person-marcus-bell' and 'name' not in foreman,
          'spelling fixes and links are saved to the project')
    check(len(data['supers']['lastExport']['entries']) == 5, 'the export snapshot is saved')
    original = json.loads(sample)
    check(data.get('credits') == original['credits'] and data.get('callSheets') == original['callSheets'] and data['contracts'] == original['contracts'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_subject_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'subject-tracker', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 5 and 'Agreed 2' in pg.inner_text('#filters'), 'lists subjects with counts by access')
    pg.click('[data-filter="declined"]')
    check(pg.locator('#rows .row').count() == 1 and 'Office of the mayor' in pg.inner_text('#rows'), 'filters by access status')
    pg.click('[data-filter="all"]'); pg.fill('#search', 'diary')
    check(pg.locator('#rows .row').count() == 1, 'search finds subjects by notes')
    pg.fill('#search', '')

    pg.click('#addBtn'); pg.fill('#f-name', 'Ida Fenn'); pg.fill('#f-about', 'Ran the sandbag line in 1993')
    pg.select_option('#f-status', 'in-conversation'); pg.fill('#f-next', '2020-01-02'); pg.fill('#f-nextNote', 'Send the release')
    pg.fill('#logNote', 'Met at the library'); pg.click('#logAddBtn')
    check('Met at the library' in pg.inner_text('#log'), 'logs a contact in the editor')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    first = pg.locator('#rows .row').first.inner_text()
    check('Ida Fenn' in first and 'overdue' in first and 'Ida Fenn' in pg.inner_text('#dueList'), 'an overdue follow-up comes first and is listed as due')

    pg.click('[data-edit="subject-clerk"]'); pg.select_option('#f-status', 'agreed'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Agreed, not in the project yet' in pg.inner_text('#rows'), 'flags agreed subjects not in the project')
    pg.click('[data-person="subject-clerk"]'); pg.wait_for_timeout(200)
    check('Agreed, not in the project yet' not in pg.inner_text('#rows'), 'adds an agreed subject to the project')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[1][0] == 'Ida Fenn' and len(lines) == 7, 'CSV lists subjects, follow-ups first')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    doris = next(p for p in data['people'] if p['name'] == 'Doris Kemp')
    clerk = next(s for s in data['subjects'] if s['id'] == 'subject-clerk')
    ida = next(s for s in data['subjects'] if s['name'] == 'Ida Fenn')
    check(clerk['personId'] == doris['id'] and doris.get('onCamera') is True and doris.get('phone') == '555-0142' and doris.get('roles') == ['Interview subject'],
          'the new person is saved with their contact details, on camera')
    check(ida.get('log') == [{'date': ida['lastContact'], 'note': 'Met at the library'}] and ida['nextFollowUp'] == '2020-01-02', 'the contact log and follow-up are saved')
    original = json.loads(sample)
    check(data.get('credits') == original['credits'] and data.get('supers') == original['supers'] and data['contracts'] == original['contracts'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_research_log(browser, fake):
    ctx, pg, errs = new_page(browser, 'research-log', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 4 and 'Research sources 2' in pg.inner_text('#tab-research'), 'shows archival leads, with research sources on their own tab')
    check('In the clearance log: Licensed' in pg.inner_text('#rows'), "shows a linked lead's clearance status")
    pg.click('#tab-research')
    check('Corps of Engineers' in pg.inner_text('#rows') and 'Flood of 1965' not in pg.inner_text('#rows'), 'switches to research sources')
    pg.click('#tab-archival')
    pg.select_option('#statusFilter', 'screener-received')
    check(pg.locator('#rows .row').count() == 1, 'filters by status')
    pg.select_option('#statusFilter', '')

    pg.click('[data-edit="source-sandbag"]'); pg.select_option('#f-status', 'ready-to-license'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Ready, not in the clearance log yet' in pg.inner_text('#rows'), 'flags a ready lead not in the clearance log')
    pg.click('[data-send="source-sandbag"]'); pg.wait_for_timeout(200)
    check('Ready, not in the clearance log yet' not in pg.inner_text('#rows') and pg.inner_text('#rows').count('In the clearance log') == 3, 'sends a lead to the clearance log')

    pg.click('#addBtn'); pg.fill('#f-title', 'Levee construction stills'); pg.fill('#f-cost', '-5'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a negative cost is refused')
    pg.fill('#f-cost', '200'); pg.select_option('#f-type', 'Archival still'); pg.fill('#f-archive', 'State archives'); pg.click('#sendBtn'); pg.wait_for_timeout(200)
    check('Levee construction stills' in pg.inner_text('#rows') and '4 sent to the clearance log' in pg.inner_text('#totals'), 'a new source can be sent straight from the editor')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(len(lines) == 8 and lines[0][0] == 'Log' and any(r[1] == 'Levee construction stills' and r[13] == 'Not started' for r in lines), 'CSV lists every source with its clearance status')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    sandbag = next(s for s in data['sources'] if s['id'] == 'source-sandbag')
    el = next(e for e in data['thirdPartyElements'] if e['id'] == sandbag.get('elementId'))
    check(el['description'] == 'Sandbag line on Front Street, 1993' and el['type'] == 'Archival still' and el['status'] == 'not-started'
          and el['rightsHolder'] == 'Riverside Public Library' and el['cost'] == 75 and 'Box 31, folder 7' in el['source'], 'the sent element carries the lead\'s details')
    new = next(s for s in data['sources'] if s.get('title') == 'Levee construction stills')
    check(new.get('cost') == 200 and new.get('status') == 'ready-to-license' and new.get('elementId'), 'the new source is saved, linked and ready')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('credits') == original['credits'] and data['contracts'] == original['contracts']
          and [e for e in data['thirdPartyElements'] if e['id'].startswith('sample-')] == original['thirdPartyElements'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_comps_tracker(browser, fake):
    ctx, pg, errs = new_page(browser, 'comps-tracker', fake)
    open_sample(pg, fake)
    rows = pg.inner_text('#rows')
    check(pg.locator('#rows .row').count() == 3 and rows.count('No source') == 1, 'lists comps and flags a figure without a source')
    pg.click('[data-tag="subjectTags:floods"]')
    check(pg.locator('#rows .row').count() == 2, 'filters by tag')
    pg.click('[data-tag="subjectTags:floods"]')
    check('Fewer than three comps' in pg.inner_text('#checks') and 'without a source' in pg.inner_text('#checks'), 'checks the comps page before the pitch')
    pg.check('[data-pitch="comp-ledger"]'); pg.wait_for_timeout(100)
    check('Fewer than three' not in pg.inner_text('#checks') and 'more than seven years old' in pg.inner_text('#checks'), 'picking a comp updates the checks')

    pg.click('[data-edit="comp-seawall"]')
    pg.locator('#figRows .fig-source').first.fill('Fictional box office tracker, 2022')
    pg.click('#addFigBtn'); pg.locator('#figRows .fig-label').last.fill('Budget'); pg.locator('#figRows .fig-amount').last.fill('$600,000')
    pg.fill('#f-style', 'archival-led, essay')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.inner_text('#rows').count('No source') == 1 and 'Style: essay' in pg.inner_text('#rows'), 'adds a figure and a tag; the new unsourced figure is flagged')

    pg.click('#printBtn'); pg.wait_for_timeout(200)
    report = pg.inner_text('#report')
    check('$210,000' in report and 'Fictional box office tracker, 2022' in report and '$600,000' not in report and 'Ledger of the Low Water' in report, 'the comps page lists picked comps with sourced figures only')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    lines = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(lines[1][0] == 'Backwater Hymnal' and 'Budget: $600,000 (no source)' in lines[2][7], 'CSV lists comps newest first with their figures')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    seawall = next(c for c in data['comps'] if c['id'] == 'comp-seawall')
    ledger = next(c for c in data['comps'] if c['id'] == 'comp-ledger')
    check(seawall['figures'][1] == {'label': 'Budget', 'amount': '$600,000'} and seawall['styleTags'] == ['archival-led', 'essay'] and ledger.get('inPitch') is True, 'comps are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('sources') == original['sources'] and data['thirdPartyElements'] == original['thirdPartyElements'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_treatment_builder(browser, fake):
    ctx, pg, errs = new_page(browser, 'treatment-builder', fake)
    open_sample(pg, fake)
    check(pg.input_value('#t-logline').startswith('When the river') and '25 / 50' in pg.inner_text('#outline'), 'opens the treatment with word counts')
    pg.fill('#t-logline', ' '.join(['word'] * 55)); pg.wait_for_timeout(100)
    check('5 over' in pg.inner_text('#wc-logline') and 'over' in pg.get_attribute('#wc-logline', 'class'), 'flags a section over its target')
    pg.fill('[data-target="logline"]', '60'); pg.wait_for_timeout(100)
    check('55 of 60 words' in pg.inner_text('#wc-logline'), 'targets can be changed')

    pg.click('[data-insert="team"]'); pg.wait_for_timeout(100)
    team = pg.input_value('#t-team')
    check('Director: Lena Ward' in team and 'Ruth Hammond' not in team, 'adds the crew, not the subjects, to the team section')
    pg.click('[data-insert="subjects"]'); pg.wait_for_timeout(100)
    subj = pg.input_value('#t-subjects')
    check('Daniel Okafor' in subj and 'Marcus Bell' in subj and 'Doris Kemp' in subj and subj.count('Ruth Hammond') == 1, 'adds missing subjects from the project and subject tracker, without repeats')

    pg.click('[data-compare="version-grant-draft"]'); pg.wait_for_timeout(200)
    body = pg.inner_html('#compareBody')
    check('<del>' in body and '<ins>' in body and 'Empty in both.' in pg.inner_text('#compareBody'), 'compares the current text with a saved version')
    pg.click('#compareClose')
    pg.fill('#versionLabel', 'Before the edit'); pg.click('#saveVersionBtn'); pg.wait_for_timeout(100)
    pg.fill('#t-access', 'Changed access text.'); pg.wait_for_timeout(100)
    pg.click('[data-compare]')
    check('Changes since "Before the edit"' in pg.inner_text('#compareTitle') and '1 section changed' in pg.inner_text('#compareLead'), 'a new version compares against later edits')
    pg.once('dialog', lambda d: d.accept())
    pg.click('#restoreVersionBtn'); pg.wait_for_timeout(200)
    check(pg.input_value('#t-access').startswith('Ruth has agreed'), 'goes back to a saved version')

    with pg.expect_download() as d:
        pg.click('#mdBtn')
    md = open(d.value.path(), encoding='utf-8').read()
    check(md.startswith('# The River Keeps') and '## Team' in md and '## Long synopsis' not in md, 'Markdown export has filled sections only')
    with pg.expect_download() as d:
        pg.click('#txtBtn')
    check('ACCESS\n\nRuth has agreed' in open(d.value.path(), encoding='utf-8').read(), 'plain text export')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    t = data['treatment']
    check(t['targets'] == {'shortSynopsis': 100, 'logline': 60} and len(t['versions']) == 2 and 'Lena Ward' in t['sections']['team'], 'sections, targets and versions are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('subjects') == original['subjects'] and data.get('credits') == original['credits'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_pitch_deck(browser, fake):
    import base64
    ctx, pg, errs = new_page(browser, 'pitch-deck', fake)
    open_sample(pg, fake)
    check(pg.locator('#deck .slide-wrap').count() == 8 and '7 slides, 1 left out' in pg.inner_text('#count'), 'opens the deck, with one slide left out')
    deck = pg.inner_text('#deck')
    check('Lena Ward' in deck and 'Backwater Hymnal' in deck and 'Fictional trade report' in deck, 'team and comps slides come from the project')

    png = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFklEQVR4nGP8z8DAwMDAxMDAwMDAAAANHQEDK+mmyAAAAABJRU5ErkJggg==')
    pg.set_input_files('#imgInput', files=[{'name': 'still.png', 'mimeType': 'image/png', 'buffer': png}])
    pg.wait_for_function("document.querySelectorAll('#imgs figure').length === 4")
    check(pg.locator('#imgs figure').count() == 4, 'adds an image from the computer')

    pg.click('#addBtn'); pg.select_option('#f-kind', 'image'); pg.fill('#f-body', 'The levee at dawn')
    pg.locator('#pickImgs input').nth(0).check(); pg.locator('#pickImgs input').nth(1).check()
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor') and 'one image' in pg.inner_text('#pickHint'), 'a full-page image slide takes one image')
    pg.locator('#pickImgs input').nth(0).uncheck(); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#deck .slide-wrap').count() == 9 and 'The levee at dawn' in pg.inner_text('#deck'), 'adds a full-page image slide')
    pg.click('[data-up="8"]'); pg.wait_for_timeout(100)
    check('Full-page image' in pg.locator('#deck .slide-wrap').nth(7).inner_text(), 'moves a slide')

    pg.check('input[name=size][value=letter]'); pg.click('#printBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#report .slide').count() == 8 and '11in 8.5in' in pg.inner_text('#pageSize'), 'prints the slides that aren\'t left out, at letter size')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    d = data['pitchDeck']
    new = d['images'][-1]
    check(d['size'] == 'letter' and new['name'] == 'still.png' and new['data'].startswith('data:image/jpeg;base64,') and d['slides'][7]['kind'] == 'image' and d['slides'][7]['imageIds'] == [d['images'][1]['id']],
          'size, images and slides are saved')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data.get('comps') == original['comps'] and data.get('treatment') == original['treatment'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

    # Starting from the project, on the sample without a deck.
    ctx, pg, errs = new_page(browser, 'pitch-deck', False)
    bare = json.loads(sample); bare.pop('pitchDeck')
    pg.set_input_files('#fileInput', files=[{'name': 'bare.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(bare).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    pg.click('#draftBtn'); pg.wait_for_timeout(200)
    deck = pg.inner_text('#deck')
    check(pg.locator('#deck .slide-wrap').count() == 8 and 'flood diary' in deck and 'Riverside has flooded' in deck and '[What you' in deck, 'drafts slides from the treatment and project')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def saved_project(pg, fake):
    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        return json.loads(pg.evaluate('window.__file.text'))
    with pg.expect_download() as d:
        pg.click('#saveBtn')
    return json.loads(open(d.value.path(), encoding='utf-8').read())

def test_grant_calendar(browser, fake):
    ctx, pg, errs = new_page(browser, 'grant-calendar', fake)
    open_sample(pg, fake)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names == ['Riverbend Documentary Fund', 'Prairie State Arts Board', 'Northern Light Media Foundation', 'Eastgate Film Initiative', 'Riverside County Heritage Trust'],
          'open applications first by deadline, then waiting, then decided %s' % names)
    north = pg.inner_text('[data-id="grant-northlight"]')
    check('3 of 5 materials ready' in pg.inner_text('[data-id="grant-riverbend"]') and '3 answers from the library' in north and 'Decision expected' in north, 'rows show materials, linked answers and the decision date')
    pg.click('[data-filter="submitted"]')
    check(pg.locator('#rows .row').count() == 1, 'filters by status')
    pg.click('[data-filter="all"]')
    check('$25,000' in pg.inner_text('#stats') and '$7,500' in pg.inner_text('#stats'), 'adds up what is waiting and what was awarded')

    pg.click('#calViewBtn')
    pg.click('#thisMonth')
    now = datetime.date.today()
    steps = (2027 * 12 + 1) - (now.year * 12 + now.month - 1)
    for _ in range(abs(steps)):
        pg.click('#nextMonth' if steps > 0 else '#prevMonth')
    check('2027' in pg.inner_text('#calTitle') and pg.locator('#calGrid [data-edit="grant-riverbend"]').count() == 1, 'the calendar shows a deadline on its day')
    pg.click('#calGrid [data-edit="grant-riverbend"]')
    check(pg.is_visible('#editor'), 'clicking a deadline in the calendar opens the grant')
    pg.locator('#matRows .mat-done').nth(2).check()
    pg.click('#addMatBtn'); pg.locator('#matRows .mat-name').last.fill('Fiscal sponsor letter')
    pg.check('#answers [data-version="version-synopsis-350c"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#listViewBtn')
    check('4 of 6 materials ready' in pg.inner_text('[data-id="grant-riverbend"]') and '1 answer from the library' in pg.inner_text('[data-id="grant-riverbend"]'), 'ticks materials, adds one and links an answer')

    pg.click('#addBtn')
    pg.fill('#f-funder', 'Test Fund'); pg.fill('#f-deadline', '2027-03-03')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names[:3] == ['Riverbend Documentary Fund', 'Test Fund', 'Prairie State Arts Board'] and '0 of 4 materials ready' in pg.inner_text('#rows'), 'a new grant starts with the usual materials and sorts by deadline')

    with pg.expect_download() as d:
        pg.click('#icsBtn')
    raw = open(d.value.path(), 'rb').read()
    lines = raw.decode('utf-8').split('\r\n')
    check(raw.count(b'BEGIN:VEVENT') == 5 and b'Eastgate' not in raw and b'DTSTART;VALUE=DATE:20270212' in raw and raw.count(b'TRIGGER:-P7D') == 3,
          'calendar file has every deadline but the declined one, with reminders for open applications')
    check(lines[0] == 'BEGIN:VCALENDAR' and all(len(l.encode()) <= 75 for l in lines) and b'\n' not in raw.replace(b'\r\n', b''), 'calendar file lines are folded and end in CRLF')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][0] == 'Funder' and rows[1][0] == 'Riverbend Documentary Fund' and rows[1][15] == 'Short synopsis (350 characters)', 'CSV lists grants with the answers used')

    pg.click('[data-edit="grant-eastgate"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Test Fund' in pg.inner_text('#report') and 'Eastgate' not in pg.inner_text('#report'), 'prints the list')
    data = saved_project(pg, fake)
    rb = next(g for g in data['grants'] if g['id'] == 'grant-riverbend')
    check(len(data['grants']) == 5 and rb['materials'][2] == {'name': 'Work sample, 10 minutes', 'done': True} and rb['materials'][-1] == {'name': 'Fiscal sponsor letter'}, 'grants are saved')
    versions = {v['id']: v for a in data['narratives'] for v in a['versions']}
    check({'grantId': 'grant-riverbend'}.items() <= versions['version-synopsis-350c']['uses'][0].items(), 'the linked answer is recorded on the library version')
    check(versions['version-logline-150c']['uses'][0] == {'funder': 'Eastgate Film Initiative: Development lab', 'date': '2026-05-29'}, 'removing a grant keeps the record of what was sent, by funder name')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data['treatment'] == original['treatment'] and data['comps'] == original['comps'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_narrative_library(browser, fake):
    ctx, pg, errs = new_page(browser, 'narrative-library', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 4 and '1 version over the limit' in pg.inner_text('#count') and '379 of 350 characters, 29 over' in pg.inner_text('#rows'), 'lists answers and flags a version over its limit')
    check('Northern Light Media Foundation' in pg.inner_text('#sentList'), 'shows what was sent recently')

    pg.click('[data-edit="narrative-synopsis"]')
    box = pg.locator('[data-vid="version-synopsis-350c"]')
    box.locator('.v-text').fill('A schoolteacher, a levee man and a grandson remember three floods as the river rises again.')
    check('of 350 characters' in box.locator('.v-count').inner_text() and 'over' not in box.locator('.v-count').inner_text(), 'counts as you type')
    pg.click('#addVersionBtn')
    new = pg.locator('#versions .v-edit').last
    new.locator('.v-limit').fill('20')
    check('69 of 20 words, 49 over' in new.locator('.v-count').inner_text(), 'a new version starts from the longest text and shows how far over it is')
    new.locator('.v-text').fill('A town remembers three floods.')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('over the limit' not in pg.inner_text('#count') and '5 of 20 words' in pg.inner_text('#rows'), 'saves the edited and the new version')

    check(pg.is_visible('#treatmentBtn'), 'offers sections of the treatment not in the library yet')
    pg.click('#treatmentBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 5 and 'Access' in pg.inner_text('#rows') and not pg.is_visible('#treatmentBtn'), 'adds them from the treatment')

    pg.click('#addBtn')
    pg.fill('#f-title', 'Budget narrative')
    pg.locator('#versions .v-limit').first.fill('250'); pg.locator('#versions .v-text').first.fill('We are raising the last third of the budget.')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('9 of 250 words' in pg.inner_text('#rows'), 'adds an answer')

    pg.click('#setBtn')
    pg.select_option('#setGrant', 'grant-riverbend')
    pg.select_option('#setList [data-answer="narrative-logline"]', 'version-logline-25w')
    pg.select_option('#setList [data-answer="narrative-impact"]', 'version-impact-150w')
    out = pg.input_value('#setOut')
    check(out.startswith('Logline (25 words)\n\nWhen the river') and 'Impact statement (150 words)' in out, 'pulls together the picked versions for one application')
    pg.click('#setCopyBtn'); pg.wait_for_timeout(200)
    check('Copied' in pg.inner_text('#toast'), 'copies the set')
    with pg.expect_download() as d:
        pg.click('#setTxtBtn')
    check(d.value.suggested_filename.endswith('riverbend-documentary-fund.txt') and 'Impact statement (150 words)' in open(d.value.path(), encoding='utf-8').read(), 'downloads the set as text')
    pg.fill('#setDate', '2027-02-10')
    pg.click('#setRecordBtn'); pg.wait_for_timeout(200)
    pg.select_option('#setList [data-answer="narrative-logline"]', 'version-logline-150c')
    pg.click('#setRecordBtn'); pg.wait_for_timeout(200)
    pg.select_option('#setGrant', '')
    pg.fill('#setFunder', 'Station pitch')
    pg.select_option('#setList [data-answer="narrative-bio-ana"]', 'version-bio-ana-50w')
    pg.click('#setRecordBtn'); pg.wait_for_timeout(200)
    pg.click('#setClose')
    check('Station pitch' in pg.inner_text('#sentList'), 'notes a set sent to a funder outside the grant calendar')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Answer', 'Version', 'Limit'] and len(rows) == 1 + 9 and any(r[0] == 'Logline' and 'Riverbend Documentary Fund' in r[9] for r in rows), 'CSV lists every version with where it was sent')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Budget narrative' in pg.inner_text('#report') and 'Access' in pg.inner_text('#report'), 'prints every answer')

    data = saved_project(pg, fake)
    versions = {v['id']: v for a in data['narratives'] for v in a['versions']}
    rb = lambda vid: [u for u in versions[vid].get('uses', []) if u.get('grantId') == 'grant-riverbend']
    check(rb('version-logline-150c') == [{'grantId': 'grant-riverbend', 'date': '2027-02-10'}] and rb('version-logline-25w') == [] and len(rb('version-impact-150w')) == 1,
          'one version of each answer per application: sending another length replaces the first')
    check(versions['version-bio-ana-50w']['uses'] == [{'funder': 'Station pitch', 'date': '2027-02-10'}], 'a funder outside the calendar is saved by name')
    check(versions['version-synopsis-350c']['updated'] != '2026-10-20' and versions['version-synopsis-100w']['updated'] == '2026-09-15', 'only changed versions get a new date')
    original = json.loads(sample)
    check(data['grants'] == original['grants'] and data['treatment'] == original['treatment'] and data['people'] == original['people'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def budget_grand(b):
    fr = {f['id']: f['percent'] for f in b['fringes']}
    sub = lambda l: round(l.get('quantity', 0) * l.get('multiplier', 1) * l.get('rate', 0), 2)
    direct = sum(sub(l) for l in b['lines'])
    fringe = sum(round(sub(l) * fr[l['fringeId']] / 100, 2) for l in b['lines'] if l.get('fringeId'))
    subtotal = direct + fringe
    return round(subtotal + sum(round(subtotal * m['percent'] / 100, 2) for m in b['markups']), 2)

def test_budget(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'budget', fake)
    open_sample(pg, fake)
    grand = budget_grand(original['budget'])
    check('${:,.0f}'.format(grand) in pg.inner_text('#topSheet') and 'Payroll taxes 12%' in pg.inner_text('#topSheet'), 'the top sheet adds up lines, fringes and percentages')
    qty = pg.locator('[data-line="line-3000-16"] [data-k="quantity"]')
    qty.fill('32')
    check('$78,848.00' in pg.inner_text('[data-line="line-3000-16"] [data-tot]') and pg.evaluate("document.activeElement.dataset.k") == 'quantity', 'a line total updates as you type, keeping your place')
    pg.click('[data-addline="account-2300"]')
    check(pg.evaluate("document.activeElement.dataset.k") == 'description', 'adding a line puts the cursor in it')
    row = pg.locator('[data-acct="account-2300"] .ln').last
    row.locator('[data-k="description"]').fill('Permit fees'); row.locator('[data-k="rate"]').fill('450')
    row.locator('[data-k="fringeId"]').select_option('fringe-payroll')
    check('$504.00' in row.locator('[data-tot]').inner_text(), 'a new line picks up its fringe')
    pg.click('#addBtn')
    pg.fill('#f-code', '4300'); pg.fill('#f-name', 'Impact campaign'); pg.select_option('#f-section', 'other')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('4300 Impact campaign' in pg.inner_text('#topSheet'), 'adds an account')
    pg.click('#ratesBtn')
    pg.locator('#markRows .r-pct').first.fill('5')
    pg.click('#ratesSubmit'); pg.wait_for_timeout(200)
    check('Contingency 5%' in pg.inner_text('#topSheet'), 'changes a percentage')
    pg.click('#versionBtn'); pg.fill('#f-vlabel', 'Test version'); pg.press('#f-vlabel', 'Enter'); pg.wait_for_timeout(200)
    check(pg.locator('#verList li').count() == 2, 'saves a version')
    pg.click('#compareBtn')
    pg.select_option('#cmpSel', 'budget-version-september')
    cmp = pg.inner_text('#cmpTable')
    check('3000 Editorial' in cmp and '+' in cmp and '−' in cmp, 'compares accounts with a saved version')
    pg.click('#compareDialog button[type=submit]')
    pg.click('[data-line="line-2100-9"] [data-delline]'); pg.wait_for_timeout(200)
    check(pg.locator('[data-line="line-2100-9"]').count() == 0, 'removes a line')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    editor = next(r for r in rows if r[3] == 'Editor')
    check(rows[0][0] == 'Account number' and editor[4] == '32' and editor[11] == '78848.00' and rows[-1][1] == 'Total', 'CSV lists every line with its fringe, then the total')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Top sheet' in pg.inner_text('#report') and 'Permit fees' in pg.inner_text('#report'), 'prints the top sheet and detail')
    data = saved_project(pg, fake)
    b = data['budget']
    check(len(b['versions']) == 2 and any(a['name'] == 'Impact campaign' for a in b['accounts']) and b['markups'][0]['percent'] == 5 and
          next(l for l in b['lines'] if l['id'] == 'line-3000-16')['quantity'] == 32 and not any(l['id'] == 'line-2100-9' for l in b['lines']), 'the budget is saved')
    check(data['grants'] == original['grants'] and data['financePlan'] == original['financePlan'] and data['budgetFormats'] == original['budgetFormats'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    ctx, pg, errs = new_page(browser, 'budget', fake)
    pg.click('#templateBtn'); pg.wait_for_timeout(200)
    check(pg.locator('.acct').count() == 19 and 'Festivals and outreach' in pg.inner_text('#sections'), 'starts from the documentary accounts')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_budget_converter(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'budget-converter', fake, extra=';window.__downloads=[];')
    open_sample(pg, fake)
    check('Not mapped yet' in pg.inner_text('#conv') and '2300 Locations: Location fees' in pg.inner_text('#checks'), 'flags a line that does not map')
    pg.select_option('[data-account="account-2300"]', 'category-rb-other'); pg.wait_for_timeout(100)
    check('Not mapped yet' not in pg.inner_text('#conv') and 'left out on purpose' in pg.inner_text('#checks'), 'mapping the account clears the flag; the left-out contingency still shows')
    pg.select_option('[data-markup="markup-contingency"]', 'category-rb-other'); pg.wait_for_timeout(100)
    grand = budget_grand(original['budget'])
    check('Everything is mapped' in pg.inner_text('#checks') and pg.inner_text('#conv').count('${:,.0f}'.format(grand)) == 2, 'the converted total matches the budget once everything is mapped')
    pg.click('[data-account="account-1000"] ~ details summary')
    pg.select_option('[data-line="line-1000-0"]', 'category-rb-personnel'); pg.wait_for_timeout(100)
    check('1 sent elsewhere' in pg.inner_text('#mapping'), 'sends one line to another category')

    pg.click('#addBtn')
    pg.select_option('#f-preset', 'sf424a')
    check(pg.locator('#catRows .cat-row').count() == 8 and pg.input_value('#f-name') == 'US federal object classes (SF-424A)', 'a common format fills in its categories')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    travel = pg.locator('[data-account="account-2200"] option:checked').inner_text()
    fringe = pg.locator('#fringeTo option:checked').inner_text()
    check(travel == 'Travel' and fringe == 'Fringe benefits' and 'not mapped' in pg.inner_text('#count'), 'it maps what it can and leaves the rest to check')
    with pg.expect_download() as d:
        pg.click('#exportFormatBtn')
    fmt_text = open(d.value.path(), encoding='utf-8').read()
    fmt = json.loads(fmt_text)
    check(fmt['format'] == 'open-filmmaker-toolkit/budget-format' and fmt['accounts'].get('2200 Travel and lodging') == 'Travel' and fmt['fringes'] == 'Fringe benefits', 'saves a format file that maps by account')
    pg.set_input_files('#formatInput', files=[{'name': 'f.budget-format.json', 'mimeType': 'application/json', 'buffer': fmt_text.encode()}]); pg.wait_for_timeout(200)
    check(pg.locator('#formatSel option').count() == 3 and pg.locator('[data-account="account-2200"] option:checked').inner_text() == 'Travel', 'opens a format file and maps the accounts it names')

    pg.select_option('#formatSel', 'budget-format-riverbend'); pg.wait_for_timeout(100)
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Category', 'Item', 'Amount'] and ['Equipment and travel', '3000 Editorial: Edit system rental', '4200.00'] in rows, 'CSV lists each category with its lines')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Riverbend Documentary Fund' in pg.inner_text('#report') and 'Music and archival' in pg.inner_text('#report'), 'prints the converted budget for the application')
    data = saved_project(pg, fake)
    rb = next(f for f in data['budgetFormats'] if f['id'] == 'budget-format-riverbend')
    check(len(data['budgetFormats']) == 3 and rb['accountMap']['account-2300'] == 'category-rb-other' and rb['markupMap']['markup-contingency'] == 'category-rb-other' and rb['lineMap']['line-1000-0'] == 'category-rb-personnel', 'mappings are saved')
    check(data['budget'] == original['budget'] and data['grants'] == original['grants'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_finance_plan(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'finance-plan', fake)
    open_sample(pg, fake)
    sums = pg.inner_text('#sums')
    check('$101,700' in sums and '$65,000' in sums and '$47,000' in sums and '$34,200' in sums, 'totals confirmed, pending and prospective money, and what is not cash')
    check('${:,.0f}'.format(budget_grand(original['budget'])) in pg.inner_text('#budgetLine'), 'reads the budget total from the budget')
    pg.click('[data-filter="pending"]')
    check(pg.locator('#rows .row').count() == 2, 'filters by status')
    pg.click('[data-filter="all"]')
    check('Jun 2026' in pg.inner_text('#months') and '$132,500 so far' in pg.inner_text('#months'), 'shows when money arrives, with the running total')
    pg.click('#fromGrantsBtn')
    check(pg.locator('#grantsList input').count() == 1, 'offers grants not in the plan yet')
    pg.click('#grantsForm button[type=submit]'); pg.wait_for_timeout(200)
    check('Prairie State Arts Board' in pg.inner_text('#rows'), 'adds a grant from the grant calendar')
    pg.click('[data-edit="source-northlight"]')
    check(pg.is_disabled('#f-amount') and pg.is_visible('#linkedNote'), 'a linked grant follows the grant calendar')
    pg.click('#unlinkBtn')
    pg.select_option('#f-status', 'confirmed')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('$126,700' in pg.inner_text('#sums'), 'unlinking lets you set the status yourself')
    pg.click('#addBtn')
    pg.fill('#f-name', 'Bridge loan'); pg.select_option('#f-kind', 'loan'); pg.fill('#f-amount', '10000'); pg.select_option('#f-status', 'pending')
    pg.click('#addPayBtn'); pg.locator('#payRows .p-date').last.fill('2027-01-15'); pg.locator('#payRows .p-amount').last.fill('10000')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Jan 2027' in pg.inner_text('#months') and '$50,000' in pg.inner_text('#sums'), 'adds a source with a payment date')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Source', 'Kind', 'Status', 'Amount'] and ['Bridge loan', 'Loan', 'Pending', '10000.00'] == rows[[r[0] for r in rows].index('Bridge loan')][:4], 'CSV lists every source')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Still to raise' in pg.inner_text('#report') and 'Bridge loan' in pg.inner_text('#report'), 'prints the finance plan')
    data = saved_project(pg, fake)
    src = {s['id']: s for s in data['financePlan']['sources']}
    check(len(src) == 10 and 'grantId' not in src['source-northlight'] and src['source-northlight']['status'] == 'confirmed' and src['source-northlight']['amount'] == 25000, 'sources are saved')
    check(data['grants'] == original['grants'] and data['budget'] == original['budget'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    nobudget = dict(original); del nobudget['budget']
    ctx, pg, errs = new_page(browser, 'finance-plan', fake)
    pg.set_input_files('#fileInput', files=[{'name': 'n.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(nobudget).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    pg.fill('#budgetIn', '300000'); pg.press('#budgetIn', 'Tab'); pg.wait_for_timeout(200)
    check('$86,300' in pg.inner_text('#sums'), 'without a budget, uses a total you type in')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_funder_crm(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'funder-crm', fake)
    open_sample(pg, fake)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names == ['Riverbend Documentary Fund', 'Northern Light Media Foundation', 'Regional public television', 'Riverside County Heritage Trust', 'Eastgate Film Initiative'],
          'organizations with the soonest next step come first, passed ones last %s' % names)
    check('Local history grant: awarded' in pg.inner_text('[data-id="funder-heritage"]') and 'Last contact Oct 2, 2026' in pg.inner_text('[data-id="funder-riverbend"]'), 'rows show linked applications and the last contact')
    pg.click('[data-filter="talking"]')
    check(pg.locator('#rows .row').count() == 3, 'filters by stage')
    pg.click('[data-filter="all"]')
    pg.fill('#search', 'whitfield')
    check(pg.locator('#rows .row').count() == 1, 'searches the people at each organization')
    pg.fill('#search', '')
    pg.click('[data-done="funder-riverbend|step-riverbend-1"]'); pg.wait_for_timeout(200)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(pg.locator('#steps input').count() == 3 and names[3] == 'Riverbend Documentary Fund', 'ticking a next step marks it done')

    pg.click('[data-edit="funder-riverbend"]')
    pg.click('#addContactBtn'); row = pg.locator('#cRows .c-row').last
    row.locator('.c-name').fill('Lee Moreno'); row.locator('.c-title').fill('Director of programs'); row.locator('.c-name').dispatch_event('change')
    pg.click('#addStepBtn'); step = pg.locator('#nRows .n-row').last
    step.locator('.n-due').fill('2026-12-01'); step.locator('.n-text').fill('Send the work sample')
    pg.fill('#logDate', '2026-10-27'); pg.select_option('#logKind', 'call')
    pg.select_option('#logWho', label='Lee Moreno')
    pg.fill('#logNote', 'Lee asked for a 10-minute work sample.')
    pg.click('#logAddBtn')
    check('Lee asked for a 10-minute work sample.' in pg.inner_text('#log') and 'With Lee Moreno' in pg.inner_text('#log'), 'logs a call with one of the people')
    pg.check('#apps input[value="grant-prairie-arts"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    rb = pg.inner_text('[data-id="funder-riverbend"]')
    check('Next: Send the work sample, due Dec 1, 2026' in rb and 'Last contact Oct 27, 2026' in rb and 'Media artist grant: researching' in rb, 'saves people, next steps, the log and linked applications')

    check(not pg.is_visible('#fromGrantsBtn'), 'a funder whose application is already linked is not offered from the grant calendar')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    rbrow = next(r for r in rows if r[0] == 'Riverbend Documentary Fund')
    check(rows[0][0] == 'Organization' and 'Dana Whitfield, Program officer, dana@example.org' in rbrow[3] and rbrow[5] == 'Send the work sample', 'CSV lists organizations with people and the next step')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Riverbend Documentary Fund' in pg.inner_text('#report') and 'Lee Moreno' in pg.inner_text('#report'), 'prints the list')
    data = saved_project(pg, fake)
    f = next(x for x in data['funders'] if x['id'] == 'funder-riverbend')
    lee = next(c for c in f['contacts'] if c['name'] == 'Lee Moreno')
    check(len(f['interactions']) == 3 and f['interactions'][-1]['contactId'] == lee['id'] and f['nextSteps'][0]['done'] is True and f['grantIds'] == ['grant-riverbend', 'grant-prairie-arts'], 'the organization is saved')
    check(data['grants'] == original['grants'] and data['financePlan'] == original['financePlan'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    ctx, pg, errs = new_page(browser, 'funder-crm', fake)
    open_sample(pg, fake)
    pg.click('#fromGrantsBtn')
    pg.click('#grantsForm button[type=submit]'); pg.wait_for_timeout(200)
    check('Prairie State Arts Board' in pg.inner_text('#rows') and 'Media artist grant: researching' in pg.inner_text('#rows'), 'adds a funder from the grant calendar, linked to its application')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_cash_flow(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'cash-flow', fake)
    open_sample(pg, fake)
    sums = pg.inner_text('#sums')
    check(pg.inner_text('#count') == '24 months · 19 short' and 'First short: Mar 2026' in sums and '$132,500' in sums, 'spreads costs and income across the months and flags shortfalls')
    check(pg.locator('#flow tr.short').count() == 19 and '1 cost not scheduled' in pg.inner_text('#unsched') and '$67,200' in pg.inner_text('#unsched'), 'lists what is not scheduled, deferred or in-kind')
    pg.click('#settingsBtn'); pg.uncheck('#s-pending'); pg.click('#settingsSubmit'); pg.wait_for_timeout(200)
    check('$67,500' in pg.inner_text('#sums') and 'Counting confirmed money' in pg.inner_text('#sums'), 'pending money can be left out')
    pg.click('#settingsBtn'); pg.check('#s-pending'); pg.check('#s-prospective'); pg.fill('#s-opening', '20000'); pg.click('#settingsSubmit'); pg.wait_for_timeout(200)
    sums = pg.inner_text('#sums')
    check('$167,500' in sums and '$20,000' in sums and 'Donations through the fiscal sponsor, no payment date' in pg.inner_text('#unsched'), 'prospective money can be counted; money with no date is listed')

    pg.click('#goSched')
    check(pg.is_visible('#schedView'), 'goes to the schedule from the list of unscheduled costs')
    pg.select_option('.mode[data-kind="markups"][data-id="markup-contingency"]', 'spread'); pg.wait_for_timeout(100)
    pg.fill('input[data-kind="markups"][data-id="markup-contingency"][data-k="from"]', '2027-01-01'); pg.locator('input[data-kind="markups"][data-id="markup-contingency"][data-k="from"]').dispatch_event('change'); pg.wait_for_timeout(100)
    pg.fill('input[data-kind="markups"][data-id="markup-contingency"][data-k="to"]', '2027-12-31'); pg.locator('input[data-kind="markups"][data-id="markup-contingency"][data-k="to"]').dispatch_event('change'); pg.wait_for_timeout(100)
    check('cost not scheduled' not in pg.inner_text('#unsched'), 'schedules a percentage')
    pg.select_option('.mode[data-kind="lines"][data-id="line-1300-4"]', 'same'); pg.wait_for_timeout(100)
    check('Deferred' not in pg.inner_text('#unsched'), 'a line can go back to its account schedule')
    pg.click('#settingsBtn'); pg.select_option('#s-period', 'week'); pg.click('#settingsSubmit'); pg.wait_for_timeout(200)
    check('weeks' in pg.inner_text('#count'), 'shows weeks')
    pg.click('#flowViewBtn')
    check('Week of' in pg.inner_text('#flow'), 'the table shows weeks')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Period', 'Starts', 'Out', 'In', 'Net', 'Balance', 'Short'] and rows[1][5] == '20000.00' and len(rows) > 90, 'CSV has a row for each week with the balance')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Cash flow' in pg.inner_text('#report') and 'Week of' in pg.inner_text('#report'), 'prints the table')
    data = saved_project(pg, fake)
    cf = data['cashFlow']
    check(cf['period'] == 'week' and cf['openingBalance'] == 20000 and cf['includeProspective'] is True and 'includePending' not in cf and
          cf['markups']['markup-contingency'] == {'mode': 'spread', 'from': '2027-01-01', 'to': '2027-12-31'} and 'line-1300-4' not in cf['lines'], 'the schedule is saved')
    check(data['budget'] == original['budget'] and data['financePlan'] == original['financePlan'], "the budget and finance plan are unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_shooting_calendar(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'shooting-calendar', fake)
    open_sample(pg, fake)
    check(pg.inner_text('#count') == '4 shoot days · 2 travel · 1 hold', 'counts shoot days, travel days and holds')
    pg.click('#thisMonth')
    now = datetime.date.today()
    steps = (2026 * 12 + 4) - (now.year * 12 + now.month - 1)
    for _ in range(abs(steps)):
        pg.click('#nextMonth' if steps > 0 else '#prevMonth')
    check('May 2026' in pg.inner_text('#calTitle') and pg.locator('#calGrid .ev').count() == 4 and pg.locator('#calGrid .ev.cs').count() == 1, 'the month view shows the days, marking the one with a call sheet')
    pg.click('#listViewBtn'); pg.check('#showPast')
    check(pg.locator('#list .row').count() == 7 and pg.locator('#list .block-head').count() == 3 and 'Day 2 of 2' in pg.inner_text('[data-id="shootday-may-2"]'), 'the list groups days by trip and numbers the shoot days')

    pg.click('#addBtn')
    pg.fill('#f-date', '2027-03-17'); pg.fill('#f-through', '2027-03-19')
    pg.fill('#f-title', 'Grain elevator b-roll'); pg.fill('#f-block', 'Spring melt')
    pg.select_option('#f-location', 'location-grain-elevator'); pg.check('#people input[value="person-teo-ramirez"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.inner_text('#count') == '7 shoot days · 2 travel · 1 hold' and 'Day 4 of 4' in pg.inner_text('#list'), 'adds several days at once')

    pg.click('#list [data-edit="shootday-mar-1"]')
    pg.click('#callSheetBtn'); pg.wait_for_timeout(200)
    check(pg.is_visible('#csNote') and 'Call sheet started, Day 1 of 4' in pg.inner_text('#csNote') and not pg.is_visible('#callSheetBtn'), 'starts a call sheet from a shoot day')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#list [data-edit="shootday-may-travel-back"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)

    with pg.expect_download() as d:
        pg.click('#icsBtn')
    raw = open(d.value.path(), 'rb').read()
    lines = raw.decode('utf-8').split('\r\n')
    check(raw.count(b'BEGIN:VEVENT') == 9 and raw.count(b'STATUS:TENTATIVE') == 1 and b'LOCATION:Riverside levee' in raw and all(len(l.encode()) <= 75 for l in lines), 'calendar file has every day, holds tentative')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Date', 'Kind', 'Trip or block'] and len(rows) == 10, 'CSV lists every day')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('May 2026' in pg.inner_text('#report') and 'March 2027' in pg.inner_text('#report') and pg.locator('#report .r-month').count() == 3, 'prints a page for each month with days')
    data = saved_project(pg, fake)
    sheet = data['callSheets'][-1]
    day = next(x for x in data['shootDays'] if x['id'] == 'shootday-mar-1')
    check(len(data['shootDays']) == 9 and day['callSheetId'] == sheet['id'] and sheet['date'] == '2027-03-16' and sheet['dayLabel'] == 'Day 1 of 4' and sheet['locationId'] == 'location-grain-elevator'
          and {'personId': 'person-leon-pryor', 'role': 'Interview subject'} in sheet['crew'], 'the days and the new call sheet are saved')
    check(data['callSheets'][0] == original['callSheets'][0] and data['people'] == original['people'] and data['locations'] == original['locations'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_interview_prep(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'interview-prep', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 2 and '1 of 2 beats with no questions' in pg.inner_text('[data-id="interview-leon"]'), 'lists planned interviews and flags a beat with no questions')
    pg.click('[data-filter="done"]')
    check(pg.locator('#rows .row').count() == 1, 'filters done interviews')
    pg.click('[data-filter="planned"]')

    pg.click('[data-edit="interview-leon"]')
    check(pg.is_visible('#fromSubject'), 'offers notes from the subject tracker')
    pg.click('#fromSubjectBtn')
    pg.fill('#newQ', 'Who did the town blame?'); pg.press('#newQ', 'Enter')
    last = pg.locator('#qs .q').last
    last.locator('[data-beat]').select_option('beat-leon-blame')
    pg.locator('#qs .q').last.locator('[data-must]').check()
    pg.locator('#qs .q').last.locator('[data-move="-1"]').click()
    order = [pg.locator('#qs .q textarea').nth(i).input_value() for i in range(4)]
    check(order[2] == 'Who did the town blame?' and pg.locator('#qs .q').nth(2).get_attribute('class') == 'q must', 'adds a question, marks it must-ask and moves it up')
    check('1 question' in pg.locator('#beats .beat-row').nth(1).inner_text(), 'the beat now has a question')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    leon = pg.inner_text('[data-id="interview-leon"]')
    check('4 questions, 2 must-ask' in leon and '2 beats covered' in leon, 'saves the questions and beats')

    pg.click('#addBtn')
    pg.fill('#f-name', 'Doris Kemp'); pg.fill('#f-date', '2027-01-05')
    pg.fill('#newQ', 'What do the county records show?'); pg.click('#addQBtn')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Doris Kemp' in pg.inner_text('#rows') and 'Not in the project yet' in pg.inner_text('#rows'), 'adds an interview with someone not in the project')

    pg.select_option('#printSel', 'interview-ruth')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Interview: Ruth Hammond' in r and 'Hammond house' in r and 'Nov 10, 2026' in r and r.count('★') >= 4 and 'The night the levee broke' in r, 'prints a one-page guide for the interview picked')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Interviewee', 'Date', 'Order', 'Question', 'Must ask', 'Story beat', 'Asked'] and len(rows) == 16, 'CSV lists every question in order')
    data = saved_project(pg, fake)
    lv = next(i for i in data['interviews'] if i['id'] == 'interview-leon')
    subj = next(s for s in original['subjects'] if s['id'] == 'subject-leon')
    check([q['text'] for q in lv['questions']][2] == 'Who did the town blame?' and lv['questions'][2]['must'] is True and lv['questions'][2]['beatId'] == 'beat-leon-blame'
          and subj['about'] in lv['research'], 'the interview is saved in order, with the subject notes')
    check(any(i.get('name') == 'Doris Kemp' and 'personId' not in i for i in data['interviews']), 'someone not in the project is saved by name')
    check(data['people'] == original['people'] and data['subjects'] == original['subjects'] and data['shootDays'] == original['shootDays'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_field_journal(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'field-journal', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3 and pg.locator('#rows .row').first.get_attribute('data-id') == 'journal-flood-markers', 'lists entries, newest first')
    check('Shoot day: May 12, 2026: Day 1 of 2' in pg.inner_text('[data-id="journal-levee-dawn"]') and 'Riverside levee' in pg.inner_text('[data-id="journal-levee-dawn"]'), 'shows the shoot day and tags')
    pg.fill('#search', 'wind noise')
    check(pg.locator('#rows .row').count() == 1 and pg.is_visible('[data-id="journal-quiet-room"]'), 'search finds words in the text')
    pg.fill('#search', 'grain elevator')
    check(pg.locator('#rows .row').count() == 1 and pg.is_visible('[data-id="journal-flood-markers"]'), 'search finds a tagged location')
    pg.fill('#search', 'day 1 of 2')
    check(pg.locator('#rows .row').count() == 1 and pg.is_visible('[data-id="journal-levee-dawn"]'), 'search finds the linked shoot day')
    pg.fill('#search', '')
    pg.select_option('#fPerson', 'person-daniel-okafor')
    check(pg.locator('#rows .row').count() == 2, 'filters by person')
    pg.select_option('#fKind', 'learned')
    check(pg.locator('#rows .row').count() == 1, 'filters by kind as well')
    pg.select_option('#fPerson', ''); pg.select_option('#fKind', '')

    pg.click('#addBtn')
    check(pg.input_value('#f-date') != '', 'a new entry starts with today')
    pg.fill('#f-date', ''); pg.fill('#f-title', 'Second unit at the elevator'); pg.fill('#f-text', 'Fictional test entry: dust everywhere.\nBring masks.')
    pg.select_option('#f-kind', 'learned')
    pg.select_option('#f-sheet', 'callsheet-day-1')
    check(pg.input_value('#f-date') == '2026-05-12', 'picking a call sheet fills the empty date')
    pg.check('[data-person="person-lena-ward"]'); pg.check('[data-location="location-grain-elevator"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 4 and 'Lena Ward' in pg.inner_text('#rows'), 'adds an entry tagged with a person and a location')
    pg.click('[data-edit="journal-quiet-room"]')
    pg.uncheck('[data-person="person-daniel-okafor"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)

    with pg.expect_download() as d:
        pg.click('#mdBtn')
    md = open(d.value.path(), encoding='utf-8').read()
    check(d.value.suggested_filename.endswith('-field-journal.md') and md.startswith('# Field journal: The River Keeps') and '## 2026-05-12 · The levee at dawn' in md
          and 'People: Ana Reyes, Daniel Okafor' in md and 'Locations: Riverside levee' in md and '*Shoot day: May 12, 2026: Day 1 of 2*' in md and md.index('The levee at dawn') < md.index('Open on the flood markers'), 'Markdown export lists every entry, oldest first, with tags and the shoot day')
    pg.fill('#search', 'masks')
    with pg.expect_download() as d:
        pg.click('#mdBtn')
    md = open(d.value.path(), encoding='utf-8').read()
    check('Second unit at the elevator' in md and 'The levee at dawn' not in md and 'dust everywhere' in md, 'Markdown exports only the entries found by a search')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Second unit at the elevator' in pg.inner_text('#report') and 'The levee at dawn' not in pg.evaluate('document.getElementById("report").textContent'), 'prints the entries shown')
    pg.fill('#search', '')

    data = saved_project(pg, fake)
    new = next(e for e in data['journal'] if e.get('title') == 'Second unit at the elevator')
    check(new['date'] == '2026-05-12' and new['kind'] == 'learned' and new['callSheetId'] == 'callsheet-day-1' and new['personIds'] == ['person-lena-ward']
          and new['locationIds'] == ['location-grain-elevator'] and new['text'].endswith('Bring masks.'), 'the new entry is saved with its tags and shoot day')
    quiet = next(e for e in data['journal'] if e['id'] == 'journal-quiet-room')
    check('personIds' not in quiet and quiet['locationIds'] == ['location-hammond-house'], 'removing every tag drops the empty list')
    check(data['journal'][0] == original['journal'][0] and data['people'] == original['people'] and data['locations'] == original['locations'] and data['callSheets'] == original['callSheets']
          and data['interviews'] == original['interviews'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_hub(browser, fake):
    for scheme, vp in [('light', {'width': 1280, 'height': 900}), ('dark', PHONE)]:
        ctx = browser.new_context(viewport=vp, color_scheme=scheme)
        pg = ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://%s/index.html' % root)
        check(pg.locator('.tool').count() == len(TOOLS) and horizontal_overflow(pg) <= 1, 'home (%s): lists every tool and does not scroll sideways' % scheme)
        for k, (fg, bg) in pg.evaluate(COLORS_JS).items():
            check(contrast(fg, bg) >= 4.5, 'home (%s): %s text contrast %.1f:1' % (scheme, k, contrast(fg, bg)))
        check(not errs, 'no page errors %s' % errs)
        ctx.close()
    ctx = browser.new_context(); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://%s/index.html' % root)
    pg.fill('#q', 'release')
    visible = pg.locator('.tool:not([hidden]) h4').all_inner_texts()
    check('Release tracker' in visible and 'Budget' not in visible and pg.is_visible('#prep') and not pg.is_visible('#develop'), 'search shows only the tools that match, and hides stages with none')
    pg.fill('#q', 'zzzz nothing')
    check(pg.is_visible('#noMatch') and pg.locator('.tool:not([hidden])').count() == 0, 'search with no match offers to request a tool')
    pg.fill('#q', '')
    check(pg.locator('.tool:not([hidden])').count() == len(TOOLS), 'clearing the search shows every tool again')
    pg.click('.tool h4 a >> nth=0'); pg.wait_for_load_state('load')
    check('/tools/subject-tracker/' in pg.url and pg.title().startswith('Subject tracker'), 'a tool opens from the home page')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

# A 2x2 PNG, for adding a photo without any image files in the repo.
TINY_PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAIAAAD91JpzAAAAFklEQVR4nGP8z8DAwMDAxMDAwMDAAAANHQEDK+mmyAAAAABJRU5ErkJggg==')

def test_location_scout(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'location-scout', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 2 and 'No location release yet' in pg.inner_text('[data-id="scout-levee"]') and 'Location release signed' in pg.inner_text('[data-id="scout-elevator"]'),
          'lists scouts with their location release')
    check('Hammond house' in pg.inner_text('#todo'), 'lists places with no scout')
    pg.click('[data-filter="maybe"]')
    check(pg.locator('#rows .row').count() == 1, 'filters by verdict')
    pg.click('[data-filter="all"]')

    pg.click('[data-scout="location-hammond-house"]')
    check(pg.input_value('#f-location') == 'location-hammond-house' and 'waiting for signature' in pg.inner_text('#relNote'), 'scouting a listed place shows its release')
    pg.set_input_files('#photoInput', files=[{'name': 'porch.png', 'mimeType': 'image/png', 'buffer': TINY_PNG}])
    pg.wait_for_function("document.querySelectorAll('#photos .photo').length === 1")
    pg.fill('#photos [data-caption="0"]', 'The porch at noon')
    pg.fill('#f-power', 'Kitchen outlets'); pg.select_option('#f-verdict', 'good')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 3 and pg.locator('[data-id] img.thumb').count() == 3 and 'Every place' in pg.inner_text('#todo'), 'adds a scout with a photo')

    pg.click('#addBtn')
    pg.select_option('#f-location', '__new')
    pg.fill('#f-locName', 'Boat launch'); pg.fill('#f-locAddress', 'River Road')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Boat launch' in pg.inner_text('#rows'), 'a new place is added with its scout')

    pg.click('[data-edit="scout-levee"]')
    pg.click('#photos [data-delphoto="0"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Location', 'Address', 'Scouted on'] and len(rows) == 5, 'CSV lists every scout')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#report .r-scout').count() == 4 and pg.locator('#report .r-photos img').count() == 2, 'prints a report for each scout, with photos')
    data = saved_project(pg, fake)
    sc = {s['locationId']: s for s in data['scouts']}
    photo = next(a for a in data['assets'] if a['id'] == sc['location-hammond-house']['photoIds'][0])
    newloc = next(l for l in data['locations'] if l['name'] == 'Boat launch')
    check(photo['type'] == 'scout photo' and photo['data'].startswith('data:image/jpeg') and photo['caption'] == 'The porch at noon', 'the photo is saved in the project file')
    check('photoIds' not in sc['location-riverside-levee'] and not any(a['id'] == 'asset-scout-levee-1' for a in data['assets']) and newloc['address'] == 'River Road' and newloc['id'] in sc,
          'a removed photo is gone, and the new place is in the project')
    check(data['contracts'] == original['contracts'] and data['budget'] == original['budget'], "other tools' data is unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

# Pins the page's clock to a date, so checks that depend on what's coming up don't change with the day the tests run.
def fixed_today(iso):
    return "(() => { const T = new Date('%sT12:00:00').getTime(); const D = Date; class F extends D { constructor(...a) { super(...(a.length ? a : [T])); } static now() { return T; } } window.Date = F; })();" % iso

def test_gear_list(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'gear-list', fake, fixed_today('2026-11-01'))
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#gearView .row').count() == 8 and 'Rented from Northside Camera Rental' in pg.inner_text('[data-id="gear-primes"]'), 'lists gear by department, with where it comes from')
    sums = pg.inner_text('#sums')
    check('$10,520' in sums and '$360' in sums and '$455' in sums, 'totals owned value and rentals for the days packed')

    pg.click('#addBtn')
    pg.fill('#f-name', 'Slider'); pg.select_option('#f-dept', 'grip'); pg.select_option('#f-source', 'rental')
    check(pg.inner_text('#fromLabel') == 'Rental house', 'asks for the rental house when the gear is rented')
    pg.fill('#f-from', 'Bright Line Grip'); pg.fill('#f-day', '40'); pg.fill('#f-week', '160'); pg.fill('#f-value', '1200'); pg.fill('#f-serial', 'BLG-0981')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    slider = pg.locator('#gearView .row:has-text("Slider")')
    check(slider.count() == 1 and 'Not in a package yet' in slider.inner_text(), 'adds gear')

    pg.click('#addPkgBtn')
    check(pg.is_disabled('#p-day option[value="shootday-nov-1"]'), "a day that has a package can't get a second one")
    pg.select_option('#p-day', 'shootday-mar-1'); pg.select_option('#p-copy', 'package-nov-1')
    check(pg.locator('#picks input:checked').count() == 6, 'starts a package from another day')
    pg.check('#picks input[value="%s"]' % slider.get_attribute('data-id'))
    pg.click('#pkgForm button[type="submit"]'); pg.wait_for_timeout(200)
    check(pg.is_visible('#pkgView') and pg.locator('#pkgs .pkg').count() == 3 and 'Leon at the grain elevator' in pg.inner_text('#pkgs'), 'adds a package for a shoot day')
    check('$630' in pg.inner_text('#sums'), 'rental costs follow the days packed, at the cheaper of day or week rates')

    pg.select_option('#printSel', 'package-nov-1')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Load-out: Hammond house interview' in r and 'NCR-PR-1107' in r and 'Out' in r and 'Boom pole' not in r, 'prints a load-out checklist for a package')
    pg.click('#scheduleBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Equipment schedule' in r and 'FX6-0042117' in r and '$10,520' in r and 'Rented' in r, 'prints the insurance schedule with values and serial numbers')

    pg.click('#gearViewBtn')
    pg.click('[data-edit="gear-boom"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Item', 'Department', 'How many'] and len(rows) == 9, 'CSV lists every item')
    data = saved_project(pg, fake)
    g = data['gear']
    new = next(i for i in g['items'] if i['name'] == 'Slider')
    pk = {p['id']: p for p in g['packages']}
    mar = next(p for p in g['packages'] if p.get('shootDayId') == 'shootday-mar-1')
    check(new['source'] == 'rental' and new['dayRate'] == 40 and new['department'] == 'grip' and new['id'] in mar['itemIds'] and 'gear-primes' in mar['itemIds'],
          'the new gear and package are saved')
    check('gear-boom' not in pk['package-may-1']['itemIds'] and not any(i['id'] == 'gear-boom' for i in g['items']), 'removed gear leaves its packages')
    check(data['contracts'] == original['contracts'] and data['shootDays'] == original['shootDays'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_coi_permits(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'coi-permit-tracker', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3, 'lists certificates and permits')
    days = pg.inner_text('#days')
    check('requested since' in days and 'No certificate logged for Bright Line Grip' in days and pg.inner_text('#daysCount') == '2 to sort out', 'flags what is missing before each shoot day')
    check('Northside Camera Rental' in pg.inner_text('#soon') and 'Bright Line Grip' in pg.inner_text('#vendors'), 'lists what expires soon, and rental houses from the gear list without a certificate')

    pg.click('#vendors [data-vendor="Bright Line Grip"]')
    check(pg.input_value('#f-party') == 'Bright Line Grip' and pg.input_value('#f-type') == 'certificate of insurance' and pg.is_visible('#f-named') and not pg.is_visible('#f-conditions'), 'starts a certificate for the rental house')
    pg.fill('#f-named', 'Bright Line Grip, additional insured'); pg.fill('#f-expires', '2027-01-31')
    pg.set_input_files('#scanInput', files=[{'name': 'bl coi.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 sample'}])
    check(pg.input_value('#f-status') == 'received', 'attaching a scan marks it received')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Every rental house has a certificate' in pg.inner_text('#vendors'), 'the rental house is covered')

    pg.click('#days [data-loc="location-grain-elevator"]')
    check(pg.input_value('#f-type') == 'permit' and pg.is_checked('#locPicks input[value="location-grain-elevator"]') and pg.is_checked('#dayPicks input[value="shootday-mar-1"]'),
          'starts a permit for the location and day')
    pg.fill('#f-party', 'County film office'); pg.fill('#f-ref', 'CF-27-112'); pg.fill('#f-conditions', 'Weekdays only'); pg.select_option('#f-status', 'applied')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('[data-edit="contract-coi-hammond-house"]'); pg.select_option('#f-status', 'received'); pg.fill('#f-expires', '2026-11-30')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.inner_text('#daysCount') == '1 to sort out' and 'County film office: applied for' in pg.inner_text('#days'), 'the checks follow what changed')
    pg.click('[data-filter="permit"]')
    check(pg.locator('#rows .row').count() == 2, 'filters to permits')

    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Before each shoot day' in r and 'Missing' in r and 'CF-27-112' in r and 'Weekdays only' in r, 'prints the shoot-day check')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Type', 'Vendor or issuing office', 'Status'] and len(rows) == 6, 'CSV lists every certificate and permit')
    data = saved_project(pg, fake)
    cs = {c['id']: c for c in data['contracts']}
    bl = next(c for c in cs.values() if c.get('vendor') == 'Bright Line Grip')
    scan = next(a for a in data['assets'] if a['id'] == bl['assetIds'][0])
    permit = next(c for c in cs.values() if c.get('issuer') == 'County film office')
    check(bl['status'] == 'received' and bl['receivedDate'] == '2026-11-01' and scan['type'] == 'certificate scan' and scan['relativePath'] == 'certificates-and-permits/bl coi.pdf',
          'the certificate and its scan are saved')
    check(permit['type'] == 'permit' and permit['locationIds'] == ['location-grain-elevator'] and permit['shootDayIds'] == ['shootday-mar-1'] and permit['requestedDate'] == '2026-11-01' and 'namedOn' not in permit,
          'the permit is saved, linked to the location and day')
    check(cs['contract-coi-hammond-house']['receivedDate'] == '2026-11-01', 'marking a certificate received records the date')
    others = lambda d: [c for c in d['contracts'] if c.get('type') not in ('certificate of insurance', 'permit')]
    check(others(data) == others(original) and data['gear'] == original['gear'], 'other contracts and data are unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_travel_sheet(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'travel-sheet', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 1 and 'Anniversary shoot' in pg.inner_text('#cal') and 'Spring flood trip' not in pg.inner_text('#cal'), 'lists trips, and trips in the shooting calendar without a sheet')
    pg.click('#cal [data-block="Anniversary shoot"]')
    check(pg.input_value('#f-name') == 'Anniversary shoot' and pg.input_value('#f-start') == '2026-11-10' and pg.input_value('#f-end') == '2026-11-11'
          and pg.is_checked('#peoplePicks input[value="person-ruth-hammond"]') and pg.is_checked('#locPicks input[value="location-hammond-house"]'), 'a trip from the calendar starts with its dates, people and places')
    check(pg.is_visible('#hospNote'), "offers the hospital from a call sheet")
    pg.click('#hospBtn')
    check(pg.input_value('#f-hname').startswith('Riverside Community Hospital'), 'uses the call sheet hospital')
    pg.click('[data-add="legs"]')
    pg.select_option('#legs-0-kind', 'flight'); pg.fill('#legs-0-date', '2026-11-09'); pg.fill('#legs-0-from', 'MSP'); pg.fill('#legs-0-to', 'ONT'); pg.fill('#legs-0-number', 'EA 88')
    pg.check('#legs [data-who][value="person-teo-ramirez"]')
    pg.click('[data-add="stays"]'); pg.fill('#stays-0-name', 'Mission Lodge (fictional)'); pg.fill('#stays-0-checkIn', '2026-11-09')
    pg.click('[data-add="contacts"]')
    pg.fill('#f-emergency', '911')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    row = pg.inner_text('#rows .row:has-text("Anniversary shoot")')
    check('No travel for' in row and 'Lena Ward' in row.split('No travel for')[1] and 'Ruth Hammond' in row.split('No travel for')[1] and 'Teo' not in row.split('No travel for')[1] and 'No hospital' not in row, 'flags people going with no travel')
    trip_id = pg.locator('#rows .row:has-text("Anniversary shoot")').get_attribute('data-id')
    pg.select_option('#printSel', trip_id); pg.select_option('#printWho', 'person-teo-ramirez')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Anniversary shoot: Teo Ramirez' in r and 'MSP to ONT' in r and 'Emergency: 911' in r and 'Ruth reads from the diary' in r, "prints one person's sheet with their travel and shoot days")
    pg.select_option('#printWho', 'person-lena-ward'); pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('MSP to ONT' not in pg.inner_text('#report') and 'Mission Lodge' in pg.inner_text('#report'), "leaves out travel that isn't theirs")
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Trip', 'Type', 'Date'] and len(rows) == 8, 'CSV lists travel, stays and contacts')
    data = saved_project(pg, fake)
    t = next(x for x in data['trips'] if x.get('block') == 'Anniversary shoot')
    check(t['legs'][0]['personIds'] == ['person-teo-ramirez'] and t['legs'][0]['id'] and t['stays'][0]['checkIn'] == '2026-11-09' and 'contacts' not in t and t['emergencyNumber'] == '911',
          'the trip is saved, and empty rows are dropped')
    check(data['trips'][0] == original['trips'][0] and data['shootDays'] == original['shootDays'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_risk_plan(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'risk-plan', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    check('2 rated high' in pg.inner_text('#rows') and pg.inner_text('#uncCount') == '3', 'flags high hazards, and shoot days no plan covers')
    pg.click('#uncovered [data-day="shootday-nov-1"]')
    check(pg.input_value('#f-title') == 'Anniversary shoot' and pg.is_checked('#locPicks input[value="location-hammond-house"]') and pg.locator('#escalation .item').count() == 3 and pg.locator('#hospitals .item').count() == 1,
          'a plan from a shoot day starts with its places, call sheet hospitals and default check-in steps')
    pg.click('[data-add="hazards"]')
    pg.fill('#hazards-0-hazard', 'Heat'); pg.locator('#hazards-0-hazard').dispatch_event('change')
    check(pg.input_value('#hazards-0-controls').startswith('Water and shade'), 'a common hazard suggests what to do')
    pg.select_option('#hazards-0-likelihood', '3'); pg.select_option('#hazards-0-impact', '2'); pg.select_option('#hazards-0-ownerId', 'person-lena-ward')
    check('High (6)' in pg.inner_text('#hazards legend'), 'rates the hazard')
    pg.click('#fromSheetsBtn'); pg.wait_for_timeout(100)
    check(pg.locator('#hospitals .item').count() == 1, "doesn't add the same hospital twice")
    pg.fill('#f-ciTimes', '08:00, 20:00'); pg.fill('#f-ciWho', 'Sam Okafor')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.inner_text('#uncCount') == '1', 'the new plan covers its days')
    plan_id = pg.locator('#rows .row:has-text("Anniversary shoot")').get_attribute('data-id')
    pg.select_option('#printSel', plan_id)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('If someone misses a check-in' in r and 'Heat' in r and 'Riverside Community Hospital' in r and 'Risk assessment' not in r, 'prints the crew copy')
    pg.click('#insurerBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Risk assessment' in r and 'High (6)' in r and 'Signed for the production' in r and 'Lena Ward' in r, "prints the insurer's copy")
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Plan', 'Kind of shoot', 'Hazard'] and len(rows) == 5, 'CSV lists every hazard')
    data = saved_project(pg, fake)
    p = next(x for x in data['riskPlans'] if x['id'] == plan_id)
    h = p['hazards'][0]
    check(h['likelihood'] == 3 and h['impact'] == 2 and h['ownerId'] == 'person-lena-ward' and len(p['checkIns']['escalation']) == 3 and p['checkIns']['times'] == '08:00, 20:00' and 'escalation' not in p,
          'the plan is saved with its hazards and check-ins')
    check(data['riskPlans'][0] == original['riskPlans'][0] and data['people'] == original['people'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_security_checklist(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'security-checklist', fake)
    open_sample(pg, fake)
    check(pg.inner_text('#count') == '29 items · 4 people' and '3 of 29' in pg.inner_text('#progress'), 'shows the checklist and who has done what')
    pg.click('#highBtn'); pg.wait_for_timeout(100)
    check(pg.inner_text('#count').startswith('36 items') and pg.locator('.high-note').count() == 6, 'a high-risk shoot adds items and notes')
    pg.select_option('#whoSel', 'person-lena-ward')
    pg.check('#chk-dev-phone'); pg.wait_for_timeout(100)
    check('2 of 36' in pg.inner_text('#progress li:has-text("Lena Ward")'), 'ticks an item off for one person')
    pg.click('[data-hide="phy-lost"]'); pg.wait_for_timeout(100)
    check(pg.is_visible('#hiddenLine') and pg.inner_text('#count').startswith('35 items'), 'sets aside an item')
    pg.click('#addBtn'); pg.fill('#f-text', 'Agree a code word for when someone can’t talk freely'); pg.select_option('#f-section', 'borders'); pg.check('#f-high')
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check('Agree a code word' in pg.inner_text('#sections') and pg.inner_text('#count').startswith('36 items'), 'adds your own item')
    pg.click('#crewBtn'); pg.click('#crewFromShoot')
    check(pg.is_checked('#crewPicks input[value="person-teo-ramirez"]') and not pg.is_checked('#crewPicks input[value="person-ruth-hammond"]'), 'ticks the crew, not people on camera')
    pg.check('#crewPicks input[value="person-sam-okafor"]'); pg.click('#crewForm button[type="submit"]'); pg.wait_for_timeout(100)
    pg.fill('#planNotes', 'Signal only.'); pg.locator('#planNotes').dispatch_event('change')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('High-risk shoot:' in r and 'Sam Okafor' in r and '✓' in r and 'Signal only.' in r, 'prints the checklist with a tick for each person')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Section', 'Item', 'For high-risk shoots', 'Person', 'Done'] and len(rows) == 1 + 36 * 5, 'CSV has a row for each item and person')
    data = saved_project(pg, fake)
    sec = data['security']
    check(sec['level'] == 'high' and 'person-lena-ward' in sec['done']['dev-phone'] and sec['hidden'] == ['phy-lost'] and len(sec['items']) == 2 and sec['items'][1]['high'] is True
          and 'person-sam-okafor' in sec['personIds'] and sec['notes'] == 'Signal only.', 'the checklist is saved')
    check(data['people'] == original['people'] and data['trips'] == original['trips'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_camera_sound(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'camera-sound-reports', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    check(pg.locator('#days .row').count() == 2 and 'A001C001 to A001C004' in pg.inner_text('#days') and pg.inner_text('#missCount') == '1', 'lists reports by day, and shoot days with none')
    pg.click('#missing [data-day="shootday-may-2"]')
    check(pg.input_value('#f-roll') == 'A002' and pg.input_value('#f-device') == 'A camera' and pg.input_value('#f-codec') == 'ProRes 422 HQ' and pg.input_value('#f-date') == '2026-05-13' and not pg.is_visible('#sheetNote'),
          'a new report takes the next card name and the last settings')
    pg.click('[data-add="clips"]'); pg.fill('#clips-0-clip', 'A002C001'); pg.fill('#clips-0-subject', 'Levee crew'); pg.check('#clips-0-good')
    pg.fill('#f-path', 'footage/2026-05-13/A002'); pg.check('#f-backed')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Every shoot day so far has a report' in pg.inner_text('#missing'), 'the day now has a report')
    pg.click('#addSoundBtn')
    check(pg.input_value('#f-kind') == 'sound' and pg.input_value('#f-roll') == 'S002' and pg.is_visible('#f-layout') and not pg.is_visible('#f-codec'), 'a sound report asks for sound settings')
    pg.select_option('#f-day', 'shootday-may-1')
    check(pg.is_visible('#sheetNote') and 'Day 1 of 2' in pg.inner_text('#sheetNote'), 'links to the call sheet for the day')
    pg.click('[data-add="clips"]')
    check(pg.input_value('#clips-0-lens') == '1 mix, 2 boom, 3 lav (Daniel)', 'a new file starts with the track layout')
    pg.fill('#clips-0-clip', 'S002T01')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.select_option('#printSel', 'day:shootday-may-1')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Camera report: A001' in r and 'Sound report: S002' in r and 'Day 1 of 2' in r and 'A002' not in r, "prints a day's reports")
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Date', 'Shoot day', 'Report', 'Card or roll'] and len(rows) == 9, 'CSV for the edit has a row for each clip and file')
    data = saved_project(pg, fake)
    rs = {r['roll']: r for r in data['mediaReports']}
    a = next(x for x in data['assets'] if x['id'] == rs['A002']['assetId'])
    check(rs['A002']['shootDayId'] == 'shootday-may-2' and 'callSheetId' not in rs['A002'] and rs['A002']['backedUp'] is True and rs['A002']['clips'][0]['good'] is True
          and a['type'] == 'camera card' and a['relativePath'] == 'footage/2026-05-13/A002', 'the camera report and its card are saved')
    check(rs['S002']['kind'] == 'sound' and rs['S002']['callSheetId'] == 'callsheet-day-1' and 'codec' not in rs['S002'] and rs['S002']['trackLayout'], 'the sound report is saved')
    check(data['interviews'] == original['interviews'] and data['callSheets'] == original['callSheets'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_interview_log(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'interview-log', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    daniel = pg.inner_text('[data-id="interview-daniel"]')
    check(pg.locator('#rows .row').count() == 3 and 'No release on file' in daniel and 'Cards A001, S001' in daniel and 'Release pending' in pg.inner_text('[data-id="interview-leon"]'),
          'lists interviews with their cards and release status')
    pg.click('[data-edit="interview-ruth"]')
    check('Release signed' in pg.inner_text('#releaseNote') and pg.input_value('#f-day') == 'shootday-nov-1' and pg.input_value('#f-loc') == 'location-hammond-house', 'opens a planned interview with its release, day and place')
    pg.fill('#f-cards', 'A010, S010')
    pg.click('[data-add="moments"]'); pg.fill('#moments-0-tc', '00:42:10'); pg.fill('#moments-0-text', 'Reads the entry from the night of the flood'); pg.select_option('#moments-0-beatId', 'beat-ruth-diary'); pg.check('#moments-0-fav')
    pg.click('[data-add="moments"]'); pg.fill('#moments-1-tc', '00:05:00'); pg.fill('#moments-1-text', 'The house she grew up in')
    pg.click('[data-add="moments"]'); pg.fill('#moments-2-tc', '5 min'); pg.fill('#moments-2-text', 'Shows the diary to camera')
    pg.fill('#f-transcript', 'transcripts/ruth-hammond.docx')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.is_visible('#editor'), 'a badly formed timecode is refused')
    pg.fill('#moments-2-tc', '01:02:03')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    ruth = pg.inner_text('[data-id="interview-ruth"]')
    check('Done' in ruth and '3 moments, 1 ★' in ruth and 'Transcript' in ruth and 'A010' in ruth, 'logging moments marks the interview done')
    pg.select_option('#printSel', 'interview-ruth'); pg.check('#favOnly')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Reads the entry' in r and 'The house she grew up in' not in r and 'Why she kept the diary secret' in r, 'prints favorites with their story beat')
    pg.uncheck('#favOnly'); pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check(r.index('The house she grew up in') < r.index('Reads the entry') < r.index('Shows the diary'), 'prints moments in timecode order')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:5] == ['Interview', 'Date', 'Location', 'Cards', 'Timecode'] and len(rows) == 7 and [x[4] for x in rows if x[0] == 'Ruth Hammond'] == ['00:05:00', '00:42:10', '01:02:03'],
          'CSV for the paper edit lists every moment in order')
    pg.click('#addBtn'); pg.select_option('#f-person', '__name'); pg.fill('#f-name', 'Neighbor on Mill Road'); pg.fill('#f-date', '2026-05-13')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Neighbor on Mill Road' in pg.inner_text('#todo'), 'lists interviews filmed but not logged')
    data = saved_project(pg, fake)
    iv = {i['id']: i for i in data['interviews']}
    ruth = iv['interview-ruth']
    t = next(a for a in data['assets'] if a['id'] == ruth['transcriptAssetId'])
    check(ruth['status'] == 'done' and ruth['cards'] == 'A010, S010' and ruth['moments'][0]['beatId'] == 'beat-ruth-diary' and ruth['moments'][0]['fav'] is True and 'locationId' not in ruth
          and t['type'] == 'transcript' and t['relativePath'] == 'transcripts/ruth-hammond.docx', 'the log is saved on the interview')
    orig = next(i for i in original['interviews'] if i['id'] == 'interview-ruth')
    check(ruth['questions'] == orig['questions'] and ruth['beats'] == orig['beats'] and ruth['goal'] == orig['goal'], 'the plan from interview prep is kept')
    check(any(i.get('name') == 'Neighbor on Mill Road' for i in iv.values()) and data['contracts'] == original['contracts'], 'a new interview is saved and other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_footage_log(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'footage-log', fake)
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 4, 'lists the clips')
    pg.select_option('#fPerson', 'person-daniel-okafor')
    check(pg.locator('#rows .row').count() == 2, 'finds clips by who is in them')
    pg.select_option('#fPerson', ''); pg.fill('#q', 'sandbags')
    check(pg.locator('#rows .row').count() == 1 and 'A002C001' in pg.inner_text('#rows'), 'finds clips by words')
    pg.fill('#q', '')
    pg.click('#importBtn'); pg.click('#reportsBtn'); pg.wait_for_timeout(200)
    row = pg.locator('#rows .row:has-text("A001C004")')
    check(pg.locator('#rows .row').count() == 5 and row.count() == 1 and '★★★★☆' in row.inner_text() and 'Sandbags at the levee gate' in row.inner_text(), 'imports the clips from camera reports that are not in the log')
    pg.click('#importBtn'); pg.fill('#folderPrefix', 'footage/day3')
    folder = pathlib.Path(tempfile.mkdtemp()) / 'B001'
    folder.mkdir()
    (folder / 'B001C001.MOV').write_bytes(b'x'); (folder / 'notes.txt').write_bytes(b'x')
    pg.set_input_files('#folderInput', str(folder))
    pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 6 and pg.locator('#rows .row:has-text("notes.txt")').count() == 0, 'imports the video files in a folder and skips the rest')
    csv_in = 'File Name,Clip Directory,Description,People,Keywords,Rating\r\nB001C002.MOV,footage/day3,Ruth at the window,"Ruth Hammond, Jo Nobody",diary,3\r\nA001C001.mov,footage/2026-05-12/A001,,,,\r\n'
    pg.click('#importBtn'); pg.set_input_files('#csvInput', files=[{'name': 'clips.csv', 'mimeType': 'text/csv', 'buffer': csv_in.encode()}]); pg.wait_for_timeout(300)
    b2 = pg.locator('#rows .row:has-text("B001C002")')
    check(pg.locator('#rows .row').count() == 7 and 'Ruth Hammond' in b2.inner_text() and 'diary' in b2.inner_text() and '★★★☆☆' in b2.inner_text(), 'imports a CSV, matching people by name and skipping clips already logged')
    for name in ['B001C001', 'B001C002']:
        pg.check('#rows .row:has-text("%s") [data-sel]' % name)
    check(pg.is_visible('#selbar') and '2 selected' in pg.inner_text('#selCount'), 'selects several clips')
    pg.click('#tagSelBtn'); pg.select_option('#t-place', 'location-hammond-house'); pg.fill('#t-topics', 'day three'); pg.select_option('#t-rating', '2'); pg.click('#tagSubmit'); pg.wait_for_timeout(200)
    check('Hammond house' in pg.inner_text('#rows .row:has-text("B001C001")') and 'day three' in pg.inner_text('#rows .row:has-text("B001C002")'), 'tags several clips at once')
    pg.click('[data-edit="clip-a001c003"]'); pg.check('#rating input[value="4"]'); pg.fill('#f-topics', 'river, b-roll, high water'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.select_option('#fRating', '4')
    check(pg.locator('#rows .row').count() == 4, 'filters by rating')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Footage log' in pg.inner_text('#report') and '★★★★ and up' in pg.inner_text('#report') and 'A001C003.mov' in pg.inner_text('#report'), 'prints the clips shown')
    pg.select_option('#fRating', '0')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['File Name', 'Clip Directory', 'Date'] and len(rows) == 8 and ['A001C001.mov', 'footage/2026-05-12/A001'] == rows[1][:2], 'CSV has a row for each clip, with its folder')
    data = saved_project(pg, fake)
    cl = {a['name']: a for a in data['assets'] if a.get('type') == 'clip'}
    check(cl['B001C001.MOV']['relativePath'] == 'footage/day3/B001/B001C001.MOV' and cl['B001C001.MOV']['locationIds'] == ['location-hammond-house'] and cl['B001C001.MOV']['rating'] == 2
          and cl['B001C002.MOV']['personIds'] == ['person-ruth-hammond'] and 'Jo Nobody' in cl['B001C002.MOV']['notes'] and cl['A001C003.mov']['rating'] == 4 and cl['A001C004']['mediaReportId'] == 'report-a001',
          'the clips are saved as assets')
    check([a for a in data['assets'] if a.get('type') != 'clip'] == [a for a in original['assets'] if a.get('type') != 'clip'] and data['mediaReports'] == original['mediaReports'], 'other assets and data are unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

VTT_SAMPLE = 'WEBVTT\n\n00:00:01.000 --> 00:00:04.500\n<v Ruth Hammond>I kept it under the floorboards.\n\n00:00:05.000 --> 00:00:09.000\n<v Ruth Hammond>Nobody asked, so I never said.\n\n00:00:10.000 --> 00:00:12.000\n<v Lena Ward>Will you read it?\n'

def test_paper_edit(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'paper-edit', fake)
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#segs .seg').count() == 6 and pg.locator('#scenes .scene').count() == 2 and 'Running time 1:01' in pg.inner_text('#runTime'), 'shows the transcript and the scenes')
    pg.click('#addBtn')
    pg.set_input_files('#f-file', files=[{'name': 'ruth.vtt', 'mimeType': 'text/vtt', 'buffer': VTT_SAMPLE.encode()}]); pg.wait_for_timeout(200)
    check('3 lines read from ruth.vtt, with timecodes' in pg.inner_text('#parseNote') and pg.input_value('#f-name') == 'ruth', 'reads a VTT transcript')
    pg.select_option('#f-interview', 'interview-ruth')
    check(pg.input_value('#f-person') == 'person-ruth-hammond', "the interview fills in the speaker")
    pg.fill('#f-clipname', 'B001C002.mov'); pg.fill('#f-reel', 'B001'); pg.fill('#f-start', '10:00:00:00')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    segs = pg.locator('#segs .seg')
    check(segs.count() == 3 and segs.first.inner_text().startswith('10:00:01:00') and 'Ruth Hammond' in segs.first.inner_text(), 'shows source timecodes from the clip start')
    segs.nth(0).click(); segs.nth(1).click(modifiers=['Shift'])
    check('2 lines picked' in pg.inner_text('#selCount'), 'shift-click picks a run of lines')
    pg.select_option('#sceneSel', '__new'); pg.click('#addBiteBtn'); pg.wait_for_timeout(200)
    s3 = pg.locator('#scenes .scene').nth(2)
    check(pg.locator('#scenes .scene').count() == 3 and '10:00:01:00 to 10:00:09:00' in s3.inner_text() and 'Scene 3' in s3.locator('input').input_value(), 'adds the bite to a new scene with its source in and out')
    check('Scene 3' in segs.first.inner_text(), 'marks lines already in a scene')
    s3.locator('[data-bite]').click()
    pg.fill('#b-in', '10:00:01:30'); pg.click('#biteForm button[type="submit"]')
    check(pg.is_visible('#biteDialog'), 'refuses a timecode with too many frames')
    pg.fill('#b-in', '10:00:01:00'); pg.fill('#b-out', '10:00:08:12'); pg.fill('#b-note', 'Hold on her hands')
    pg.click('#biteForm button[type="submit"]'); pg.wait_for_timeout(200)
    s3.locator('input').fill('The floorboards'); s3.locator('input').dispatch_event('change'); pg.wait_for_timeout(100)
    pg.locator('#scenes .scene').nth(2).locator('[data-smove="-1"]').click(); pg.wait_for_timeout(100)
    check(pg.locator('#scenes .scene').nth(1).locator('input').input_value() == 'The floorboards', 'moves a scene up')
    pg.click('#addBtn')
    pg.set_input_files('#f-file', files=[{'name': 'notes.txt', 'mimeType': 'text/plain', 'buffer': b'Some words without times.\n\nAnother paragraph.\n'}]); pg.wait_for_timeout(200)
    check('no timecodes' in pg.inner_text('#parseNote'), 'warns about a transcript with no timecodes')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.is_visible('#untimedNote') and pg.locator('#segs .seg').count() == 2, 'imports it as paragraphs')
    pg.locator('#segs .seg').first.click(); pg.select_option('#sceneSel', 'scene-shoebox'); pg.click('#addBiteBtn'); pg.wait_for_timeout(200)
    with pg.expect_download() as d:
        pg.click('#edlBtn')
    edl = open(d.value.path(), encoding='utf-8', newline='').read().split('\r\n')
    events = [l for l in edl if re.match(r'^\d{3}  ', l)]
    check(edl[0] == 'TITLE: The River Keeps paper edit' and edl[1] == 'FCM: NON-DROP FRAME' and len(events) == 4, 'the edit list has a title and one event for each timed bite')
    check(events[0] == '001  A001     AA/V  C        08:04:20:05 08:04:47:23 01:00:00:00 01:00:27:18' and '* FROM CLIP NAME: A001C001.mov' in edl, 'events keep the source timecodes and the clip name')
    check(events[1] == '002  B001     AA/V  C        10:00:01:00 10:00:08:12 01:00:27:18 01:00:35:06', 'a trimmed bite keeps its new in and out, and record times follow on')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Scene', 'Order', 'Speaker'] and len(rows) == 6 and rows[-1][8] == '', 'CSV lists every bite; one without timecode has none')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('The floorboards' in r and '10:00:08:12' in r and 'Hold on her hands' in r and 'No timecode' in r, 'prints the paper edit')
    data = saved_project(pg, fake)
    pe = data['paperEdit']
    ruth = next(t for t in pe['transcripts'] if t.get('interviewId') == 'interview-ruth')
    b = next(s for s in pe['scenes'] if s['title'] == 'The floorboards')['bites'][0]
    check(len(pe['transcripts']) == 3 and ruth['segments'][0]['speaker'] == 'Ruth Hammond' and ruth['startTc'] == '10:00:00:00' and ruth['format'] == 'vtt', 'the transcript is saved')
    check(b['in'] == 1 and abs(b['out'] - 8.509) < 0.002 and b['tcOut'] == '10:00:08:12' and b['reel'] == 'B001' and b['note'] == 'Hold on her hands', 'the bite is saved with its source in and out')
    check(data['interviews'] == original['interviews'] and data['assets'] == original['assets'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_structure_board(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'structure-board', fake)
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    order = lambda sel: [x.get_attribute('data-card') for x in pg.locator(sel + ' > [data-card]').all()]
    check(pg.locator('[data-card]').count() == 7 and order('#drop-tray') == ['card-leon'] and '4:13' in pg.inner_text('[data-actbox="act-1"] .time'), 'shows acts, sequences, cards and running times')
    pg.click('[data-card="card-diary-night"] [data-move="-1"]'); pg.wait_for_timeout(100)
    check(order('.drop[data-seq="sequence-1965"]') == ['card-diary-night', 'card-roof'], 'moves a card with its arrows')
    pg.drag_and_drop('[data-card="card-leon"]', '.drop[data-act="act-3"][data-seq=""]'); pg.wait_for_timeout(200)
    check(sorted(order('.drop[data-act="act-3"][data-seq=""]')) == ['card-crew', 'card-leon'] and order('#drop-tray') == [], 'drags a card into an act')
    pg.drag_and_drop('[data-card="card-leon"]', '[data-card="card-crew"]', target_position={'x': 20, 'y': 4}); pg.wait_for_timeout(200)
    check(order('.drop[data-act="act-3"][data-seq=""]') == ['card-leon', 'card-crew'], 'drops a card before another')
    pg.drag_and_drop('[data-card="card-leon"]', '[data-card="card-crew"]', target_position={'x': 20, 'y': 60}); pg.wait_for_timeout(200)
    check(order('.drop[data-act="act-3"][data-seq=""]') == ['card-crew', 'card-leon'], 'drops a card after another')
    pg.click('#threadsBtn'); pg.click('#addThreadBtn')
    pg.fill('#tn-3', 'Marcus'); pg.select_option('#tc-3', 'red'); pg.select_option('#tp-3', 'person-marcus-bell')
    pg.click('#threadForm button[type="submit"]'); pg.wait_for_timeout(100)
    check('Marcus' in pg.inner_text('#legend'), 'adds a story thread linked to a person')
    pg.click('#addBtn'); pg.fill('#f-title', 'Ruth at the window'); pg.fill('#f-time', '1:45')
    pg.select_option('#f-act', 'act-2'); pg.select_option('#f-seq', 'sequence-boxes'); pg.check('#thPicks input[value="thread-ruth"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    new_id = pg.locator('.drop[data-seq="sequence-boxes"] > [data-card]').last.get_attribute('data-card')
    check(len(order('.drop[data-seq="sequence-boxes"]')) == 3 and 'Ruth at the window' in pg.inner_text('[data-card="%s"]' % new_id), 'adds a card to a sequence')
    pg.select_option('#hl', 'thread-ruth')
    check(pg.locator('.card-s.dim').count() == 5, 'highlights one thread')
    pg.select_option('#hl', '')
    pg.click('[data-actbox="act-3"] [data-addseq]'); pg.wait_for_timeout(100)
    check(pg.locator('[data-actbox="act-3"] .seq').count() == 1, 'adds a sequence to an act')
    pg.click('[data-actbox="act-3"] [data-seqremove]'); pg.wait_for_timeout(100)
    check(not pg.is_visible('#fromPeBtn'), 'offers paper edit scenes only when some have no card')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Act', 'Sequence', 'Order', 'Scene'] and len(rows) == 9 and rows[1][0] == 'Act one: the water' and rows[-1][3] == 'Leon at the grain elevator', 'CSV lists the cards in board order')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Act two: what was kept' in r and 'Boxes and closets' in r and 'Ruth at the window' in r and 'Not on the board yet' not in r, 'prints the board')
    data = saved_project(pg, fake)
    st = data['structure']
    ids = [c['id'] for c in st['cards']]
    new = next(c for c in st['cards'] if c['title'] == 'Ruth at the window')
    leon = next(c for c in st['cards'] if c['id'] == 'card-leon')
    check(ids.index('card-diary-night') < ids.index('card-roof') and leon['actId'] == 'act-3' and ids.index('card-crew') < ids.index('card-leon') and new['sequenceId'] == 'sequence-boxes' and new['seconds'] == 105
          and new['threadIds'] == ['thread-ruth'] and len(st['threads']) == 4 and st['threads'][3]['personId'] == 'person-marcus-bell' and len(st['sequences']) == 2, 'the board is saved')
    check(data['paperEdit'] == original['paperEdit'] and data['people'] == original['people'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_cut_tracker(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'cut-tracker', fake)
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3 and 'Locked cut v12' in pg.inner_text('#lockedBox') and '1 deferred' in pg.inner_text('[data-id="cut-fine-3"]'), 'lists the cuts and the locked cut')
    pg.click('#addBtn')
    check(pg.input_value('#f-name') == 'Locked cut v13', 'a new cut takes the next number')
    pg.fill('#f-name', 'Fine cut 4'); pg.fill('#f-date', '2026-10-01'); pg.locator('#f-date').dispatch_event('change')
    check(pg.is_visible('#carryNote') and '1 note' in pg.inner_text('#carryText'), 'offers to carry notes still open in earlier cuts')
    pg.click('#carryBtn')
    check(pg.locator('#notes .item').count() == 1 and 'from Fine cut 3' in pg.inner_text('#notes legend'), 'carries the note in')
    pg.click('[data-add="screenings"]'); pg.fill('#screenings-0-date', '2026-10-05'); pg.fill('#screenings-0-audience', 'Lena and Priya')
    pg.locator('#screenings-0-audience').dispatch_event('change')
    pg.click('[data-add="notes"]'); pg.fill('#notes-1-tc', '45 min'); pg.select_option('#notes-1-cardId', 'card-secret'); pg.fill('#notes-1-text', 'Trim the pause before she answers'); pg.fill('#notes-1-from', 'Lena')
    check(pg.locator('#notes-1-screeningId option').count() == 2, 'a note can name the screening it came from')
    pg.fill('#f-rt', '1:25:10')
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'refuses a badly formed time in the cut')
    pg.fill('#notes-1-tc', '0:45:00')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    new = pg.locator('#rows .row:has-text("Fine cut 4")')
    check('2 to do' in new.inner_text() and '1 carried' in pg.inner_text('[data-id="cut-fine-3"]'), 'the original note is marked carried')
    new.locator('[data-edit]').click(); pg.check('#f-locked'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Fine cut 4' in pg.inner_text('#lockedBox') and 'Fine cut 4, Oct 1, 2026' in pg.inner_text('#lockedBox') and pg.locator('#rows .st-locked').count() == 1, 'locking a cut sets the project cut version')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Fine cut 4: notes' in r and 'From Fine cut 3' in r and 'Trim the pause' in r and 'Why she kept it secret' in r, "prints a cut's notes")
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Cut', 'Cut date', 'Running time'] and len(rows) == 9, 'CSV lists every note')
    data = saved_project(pg, fake)
    cs = {c['id']: c for c in data['cuts']}
    f4 = next(c for c in data['cuts'] if c['name'] == 'Fine cut 4')
    old = next(n for n in cs['cut-fine-3']['notes'] if n['id'] == 'note-f3-3')
    check(old['status'] == 'carried' and old['carriedToCutId'] == f4['id'] and f4['notes'][0]['carriedFromNoteId'] == 'note-f3-3' and f4['notes'][1]['cardId'] == 'card-secret' and f4['notes'][1]['screeningId'] == f4['screenings'][0]['id'],
          'the notes and screening are saved')
    check(f4['locked'] is True and 'locked' not in cs['cut-locked-12'] and data['project']['cutVersion'] == 'Fine cut 4, Oct 1, 2026' and data['project']['runningTime'] == '1:25:10', 'the locked cut and project are saved')
    check(data['structure'] == original['structure'] and data['contracts'] == original['contracts'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_budget_actuals(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'budget-to-actuals', fake)
    open_sample(pg, fake)
    check('(4)' in pg.inner_text('#addBtn') and 'Drone with operator' in pg.inner_text('#over') and '$600' in pg.inner_text('#over'), 'flags expenses to assign and lines over budget')
    check('$9,118 spent of $452,260' in pg.inner_text('#meterText'), 'totals what is spent against the budget')
    pg.click('#addBtn'); pg.select_option('#as-expense-motel', 'line-2200-10'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('(3)' in pg.inner_text('#addBtn') and '$1,080.00' in pg.inner_text('tr:has([data-line="line-2200-10"])'), 'assigns an expense to its line')
    pg.click('[data-line="line-3000-16"]'); pg.fill('#l-etc', '80000'); pg.fill('#l-note', 'Two more weeks of editing'); pg.click('#lineForm button[type="submit"]'); pg.wait_for_timeout(200)
    check('$6,080 over' in pg.inner_text('tr:has([data-line="line-3000-16"])') and pg.inner_text('#overCount') == '2', 'an estimate to complete changes the variance')
    pg.fill('#asOf', '2026-05-13'); pg.locator('#asOf').dispatch_event('change'); pg.wait_for_timeout(100)
    check('$3,196 spent' in pg.inner_text('#meterText'), 'reports as of a date')
    pg.fill('#asOf', ''); pg.locator('#asOf').dispatch_event('change'); pg.wait_for_timeout(100)
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    drone = next(r for r in rows if r[2] == 'Drone with operator')
    check(rows[0][:4] == ['Section', 'Account', 'Line', 'Budget'] and drone[4] == '3000.00' and drone[7] == '-600.00' and rows[-1][0] == 'Total', 'CSV has every line and the total')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Cost report' in r and 'Summary' in r and 'Two more weeks of editing' in r and 'Contingency 10%' in r, 'prints the cost report')
    data = saved_project(pg, fake)
    ex = {e['id']: e for e in data['expenses']}
    check(ex['expense-motel']['budgetLineId'] == 'line-2200-10' and 'budgetLineId' not in ex['expense-lunch'] and any(e.get('lineId') == 'line-3000-16' and e['toComplete'] == 80000 for e in data['costReport']['estimates']) and 'asOf' not in data['costReport'],
          'the assignment and estimate are saved')
    check(data['budget'] == original['budget'] and [e for e in data['expenses'] if e['id'] != 'expense-motel'] == [e for e in original['expenses'] if e['id'] != 'expense-motel'], 'the budget and other expenses are unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    # An expense with no budget account counts in the total, outside the budget.
    loose = json.loads(sample); loose['expenses'].append({'id': 'expense-loose', 'date': '2026-06-01', 'amount': 10, 'description': 'Parking'})
    ctx, pg, errs = new_page(browser, 'budget-to-actuals', False)
    pg.set_input_files('#fileInput', files=[{'name': 'p.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(loose).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    check(pg.is_visible('#looseCard') and 'Parking' in pg.inner_text('#loose') and '$9,128 spent' in pg.inner_text('#meterText'), 'expenses outside the budget are listed and counted')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_fair_use(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'fair-use-log', fake, fixed_today('2026-11-07'))
    open_sample(pg, fake)
    row = pg.inner_text('[data-id="sample-04"]')
    check(pg.locator('#rows .row').count() == 1 and 'Ready for the attorney' in row and '4 of 4 factors written' in row and '4 seconds' in row, 'lists the elements marked fair use in the clearance log')
    check(pg.locator('#maybe li').count() == 4, 'lists elements not cleared another way')
    pg.click('#addBtn')
    check('Riverside Courier (defunct)' in pg.inner_text('#facts') and pg.is_visible('#whereWarn'), 'opens the next element with its clearance log details, and warns about countries outside the US')
    pg.select_option('#f-where', 'us')
    check(not pg.is_visible('#whereWarn'), 'no warning for the US only')
    pg.select_option('#f-where', 'outside'); pg.select_option('#f-status', 'reviewed'); pg.fill('#f-attorney', '')
    pg.click('#editorSubmit')
    check(pg.is_visible('#editor'), 'a reviewed memo needs the attorney')
    pg.fill('#f-attorney', 'J. Rivera, Esq.'); pg.fill('#f-advice', 'Comfortable with the use as cut')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Reviewed' in pg.inner_text('[data-id="sample-04"]'), 'saves the review')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check(r.startswith('Not legal advice.') and 'Purpose and character of the use' in r and 'Outside the United States only' in r and 'J. Rivera, Esq.' in r, 'prints a draft memo with the notice first')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Element', 'Type', 'Source'] and len(rows) == 2, 'CSV lists the fair use elements')
    data = saved_project(pg, fake)
    e = next(x for x in data['thirdPartyElements'] if x['id'] == 'sample-04')
    o = next(x for x in original['thirdPartyElements'] if x['id'] == 'sample-04')
    check(e['fairUse']['status'] == 'reviewed' and e['fairUse']['reviewedDate'] == '2026-11-07' and e['fairUse']['where'] == 'outside' and e['fairUse']['purpose'] == o['fairUse']['purpose'], 'the review is saved on the element')
    check({k: v for k, v in e.items() if k not in ('fairUse', 'updatedAt')} == {k: v for k, v in o.items() if k != 'fairUse'} and data['contracts'] == original['contracts'], 'the element and other data are otherwise unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_license_tracker(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'license-tracker', fake, fixed_today('2026-11-07'))
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3 and 'Payment due Nov 20, 2026' in pg.inner_text('#due') and '$4,850' in pg.inner_text('#fees'), 'lists licenses, what is coming up and the fees')
    pg.click('[data-filter="music"]')
    check(pg.locator('#rows .row').count() == 2, 'filters to music')
    pg.click('[data-filter="all"]')
    pg.click('#addBtn')
    pg.fill('#f-title', 'Channel 6, 1993 flood report'); pg.select_option('#f-kind', 'archival'); pg.fill('#f-licensor', 'Channel 6')
    pg.check('#elPicks input[value="sample-08"]')
    pg.fill('#f-media', 'All media'); pg.fill('#f-territory', 'Worldwide'); pg.fill('#f-term', '10 years'); pg.fill('#f-start', '2026-12-01'); pg.fill('#f-end', '2036-11-30'); pg.fill('#f-fee', '900')
    pg.click('[data-add="payments"]'); pg.fill('#payments-0-amount', '450'); pg.fill('#payments-0-due', '2026-11-01')
    pg.click('[data-add="options"]'); pg.fill('#options-0-what', 'Add educational use'); pg.fill('#options-0-fee', '200'); pg.fill('#options-0-deadline', '2026-12-20')
    pg.fill('#f-doc', 'licenses/channel6.pdf')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    due = pg.inner_text('#due')
    check('Payment overdue since Nov 1, 2026: $450' in due and 'Exercise by Dec 20, 2026: Add educational use' in due, 'flags an overdue payment and an option to exercise soon')
    pg.click('[data-edit="contract-muddy-water-license"]'); pg.check('#payments-0-paid'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Nov 20' not in pg.inner_text('#due') and '$1,750 paid of $3,500' in pg.inner_text('[data-id="contract-muddy-water-license"]'), 'marks a payment paid')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('License schedule' in r and 'Channel 6, 1993 flood report' in r and 'Add educational use' in r and 'Payments' in r, 'prints the license schedule')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['License', 'Kind', 'Licensor'] and len(rows) == 5, 'CSV lists every license')
    data = saved_project(pg, fake)
    lic = next(c for c in data['contracts'] if c.get('title') == 'Channel 6, 1993 flood report')
    el = next(e for e in data['thirdPartyElements'] if e['id'] == 'sample-08')
    mw = next(c for c in data['contracts'] if c['id'] == 'contract-muddy-water-license')
    a = next(x for x in data['assets'] if x['id'] in lic['assetIds'])
    check(lic['type'] == 'license' and lic['thirdPartyElementIds'] == ['sample-08'] and lic['payments'][0]['amount'] == 450 and lic['options'][0]['deadline'] == '2026-12-20' and lic['id'] in el['contractIds']
          and a['type'] == 'license' and a['relativePath'] == 'licenses/channel6.pdf', 'the license is saved and linked to its element')
    check(mw['payments'][0]['paid'] is True and mw['payments'][0]['paidDate'] == '2026-11-07', 'the payment is saved as paid')
    check([c for c in data['contracts'] if c.get('type') != 'license'] == [c for c in original['contracts'] if c.get('type') != 'license'], 'other contracts are unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

VTT_CLEAR = 'WEBVTT\n\n00:00:01.000 --> 00:00:05.000\nWe spoke with Ruth Hammond at the Hammond house.\n\n00:00:06.000 --> 00:00:10.000\nThen Muddy Water Hymn came on the radio.\n'

def test_clearance_report(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'clearance-report', fake)
    open_sample(pg, fake)
    check(pg.locator('#lines > li').count() == 6 and '7 marks · 4 not cleared' in pg.inner_text('#count') and pg.locator('#open li').count() == 4, 'shows the script, its marks and what is not cleared')
    check('Riverside Courier (defunct)' not in pg.inner_text('#open') and 'Leon Pryor: Release not signed yet' in pg.inner_text('#open'), 'reads clearances from the clearance log and releases')
    pg.click('#addBtn')
    pg.set_input_files('#f-file', files=[{'name': 'act-two.vtt', 'mimeType': 'text/vtt', 'buffer': VTT_CLEAR.encode()}]); pg.wait_for_timeout(200)
    check('2 lines read from act-two.vtt, with timecodes' in pg.inner_text('#parseNote'), 'reads a VTT script')
    pg.fill('#f-start', '01:10:00:00')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#lines > li').count() == 2 and pg.locator('#lines > li').first.inner_text().startswith('01:10:01:00'), 'shows program timecode for each line')
    pg.click('#findBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#lines .chip').count() == 3, 'finds the names of people, places and music from the project')
    pg.locator('#lines [data-mark]').nth(1).click()
    pg.fill('#m-words', 'television'); pg.select_option('#m-kind', 'product')
    pg.click('#markForm button[type="submit"]')
    check(pg.is_visible('#markDialog'), 'refuses words that are not in the line')
    pg.fill('#m-words', 'the radio'); pg.select_option('#m-override', 'cleared'); pg.fill('#m-note', 'A generic radio, no brand visible')
    check('Cleared: A generic radio' in pg.inner_text('#markStatus'), 'shows the clearance as you mark')
    pg.click('#markForm button[type="submit"]'); pg.wait_for_timeout(200)
    check(pg.locator('#lines .chip').count() == 4 and pg.locator('#open li').count() == 2 and 'Ruth Hammond' not in pg.inner_text('#open'), 'a signed release clears a person; a pending one does not')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Annotated script: clearance report' in r and '[1] Person: Ruth Hammond: Release signed' in r and 'NOT CLEARED' in r and 'Not cleared yet' in r and '01:10:06:00' in r, 'prints the report')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Timecode', 'Speaker', 'Line', 'Marked words'] and len(rows) == 5, 'CSV has a row for each mark')
    data = saved_project(pg, fake)
    sc = data['clearanceReport']['scripts']
    new = next(x for x in sc if x['name'] == 'act-two')
    ruth = next(m for m in new['marks'] if m['words'] == 'Ruth Hammond')
    radio = next(m for m in new['marks'] if m['words'] == 'the radio')
    check(new['startTc'] == '01:10:00:00' and len(new['marks']) == 4 and ruth['personId'] == 'person-ruth-hammond' and ruth['auto'] is True and radio['override'] == 'cleared' and radio['kind'] == 'product', 'the script and marks are saved')
    check(sc[0] == original['clearanceReport']['scripts'][0] and data['contracts'] == original['contracts'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_chain_of_title(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'chain-of-title', fake)
    open_sample(pg, fake)
    miss = pg.inner_text('#missing')
    check('Composer agreement' in miss and 'Appearance release: Daniel Okafor' in miss and 'Fair use opinion letter' in miss and 'Muddy Water Hymn' in miss, 'flags what is missing, from the project and the checklist')
    check('In hand' in pg.inner_text('[data-key="ot-eo"]') and 'legal/eo-certificate-2026.pdf' in pg.inner_text('[data-key="ot-eo"]') and 'Not needed' in pg.inner_text('[data-key="ul-option"]'), 'shows linked documents and items not needed')
    check('2 of 3 deal memos not signed' in pg.inner_text('[data-key="ag-crew"]'), 'works out the crew deal memos from the project')
    before = pg.inner_text('#count')
    pg.click('[data-edit="contract:contract-pryor-appearance"]')
    check('Missing, from the project: Not signed yet' in pg.inner_text('#autoNote'), 'explains a status from the project')
    pg.click('#editorCancel')
    pg.click('[data-edit="cr-film"]'); pg.select_option('#f-status', ''); pg.fill('#f-path', 'legal/copyright-certificate.pdf'); pg.fill('#f-note', 'Registered Nov 2026')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('In hand' in pg.inner_text('[data-key="cr-film"]'), 'linking a document puts an item in hand')
    pg.click('[data-edit="ag-finance"]'); pg.select_option('#f-status', 'na'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#addBtn'); pg.fill('#f-title', 'Distribution agreement'); pg.select_option('#f-section', 'agreements'); pg.fill('#f-path', 'legal/distribution.pdf')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('[data-key] .nm:has-text("Distribution agreement")').count() == 1 and pg.inner_text('#count') != before, 'adds your own item')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Chain of title' in r and 'Tab' in r and 'MISSING' in r and 'Distribution agreement' in r and 'legal/copyright-certificate.pdf' in r and 'Co-production' not in r, 'prints the index and cover sheets, without items not needed')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Tab', 'Section', 'Document', 'Status'] and len(rows) == pg.locator('#sections .row').count() + 1, 'CSV lists every item')
    data = saved_project(pg, fake)
    it = {x['key']: x for x in data['chainOfTitle']['items']}
    a = next(x for x in data['assets'] if x['id'] == it['cr-film']['assetIds'][0])
    custom = next(x for x in data['chainOfTitle']['items'] if x.get('custom'))
    check(a['type'] == 'chain of title document' and a['relativePath'] == 'legal/copyright-certificate.pdf' and 'status' not in it['cr-film'] and it['ag-finance']['status'] == 'na' and custom['title'] == 'Distribution agreement' and custom['section'] == 'agreements', 'the binder is saved')
    check(data['contracts'] == original['contracts'] and data['people'] == original['people'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_deal_memos(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'deal-memos', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3 and 'In the budget' in pg.inner_text('[data-id="contract-deal-teo"]') and 'Not in the budget yet' in pg.inner_text('[data-id="contract-deal-priya"]'),
          'lists deal memos with their place in the budget')
    check('Priya Nair' in pg.inner_text('#waiting') and 'Lena Ward' in pg.inner_text('#crew'), 'lists memos waiting for a signature, and crew without one')

    pg.click('[data-for="person-lena-ward"]')
    check(pg.input_value('#f-role') == 'Director' and pg.is_visible('#calNote') and '4 days' in pg.inner_text('#calText'), 'fills in the role, and finds their days in the shooting calendar')
    pg.click('#calBtn')
    pg.fill('#f-rate', '900'); pg.locator('#f-rate').dispatch_event('input')
    check(pg.input_value('#f-start') == '2026-05-12' and pg.input_value('#f-guarantee') == '4' and pg.input_value('#f-total') == '$3,600', 'uses the calendar dates and works out the total')
    pg.fill('#f-credit', 'Directed by Lena Ward')
    pg.select_option('#f-account', 'account-1300'); pg.select_option('#f-fringe', 'fringe-payroll'); pg.select_option('#f-status', 'sent')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)
    check('In the budget' in pg.inner_text('#rows .row:has-text("Lena Ward")'), 'sends the rate to the budget')

    pg.click('[data-edit="contract-deal-teo"]')
    pg.fill('#f-rate', '800')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)
    pg.click('#addBtn')
    pg.select_option('#f-person', '__new'); pg.fill('#f-pname', 'Jo Park'); pg.fill('#f-role', 'Sound recordist'); pg.fill('#f-rate', '550')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)
    pg.click('[data-edit="contract-deal-priya"]')
    pg.set_input_files('#scanInput', files=[{'name': 'priya signed.pdf', 'mimeType': 'application/pdf', 'buffer': b'%PDF-1.4 sample'}])
    check(pg.input_value('#f-status') == 'signed', 'attaching a signed copy marks the memo signed')
    pg.click('#editorSubmit'); pg.wait_for_timeout(300)

    pg.select_option('#printSel', 'contract-deal-teo')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check(r.startswith('Not legal advice') and 'written for California, USA' in r and '$800 a day' in r and 'Crew member' in r, 'prints the memo to sign, with the notice first')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Name', 'Role', 'Status'] and len(rows) == 6, 'CSV lists every deal memo')
    data = saved_project(pg, fake)
    memos = {c['id']: c for c in data['contracts'] if c.get('type') == 'deal memo'}
    lines = {l['id']: l for l in data['budget']['lines']}
    lena = next(c for c in memos.values() if c['personIds'] == ['person-lena-ward'])
    ll = lines[lena['budgetLineIds'][0]]
    check(ll['accountId'] == 'account-1300' and ll['quantity'] == 4 and ll['rate'] == 900 and ll['unit'] == 'Days' and ll['fringeId'] == 'fringe-payroll' and lena['status'] == 'sent' and lena['sentDate'],
          'the new memo and its budget line are saved')
    check(lines['line-2000-5']['rate'] == 800 and lines['line-2000-5']['description'] == 'Cinematographer' and lines['line-2100-7']['accountId'] == 'account-2100',
          'an existing budget line takes the new rate and keeps its account and name')
    jo = next(p for p in data['people'] if p['name'] == 'Jo Park')
    priya = memos['contract-deal-priya']
    scan = next(a for a in data['assets'] if a['id'] == priya['assetIds'][0])
    check(jo['roles'] == ['Sound recordist'] and priya['status'] == 'signed' and scan['type'] == 'signed deal memo' and scan['relativePath'] == 'deal-memos/priya signed.pdf',
          'a new person joins the project, and the signed copy is recorded')
    check(data['locations'] == original['locations'] and [c for c in data['contracts'] if c.get('type') != 'deal memo'] == [c for c in original['contracts'] if c.get('type') != 'deal memo'],
          "other contracts and data are unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()
    # The credits builder checks the credit a deal memo requires.
    ctx, pg, errs = new_page(browser, 'credits-builder', False)
    pg.set_input_files('#fileInput', files=[{'name': 'p.oft.json', 'mimeType': 'application/json', 'buffer': json.dumps(data).encode()}])
    pg.wait_for_function("document.getElementById('filmMeta').textContent.trim() !== ''")
    check('Directed by Lena Ward' in pg.inner_text('body'), "the credits builder lists a deal memo's required credit")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_daily_report(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'daily-production-report', fake, fixed_today('2026-11-01'))
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 1 and '23.5 h total' in pg.inner_text('#rows') and '20 min lost' in pg.inner_text('#rows') and pg.inner_text('#missCount') == '1' and 'May 13' in pg.inner_text('#missing'),
          'lists reports with total hours and minutes lost, and shoot days with none')
    pg.click('#missing [data-day="shootday-may-2"]')
    check(pg.input_value('#f-day') == 'shootday-may-2' and pg.input_value('#f-call') == '' and pg.input_value('#f-wrap') == '' and pg.locator('#crew .item').count() == 0 and 'No call sheet' in pg.inner_text('#sheetNote'),
          'a day with no call sheet starts blank')
    pg.fill('#f-call', '07:30'); pg.fill('#f-wrap', '18:00'); pg.fill('#f-lunch1', '12:30'); pg.fill('#f-lunch2', '13:00')
    pg.click('[data-add="crew"]')
    check(pg.input_value('#crew-0-call') == '07:30' and pg.input_value('#crew-0-wrap') == '18:00' and pg.input_value('#crew-0-mealMinutes') == '30', 'a new person starts with the day\'s call, wrap and lunch')
    pg.select_option('#crew-0-personId', 'person-lena-ward'); pg.fill('#crew-0-role', 'Camera')
    pg.click('[data-add="crew"]')
    pg.fill('#crew-1-name', '=Temp sound'); pg.fill('#crew-1-call', '22:00'); pg.fill('#crew-1-wrap', '02:00'); pg.fill('#crew-1-mealMinutes', '0')
    check('Lena Ward' in pg.inner_text('#crew') and 'wraps next day' in pg.inner_text('#crew') and pg.inner_text('#totals') == 'Total hours: 14 · Minutes lost: 0', 'hours are worked out, less the meal break, and a wrap past midnight counts as the next day')
    pg.fill('#f-shot', 'Pickup shots at the diner')
    pg.click('[data-add="incidents"]'); pg.select_option('#incidents-0-kind', 'equipment'); pg.fill('#incidents-0-time', '10:15'); pg.fill('#incidents-0-minutesLost', '15'); pg.fill('#incidents-0-text', 'Battery failed on the A camera')
    check(pg.inner_text('#totals') == 'Total hours: 14 · Minutes lost: 15', 'minutes lost are totalled')
    pg.fill('#f-call', '25:00'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.is_visible('#editor') and pg.locator('#editor').evaluate('d => d.open'), 'a badly formed time is refused')
    pg.fill('#f-call', '7:30'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(not pg.is_visible('#editor') and pg.locator('#rows .row').count() == 2 and 'Every shoot day so far has a report' in pg.inner_text('#missing'), 'saving the report adds it and clears the shoot day from the list')
    pg.click('[data-edit="dailyreport-may-1"]')
    check(pg.input_value('#f-call') == '07:00' and pg.locator('#crew .item').count() == 3 and pg.locator('#cards input:checked').count() == 2 and pg.inner_text('#totals') == 'Total hours: 23.5 · Minutes lost: 20',
          'opens the existing report with its crew, cards and totals')
    pg.click('[data-add="incidents"]'); pg.fill('#incidents-1-minutesLost', '10'); pg.fill('#incidents-1-text', 'Generator trouble')
    pg.fill('#crew-2-wrap', '13:00')
    check(pg.inner_text('#totals') == 'Total hours: 24.5 · Minutes lost: 30', 'editing a wrap time and adding an incident updates the totals')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.select_option('#printSel', 'dailyreport-may-1')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Daily production report' in r and 'Daniel Okafor' in r and 'Interview subject' in r and '24.5' in r and 'Wind gusts' in r and 'Generator trouble' in r and 'Camera' in r and 'A001' in r and 'S001' in r and 'Battery failed' not in r,
          "prints the chosen day's report with crew, cards and incidents")
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    by = {x[2]: x for x in rows[1:]}
    check(rows[0][:3] == ['Date', 'Shoot day', 'Name'] and len(rows) == 6 and by['Ana Reyes'][7] == '9.75' and by['Daniel Okafor'][7] == '5' and by["'=Temp sound"][7] == '4' and by['Lena Ward'][4] in ('07:00', '07:30'),
          'CSV has crew hours, one row for each person each day, with a guard against formulas')
    data = saved_project(pg, fake)
    rs = {x['id']: x for x in data['dailyReports']}
    new = next(x for x in data['dailyReports'] if x['shootDayId'] == 'shootday-may-2')
    may1 = rs['dailyreport-may-1']
    check(new['callTime'] == '07:30' and new['wrapTime'] == '18:00' and new['lunchStart'] == '12:30' and new['shot'] == 'Pickup shots at the diner' and 'callSheetId' not in new and 'mediaReportIds' not in new
          and new['crew'][0]['personId'] == 'person-lena-ward' and new['crew'][1]['name'] == '=Temp sound' and new['crew'][1]['wrap'] == '02:00' and new['incidents'][0]['kind'] == 'equipment' and new['incidents'][0]['minutesLost'] == 15,
          'the new report is saved')
    check(may1['callSheetId'] == 'callsheet-day-1' and may1['mediaReportIds'] == ['report-a001', 'report-s001'] and len(may1['incidents']) == 2 and may1['crew'][2]['wrap'] == '13:00' and may1['crew'][2]['note'] == 'Morning only' and may1['notes'] == 'Fictional sample report.'
          and 'hours' not in json.dumps(data['dailyReports']).lower(), 'the edited report keeps its other fields and never stores hours')
    check(data['callSheets'] == original['callSheets'] and data['mediaReports'] == original['mediaReports'] and data['people'] == original['people'] and data['shootDays'] == original['shootDays'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

    ctx, pg, errs = new_page(browser, 'daily-production-report', fake, fixed_today('2026-11-01'))
    pg.on('dialog', lambda d: d.accept())
    open_sample(pg, fake)
    pg.click('[data-edit="dailyreport-may-1"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 0 and pg.inner_text('#missCount') == '2' and 'starts from the call sheet' in pg.inner_text('#missing'), 'removing a report puts its day back in the list, which says it starts from the call sheet')
    pg.click('#missing [data-day="shootday-may-1"]')
    check(pg.input_value('#f-call') == '07:00' and pg.input_value('#f-wrap') == '17:00' and pg.input_value('#f-lunch1') == '12:00' and pg.input_value('#f-lunch2') == '13:00' and 'Day 1 of 2' in pg.inner_text('#sheetNote'),
          "a new report starts from the day's call sheet: call, wrap and lunch")
    check(pg.locator('#crew .item').count() == 2 and pg.input_value('#crew-0-personId') == 'person-ana-reyes' and pg.input_value('#crew-0-role') == 'Producer' and pg.input_value('#crew-1-call') == '08:00' and pg.input_value('#crew-0-mealMinutes') == '60'
          and pg.locator('#cards input:checked').count() == 2, 'the call sheet crew and the day\'s cards come across')
    pg.select_option('#f-day', 'shootday-may-2')
    check(pg.input_value('#f-call') == '' and pg.locator('#crew .item').count() == 0, 'choosing another day starts over while nothing is typed')
    pg.select_option('#f-day', 'shootday-may-1')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    data = saved_project(pg, fake)
    r = data['dailyReports'][0]
    check(len(data['dailyReports']) == 1 and r['shootDayId'] == 'shootday-may-1' and r['callSheetId'] == 'callsheet-day-1' and r['callTime'] == '07:00' and r['lunchEnd'] == '13:00' and [c['personId'] for c in r['crew']] == ['person-ana-reyes', 'person-daniel-okafor']
          and r['mediaReportIds'] == ['report-a001', 'report-s001'] and data['callSheets'] == original['callSheets'], 'the report started from the call sheet is saved and the call sheet is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_expense_log(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'expense-log', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    n0 = len(original['expenses']); t0 = sum(e['amount'] for e in original['expenses'])
    check(pg.locator('#rows tr').count() == n0 and '${:,.2f}'.format(t0) in pg.inner_text('#grandTotal'), 'lists expenses and the grand total')
    pg.select_option('#kindFilter', 'perdiem')
    check(pg.locator('#rows tr').count() == 1, 'filters by type')
    pg.select_option('#kindFilter', '')
    pg.fill('#search', 'diner'); check(pg.locator('#rows tr').count() == 1, 'searches expenses'); pg.fill('#search', '')
    pg.click('#addBtn')
    pg.fill('#f-date', '2026-05-13'); pg.fill('#f-amount', '12.50'); pg.select_option('#f-account', 'account-2400')
    pg.fill('#f-description', 'Batteries'); pg.fill('#f-payee', 'Corner Shop (fictional)')
    pg.set_input_files('#f-receipt', {'name': 'Batteries Receipt.jpg', 'mimeType': 'image/jpeg', 'buffer': b'fake'})
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(not pg.is_visible('#editor') and pg.locator('#rows tr').count() == n0 + 1 and 'Batteries Receipt.jpg' in pg.inner_text('#rows'), 'adds an expense with a receipt name')
    pg.click('#addBtn'); pg.select_option('#f-kind', 'perdiem'); pg.fill('#f-amount', '45'); pg.select_option('#f-account', 'account-2400')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.is_visible('#editor'), 'a per diem needs a person')
    pg.select_option('#f-person', 'person-daniel-okafor'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows tr').count() == n0 + 2 and '${:,.2f}'.format(t0 + 57.5) in pg.inner_text('#grandTotal'), 'adds a per diem and updates totals')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Date', 'Amount', 'Kind', 'Budget account'] and len(rows) == n0 + 3 and any('Batteries' in r[6] for r in rows), 'CSV lists every expense')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Batteries' in pg.inner_text('#report'), 'prints the expense report')
    data = saved_project(pg, fake)
    ex = next(e for e in data['expenses'] if e.get('description') == 'Batteries')
    a = next(x for x in data['assets'] if x['id'] == ex['receiptAssetId'])
    check(a['type'] == 'receipt' and a['relativePath'].startswith('receipts/2026-05-13-') and ex['amount'] == 12.5 and ex['accountId'] == 'account-2400', 'saves the expense and the receipt asset')
    check(data['callSheets'] == original['callSheets'] and data['budget'] == original['budget'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_festivals(browser, fake):
    ctx, pg, errs = new_page(browser, 'festival-submissions', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names == ['Riverbend Documentary Festival', 'Northern Light Film Festival', 'Prairie Docs', 'Eastgate Shorts'], 'planned first, then submitted, accepted, declined last %s' % names)
    check('Next screening Mar 12, 2027 · 19:00 · Prairie Theater (fictional)' in pg.inner_text('[data-id="festival-prairie"]') and 'Waiver code RIVER-WAIVE' in pg.inner_text('[data-id="festival-riverbend"]'), 'rows show the next screening and waiver codes')
    check('Mar 12, 2027' in pg.inner_text('#screenList') and pg.locator('#screenList li').count() == 1, 'lists upcoming screenings beside the list')
    check('$60' in pg.inner_text('#stats') and '$45' in pg.inner_text('#stats'), 'adds up planned and submitted fees')
    pg.click('[data-filter="accepted"]')
    check(pg.locator('#rows .row').count() == 1 and 'Accepted 1' in pg.inner_text('#filters'), 'filters by status, with counts')
    pg.click('[data-filter="all"]')
    pg.fill('#search', 'river-waive')
    check(pg.locator('#rows .row').count() == 1, 'searches waiver codes')
    pg.fill('#search', 'theater')
    check(pg.locator('#rows .row').count() == 1 and 'Prairie' in pg.inner_text('#rows'), 'searches screening venues')
    pg.fill('#search', '')

    pg.click('#addBtn')
    check(pg.is_visible('#editor') and not pg.is_visible('#scRows'), 'add opens the editor, with no screenings until accepted')
    pg.fill('#f-name', 'Test Fest'); pg.fill('#f-deadline', '2026-11-10'); pg.fill('#f-fee', '30'); pg.fill('#f-url', 'javascript:alert(1)')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#addBtn')
    pg.fill('#f-name', 'Old Fest'); pg.fill('#f-deadline', '2026-10-25'); pg.fill('#f-url', 'https://example.org/old')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names[:4] == ['Test Fest', 'Riverbend Documentary Festival', 'Old Fest', 'Northern Light Film Festival'], 'upcoming planned deadlines come first, passed ones after %s' % names)
    check('Deadline soon' in pg.inner_text('[data-id]:has-text("Test Fest")') and 'In 9 days' in pg.inner_text('#rows .row >> nth=0'), 'flags a deadline within 14 days')
    old = pg.locator('#rows .row', has_text='Old Fest')
    check('Deadline passed' in old.inner_text() and 'Passed 7 days ago' in old.inner_text() and '2 due' not in pg.inner_text('#count'), 'flags a passed deadline')
    check(old.locator('a[href="https://example.org/old"][rel="noopener noreferrer"]').count() == 1 and pg.locator('#rows a').count() == 2, 'only http and https links are made clickable')
    check('1 due in the next two weeks' in pg.inner_text('#count') and '1 planned deadline passed' in pg.inner_text('#count'), 'counts due and passed deadlines')

    pg.click('#rows .row >> nth=0 >> .what')
    pg.select_option('#f-status', 'submitted')
    check(pg.input_value('#f-submitted') == '2026-11-01', 'submitting defaults the date to today')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('[data-edit="festival-northern-light"]')
    pg.select_option('#f-status', 'accepted')
    check(pg.is_visible('#scRows') or pg.is_visible('#addScreeningBtn'), 'accepted shows the screening dates')
    pg.click('#addScreeningBtn')
    row = pg.locator('#scRows .sc-row').last
    row.locator('.sc-date').fill('2026-12-05'); row.locator('.sc-time').fill('7:30 pm'); row.locator('.sc-venue').fill('Main Hall (fictional)')
    pg.click('#addScreeningBtn')
    pg.locator('#scRows .sc-row').last.locator('.sc-date').fill('2026-12-06')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names[-3:] == ['Northern Light Film Festival', 'Prairie Docs', 'Eastgate Shorts'] and 'Next screening Dec 5, 2026' in pg.inner_text('[data-id="festival-northern-light"]') and '2 screenings' in pg.inner_text('[data-id="festival-northern-light"]'), 'accepted festivals sort by next screening')
    check(pg.locator('#screenList li').count() == 3 and 'Northern Light' in pg.locator('#screenList li').first.inner_text(), 'the screenings list is in date order')
    pg.click('[data-edit="festival-northern-light"]')
    pg.locator('#scRows .sc-row').nth(1).locator('[data-delsc]').click()
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#screenList li').count() == 2, 'removes a screening')

    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    nl = next(r for r in rows if r[0] == 'Northern Light Film Festival')
    check(rows[0] == ['Festival', 'Status', 'Deadline', 'Platform', 'Fee', 'Waiver code', 'Submitted', 'Screenings', 'Link', 'Notes'] and len(rows) == 7
          and nl[1] == 'Accepted' and nl[4] == '45' and nl[7] == '2026-12-05 7:30 pm Main Hall (fictional)' and next(r for r in rows if r[0] == 'Test Fest')[6] == '2026-11-01'
          and next(r for r in rows if r[0] == 'Riverbend Documentary Festival')[5] == 'RIVER-WAIVE', 'CSV lists every festival with fees, waiver codes and screenings')

    pg.click('[data-edit="festival-eastgate"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    rep = pg.inner_text('#report')
    check('Test Fest' in rep and 'Main Hall' in rep and 'Eastgate' not in rep and 'The River Keeps' in rep, 'prints the list')
    data = saved_project(pg, fake)
    f = {x['id']: x for x in data['festivals']}
    check(len(data['festivals']) == 5 and f['festival-northern-light']['status'] == 'accepted' and f['festival-northern-light']['fee'] == 45 and len(f['festival-northern-light']['screenings']) == 1
          and f['festival-prairie']['screenings'][0]['note'] == 'Q&A after' and data['festivals'][-1]['url'] == 'https://example.org/old', 'festivals are saved')
    check(any(x.get('url') == 'javascript:alert(1)' for x in data['festivals']), 'a link that is not http or https is kept as text')
    original = json.loads(sample)
    check(data['people'] == original['people'] and data['grants'] == original['grants'] and data['treatment'] == original['treatment'], "other tools' data is unchanged")
def test_press_list(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'press-list', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names == ['Hammond Gazette', 'Rivers Remembered podcast'] and 'Covered the film' in pg.inner_text('[data-id="outlet-gazette"]'), 'lists outlets with where each stands %s' % names)
    pg.click('[data-filter="none"]')
    check(pg.locator('#rows .row').count() == 1, 'filters outlets with no screener sent')
    pg.click('[data-filter="all"]'); pg.select_option('#beatFilter', 'Local history')
    check(pg.locator('#rows .row').count() == 1 and 'Hammond Gazette' in pg.inner_text('#rows'), 'filters by beat')
    pg.select_option('#beatFilter', ''); pg.fill('#search', 'flood')
    check(pg.locator('#rows .row').count() == 1, 'searches coverage headlines')
    pg.fill('#search', '')
    pg.click('[data-edit="outlet-river-pod"]')
    pg.fill('#shDate', '2026-10-30'); pg.select_option('#shWho', label='Dev Anand'); pg.fill('#shUrl', 'https://screeners.example.org/podcast')
    pg.click('#shAddBtn')
    check('screeners.example.org/podcast' in pg.inner_text('#shLog') and 'To Dev Anand' in pg.inner_text('#shLog'), 'logs a screener sent to a person')
    pg.fill('#scrTitle', 'Press night'); pg.fill('#scrDate', '2027-01-20'); pg.fill('#scrPlace', 'Riverside Cinema'); pg.click('#scrAddBtn')
    check(pg.input_value('#rvScr') != '' and 'Press night' in pg.inner_text('#rvScr'), 'adds a screening and offers it for RSVPs')
    pg.select_option('#rvStatus', 'yes'); pg.select_option('#rvWho', label='Dev Anand'); pg.click('#rvAddBtn')
    check('Press night' in pg.inner_text('#rvLog') and 'Coming' in pg.inner_text('#rvLog'), 'records an RSVP')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Coming to a screening' in pg.inner_text('[data-id="outlet-river-pod"]'), 'an RSVP moves the outlet along')
    pg.click('[data-edit="outlet-river-pod"]')
    pg.fill('#cvDate', '2027-01-25'); pg.select_option('#cvKind', 'review'); pg.fill('#cvHeadline', 'A quiet film about a loud river'); pg.fill('#cvUrl', 'javascript:alert(1)')
    pg.click('#cvAddBtn')
    check(pg.locator('#cvLog a').count() == 0 and 'A quiet film' in pg.inner_text('#cvLog'), 'only web links are made clickable')
    pg.fill('#cvHeadline', 'A quiet film about a loud river'); pg.fill('#cvUrl', 'https://riverspod.example.org/episodes/12')
    pg.click('#cvAddBtn')
    check(pg.locator('#cvLog a').count() == 1, 'a web link is clickable')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Covered the film' in pg.inner_text('[data-id="outlet-river-pod"]') and 'riverspod' not in pg.inner_text('#steps') and 'A quiet film' in pg.inner_text('#steps'), 'logged coverage shows in the list and the sidebar')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    pod = next(r for r in rows if r[0] == 'Rivers Remembered podcast')
    check(rows[0][:3] == ['Outlet', 'Kind', 'Status'] and pod[4] == 'Environment and water' and pod[5] == '1' and 'Press night: Coming (Dev Anand)' in pod[7] and pod[9] == '2027-01-25', 'CSV lists outlets with beats, screeners, RSVPs and coverage')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Hammond Gazette' in pg.inner_text('#report') and 'Local history' in pg.inner_text('#report'), 'prints the list')
    data = saved_project(pg, fake)
    o = {x['id']: x for x in data['pressOutlets']}['outlet-river-pod']
    new = next(s for s in data['screenings'] if s['title'] == 'Press night')
    check(o['screeners'][0]['contactId'] == 'contact-pod-host' and o['rsvps'][0]['screeningId'] == new['id'] and o['rsvps'][0]['status'] == 'yes' and len(o['coverage']) == 2 and o['coverage'][1]['url'].startswith('https://') and new['place'] == 'Riverside Cinema' and len(data['screenings']) == 3, 'the outlet and its screening are saved')
    check(data['pressOutlets'][0] == original['pressOutlets'][0] and data['funders'] == original['funders'] and data['callSheets'] == original['callSheets'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_partner_crm(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'partner-crm', fake, fixed_today('2026-11-01'))
    open_sample(pg, fake)
    names = [t.split('\n')[0] for t in pg.locator('#rows .row .nm').all_inner_texts()]
    check(names == ['River Valley Trust', 'Hammond Public Library'] and 'Library premiere' in pg.inner_text('[data-id="partner-library"]'), 'lists partners, soonest next step first, with their screenings %s' % names)
    check(pg.locator('#scrList li').count() == 2 and '1 partner' in pg.inner_text('#scrList'), 'lists screenings with how many partners are in each')
    pg.click('[data-filter="talking"]')
    check(pg.locator('#rows .row').count() == 1, 'filters by stage')
    pg.click('[data-filter="all"]'); pg.fill('#search', 'priya')
    check(pg.locator('#rows .row').count() == 1, 'searches the people at each partner')
    pg.fill('#search', '')
    pg.click('[data-edit="partner-river-trust"]')
    pg.click('#addContactBtn'); row = pg.locator('#cRows .c-row').last
    row.locator('.c-name').fill('Sam Whitaker'); row.locator('.c-title').fill('Outreach lead')
    pg.click('#addStepBtn'); step = pg.locator('#nRows .n-row').last
    step.locator('.n-due').fill('2026-11-10'); step.locator('.n-by').select_option('them'); step.locator('.n-text').fill('Confirm the panelists')
    pg.check('#scrChecks input[value="screening-library"]')
    pg.fill('#scrTitle', 'Spring panel'); pg.fill('#scrDate', '2027-03-01'); pg.fill('#scrPlace', 'Riverside'); pg.click('#scrAddBtn')
    check('Spring panel' in pg.inner_text('#scrChecks') and pg.is_checked('#scrChecks input:last-of-type'), 'adds a screening and links it')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    t = pg.inner_text('[data-id="partner-river-trust"]')
    check('Next: Confirm the panelists, due Nov 10, 2026' in t and 'Spring panel' in t and 'Library premiere' in t, 'saves people, commitments and screenings')
    pg.click('[data-done="partner-river-trust|commitment-trust-1"]'); pg.wait_for_timeout(200)
    check(pg.locator('#steps li').count() == 2, 'ticking a commitment marks it done')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    trust = next(r for r in rows if r[0] == 'River Valley Trust')
    check(rows[0][:3] == ['Organization', 'Kind', 'Stage'] and 'Sam Whitaker, Outreach lead' in trust[3] and 'Spring panel' in trust[4] and trust[5] == 'Confirm the panelists' and trust[6] == '2026-11-10', 'CSV lists partners with people, screenings and the next step')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Hammond Public Library' in pg.inner_text('#report') and 'Priya Nair' in pg.inner_text('#report'), 'prints the list')
    data = saved_project(pg, fake)
    p = {x['id']: x for x in data['partners']}['partner-river-trust']
    spring = next(s for s in data['screenings'] if s['title'] == 'Spring panel')
    check(set(p['screeningIds']) == {'screening-grain-elevator', 'screening-library', spring['id']} and p['commitments'][0]['done'] is True and p['commitments'][1]['by'] == 'them' and len(data['screenings']) == 3, 'the partner and its screening are saved')
    check(data['partners'][0] == original['partners'][0] and data['pressOutlets'] == original['pressOutlets'] and data['funders'] == original['funders'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_discussion_guide(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'discussion-guide', fake)
    open_sample(pg, fake)
    check('Riverside has flooded three times' in pg.input_value('#synopsis'), 'starts from the treatment synopsis')
    credit_preview = pg.inner_text('#creditsPreview')
    check('Hammond Public Library' in pg.inner_text('#partnerList') and 'Directed by' in credit_preview
          and 'Shall We Gather at the River' in credit_preview and 'Riverbed Ambience 04' in credit_preview
          and 'The River Keeps (Main Title)' not in credit_preview and 'Riverside Courier (defunct)' not in credit_preview,
          'shows project credits, including current music and archival credits')
    pg.fill('#synopsis', 'A screening-specific synopsis for this audience.')
    pg.fill('#themes', 'Memory and history\nCommunity preparedness')
    pg.fill('#questions', 'What moment stayed with you?\nWhat should a town owe its neighbors?')
    pg.fill('#resourceNotes', 'Flood readiness: https://example.org/prepare')
    pg.check('[data-partner="partner-library"]')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    report = pg.inner_text('#report')
    check('A screening-specific synopsis' in report and 'Community preparedness' in report and 'What moment stayed with you?' in report
          and 'Flood readiness' in report and 'Hammond Public Library' in report and 'library.example.org' in report
          and 'Shall We Gather at the River' in report and 'Riverside County Historical Society' in report,
          'prints the synopsis, themes, questions, resources and selected organization')
    data = saved_project(pg, fake)
    guide = data['discussionGuide']
    check(guide['synopsis'] == 'A screening-specific synopsis for this audience.' and guide['themes'] == 'Memory and history\nCommunity preparedness'
          and guide['questions'].startswith('What moment stayed with you?') and guide['resourceNotes'].startswith('Flood readiness')
          and guide['partnerIds'] == ['partner-library'], 'saves the guide content and partner selection')
    check(data['project'] == original['project'] and data['partners'] == original['partners'] and data['credits'] == original['credits']
          and data['treatment'] == original['treatment'], 'source project, partner and credit records stay unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_archive_log(browser, fake):
    original = json.loads(sample)
    original_asset = next(a for a in original['assets'] if a['id'] == 'asset-card-a001')
    ctx, pg, errs = new_page(browser, 'archive-log', fake)
    open_sample(pg, fake)

    pg.click('#addBtn')
    pg.select_option('#f-asset', 'asset-card-a001')
    pg.fill('#f-copyLabel', 'Off-site drive 1')
    pg.fill('#f-copiedAt', '2026-05-13')
    pg.fill('#f-location', 'Locked cabinet, second location')
    pg.fill('#f-hashList', 'SHA256 A001/clip001.mov abc123')
    pg.fill('#f-nextCheck', '2001-01-01')
    pg.fill('#f-checkDate', '2026-05-14')
    pg.select_option('#f-checkResult', 'partial')
    pg.fill('#f-checkNotes', 'One folder needs another look.')
    pg.click('#recordCheckBtn')
    check('Partial or needs review' in pg.inner_text('#checkHistory'), 'read-back result appears in check history before saving')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows tr').count() == 1 and 'Overdue by' in pg.inner_text('#rows'), 'copy is listed and its overdue check is flagged')
    check('A001' in pg.inner_text('#dueList')
          and pg.locator('#stats .stat').all_inner_texts() == ['1\narchived copies', '%d\nproject assets' % len(json.loads(sample)['assets']), '1\noverdue checks', '1/1\nwith a hash manifest'],
          'summary shows the due copy and project totals')
    pg.select_option('#statusFilter', 'overdue')
    check(pg.locator('#rows tr').count() == 1, 'overdue filter shows the matching copy')
    pg.select_option('#statusFilter', '')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    archive_csv = open(d.value.path(), encoding='utf-8-sig').read()
    check('SHA256 A001/clip001.mov abc123' in archive_csv and 'One folder needs another look.' in archive_csv,
          'archive CSV includes the full hash manifest and read-back history')

    pg.click('#addBtn')
    pg.select_option('#f-asset', '__new__')
    check(not pg.is_hidden('#newAssetFields'), 'new project asset fields appear when selected')
    pg.fill('#f-assetName', 'Festival master')
    pg.fill('#f-assetType', 'master')
    pg.fill('#f-assetPath', 'masters/festival-master.mov')
    pg.fill('#f-copiedAt', '2026-05-15')
    pg.fill('#f-location', 'Off-site storage')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows tr').count() == 2 and 'Festival master' in pg.inner_text('#rows'), 'new asset and first copy are added together')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    pg.emulate_media(media='print')
    check('Festival master' in pg.inner_text('#report') and 'Locked cabinet, second location' in pg.inner_text('#report'),
          'print report includes the assets, storage locations and checks')
    pg.emulate_media(media='screen')

    with pg.expect_download() as d:
        pg.click('#projectCsvBtn')
        pg.locator('#projectCsvCollection').select_option('assets')
        pg.click('#projectCsvForm button[type=submit]')
    assets_csv = open(d.value.path(), encoding='utf-8-sig').read()
    check('archiveCopies' in assets_csv and 'SHA256 A001/clip001.mov abc123' in assets_csv,
          'project asset CSV includes the nested archive records')

    if fake:
        pg.click('#saveBtn'); pg.wait_for_timeout(300)
        data = json.loads(pg.evaluate('window.__file.text'))
    else:
        with pg.expect_download() as d:
            pg.click('#saveBtn')
        data = json.loads(open(d.value.path(), encoding='utf-8').read())
    asset = next(a for a in data['assets'] if a['id'] == 'asset-card-a001')
    copy = asset['archiveCopies'][0]
    check(copy['storageLocation'] == 'Locked cabinet, second location' and copy['hashList'].startswith('SHA256')
          and copy['checks'][0]['result'] == 'partial' and copy['nextCheckDate'] == '2001-01-01',
          'saves copy location, manifest, next-check date and manual check history')
    check({k: v for k, v in asset.items() if k != 'archiveCopies'} == original_asset
          and data['callSheets'] == original['callSheets'] and data['musicCueSheet'] == original['musicCueSheet'],
          "other asset fields and project collections stay unchanged")
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_festival_strategy(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'festival-strategy', fake)
    open_sample(pg, fake)
    rows = pg.locator('#rows .row').all_inner_texts()
    check(len(rows) == 4 and 'Prairie Docs' in rows[0] and 'Riverbend' in rows[2], 'lists festivals in date order')
    nl = pg.inner_text('[data-id="festival-northern-light"]')
    check('World premiere' in nl and 'Prairie Docs screens first and ends this premiere' in nl, 'flags a premiere lost to an earlier festival')
    check('Ends the premiere at Northern Light' in pg.inner_text('[data-id="festival-prairie"]'), 'flags the earlier festival too')
    check('Northern Light' in pg.inner_text('#hear') and '$105.00' in pg.inner_text('#fees') and '$165.00' in pg.inner_text('#fees'), 'lists whose answer to wait for, and totals the fees')
    pg.click('[data-edit="festival-riverbend"]'); pg.select_option('#f-premiere', 'city')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('screens first' not in pg.inner_text('[data-id="festival-riverbend"]') and 'Riverbend premiere' in pg.inner_text('[data-id="festival-riverbend"]'), 'a city premiere in another city has no clash')
    pg.click('#addBtn'); pg.fill('#f-name', 'Harbor Lights'); pg.select_option('#f-premiere', 'international'); pg.fill('#f-country', 'France'); pg.select_option('#f-region', 'Europe')
    pg.fill('#f-start', '2027-06-01'); pg.fill('#f-end', '2027-05-01')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.is_visible('#editor'), 'an end date before the start is refused')
    pg.fill('#f-end', '2027-06-07'); pg.fill('#f-fee', '50')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    harbor = pg.locator('#rows .row').filter(has=pg.locator('.nm', has_text='Harbor Lights')).inner_text()
    check('Harbor Lights' in harbor and 'If Northern Light Film Festival takes it, you lose this premiere' in harbor, 'warns that a festival abroad could cost an international premiere')
    pg.fill('#homeCountry', 'Canada'); pg.locator('#homeCountry').dispatch_event('change'); pg.wait_for_timeout(100)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Festival strategy' in pg.inner_text('#report') and 'Harbor Lights' in pg.inner_text('#report'), 'prints the run')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Festival', 'Tier', 'Premiere'] and len(rows) == 6 and rows[1][0] == 'Prairie Docs', 'CSV lists the run in date order')
    data = saved_project(pg, fake)
    f = {x['name']: x for x in data['festivals']}
    check(f['Harbor Lights']['fee'] == 50 and f['Harbor Lights']['premiere'] == 'international' and f['Riverbend Documentary Festival']['premiere'] == 'city'
          and f['Riverbend Documentary Festival']['waiverCode'] == 'RIVER-WAIVE' and data['festivalStrategy']['homeCountry'] == 'Canada', 'saves festivals and keeps the submission tracker fields')
    check(data['people'] == original['people'] and data['screenings'] == original['screenings'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_press_notes(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'press-notes', fake)
    open_sample(pg, fake)
    check('From the project' in pg.inner_text('[data-key="logline"]') and 'Written' in pg.inner_text('[data-key="directorStatement"]') and 'Not done yet' in pg.inner_text('[data-key="aboutProduction"]'), 'marks what is written, from the project or still to do')
    check('Directed by Lena Ward' in pg.inner_text('[data-key="credits"]') and 'Prairie Docs' in pg.inner_text('[data-key="festivals"]') and 'Priya Nair (no bio yet)' in pg.inner_text('[data-key="bios"]'), 'pulls credits, festivals and bios from the project')
    pg.click('[data-edit="bios"]'); pg.fill('[data-bio="person-priya-nair"]', 'Priya Nair edits documentaries.'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Written' in pg.inner_text('[data-key="bios"]'), 'writes a bio')
    pg.click('[data-edit="shortSynopsis"]'); pg.click('#useTreatment')
    check(pg.input_value('#f-text').startswith('Riverside has flooded'), 'copies the treatment synopsis')
    pg.fill('#f-text', 'A town remembers its floods.'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('[data-edit="aboutProduction"]'); pg.check('#f-hide'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Left out' in pg.inner_text('[data-key="aboutProduction"]'), 'leaves a section out')
    pg.click('#addBtn')
    pg.set_input_files('#stillInput', files=[{'name': 'porch.png', 'mimeType': 'image/png', 'buffer': TINY_PNG}])
    pg.wait_for_function("document.querySelectorAll('#stillList [data-still]').length === 2")
    pg.fill('#still-cap-1', 'Ruth on her porch'); pg.fill('#still-cred-1', 'Lena Ward'); pg.click('[data-up="1"]')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#thumbs img').count() == 2 and pg.get_attribute('#thumbs img >> nth=0', 'alt') == 'Ruth on her porch', 'adds and orders stills')
    pg.click('[data-edit="contacts"]'); pg.click('#addContactBtn'); pg.fill('#c-role-1', 'Publicist'); pg.fill('#c-name-1', 'Jo Park'); pg.fill('#c-email-1', 'jo@example.com')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Press notes' in r and 'A town remembers its floods.' in r and 'Directed by' in r and 'Priya Nair edits documentaries.' in r and 'Photo: Lena Ward' in r and 'Jo Park' in r and 'About the production' not in r and '1.85:1' in r, 'prints the press notes')
    data = saved_project(pg, fake)
    pn = data['pressNotes']
    new = next(a for a in data['assets'] if a['id'] == pn['stillIds'][0])
    check(len(pn['stillIds']) == 2 and new['type'] == 'still' and new['photoCredit'] == 'Lena Ward' and new['data'].startswith('data:image/jpeg') and pn['hidden'] == ['aboutProduction']
          and pn['shortSynopsis'] == 'A town remembers its floods.' and pn['contacts'][1]['name'] == 'Jo Park', 'saves the press notes and stills')
    priya = next(p for p in data['people'] if p['id'] == 'person-priya-nair')
    check(priya['bio'] == 'Priya Nair edits documentaries.' and [p for p in data['people'] if p['id'] != 'person-priya-nair'] == [p for p in original['people'] if p['id'] != 'person-priya-nair'], 'saves the bio with the person')
    check(data['credits'] == original['credits'] and data['festivals'] == original['festivals'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_stills_library(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'stills-library', fake)
    open_sample(pg, fake)
    porch = pg.inner_text('[data-id="asset-still-porch"]')
    check(pg.locator('#rows .row').count() == 2 and 'Daniel Okafor: No release' in porch and 'Waiting for approval' in porch and 'No photo credit' in porch, 'lists stills with release problems and approvals')
    check('Daniel Okafor' in pg.inner_text('#releases') and 'Ruth Hammond' not in pg.inner_text('#releases'), 'lists people pictured without a signed release')
    pg.click('[data-f="release"]')
    check(pg.locator('#rows .row').count() == 1, 'filters to release problems')
    pg.click('[data-f="all"]')
    pg.set_input_files('#stillInput', files=[{'name': 'crew.png', 'mimeType': 'image/png', 'buffer': TINY_PNG}])
    pg.wait_for_selector('#editor[open]')
    pg.fill('#f-caption', 'The crew on the levee'); pg.fill('#f-credit', 'Teo Ramirez'); pg.select_option('#f-kind', 'key art')
    pg.check('#f-people input[value="person-marcus-bell"]'); pg.select_option('#f-approval', 'approved'); pg.fill('#f-approvedBy', 'Ana Reyes'); pg.fill('#f-path', 'stills/crew-full.tif')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 3 and 'Key art' in pg.inner_text('#rows') and 'Marcus Bell' in pg.inner_text('#releases'), 'adds a still with people pictured')
    pg.click('[data-edit="asset-still-levee"]'); pg.click('#removeBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 2, 'removes a still')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['File', 'Kind', 'Caption'] and len(rows) == 3 and any('Daniel Okafor: No release' in r[6] for r in rows), 'exports the caption sheet')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Caption sheet' in pg.inner_text('#report') and 'Photo: Teo Ramirez' in pg.inner_text('#report'), 'prints the caption sheet')
    data = saved_project(pg, fake)
    new = next(a for a in data['assets'] if a.get('caption') == 'The crew on the levee')
    check(new['type'] == 'key art' and new['personIds'] == ['person-marcus-bell'] and new['approval'] == 'approved' and new['relativePath'] == 'stills/crew-full.tif'
          and not any(a['id'] == 'asset-still-levee' for a in data['assets']) and 'stillIds' not in data['pressNotes'], 'saves stills and takes a removed one out of the press notes')
    check(data['people'] == original['people'] and data['contracts'] == original['contracts'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_awards_social(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'awards-social', fake)
    open_sample(pg, fake)
    ag = pg.inner_text('#agenda')
    check('Entry deadline: Riverbend Documentary Awards' in ag and 'Screening: Prairie Docs' in ag and 'premieres at Prairie Docs' in ag, 'puts awards, festivals and posts on one calendar')
    aw = pg.inner_text('#awards')
    check('inside the eligibility window' in aw and 'outside the eligibility window' in aw, 'checks eligibility windows against the first screening')
    sug = pg.locator('#suggest li').count()
    check(sug >= 3 and 'One week until' in pg.inner_text('#suggest') and 'is screening at Prairie Docs' not in pg.inner_text('#suggest'), 'suggests posts around accepted festivals, leaving out ones already added')
    before = pg.locator('#agenda [data-post]').count()
    pg.click('#suggestBtn'); pg.wait_for_timeout(200)
    check(pg.locator('#agenda [data-post]').count() == before + sug and pg.is_hidden('#suggestBtn'), 'adds the suggestions as drafts')
    pg.click('#addBtn'); pg.fill('#a-name', 'Northern Docs Prize'); pg.fill('#a-from', '2027-06-01'); pg.fill('#a-to', '2027-01-01')
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a window that ends before it starts is refused')
    pg.fill('#a-to', '2027-12-31'); pg.fill('#a-deadline', '2027-08-01'); pg.fill('#a-fee', '40'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Northern Docs Prize' in pg.inner_text('#awards') and 'outside' in pg.inner_text('#awards li:has-text("Northern Docs Prize")'), 'adds an award and checks it')
    pg.click('#postBtn'); pg.fill('#p-date', '2027-03-01'); pg.fill('#p-text', 'Trailer out now'); pg.fill('#p-platform', 'Newsletter'); pg.click('#postSubmit'); pg.wait_for_timeout(200)
    pg.click('[data-f="post"]')
    check('Trailer out now' in pg.inner_text('#agenda') and 'Entry deadline' not in pg.inner_text('#agenda'), 'filters the calendar')
    pg.click('[data-f="all"]')
    with pg.expect_download() as d:
        pg.click('#icsBtn')
    ics = open(d.value.path(), encoding='utf-8', newline='').read()
    check(ics.startswith('BEGIN:VCALENDAR') and 'SUMMARY:Trailer out now' in ics and 'DTSTART;VALUE=DATE:20270901' in ics and '\r\n' in ics, 'exports a calendar file')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Northern Docs Prize' in pg.inner_text('#report') and 'Trailer out now' in pg.inner_text('#report'), 'prints the calendar and awards')
    data = saved_project(pg, fake)
    aw = next(a for a in data['awards'] if a['name'] == 'Northern Docs Prize')
    check(aw['fee'] == 40 and aw['windowEnd'] == '2027-12-31' and len(data['socialPosts']) == 2 + sug and any(p.get('eventKey') == 'festival:festival-prairie:week' for p in data['socialPosts']), 'saves awards and posts')
    check(data['festivals'] == original['festivals'] and data['project'] == original['project'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_rights_matrix(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'rights-matrix', fake)
    open_sample(pg, fake)
    pg.fill('#asOf', '2027-03-15'); pg.locator('#asOf').dispatch_event('change'); pg.wait_for_timeout(100)
    us = pg.inner_text('#grid tbody tr:has-text("United States")')
    check('Sold' in us and 'Riverside Streaming' in us and 'Available' in us, 'shows sold and available rights by territory and media')
    check('On hold' in pg.inner_text('#grid tbody tr:has-text("Canada")') and pg.locator('.cell.c-clash').count() == 1, 'shows a right on hold, and marks the overlap')
    check(pg.locator('#grid tbody tr').filter(has_text='Airline').count() == 0 and pg.locator('#grid tbody tr').count() == 10 and pg.locator('#grid .cell:has-text("Skyway")').count() == 10, 'a worldwide deal covers every territory')
    check('Riverside Streaming (fictional) and Northbound Media (fictional)' in pg.inner_text('#clashes') and 'Riverside Streaming' in pg.inner_text('#reverts'), 'lists overlaps and rights reverting soon')
    pg.click('#addBtn'); pg.fill('#f-licensee', 'Harbor Educational'); pg.check('#f-terr input[value="Canada"]'); pg.fill('#f-terrOther', 'Ireland')
    pg.check('#f-media input[value="educational"]'); pg.select_option('#f-status', 'signed'); pg.fill('#f-start', '2027-01-01'); pg.fill('#f-end', '2026-01-01')
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a term that ends before it starts is refused')
    pg.fill('#f-end', '2029-12-31'); pg.uncheck('#f-excl'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#grid tbody tr:has-text("Ireland")').count() == 1 and 'Harbor Educational' in pg.inner_text('#grid tbody tr:has-text("Ireland")'), 'adds a deal and its territory to the grid')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Territory', 'Media', 'Status', 'Held by', 'Until', 'Overlap'] and len(rows) == 11 * 9 + 1 and ['United States', 'Subscription streaming', 'Sold'] == rows[5][:3] and rows[5][5] == 'Yes', 'CSV has a row for each territory and media')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Rights availability' in pg.inner_text('#report') and 'Harbor Educational' in pg.inner_text('#report'), 'prints the grid')
    data = saved_project(pg, fake)
    h = next(c for c in data['contracts'] if c.get('licensee') == 'Harbor Educational')
    check(h['type'] == 'distribution' and h['territories'] == ['Canada', 'Ireland'] and h['mediaRights'] == ['educational'] and h['exclusive'] is False and h['status'] == 'signed', 'saves the deal')
    check([c for c in data['contracts'] if c['id'] != h['id']] == original['contracts'], 'other contracts are unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_deliverables(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'deliverables', fake)
    open_sample(pg, fake)
    check(pg.input_value('#deliverTo') == 'Riverside Streaming (fictional)' and 'Delivered' in pg.inner_text('[data-key="master"]') and 'Not needed' in pg.inner_text('[data-key="dcp"]'), 'shows who it is for and each status')
    check('Latest QC report: failed' in pg.inner_text('[data-key="qc"]') and '1 approved still' in pg.inner_text('[data-key="stills"]') and 'Platform tile artwork' in pg.inner_text('#sections'), 'shows what the project has, and your own items')
    pg.click('[data-edit="cue"]')
    check('music cue sheet' in pg.inner_text('#fromNote') and pg.is_disabled('#f-section') and pg.is_hidden('#deleteBtn'), 'links a built-in item to its tool')
    pg.select_option('#f-status', 'accepted'); pg.fill('#f-owner', 'Sam Okafor'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#addBtn'); pg.fill('#f-title', 'Lab access letter'); pg.select_option('#f-section', 'legal'); pg.fill('#f-due', '2000-01-01'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('Lab access letter' in pg.inner_text('#late') and 'Overdue' in pg.inner_text('#sections'), 'adds an item and flags it overdue')
    pg.click('[data-edit="deliverable-poster"]'); pg.click('#deleteBtn'); pg.wait_for_timeout(200)
    check('Platform tile artwork' not in pg.inner_text('#sections'), 'deletes your own item')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:3] == ['Section', 'Deliverable', 'Status'] and len(rows) == 25, 'CSV lists every item')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('Deliverables' in r and 'Lab access letter' in r and 'Digital cinema package' not in r, 'prints the checklist without items not needed')
    data = saved_project(pg, fake)
    it = {x['key']: x for x in data['deliverables']['items']}
    check(it['cue']['status'] == 'accepted' and it['cue']['owner'] == 'Sam Okafor' and 'deliverable-poster' not in it and any(x.get('title') == 'Lab access letter' and x['custom'] for x in it.values()), 'saves the checklist')
    check(data['contracts'] == original['contracts'] and data['assets'] == original['assets'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_qc_tracker(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'qc-tracker', fake)
    open_sample(pg, fake)
    rows = pg.locator('#rows .row').all_inner_texts()
    check(len(rows) == 4 and rows[0].startswith('00:58:02:15') and 'Fixed in v2 master' in pg.inner_text('[data-id="qc-1"]'), 'lists issues in timecode order with the version they were fixed in')
    check('2 open issues' in pg.inner_text('#count'), 'counts open and disputed issues')
    pg.select_option('#ownerSel', 'mixer')
    check(pg.inner_text('#fixSum li >> nth=0').endswith('1'), 'filters the fix list by who fixes it')
    pg.click('[data-edit="qc-2"]'); pg.select_option('#f-fixedIn', 'master-v2'); pg.select_option('#f-fix', 'fixed'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.fill('#v-name', 'v3 master'); pg.fill('#v-date', '2026-11-10'); pg.click('#versionBtn'); pg.wait_for_timeout(100)
    pg.click('#reportBtn'); pg.select_option('#r-version', label='v3 master'); pg.fill('#r-vendor', 'Clearframe QC'); pg.select_option('#r-result', 'fail'); pg.click('#reportSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 0 and 'v3 master' in pg.inner_text('#reportSel'), 'adds a report for a new version')
    pg.click('#addBtn'); pg.fill('#f-tc', '1:2'); pg.fill('#f-desc', 'Hit in the left surround'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a timecode in the wrong form is refused')
    pg.fill('#f-tc', '01:30:00:10'); pg.select_option('#f-sev', 'major'); pg.select_option('#f-area', 'sound'); pg.select_option('#f-owner', 'mixer'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    r = pg.inner_text('#report')
    check('QC fix list: Mixer' in r and 'Hit in the left surround' in r and 'Dialogue peaks' not in r and 'Dead pixel' not in r, 'prints the open fixes for one person')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][:4] == ['Report', 'Version', 'Result', 'Timecode'] and len(rows) == 6, 'CSV lists every issue')
    data = saved_project(pg, fake)
    q = data['qc']
    new = q['reports'][-1]
    check(len(q['versions']) == 3 and new['issues'][0]['tc'] == '01:30:00:10' and new['versionId'] == q['versions'][2]['id'] and q['reports'][0]['issues'][1]['fix'] == 'fixed', 'saves versions, reports and fixes')
    check(data['assets'] == original['assets'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_waterfall(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'waterfall', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 6 and 'Actual revenue to date: $55,500.00' in pg.inner_text('#scenSel'), 'lists tiers and offers actual revenue as a scenario')
    pg.select_option('#scenSel', label='High: $400,000.00')
    check('$237,500.00' in pg.inner_text('#parties') and '$57,500.00' in pg.inner_text('#results'), 'runs a scenario down the tiers')
    pg.select_option('#scenSel', label='Low: $120,000.00')
    check('$68,000.00 still owed' in pg.inner_text('[data-id="tier-recoup"]') and '$264,706.00' in pg.inner_text('#breakeven'), 'shows what is still owed and the break-even point')
    pg.fill('#scenGross', '1000000')
    check('$1,000,000.00' in pg.inner_text('#results'), 'tries any amount')
    pg.click('#scenAdd'); pg.wait_for_timeout(100)
    pg.click('[data-down="0"]'); pg.wait_for_timeout(100)
    check(pg.locator('#rows .row').first.get_attribute('data-id') == 'tier-sales-expenses', 'reorders tiers')
    pg.click('[data-edit="tier-profits"]'); pg.fill('#sp-s-1', '40')
    check('90%' in pg.inner_text('#splitSum'), 'adds up the split shares')
    pg.fill('#sp-s-1', '50'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    pg.click('#addBtn'); pg.fill('#f-name', 'Composer bonus'); pg.select_option('#f-kind', 'percent'); pg.fill('#f-pct', '150'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a percentage over 100 is refused')
    pg.fill('#f-pct', '5'); pg.fill('#f-party', 'Mira Castellanos'); pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('A split takes everything left' in pg.inner_text('#rows'), 'warns when a tier comes after the split')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0] == ['Scenario', 'Gross receipts', 'Tier', 'Paid to', 'Paid', 'Still owed'] and any(r[0] == 'Actual revenue to date' for r in rows), 'CSV has every scenario')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Recoupment waterfall' in pg.inner_text('#report') and 'By party' in pg.inner_text('#report'), 'prints the summary')
    data = saved_project(pg, fake)
    w = data['waterfall']
    check(len(w['tiers']) == 7 and w['tiers'][0]['id'] == 'tier-sales-expenses' and w['tiers'][-1]['percent'] == 5 and len(w['scenarios']) == 3 and w['scenarios'][2]['gross'] == 1000000, 'saves tiers and scenarios')
    check(data['revenueStatements'] == original['revenueStatements'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_revenue_tracker(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'revenue-tracker', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 2 and '$35,000.00' in pg.inner_text('[data-id="statement-riverside-q3"]'), 'works out what is due from gross, fees and expenses')
    t = pg.inner_text('#totals')
    check('$55,500.00' in t and '$38,500.00' in t, 'totals gross and what is due')
    pg.select_option('#bySel', 'territory')
    check('Worldwide' in pg.inner_text('#by') and 'United States' in pg.inner_text('#by'), 'groups by territory')
    pg.click('#addBtn'); pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'a statement needs a source')
    pg.select_option('#f-deal', 'contract-dist-riverside-streaming'); pg.fill('#f-from', '2026-10-01'); pg.fill('#f-to', '2026-12-31'); pg.select_option('#f-media', 'tvod')
    pg.fill('#f-gross', '10000'); pg.fill('#f-fees', '2500'); pg.fill('#f-net', '7000')
    check('$7,500.00' in pg.inner_text('#netHint'), 'shows gross less fees and expenses')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check('differs from gross less fees and expenses' in pg.inner_text('#rows') and 'Riverside Streaming' in pg.inner_text('#unpaid'), 'flags a statement that does not add up, and lists it as unpaid')
    pg.select_option('#bySel', 'quarter')
    check('2026 Q4' in pg.inner_text('#by'), 'groups by quarter')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][0] == 'Source' and len(rows) == 4 and rows[1][9] == '7000', 'CSV lists every statement')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('By territory' in pg.inner_text('#report'), 'prints the statements and totals')
    data = saved_project(pg, fake)
    s = next(x for x in data['revenueStatements'] if x['id'] not in ('statement-riverside-q3', 'statement-skyway-1'))
    check(s['contractId'] == 'contract-dist-riverside-streaming' and s['gross'] == 10000 and s['net'] == 7000 and 'expenses' not in s, 'saves the statement')
    check(data['contracts'] == original['contracts'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_bookings(browser, fake):
    original = json.loads(sample)
    ctx, pg, errs = new_page(browser, 'bookings', fake)
    open_sample(pg, fake)
    check(pg.locator('#rows .row').count() == 3 and 'Box office split 35%' in pg.inner_text('[data-id="booking-prairie-cinema"]') and 'To send: Blu-ray, Discussion guide' in pg.inner_text('[data-id="booking-riverside-library"]'), 'lists bookings with terms and materials to send')
    t = pg.inner_text('#totals')
    check('$450.00' in t and '$250.00' in t and '$700.00' in t, 'totals fees paid and invoiced')
    pg.click('[data-f="educational"]')
    check(pg.locator('#rows .row').count() == 1, 'filters by kind')
    pg.click('#addBtn')
    check(pg.input_value('#f-kind') == 'educational', 'a new booking starts in the kind you are looking at')
    pg.fill('#f-venue', 'Valley College'); pg.select_option('#f-license', 'one-year'); pg.fill('#f-fee', '300'); pg.fill('#f-start', '2027-01-15'); pg.fill('#f-end', '2026-01-15')
    pg.click('#editorSubmit'); pg.wait_for_timeout(100)
    check(pg.is_visible('#editor'), 'an end before the start is refused')
    pg.fill('#f-end', '2028-01-14'); pg.fill('[data-sent="file"]', '2027-01-10'); pg.locator('[data-sent="file"]').dispatch_event('change'); pg.fill('#f-paid', '2027-01-20')
    pg.click('#editorSubmit'); pg.wait_for_timeout(200)
    check(pg.locator('#rows .row').count() == 2 and 'Materials sent' in pg.inner_text('#rows'), 'adds a booking with materials sent')
    pg.click('[data-f="all"]'); pg.select_option('#perSel', 'year')
    check('2027' in pg.inner_text('#periods') and '2026' in pg.inner_text('#periods'), 'totals by year')
    with pg.expect_download() as d:
        pg.click('#csvBtn')
    rows = list(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
    check(rows[0][0] == 'Venue or institution' and len(rows) == 5, 'CSV lists every booking')
    pg.click('#printBtn'); pg.wait_for_timeout(200)
    check('Valley College' in pg.inner_text('#report'), 'prints the bookings')
    data = saved_project(pg, fake)
    b = next(x for x in data['bookings'] if x['venue'] == 'Valley College')
    check(b['payment'] == 'paid' and b['materialsNeeded'] == ['file'] and b['materials'] == {'file': '2027-01-10'} and b['fee'] == 300 and b['kind'] == 'educational', 'saves the booking, marking it paid when it has a paid date')
    check(data['screenings'] == original['screenings'], 'other data is unchanged')
    check(not errs, 'no page errors %s' % errs)
    ctx.close()

def test_template_columns(browser, fake):
    for name, template in TEMPLATE_EXPORTS:
        ctx, pg, errs = new_page(browser, name, fake)
        open_sample(pg, fake)
        with pg.expect_download() as d:
            pg.click('#csvBtn')
        exported = next(csv.reader(io.StringIO(open(d.value.path(), encoding='utf-8-sig').read())))
        wanted = next(csv.reader(io.StringIO((root / 'templates' / template).read_text(encoding='utf-8-sig'))))
        remaining = iter(exported)
        check(all(col in remaining for col in wanted), '%s: template columns appear in the export, in order' % template)
        check(not errs, 'no page errors %s' % errs)
        ctx.close()

def main():
    global FALLBACK
    mode = sys.argv[1] if len(sys.argv) > 1 else 'chromium'
    FALLBACK = mode == 'chromium-fallback'
    engine = 'chromium' if FALLBACK else mode
    fake = mode == 'chromium'
    with sync_playwright() as p:
        # PLAYWRIGHT_CHANNEL=chrome uses an installed Google Chrome instead of Playwright's own Chromium (CI does this).
        channel = os.environ.get('PLAYWRIGHT_CHANNEL') if engine == 'chromium' else None
        browser = getattr(p, engine).launch(headless=True, **({'channel': channel} if channel else {}))
        print('#### %s %s' % (mode, browser.version))
        for name in TOOLS:
            for label, fn in [('core', lambda: test_core(browser, name, fake)), ('phone', lambda: test_phone(browser, name, fake)),
                              ('dark mode', lambda: test_dark(browser, name, fake)), ('print', lambda: test_print(browser, name, fake, fake))]:
                print('== %s / %s' % (name, label))
                fn()
        print('== call-sheet / spreadsheet export')
        test_call_sheet_export(browser, fake)
        print('== release-tracker / releases, coverage and scans')
        test_release_tracker(browser, fake)
        print('== credits-builder / credits, requirements and export')
        test_credits_builder(browser, fake)
        print('== name-supers / flags, spelling and export')
        test_name_supers(browser, fake)
        print('== subject-tracker / filters, follow-ups and adding people')
        test_subject_tracker(browser, fake)
        print('== research-log / tabs, statuses and sending to the clearance log')
        test_research_log(browser, fake)
        print('== comps-tracker / sources, tags and the comps page')
        test_comps_tracker(browser, fake)
        print('== treatment-builder / counts, project lines and versions')
        test_treatment_builder(browser, fake)
        print('== pitch-deck / slides, images and print sizes')
        test_pitch_deck(browser, fake)
        print('== grant-calendar / deadlines, materials, calendar file and links')
        test_grant_calendar(browser, fake)
        print('== narrative-library / counts, versions, sets and who got what')
        test_narrative_library(browser, fake)
        print('== budget / lines, fringes, versions and the top sheet')
        test_budget(browser, fake)
        print('== budget-converter / mapping, formats and totals')
        test_budget_converter(browser, fake)
        print('== finance-plan / sources, grants, gap and timing')
        test_finance_plan(browser, fake)
        print('== funder-crm / steps, log, people and links')
        test_funder_crm(browser, fake)
        print('== cash-flow / schedule, income, balance and shortfalls')
        test_cash_flow(browser, fake)
        print('== shooting-calendar / days, trips, call sheets and exports')
        test_shooting_calendar(browser, fake)
        print('== interview-prep / beats, questions and the guide')
        test_interview_prep(browser, fake)
        print('== field-journal / entries, tags, search and Markdown')
        test_field_journal(browser, fake)
        print('== home page / tools, search and links')
        test_hub(browser, fake)
        print('== location-scout / scouts, photos and releases')
        test_location_scout(browser, fake)
        print('== deal-memos / calendar, budget, signed copies and print')
        test_deal_memos(browser, fake)
        print('== gear-list / gear, packages, costs and print')
        test_gear_list(browser, fake)
        print('== coi-permit-tracker / certificates, permits and shoot-day checks')
        test_coi_permits(browser, fake)
        print('== travel-sheet / trips, travel for each person and print')
        test_travel_sheet(browser, fake)
        print('== risk-plan / hazards, check-ins and two prints')
        test_risk_plan(browser, fake)
        print('== security-checklist / items, people and high-risk shoots')
        test_security_checklist(browser, fake)
        print('== press-list / outlets, beats, screeners, RSVPs and coverage')
        test_press_list(browser, fake)
        print('== partner-crm / partners, commitments and screenings')
        test_partner_crm(browser, fake)
        print('== discussion-guide / synopsis, questions, resources and print')
        test_discussion_guide(browser, fake)
        print('== archive-log / copies, manifests, read-back checks and export')
        test_archive_log(browser, fake)
        print('== camera-sound-reports / cards, clips, call sheets and CSV')
        test_camera_sound(browser, fake)
        print('== interview-log / moments, releases and the paper edit')
        test_interview_log(browser, fake)
        print('== daily-production-report / hours, call sheet start, incidents and CSV')
        test_daily_report(browser, fake)
        print('== expense-log / totals, receipts, per diems and CSV')
        test_expense_log(browser, fake)
        print('== festival-submissions / ordering, flags, screenings and CSV')
        test_festivals(browser, fake)
        print('== footage-log / imports, tags, filters and CSV')
        test_footage_log(browser, fake)
        print('== paper-edit / transcripts, bites, scenes and the edit list')
        test_paper_edit(browser, fake)
        print('== structure-board / cards, drag, threads and print')
        test_structure_board(browser, fake)
        print('== cut-tracker / notes, carrying and the locked cut')
        test_cut_tracker(browser, fake)
        print('== budget-to-actuals / lines, estimates and the cost report')
        test_budget_actuals(browser, fake)
        print('== fair-use-log / factors, countries and the memo')
        test_fair_use(browser, fake)
        print('== license-tracker / terms, payments and options')
        test_license_tracker(browser, fake)
        print('== clearance-report / scripts, marks and clearances')
        test_clearance_report(browser, fake)
        print('== chain-of-title / checklist, links and the binder')
        test_chain_of_title(browser, fake)
        print('== festival-strategy / premiere clashes, fees and the run')
        test_festival_strategy(browser, fake)
        print('== press-notes / sections, bios, stills and print')
        test_press_notes(browser, fake)
        print('== stills-library / captions, releases, approvals and the caption sheet')
        test_stills_library(browser, fake)
        print('== awards-social / awards, posts, suggestions and the calendar file')
        test_awards_social(browser, fake)
        print('== rights-matrix / the grid, overlaps and reverting rights')
        test_rights_matrix(browser, fake)
        print('== deliverables / the list, the project and the checklist')
        test_deliverables(browser, fake)
        print('== qc-tracker / reports, issues, versions and the fix list')
        test_qc_tracker(browser, fake)
        print('== waterfall / tiers, scenarios, break-even and actual revenue')
        test_waterfall(browser, fake)
        print('== revenue-tracker / statements, totals and payments')
        test_revenue_tracker(browser, fake)
        print('== bookings / terms, payments, materials and totals')
        test_bookings(browser, fake)
        print('== templates / columns match the tools\' exports')
        test_template_columns(browser, fake)
        browser.close()
    print('FAILS', fails)
    sys.exit(1 if fails else 0)

main()
