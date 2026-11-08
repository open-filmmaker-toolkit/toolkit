<p align="center">
  <b>What each license covers, what you owe, and what runs out.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# License tracker

Track the terms of each archival and music license: the media, territory and term it covers, its dates, the fees and payment schedule, and the options and step deals you have to exercise in time. Licenses that are about to expire, options about to lapse and payments coming due are flagged.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#74](https://github.com/open-filmmaker-toolkit/toolkit/issues/74).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's licenses, fees and options are made up.

## What it does

- **License terms:** kind (archival, or music sync, master or both), licensor, status, media, territory, term, signed and start and end dates, fee, the credit it requires, and where the signed copy is.
- **Linked to the [clearance log](../clearance-log/)** both ways: pick the elements a license covers, and each element lists the license too. Archival and music that's licensed or being negotiated in the clearance log with no license here is listed, and a license started from one is filled in from it.
- **A payment schedule:** each payment's amount, due date and whether it's paid, with what's paid and still owed for each license and in total.
- **Options and step deals,** such as a festival license with an option for all media: what each adds, its fee, the date to exercise it by and whether you have.
- **Coming up:** licenses that expire within 90 days, options to exercise within 60 days, and payments due within 30 days or overdue.
- **Prints a license schedule** with every license's terms, elements, payments and options. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/licenses-template.csv) with the same columns as the export.

This is not legal advice. Your licenses' own terms are what count. See [Not legal advice](../../README.md#not-legal-advice).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Licenses are `contracts` with `type` "license", and this tool adds optional `licenseKind`, `licensor`, `media`, `territory`, `term`, `fee`, `payments` (each an `id`, `amount`, `due`, `paid`, `paidDate` and `note`) and `options` (each an `id`, `what`, `fee`, `deadline`, `exercised` and `exercisedDate`). It uses the contract's `thirdPartyElementIds`, `signedDate`, `effectiveDate`, `expirationDate`, `requiredCredit` and `notes`, and adds the license's id to each element's `contractIds`.

The signed copy is an asset with `type` "license" and a `relativePath`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reminders outside the browser, such as a calendar file of deadlines
- Most-favored-nations terms across licenses
- Fees in other currencies

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
