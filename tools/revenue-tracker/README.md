<p align="center">
  <b>Every statement logged, every payment followed up.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Revenue tracker

Log revenue from each statement your distributors, sales agents and platforms send, and see totals by territory, media and period. The recoupment waterfall model can run the actual revenue.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#87](https://github.com/open-filmmaker-toolkit/toolkit/issues/87).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's data is made up.

## What it does

- **Statements** with the distribution deal (from the [rights availability matrix](../rights-matrix/)) or whoever sent it, the period, statement date, territory and media, gross receipts, their fees and expenses, what's due to you, when it was paid and a reference.
- **Due to you** is worked out from gross less fees and expenses unless you enter it, and a statement that doesn't add up is flagged.
- **Totals:** gross, fees, expenses, due, paid and still to come. **Gross by** source, territory, media, year or quarter.
- **Checks statements against the deal.** Each statement is checked against its deal's dates, territories and media. Set a deal's fee percentage, expense cap and when statements and payments are due, and it also flags a fee higher than the deal allows, with how much too much, expenses over the cap across all the deal's statements, and statements or payments that came late. Problems show on the statement and in a side list.
- **Not paid yet:** statements with money still owed.
- **Feeds the [recoupment waterfall model](../waterfall/),** which can run actual revenue to date through the tiers.
- **Prints** the statements with totals by territory, media and year, and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/revenue-template.csv) with the same columns as the export.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/revenue-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `revenueStatements` collection: `contractId` (a distribution deal) or `source`, `periodStart`, `periodEnd`, `statementDate`, `territory`, `media`, `gross`, `fees`, `expenses`, `net` (due to you, when it differs from gross less fees and expenses), `paidDate`, `reference` and `notes`. Deal terms for the checks are kept on the deal, as `revenueTerms` on the contract: `feePercent`, `expenseCap`, `reportingDays` and `paymentDays`.

It reads distribution deals in `contracts`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Currencies other than the project currency

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
