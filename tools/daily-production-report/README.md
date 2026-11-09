<p align="center">
  <b>What happened on set today, in one page.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Daily production report

Record what happened on each shoot day: call, meal and wrap times and hours for crew and talent, what was shot and on which cards, and incidents, delays and notes. A new report starts from that day's call sheet. Print it, and export crew hours as CSV.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#64](https://github.com/open-filmmaker-toolkit/toolkit/issues/64).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's report is made up.

## What it does

- **One report for each shoot day,** from the [shooting calendar](../shooting-calendar/). The side panel lists shoot days up to today that have no report yet.
- **Starts from the call sheet.** If the day has a [call sheet](../call-sheet/), by link or by date, a new report starts with its general call and wrap, the lunch from a schedule item that says "lunch" (it ends when the next item starts), and the crew with their roles and call times. Change anything. A day with no call sheet starts blank.
- **Call, meal and wrap times,** for the day and for each person. Times are 24-hour, like 07:30.
- **Hours for crew and talent:** wrap minus call, less the meal break, worked out each time and never stored. A wrap earlier than the call counts as the next day. Total hours and total minutes lost show on each report. People are picked from the project's people, or typed in if they aren't there.
- **What was shot, and on which cards:** a note, and ticks for that day's camera and sound reports from [camera and sound reports](../camera-sound-reports/).
- **Scenes and takes:** the day's scenes from the [stripboard](../stripboard/), to tick off as they're finished, with the pages shot. Setups, takes and circled takes are counted from the scene and take numbers in the camera reports. The printed report adds a script supervisor's page listing every take with its notes.
- **The weather** comes from the call sheet, and prints with the day's facts.
- **Incidents and delays:** delay, injury, equipment, weather or other, with the time, minutes lost and what happened, and notes for the day.
- **Prints** one page for the chosen day, with signature lines for whoever prepared and approved it. Their names carry over from the last report. **Exports crew hours as CSV,** one row for each person each day. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

`dailyReports`: each has an `id`, `shootDayId` and optional `callSheetId`, `callTime`, `lunchStart`, `lunchEnd`, `wrapTime`, `crew`, `shot`, `weather`, `mediaReportIds`, `completedSceneIds` (the scenes finished that day, in `scenes`), `incidents`, `notes`, `preparedBy` and `approvedBy` (names for the signature lines).

- Each `crew` entry has an `id` and optional `personId`, `name`, `role`, `call`, `wrap`, `mealMinutes` and `note`. Hours aren't stored.
- Each `incidents` entry has an `id` and optional `kind` (`delay`, `injury`, `equipment`, `weather` or `other`), `time`, `minutesLost` and `text`.
- `mediaReportIds` are the camera and sound reports shot that day.

It reads `people`, `locations`, `shootDays`, `callSheets` and `mediaReports`. Everything else in the file is preserved, including fields on a report that this tool doesn't edit. See the [data model notes](../../schemas/README.md).

## Not yet

- Overtime and meal penalty rules
- Footage totals

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
