<p align="center">
  <b>On-screen names and titles, spelled the way the rest of your project spells them, with what changed since graphics last saw the list.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Name supers list

Keep the names and titles that appear on screen (supers, lower thirds) in one list, in the order they appear. Names come from the people in your project, so they're spelled the same as in your credits, call sheets and releases. When you send the list to your graphics artist, the tool remembers it, and flags anything that changes afterwards.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#71](https://github.com/open-filmmaker-toolkit/toolkit/issues/71).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample has a title that changed since the last export, and a name typed with a spelling mistake.

## What it does

- **Lists supers in order.** Each super has a name, a title (the second line), the timecode where it first appears, and notes. The list is sorted by timecode.
- **Uses the project's spelling.** Pick a person from the project and the super uses their name as the project spells it. Fixing the spelling in the editor fixes it in the project, so every other tool uses it too.
- **Catches near misses.** A typed name that's close to someone in the project ("Marcus Bel" for Marcus Bell) is flagged, with a button to use the project's spelling. Supers listed twice, and timecodes in the wrong format, are flagged too.
- **Shows who's missing.** Anyone in the project marked as on camera, or as an interview subject or contributor, who doesn't have a super yet is listed. Click a name to add one.
- **Previews the lower third** on a 16:9 frame with a title-safe area, as a rough check of length.
- **Tracks changes since the last export.** **Export for graphics (CSV)** downloads the list with a "Since last export" column (new, changed with what it was, removed or no change) and remembers what you sent. Until the next export, the list flags every super that's new or changed. Save the project file after exporting so the tool remembers it next time.
- **Prints** the list for proofreading, with flags.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/name-supers-template.csv) with the same columns.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `supers` object:

- `entries`: each super has an `id`, and either a `personId` (a person in `people`, whose `name` is used) or a `name`, plus optional `title`, `firstAppears` (timecode as HH:MM:SS:FF) and `notes`.
- `lastExport`: when the list was last exported for graphics (`at`), the `cutVersion` it was for, and the `entries` as they were then (`id`, `name`, `title`, `firstAppears`).

Fixing a spelling in the editor changes that person's `name` in `people`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Importing supers from an edit, such as markers or an edit decision list
- More than one appearance per super, and supers for places or dates
- Exports for specific titling tools, beyond CSV

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
