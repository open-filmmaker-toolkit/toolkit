# Drives the desktop app on Linux: open a project with the real file dialog, save it back to the same file,
# export a file, carry the project to another tool, connect the project folder, reopen the remembered file after a
# restart, and print. Also checks the website-only notes are hidden.
# Needs a debug build (npx tauri build --debug --no-bundle), tauri-driver, WebKitWebDriver, Xvfb, xdotool
# and selenium. Run from the desktop folder: python3 tests/smoke.py
import json, os, shutil, subprocess, sys, tempfile, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.options import ArgOptions

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(HERE, 'src-tauri', 'target', 'debug', 'open-filmmaker-toolkit')
SAMPLE = os.path.join(os.path.dirname(HERE), 'samples', 'the-river-keeps.oft.json')
WORK = tempfile.mkdtemp(prefix='oft-app-')
PROJECT = os.path.join(WORK, 'river.oft.json')
EXPORT = os.path.join(WORK, 'crew.csv')
shutil.copy(SAMPLE, PROJECT)
results = []


def check(ok, what):
    results.append((bool(ok), what))
    print(('PASS ' if ok else 'FAIL ') + what, flush=True)


def xdo(*args):
    return subprocess.run(['xdotool', *args], capture_output=True, text=True).stdout.strip()


def windows(word):
    return xdo('search', '--onlyvisible', '--name', word).split()


def answer_dialog(path, title_words=('Open', 'Save'), before=()):
    # The app's file dialogs are GTK dialogs. There's no window manager under Xvfb, so focus the dialog,
    # open its location box, type the full path and press Enter, and try again until
    # the dialog closes.
    # `before` is the windows there were before the click that opens the dialog.
    before = set(before)
    for _ in range(60):
        new = [w for w in windows('.') if w not in before and any(t in xdo('getwindowname', w) for t in title_words)]
        if new:
            break
        time.sleep(0.25)
    else:
        return False
    wid = new[-1]
    time.sleep(1.2)
    for _ in range(4):
        xdo('windowfocus', '--sync', wid)
        time.sleep(0.3)
        xdo('key', 'ctrl+l')
        time.sleep(0.4)
        xdo('key', 'ctrl+a')
        xdo('type', '--delay', '15', path)
        time.sleep(0.5)
        xdo('key', 'Return')
        time.sleep(1.2)
        # Saving over a file asks to replace it.
        for w in windows('.'):
            if w not in before and w != wid and 'Replace' in xdo('getwindowname', w):
                xdo('windowfocus', '--sync', w); xdo('key', 'Return'); time.sleep(0.5)
        if wid not in windows('.'):
            return True
    return False


def choose_folder(before=()):
    # The folder dialog opens in the project file's folder, so choosing it is a click on the button at its
    # bottom right. (Typing a folder's path there only goes into it.)
    before = set(before)
    for _ in range(60):
        new = [w for w in windows('.') if w not in before and 'Folder' in xdo('getwindowname', w)]
        if new:
            break
        time.sleep(0.25)
    else:
        return False
    wid = new[-1]
    time.sleep(1.5)
    geo = dict(l.split('=') for l in xdo('getwindowgeometry', '--shell', wid).split())
    for _ in range(3):
        xdo('mousemove', '--window', wid, str(int(geo['WIDTH']) - 50), str(int(geo['HEIGHT']) - 24)); xdo('click', '1')
        time.sleep(1)
        if wid not in windows('.'):
            return True
    return False


def start():
    opts = ArgOptions()
    opts.set_capability('tauri:options', {'application': APP})
    opts.set_capability('browserName', 'wry')
    d = webdriver.Remote(command_executor='http://127.0.0.1:4444', options=opts)
    d.implicitly_wait(0)
    return d


def wait(d, js, secs=10):
    end = time.time() + secs
    while time.time() < end:
        try:
            if d.execute_script('return !!(' + js + ')'):
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def rename(d, title):
    # Change the film's title in the film details dialog.
    d.execute_script("document.getElementById('editProjectBtn').click()")
    time.sleep(0.4)
    d.execute_script("const f = document.getElementById('p-title'); f.value = arguments[0]; f.dispatchEvent(new Event('input', { bubbles: true })); document.querySelector('#projectForm button[type=submit]').click();", title)
    time.sleep(0.4)


def go(d, path):
    d.execute_script('window.location.href = new URL(arguments[0], window.location.origin + "/").href', path)
    time.sleep(1.2)


