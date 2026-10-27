<p align="center">
  <b>Who you've talked to at each funder, what you asked for, and what's next.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Funder CRM

Keep track of your relationships with foundations, government funders, investors, broadcasters and distributors: the people you know there, every meeting, call and email, the applications you've sent, and the next step with each one.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#50](https://github.com/open-filmmaker-toolkit/toolkit/issues/50).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's funders and the people at them are made up.

## What it does

- **Logs organizations** with their kind (foundation, government, broadcaster, investor, distributor, company, individual donor), a stage (prospect, in conversation, funding the film, or passed), a website and notes.
- **Keeps the people** at each one, with title, email and phone.
- **Logs meetings, calls, emails and events** with the date, who it was with, and notes. The list shows the last contact with each organization.
- **Keeps next steps with due dates.** Organizations with an overdue step come first, then the soonest. The side panel lists every open step across all of them; tick one to mark it done.
- **Links to applications in the [grant calendar](../grant-calendar/),** showing each one's status. "Add from the grant calendar" adds the funders named there that aren't in the CRM yet, already linked to their applications.
- **Filters by stage** and searches names, people and notes.
- **Exports CSV and prints** one row per organization, with people, last contact, next step and applications. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/funder-crm-template.csv) with the same columns.

This tool holds other people's contact details. Keep the project file somewhere private, and don't attach it to an issue.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `funders` list. Each organization has an `id`, a `type` and a `stage`, and optional `name`, `website`, `notes`, `contacts` (each with `id`, and optional `name`, `title`, `email`, `phone`), `interactions` (each with `id`, `date`, `kind` and `note`, and an optional `contactId`), `nextSteps` (each with `id`, and optional `due`, `text` and `done`) and `grantIds`, pointing to grants in `grants`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reminders outside the tool, such as a calendar file of next steps
- Importing contacts from a spreadsheet or an address book
- Linking investors and broadcasters to sources in the finance plan

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
