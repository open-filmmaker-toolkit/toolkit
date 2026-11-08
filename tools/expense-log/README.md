<p align="center">
  <b>Log every receipt against a budget account while the details are still fresh.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Expense log

Record production expenses, per diems and petty cash as you go, linked to budget accounts, then print a report or export a CSV for your accountant.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#65](https://github.com/open-filmmaker-toolkit/toolkit/issues/65).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, accounts or network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. Its expenses, people, shoot days and budget accounts are fictional.

## What it does

- **Logs expenses** with a date, amount, description, payee, budget account, type and payment method. Optionally link an expense to a shoot day.
- **Records per diems** for a person and remembers the most recently used per diem amount for the next one. Petty cash is a separate expense type.
- **Keeps receipt references, not receipt files.** Choose an image or PDF to record its file name, type and a suggested path under `receipts/`. The file is never read, stored or sent by the tool. Keep the actual receipt in a `receipts` folder next to the project file.
- **Shows totals** by budget account and expense type, with a grand total. Filter by account or type and search the entries; totals update to match the current view.
- **Exports an accountant-ready CSV** with one row per visible entry and columns for date, amount, kind, budget account, payment method, payee, description, person, shoot day, receipt and notes. Also prints an expense report and can export other project collections as CSV.

This tool contains financial records. Keep the project file and any receipt files somewhere private; don't attach them to an issue.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

An `expenses` list. Each expense has an `id` and can include `date`, `amount`, `description`, `payee`, `accountId` (a budget account ID), `kind` (`expense`, `perdiem` or `pettycash`), `method` (`card`, `cash`, `check`, `transfer` or `other`), `personId` (for a per diem), `shootDayId`, `receiptAssetId` and `notes`. A selected receipt adds an `assets` entry with `type: "receipt"`, its name, MIME type and suggested relative path; the file itself is not part of the project. [Budget-to-actuals](../budget-to-actuals/) can add `budgetLineId` to an expense, for the budget line it counts against. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reading, embedding or copying receipt files; put them in the project folder yourself.
- Importing expenses from a bank or card statement.

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
