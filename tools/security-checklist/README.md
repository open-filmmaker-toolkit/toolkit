<p align="center">
  <b>Footage, sources and devices, protected and checked off.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Security checklist

Protect footage, sources and devices on sensitive productions with a checklist for digital and physical security: device encryption, accounts, protecting sources, footage, crossing borders and physical security. Tick items off for each person on the crew, and switch to a high-risk shoot for extra items and notes on what to change.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#61](https://github.com/open-filmmaker-toolkit/toolkit/issues/61).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's crew, ticks and plan are made up.

## What it does

- **A checklist in six sections:** devices, accounts, protecting sources, footage and files, crossing borders, and physical security.
- **Ticked off for each person.** Pick the crew from the project, or tick everyone on call sheets and shoot days who isn't on camera. Choose whose list you're checking off; each item shows how many have done it, and the side panel shows each person's progress.
- **Standard or high-risk shoot.** A high-risk shoot adds items, such as travel devices and agreeing what to do if a device is taken, and a note in each section on what to change.
- **Make it yours.** Add your own items to any section, set aside built-in ones that don't apply, and write down your production's plan: which messaging app, where backups go, who holds the source list.
- **Items for a country or border.** Give your own items a country or border, then pick one to see the list for that trip. The toolkit doesn't come with rules for each country, because they change; ask a press-freedom or digital-security organization, then save your items as a list file to share with other productions. **Add items from a list** reads one back and marks items you already have.
- **Reminds you before each trip.** Two weeks before a trip in the [travel sheet](../travel-sheet/), a reminder at the top says to go through the list again, with the items for the trip's country if you have any. Dismiss it once you have; it comes back if the trip moves.
- **Prints** every item with a tick or box for each person, the high-risk notes when it's a high-risk shoot, and your plan. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/security-checklist-template.csv) with the same columns as the export.

This is a starting point, not a full security plan. For a high-risk shoot, get advice from a digital-security or press-freedom organization, and write a [risk plan](../risk-plan/) too.
- **Links items to devices** in the [gear list](../gear-list/), such as the laptops and drives to encrypt.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `security` record with `level` (`standard` or `high`), `personIds` (who's on the checklist), `items` (your own items, each with an `id`, `section`, `text` and optional `high` and `place`, the country or border it's for), `hidden` (the ids of built-in items set aside), `done` (each item's id mapped to the people who have done it) optional `notes`, and `tripChecks` (for each trip with a reminder, its `id` and the `dismissedReminders`).

It reads `people`, `callSheets`, `shootDays` and `trips`. Items can have `gearIds`, in the gear list's `items`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
