<p align="center">
  <b>The people you might film: who they are, how you found them, where access stands and when to follow up.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Subject tracker

Keep a list of possible subjects while you're still finding your film: who they are, how you found them, where the conversation stands, and what to follow up about. When someone agrees, add them to the project, ready for the release tracker, call sheets, supers and credits.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#41](https://github.com/open-filmmaker-toolkit/toolkit/issues/41).

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

- **Logs possible subjects** with who they are, how you found them, phone, email, story notes, and access: researching, in conversation, agreed or declined.
- **Puts follow-ups first.** Set a follow-up date and what it's about. The list sorts by the next follow-up, and anything overdue or due in the next week is flagged and listed on the side.
- **Keeps a contact log.** Log each call, email or meeting with a date and a note. The latest one is the last contact date.
- **Adds subjects to the project.** **Add to the project** turns a subject into a person in the project, as an interview subject on camera, with their phone and email. If someone with the same name is already in the project, it links to them instead. Subjects who agree but aren't in the project yet are flagged.
- **Finds people.** Filter by access status and search names, notes and how you found them.
- **Prints** the list grouped by access, and **exports CSV**.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

Possible subjects stay out of the project's people until you add them, so the release tracker and credits builder don't list people you never filmed. For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/subject-tracker-template.csv) with the same columns.

The list holds contact details. Keep the project file and any printouts private.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `subjects` list. Each subject has an `id`, and optional `name`, `about`, `foundVia`, `phone`, `email`, `status` (`researching`, `in-conversation`, `agreed` or `declined`), `lastContact` and `nextFollowUp` (dates as YYYY-MM-DD), `nextFollowUpNote`, `notes`, a `log` of `{ date, note }` entries, and `personId` once they're in `people`.

**Add to the project** adds a person to `people` with `name`, `roles` ("Interview subject"), `onCamera: true`, and `phone` and `email` if you have them. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Reminders outside the tool, such as a calendar file of follow-ups
- Linking subjects to research sources and locations
- Importing contacts

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
