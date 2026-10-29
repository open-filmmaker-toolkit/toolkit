<p align="center">
  <b>A dated journal of the production: what happened, what you learned and the story ideas you don't want to lose.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Field journal

Keep a dated journal of the production. Tag each entry with the people and locations it's about, link it to a shoot day, search across everything you've written, and export it as Markdown.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#66](https://github.com/open-filmmaker-toolkit/toolkit/issues/66).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's entries are made up.

## What it does

- **Dated entries.** Each has a date (today's, to start), an optional kind (what happened, what you learned, or a story idea), a title and your text.
- **Tags from the project.** Tick the people and locations an entry is about, from the project's own lists. If someone is removed from the project later, the entry says so instead of dropping the tag.
- **Linked to a shoot day.** Pick a call sheet from the [call sheet tool](../call-sheet/). If the entry has no date yet, it takes the call sheet's.
- **Search across entries.** Type words to find them in titles, text, tags and shoot days, ignoring capitals and accents. Narrow the list to one person, one location or one kind.
- **Exports Markdown** of the entries shown, oldest first, with each entry's kind, shoot day, people and locations under its heading. Clear the search and filters to export everything.
- **Prints** the same entries as a plain journal. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `journal` list. Each entry has an `id` and optional `date` (YYYY-MM-DD), `kind` (`happened`, `learned` or `idea`), `title`, `text`, `personIds` (pointing to `people`), `locationIds` (pointing to `locations`) and `callSheetId` (pointing to `callSheets`). The tool reads `people`, `locations` and `callSheets` and doesn't change them. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Photos or audio notes attached to an entry
- Tags of your own beyond people and locations
- Linking an entry to a shoot day in the shooting calendar, or to an interview
- Rich text; entries are plain text, and Markdown you type is kept as written

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
