<p align="center">
  <b>A pitch deck or lookbook built from your project and your own stills, laid out for screen or print.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Pitch deck builder

Put together a pitch deck or lookbook: title and logline, story, characters, the look, team, comparable films, the ask and contact. Start from what's already in your project, add your stills, rework each slide, and print to PDF in widescreen for screens or letter for a printed lookbook.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#45](https://github.com/open-filmmaker-toolkit/toolkit/issues/45).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Images](#images)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. Its images are made-up illustrations.

## What it does

- **Starts from the project.** **Start from the project** drafts eight slides: title and logline, the story and characters from the [treatment builder](../treatment-builder/), the look, the team, comps, the ask and contact. Bracketed text marks what's left to write.
- **Kinds of slide:** title and logline (with a background image), text with an image on either side, the look (a grid of up to six images), a full-page image with a caption, team, and comps.
- **Team and comps follow the project.** The team slide lists the crew in your project with their roles. The comps slide shows the comps ticked "In the pitch" in the [comps tracker](../comps-tracker/), with one sourced figure each and the source as a note. Change them there and the slides follow.
- **Arranges the deck.** Move slides up and down, edit them, or leave a slide out without deleting it.
- **Prints to PDF** with one slide per page, at 13.33 × 7.5 inches for widescreen or 11 × 8.5 inches for letter. Choose **Save as PDF** in the print dialog.
- **Exports project data.** Save project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [Word outline](../../templates/pitch-deck-template.docx) with the same slides.

## Images

**Add images** takes stills and reference images from your computer. Each one is resized to 1,600 pixels on its longest side and kept inside the project file, so the deck opens the same in any browser and nothing is uploaded. A dozen images adds a few megabytes to the project file. Use stills you have the rights to show, and check what the people in them agreed to.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `pitchDeck` object:

- `size`: `widescreen` or `letter`.
- `slides`: in order, each with an `id` and a `kind` (`title`, `text`, `look`, `image`, `team` or `comps`), and optional `heading`, `body`, `layout` (`left` or `right`, for text slides), `imageIds` and `hidden`. Team and comps slides are built from `people` and `comps` each time.
- `images`: each with an `id`, `name`, `width`, `height` and `data`, the resized image as a data URL.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Themes, fonts and colors to choose from
- Export to PowerPoint or Keynote
- Slides with video or a link to a trailer

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
