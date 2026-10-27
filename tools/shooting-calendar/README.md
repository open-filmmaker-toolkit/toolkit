<p align="center">
  <b>Shoot days, travel days and holds across weeks or months, with who's needed and where.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Shooting calendar

Plan a production that shoots in bursts: each shoot day, travel day and hold, what you're filming, where, and who's needed. Group days into trips, start each day's call sheet from here, and send the whole calendar to your calendar app.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#53](https://github.com/open-filmmaker-toolkit/toolkit/issues/53).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's shoot days are made up.

## What it does

- **A month calendar and a list.** Shoot days, travel days and holds, colored by kind. Click a day to add one. The list groups days into trips or blocks, upcoming first, and can show past days too.
- **Adds several days at once.** Pick a first and last date to add a day for each, with the same details.
- **Links days to the project's people and locations,** so they're the same people and places the call sheets, releases and credits use. The side panel shows who's needed on the days coming up, and how often.
- **Numbers shoot days within a trip,** such as "Day 2 of 5".
- **Starts a call sheet from a shoot day,** with its date, day number, location and people, ready to finish in the [call sheet](../call-sheet/) tool. A day whose call sheet has moved to another date or place is flagged.
- **Exports a calendar file** (`.ics`) with an all-day event for each day; holds show as tentative. It opens in Google Calendar, Apple Calendar and Outlook.
- **Prints a month view,** one landscape page for each month with days in it. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/shooting-calendar-template.csv) with the same columns.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `shootDays` list. Each day has an `id`, a `date` and a `kind` (`shoot`, `travel` or `hold`), and optional `title` (what you're filming), `block` (the trip or block it belongs to), `locationId`, `personIds`, `callSheetId` and `notes`. Starting a call sheet adds an entry to `callSheets` with the day's date, `dayLabel`, `locationId` and `crew`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Times within a day, beyond what the call sheet holds
- Conflicts, such as one person needed in two places on the same day
- Adding new people and locations from here; for now, add them in the call sheet tool

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
