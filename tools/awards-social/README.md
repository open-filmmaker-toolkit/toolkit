<p align="center">
  <b>Awards deadlines and posts, on one calendar with your festivals.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Awards and social calendars

Plan awards campaigns and social posts around your festival and release dates. Every dated item goes on one calendar, with festival screenings from the festival tools and the release date from the project.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#82](https://github.com/open-filmmaker-toolkit/toolkit/issues/82).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's data is made up.

## What it does

- **Awards** with category, eligibility rules and window, entry deadline and fee, voting, nominations and ceremony dates, and status. Each award's window is checked against the film's first festival screening or release date.
- **Rules it can check.** Set an award's running time limits, the theatrical run it needs and in which cities, whether a festival win qualifies instead, and whether it rules out TV or streaming first. Each award then says whether the film meets them, from the running time in the film details, theatrical runs in [bookings](../bookings/), festival wins in the [festival submission tracker](../festival-submissions/), and signed TV and streaming deals. The toolkit doesn't come with each award's rules built in, because they change every year: copy them from the award's own rules.
- **Shares award lists.** **Save an award list** writes your awards, their rules, usual window and deadline and fee to a small file, without your status or notes. **Add from a list** opens one and adds the awards you pick with their next dates.
- **Social posts** with a date, where they go, the text, a link and status: idea, draft, scheduled or posted.
- **One calendar,** by month: award dates, posts, accepted and pending festival starts and screenings, and the release date. Filter by kind.
- **Suggested posts** for each accepted festival (four weeks before, a week before, the day and a thank-you) and the release, added as drafts in one click.
- **Exports a calendar file (.ics)** for your calendar app, and **prints** the calendar and the awards.
- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **A month grid.** Switch the calendar from **List** to **Month** to see the awards, posts and festival dates on a grid. Use the arrows to move between months. On a phone, the month becomes a list of the days with something on them.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

An `awards` collection (`name`, `category`, `rules`, `windowStart`, `windowEnd`, `deadline`, `fee`, `status`, `votingStart`, `nominationsDate`, `ceremonyDate`, `notes`, and `rulesCheck`: `minMinutes`, `maxMinutes`, `runDays`, `runCities`, `festivalWin` and `noTv`) and a `socialPosts` collection (`date`, `platform`, `status`, `text`, `link`, and `eventKey` for suggested posts).

It reads `festivals` and the project's `releaseDate`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Posting to social platforms (the toolkit never connects to them)

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
