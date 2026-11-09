<p align="center">
  <b>The film's shape, on cards you can move.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Structure board

Lay out the film's structure on cards: a card for each scene with a summary and running time, arranged into sequences and acts and colored by story thread or character. Move them around until the structure works, then print the board.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#69](https://github.com/open-filmmaker-toolkit/toolkit/issues/69).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's acts, threads and cards are made up.

## What it does

- **A card for each scene,** with a summary, running time and notes. Link a card to a scene in the [paper edit](../paper-edit/) and it takes that scene's running time; or start with a card for each paper edit scene.
- **Acts and sequences.** Add acts as columns and sequences inside them, name them, and reorder them. Each shows its running time, and the board shows the film's.
- **Move cards** by dragging them within a sequence, into another sequence or act, or back to "Not on the board yet". On a phone or with a keyboard, use the arrows on each card, or pick the act and sequence when you open it.
- **Color by story thread or character.** Name threads, give each a color and link a thread to a person to follow a character. A card shows the color of every thread it's in, and you can highlight one thread to see where it runs.
- **Prints the board** by act and sequence, with each card's colors, summary, threads and running time. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.
- **Prints index cards** to cut out and pin up: one 5 × 3 inch card for each scene, three to a page with cut lines, numbered in board order, with its act and sequence, summary, running time and threads.

The [cut version tracker](../cut-tracker/) ties screening notes to these cards.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/structure-board-template.csv) with the same columns as the export.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/structure-board-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Links cards to clips** in the [footage log](../footage-log/).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `structure` record with `acts` (each an `id` and `title`, in order), `sequences` (each an `id`, `actId` and `title`, in order), `threads` (each an `id`, `name`, `color` and optional `personId`) and `cards`, in order.

Each card has an `id`, a `title`, and optional `summary`, `seconds` (running time), `timeFromPaperEdit`, `sequenceId` or `actId` (where it sits; neither means it's not on the board yet), `threadIds`, `paperEditSceneId` and `notes`.

It reads `people` and `paperEdit`. Cards can have `assetIds`, clips in `assets`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Several versions of the structure to compare

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
