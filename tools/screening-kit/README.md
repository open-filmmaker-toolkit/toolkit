<p align="center">
  <b>Everything a host needs to screen the film.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Screening kit builder

Put together a kit for the people hosting a screening: about the film, how to host it, the tech specs, how to promote it, the discussion, and a checklist for the weeks before. Print it, or save it as a PDF to send.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#92](https://github.com/open-filmmaker-toolkit/toolkit/issues/92).

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

- **About the film** from the [EPK and press notes builder](../press-notes/) or the [treatment](../treatment-builder/): the logline, synopsis and running time.
- **Hosting the screening** and **promotion,** with our wording to start from, and approved stills and key art from the [stills library](../stills-library/).
- **Tech specs:** the formats you can send (DCP, Blu-ray, a file or link, DVD) and playback notes.
- **The discussion** from the [discussion guide builder](../discussion-guide/): themes, questions, resources and partner organizations.
- **A host checklist** by when: four weeks before, two weeks, the week before, the day and afterward, including sending you the attendance for the [impact report](../impact-report/). Remove items or add your own.
- **A kit for each host.** Pick a partner from the [partner CRM](../partner-crm/) or a venue from [bookings](../bookings/) under **Kit for**. Add a note for that host, and change any of hosting, tech specs, promotion or contact for them only; everything else comes from the kit for every host. The print is headed with the host's name.
- **Prints the kit,** with the checklist on its own page.
- **Kits in other languages.** Choose a language next to **Print the kit**, for all hosts or for one. The headings, checklist and our starting wording print in that language; what you write prints as you wrote it. See [translations](../../translations/README.md) for the languages there are.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `screeningKit` record: `hosting`, `tech`, `promotion` and `contact` text, `formats`, `imageIds` (approved stills and key art), `checklist` (your own items, with `when` and `text`), `removed` (built-in items taken out), `hidden` (sections left out) and `hosts`: for each host, by `partner:` or `booking:` and its id, a `note` and any of `hosting`, `tech`, `promotion` and `contact` that differ from the kit for every host.

It reads `pressNotes`, `treatment`, `discussionGuide`, `partners` and `assets`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Sending the kit by email (the toolkit never connects to the internet)

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
