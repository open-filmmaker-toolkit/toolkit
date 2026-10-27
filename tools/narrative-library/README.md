<p align="center">
  <b>Your grant application answers, in every length funders ask for, with a count as you write.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Grant narrative library

Keep the answers grant applications ask for again and again, such as the logline, synopsis, impact statement, budget narrative and bios, each in the lengths funders ask for. Pull a set together for one application, copy it in, and keep a note of who got which version.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#47](https://github.com/open-filmmaker-toolkit/toolkit/issues/47).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's answers and funders are made up.

## What it does

- **Keeps each answer in versions by length,** such as a 25-word and a 150-character logline. Each version has a limit in words or characters, and a name if the length isn't enough to tell them apart.
- **Counts as you write.** The count shows against the limit, in red with how far over when it's too long, along with the other count. Characters include spaces, the way most application forms count them.
- **Starts a new version from the longest one,** so you can cut it down to the new length.
- **Starts from the treatment.** If the [treatment builder](../treatment-builder/) has a logline, synopsis, approach, access or why-now section that isn't in the library yet, add it in one click.
- **Pulls together the answers for one application.** Pick an application from the [grant calendar](../grant-calendar/), or type a funder that isn't in it, then choose a version of each answer. Copy the set, or download it as a text file.
- **Notes who got which version, and when.** Noting a set as sent records the funder and date on each version. Each version lists where it went, and the side panel shows what was sent most recently. Versions linked from the grant calendar show here too.
- **Exports CSV and prints** every answer with its versions, counts and where each was sent. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [Word template](../../templates/grant-narrative-library-template.docx) with the usual answers and lengths.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `narratives` list. Each answer has an `id`, a `title`, `versions` and optional `notes`. Each version has an `id`, a `unit` (`words` or `characters`), and optional `limit`, `label`, `text`, `updated` (the date the text last changed) and `uses`. Each use has a `date` and either a `grantId`, pointing to a grant in the grant calendar's `grants`, or a `funder` name. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Comparing two versions side by side
- Answers in more than one language
- Funder-specific prompts saved with each application
- Spell check beyond what your browser does

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
