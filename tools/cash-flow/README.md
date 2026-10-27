<p align="center">
  <b>When money goes out and comes in, and where the balance runs short.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Cash flow

Plan when the film's money goes out and comes in, month by month or week by week. Spread the budget across the schedule, add the payments expected in the finance plan, and see the running balance, with every period where it runs short.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#52](https://github.com/open-filmmaker-toolkit/toolkit/issues/52).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's schedule is made up.

## What it does

- **Spreads the budget across the schedule.** Pick the dates each account is paid over, and the cost is split evenly across those months or weeks. Open an account to schedule a single line differently. Contingency and other percentages are scheduled the same way.
- **Leaves out what isn't cash.** Mark a line or account as deferred (such as fees paid from revenue later) or in-kind, and it stays out of the cash going out.
- **Adds the money coming in** from the [finance plan](../finance-plan/): each payment in the period it's expected. Confirmed money always counts; pending money counts unless you turn it off, and prospective money only if you turn it on. In-kind support and deferrals never count as cash.
- **Shows the running balance** from the cash on hand at the start, period by period, with every period where it goes below zero marked short.
- **Sums it up:** money in and out, the balance at the end, the first period that's short and the lowest point.
- **Lists what's not on the schedule:** costs not scheduled yet, money with no payment date, and how much is deferred or in-kind.
- **Months or weeks,** between dates you choose or across everything that's scheduled.
- **Exports CSV and prints** the table. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

It reads the budget from the [budget tool](../budget/) and the money coming in from the finance plan, in the same project file, and changes neither. For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/cash-flow-template.csv) with the same columns.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `cashFlow` record with `period` (`month` or `week`), optional `openingBalance`, `start` and `end` (dates), `includePending` (false to leave pending money out) and `includeProspective` (true to count it), and the schedule: `accounts`, `lines` and `markups`, each mapping a budget account, line or percentage id to `{ "mode": "spread", "from": date, "to": date }`, `{ "mode": "deferred" }` or `{ "mode": "in-kind" }`. A line's own schedule wins over its account's. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Spreading a cost unevenly, such as a deposit and a final payment
- One-off costs and income that aren't in the budget or the finance plan
- Actual spending from the expense log against the plan

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
