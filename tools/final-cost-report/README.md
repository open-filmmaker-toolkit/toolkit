<p align="center">
  <b>The budget, closed out, in the layout your funder wants.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Final cost report

Close out the budget with final costs, for funders and your records. It starts from [budget-to-actuals](../budget-to-actuals/): the budget, the expense log, and anything you set still to pay.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#94](https://github.com/open-filmmaker-toolkit/toolkit/issues/94).

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

- **Budget against final cost** for every account, with the variance.
- **Layouts funders ask for:** by account, by line, a top sheet by section, or in a funder's own categories from the [budget converter](../budget-converter/).
- **Costs to a date,** and draft or final.
- **Variance notes** for any account or category. Variances over 10 percent without a note are listed.
- **Final cost** is spending in the [expense log](../expense-log/) plus anything set still to pay in budget-to-actuals. Lines with nothing set still to pay are closed at what was spent.
- **An accountant's sign-off page,** printed after the report when you turn it on: the totals, what the accountant is signing in wording you can change, and lines for the accountant and producer to sign and date.
- **Prints** in the layout you pick and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/final-cost-report-template.csv) with the same columns as the export.

- **Other currencies.** Budget lines and expenses in other currencies convert at the project's exchange rates, with each expense at the rate for its date, and the report says which rates it used. Lines with several fringes or capped fringes count as they do in the budget.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `finalCostReport` record: `closeDate`, `status` ("final" when it is), `notes` by account, markup, section or funder category, and `signOff`: `include`, `name`, `firm`, `credential`, `statement` (only when you changed the wording) and `date`.

It reads `budget`, `expenses`, `costReport` and `budgetFormats`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Comparing two final cost reports

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
