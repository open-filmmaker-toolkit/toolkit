<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo-dark.svg" />
    <img alt="Open Filmmaker Toolkit" src="docs/assets/logo.svg" width="340" />
  </picture>
</p>

<p align="center">
  <b>Free tools for the paperwork behind a documentary or independent film. No accounts, no cloud, no subscriptions.</b>
</p>

<p align="center">
  <a href="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/ci.yml/badge.svg" /></a>
  <a href="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/dco.yml"><img alt="DCO" src="https://github.com/open-filmmaker-toolkit/toolkit/actions/workflows/dco.yml/badge.svg" /></a>
  <img alt="Status: early release" src="https://img.shields.io/badge/status-early%20release-d29922" />
  <a href="#licenses"><img alt="License: GPL-3.0 and CC BY-SA 4.0" src="https://img.shields.io/badge/license-GPL--3.0%20%7C%20CC%20BY--SA%204.0-blue" /></a>
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="No tracking" src="https://img.shields.io/badge/privacy-no%20tracking-8A2BE2" />
</p>

# Open Filmmaker Toolkit

Free, open-source tools and templates for documentary and independent narrative filmmakers. Open a tool in your browser, load your project file, and keep working: your data never leaves your computer.

![One project file shared by the clearance log and the music cue sheet](docs/assets/demo-preview.svg)

> **Status:** Early release. Every tool is a first version, so expect rough edges, and tell us what's broken or missing from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose). Where it's headed: the [**Roadmap**](ROADMAP.md).

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

