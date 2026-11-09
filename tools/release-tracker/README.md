<p align="center">
  <b>Who signed what: appearance, location and materials releases, tied to the people and places in your project.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Release tracker

Log every release as it comes in, link it to the people and locations it covers, attach the signed copy, and see at a glance who's on camera without a release on file.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#17](https://github.com/open-filmmaker-toolkit/toolkit/issues/17).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Who needs a release](#who-needs-a-release)
- [Signed copies](#signed-copies)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample has a signed release, two waiting for signature, and a person and a location with nothing on file.

## What it does

- **Shows coverage.** Everyone on camera and every location filmed is listed like a sign-in sheet: signed (with the date), waiting for signature, expired, declined, or no release on file. The ones that still need a signed release come first. Click a line to open its release, or to start one if there's nothing on file.
- **Logs releases.** Appearance, location, materials, group or other releases, each with a status (waiting for signature, signed or declined), the date signed, an optional expiry date, and notes.
- **Links each release** to the people and locations in your project, and, for materials releases, to the photos, home movies or documents in your clearance log. Add a person or location without leaving the release.
- **Attaches the signed copy** (see below).
- **Says which footage a release covers,** when it covers only part of what you shot: a card from the [camera and sound reports](../camera-sound-reports/), a clip on it, timecodes and a note.
- **Group releases and crowd notices.** A group release covers several people on one sign-in sheet. A crowd notice records where you posted a notice of filming, for how many people and on which shoot days. It's kept with the releases but doesn't count as anyone's own release.
- **Prints blank forms** to sign: an appearance, location or materials release, a group sign-in sheet with as many lines as you need, or a crowd notice to post. Each starts with sample wording, which isn't legal advice: replace it with wording your attorney has approved, and the tool keeps yours for next time. Pick a person or place to fill in their name.
- **Finds things.** Search, and filter by status or by releases with no scan attached.
- **Prints a release report** for your E&O attorney: what still needs a signed release, everyone and everywhere on camera with their release, and every release with its scan.
- **Exports releases (CSV),** one row per release. The blank [release log spreadsheet](../../templates/release-log-template.csv) has the same columns, and the [Word version](../../templates/release-log-template.docx) adds an on-camera list to fill in on set, for anyone who doesn't use the tool.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files. Nested values stay as JSON inside their cell.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/release-log-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **The same release status shows in other tools:** the [clearance log](../clearance-log/) shows it for the people and places in each element, and the [call sheet](../call-sheet/) for the people working each day and the location.

## Who needs a release

**Choose who and where is on camera** lists everyone and everywhere in your project. Checked people and locations need a release.

- A person or location you add from this tool is marked as on camera.
- Saving an appearance release marks the people it covers as on camera. Saving a location release marks its locations as filmed.
- A location on a call sheet counts as filmed unless you uncheck it.
- Unchecking someone takes them off the list, even if a release or call sheet names them.

A person is covered by a signed appearance or other release that hasn't expired, and a location by a signed location or other release. A materials release covers someone's photos or documents, not their appearance on camera. A declined release is flagged in red: don't use footage of the people or places it names.

## Signed copies

**Attach a scan** adds a PDF or image of the signed release.

- **Chrome and Edge:** click **Connect project folder** and choose the folder your project file is in. When you save the release, the scan is copied into a `releases` folder there, and you can open it from the tool. Nothing is uploaded anywhere.
- **Firefox, Safari, or without connecting a folder:** the tool records the scan's name as `releases/<file name>`. Put the file in a `releases` folder next to your project file so the link stays right.

Removing a scan from a release doesn't delete the file.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Releases are entries in `contracts` whose `type` contains "release": `appearance release`, `location release`, `materials release`, `group release` or `other release`, and crowd notices, with `type` `crowd notice` and optional `postedAt`, `crowdSize` and `shootDayIds`. Each has a `title`, a `status` of `pending`, `signed` or `declined`, and optionally `signedDate`, `expirationDate` (YYYY-MM-DD), `notes`, and the `personIds`, `locationIds`, `thirdPartyElementIds` and `assetIds` it covers, and `footage` (each with an optional `mediaReportId`, `clipId`, `tcIn`, `tcOut` and `note`).

Scans are entries in `assets` with `type` "release scan" and a `relativePath` relative to the project file. People and locations can carry `onCamera: true` or `false`. A materials release's link to clearance-log items is also recorded on each item as `contractIds`.

Your own wording for blank forms is kept in `releaseForms`, by `appearance`, `location`, `materials`, `group` and `crowd`. Other contracts, such as music licenses, are kept as they are and don't appear in this tool. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Signing releases on a phone or tablet

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses). This tool is a working record, not legal advice: see [Not legal advice](../../README.md#not-legal-advice).
