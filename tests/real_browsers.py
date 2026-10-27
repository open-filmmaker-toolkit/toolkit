"""Checks every tool in the real Firefox and Safari already installed on a computer.

Run: pip install selenium
     python tests/real_browsers.py firefox     (needs Firefox and geckodriver)
     python tests/real_browsers.py safari      (macOS; run `safaridriver --enable` once)

The main browser tests (tests/browser_tools.py) use Playwright, which can only drive
its own downloaded browsers. This file uses Selenium instead, so it can drive the
browsers people actually have. CI runs it weekly, on demand, and on pull requests
that change it, in the Firefox on GitHub's Linux runners and the Safari on its Mac
runners, with nothing to download.

Per tool: the page starts, the sample opens, saving produces a project file that
keeps the sample's data and reopens, the tool's own export downloads, its main
dialog opens, printing builds the report, and there are no script errors. Firefox
also checks dark mode and phone width.
"""
import ast, functools, http.server, json, pathlib, socketserver, sys, threading, time

from selenium import webdriver
from selenium.webdriver.common.by import By

root = pathlib.Path(__file__).resolve().parents[1]
sample_text = (root / 'samples/the-river-keeps.oft.json').read_text()
sample = json.loads(sample_text)

# Use the same tool list and dialog buttons as the Playwright suite.
_tree = ast.parse((root / 'tests/browser_tools.py').read_text())
_consts = {t.id: ast.literal_eval(n.value) for n in _tree.body if isinstance(n, ast.Assign)
           for t in n.targets if isinstance(t, ast.Name) and t.id in ('TOOLS', 'PRINT_BTN', 'DIALOG_BTN')}
TOOLS, PRINT_BTN, DIALOG_BTN = _consts['TOOLS'], _consts['PRINT_BTN'], _consts.get('DIALOG_BTN', {})
EXPORT_BTNS = ['#csvBtn', '#sheetCsvBtn', '#mdBtn']

# Records script errors, stubs the print dialog, and captures downloads in memory
# instead of saving files, which works the same in every browser.
HOOKS = r"""
window.__errors = window.__errors || [];
if (!window.__hooked) {
  window.__hooked = true;
  window.addEventListener('error', e => window.__errors.push(String(e.message)));
  window.addEventListener('unhandledrejection', e => window.__errors.push(String(e.reason)));
  window.print = () => { window.__printed = true; };
  window.__downloads = [];
  const click = HTMLAnchorElement.prototype.click;
  HTMLAnchorElement.prototype.click = function () {
    if (this.download && this.href.startsWith('blob:')) {
      const name = this.download;
      fetch(this.href).then(r => r.text()).then(text => window.__downloads.push({ name, text }));
      return;
    }
    return click.call(this);
  };
}
"""
OPEN = r"""
const [text, name] = arguments;
const input = document.getElementById('fileInput');
const dt = new DataTransfer();
dt.items.add(new File([text], name, { type: 'application/json' }));
input.files = dt.files;
input.dispatchEvent(new Event('change', { bubbles: true }));
"""

fails = []
def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg, flush=True)
    if not ok:
        fails.append(msg)

def wait_for(fn, timeout=8):
    end = time.time() + timeout
    while time.time() < end:
        try:
            value = fn()
            if value:
                return value
        except Exception:
            pass
        time.sleep(0.15)
    return None

def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    handler = functools.partial(Quiet, directory=str(root))
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, 'http://127.0.0.1:%d' % httpd.server_address[1]

def make_driver(browser, dark=False):
    if browser == 'firefox':
        opts = webdriver.FirefoxOptions()
        opts.add_argument('-headless')
        if dark:
            opts.set_preference('ui.systemUsesDarkTheme', 1)
        return webdriver.Firefox(options=opts)
    if browser == 'safari':
        return webdriver.Safari()
    if browser == 'chrome':
        opts = webdriver.ChromeOptions()
        opts.add_argument('--headless=new')
        return webdriver.Chrome(options=opts)
    sys.exit('Use firefox, safari or chrome')

def load(driver, base, name):
    driver.get('%s/tools/%s/index.html' % (base, name))
    wait_for(lambda: driver.execute_script("return document.readyState === 'complete'"))
    driver.execute_script(HOOKS)
    return driver.execute_script("return !document.documentElement.classList.contains('no-js') && getComputedStyle(document.getElementById('cantRun')).display === 'none'")

def open_project(driver, text, file_name='sample.oft.json'):
    driver.execute_script(OPEN, text, file_name)
    return wait_for(lambda: driver.execute_script("return document.getElementById('filmMeta').textContent.trim() !== ''"))

