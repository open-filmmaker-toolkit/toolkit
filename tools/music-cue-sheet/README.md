<p align="center">
  <b>The music cue sheet your distributor needs, built from the music already in your clearance log.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Music cue sheet

Build the music cue sheet your distributor or broadcaster needs at delivery, from the music already in your clearance log.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#24](https://github.com/open-filmmaker-toolkit/toolkit/issues/24).

## Contents

- [Use it](#use-it)
- [How it works with the clearance log](#how-it-works-with-the-clearance-log)
- [What it does](#what-it-does)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. Like the clearance log, it's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo.

## How it works with the clearance log

Both tools open the same project file. Every element with type **Music** in the clearance log is a cue here, and the cue sheet adds what the clearance log doesn't track:

| Shared with the clearance log | Kept by the cue sheet |
| --- | --- |
| Timecode in and out | Title as registered, artist, cue number |
| Clearance status (read-only here) | Usage |
| Description | Composers and authors: role, society, share |
| | Publishers: role, society, share |

Cues you add here appear in the clearance log as Music with status Not started. Deleting a cue here deletes it from the clearance log too.

If the same project is open in multiple tools, save one tool before saving another. Chrome and Edge warn if the file changed since it was opened; you can reload the latest version, save your edits as a copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead of checking or overwriting the original file.

## What it does

- **Lists cues in timecode order** with sequence numbers and durations rounded to the second (a cue that plays at all gets at least one second).
- **Records credits.** For each cue: composers and authors, and publishers, each with a role, performing rights society and share. Society names autocomplete, and you can type any society. **Split evenly** divides shares, and **Copy credits from another cue** reuses them when the same music plays twice.
- **Checks each cue.** A cue is ready when it has a title, usage, valid timecode, at least one named composer or author, a society and share for everyone, composer and author shares totaling 100%, and publisher shares totaling 100%. Public domain music (marked so in the clearance log) doesn't need a publisher. Music marked Replace or cut is flagged as being replaced.
- **Shows the music across the film.** The timeline places each cue where it plays, colored by whether its entry is ready.
- **Prints the cue sheet** in landscape with a header (production company, producer, distributor, release date, running time, music supervisor, who prepared it, which cut), every cue, and usage and role legends. If any cue isn't ready, the sheet prints marked as a draft.
- **Exports CSV** with one row per cue. The blank [spreadsheet template](../../templates/music-cue-sheet-template.csv) uses the same columns, without the ones the tool works out, and there's a [Word version](../../templates/music-cue-sheet-template.docx) to fill in or print, for anyone who doesn't use the tool.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files. Nested values stay as JSON inside their cell.

Usage codes: BI background instrumental, BV background vocal, VI visual instrumental, VV visual vocal, MT main title, ET end title.

Roles: C composer, A author (lyrics), CA composer and author, AR arranger, E publisher, AM administrator, SE sub-publisher.

## What it adds to the project file

The shared [version 1 schema](../../schemas/project-v1.schema.json) documents the complete project file format, including data owned by other tools.

```json
{
  "project": {
    "distributor": "", "releaseDate": "", "runningTime": "1:24:30", "startTimecode": ""
  },
  "thirdPartyElements": [
    {
      "type": "Music",
      "music": {
        "title": "Muddy Water Hymn", "artist": "The Low Waters", "cueId": "1M5", "usage": "BV",
        "writers": [{ "name": "Earl Whitaker", "role": "C", "society": "BMI", "share": 60 }],
        "publishers": [{ "name": "Delta Song Publishing", "role": "E", "society": "BMI", "share": 100 }]
      }
    }
  ],
  "musicCueSheet": { "musicSupervisor": "" }
}
```

Running time, distributor and release date live in `project` because other tools will need them. `startTimecode` is the timecode of the first frame of picture; if it's blank, the timeline works it out from your cues (01:00:00:00 if they all start after the first hour).

## Not yet

- Series and episodes
- Splitting a cue sheet by reel
- Importing a cue sheet from CSV or from an edit decision list
- Electronic filing formats for performing rights organizations

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice). Check cue sheet requirements with your distributor.
