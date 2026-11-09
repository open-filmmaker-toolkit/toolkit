<p align="center">
  <b>Scenes, cast, sets and everything each scene needs, read from your script.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Script breakdown

Import your screenplay and get a list of its scenes, each with its heading, length in eighths of a page and the characters who speak in it. Then tag the extras, props, wardrobe, vehicles, effects and everything else each scene needs, link each set to a real location, and say who plays each part. The schedule, call sheets and sides all start from here.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#167](https://github.com/open-filmmaker-toolkit/toolkit/issues/167).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. Its five reenactment scenes come from [`samples/the-river-keeps-reenactments.fountain`](../../samples/the-river-keeps-reenactments.fountain), which you can import into a new project too. The script and everything in the sample is made up.

## What it does

- **Imports a script in Fountain,** the open plain-text screenplay format. Final Draft, Fade In, Highland, WriterSolo, Slugline, Trelby and most other screenwriting apps can export it. Each scene heading (a line starting with INT. or EXT.) starts a scene, and scene numbers written as `#12A#` are kept.
- **Finds who speaks in each scene** and numbers the cast by how many scenes each character is in, the usual order for cast numbers. Add characters who don't speak from the scene.
- **Works out each scene's length in eighths of a page,** laid out about 55 lines to a page the way a screenplay prints. It's close to what screenwriting apps show, not exact. Change any length by hand.
- **Tags elements** in twelve kinds: extras, props, wardrobe, makeup and hair, set dressing, vehicles, animals, special effects, stunts, sound and music, special equipment and other.
- **Links sets to locations.** A set that starts with a location's name, such as HAMMOND HOUSE - KITCHEN for the Hammond house, is linked when you import. Link the rest from the Sets list, or make a new location named after the set.
- **Says who plays each part.** Pick someone from the project's people, or type a new name to add them with the role Cast, so the call sheet, deal memos and credits can use them.
- **Imports a newer draft without losing your work.** Scenes are matched by scene number, then by heading. Their headings and lengths update, and what you tagged stays. New scenes are added, and scenes that were cut are flagged so you can remove them.
- **No script?** Add scenes by hand, for a documentary's reenactments or a shoot planned without a screenplay.
- **Prints breakdown sheets:** a summary of every scene, then a sheet for each scene with its cast and a box for each kind of element. **Exports CSV,** one row per scene. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets, scenes or cast as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/script-breakdown-template.csv) with the same columns.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/script-breakdown-template.csv) imports as it is; match any other columns once and the tool remembers. Problems show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared project file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `script` record with the screenplay's `text` in Fountain, and optional `title`, `fileName`, `importedAt` and `pages`.

A `scenes` list. Each scene has an `id`, and optional `number`, `heading`, `intExt` (`INT`, `EXT`, `INT/EXT` or `EST`), `set`, `time`, `eighths` (its length in eighths of a page), `page`, `order`, `synopsis`, `characterIds`, `elements` (each with `id`, `category` and `name`), `locationId`, `notInScript` and `notes`.

A `characters` list. Each character has an `id`, and optional `name`, `number` (the cast number) and `personId` (who plays the part). Casting someone new adds them to `people`, and a new location for a set is added to `locations`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reading Final Draft (`.fdx`) or PDF scripts; export Fountain from your screenwriting app instead
- Tagging elements by selecting words in the script text
- Revision colors and locked scene numbers

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
