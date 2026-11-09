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
- **Add a folder of stills.** Pick a folder and every image in it is added, with its path inside the folder kept as the full-size file and its size noted. Keep the folder next to your project file so the paths stay right. Stills already in the library are skipped, so you can pick the same folder again after a shoot day.
- **Caption, photo credit and date,** and whether it is a production still or key art.
- **People pictured, checked against releases.** Anyone without a signed appearance release in the [release tracker](../release-tracker/) is flagged on the still and listed in the release check.
- **Releases for a still alone.** Add a model release for a person, or a property release for a building, artwork or the like, that covers one photo and not the film. A signed model release clears that person in that still; a property release waiting for a signature is flagged.
- **Approvals:** waiting, approved or not approved, and who approved it. Filter by approval or release problems.
- **Prints a caption sheet** of approved and waiting stills, and **exports it as CSV.** Stills here are the same ones the [EPK and press notes builder](../press-notes/) uses.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/stills-caption-sheet-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Stills are `assets` with `type` "still" or "key art", the resized image in `data`, and `caption`, `photoCredit`, `date`, `relativePath`, `personIds` (people pictured), `approval` (`pending`, `approved` or `rejected`), `approvedBy` and `notes`. Stills added from a folder also have `fullWidth` and `fullHeight`, the size of the full-size file.

A release for a still alone is a `contracts` entry with `type` "model release" (with `personIds`) or "property release", a `title`, a `status` (`pending` or `signed`), an optional `signedDate` and `stillIds`, the stills it covers. Other tools don't count these as releases for the film.

It reads `people` and `contracts`. Removing a still also takes it out of the press notes. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Face tagging

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
