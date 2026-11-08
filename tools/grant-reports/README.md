<p align="center">
  <b>Every grant's final report, in on time.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Grant final reports

Write the final report for each awarded grant before it's due: what you did, what changed, the deliverables you promised, the final costs and the impact. Print it, or save it as a PDF.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#95](https://github.com/open-filmmaker-toolkit/toolkit/issues/95).

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

- **One report for each grant** marked awarded in the [grant calendar](../grant-calendar/), with its due date and status. Reports coming due or overdue are listed.
- **The narrative,** with answers from the [grant narrative library](../narrative-library/) to insert and a word count, plus **outcomes** and the **deliverables** you promised.
- **Final costs** from the [final cost report](../final-cost-report/), in the funder's categories when the [budget converter](../budget-converter/) has a format for the grant, with your variance notes.
- **The impact report's** summary, screenings, audience, results and quotes, from the [impact report](../impact-report/).
- **Prints** the report for the grant you pick.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `grantReports` collection: `grantId`, `dueDate`, `status` (`drafting` or `submitted`), `submittedDate`, `narrative`, `outcomes`, `deliverables`, `budgetFormatId` and `includeImpact`.

It reads `grants`, `narratives`, `budget`, `expenses`, `costReport`, `finalCostReport`, `budgetFormats`, `impactReport`, `theoryOfChange`, `screenings` and `bookings`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Interim reports
- Each funder's own report form
- Recording who used which narrative version in the narrative library

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
