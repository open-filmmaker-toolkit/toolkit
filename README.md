<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg" />
    <img alt="Open Filmmaker Toolkit" src="docs/assets/logo.svg" width="340" />
  </picture>
</p>

<p align="center">
  <b>Free tools for the paperwork behind a documentary. No accounts, no cloud, no subscriptions.</b>
</p>

<p align="center">
  <a href="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/dco.yml"><img alt="DCO" src="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/dco.yml/badge.svg" /></a>
  <img alt="Status: pre-launch" src="https://img.shields.io/badge/status-pre--launch-d29922" />
  <a href="#licenses"><img alt="License: GPL-3.0 and CC BY-SA 4.0" src="https://img.shields.io/badge/license-GPL--3.0%20%7C%20CC%20BY--SA%204.0-blue" /></a>
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="No tracking" src="https://img.shields.io/badge/privacy-no%20tracking-8A2BE2" />
</p>

# Open Filmmaker Toolkit

Free, open-source tools and templates for documentary and independent narrative filmmakers. Open a tool in your browser, load your project file, and keep working: your data never leaves your computer.

![One project file shared by the clearance log and the music cue sheet](docs/assets/demo-preview.svg)

> **Status:** Pre-launch. This repository is private until we launch. Curious where this is headed? See the [**Roadmap**](ROADMAP.md).

## Contents

