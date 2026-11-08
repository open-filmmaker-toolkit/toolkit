<p align="center">
  <b>What the campaign did, and what changed.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Impact report

Report on the film's impact campaign for a period: the results against your theory of change, how many screenings and people, which partners, and the stories and quotes that go with the numbers. Print it, or save it as a PDF for funders and partners.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#93](https://github.com/open-filmmaker-toolkit/toolkit/issues/93).

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

- **Results against the [theory of change](../theory-of-change/):** enter the result for each indicator and see progress to its target.
- **Screenings and audiences:** screenings in the period from the [press list](../press-list/) and [partner CRM](../partner-crm/), and community and educational [bookings](../bookings/). Enter the attendance for each.
- **Partners** active in the period, from the partner CRM.
- **Stories and quotes,** with who said it, where, the outcome it shows, and whether they agreed to be quoted. Only quotes with permission are printed.
- **A summary** and **totals:** screenings, audience, partners and targets met.
- **Prints the report** and **exports the results as CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/impact-results-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

An `impactReport` record: `periodStart`, `periodEnd`, `summary`, `results` (by indicator id: `value` and `note`) and `stories` (`quote`, `who`, `date`, `context`, `outcomeId` and `permission`). Attendance is saved as `attendance` on `screenings` and `bookings`.

It reads `theoryOfChange`, `screenings`, `bookings` and `partners`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reports for more than one period side by side
- Charts
- Survey results (the toolkit never collects data from the public)

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
