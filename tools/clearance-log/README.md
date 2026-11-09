<p align="center">
  <b>Track every piece of third-party material in your film until it's cleared.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Clearance log

Track every piece of third-party material in your film (archival footage, stills, music, artwork, logos, recognizable people) until it's cleared. Then print a report for your E&O attorney.

This is the first tool in the [Open Filmmaker Toolkit](../../README.md) and the first slice of the shared project file ([#13](https://github.com/open-filmmaker-toolkit/toolkit/issues/13)). Tracking issue: [#18](https://github.com/open-filmmaker-toolkit/toolkit/issues/18).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving](#saving)
- [Project file format](#project-file-format)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests, so it also works offline.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The same file opens in the [music cue sheet](../music-cue-sheet/).

## What it does

- **Log elements.** For each one, record what it is, its type, source, rights holder and contact, where it sits in the cut (timecode in and out), how it's used, the rights you need, cost, the license or memo on file, and notes.
- **Track status.** Not started, Requested, Negotiating, Licensed, Fair use, Public domain, or Replace or cut. Licensed, Fair use and Public domain count as cleared.
- **See where you stand.** The filmstrip shows one frame per element, colored by status. Below it are cleared counts, total licensing cost and total timed footage.
- **Find things.** Search, filter by status or type, and sort by any column.
- **Print a report.** Prints the elements currently shown, with a status summary, for your E&O attorney or a production meeting.
- **Export CSV.** Exports every element for a spreadsheet, whatever the filters. The blank [spreadsheet template](../../templates/clearance-log-template.csv) has the same columns, and there's a [Word version](../../templates/clearance-log-template.docx) to fill in or print, for anyone who doesn't use the tool.
- **Export project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files. Nested values stay as JSON inside their cell.

**Edit film details** holds the title, production company, producer, who prepared the log and how to reach them, and the cut the timecodes refer to. All of these print at the top of the report. Update the cut whenever you re-time the log against a new version of the edit.

Lengths are worked out from timecode at the film's frame rate (also set in **Edit film details**). Drop-frame timecode is treated as non-drop, so long 29.97 segments can be off by a frame or two.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/clearance-log-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Finds archive and music in the edit:** import the locked cut's CMX 3600 edit list. Each source clip is matched to the clearance log, by clip names it has matched before or by the element's license file, description or source, and to your own footage in the footage log. It shows new material that isn't in the log yet, elements that are no longer in the cut, and updates each element's uses with the timecodes from the edit, for the clearance report and cue sheet.
- **Links the license file** for each element: where the signed license or memo is, relative to your project file. Pick the file to fill in its name. Signed copies recorded in the [license tracker](../license-tracker/) show there too.
- **People and places in an element,** with their release status from the [release tracker](../release-tracker/): signed, not signed yet, expired, declined or no release. Open **People and places in it** in the element's editor.

## Saving

Your log lives in a project file on your computer (`your-film.oft.json`).

- **Chrome and Edge** save straight back to the file you opened.
- **Safari and Firefox** download a new copy each time you save. Keep the latest one with your project files.
- If the file changed on disk since you opened it, Chrome or Edge warns before saving. You can reload the latest version, save your edits as a copy, or explicitly overwrite the changed file.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time. That copy is a safety net, not a substitute for saving the file: clearing browser data deletes it.

## Project file format

The file is plain JSON. The shared [version 1 schema](../../schemas/project-v1.schema.json) documents the complete format, including data owned by other tools:

```json
{
  "format": "open-filmmaker-toolkit/project",
  "formatVersion": 1,
  "project": {
    "title": "", "company": "", "producer": "",
    "preparedBy": "", "preparedContact": "", "cutVersion": "",
    "frameRate": 24, "currency": "USD"
  },
  "thirdPartyElements": [
    {
      "id": "…", "description": "…", "type": "Music", "status": "negotiating",
      "source": "…", "rightsHolder": "…", "contact": "…",
      "tcIn": "00:11:02:00", "tcOut": "00:12:30:00",
      "use": "…", "rights": "…", "cost": 3500, "licenseRef": "…", "notes": "…",
      "personIds": ["…"], "locationIds": ["…"], "licenseAssetId": "…"
    }
  ]
}
```

The clearance log only changes `project`, `thirdPartyElements`, and the license files it links, which are `assets` with `type` "license file" and a `relativePath`. Anything else in the file, such as the cue sheet credits the music cue sheet keeps on each Music element, is kept as it is when you save.

Status values are `not-started`, `requested`, `negotiating`, `licensed`, `fair-use`, `public-domain` and `replace`.

## Not yet

- Installing as an offline app (works offline now as a saved file; installable once the site is published)

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
