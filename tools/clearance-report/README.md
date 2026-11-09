<p align="center">
  <b>Every reference in the film, and how it's cleared.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Annotated-transcript clearance report

Produce the annotated script or transcript an errors and omissions insurer asks for. Import the as-broadcast script or a transcript of the cut with its timecodes, mark every reference to a person, place, product, quote, music or archival material, and see how each one is cleared. Then print the report.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#75](https://github.com/open-filmmaker-toolkit/toolkit/issues/75).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's script and marks are made up.

## What it does

- **Imports a script or transcript** as SRT or VTT, a Word document, a PDF with text in it (not a scan), noScribe's HTML, or text with a timestamp at the start of each paragraph, or uses a transcript already in the [paper edit](../paper-edit/). Set the timecode at time zero, such as 01:00:00:00, and the frame rate, so each line shows its program timecode.
- **Mark references.** Select words in a line and press Mark to note a person, place, product or logo, quote, music, archival material, artwork or something else. The tool guesses from the words when they're a name in the project. When the words run on into the next line, tick the box and they're highlighted on both lines. **Add it to the clearance log** makes a new clearance log element from the marked words, at the line's timecode, and links the mark to it.
- **Find names from the project:** marks every mention of the project's people, places and music titles in one go, for you to check.
- **Shows each mark's clearance.** People and places use their appearance and location releases, the way the [release tracker](../release-tracker/) works them out. Everything else uses the element's status in the [clearance log](../clearance-log/), with its license. When something is cleared another way, such as a public figure in the news, say so with a note, or mark it not cleared.
- **Prints the report:** every line with its timecode, the marked words numbered, and each mark's clearance beside it, then a list of what isn't cleared yet. **Exports CSV,** one row for each mark. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/clearance-report-template.csv) with the same columns as the export.

This is not legal advice. Your insurer and attorney decide what needs clearing. See [Not legal advice](../../README.md#not-legal-advice).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `clearanceReport` record with `scripts`. Each script has an `id`, `name`, `format`, `frameRate`, optional `startTc`, `segments` (each an `id`, `text`, and optional `start`, `end` and `speaker`) and `marks`.

Each mark has an `id`, `segId` (its line), `words`, `kind` (`person`, `place`, `product`, `quote`, `music`, `archival`, `artwork` or `other`), and optional `endSegId` (the next line, when the words run on into it), `personId`, `locationId` or `elementId`, `override` (`cleared` or `not`), `note` and `auto` (found from the project's names).

It reads `people`, `locations`, `thirdPartyElements`, `contracts` and `paperEdit`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
