<p align="center">
  <b>Every grant and fund deadline in one place, with what each application needs and where it stands.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Grant calendar

Keep track of the grants and funds you're applying to, or thinking about: the deadline, what's on offer, who can apply, what the application asks for, and where yours stands. See them as a list or a month calendar, and send the deadlines to your own calendar app.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#46](https://github.com/open-filmmaker-toolkit/toolkit/issues/46).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's funders are made up.

## What it does

- **Logs each grant** with the funder, program, deadline and time zone, amount available, what you asked for, what you were awarded, eligibility, a link to the guidelines, a contact, the dates you submitted and expect a decision, and notes.
- **Tracks status:** researching, drafting, submitted, awarded or declined. Filter the list by status.
- **Keeps a checklist of what the application needs.** New grants start with a narrative, budget, work sample and bios; add or remove items and tick them off as they're ready. The list shows how many are ready, in red when the deadline is two weeks away or less.
- **Shows the next deadlines first.** Open applications by deadline, then those waiting on a decision, then decided ones. Each row says how many days are left, or that the deadline passed.
- **Has a calendar view.** A month at a time, starting at the next open deadline, with grants colored by status.
- **Adds up where things stand:** open applications, how many are waiting on a decision, the total you've asked for that's still waiting, and the total awarded, in the project's currency.
- **Links the answers you used.** Tick the versions from the [grant narrative library](../narrative-library/) that went into each application. The library then shows which funder got which version, and when.
- **Reminds you** when you open it: deadlines coming up, deadlines that passed with nothing sent, and decisions that are late. Choose how early each grant reminds you, or turn it off. Dismiss a reminder and it comes back only if its date changes.
- **Shares funder lists.** **Save a list** writes your funders, their usual deadlines, amounts, eligibility and what they ask for to a small list file, without your notes or answers. **Add from a list** opens one, from your team or an earlier project, and adds the funders you pick with the next deadline coming up. There's a [sample list](../../samples/shared-funder-list.json) of fictional funders to try.
- **Exports a calendar file** (`.ics`) with an all-day event for each deadline and a reminder before each open application's deadline: two weeks unless you change it in the grant. It opens in Google Calendar, Apple Calendar and Outlook. Declined grants are left out.
- **Exports CSV and prints** the list. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/grant-calendar-template.csv) with the same columns.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/grant-calendar-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Imports from a funder database:** the spreadsheet import also matches the columns funder databases use in their exports, such as Grantmaker Name, Opportunity Title, Application Deadline and Award Amount. A grant already here, with the same funder, program and deadline, is skipped.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `grants` list. Each grant has an `id` and a `status` (`researching`, `drafting`, `submitted`, `awarded` or `declined`), and optional `funder`, `program`, `deadline` (a date), `deadlineTime` (text, such as "5 pm Eastern"), `amount` (what's available, as text), `requested` and `awarded` (numbers, in the project's currency), `eligibility`, `materials` (each with `name` and `done`), `url`, `contact`, `submittedOn`, `decisionOn`, `notes`, `remindDays` (how many days before the deadline to remind you, `0` for never; two weeks when it's missing) and `dismissedReminders` (the reminders you dismissed).

Which answers went to which grant is kept on the answers, in the library's `narratives`, so there's one record of it. Removing a grant keeps that record, with the funder's name in place of the link. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- A list of funders that the toolkit keeps up to date for everyone. Lists are shared as files instead, so nothing is fetched

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
