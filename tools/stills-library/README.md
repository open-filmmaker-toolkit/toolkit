<p align="center">
  <b>Every still captioned, credited and cleared.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Stills library

Organize production stills and key art. Give each still a caption and photo credit, tag the people pictured, and record who approved it. The tool checks everyone pictured against your releases and prints a caption sheet.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#80](https://github.com/open-filmmaker-toolkit/toolkit/issues/80).

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

- **Add stills** from your computer. Each is resized and kept in the project file, with a note of where the full-resolution file is.
- **Caption, photo credit and date,** and whether it is a production still or key art.
- **People pictured, checked against releases.** Anyone without a signed appearance release in the [release tracker](../release-tracker/) is flagged on the still and listed in the release check.
- **Approvals:** waiting, approved or not approved, and who approved it. Filter by approval or release problems.
- **Prints a caption sheet** of approved and waiting stills, and **exports it as CSV.** Stills here are the same ones the [EPK and press notes builder](../press-notes/) uses.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/stills-caption-sheet-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Stills are `assets` with `type` "still" or "key art", the resized image in `data`, and `caption`, `photoCredit`, `date`, `relativePath`, `personIds` (people pictured), `approval` (`pending`, `approved` or `rejected`), `approvedBy` and `notes`.

It reads `people` and `contracts`. Removing a still also takes it out of the press notes. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Importing a folder of stills at full size
- Face tagging
- Model and property releases for stills alone

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
