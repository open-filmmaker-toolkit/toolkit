<p align="center">
  <b>Every signed agreement, filed and findable.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Contract and release archive

Gather every signed contract and release into one indexed archive for the long term. Each agreement in the project gets a folder, a tab number and its signed copy, and anything signed without a copy is flagged.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#97](https://github.com/open-filmmaker-toolkit/toolkit/issues/97).

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

- **Every agreement in the project:** releases from the [release tracker](../release-tracker/), licenses, deal memos, certificates and permits, distribution deals and anything else, in folders by kind.
- **A tab number and a suggested file name** for each, by folder and date.
- **Signed copies:** link a file already in the project or say where it is. Agreements signed without a copy are flagged; filter by missing copies or not signed yet.
- **Where the archive is kept** and when you last checked it, with a note for each agreement.
- **Exports the index as CSV** and **a suggested folder layout as a text file,** and **prints the index.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/contract-archive-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `contractArchive` record: `location`, `checkedDate` and `notes` by contract id. A signed copy you name is an asset with `type` "release scan" or "signed contract" and a `relativePath`, added to the contract's `assetIds`.

It reads `contracts`, `assets`, `people` and `locations`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Copying the files into the folders (the toolkit never touches files on your computer)
- Retention dates for each kind of agreement
- Checking a file is still where you said

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
