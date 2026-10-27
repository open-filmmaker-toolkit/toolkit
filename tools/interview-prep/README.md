<p align="center">
  <b>Research, story beats and questions in order, with a one-page guide to take into the interview.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Interview prep

Prepare each interview: your research notes, the story beats it has to cover, and the questions in the order you'll ask them, with the ones you can't leave without marked. Print a one-page guide to take with you.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#54](https://github.com/open-filmmaker-toolkit/toolkit/issues/54).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's interviews are made up.

## What it does

- **Links each interview to the person in the project,** or to someone not in it yet, and to a day in the [shooting calendar](../shooting-calendar/) if there is one. People on camera are listed first.
- **Keeps research notes.** If the [subject tracker](../subject-tracker/) has notes on the person, add them in one click.
- **Story beats to cover.** Each question can belong to a beat, and beats with no questions yet are flagged, so nothing you meant to cover gets left out.
- **Questions in order.** Type a question and press Enter to add it. Move questions up or down, and mark the must-asks.
- **After the interview,** mark it done and tick the questions you asked.
- **Prints a one-page guide** for the interview you pick: who, when and where, what it's for, the beats as a checklist, the questions numbered with must-asks starred, and your notes.
- **Exports CSV** of every question, in order. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/interview-questions-template.csv) with the same columns.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

An `interviews` list. Each interview has an `id` and a `status` (`planned` or `done`), and optional `personId` (or `name` for someone not in the project), `date`, `shootDayId`, `minutes`, `goal`, `research`, `beats` (each with `id` and `text`) and `questions` (each with `id`, `text`, and optional `must`, `beatId` and `asked`), in the order they're asked. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Follow-up questions nested under a question
- Timecodes for answers, once the footage is in (planned as the transcript and selects tools)
- A question bank shared across interviews

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
