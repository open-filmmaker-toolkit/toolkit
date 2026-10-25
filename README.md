# Open Filmmaker Toolkit

Free, open-source tools and templates for documentary and independent narrative filmmakers. Forever free.

> **Status:** Pre-launch. This repository is private while licenses go through legal review. See [ROADMAP.md](ROADMAP.md).

## What this is

The toolkit has two halves:

1. **A directory of open-source tools that already exist,** sorted by production phase, so filmmakers don't pay for what's already free. See [TOOLS.md](TOOLS.md).
2. **Tools we build to fill the gaps,** especially the paperwork that runs on hand-built spreadsheets today: clearances, releases, rights, funding and impact.

## How our tools work

- **Forever free.** No subscriptions, no paid tiers, no "pro" version.
- **Local-first.** Every tool runs in your browser or on your own machine. No accounts and no cloud. Your project data never leaves your computer.
- **Works offline.** Tools can be installed from the browser and used on set with no signal.
- **One shared project file.** All tools read and write the same project: people, locations, third-party elements, contracts. Enter a person once in the release tracker and they show up in your credits, clearance log and chain-of-title binder.
- **Your file, your copy.** Projects save as a file on disk that you back up and share however you already do (Drive, Dropbox, a hard drive).
- **Plain templates too.** Every tool also ships as a DOCX, spreadsheet or PDF template for people who never open the app.

## Shared project file

Tools share a local `.oft.json` project file. Its version 1 format is described by the [JSON Schema](schemas/project-v1.schema.json), with the [data model notes](schemas/README.md) and a [sample project](samples/the-river-keeps.oft.json). Tools preserve fields they do not own when saving.

## Who it's for

Documentary and independent narrative filmmakers, producers, coordinators and ADs working without a studio's back office.

## Licenses

Licensing is under legal review. Our intent:

| What | Planned license |
| --- | --- |
| Code | GPL-3.0 (AGPL-3.0 for anything hosted) |
| Templates and guides | CC BY-SA 4.0 |
| Legal forms (releases, deal memos) | CC0 or CC BY 4.0 |

Legal templates are starting points, not legal advice. Have a lawyer in your jurisdiction review anything you sign.

## Maintainers

- Basil Shadid
- Alex Perrault

See [GOVERNANCE.md](GOVERNANCE.md) for how decisions get made.

## Contributing

You don't need to code to help. Request a tool, submit a template or report a problem from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose). Code contributions are signed off under the Developer Certificate of Origin. See [CONTRIBUTING.md](CONTRIBUTING.md) for both, and our [code of conduct](CODE_OF_CONDUCT.md).
