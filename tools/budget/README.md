<p align="center">
  <b>A documentary or indie budget with detail lines that roll up to a top sheet.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Budget

Build the film's budget account by account. Each line is a quantity, a unit and a rate, with fringes on payroll lines and contingency, insurance and fees as percentages on top. Totals roll up to the top sheet as you type, and saved versions show what changed since you sent the budget anywhere.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#51](https://github.com/open-filmmaker-toolkit/toolkit/issues/51).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's budget is made up.

## What it does

- **Detail lines by account.** Each line has a description, quantity, unit, an optional multiplier (such as two people) and a rate. Its total is quantity × multiplier × rate.
- **Accounts in four sections:** above the line, production, post-production and other costs, each with an account number.
- **Starts from the usual documentary accounts,** from development and research to festivals and outreach, if you'd rather not set them up yourself.
- **Fringes.** Add payroll taxes, benefits or union contributions as percentages, and pick one on each payroll line. The line shows its fringe, and the top sheet shows each fringe's total.
- **Percentages on the whole budget,** such as contingency, insurance, fees or overhead, worked out on all lines plus fringes.
- **The top sheet** updates as you type: each section and account, the subtotal, each percentage and the total, in the project's currency.
- **Versions to compare.** Save a version before you send the budget to a funder. Compare shows each account then and now, with what went up or down.
- **Prints** the top sheet, then the detail by account. **Exports CSV** of every line with its fringe and total, followed by the percentages and the total. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/budget-template.csv) with the same columns. The [budget converter](../budget-converter/) turns this budget into a funder's categories, and the [finance plan](../finance-plan/) measures what you've raised against its total.

The rates in the documentary accounts start at zero for fringes and insurance: set your own. Check what your funders, insurer and payroll company need.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `budget` record with `accounts` (each with `id`, `code`, `name`, `section` and optional `notes`), `lines` (each with `id`, `accountId`, and optional `description`, `quantity`, `unit`, `multiplier`, `rate` and `fringeId`), `fringes` and `markups` (each with `id`, `name` and `percent`), and `versions` (each with `id`, `label`, `at`, and copies of `accounts`, `lines`, `fringes` and `markups` as they were). `section` is `atl`, `production`, `post` or `other`. Amounts are in the project's `currency`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Globals, such as a shoot length every line can refer to
- Several fringes on one line, or fringes with a cap
- Importing a budget from another budgeting program or a spreadsheet
- Actual costs against the budget (planned as the budget-to-actuals tool)

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
