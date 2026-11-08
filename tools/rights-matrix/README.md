<p align="center">
  <b>Who holds which rights, where, and until when.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Rights availability matrix

See which rights you hold and which you've sold. Add each distribution deal with its territories, media and term, and the grid shows every territory and medium as sold, on hold or available, on any date you pick.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#83](https://github.com/open-filmmaker-toolkit/toolkit/issues/83).

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

- **Distribution deals** with the distributor or buyer, territories (or Worldwide), media, term, advance or fee, exclusivity and notes on holdbacks. Status is negotiating (on hold), signed (sold) or fell through.
- **The grid:** territories down the side and media across the top: theatrical, educational, free and pay TV, subscription streaming, rental and purchase, free streaming with ads, airline, and DVD and Blu-ray. Pick a date to see rights as of then.
- **Overlaps:** exclusive deals that cover the same territory and media at the same time are flagged in the grid and listed.
- **Reverting soon:** signed deals that end in the next six months.
- **Prints the grid** in landscape and **exports CSV**, one row for each territory and media.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/rights-matrix-template.csv) with the same columns as the export.

This is not legal advice. Your agreements decide who holds which rights. See [Not legal advice](../../README.md#not-legal-advice).

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Distribution deals are `contracts` with `type` "distribution", `status` (`negotiating`, `signed` or `declined`), and `licensee`, `territories`, `mediaRights`, `effectiveDate`, `expirationDate`, `fee`, `exclusive` (false for a non-exclusive deal) and `notes`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Holdbacks and windows between media
- Language rights
- Sub-territories, such as French-speaking Canada

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
