<p align="center">
  <b>End credits built from the people, music and archival material in your project, checked against the credits your contracts require.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Credits builder

Draft your end credits from the people in your project, the music in your clearance log and cue sheet, and your licensed archival material. Put them in order, see the crawl as it will play, check that every credit a contract requires is there, and export the crawl as text.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#19](https://github.com/open-filmmaker-toolkit/toolkit/issues/19).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Music and archival credits](#music-and-archival-credits)
- [Credits required by contracts](#credits-required-by-contracts)
- [Exporting the crawl](#exporting-the-crawl)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's credits meet one of its two required credits, so you can see how a missing one is flagged.

## What it does

- **Drafts credits from your project.** On a project with no credits yet, **Draft credits from the project** groups people by their role, with key creatives first. It lists interview subjects and contributors under "Featuring", and adds music and archival blocks, any required wording, and a copyright line.
- **Keeps credits in order.** Each entry is a credit (a line with names under it), a heading, a block of text, or a music or archival block. Move entries up and down; edit or remove them.
- **Uses the people in your project.** Check people from the project for a credit, and type other names, such as organizations for special thanks. Names follow the project, so fixing a spelling in one place fixes it everywhere.
- **Shows who isn't credited.** Anyone in the project who isn't in a credit is listed. Add them in one click (to a credit with their role, if there is one), or mark them as not credited.
- **Shows the crawl as it plays.** The preview is white on black, centered, like the screen. **Play crawl** rolls it, and you can stop it any time. With reduced motion turned on, it doesn't roll.
- **Prints** the credits for proofreading, with any missing required credits listed at the top.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files. Nested values stay as JSON inside their cell.

## Music and archival credits

Music and archival blocks are built from the project each time, so they stay current as the clearance log and cue sheet change.

- **Music** lists each song or cue once, however many times it's used: the title, written by (composers and authors from the music cue sheet), arranged by, performed by (the artist) and published by (publishers with their society). Music marked "Replace or cut" in the clearance log is left out. Uncheck original score cues and credit the composer instead.
- **Archival** lists the rights holders of licensed, fair use and public domain archival footage, stills, artwork and quotes, once each. Where the rights holder is "Public domain", it uses the source instead. Uncheck any you'd rather credit another way.

## Credits required by contracts

Licenses and agreements often spell out an on-screen credit. Add each one under **Required by contracts**: pick the contract, or name a new license and the clearance log item it covers, and type the wording exactly as the contract gives it.

The tool checks the credits for that wording, ignoring capitals and punctuation. A credit line and its names count as one line ("Director of photography / Teo Ramirez" meets "Director of photography: Teo Ramirez"), and so does a heading with the credit right under it. Anything missing is flagged in red, with **Add to credits** to append the exact wording. It's also listed at the top of the printout.

## Exporting the crawl

**Export text** gives you the crawl as plain text, to download as a `.txt` file or copy:

- **Credit above names:** each credit line, its names below, and a blank line between credits.
- **Two columns, separated by a tab:** the credit and the first name on one line, more names below with an empty first column. This pastes into a spreadsheet or a two-column title template.

For anyone who doesn't use the tool, there's a blank [end credits template](../../templates/end-credits-template.docx) in Word, with a table of required credits to tick off, and a two-column [spreadsheet version](../../templates/end-credits-template.csv).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `credits` object with an ordered `entries` list and an optional `notCredited` list of people left out on purpose. Each entry has an `id` and a `kind`:

| `kind` | Fields |
| --- | --- |
| `credit` | `role` (the line above the names), `personIds`, and `names` for anyone not in the project |
| `heading` | `text` |
| `text` | `text`, shown line by line |
| `music` | `heading`, and `excluded` song keys |
| `archival` | `heading`, and `excluded` source keys |

Contracts can carry a `requiredCredit` with the exact wording they require. A new license added from this tool is a contract with `type` "license", linked to its clearance log item through `thirdPartyElementIds`, and the item records it in `contractIds`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Opening titles and the order of credits within a heading by billing
- Crawl formats for specific titling tools and crawl services
- Checking where a required credit appears (opening titles or end credits) and its size, not just its wording

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
