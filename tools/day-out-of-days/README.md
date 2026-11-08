<p align="center">
  <b>Which days each cast member works, holds and travels.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Day-out-of-days

The day-out-of-days is the grid an assistant director or line producer makes for each actor's deal: one row per cast member, one column per shoot day, showing when each of them starts, works, holds, travels and finishes. This one is worked out from the stripboard, so it changes when the schedule does.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#169](https://github.com/open-filmmaker-toolkit/toolkit/issues/169).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. Its cast of four each work one of the two scheduled days. Everything in the sample is made up.

## What it does

- **A row for each character,** by cast number, with who plays the part, from the [script breakdown](../script-breakdown/).
- **A column for each shoot day with scenes** on the [stripboard](../stripboard/), numbered the same way, and for each travel day in the [shooting calendar](../shooting-calendar/) with an actor on it.
- **Codes for each day:** SW start work, W work, WF work finish, SWF start and finish on the same day, H hold, T travel, WD work and then drop, and PW pick up and work. Holds are the shoot days between someone's first and last day that they don't work.
- **Drop and pick up:** when the gap between two work days is longer than a number of days you choose (10 to start with), the person is dropped and picked up again instead of held. Set it to 0 to never drop. Union agreements have their own rules, so check yours.
- **Counts work, hold and travel days** for each person, for their deal memo, with totals in the side panel.
- **Prints** the grid landscape with what the codes mean. **Exports CSV** with the codes, counts and each person's start and finish dates. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets, cast or shoot days as separate CSV files.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared project file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `dayOutOfDays` record with `dropDays`, the gap that drops someone. Everything else comes from `scenes`, `characters` and `shootDays`, and is preserved as it is. See the [data model notes](../../schemas/README.md).

## Not yet

- Days off and weekends as columns, for counting paid days by the calendar
- Rehearsal, fitting and other work days that aren't shoot days
- Rows for extras and stand-ins

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
