<p align="center">
  <b>The day's scenes from your script, printed small for cast and crew.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Sides

Sides are the pages of the script being shot on a given day, handed out with the call sheet. Pick a shoot day and this tool lays out its scenes from your script in shooting order, marks where each one starts and ends, and crosses out the rest of each page, ready to print at full or half size.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#170](https://github.com/open-filmmaker-toolkit/toolkit/issues/170).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. It opens on the Nov 10 shoot day, with scenes 2 and 4. Everything in the sample is made up.

## What it does

- **Lays out the script** you imported in the [script breakdown](../script-breakdown/) the way a screenplay prints, about 55 lines a page, so page numbers come out close to your screenwriting app's.
- **Shows a shoot day's scenes** from the [stripboard](../stripboard/), in shooting order. Each scene's pages are included, with START and END marks at its first and last lines and everything else on those pages crossed out.
- **Opens on the next shoot day with scenes,** or the day the [call sheet](../call-sheet/) sent you from: **Print sides** in a call sheet's editor opens this tool in a new tab with the project and that day.
- **Flags a scene that isn't in the script text,** such as one added by hand or renamed in a newer draft, so you know to import the script again.
- **Prints at full size,** one script page to a sheet, or **half size,** two pages side by side on a landscape sheet, to fold or cut for pockets. Each page is headed with the film, the shoot day and the page number.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared project file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Nothing. It reads `script`, `scenes` and `shootDays`, and only changes the film details if you edit them. Everything in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Revision colors, and scene numbers in the margins
- Adding the call sheet as the first page
- Watermarking each set of sides with the person's name

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
