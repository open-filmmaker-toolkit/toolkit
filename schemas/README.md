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
| `assets` | Project materials such as footage, scans and documents; `relativePath`, when present, is relative to the project file |

Tools should add only fields they own and preserve unknown fields and collections when saving. New collections and their fields are optional in version 1, so existing tools can continue to open files that do not use them. A tool that consumes references should report missing targets rather than silently discarding them. JSON Schema checks field shapes; tools remain responsible for ensuring IDs are unique within collections and references point to existing records.

Do not change `formatVersion` or make a breaking change to this model without a maintainer decision. Additive fields and collections can be introduced in version 1 while they remain optional and compatible with tools that preserve unknown data.
