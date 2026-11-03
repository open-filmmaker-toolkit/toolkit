<p align="center">
  <b>A printable screening guide with your film synopsis, discussion questions, resources, outreach partners and credits.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Discussion guide builder

Prepare a handout for a screening: start with the synopsis and credits in your project, then add themes, questions, resources and organizations that can help audiences take the conversation further. Select organizations from the Partner CRM and print the finished guide to PDF.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#91](https://github.com/open-filmmaker-toolkit/toolkit/issues/91).

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, accounts or network requests. Click **Open file** and choose your `.oft.json` project. The tool starts the synopsis from the treatment's short synopsis, long synopsis or logline, in that order. Edit it for this screening, add themes, discussion questions and resource links, and choose any partner organizations to include. **Print to PDF** opens the browser's print dialog.

Save changes to the shared project file. Chrome and Edge can save directly and warn if the file changed since it was opened. Firefox and Safari download a new copy instead. The project file stays on your computer.

## What it adds to the project file

An optional `discussionGuide` record:

| Field | Purpose |
| --- | --- |
| `synopsis` | Screening-specific synopsis, initially copied from the treatment |
| `themes` | Themes, one per line |
| `questions` | Discussion questions, one per line |
| `resourceNotes` | Audience-facing resources or links, one per line |
| `partnerIds` | Selected organization IDs from the Partner CRM |

Credits and partner organization details are read from their existing project records; they are not duplicated in the guide. Everything else in the project file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Separate guides for different audiences or screenings
- Audience feedback or attendance tracking
- Importing resource lists from outside the project

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
