<p align="center">
  <b>Comparable films for pitches and sales, with a source for every figure, and a comps page to print.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Comps tracker

Keep a list of films like yours: where they premiered, who distributed them, where they played, and what's known about how they did, with where each figure was reported. Tag them, pick the ones for your pitch, and print a comps page.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#43](https://github.com/open-filmmaker-toolkit/toolkit/issues/43).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's comps are made up.

## What it does

- **Logs comps** with title, year, running time, director, premiere, distributor, where it played, why it's comparable, and notes.
- **Keeps a source with every figure.** Reported sales, box office, budgets or audience numbers each have a label, an amount and where it was reported. Figures without a source are flagged in red.
- **Tags comps** by subject, style and audience. Click a tag to show only the comps that have it, and search titles, distributors, festivals, figures and notes.
- **Prints a comps page.** Tick **In the pitch** on the comps you want. The printed page lists them with their premiere, distributor, figures and why they're comparable, with each figure's source as a numbered note. Figures without a source are left off. If nothing is ticked, it prints every comp.
- **Checks the page before you pitch:** figures without a source, comps with no line on why they're comparable, comps more than seven years old, and fewer than three comps.
- **Exports CSV**, and exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/comps-tracker-template.csv) with the same columns.

Reported figures are often estimates or rounded. The tool shows them as reported; it doesn't check them.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `comps` list. Each comp has an `id`, and optional `title`, `year`, `runtime` (minutes), `director`, `premiere`, `distributor`, `platforms`, `figures` (each with `label`, `amount` and `source`), `subjectTags`, `styleTags`, `audienceTags`, `why`, `notes`, and `inPitch` (on the comps page). Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Comparing comps side by side, or charting their figures
- A comps slide for the pitch deck builder
- Importing comps from a spreadsheet

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
