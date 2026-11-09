<p align="center">
  <b>Every festival you submit to, with its deadline, fee, platform and result, and the screening dates once you're in.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Festival submissions

Keep track of the festivals you plan to submit to, and the ones you have: the deadline, the fee and any waiver code, the platform you submit through, and where each one stands. When a festival accepts you, add its screening dates and see them in one list.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#78](https://github.com/open-filmmaker-toolkit/toolkit/issues/78).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's festivals are made up.

## What it does

- **Logs each submission** with the festival, the platform, a link, the deadline, the fee, a waiver code, the date you submitted, and notes.
- **Tracks status:** planned, submitted, accepted or declined. Filter the list by status; each filter shows how many festivals it holds. Search by festival, platform, waiver code, notes or screening venue.
- **Shows the next deadlines first.** Planned festivals with an upcoming deadline come first, then planned ones whose deadline has passed, then submitted, accepted and declined. Each planned row says how many days are left. A deadline within two weeks is flagged, and so is one that has passed.
- **Keeps screening dates for accepted festivals.** Add a date, time, venue and note for each screening. Accepted festivals show their next screening, and a side list shows every upcoming screening in date order.
- **Adds up the fees:** what's still to pay on planned festivals and what you've paid on submitted ones, in the project's currency.
- **Laurels, screening fees and travel** for accepted festivals: official selection, nominee or winner with the award's name and whether you have the laurel files, what the festival pays you to screen and whether it's paid, and what it covers for travel against what travel will cost you. The side panel adds up screening fees still owed and travel.
- **Reminders** at the top when you open it: a deadline in the next two weeks or one that has passed, a decision that's late, a screening in the next week, and a screening fee not paid two weeks after the festival. Dismiss one and it comes back only if its date changes.
- **Shares festival lists.** **Save a festival list** writes your festivals, their usual deadlines, fees, deadline tiers and premiere rules to a small list file, without waiver codes or notes. **Add from a list** opens one, from your team or an earlier project, and adds the festivals you pick with the next deadlines coming up. There's a [sample list](../../samples/shared-festival-list.json) of fictional festivals to try.
- **Shows deadline tiers** set in the [festival strategy map](../festival-strategy/): early, regular and late, each with its fee. Reminders use the next one still open.
- **Fills in the submitted date.** Change a festival to submitted and the date defaults to today. You can change it.
- **Exports CSV and prints** the list on one page. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

The festival link is stored as plain text. It only becomes a clickable link if it starts with `http://` or `https://`.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet or a submission platform:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file: one with the columns of the [spreadsheet template](../../templates/festival-submissions-template.csv), or the export a submission platform gives you. Its usual column names, such as Festival Name, Deadline Date, Entry Fee and Judging Status, are matched for you, and statuses such as In Consideration, Not Selected and Official Selection become submitted, declined and accepted. A festival already here is skipped.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `festivals` list. Each festival has an `id` and a `status` (`planned`, `submitted`, `accepted` or `declined`), and optional `name`, `platform`, `url` (text), `deadline` (a date), `fee` (a number, in the project's currency), `waiverCode`, `submittedOn` (a date), `notes` and `dismissedReminders`. An accepted festival can also have `laurel` (`selection`, `nominee` or `winner`), `laurelAward`, `laurelFiles` (true once you have them), `screeningFee` and `screeningFeePaid`, `travelSupport` (what the festival covers) and `travelCost`. An accepted festival can have `screenings`, each with an `id` and optional `date`, `time` (text), `venue` and `note`. Screenings are kept if you change the status later.

Everything else in the file is preserved, including fields this tool doesn't recognize. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
