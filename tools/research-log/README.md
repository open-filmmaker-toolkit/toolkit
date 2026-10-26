<p align="center">
  <b>Archival leads and research sources, logged as you find them, and sent to the clearance log when they're ready.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Research and archival log

Log archival leads and research sources while you research: what each one is, where it's from, who to ask, what it might cost, and what you know about the rights. Track each archival lead from found to ready to license, then send it to the clearance log, so research and clearances start from the same list.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#42](https://github.com/open-filmmaker-toolkit/toolkit/issues/42).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Sending to the clearance log](#sending-to-the-clearance-log)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo.

## What it does

- **Two logs in one place.** **Archival leads** are footage, stills, artwork and other material you might license. **Research sources** are reports, articles, books and anything else you're working from.
- **Logs each source** with what it is, its type, archive or collection (or author and publisher), item ID, a link or call number kept as text, rights holder, contact, estimated cost and currency, rights notes and notes.
- **Tracks each archival lead** from found, to screener requested, to screener received, to ready to license, or not using. Research sources go from to check, to checked, to using, or not using.
- **Shows the pipeline.** A side panel counts archival leads at each step, how many are in the clearance log, and the estimated cost of the leads not sent yet.
- **Finds things.** Filter by status and search titles, archives, item IDs and notes.
- **Prints** both logs, and **exports CSV**.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [spreadsheet template](../../templates/research-log-template.csv) with the same columns.

## Sending to the clearance log

**Send to clearance log** adds the source to the clearance log as a third-party element, with its title, type, where it's from, rights holder, contact, cost and notes, at "Not started". The lead moves to ready to license, and both stay linked: the log shows the element's clearance status as it changes. Leads marked ready to license that aren't in the clearance log yet are flagged with a button to send them.

Clearance continues in the clearance log. Editing the source afterwards doesn't change the element.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `sources` list. Each source has an `id`, a `kind` (`archival` or `research`), and optional `title`, `status`, `type`, `archive`, `itemId`, `link`, `rightsHolder`, `contact`, `cost`, `currency`, `rightsNotes`, `notes`, and `elementId` once it's in `thirdPartyElements`.

Archival statuses are `found`, `screener-requested`, `screener-received`, `ready-to-license` and `not-using`. Research statuses are `to-check`, `checked`, `using` and `not-using`.

Sending to the clearance log adds an element to `thirdPartyElements`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Attaching screeners and documents
- Citations in a standard style for research sources
- Linking sources to subjects and to places in the cut

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
