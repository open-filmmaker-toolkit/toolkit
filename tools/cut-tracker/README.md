<p align="center">
  <b>Every cut, every note, and the one you locked.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Cut version tracker

Track every cut of the film: when it was made, how long it runs and what changed, who saw it at each feedback screening, and the notes they gave, each tied to a time in the cut and its scene. Keep track of which notes are done, deferred or carried to the next cut, and mark the locked cut.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#70](https://github.com/open-filmmaker-toolkit/toolkit/issues/70).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's cuts, screenings and notes are made up.

## What it does

- **A record for each cut:** name, date, running time and what changed. A new cut takes the next number after the last one, such as Fine cut 4 after Fine cut 3.
- **Feedback screenings** for each cut: when, and who saw it.
- **Notes,** each tied to a time or range in the cut, the scene from the [structure board](../structure-board/) and the shot when you know them, who gave it and the screening it came from.
- **Done, deferred or carried.** Mark each note to do, done or deferred. When you open a later cut, the notes still to do or deferred in earlier cuts can be carried into it: the copies start as to do with where they came from, and the originals are marked carried to that cut.
- **The locked cut.** Mark one cut locked and the project's cut version and running time are set from it, which the [clearance log](../clearance-log/) and [music cue sheet](../music-cue-sheet/) use for their reports. Only one cut is locked at a time.
- **Prints a cut's notes** by status and time, with what changed and the screenings. **Exports CSV** of every note. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/cut-notes-template.csv) with the same columns as the export.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

`cuts`: each has an `id`, `name`, and optional `date`, `runningTime`, `changes`, `locked`, `screenings` (each an `id`, `date` and `audience`) and `notes`.

Each note has an `id`, a `status` (`open`, `done`, `deferred` or `carried`), and optional `screeningId`, `tc` and `tcOut` (time in the cut), `cardId` (a card in `structure`), `shot`, `from`, `text`, `carriedToCutId`, and `carriedFromCutId` and `carriedFromNoteId` for a carried copy.

Locking a cut sets `project.cutVersion` to its name and date, and `project.runningTime` to its running time. It reads `structure`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Linking a cut to its exported file
- Shifting carried notes' times when scenes move
- Notes from people who fill in a form, rather than typed in by you

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
