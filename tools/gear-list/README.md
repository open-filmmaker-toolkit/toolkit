<p align="center">
  <b>Every piece of gear, packed by shoot day, with what it costs and what it’s worth.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Gear list

List the gear for a shoot by department: what you own, what you're borrowing and what you're renting and from whom, with day and week rates, replacement values and serial numbers. Pack it by shoot day, print a load-out checklist, and print the equipment schedule your insurer asks for.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#57](https://github.com/open-filmmaker-toolkit/toolkit/issues/57).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's gear, rental houses and serial numbers are made up.

## What it does

- **Gear by department:** camera, lenses, sound, lighting, grip and electric, data and media, and other. For each item: how many, whether it's owned, borrowed or rented, the owner or rental house, day and week rates, replacement value, serial numbers and notes.
- **Packages for each shoot day.** Pick a day from the [shooting calendar](../shooting-calendar/), or name a package that isn't tied to one, and tick what's going. Start from another day's package to save ticking it all again.
- **Costs and values.** The side panel totals the value of owned and borrowed gear, and what each rental house costs for the days its gear is packed, at the day rate or the week rate, whichever is cheaper. Gear that isn't owned and has no value is flagged, since the insurance schedule needs one.
- **Prints a load-out checklist** for a package, by department, with boxes to tick each item out at load-out and back at wrap, and its serial numbers.
- **Prints an insurance schedule:** every item with its owner or rental house, serial numbers, quantity and value, with totals for owned, borrowed and rented gear.
- **Exports CSV,** with the days each item is packed and what each rental costs. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

The [COI and permit tracker](../coi-permit-tracker/) reads the rental houses from this list and flags any without a certificate of insurance before the days their gear is packed.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/gear-list-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `gear` record with `items` and `packages`. Each item has an `id`, `name`, `department` (`camera`, `lenses`, `sound`, `lighting`, `grip`, `data` or `other`), `source` (`owned`, `borrowed` or `rental`), and optional `quantity`, `from` (the owner, lender or rental house), `dayRate`, `weekRate`, `value` (the replacement value of one), `serial` and `notes`. Each package has an `id`, a `shootDayId` pointing to `shootDays` or a `name`, `itemIds` pointing to the items, and optional `notes`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Sending rental costs to the budget
- Checking gear out to a person and back in
- Purchase dates and receipts for the insurance schedule
- Kits that bundle several items, such as a camera with its batteries and cards

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
