# Shared project file

`project-v1.schema.json` describes the version 1 `.oft.json` project file. The existing [sample project](../samples/the-river-keeps.oft.json) demonstrates the format and can be used to test tools.

## Data model

The file is a JSON object with a `project` record and collections for reusable entities. Each entity has an `id` unique within its collection. References are IDs in the collection named by the field: contracts can refer to `personIds`, `locationIds`, `thirdPartyElementIds` and `assetIds`; a third-party element can refer back through `contractIds`.

| Collection | Purpose |
| --- | --- |
| `people` | Cast, crew, subjects and other contributors |
| `locations` | Places involved in production |
| `thirdPartyElements` | Archival material, music, artwork, logos and other clearances |
| `contracts` | Releases, licenses and other agreements; references the people, locations, elements and assets they cover |
| `callSheets` | Shoot days: date, call and wrap times, a location, weather, schedule, and crew with call times; references `locations` and `people`. `locations` may also carry `latitude` and `longitude` |
| `assets` | Project materials such as footage, scans and documents; `relativePath`, when present, is relative to the project file |

Tools should add only fields they own and preserve unknown fields and collections when saving. New collections and their fields are optional in version 1, so existing tools can continue to open files that do not use them. A tool that consumes references should report missing targets rather than silently discarding them. JSON Schema checks field shapes; tools remain responsible for ensuring IDs are unique within collections and references point to existing records.

## CSV exports

Each tool can export one project record or collection at a time to its own CSV file: `project`, `people`, `locations`, `thirdPartyElements`, `contracts`, `assets`, `musicCueSheet` and `callSheets`. Each property becomes a column; nested arrays and objects are encoded as JSON in a cell. The export includes all records in that collection, not only records visible under a tool's current filters.

## Concurrent edits

When a browser supports direct file access, a tool compares the opened file with the last version it read or saved before writing. If the file changed, the user can reload the latest version, save their edits to a separate copy, or explicitly overwrite the newer file. The check cannot lock the file against a simultaneous write, so teams should save in one tool at a time. Download-based save flows cannot check the source file and instead produce a new download; users should open the latest shared copy before continuing.

Do not change `formatVersion` or make a breaking change to this model without a maintainer decision. Additive fields and collections can be introduced in version 1 while they remain optional and compatible with tools that preserve unknown data.
