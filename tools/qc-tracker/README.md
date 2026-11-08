<p align="center">
  <b>Every QC note fixed, waived or argued, until the master passes.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# QC tracker

Track quality-control reports and fixes until the master passes. Log each issue with its timecode and severity, print a fix list for whoever fixes it, and record the version it was fixed in.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#85](https://github.com/open-filmmaker-toolkit/toolkit/issues/85).

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

- **Master versions** with dates, and whether each has passed QC.
- **QC reports** for a version, with the QC house, date and result: waiting, failed or passed.
- **Issues** with timecode or a range, severity (major, minor or a note), area (picture, sound, captions or other), who fixes it, and the fix: open, fixed, waived or disputed, with the version it was fixed in.
- **A fix list** of open and disputed issues, for everyone or for the editor, colorist, mixer or captioner, with counts by severity. **Prints** it in timecode order.
- **Exports CSV** of every issue in every report.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/qc-issues-template.csv) with the same columns as the export.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/qc-issues-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Links issues to cuts** in the [cut version tracker](../cut-tracker/): the cut an issue was found in and the cut that fixed it. The cut tracker shows each cut's open QC issues and fixes.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `qc` record with `versions` (`name`, `date`, `notes`) and `reports` (`versionId`, `vendor`, `date`, `result` of `pending`, `fail` or `pass`, `notes`, and `issues`). Each issue has `tc`, `tcOut`, `description`, `severity`, `area`, `owner`, `fix`, `fixedInId` (a version), and `cutId` and `fixedCutId` (in `cuts`).

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Importing QC reports from a QC house's file
- Markers for an editing app

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
