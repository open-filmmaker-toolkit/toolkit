<p align="center">
  <b>The shots for each scene, with a frame for each to print as a storyboard.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Shot list and storyboard

List the shots you plan for each scene, with size, angle, movement and lens, and add a frame to each: a sketch, a photo from the scout or a reference still. Print it as a shot list for the camera department or as storyboard pages, and tick shots off as you get them.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#171](https://github.com/open-filmmaker-toolkit/toolkit/issues/171).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. It has shots for two reenactment scenes and some river b-roll, and two shots linked to the sources behind them. Everything in the sample is made up.

## What it does

- **Groups shots by scene,** in script order, using the scenes from the [script breakdown](../script-breakdown/). Without a script, as for most documentary shoots, give shots a group instead, such as "River b-roll".
- **Numbers shots for you:** 3A, 3B and so on within scene 3, or 1, 2, 3 within a group. Change any number.
- **Size, angle, movement and lens** for each shot, chosen from the usual terms, with what we see and notes.
- **Links each shot to its sources** in the [research and archival log](../research-log/): the archival clip a shot uses, or the document behind what it shows. This is how a documentary keeps each claim on screen tied to where it came from. The list and the printed shot list show a shot's sources, and the research log shows which shots use each source.
- **A frame for each shot.** Add a picture and it's made smaller (at most 640 pixels wide) and kept in the project file, so it travels with the project.
- **Two views:** a list and a storyboard grid. Filter by scene and hide the shots already done. The side panel shows how many are done, overall and for each scene.
- **Prints as a shot list,** a table for each scene with small frames, or **as a storyboard,** three frames across with what we see under each. **Exports CSV** with every column but the frames. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets, scenes or shots as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/shot-list-template.csv) with the same columns.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/shot-list-template.csv) imports as it is, with each shot put under the scene with that number or in a group of that name. Problems show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared project file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `shots` list. Each shot has an `id`, and optional `sceneId` (in `scenes`) or `group`, `number`, `size`, `angle`, `movement`, `lens`, `description`, `notes`, `sourceIds` (sources in `sources`, from the research log), `frame` (the picture, as a data URL) and `done`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Drawing frames in the tool
- Sources in the CSV export and import
- Shot lists for each shoot day, from the stripboard
- Overhead diagrams of camera and actor positions

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
