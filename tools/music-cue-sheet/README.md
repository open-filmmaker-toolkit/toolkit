# Music cue sheet

Build the music cue sheet your distributor or broadcaster needs at delivery, from the music already in your clearance log.

Tracking issue: [#24](https://github.com/open-filmmaker-toolkit/toolkit/issues/24).

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

Open a project file in one tool at a time, and save before switching. If both tools have the same file open and both save, the last save wins ([#16](https://github.com/open-filmmaker-toolkit/toolkit/issues/16)).

## What it does

- **Lists cues in timecode order** with sequence numbers and durations rounded to the second (a cue that plays at all gets at least one second).
- **Records credits.** For each cue: composers and authors, and publishers, each with a role, performing rights society and share. Society names autocomplete, and you can type any society. **Split evenly** divides shares, and **Copy credits from another cue** reuses them when the same music plays twice.
- **Checks each cue.** A cue is ready when it has a title, usage, valid timecode, at least one named composer or author, a society and share for everyone, composer and author shares totaling 100%, and publisher shares totaling 100%. Public domain music (marked so in the clearance log) doesn't need a publisher. Music marked Replace or cut is flagged as being replaced.
- **Shows the music across the film.** The timeline places each cue where it plays, colored by whether its entry is ready.
- **Prints the cue sheet** in landscape with a header (production company, producer, distributor, release date, running time, music supervisor, who prepared it, which cut), every cue, and usage and role legends. If any cue isn't ready, the sheet prints marked as a draft.
- **Exports CSV** with one row per cue.

Usage codes: BI background instrumental, BV background vocal, VI visual instrumental, VV visual vocal, MT main title, ET end title.

Roles: C composer, A author (lyrics), CA composer and author, AR arranger, E publisher, AM administrator, SE sub-publisher.

## What it adds to the project file

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

Pending legal review ([#3](https://github.com/open-filmmaker-toolkit/toolkit/issues/3)). Check cue sheet requirements with your distributor; this tool is a working record, not legal advice.