# The app keeps its storage (the remembered file, earlier versions) under XDG_DATA_HOME; start clean.
env = dict(os.environ, DISPLAY=':99', XDG_DATA_HOME=os.path.join(WORK, 'data'), XDG_CONFIG_HOME=os.path.join(WORK, 'config'), XDG_CACHE_HOME=os.path.join(WORK, 'cache'))
os.environ['DISPLAY'] = ':99'
xvfb = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '1440x900x24'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
driver_proc = subprocess.Popen(['tauri-driver', '--native-driver', shutil.which('WebKitWebDriver')], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)
try:
    d = start()
    check(wait(d, "document.querySelector('h1')"), 'the app opens the home page')
    check(wait(d, 'typeof window.showSaveFilePicker === "function" && window.__TAURI__'), 'the bridge gives pages a file picker')
    check(wait(d, "document.getElementById('homeBrowser') && document.getElementById('homeBrowser').hidden"), 'the "saves a new copy" note stays hidden in the app')
    check(wait(d, "document.getElementById('offlineNote') && getComputedStyle(document.getElementById('offlineNote')).display === 'none'"), 'the "install it as an app" note is hidden in the app')

    go(d, 'tools/call-sheet/index.html')
    shown = windows('.')
    d.find_element(By.ID, 'openBtn').click()
    check(answer_dialog(PROJECT, before=shown), 'Open file shows the open dialog')
    check(wait(d, "document.getElementById('filmTitle').textContent.includes('River')"), 'the project opens from the dialog')

    rename(d, 'The River Keeps (app)')
    d.find_element(By.ID, 'saveBtn').click()
    saved = False
    for _ in range(40):
        time.sleep(0.25)
        if json.load(open(PROJECT, encoding='utf-8'))['project']['title'] == 'The River Keeps (app)':
            saved = True
            break
    check(saved, 'Save writes back to the same file, with no dialog')
    check(len([f for f in os.listdir(WORK) if f.endswith('.json')]) == 1, 'and no copies appear next to it')

    shown = windows('.')
    d.find_element(By.ID, 'csvBtn').click()
    check(answer_dialog(EXPORT, ('Save',), before=shown), 'an export asks where to save it')
    time.sleep(1)
    check(os.path.exists(EXPORT) and 'Name' in open(EXPORT, encoding='utf-8').read(), 'the export is written where you chose')

    d.find_element(By.CSS_SELECTOR, '.home-link').click(); time.sleep(1.2)
    go(d, 'tools/budget/index.html')
    check(wait(d, "document.getElementById('filmTitle').textContent.includes('(app)')"), 'the next tool has the project already open')
    rename(d, 'The River Keeps (budget)')
    d.find_element(By.ID, 'saveBtn').click(); time.sleep(1.5)
    check(json.load(open(PROJECT, encoding='utf-8'))['project']['title'] == 'The River Keeps (budget)', 'saving in the second tool writes to the same file')

    # Connect project folder: a conflicted copy next to the project file shows up, and a tool can make a folder
    # inside the project folder and write a file there, the way the release tracker copies in scans.
    shutil.copy(PROJECT, os.path.join(WORK, 'river (conflicted copy).oft.json'))
    shown = windows('.')
    d.execute_script("document.getElementById('oftFolderBtn').click()")
    check(choose_folder(before=shown), 'Choose the folder shows a folder dialog')
    check(wait(d, "!document.getElementById('oftCopies').hidden"), 'the tool finds the conflicted copy in the folder')
    os.remove(os.path.join(WORK, 'river (conflicted copy).oft.json'))
    go(d, 'tools/release-tracker/index.html')
    d.execute_script("const b = document.querySelector('#peopleCov .is-missing .cov-sig'); if (b) b.click();")
    check(wait(d, "!document.getElementById('connectFolderBtn').hidden"), 'the release tracker offers Connect project folder')
    shown = windows('.')
    d.execute_script("document.getElementById('connectFolderBtn').click()")
    check(choose_folder(before=shown), 'Connect project folder shows a folder dialog')
    check(wait(d, "/Connected/.test(document.getElementById('toast').textContent)"), 'and connects the folder the project file is in')
    d.execute_script("""const path = arguments[0];
      (async () => { const dir = window.oftDesktopHandle(path, 'directory');
        const sub = await dir.getDirectoryHandle('scans', { create: true });
        const w = await (await sub.getFileHandle('release.txt', { create: true })).createWritable();
        await w.write('signed'); await w.close(); window.__dirTest = (await dir.resolve(await sub.getFileHandle('release.txt'))).join('/'); })().catch(e => { window.__dirTest = String(e); });""", WORK)
    wait(d, 'window.__dirTest')
    check(d.execute_script('return window.__dirTest') == 'scans/release.txt' and open(os.path.join(WORK, 'scans', 'release.txt')).read() == 'signed', 'a tool can make a folder in the project folder and save a file there')

    # Under WebDriver, WebKitGTK ignores window.print(), so ask the app to print the way it does on a Mac.
    d.execute_script("setTimeout(() => window.__TAURI_INTERNALS__.invoke('plugin:webview|print'), 50)")
    printed = False
    for _ in range(40):
        time.sleep(0.25)
        if any('Print' in xdo('getwindowname', w) for w in windows('.')):
            printed = True
            xdo('key', 'Escape')
            break
    check(printed, 'Print opens the print dialog')
    d.quit()

    # A new launch starts with nothing open, and offers the file it remembers.
    d = start()
    go(d, 'tools/gear-list/index.html')
    check(wait(d, "!document.getElementById('oftReopen').hidden"), 'after a restart, a tool offers the file you had open')
    d.find_element(By.ID, 'oftReopenBtn').click()
    check(wait(d, "document.getElementById('filmTitle').textContent.includes('(budget)')"), 'one click opens it again')
    d.quit()
finally:
    driver_proc.terminate(); xvfb.terminate()
    subprocess.run(['pkill', '-f', 'WebKitWebDriver'], capture_output=True)
fails = [w for ok, w in results if not ok]
print('FAILS', fails)
sys.exit(1 if fails else 0)
