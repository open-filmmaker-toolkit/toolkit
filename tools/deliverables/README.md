<p align="center">
  <b>Everything the distributor asked for, checked off.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Deliverables checklist

Track every deliverable a distributor or broadcaster asks for, from the DCP and the mixes to captions, artwork and the legal paperwork, with who's responsible and when it's due.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#84](https://github.com/open-filmmaker-toolkit/toolkit/issues/84).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's data is made up.

## What it does

- **The usual list to start from:** DCP, masters with titles and textless, broadcast master and trailer; 5.1 and stereo mixes, M&E and stems; closed captions, SDH, the dialogue and continuity list and other subtitles; key art, stills and the EPK; chain of title, E&O certificate, music cue sheet, credits, licenses, releases and the QC report.
- **Status, due date, who's responsible, specs and where the file is** for each. Mark items not needed, rename them, or add your own.
- **What the project already has:** approved stills, press notes, signed licenses and releases, credits and the latest QC result, with links to the [stills library](../stills-library/), [chain-of-title binder](../chain-of-title/), [music cue sheet](../music-cue-sheet/), [credits builder](../credits-builder/) and [QC tracker](../qc-tracker/).
- **Delivering to** a distributor and an overall due date, with overdue items and items due in the next two weeks listed.
- **A distributor's delivery schedule.** **Add a distributor's schedule** takes the list copied from their schedule, one item a line, and adds each as your own item marked with their name, in the section it most likely belongs to. Numbering, bullets and headings are left out, and so is anything already on the list. **Save your items as a list** writes them to a small file for another production, and **Add from a list** reads one back.
- **Prints a checklist** by section and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/deliverables-template.csv) with the same columns as the export.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/deliverables-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `deliverables` record with `deliverTo`, `dueDate` and `items`. Items are kept only for what you've changed or added: each has an `id`, a `key` (a built-in item such as `dcp` or `cue`), and optional `status` (`todo`, `progress`, `delivered`, `accepted` or `na`), `due`, `owner`, `spec`, `path`, `note` and `title`. Your own items add `custom` and `section`, and `schedule` when they came from a distributor's delivery schedule.

It reads `assets`, `contracts`, `credits`, `musicCueSheet`, `chainOfTitle`, `pressNotes` and `qc`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- More than one delivery at a time
- Checking files on disk

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
