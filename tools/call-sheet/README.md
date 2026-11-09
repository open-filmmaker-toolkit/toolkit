<p align="center">
  <b>Shoot-day call sheets built from the people and locations already in your project.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="Online lookups: optional" src="https://img.shields.io/badge/online%20lookups-optional-d29922" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Call sheet

Build a printable call sheet for each shoot day, using the crew and locations you already entered for the rest of your project.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#21](https://github.com/open-filmmaker-toolkit/toolkit/issues/21).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Optional online lookup](#optional-online-lookup)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs and no accounts.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo.

## What it does

- **Lists your shoot days** by date, with general call, location and crew count.
- **Edits a day:** date, label, general call, wrap, location, parking, weather, sunrise and sunset, nearest hospital, a schedule, and notes.
- **Picks crew from your project.** Check who's working, set a role and call time for each, or **Use general call for everyone checked**. Add a person or location without leaving the day.
- **Copies a day to the next one,** keeping crew, location and hospital, and clearing weather and daylight.
- **Lists the day's scenes** when the [stripboard](../stripboard/) has put scenes on the shoot day: each scene's number, set, day or night, pages and cast numbers, with its shots from the [shot list](../shot-list/). They show in the editor and on the printed sheet; change them in those tools.
- **Opens the sides** for a day whose scenes are on the [stripboard](../stripboard/): choose **Print sides** in the day's editor, and the [sides](../sides/) tool opens in a new tab with the project and that day.
- **Prints** one portrait page per day. Choose "Save as PDF" in the print dialog to make a PDF.
- **Exports call sheets as a spreadsheet (CSV).** One day from the editor, or every day at once. The layout matches the blank [call sheet template](../../templates/call-sheet-template.csv), which opens in Excel, Numbers or Google Sheets, so people can fill it in by hand without this tool.  Save it as `.xlsx` from there if you need that format.
- **Exports a crew list (CSV)** with one row per person per day.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files. Nested values stay as JSON inside their cell.
- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Release status** for people on camera and the location, from the [release tracker](../release-tracker/), in the editor and on the printed sheet.
- **The day's permits and insurance certificates** from the [certificate and permit tracker](../coi-permit-tracker/): the ones that name the shoot day, or its location when they name no days.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead of checking or overwriting the original file.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

## Optional online lookup

Everything works offline. The **Look up weather and daylight** button is the only thing that uses the network, and nothing is sent unless you click it and confirm.

- It sends the location's address to `photon.komoot.io` to find coordinates (skipped if the location already has them).
- It sends the coordinates and date to `api.open-meteo.com` for the forecast, sunrise and sunset.
- Forecasts cover about the next two weeks. For later dates, type the weather in by hand.
- Check what it fills in before you print.

## What it adds to the project file

A `callSheets` array. Each entry has an `id` and `date`, and optionally times, a `locationId`, weather, hospital, schedule and a `crew` list of `personId` with role and call time. Locations may gain `latitude` and `longitude` after a lookup. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- A DOCX export (the spreadsheet export and blank template cover plain-file use)
- Sending the sheet to the crew

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
