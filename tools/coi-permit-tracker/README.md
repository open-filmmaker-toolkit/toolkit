<p align="center">
  <b>Certificates and permits in hand before every shoot day.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# COI and permit tracker

Log the certificates of insurance you request from rental houses and locations, and the filming permits you apply for: who issued them, who's named on them, their conditions and when they expire. Link them to locations and shoot days, and see what's missing or about to run out before each day.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#58](https://github.com/open-filmmaker-toolkit/toolkit/issues/58).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's certificates, permits and insurer are made up.

## What it does

- **Certificates of insurance** for each vendor and location: requested, received or still needed, with the dates, the insurer or broker, and who's named on it, such as the certificate holder and additional insured.
- **Filming permits:** the issuing office, the permit number, applied for and issued dates, the dates it's in effect, and its conditions.
- **Linked to locations and shoot days.** A certificate or permit picked for shoot days covers those days. One picked only for locations covers every day at those locations.
- **Before each shoot day,** the side panel lists every upcoming day from the [shooting calendar](../shooting-calendar/) with what's missing: anything not received or issued yet, anything that expires before the day or isn't in effect yet, and anything that expires within a week after. It also flags rental houses with gear packed for the day in the [gear list](../gear-list/) and no certificate, and locations with nothing logged, so you can check whether they need a permit.
- **Expiring soon:** certificates and permits that run out in the next 30 days, and rental houses in the gear list without any certificate.
- **Keeps the scan.** Attach the certificate or permit as a PDF or photo. In Chrome and Edge, connect the project folder and it's copied into a `certificates-and-permits` folder next to your project file; otherwise the tool records the file name, and you keep the file there.
- **Permit fees,** sent to the budget: choose **Send costs to the budget** under the file buttons and pick an account. Each permit with a fee gets a line, which follows the permit from then on.
- **Prints a shoot-day check** with each upcoming day and everything logged. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/certificates-and-permits-template.csv) with the same columns as the export.

This is not legal or insurance advice. Check with your insurer what a vendor or location needs on a certificate, and with the film office what a permit covers. See [Not legal advice](../../README.md#not-legal-advice).

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/certificates-and-permits-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Certificates and permits are `contracts` with `type` "certificate of insurance" or "permit" and a `status`: `needed`, `requested` or `received` for certificates, and `needed`, `applied` or `issued` for permits. Both have optional `requestedDate` (applied for, for permits), `receivedDate` (issued, for permits), `effectiveDate`, `expirationDate`, `locationIds`, `shootDayIds`, `notes` and `assetIds` (the scan, an asset with `type` "certificate scan" or "permit scan"). Certificates add `vendor`, `insurer` and `namedOn`; permits add `issuer`, `reference` (the permit number), `conditions` and `fee`. Sending fees to the budget adds lines to `budget` with a `source` and keeps the account in `budgetLinks`.

It reads `locations`, `shootDays` and the rental houses in `gear`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Insurance requirements for each vendor, such as limits to check a certificate against
- Linking certificates to call sheets

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
