<p align="center">
  <b>Everything about a trip on one sheet.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Travel sheet

Give everyone on a trip one sheet: who's going, flights, trains and drives, hotels, ground transport, local contacts, the emergency number and the nearest hospital. Print one sheet for everyone, or one for each person with only their own travel.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#59](https://github.com/open-filmmaker-toolkit/toolkit/issues/59).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's trip, flight, motel and contacts are made up.

## What it does

- **Trips from the [shooting calendar](../shooting-calendar/).** Shoot days that share a trip name show up in the side panel; make a sheet from one and it starts with the dates, the people on those days and the locations.
- **Who's going,** picked from the project's people, and the locations, picked from the project's locations.
- **Travel for each person:** flights, trains, drives, cars and shuttles, with the date, times, from and to, the airline or company, the flight or train number and the confirmation. Tick who each one is for; nobody ticked means everyone. A trip flags anyone going who isn't on any travel.
- **Places to stay,** with address, phone, check-in and check-out, confirmation and who's staying.
- **Local contacts,** such as a fixer, driver or location contact.
- **Emergencies:** the local emergency number and the nearest hospital. If a [call sheet](../call-sheet/) for the trip's locations or dates already lists a hospital, the tool offers it.
- **Costs:** a per diem for each trip, a day for each person on it, and what each leg and place to stay costs.
- **Sends them to the budget:** choose **Send costs to the budget** under the file buttons and pick an account. Each trip gets a line for its per diems (days × people × the per diem), one for its travel and one for its places to stay. From then on the lines follow the travel sheet.
- **Prints a travel sheet** with the emergency details at the top, then the itinerary in order (travel, check-ins and check-outs, and the shoot days), places to stay, locations, and contacts with everyone's phone and email. Pick one person and the sheet shows only their travel. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/travel-sheet-template.csv) with the same columns as the export.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/travel-sheet-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

`trips`: each has an `id`, `name`, and optional `perDiem`, `block` (the trip in the shooting calendar, matched by `shootDays[].block`), `destination`, `startDate`, `endDate`, `personIds`, `locationIds`, `legs`, `stays`, `contacts`, `emergencyNumber`, `hospital` (`name`, `address`, `phone`) and `notes`.

- Each leg has an `id`, a `kind` (`flight`, `train`, `drive`, `ground` or `other`), and optional `date`, `departs`, `arrives`, `from`, `to`, `carrier`, `number`, `confirmation`, `cost`, `personIds` and `notes`.
- Each stay has an `id` and optional `name`, `address`, `phone`, `checkIn`, `checkOut`, `confirmation`, `cost`, `personIds` and `notes`.
- Each contact has an `id` and optional `name`, `role`, `phone` and `notes`.

A leg or stay with no `personIds` is for everyone on the trip. It reads `people`, `locations`, `shootDays` and the hospitals on `callSheets`. Sending costs to the budget adds lines to `budget` with a `source` and keeps the account in `budgetLinks`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Passport and visa details for each person
- Time zones on travel that crosses them
- Sending each person their own sheet

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
