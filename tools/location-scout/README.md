<p align="center">
  <b>What you learn on a location scout, with your photos, ready to print for the crew.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Locations

Record what you learn when you visit a place you might film: who to call, when you can get in, power, sound, light, parking, restrooms, cell signal and permits, with your own photos. Link it to the place in your project and its location release, and print a scout report for the crew.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#55](https://github.com/open-filmmaker-toolkit/toolkit/issues/55).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's scouts and photos are made up.

## What it does

- **Every place in the film,** listed first: each place with its address, its scouts and what they found, and whether its location release is signed. **Add a place** or edit one, and **Add a scout** from any place. A place another tool still uses can't be removed, and the tool says where it's used.
- **Paste a list of places.** Paste one place per line, from your treatment, a spreadsheet or an email, with the address or city after a comma. You see every row first, and places already in the project are unticked. Plain text matching, with no AI.
- **One scout for each visit,** with the date, who scouted, a verdict (good to film, maybe, or not for us), and who to call there.
- **The things a crew asks about:** access and hours, power, sound, light, parking and load-in, restrooms, cell signal, and permits and permission, plus notes.
- **Photos that stay on your computer.** Add scout photos, with captions. They're resized to 1280 pixels on the long side and kept in the project file. Nothing is uploaded.
- **Or link them,** for long scouts with many photos. **Link photos in the project folder** keeps each photo where it is, at full size, and puts only its path and a small preview in the project file. The scout report shows the preview with the path to the full-size photo.
- **The sun's path.** Type the place's latitude and longitude, and pick a day: the tool shows sunrise and sunset with the direction of the sun, the golden hours, when the sun is highest and how high, and the sun's height each hour. It's worked out on your computer, and printed on the scout report.
- **A checklist you can change.** Untick the built-in items your crew doesn't ask about and add your own, such as drone rules. The checklist is the same for every scout in the project.
- **Links to the place in the project.** Pick a location, or add a new one; it's added to the project for call sheets and releases to use. The side panel lists places with no scout yet.
- **Shows the location release** from the [release tracker](../release-tracker/): signed, waiting for signature, or none yet, so you know what to sort out before the shoot.
- **Prints a scout report** for each scout, on its own page, with the photos. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [scout sheet](../../templates/location-scout-template.docx) to print and fill in on the visit, and a [spreadsheet template](../../templates/location-scout-template.csv) with the same columns as the export.

Scout reports have contact details in them. Keep printed copies private.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/location-scout-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `scouts` list. Each scout has an `id` and a `locationId`, pointing to a place in `locations`, and optional `date`, `scoutedBy`, `verdict` (`good`, `maybe` or `no`), `contactName`, `contactPhone`, `contactEmail`, `access`, `power`, `sound`, `light`, `parking`, `restrooms`, `cellSignal`, `permits`, `notes`, `photoIds`, `latitude`, `longitude`, `sunDate` (the day to show the sun for; the scout's date when it's missing), `utcOffset` (hours from UTC, when the place isn't in your computer's time zone) and `checklist` (answers to the project's own items, by item id).

Photos are `assets` with `type` "scout photo", the image as a JPEG data URL in `data`, its `width` and `height`, and an optional `caption`. A linked photo has a `relativePath` in the project folder and a small preview in `thumb` instead of `data`. A `scoutChecklist` object holds the built-in items the project `hidden`, and its `extra` items, each with an `id` and `label`. Adding a new place adds it to `locations`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Pinning the place on a map, which would need map tiles from the internet
- Showing linked photos at full size, which needs the project folder open in the browser

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
