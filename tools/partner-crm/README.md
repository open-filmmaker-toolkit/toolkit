<p align="center">
  <b>Who's helping the film reach people, what each side promised, and where you've screened together.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Partner CRM

Keep track of the community groups, nonprofits, schools, libraries, venues and campaigns that partner on your film's outreach: the people you know there, what you've promised each other and by when, and the screenings you're doing together.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#90](https://github.com/open-filmmaker-toolkit/toolkit/issues/90).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's partners and the people at them are made up.

## What it does

- **Keeps partner organizations** with a kind (community group, nonprofit, school or university, library, museum or cinema, government, faith or civic group, company), a stage (prospect, in conversation, partnering or finished), a website and notes.
- **Keeps the people** at each one, with title, email and phone.
- **Tracks commitments and next steps** with due dates, marked as what you will do or what they will do. Partners with an overdue step come first, then the soonest. The side panel lists every open step; tick one to mark it done.
- **Links partners to screenings.** Screenings are shared with the [press list](../press-list/), and you can add one right in the partner. The side panel shows how many partners are part of each.
- **Edits and removes screenings** from the Screenings list in the side panel. Before removing one, it says which partners link to it and how many press RSVPs name it, and removes those links with it. Changes show in the press list too.
- **Filters by stage** and searches names, people, commitments and screenings.
- **Exports CSV and prints** one row per partner. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets or screenings as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/partner-crm-template.csv) with the same columns.

This tool holds other people's contact details. Keep the project file somewhere private, and don't attach it to an issue.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/partner-crm-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Imports contacts from an address book.** Choose **Import from an address book** under the file buttons and pick a .vcf file exported from Apple Contacts, Google Contacts or Outlook. Every contact is listed first, so you pick which to add. Each joins the partner named by their organization, which is added if it's new. A contact that matches one already here, by name or email, starts unticked; ticking it fills in only what it's missing.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `partners` list. Each partner has an `id`, a `type` and a `stage`, and optional `name`, `website`, `notes`, `contacts` (each with `id`, and optional `name`, `title`, `email`, `phone`), `commitments` (each with `id`, and optional `text`, `due`, `done` and `by`, which is `us` or `them`) and `screeningIds`, pointing to screenings.

It also adds screenings to a shared `screenings` list, each with an `id` and optional `title`, `date`, `place`, `locationId` and `notes`, which the press list uses too. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
