<p align="center">
  <b>What you've spent, against what you planned.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Budget-to-actuals

Compare what you've spent against the budget, line by line. The tool reads the budget and the expense log, and shows what's spent, the estimate to complete, the estimated final cost and the variance for each line, account and the whole budget. Print it as a cost report.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#72](https://github.com/open-filmmaker-toolkit/toolkit/issues/72).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's budget and expenses are made up.

## What it does

- **Reads the [budget](../budget/) and the [expense log](../expense-log/).** Each line shows its budget, with fringes, and what's been spent on it.
- **Expenses on the right line.** The expense log records an expense's account. When an account has one line, its expenses count against that line. When it has several, assign each expense to its line; until then it's shown as not assigned, and comes out of the account's estimate to complete.
- **Estimate to complete.** It starts as whatever is left of the line's budget. Click a line to set your own estimate, such as when a line is done or you know more is coming, and add a note.
- **Variance** for each line, account and section and in total: the budget less the estimated final cost, which is what's spent plus the estimate to complete. Lines over budget are listed in the side panel.
- **Percentages,** such as contingency and insurance, are rows too, with estimates you can set.
- **Not in the budget:** expenses with no account, or an account the budget doesn't have, are listed and counted in the total.
- **Report as of a date,** to count only the expenses up to it.
- **Prints a cost report:** a summary by section, then every account and line. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/cost-report-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `costReport` record with optional `asOf` (the report date) and `estimates`, each with an `id`, a `lineId` (in `budget.lines`) or `markupId` (in `budget.markups`), and optional `toComplete` and `note`.

Assigning an expense to a line adds `budgetLineId` to it in `expenses`. It reads `budget` and `expenses`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Committed costs, such as signed deal memos and purchase orders, separate from what's spent
- Cost reports by period, and comparing two reports
- Spending in other currencies

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