The easiest way in is the [toolkit's home page](https://open-filmmaker-toolkit.github.io/toolkit/): every tool, by stage of production, with how they connect. Click a tool to use it in your browser.

To use the tools offline, or to work on them:

1. Clone the repo, or [download it as a ZIP](https://github.com/open-filmmaker-toolkit/toolkit/archive/refs/heads/main.zip):
   ```bash
   git clone https://github.com/open-filmmaker-toolkit/toolkit.git
   ```
2. Open [`tools/clearance-log/index.html`](tools/clearance-log/index.html) in Chrome, Edge, Firefox or Safari.
3. Click **Open file** and choose [`samples/the-river-keeps.oft.json`](samples/the-river-keeps.oft.json).
4. Make a change, then save. The same file opens in the [music cue sheet](tools/music-cue-sheet/index.html).

That's it. No install, no build step, no account. Each tool is one self-contained HTML file. Open [`index.html`](index.html) for the home page, which works offline too.

## What this is

The toolkit has two halves:

1. **Tools we build to fill the gaps,** especially the paperwork that runs on hand-built spreadsheets today: clearances, releases, rights, funding and impact. All of them, built and planned, are listed by production phase in [TOOLS.md](TOOLS.md).
2. **A directory of other people's open-source tools,** sorted by production phase, so filmmakers don't pay for what's already free. See [Other open-source tools](docs/other-tools.md), also linked from the home page.

## The tools

| Tool | Phase | Use it for |
| --- | --- | --- |
| [Subject tracker](tools/subject-tracker/) | Development | Keep track of the people you might film, and when to follow up. |
| [Research and archival log](tools/research-log/) | Development | Write down archival leads and sources as you find them. |
| [Comps tracker](tools/comps-tracker/) | Development | Comparable films for your pitch, with where every number came from. |
| [Treatment builder](tools/treatment-builder/) | Development | Write your treatment a section at a time, with word counts. |
| [Pitch deck builder](tools/pitch-deck/) | Development | Make a pitch deck or lookbook from your project and your own stills. |
| [Grant calendar](tools/grant-calendar/) | Funding | Every grant deadline in one place, and what each application needs. |
| [Grant narrative library](tools/narrative-library/) | Funding | Your application answers, in every length funders ask for. |
| [Budget converter](tools/budget-converter/) | Funding | Put your budget into the categories a funder wants. |
| [Finance plan](tools/finance-plan/) | Funding | How the film gets paid for, and how much you still need to raise. |
| [Funder CRM](tools/funder-crm/) | Funding | Who you know at each funder, and what you said you'd do next. |
| [Budget](tools/budget/) | Pre-production | A real production budget, from detail lines up to the top sheet. |
| [Cash flow](tools/cash-flow/) | Pre-production | When money goes out and comes in, and the months you'll run short. |
| [Shooting calendar](tools/shooting-calendar/) | Pre-production | Shoot days, travel days and holds, with who's needed where. |
| [Interview prep](tools/interview-prep/) | Pre-production | Research and questions for each interview, on one page you can print. |
| [Location scout sheet](tools/location-scout/) | Pre-production | What you found on a scout, with photos, for the rest of the crew. |
| [Deal memos](tools/deal-memos/) | Pre-production | Crew deal memos to print and sign, with the rates sent to the budget. |
| [Gear list](tools/gear-list/) | Pre-production | What gear you're bringing, where it's from, and what goes out each day. |
| [COI and permit tracker](tools/coi-permit-tracker/) | Pre-production | Insurance certificates and permits, and what's still missing before each shoot day. |
| [Travel sheet](tools/travel-sheet/) | Pre-production | Flights, hotels and who to call, on one sheet for everyone on the trip. |
| [Risk and hostile-environment plans](tools/risk-plan/) | Pre-production | What could go wrong on a shoot, and the plan if it does. |
| [Security checklist](tools/security-checklist/) | Pre-production | Keep footage, sources and devices safe on a sensitive shoot. |
| [Call sheet](tools/call-sheet/) | Production | Call sheets built from the people and places already in your project. |
| [Camera and sound reports](tools/camera-sound-reports/) | Production | What's on every camera and sound card, for the shoot and the edit. |
| [Interview log](tools/interview-log/) | Production | Who you interviewed, which cards it's on, and the moments worth finding again. |
| [Daily production report](tools/daily-production-report/) | Production | What happened each shoot day: the hours, what you got, and what went wrong. |
| [Expense log](tools/expense-log/) | Production | Log what you spend against the budget, and keep the receipts. |
| [Festival submission tracker](tools/festival-submissions/) | Launch | Festival deadlines, fees, results and screenings. |
| [Release tracker](tools/release-tracker/) | Production | Who's signed what, and who's on camera without a release. |
| [Field journal](tools/field-journal/) | Production | A dated journal of the production, tied to the people and places in it. |
| [Footage log](tools/footage-log/) | Post-production | Every clip, what's in it and who's in it, so the editor can find it. |
| [Paper edit](tools/paper-edit/) | Post-production | Pick bites from transcripts, build scenes, and send an edit list to your editing app. |
| [Structure board](tools/structure-board/) | Post-production | Scene cards you can move around until the structure works. |
| [Cut version tracker](tools/cut-tracker/) | Post-production | Each cut, who saw it, and what happened to their notes. |
| [Name supers list](tools/name-supers/) | Post-production | On-screen names and titles, spelled right and kept up to date. |
| [Music cue sheet](tools/music-cue-sheet/) | Post-production | The cue sheet your distributor needs, built from your clearance log. |
| [Credits builder](tools/credits-builder/) | Post-production | End credits from your project, with every credit your contracts require checked. |
| [Budget-to-actuals](tools/budget-to-actuals/) | Post-production | What you've spent against the budget, line by line. |
| [Clearance log](tools/clearance-log/) | Legal and clearances | Every bit of third-party material in the film, until it's cleared. |
| [Fair use log](tools/fair-use-log/) | Legal and clearances | Your fair use reasoning, written down for your attorney. |
| [License tracker](tools/license-tracker/) | Legal and clearances | What each license covers, what you still owe, and when it runs out. |
| [Annotated-transcript clearance report](tools/clearance-report/) | Legal and clearances | The annotated script your E&O insurer asks for. |
| [Chain-of-title binder](tools/chain-of-title/) | Legal and clearances | The rights documents a distributor wants, with the gaps showing. |
| [Press list](tools/press-list/) | Marketing and festivals | Press contacts, the screeners you sent, and the coverage you got. |
| [Partner CRM](tools/partner-crm/) | Impact and outreach | Impact partners, what they've committed to, and the screenings you've done together. |
| [Discussion guide builder](tools/discussion-guide/) | Impact and outreach | A handout for screenings, with discussion questions and resources. |
| [Archive log](tools/archive-log/) | Close-out and archive | Where every copy of your project lives, and when you last checked it. |

All 46 are first versions: they work, and they're still changing. Everything else we plan to build is listed by production phase in [TOOLS.md](TOOLS.md).

## How our tools work

- **Forever free.** No subscriptions, no paid tiers, no "pro" version.
- **Local-first.** Every tool runs in your browser or on your own machine. No accounts and no cloud. Your project data never leaves your computer.
- **Works offline.** Each tool is one HTML file. Keep a copy on your laptop and it works on set with no signal.
- **One shared project file.** All tools read and write the same project. Add a person once and they show up in your call sheets, releases, name supers and credits; log an archival clip once and it flows from the research log to the clearance log to the credits.
- **Your file, your copy.** Projects save as a file on disk that you back up and share however you already do (Drive, Dropbox, a hard drive).
- **Plain templates too.** Most tools also have a blank spreadsheet or Word [template](templates/) for people who'd rather not use the tool.

## Shared project file

Tools share a local `.oft.json` project file. Its version 1 format is described by the [JSON Schema](schemas/project-v1.schema.json), with the [data model notes](schemas/README.md) and a [sample project](samples/the-river-keeps.oft.json). Tools preserve fields they do not own when saving.

## Who it's for

Documentary and independent narrative filmmakers, producers, coordinators and ADs working without a studio's back office.

## Repository layout

```text
toolkit/
|-- index.html            # The home page: every tool by stage, how they connect, search
|-- tools/                # One folder per tool: index.html plus its own README
|-- schemas/              # JSON Schema and data model notes for the project file
|-- samples/              # Fictional sample project to try the tools with
|-- templates/            # Blank templates for people who don't use the tools
|-- tests/                # Browser tests CI runs in Chromium
|-- docs/                 # Directory of other open-source tools; logo and artwork in docs/assets/
|-- .github/
|   |-- workflows/        # DCO and CI checks
|   `-- scripts/          # validate_repo.py, the check CI runs
|-- TOOLS.md              # Every tool we build or plan to, by production phase
|-- ROADMAP.md            # Milestones, each linked to its issue
|-- GOVERNANCE.md         # How decisions get made
|-- CONTRIBUTING.md       # How to contribute, DCO sign-off, CI practices
`-- README.md             # This page
```

## Validation

CI checks the project schema against the sample files, that IDs and references in samples resolve, that every tool has a README and makes no network requests, that the home page lists every tool just as TOOLS.md does, and that templates are plain spreadsheets or Word files with no macros or external links. Run the same check locally:

```bash
python3 -m pip install jsonschema
python3 .github/scripts/validate_repo.py
```

CI also runs [browser tests](tests/browser_tools.py) in Chromium: opening and saving the sample, CSV exports, the save-conflict warning, phone width, dark mode and print layout. A second run turns off Chromium's file access, to test the download-and-upload saving that Firefox and Safari use. A weekly check runs the basics in the real Firefox and Safari. CI can't judge look and feel or drive a real printer or phone. Those checks are manual: see [Before you open a pull request](CONTRIBUTING.md#before-you-open-a-pull-request).

## Licenses

Copyright © 2026 the Open Filmmaker Toolkit contributors. Contributors keep the copyright to their work and share it under these licenses:

| What | Where | License |
| --- | --- | --- |
| Code | The tools, project schema, sample project, tests and CI scripts | [GPL-3.0-or-later](LICENSE) |
| Templates, guides and documentation | `templates/` (except legal forms), `docs/`, and the README and other Markdown files | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Legal forms, such as releases and deal memos | `templates/legal-forms/` | [CC0 1.0](LICENSES/CC0-1.0.txt): no rights reserved, so you can turn a form into your own contract without crediting us |

If we ever run a tool as a hosted service, that code will be under AGPL-3.0.

## Not legal advice

The templates and forms in this toolkit are general starting points, and the tools are working records. None of it is legal advice. No lawyer has reviewed any of it for your film or where you work, and laws differ from place to place. Have a lawyer licensed where you work review any release, contract or other legal document before you use it. You use the toolkit at your own risk. It's provided "as is," without warranty of any kind, and the maintainers and contributors aren't liable for any loss or claim that comes from using it. The licenses say the same in their own terms.

## Maintainers

- Basil Shadid
- Alex Perrault

See [GOVERNANCE.md](GOVERNANCE.md) for how decisions get made.

## Contributing

You don't need to code to help. Request a tool, submit a template or report a problem from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose). Code contributions are signed off under the Developer Certificate of Origin. See [CONTRIBUTING.md](CONTRIBUTING.md) for both, and our [code of conduct](CODE_OF_CONDUCT.md).