- [Quick start](#quick-start)
- [What this is](#what-this-is)
- [The tools](#the-tools)
- [How our tools work](#how-our-tools-work)
- [Shared project file](#shared-project-file)
- [Who it's for](#whos-it-for)
- [Repository layout](#repository-layout)
- [Validation](#validation)
- [Licenses](#licenses)
- [Not legal advice](#not-legal-advice)
- [Maintainers](#maintainers)
- [Contributing](#contributing)

## Quick start

1. Clone the repo:
   ```bash
   git clone https://github.com/open-filmmaker-toolkit/toolkit.git
   ```
2. Open [`tools/clearance-log/index.html`](tools/clearance-log/index.html) in Chrome, Edge, Firefox or Safari.
3. Click **Open file** and choose [`samples/the-river-keeps.oft.json`](samples/the-river-keeps.oft.json).
4. Make a change, then save. The same file opens in the [music cue sheet](tools/music-cue-sheet/index.html).

That's it. No install, no build step, no account. Each tool is one self-contained HTML file.

## What this is

The toolkit has two halves:

1. **A directory of open-source tools that already exist,** sorted by production phase, so filmmakers don't pay for what's already free. See [TOOLS.md](TOOLS.md).
2. **Tools we build to fill the gaps,** especially the paperwork that runs on hand-built spreadsheets today: clearances, releases, rights, funding and impact.

## The tools

| Tool | Use it for | Status |
| --- | --- | --- |
| [Clearance log](tools/clearance-log/) | Tracking every piece of third-party material until it's cleared, then printing a report for your E&O attorney | First version |
| [Music cue sheet](tools/music-cue-sheet/) | Building the music cue sheet your distributor or broadcaster needs, from the music already in your clearance log | First version |
| [Call sheet](tools/call-sheet/) | Building shoot-day call sheets from the people and locations in your project; weather lookup is optional and off until you click it | First version |
| [Release tracker](tools/release-tracker/) | Tracking who signed what: appearance, location and materials releases, with the signed copies, and flagging anyone on camera with no release on file | First version |
| [Credits builder](tools/credits-builder/) | Building end credits from the people, music and archival material in your project, checking that every credit your contracts require is there, and exporting the crawl as text | First version |

Everything else we plan to build is listed by production phase in [TOOLS.md](TOOLS.md#part-2-built-here).

## How our tools work

- **Forever free.** No subscriptions, no paid tiers, no "pro" version.
- **Local-first.** Every tool runs in your browser or on your own machine. No accounts and no cloud. Your project data never leaves your computer.
- **Works offline.** Tools can be installed from the browser and used on set with no signal.
- **One shared project file.** All tools read and write the same project: people, locations, third-party elements, contracts. Enter a person once in the release tracker and they show up in your credits, clearance log and chain-of-title binder.
- **Your file, your copy.** Projects save as a file on disk that you back up and share however you already do (Drive, Dropbox, a hard drive).
- **Plain templates too.** Every tool also has a blank spreadsheet or Word [template](templates/) for people who never open the app.

## Shared project file

Tools share a local `.oft.json` project file. Its version 1 format is described by the [JSON Schema](schemas/project-v1.schema.json), with the [data model notes](schemas/README.md) and a [sample project](samples/the-river-keeps.oft.json). Tools preserve fields they do not own when saving.

## Who it's for

Documentary and independent narrative filmmakers, producers, coordinators and ADs working without a studio's back office.

## Repository layout

```text
toolkit/
|-- tools/                # One folder per tool: index.html plus its own README
|   |-- clearance-log/
|   |-- music-cue-sheet/
|   |-- call-sheet/
|   |-- release-tracker/
|   `-- credits-builder/
|-- schemas/              # JSON Schema and data model notes for the project file
|-- samples/              # Fictional sample project to try the tools with
|-- templates/            # Blank templates for people who don't use the tools
|-- tests/                # Browser tests CI runs in Chromium
|-- docs/assets/          # Logo and preview artwork
|-- .github/
|   |-- workflows/        # DCO and CI checks
|   `-- scripts/          # validate_repo.py, the check CI runs
|-- TOOLS.md              # Directory of existing open-source tools, plus what we build
|-- ROADMAP.md            # Milestones, each linked to its issue
|-- GOVERNANCE.md         # How decisions get made
|-- CONTRIBUTING.md       # How to contribute, DCO sign-off, CI practices
`-- README.md             # This page
```

## Validation

CI checks the project schema against the sample files, that IDs and references in samples resolve, that every tool has a README and makes no network requests, and that templates are plain spreadsheets or Word files with no macros or external links. Run the same check locally:

```bash
python3 -m pip install jsonschema
python3 .github/scripts/validate_repo.py
```

CI also runs [browser tests](tests/browser_tools.py) in Chromium: opening and saving the sample, CSV exports, the save-conflict warning, phone width, dark mode and print layout. A second run turns off Chromium's file access, to test the download-and-upload saving that Firefox and Safari use. CI doesn't run Firefox or Safari themselves, and it can't judge look and feel or drive a real printer or phone. Those checks are manual: see [Before you open a pull request](CONTRIBUTING.md#before-you-open-a-pull-request).

## Licenses

Copyright © 2026 the Open Filmmaker Toolkit contributors. Contributors keep the copyright to their work and share it under these licenses:

| What | Where | License |
| --- | --- | --- |
| Code | The tools, project schema, sample project, tests and CI scripts | [GPL-3.0-or-later](LICENSE) |
| Templates, guides and documentation | `templates/` (except legal forms), `docs/`, and the README and other Markdown files | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Legal forms, such as releases and deal memos | `templates/legal-forms/`, once we add them | [CC0 1.0](LICENSES/CC0-1.0.txt): no rights reserved, so you can turn a form into your own contract without crediting us |

If we ever run a tool as a hosted service, that code will be under AGPL-3.0.

## Not legal advice

The templates and forms in this toolkit are general starting points, and the tools are working records. None of it is legal advice. No lawyer has reviewed any of it for your film or where you work, and laws differ from place to place. Have a lawyer licensed where you work review any release, contract or other legal document before you use it. You use the toolkit at your own risk. It's provided "as is," without warranty of any kind, and the maintainers and contributors aren't liable for any loss or claim that comes from using it. The licenses say the same in their own terms.

## Maintainers

- Basil Shadid
- Alex Perrault

See [GOVERNANCE.md](GOVERNANCE.md) for how decisions get made.

## Contributing

You don't need to code to help. Request a tool, submit a template or report a problem from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose). Code contributions are signed off under the Developer Certificate of Origin. See [CONTRIBUTING.md](CONTRIBUTING.md) for both, and our [code of conduct](CODE_OF_CONDUCT.md).
