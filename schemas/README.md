# Shared project file

`project-v1.schema.json` describes the version 1 `.oft.json` project file. The existing [sample project](../samples/the-river-keeps.oft.json) demonstrates the format and can be used to test tools.

## Data model

The file is a JSON object with a `project` record and collections for reusable entities. Each entity has an `id` unique within its collection. References are IDs in the collection named by the field: contracts can refer to `personIds`, `locationIds`, `thirdPartyElementIds` and `assetIds`; a third-party element can refer back through `contractIds`.

| Collection | Purpose |
| --- | --- |
| `subjects` | People you might film, kept by the [subject tracker](../tools/subject-tracker/README.md#what-it-adds-to-the-project-file) until they're added to `people`; `personId` points to the person they became |
| `people` | Cast, crew, subjects and other contributors. `onCamera` marks someone who needs a release |
| `locations` | Places involved in production. `onCamera` marks a place that's filmed |
| `thirdPartyElements` | Archival material, music, artwork, logos and other clearances |
| `contracts` | Releases, licenses and other agreements; references the people, locations, elements and assets they cover. See [Releases](#releases) |
| `callSheets` | Shoot days: date, call and wrap times, a location, weather, schedule, and crew with call times; references `locations` and `people`. `locations` may also carry `latitude` and `longitude` |
| `assets` | Project materials such as footage, scans and documents; `relativePath`, when present, is relative to the project file |
| `credits` | The end credits, in order. A record rather than a collection; see [Credits](#credits) |
| `supers` | On-screen names and titles (supers and lower thirds), and the list as it was last exported for graphics. A record rather than a collection; entries refer to `people` by `personId`, whose `name` is the spelling used. See the [name supers list](../tools/name-supers/README.md#what-it-adds-to-the-project-file) |

Tools should add only fields they own and preserve unknown fields and collections when saving. New collections and their fields are optional in version 1, so existing tools can continue to open files that do not use them. A tool that consumes references should report missing targets rather than silently discarding them. JSON Schema checks field shapes; tools remain responsible for ensuring IDs are unique within collections and references point to existing records.

## Releases

The release tracker treats a contract as a release when its `type` contains "release". It writes `appearance release`, `location release`, `materials release` and `other release`, with a `status` of `pending`, `signed` or `declined`, and dates as YYYY-MM-DD. A release is expired when it's signed and its `expirationDate` has passed.

- A person needs a release when `onCamera` is true, or when it's unset and an appearance or other release names them.
- A location needs a release when `onCamera` is true, or when it's unset and a call sheet or a location or other release names it.
- `onCamera: false` takes someone or somewhere off the list even if a release or call sheet names them.
- Materials releases cover clearance-log items through `thirdPartyElementIds`; each item records the release in `contractIds`. They don't cover a person's appearance.
- Signed copies are `assets` with `type` "release scan" and a `relativePath` under `releases/`, relative to the project file.

## CSV exports

Each tool can export one project record or collection at a time to its own CSV file: `project`, `people`, `locations`, `thirdPartyElements`, `contracts`, `assets`, `musicCueSheet` and `callSheets`. Each property becomes a column; nested arrays and objects are encoded as JSON in a cell. The export includes all records in that collection, not only records visible under a tool's current filters.

## Credits

The credits builder keeps the end credits in a `credits` record: `entries` in the order they roll, and `notCredited`, the IDs of people left out on purpose so they aren't flagged as missing.

- Each entry has an `id` and a `kind`: `credit` (a `role`, with `personIds` from `people` and `names` for anyone not in the project), `heading`, `text`, `music` or `archival`.
- `music` and `archival` entries don't store their lines. They're built from the clearance log and music cue sheet each time, and store only a `heading` and the `excluded` keys of songs or sources left out. A key is the song title, or the source's name, in lowercase with accents and punctuation removed.
- A contract's `requiredCredit` is the on-screen credit it requires, word for word. The credits meet it when a line contains that wording, ignoring capitals and punctuation.
- Credits aren't one of the CSV exports. The credits builder exports them as text for the crawl.

## Concurrent edits

When a browser supports direct file access, a tool compares the opened file with the last version it read or saved before writing. If the file changed, the user can reload the latest version, save their edits to a separate copy, or explicitly overwrite the newer file. The check cannot lock the file against a simultaneous write, so teams should save in one tool at a time. Download-based save flows cannot check the source file and instead produce a new download; users should open the latest shared copy before continuing.

Do not change `formatVersion` or make a breaking change to this model without a maintainer decision. Additive fields and collections can be introduced in version 1 while they remain optional and compatible with tools that preserve unknown data.

## License

The schema is code, under GPL-3.0-or-later. These notes are documentation, under CC BY-SA 4.0. See [Licenses](../README.md#licenses).
