<p align="center">
  <b>Every clip, findable.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Footage log

Catalog every clip so the editor can find it: what's in it, who's in it, where and when, with topics, notes and a rating. Bring in the clip names from a folder, a CSV or your camera reports, and export a CSV for your editing app.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#67](https://github.com/open-filmmaker-toolkit/toolkit/issues/67).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's clips, tags and ratings are made up.

## What it does

- **Import clips from a folder.** Pick the folder with your footage and the tool lists the video and audio files in it and its subfolders, with each one's location relative to your project file and the date it was last changed. Nothing is uploaded and the files aren't opened.
- **Import from a CSV,** such as a clip list from your editing app or another log. The tool reads common column names: File Name, Clip Directory or Path, Date, Description, People, Location, Keywords or Topics, Rating, Comments or Notes, Start TC, Duration and Card. People and places are matched to the project by name; names it doesn't know go in the notes.
- **Import from [camera and sound reports](../camera-sound-reports/):** each logged camera clip comes in with its card, what's in it, timecode, the shoot day's date and place, and circled clips rated four stars.
- **Tag people, locations and topics** from the project, and add notes and a rating from one to five stars. Select several clips and tag them at once.
- **Find clips** by words in their names, descriptions, notes or topics, or by who, where, topic or rating. The side panel counts clips for each person and place.
- **Exports CSV** of the clips shown, with column names DaVinci Resolve's metadata import uses (File Name, Clip Directory, Description, Keywords, Comments), so it can match clips by file name; check the result in your app. Other apps open it as a spreadsheet. **Prints** the clips shown. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/footage-log-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Clips are `assets` with `type` "clip", a `name` (the file name), and optional `relativePath`, `date`, `description`, `personIds`, `locationIds`, `topics`, `rating` (1 to 5), `notes`, `timecode`, `duration`, `card`, and `mediaReportId` and `clipId` for a clip that came from a camera report.

It reads `people`, `locations`, `shootDays` and `mediaReports`. Everything else in the file is preserved, including other assets. See the [data model notes](../../schemas/README.md).

## Not yet

- Reading each clip's length, timecode and other metadata from the file itself
- Thumbnails
- Exporting an Avid ALE
- Tagging moments inside a clip; use the [interview log](../interview-log/) for interviews

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
