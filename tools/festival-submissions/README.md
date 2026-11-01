<p align="center">
  <b>Every festival you submit to, with its deadline, fee, platform and result, and the screening dates once you're in.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Festival submissions

Keep track of the festivals you plan to submit to, and the ones you have: the deadline, the fee and any waiver code, the platform you submit through, and where each one stands. When a festival accepts you, add its screening dates and see them in one list.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#78](https://github.com/open-filmmaker-toolkit/toolkit/issues/78).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's festivals are made up.

## What it does

- **Logs each submission** with the festival, the platform, a link, the deadline, the fee, a waiver code, the date you submitted, and notes.
- **Tracks status:** planned, submitted, accepted or declined. Filter the list by status; each filter shows how many festivals it holds. Search by festival, platform, waiver code, notes or screening venue.
- **Shows the next deadlines first.** Planned festivals with an upcoming deadline come first, then planned ones whose deadline has passed, then submitted, accepted and declined. Each planned row says how many days are left. A deadline within two weeks is flagged, and so is one that has passed.
- **Keeps screening dates for accepted festivals.** Add a date, time, venue and note for each screening. Accepted festivals show their next screening, and a side list shows every upcoming screening in date order.
- **Adds up the fees:** what's still to pay on planned festivals and what you've paid on submitted ones, in the project's currency.
- **Fills in the submitted date.** Change a festival to submitted and the date defaults to today. You can change it.
- **Exports CSV and prints** the list on one page. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

The festival link is stored as plain text. It only becomes a clickable link if it starts with `http://` or `https://`.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `festivals` list. Each festival has an `id` and a `status` (`planned`, `submitted`, `accepted` or `declined`), and optional `name`, `platform`, `url` (text), `deadline` (a date), `fee` (a number, in the project's currency), `waiverCode`, `submittedOn` (a date) and `notes`. An accepted festival can have `screenings`, each with an `id` and optional `date`, `time` (text), `venue` and `note`. Screenings are kept if you change the status later.

Everything else in the file is preserved, including fields this tool doesn't recognize. See the [data model notes](../../schemas/README.md).

## Not yet

- A festival strategy map, to plan which festivals to target and in what order ([#77](https://github.com/open-filmmaker-toolkit/toolkit/issues/77), planned)
- Reminders inside the tool, or a calendar file of deadlines and screenings
- Importing festivals from a spreadsheet or a submission platform
- Tracking laurels, screening fees or travel for each festival
- A shared list of festivals and their usual deadlines

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
