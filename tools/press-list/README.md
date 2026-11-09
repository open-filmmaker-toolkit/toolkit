<p align="center">
  <b>Who covers what, who has seen the film, and what they've published.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Press list

Keep a press list for your film: the outlets, the journalists and critics who cover them and the beat each one writes about, the screener links you've sent, who has said they'll come to a screening, and the coverage that comes back.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#81](https://github.com/open-filmmaker-toolkit/toolkit/issues/81).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's outlets and the people at them are made up.

## What it does

- **Keeps outlets** with a kind (newspaper or magazine, website, TV or radio, podcast, newsletter, trade or festival press, freelancer), a website and notes.
- **Keeps the people at each outlet by beat,** with email and phone. Pick a beat above the list to see only the outlets with someone on it.
- **Logs screeners sent** with the date, who got it and the link.
- **Tracks screening RSVPs** for each person: invited, coming, declined or attended. Screenings are shared with the [partner CRM](../partner-crm/), and you can add one right in the outlet.
- **Edits and removes screenings** from the Screenings list in the side panel. Before removing one, it says which partners link to it and how many press RSVPs name it, and removes those links with it. Changes show in the partner CRM too.
- **Logs coverage** with the date, kind (review, article, interview or mention), headline and link. Only web links are made clickable.
- **Reminds you to follow up.** Set a date and what it's about, and a reminder shows at the top from a week before. A screener you sent two weeks ago with no RSVP or coverage since shows too. Dismiss a reminder and it comes back only if its date changes.
- **Shows where each outlet stands:** not yet sent a screener, screener sent, coming to a screening, or covered the film. Filter by that, and search names, people, beats and headlines.
- **Exports CSV and prints** one row per outlet. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details, call sheets or screenings as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/press-list-template.csv) with the same columns.

This tool holds other people's contact details. Keep the project file somewhere private, and don't attach it to an issue.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/press-list-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **The press kit:** what's in the [EPK and press notes builder](../press-notes/), with a button that copies the logline, synopsis, director's statement, technical details and press contacts to paste into an email with a screener link.
- **Imports contacts from an address book.** Choose **Import from an address book** under the file buttons and pick a .vcf file exported from Apple Contacts, Google Contacts or Outlook. Every contact is listed first, so you pick which to add. Each joins the outlet named by their organization, which is added if it's new, and their job title becomes their beat. A contact that matches one already here, by name or email, starts unticked; ticking it fills in only what it's missing.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `pressOutlets` list. Each outlet has an `id` and a `type`, and optional `name`, `website`, `notes`, `followUpDate` and `followUpWhat` (when to follow up and what about), `dismissedReminders`, `contacts` (each with `id`, and optional `name`, `beat`, `email`, `phone`), `screeners` (each with `id`, and optional `date`, `contactId`, `url` and `note`), `rsvps` (each with `id`, a `screeningId` and a `status` of `invited`, `yes`, `no` or `attended`, and an optional `contactId`) and `coverage` (each with `id`, and optional `date`, `kind`, `headline`, `url` and `contactId`).

It also adds screenings to a shared `screenings` list, each with an `id` and optional `title`, `date`, `place`, `locationId` and `notes`, which the partner CRM uses too. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
