<p align="center">
  <b>How the film gets paid for, against the budget, and when the money arrives.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Finance plan

List every source of money for the film: grants, investors, presales and licenses, in-kind support, deferred fees, loans and donations. See how much is confirmed, pending and prospective against the budget, the gap still to raise, and when the money should arrive. Print it for funders and investors.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#49](https://github.com/open-filmmaker-toolkit/toolkit/issues/49).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's investors, broadcaster and donors are made up.

## What it does

- **Logs each source** with its kind, amount, status (confirmed, pending or prospective), terms such as recoupment or rights, payment dates, and notes.
- **Links grants from the [grant calendar](../grant-calendar/).** A linked grant follows the calendar: awarded is confirmed at the amount awarded, submitted is pending, and researching or drafting is prospective, at the amount you asked for. Declined grants drop out of the totals. Unlink a grant to set its amount and status yourself.
- **Shows totals against the budget,** from the [budget tool](../budget/) if the project has one, or a total you type in. Confirmed, pending and prospective money, what's still to confirm, and the gap with nothing lined up.
- **Separates money from in-kind support and deferrals,** which cover costs without cash.
- **Shows when money arrives:** confirmed and pending payments by month, with the running total, and the sources with no date yet.
- **Prints a finance plan** for funders and investors: the totals, sources by kind with their terms, and when money arrives. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/finance-plan-template.csv) with the same columns.

A finance plan isn't an offering to investors. Talk to a lawyer before you raise equity.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `financePlan` record with `sources`, and an optional `budgetTotal` used when the project has no budget. Each source has an `id`, a `kind` (`grant`, `equity`, `presale`, `in-kind`, `deferral`, `loan`, `donation` or `other`) and a `status` (`confirmed`, `pending` or `prospective`), and optional `name`, `amount`, `terms`, `payments` (each with `date` and `amount`), `notes`, and `grantId`, pointing to a grant in `grants`. A linked source takes its amount and status from the grant. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Linking investors and broadcasters to their organization in the funder CRM
- Recoupment waterfalls for investors
- Several currencies in one plan

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
