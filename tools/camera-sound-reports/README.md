<p align="center">
  <b>What was shot, on which card, and how.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Camera and sound reports

Log what was shot on each card or roll: a camera report with the clips, codec, frame rate and lens notes, and a sound report with each file, its tracks and notes. Link them to the shoot day and its call sheet, print them for the shoot, and export a CSV for the edit.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#62](https://github.com/open-filmmaker-toolkit/toolkit/issues/62).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's cards, clips and settings are made up.

## What it does

- **A camera report for each card:** the camera and operator, codec, resolution, frame rate and lens notes, and each clip with what or who it is, timecode, lens, notes and whether it's circled. When you don't log every clip, fill in the first and last.
- **A sound report for each card or roll:** the recorder and sound recordist, file format, sample rate and bit depth, timecode, the track layout, and each file with its tracks and notes. New files start with the report's track layout.
- **Scene, setup and take for each clip,** for scripted scenes, with the script supervisor's notes. They print as a slate number such as 12A-3, and the [daily production report](../daily-production-report/) counts setups and takes from them.
- **Linked to the shoot day** from the [shooting calendar](../shooting-calendar/), and to the [call sheet](../call-sheet/) started from that day. Reports are grouped by day, and the side panel lists shoot days so far with no reports.
- **A new report picks up the last one's settings,** with the next card name, such as A002 after A001.
- **Offload:** say where the card was copied, relative to your project file, and whether it's backed up. The card is recorded in the project's files, and the list flags cards not offloaded or not backed up.
- **Prints** every report for a day, or one report, with the settings and the clip list. **Exports CSV for the edit,** one row for each clip or file. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

The [interview log](../interview-log/) links interviews to the cards they're on.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/camera-and-sound-reports-template.csv) with the same columns as the export.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/camera-and-sound-reports-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

`mediaReports`: each has an `id`, `kind` (`camera` or `sound`), and optional `shootDayId`, `callSheetId`, `date`, `roll`, `device`, `operatorId`, `firstClip`, `lastClip`, `clips` (each with `id`, and optional `clip`, `subject`, `tc`, `lens`, `good`, `notes`, `scene`, `shot`, `take` and `scriptNotes`), `assetId`, `backedUp` and `notes`.

- Camera reports add `codec`, `resolution`, `frameRate` and `lensNotes`. Sound reports add `fileFormat`, `sampleRate`, `timecode` and `trackLayout`.
- Each clip or file has an `id` and optional `clip`, `subject`, `tc`, `lens` (the tracks, for sound), `good` (circled) and `notes`.
- The card is an asset with `type` "camera card" or "sound card" and a `relativePath`, linked by `assetId`.

It reads `people`, `locations`, `shootDays` and `callSheets`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reading clip names and metadata from the card itself
- Checksums for offloads
- Syncing camera clips with sound files

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
