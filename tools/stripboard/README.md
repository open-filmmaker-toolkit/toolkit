<p align="center">
  <b>The script's scenes, arranged into shoot days.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Stripboard

Schedule a scripted shoot the way assistant directors always have: one strip for each scene, colored by interior or exterior and day or night, arranged into shoot days. Each day shows its page count, its cast and whether there's a company move, and the days are the same shoot days the shooting calendar and call sheets use.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#168](https://github.com/open-filmmaker-toolkit/toolkit/issues/168).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. Two of its five reenactment scenes are on the Nov 10 shoot day and one on Mar 16; the other two aren't scheduled yet. Everything in the sample is made up.

## What it does

- **A strip for each scene** from the [script breakdown](../script-breakdown/): scene number, interior or exterior, set, time of day, length in eighths of a page and the cast by number. Strips are colored the usual way: white for interior day, yellow for exterior day, blue for interior night and green for exterior night. Scenes cut from the script aren't shown.
- **Moves strips between days** by dragging, or from each strip's menu, which works by keyboard. The arrows reorder strips within a day, which is the shooting order.
- **Shows each day's page count, scenes and places,** and flags a company move when a day's scenes are in more than one place.
- **Uses the shooting calendar's shoot days.** Add a day here and it's in the [shooting calendar](../shooting-calendar/) too. When a day gets scenes, it gets the actors who play the parts, the place of its first scene if it had none, and a title listing its scenes if it had none. A title you wrote is kept.
- **The side panel** totals the schedule (days, scenes and pages scheduled, pages a day and company moves) and shows how many days each character works. The [day-out-of-days](../day-out-of-days/) has the full report.
- **Prints the board** day by day, landscape, with the scenes not yet scheduled at the end. **Exports CSV,** one row per scene with its day. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets, scenes or shoot days as separate CSV files.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared project file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `sceneIds` list on each shoot day in `shootDays`, in shooting order, referring to `scenes`. Adding a day adds a shoot day with an `id`, a `date`, `kind` `shoot` and optional `title` and `notes`. Scheduling scenes can fill in a day's `personIds`, `locationId` and `title`, as described above. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Banners and day breaks with notes, and a one-line print of the whole board
- Sorting the unscheduled strips by set, cast or time of day
- Moving several strips at once

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
