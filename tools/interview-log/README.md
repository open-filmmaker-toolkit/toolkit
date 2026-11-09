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
- **String-outs across interviews.** Pick selects from any interview, favorites or all, by story beat, or by searching what they say, and put them in the order you want them: everyone on the night the levee broke, say. Print a string-out for the edit, or export it as CSV with the clip and timecode for each.
- **Flags** interviews that are done with no moments logged, and lists them in the side panel.
- **Prints the moments** for the paper edit, for one interview or all, or favorites only. **Exports CSV for the paper edit,** one row for each moment. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/interview-moments-template.csv) with the same columns as the export.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/interview-moments-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Imports a transcript with timecodes:** an SRT, WebVTT, Word, HTML or timecoded text file from a transcription app such as Buzz or noScribe, keeping the timecodes and speakers. Mark the moments worth finding again straight from it. The transcript is kept with the paper edit's, so the paper edit uses it without importing it twice.
- **Links each moment to its clip** on the interview's cards, from the [camera reports](../camera-sound-reports/). The [paper edit](../paper-edit/) brings favorite moments in as bites, with their clips.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

It adds to `interviews`, the same list interview prep keeps: optional `locationId` (when it differs from the shoot day's), `mediaReportIds` (in `mediaReports`), `cards`, `transcriptAssetId` (an asset with `type` "transcript" and a `relativePath`), `moments` (each with an `id` and optional `tc`, `text`, `fav`, `beatId` and `clipId`, a clip in `mediaReports`) and `logNotes`. Logging moments marks a planned interview done. A `stringOuts` list keeps string-outs, each with an `id`, optional `title` and `notes`, and `items` in order, each an `interviewId` and `momentId`.

It reads `people`, `locations`, `contracts`, `shootDays` and `mediaReports`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Sending a string-out to an editing app as a timeline. The paper edit exports an edit list

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
