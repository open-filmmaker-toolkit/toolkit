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

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs and no accounts.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo.

## What it does

- **Lists your shoot days** by date, with general call, location and crew count.
- **Edits a day:** date, label, general call, wrap, location, parking, weather, sunrise and sunset, nearest hospital, a schedule, and notes.
- **Picks crew from your project.** Check who's working, set a role and call time for each, or **Use general call for everyone checked**. Add a person or location without leaving the day.
- **Copies a day to the next one,** keeping crew, location and hospital, and clearing weather and daylight.
- **Prints** one portrait page per day. Choose "Save as PDF" in the print dialog to make a PDF.
- **Exports a crew list (CSV)** with one row per person per day.

## Optional online lookup

Everything works offline. The **Look up weather and daylight** button is the only thing that uses the network, and nothing is sent unless you click it and confirm.

- It sends the location's address to `photon.komoot.io` to find coordinates (skipped if the location already has them).
- It sends the coordinates and date to `api.open-meteo.com` for the forecast, sunrise and sunset.
- Forecasts cover about the next two weeks. For later dates, type the weather in by hand.
- Check what it fills in before you print.

## What it adds to the project file

A `callSheets` array. Each entry has an `id` and `date`, and optionally times, a `locationId`, weather, hospital, schedule and a `crew` list of `personId` with role and call time. Locations may gain `latitude` and `longitude` after a lookup. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- A plain DOCX or spreadsheet template ([#22](https://github.com/open-filmmaker-toolkit/toolkit/issues/22))
- Scene and shot lists, and sending the sheet to the crew
