<p align="center">
  <b>Press notes from your project, ready to print.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# EPK and press notes builder

Build press notes, the core of an electronic press kit, in the usual order: logline, synopses, director's statement, the production story, key creatives, credits, festivals, technical details, stills and press contacts. Print them, or save them as a PDF.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#79](https://github.com/open-filmmaker-toolkit/toolkit/issues/79).

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

- **Sections in the usual order,** each marked written, from the project, not done yet or left out.
- **From the project:** the logline and synopses start from the [treatment](../treatment-builder/), credits come from the [credits builder](../credits-builder/), and festivals marked accepted in the [festival submission tracker](../festival-submissions/) are listed with their screenings.
- **Bios are saved with each person,** so other tools can use them. Pick who to include, in order.
- **Stills** from the [stills library](../stills-library/), or added from your computer, resized and kept in the project file, with a caption and photo credit. The first is used on the title page. Taking a still out of the press notes leaves it in the stills library.
- **Press contacts** with role, company, email and phone.
- **Prints** a title page, then each section, with the stills two to a page. Also exports project data as separate CSV files.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `pressNotes` record: `logline`, `shortSynopsis`, `longSynopsis`, `directorStatement`, `aboutProduction`, `bioIds` (people, in order), `stillIds` (assets, in order), `specs` (year, country, language, subtitles, format, aspect ratio and sound), `contacts` and `hidden` (sections left out).

Bios are saved as `bio` on `people`. Stills are `assets` with `type` "still", the image in `data`, and `caption` and `photoCredit`. It reads `treatment`, `credits` and `festivals`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- A downloadable EPK folder with the stills at full size
- Q&A and press quotes sections

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
