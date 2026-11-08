<p align="center">
  <b>Your fair use reasoning, written down for your attorney.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Fair use log

Document each fair use decision, element by element, with the reasoning your errors and omissions attorney will ask for: the purpose of the use, the nature of the original, how much you use and why, and the effect on the original's market. Note where the film will be shown, and print a draft memo for your attorney.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#73](https://github.com/open-filmmaker-toolkit/toolkit/issues/73).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's elements and reasoning are made up.

## What it does

- **Reads the [clearance log](../clearance-log/).** Every element marked fair use there shows up here, with its source, rights holder, timecodes, length and how it's used. Change those details in the clearance log.
- **The four factors, with the questions to answer for each:** the purpose and character of the use, the nature of the original work, how much is used and why, and the effect on the market for the original. Add how you got the material and how it's credited.
- **Where the film will be shown.** Fair use is a US doctrine. Other countries have narrower exceptions, such as fair dealing in Canada, the UK and Australia, so when the film will be shown outside the US the tool says so and keeps a note on each country.
- **The attorney's review:** a memo status (draft, ready for the attorney, reviewed), the attorney, when they reviewed it and what they said.
- **Prints a draft memo for your attorney,** for one element or all of them, with the not-legal-advice notice first. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.
- Lists elements that aren't licensed, public domain or marked fair use, in case any of them should be.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/fair-use-template.csv) with the same columns as the export.

This is not legal advice. See [Not legal advice](../../README.md#not-legal-advice). Whether a use is fair is a legal judgment. Have an attorney who knows fair use review the memo before you rely on it.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

It adds `fairUse` to elements in `thirdPartyElements` marked fair use, with optional `purpose`, `nature`, `amount`, `market`, `sourced`, `where` (`us`, `us-plus` or `outside`), `countries`, `otherCountries`, `status` (`draft`, `ready` or `reviewed`), `attorney`, `reviewedDate` and `advice`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Linking to the documentary fair use best practices statements for your kind of use
- Clip-by-clip timecodes when one element is used in several places
- Marking an element fair use from here; do it in the clearance log

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