def downloads(driver):
    return driver.execute_script('return window.__downloads.slice()')

def next_download(driver, before):
    return wait_for(lambda: (lambda d: d[before] if len(d) > before else None)(downloads(driver)))

def visible(driver, selector):
    els = driver.find_elements(By.CSS_SELECTOR, selector)
    return els[0] if els and els[0].is_displayed() else None

def close_dialogs(driver):
    driver.execute_script("document.querySelectorAll('dialog[open]').forEach(d => d.close())")

def test_tool(driver, base, name):
    print('== %s' % name, flush=True)
    check(load(driver, base, name), '%s: the page starts' % name)
    check(open_project(driver, sample_text), '%s: the sample opens' % name)
    check('River' in driver.find_element(By.ID, 'filmTitle').text, '%s: shows the film title' % name)

    n = len(downloads(driver))
    driver.find_element(By.ID, 'saveBtn').click()
    saved = next_download(driver, n)
    data = None
    try:
        data = json.loads(saved['text']) if saved else None
    except ValueError:
        pass
    check(bool(data) and data.get('format') == sample['format'] and all(k in data for k in sample)
          and [p['name'] for p in data.get('people', [])] == [p['name'] for p in sample['people']],
          '%s: saving keeps the sample\'s data' % name)
    if data:
        close_dialogs(driver)
        check(open_project(driver, json.dumps(data), 'saved.oft.json') and 'River' in driver.find_element(By.ID, 'filmTitle').text,
              '%s: the saved file reopens' % name)

    for sel in EXPORT_BTNS:
        btn = visible(driver, sel)
        if btn:
            n = len(downloads(driver))
            btn.click()
            got = next_download(driver, n)
            check(bool(got) and got['text'].strip() != '', '%s: %s downloads %s' % (name, sel, got['name'] if got else 'nothing'))
            close_dialogs(driver)
            break

    opener = visible(driver, DIALOG_BTN.get(name, '#addBtn'))
    if opener:
        opener.click()
        check(bool(wait_for(lambda: driver.find_elements(By.CSS_SELECTOR, 'dialog[open]'), 3)), '%s: the main dialog opens' % name)
        close_dialogs(driver)

    printer = visible(driver, PRINT_BTN.get(name, '#printBtn'))
    if printer:
        printer.click()
        check(driver.execute_script("return window.__printed === true && document.getElementById('report').textContent.trim().length > 0"),
              '%s: printing builds the report' % name)

    errors = driver.execute_script('return window.__errors')
    check(not errors, '%s: no script errors %s' % (name, errors or ''))

def luminance(css):
    nums = [float(x) for x in css[css.index('(') + 1:css.index(')')].split(',')[:3]]
    ch = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(nums[0]) + 0.7152 * ch(nums[1]) + 0.0722 * ch(nums[2])

def test_dark_and_phone(base, browser):
    driver = make_driver(browser, dark=True)
    try:
        driver.set_window_size(390, 844)
        for name in TOOLS:
            load(driver, base, name)
            open_project(driver, sample_text)
            bg = driver.execute_script('return getComputedStyle(document.body).backgroundColor')
            check(luminance(bg) < 0.2, '%s: dark mode background is dark (%s)' % (name, bg))
            width = driver.execute_script('return window.innerWidth')
            if width <= 440:
                over = driver.execute_script('return document.documentElement.scrollWidth - document.documentElement.clientWidth')
                check(over <= 1, '%s: phone width (%dpx) does not scroll sideways (%dpx over)' % (name, width, over))
            else:
                print('SKIP %s: the window could not be made phone-sized (%dpx)' % (name, width))
    finally:
        driver.quit()

def main():
    browser = sys.argv[1] if len(sys.argv) > 1 else 'firefox'
    httpd, base = serve()
    driver = make_driver(browser)
    try:
        caps = driver.capabilities
        print('#### %s %s' % (caps.get('browserName'), caps.get('browserVersion')), flush=True)
        driver.set_window_size(1280, 900)
        for name in TOOLS:
            try:
                test_tool(driver, base, name)
            except Exception as exc:  # keep going, so one tool's failure doesn't hide the others
                check(False, '%s: stopped with %s: %s' % (name, type(exc).__name__, str(exc).splitlines()[0] if str(exc) else ''))
    finally:
        driver.quit()
    if browser == 'firefox':
        print('== dark mode and phone width', flush=True)
        test_dark_and_phone(base, browser)
    httpd.shutdown()
    print('FAILS', fails)
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
