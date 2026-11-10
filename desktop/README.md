# Desktop app (test build)

The Open Filmmaker Toolkit in its own window, for Mac, Windows and Linux. It's the same tools as the website. The difference is that saving goes straight back to your project file on every computer, including the ones where Firefox and Safari can only download a new copy.

This is a first test build. It isn't signed yet, and it isn't on the home page.

## Try it on a Mac

1. On GitHub, open **Actions**, then **Desktop app**, then **Run workflow**. It takes about 15 minutes.
2. When it's done, open the run and download **open-filmmaker-toolkit-mac** under Artifacts. Unzip it and open the `.dmg`.
3. Drag **Open Filmmaker Toolkit** to Applications.
4. The app isn't signed by Apple yet, so the first time you open it, macOS says it can't check it. Open **System Settings**, then **Privacy & Security**, scroll down and choose **Open Anyway**. You only need to do this once.

Then check what step one is for:

- **Open and save.** Open a project file, change something and save. It should save straight back to the same file, with no dialog and no copies.
- **Move between tools.** Go to another tool and back home. The project should stay open.
- **Export.** Export something, like the crew list from the call sheet. The app asks where to save it.
- **Print.** Print a call sheet or a report. The Mac print dialog should open with the printout, and you can save it as a PDF from there.
- **Reopen.** Quit the app and open it again. A tool should offer to open the file you had open.
- **Connect project folder.** In the release tracker, open a release and choose **Connect project folder**. The folder dialog should open in your project file's folder. Attach a scan and save, and the scan should appear in a `scans` folder next to your project file.

## How it works

The tools already save through the file picker that Chrome and Edge have and Safari and Firefox don't. [`bridge.js`](bridge.js) runs before every page in the app and gives the tools that picker, backed by the app's own file access, so the tools don't change at all. It also:

- turns downloads into a save dialog
- opens web links in your browser instead of in the app
- gives the tools a folder picker, for **Connect project folder** and for finding conflicted copies your sync app made
- hides what only applies on the website, like installing the toolkit as an app (anything marked `class="web-only"`)
- on a Mac, tells each tool to build its printout before the print dialog opens

The app is built with [Tauri](https://tauri.app). It uses the browser engine already on the computer: Safari's engine on a Mac, Edge's on Windows, and WebKitGTK on Linux. That keeps the download to a few megabytes.

- [`stage.py`](stage.py) copies the toolkit's pages into `dist/` for the app to load. Nothing in them is changed.
- [`src-tauri/`](src-tauri) is the app itself: the window, the plugins for dialogs, files and links, and [what the pages are allowed to do](src-tauri/capabilities/default.json). That's picking files and folders, reading and writing the files you pick and what's inside the folders you pick, printing, and opening web links in your browser.
- The app makes no network requests of its own. The call sheet's optional weather lookup works as it does on the website, only when you click it.

The tools have no build step and no dependencies, and that doesn't change. Everything to do with building the app stays in this folder.

## Build it yourself

You need [Rust](https://rustup.rs), Node and Python 3, plus on Linux the WebKitGTK libraries (`libwebkit2gtk-4.1-dev` and friends, see the [Tauri prerequisites](https://tauri.app/start/prerequisites/)).

```
cd desktop
npm ci
npx tauri dev                    # run it
npx tauri build                  # make an installer for this computer
```

## Test

[`tests/smoke.py`](tests/smoke.py) drives the real app on Linux. It covers:

- opening a project through the real file dialog
- saving back to the same file
- exporting
- carrying the project to another tool and saving there
- connecting the project folder, finding a conflicted copy in it, and writing a scan into a folder inside it
- hiding the website-only notes
- printing
- reopening the remembered file after a restart

It needs a debug build (`npx tauri build --debug --no-bundle`), `tauri-driver` (`cargo install tauri-driver`), WebKitWebDriver, Xvfb, xdotool and selenium. The [Desktop app workflow](../.github/workflows/desktop.yml) runs it, along with the Mac build.

There's no way to drive the app automatically on a Mac, so the Mac checks above are by hand.

## Not yet

- Signing for Mac and Windows, so there's no warning the first time you open it
- Windows and Linux installers in the workflow (the code is ready; only Linux is tested)
- A Releases page and a link from the home page
- Updates. For now, you download a new version.
