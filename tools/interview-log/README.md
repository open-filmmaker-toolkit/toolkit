<p align="center">
  <b>Every interview, and the moments worth finding again.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Interview log

Log each interview: who, when, where, which cards it's on, and the moments you'll want to find later, with timecodes and favorites marked. See whether the person has signed a release, link the transcript, and export the moments for the paper edit.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#63](https://github.com/open-filmmaker-toolkit/toolkit/issues/63).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's interviews, moments and transcript path are made up.

## What it does

- **One record from plan to log.** The log uses the same interviews as [interview prep](../interview-prep/), so an interview you planned there is the one you log here, with its story beats.
- **Who, when and where:** the person from the project, or someone not in it yet, the shoot day from the [shooting calendar](../shooting-calendar/), the date and the location.
- **Which cards:** tick the [camera and sound reports](../camera-sound-reports/) for that day, or type other cards and files.
- **Timestamped moments:** timecode, what they say or do, a favorite mark, and the story beat it belongs to. Moments print and export in timecode order.
- **The release.** Each interview shows whether the person has a signed appearance release, a pending one, an expired one or none, as the [release tracker](../release-tracker/) records it.
- **The transcript:** where it is, relative to your project file, or a link, recorded in the project's files.
- **Flags** interviews that are done with no moments logged, and lists them in the side panel.
- **Prints the moments** for the paper edit, for one interview or all, or favorites only. **Exports CSV for the paper edit,** one row for each moment. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/interview-moments-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

It adds to `interviews`, the same list interview prep keeps: optional `locationId` (when it differs from the shoot day's), `mediaReportIds` (in `mediaReports`), `cards`, `transcriptAssetId` (an asset with `type` "transcript" and a `relativePath`), `moments` (each with an `id` and optional `tc`, `text`, `fav` and `beatId`) and `logNotes`. Logging moments marks a planned interview done.

It reads `people`, `locations`, `contracts`, `shootDays` and `mediaReports`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Importing a transcript and its timecodes
- Selects and string-outs across interviews
- Linking moments to clips in the camera reports

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
