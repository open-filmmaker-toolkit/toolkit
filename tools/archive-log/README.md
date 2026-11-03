<p align="center">
  <b>Know where each project asset is stored, keep its hash manifest, and record when you last checked it could be read back.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Archive log

Record each copy of a project asset, where it is stored, when it was copied, and when its next read-back check is due. Keep a hash manifest with each copy and log the results of checks you perform.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#96](https://github.com/open-filmmaker-toolkit/toolkit/issues/96).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, accounts or network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample project and its assets are fictional.

## What it does

- **Logs multiple copies of a project asset.** Select an existing asset or create one as you record its first copy. Add a copy label, storage location and copy date.
- **Keeps a hash manifest with a copy.** Paste manifest text or enter a reference to a manifest produced by another tool. The Archive log does not read media or calculate hashes.
- **Tracks read-back checks.** Record the check date, whether it passed, was partial or failed, and any notes. Set a next-check date; overdue and upcoming checks appear when the tool is open. The tool does not send reminders while closed.
- **Searches and filters** by asset details, storage location, manifest text, check status and asset type.
- **Exports CSV.** Each archive row includes its complete hash manifest and read-back history. Project asset CSV export also includes `archiveCopies` as JSON.
- **Prints an archive report** with copy locations, dates and current check status.
- **Preserves the rest of the project file**, including asset fields this tool doesn't edit.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your work as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

An optional `archiveCopies` array on each `assets` record. A copy has an `id`, `storageLocation` and `copiedAt`, and may include a `copyLabel`, `hashList`, `nextCheckDate` and `checks`. Each check has an `id`, `checkedAt`, `result` (`passed`, `partial` or `failed`) and optional `notes`. Hash manifests are text or references supplied by the user; they are not generated or validated by this tool.

All other project data is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Notifications or automatic reminders while the tool is closed
- Verifying that media can be read back or comparing its hashes; record those results after checking with another tool
- Importing hash manifests from external files
- Comparing copies to identify which assets have no off-site copy

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
