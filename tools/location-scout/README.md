<p align="center">
  <b>What you learn on a location scout, with your photos, ready to print for the crew.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Location scout sheet

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

- **One scout for each visit,** with the date, who scouted, a verdict (good to film, maybe, or not for us), and who to call there.
- **The things a crew asks about:** access and hours, power, sound, light, parking and load-in, restrooms, cell signal, and permits and permission, plus notes.
- **Photos that stay on your computer.** Add scout photos, with captions. They're resized to 1280 pixels on the long side and kept in the project file. Nothing is uploaded.
- **Links to the place in the project.** Pick a location, or add a new one; it's added to the project for call sheets and releases to use. The side panel lists places with no scout yet.
- **Shows the location release** from the [release tracker](../release-tracker/): signed, waiting for signature, or none yet, so you know what to sort out before the shoot.
- **Prints a scout report** for each scout, on its own page, with the photos. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [scout sheet](../../templates/location-scout-template.docx) to print and fill in on the visit, and a [spreadsheet template](../../templates/location-scout-template.csv) with the same columns as the export.

Scout reports have contact details in them. Keep printed copies private.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `scouts` list. Each scout has an `id` and a `locationId`, pointing to a place in `locations`, and optional `date`, `scoutedBy`, `verdict` (`good`, `maybe` or `no`), `contactName`, `contactPhone`, `contactEmail`, `access`, `power`, `sound`, `light`, `parking`, `restrooms`, `cellSignal`, `permits`, `notes` and `photoIds`.

Photos are `assets` with `type` "scout photo", the image as a JPEG data URL in `data`, its `width` and `height`, and an optional `caption`. Adding a new place adds it to `locations`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Pinning the place on a map, or the sun's path for a given day
- Linking photos stored in the project folder instead of in the file, for long scouts with many photos
- A scout checklist you can change, for crews who ask about different things

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
