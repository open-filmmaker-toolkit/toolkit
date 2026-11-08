<p align="center">
  <b>The binder a distributor asks for, with the gaps showing.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Chain-of-title binder

Gather the chain-of-title documents a distributor asks for, in the order they usually go in the binder: underlying rights, agreements, copyright and title, releases and licenses. Link each to its document in the project, see what's missing, and print an index with a cover sheet for each tab.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#76](https://github.com/open-filmmaker-toolkit/toolkit/issues/76).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's documents and notes are made up.

## What it does

- **The usual checklist, in order:** option or purchase agreements for underlying material, life rights, director, producer, writer and composer agreements, crew deal memos, financing agreements, copyright registrations for the script and the film, the title report and opinion, the errors and omissions insurance certificate, a fair use opinion letter and the music cue sheet.
- **Releases and licenses from the project.** Every release in the [release tracker](../release-tracker/) and license in the [license tracker](../license-tracker/) has its own item, with its status. People marked on camera with no release, and clearance log elements still waiting on a license, are listed as missing.
- **Worked out from the project where it can be:** crew deal memos are in hand when every [deal memo](../deal-memos/) is signed, and the fair use letter isn't needed when nothing is marked fair use.
- **Link each item to its document:** pick agreements and files already in the project, or say where the file is. Mark an item in hand, missing or not needed for this film, with a note.
- **Add your own items** to any section, such as a distribution agreement.
- **Prints an index** with a tab number for each document and its status, **then a cover sheet for each tab** with the agreement's parties and dates and where the file is. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/chain-of-title-template.csv) with the same columns as the export.

This is not legal advice. Your distributor's delivery schedule and your attorney decide what the binder needs. See [Not legal advice](../../README.md#not-legal-advice).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `chainOfTitle` record with `items`, kept only for what you've changed: each has an `id` and `key` (a built-in item such as `cr-film`, or `contract:`, `person:` or `element:` and an id), and optional `status` (`have`, `missing` or `na`), `contractIds`, `assetIds` and `note`. Your own items add `custom`, `title` and `section`. A file you name is an asset with `type` "chain of title document".

It reads `people`, `contracts`, `thirdPartyElements` and `assets`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Delivery schedules from specific distributors
- Merging the documents into one PDF
- Checking that agreements contain work-for-hire or assignment language

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
