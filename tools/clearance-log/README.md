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
- **Export CSV.** Exports every element for a spreadsheet, whatever the filters.

**Edit film details** holds the title, production company, producer, who prepared the log and how to reach them, and the cut the timecodes refer to. All of these print at the top of the report. Update the cut whenever you re-time the log against a new version of the edit.

Lengths are worked out from timecode at the film's frame rate (also set in **Edit film details**). Drop-frame timecode is treated as non-drop, so long 29.97 segments can be off by a frame or two.

## Saving

Your log lives in a project file on your computer (`your-film.oft.json`).

- **Chrome and Edge** save straight back to the file you opened.
- **Safari and Firefox** download a new copy each time you save. Keep the latest one with your project files.

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
      "use": "…", "rights": "…", "cost": 3500, "licenseRef": "…", "notes": "…"
    }
  ]
}
```

The clearance log only changes `project` and `thirdPartyElements`. Anything else in the file, such as the cue sheet credits the music cue sheet keeps on each Music element, is kept as it is when you save.

Status values are `not-started`, `requested`, `negotiating`, `licensed`, `fair-use`, `public-domain` and `replace`.

## Not yet

- Importing an existing clearance spreadsheet (CSV)
- Attaching license PDFs to an element
- Linking to people and locations from the release tracker
- Installing as an offline app (works offline now as a saved file; installable once the site is published)

## License

Pending legal review ([#3](https://github.com/open-filmmaker-toolkit/toolkit/issues/3)). This tool is a working record, not legal advice.
