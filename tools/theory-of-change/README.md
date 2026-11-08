<p align="center">
  <b>How the campaign leads to change, on one page.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Theory of change builder

Map how the film's impact campaign leads to change: who it reaches, what it does, what changes in the short, medium and long term, and how you'll know. Print it as a one-page diagram, and record results against it in the impact report.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#89](https://github.com/open-filmmaker-toolkit/toolkit/issues/89).

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

- **The goal:** the change the campaign works toward.
- **Audiences, activities and outcomes,** in columns from who you reach to what changes, with outcomes in the short, medium and long term. Activities point to the outcomes they lead to.
- **Indicators** for each outcome, with a target, unit, starting point and how you'll measure it. The [impact report](../impact-report/) records results against them.
- **Gaps:** outcomes with no indicator or no activity leading to them, and audiences no activity reaches.
- **Prints a one-page diagram** in landscape and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/theory-of-change-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `theoryOfChange` record with `goal`, `audiences` (`name`), `activities` (`text`, `audienceIds`, `outcomeIds`), `outcomes` (`text`, `term` of `short`, `medium` or `long`, `audienceIds`) and `indicators` (`text`, `outcomeId`, `target`, `unit`, `baseline`, `source`). Each can have `notes`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Drawing arrows between boxes
- Assumptions and risks for each step
- Versions to compare as the plan changes

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
