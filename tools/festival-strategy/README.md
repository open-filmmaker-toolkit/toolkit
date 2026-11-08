<p align="center">
  <b>A festival run that keeps your premiere.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Festival strategy map

Plan a festival run. Give each festival its tier, the premiere it asks for, where it is and when. The map puts them in date order and warns you when an earlier festival would cost you a premiere at a later one.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#77](https://github.com/open-filmmaker-toolkit/toolkit/issues/77).

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

- **Festivals with their premiere rules:** tier 1 to 4, world, international, regional, country or city premiere, or none, plus city, country, region, festival dates, deadline, fee and notification date.
- **Premiere clashes.** If a festival that screens first would end the premiere a later one asks for, both are flagged. It's a firm clash when the earlier festival has accepted you, and a risk when you're still waiting.
- **Hear back first:** festivals that want a premiere, by tier and notification date, so you know whose answer to wait for before accepting an earlier one.
- **Fees:** paid, still to pay and the total. **Next deadlines** for festivals you plan to enter.
- Works on the same festivals as the [festival submission tracker](../festival-submissions/), which keeps platforms, waivers and screenings.
- **Prints the run** in landscape and **exports CSV.** Also exports project data as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/festival-strategy-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Adds `tier`, `premiere` (`world`, `international`, `regional`, `national`, `city` or `none`), `city`, `country`, `region`, `startDate`, `endDate` and `notifyDate` to `festivals`, and a `festivalStrategy` record with `homeCountry` and `homeRegion`.

Screening dates from the festival submission tracker count as the first day a film screens. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Each festival's own premiere rules, such as which earlier screenings it allows
- Early, regular and late deadlines with their fees
- A calendar view

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
