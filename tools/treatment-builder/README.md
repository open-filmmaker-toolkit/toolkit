<p align="center">
  <b>A treatment written section by section, with word counts, subjects and team from your project, and versions you can compare.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Treatment builder

Write a documentary or narrative treatment from a structured outline: logline, short and long synopsis, characters and subjects, story and structure, visual approach, access, why now, and team. Each section counts its words against a target you can change. Save a version before a draft goes out, and see exactly what changed since.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#44](https://github.com/open-filmmaker-toolkit/toolkit/issues/44).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo.

## What it does

- **Sections for each part of a treatment,** with a short note on what goes in each.
- **Counts words against a target.** Each section starts with a typical target (50 words for a logline, 150 for a short synopsis, 750 for a long one, and so on). Change any target to match a funder's limit. Counts turn amber near the target and red over it, and the outline on the side shows every section at a glance.
- **Pulls subjects and team from the project.** **Add subjects from the project** adds a line for each person on camera or interviewed, with what the subject tracker says about them, and for possible subjects you haven't added to the project yet. **Add the team from the project** adds each crew member's role and name. Lines already in the section aren't added twice. Write them up in your own words from there.
- **Keeps versions.** **Save version** keeps a named copy of every section. **Compare** shows what changed since then, section by section, with removed words struck through and added words highlighted. You can also go back to a saved version.
- **Exports** to PDF through the print dialog, and as Markdown or plain text.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [Word template](../../templates/treatment-template.docx) with the same sections and targets.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `treatment` object:

- `sections`: the text of each section, by key: `logline`, `shortSynopsis`, `longSynopsis`, `subjects`, `structure`, `approach`, `access`, `whyNow` and `team`. Empty sections are left out.
- `targets`: word targets you changed from the defaults, by the same keys.
- `versions`: saved versions, each with an `id`, `at` (when it was saved), a `label` and a copy of `sections`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Character counts, for funders who limit characters instead of words. The grant narrative library has them, for answers you reuse
- More than one treatment in a project, such as a short and a long version
- Export to Word

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
