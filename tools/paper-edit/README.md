<p align="center">
  <b>Transcripts in, an edit list out.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Paper edit

Build a paper edit from your transcripts. Import them with their timecodes, pick the bites you want, arrange them into scenes, print the paper edit, and export an edit list that Premiere, Resolve or Avid can open, with each bite's source timecodes kept all the way through.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#68](https://github.com/open-filmmaker-toolkit/toolkit/issues/68).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's transcript and scenes are made up.

## What it does

- **Imports transcripts** as SRT or VTT files, or as text with a timestamp such as `[00:01:23]` at the start of each paragraph, the way Buzz, noScribe and other transcription apps can write them. Speakers are read from VTT voice tags and from lines that start with a name, such as `Ruth Hammond:` or `SPEAKER_01:`. Text without timestamps can be imported too, but its bites can't go in the edit list.
- **Links each transcript to its clip:** the clip name your editing app knows the media by, the reel, and the timecode the clip starts at, picked from the [footage log](../footage-log/) or typed in. Link it to the [interview](../interview-log/) and the person speaking, too.
- **Pick bites** by clicking lines in a transcript; shift-click to pick a run. Lines that follow one another become one bite. Find words across the transcript, and see which lines are already in a scene.
- **Arrange bites into scenes.** Name the scenes, move bites and scenes up and down, move a bite into the next or previous scene, trim a bite's words, adjust its source in and out, and add a note for the editor. Each scene shows its length and the paper edit its running time.
- **Keeps each bite's source in and out** as the clip's starting timecode plus the transcript's times, at the frame rate you set. A bite keeps its timecodes even if its transcript is later removed.
- **Prints the paper edit** by scene, with each bite's source in and out, clip, speaker, words and note.
- **Exports an edit list** in the CMX 3600 EDL format, which Premiere, Resolve and Avid can import, with each bite as an event in order from the sequence start you set, and the clip name in a `FROM CLIP NAME` comment so the app can relink the media. Timecode is non-drop-frame. **Exports CSV** with the same timecodes. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/paper-edit-template.csv) with the same columns as the CSV export.

Test the edit list with a few bites in your editing app before you depend on it. Apps differ in how they match an EDL's reels and clip names to media.

- **Shares transcripts with the interview log.** A transcript imported in either tool shows in both, linked to its interview.
- **Brings in favorite moments** from the [interview log](../interview-log/) as bites: choose **Add favorite moments** in Scenes. A moment marked from a transcript in the paper edit keeps its timecodes; the others come in with the clip they're linked to, to time later. Each bite keeps its `momentId`, so a moment isn't brought in twice.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `paperEdit` record with `frameRate`, `recordStart` (where the sequence starts), `transcripts` and `scenes`.

- Each transcript has an `id`, `name`, `format` (`srt`, `vtt` or `text`), `segments` (each with an `id`, `text`, and optional `start` and `end` in seconds from the start of the clip, and `speaker`), and optional `interviewId`, `personId`, `clipId` (a clip in the footage log), `clipName`, `reel` and `startTc`.
- Each scene has an `id`, `title` and `bites`. Each bite has an `id`, `transcriptId`, `segmentIds`, `text`, and optional `in` and `out` in seconds, `speaker`, `note`, and `clipName`, `reel`, `sourceName`, `tcIn` and `tcOut`, kept so a bite keeps its source if its transcript is removed.

It reads `people`, `interviews` and the clips in `assets`. A bite brought in from the interview log has a `momentId`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Drop-frame timecode
- FCPXML and AAF exports, and separate audio tracks in the edit list
- Reading transcripts from Word documents or noScribe's HTML; export VTT or text from those apps instead

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
