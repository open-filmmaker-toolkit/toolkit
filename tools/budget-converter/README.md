<p align="center">
  <b>One budget, in the categories each funder asks for.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Budget converter

Funders each ask for the budget in their own categories. Map your budget's accounts to a funder's categories once, and the tool adds up the converted budget, flags anything that doesn't map, and shows where the total differs from your budget. The mapping is saved for next time.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#48](https://github.com/open-filmmaker-toolkit/toolkit/issues/48).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's funder format is made up.

## What it does

- **Reads the budget** from the [budget tool](../budget/), in the same project file.
- **Maps accounts to a funder's categories.** Choose a category for each account, or open it to send a single line somewhere else. Fringes go with their lines or to a category of their own, and each percentage, such as contingency, goes to a category or is left out.
- **Starts from a common format:** top sheet sections, phases of production, or the cost categories on US federal form SF-424A. Each fills in the categories and maps what it can; check the rest against the funder's own form.
- **Flags lines that don't map,** and shows the converted total next to the budget total, with what's not mapped yet and what you left out on purpose.
- **Saves each mapping** in the project file, and links it to an application in the [grant calendar](../grant-calendar/) if you want.
- **Saves a format file** you can open in another project. It maps by account number and name, so it works with any budget that uses the same accounts.
- **Prints** the converted budget, with each category's lines, and **exports it as CSV**. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

Funders' forms change. The common formats are starting points, not the funder's official form.

### Contributing a format

If you've mapped a funder's budget form that others apply to, share it: save it as a format file and attach it from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose) with **Submit a template**, saying which funder and year it's from. Formats that are widely useful get added to the list the tool starts from.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `budgetFormats` list. Each format has an `id`, a `name`, `categories` (each with `id` and `name`), and mappings: `accountMap` and `lineMap` (account or line id to category id), `markupMap` (percentage id to category id), and optional `fringeTo` (`line`, or a category id). An empty string means left out on purpose; anything missing isn't mapped yet. Optional `grantId` points to a grant in `grants`, and `notes` say what the funder allows. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Funder forms with their own line items rather than categories
- Splitting one line across two categories
- More common formats, as they're contributed

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
