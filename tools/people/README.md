<p align="center">
  <b>Everyone in your film in one list: subjects, crew and contacts.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# People

Add everyone in the film once: subjects, crew, interviewees and contacts, with what they do and how to reach them. The call sheet, release tracker, deal memos, credits, name supers and the other tools all use this list, so you never type a name twice. It's also where the home page's **People** part sends you to add someone or paste a list.

Part of the [Open Filmmaker Toolkit](../../README.md).

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

- **Lists everyone** with their roles, email and phone, and whether they're on camera or a subject. Filter by subjects, on camera, or crew and contacts, and search names, roles, contact details and notes.
- **Pastes a list.** Choose **Paste a list** and paste one person per line, from your treatment, a spreadsheet or an email. Anything after a comma is what they do. You see every row before it's added, and anyone already here is unticked so no one is added twice. Type "subject" as the role to add someone to the [subject tracker](../subject-tracker/) as well. It's plain text matching, with no AI.
- **Works with the subject tracker.** Tick **A subject of the film** to add someone to the subject tracker, where you keep their follow-ups and contact log. Subjects in the tracker who aren't in this list yet are listed on the side, with **Add to People**.
- **Keeps the project whole.** You can't remove someone another tool still uses, such as on a call sheet or a release. The tool says where, so you can change it there first.
- **Prints** the list and **exports CSV.** For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/people-template.csv) with the same columns.
- **Imports from a spreadsheet** (the template's columns import as they are) and **from an address book** (a .vcf file from Apple Contacts, Google Contacts or Outlook). Importing only adds.
- **Keeps earlier versions** of the project file each time you save, under **Earlier versions**, to look back at or restore.

The list holds contact details. Keep the project file and any printouts private.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Nothing new: it edits the `people` list that every tool shares. Each person has an `id`, and optional `name`, `roles` (a list), `email`, `phone`, `onCamera`, `bio` and `notes`. Ticking **A subject of the film**, or pasting someone as a subject, also adds a `subjects` entry with their `name`, `personId`, `email`, `phone` and `status: "agreed"`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Merging two entries for the same person
- Photos of people

If something else you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
