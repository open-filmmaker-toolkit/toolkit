# Roadmap

Each milestone below is a [GitHub milestone](https://github.com/open-filmmaker-toolkit/toolkit/milestones), and each item links to its issue.

## Milestone 0: Foundations (private)

- [x] Create the GitHub organization and private repo ([#1](https://github.com/open-filmmaker-toolkit/toolkit/issues/1))
- [x] Write README, ROADMAP, TOOLS and GOVERNANCE ([#2](https://github.com/open-filmmaker-toolkit/toolkit/issues/2))
- [x] Decide the licenses: GPL-3.0-or-later for code, CC BY-SA 4.0 for templates and guides, CC0 for legal forms, with a not-legal-advice notice instead of a lawyer's review ([#3](https://github.com/open-filmmaker-toolkit/toolkit/issues/3))
- [x] Add LICENSE files ([#4](https://github.com/open-filmmaker-toolkit/toolkit/issues/4))
- [x] Write CONTRIBUTING.md with Developer Certificate of Origin (DCO) sign-off ([#5](https://github.com/open-filmmaker-toolkit/toolkit/issues/5))
- [x] Adopt a code of conduct ([#6](https://github.com/open-filmmaker-toolkit/toolkit/issues/6))
- [x] Add issue forms: "Request a tool," "Submit a template," "Report a problem" ([#7](https://github.com/open-filmmaker-toolkit/toolkit/issues/7))

## Milestone 1: The directory (public launch)

- [x] Verify every tool in [TOOLS.md](TOOLS.md): license, platforms, last release, still maintained ([#9](https://github.com/open-filmmaker-toolkit/toolkit/issues/9))
- [x] Add a one-line "use it for" note to each entry ([#10](https://github.com/open-filmmaker-toolkit/toolkit/issues/10))
- [x] Remove anything unmaintained or not actually open source ([#11](https://github.com/open-filmmaker-toolkit/toolkit/issues/11))
- [ ] Make the repo public ([#12](https://github.com/open-filmmaker-toolkit/toolkit/issues/12))

## Milestone 2: The shared project file

- [x] Define the data model: people, locations, third-party elements, contracts, assets ([#13](https://github.com/open-filmmaker-toolkit/toolkit/issues/13))
- [x] Publish it as a JSON Schema with a sample project ([#14](https://github.com/open-filmmaker-toolkit/toolkit/issues/14))
- [x] Build save and load to a file on disk, with export to CSV ([#15](https://github.com/open-filmmaker-toolkit/toolkit/issues/15))
- [x] Decide how tools handle a file edited by two people: warn on conflict, with reload, save a copy or explicit overwrite ([#16](https://github.com/open-filmmaker-toolkit/toolkit/issues/16))

## Milestone 3: The clearances core

Three tools on one data model. This is the documentary-specific gap.

- [x] Release tracker: who signed what, linked to the people and locations in the project, with scans stored locally and anyone on camera without a release flagged ([#17](https://github.com/open-filmmaker-toolkit/toolkit/issues/17)). Linking to specific footage is listed under the tool's "Not yet"
- [x] Clearance / E&O log: every third-party element, its source, license status and cost ([#18](https://github.com/open-filmmaker-toolkit/toolkit/issues/18))
- [x] Music cue sheet: built from the music in the clearance log, with credits, share checks and a printable sheet ([#24](https://github.com/open-filmmaker-toolkit/toolkit/issues/24))
- [x] Credits builder: pulls names and roles from the project, adds music and archival credits from the clearance log and cue sheet, flags contractually required credits, and exports the crawl as text ([#19](https://github.com/open-filmmaker-toolkit/toolkit/issues/19))
- [x] Plain template versions ([#20](https://github.com/open-filmmaker-toolkit/toolkit/issues/20)): a spreadsheet and a Word document for the release tracker, clearance log and credits builder, plus the music cue sheet, in [templates](templates/)

## Milestone 4: Call sheet generator

- [x] Call sheet built from the project's people and locations ([#21](https://github.com/open-filmmaker-toolkit/toolkit/issues/21)), first version with optional online weather lookup
- [x] Plain template version ([#22](https://github.com/open-filmmaker-toolkit/toolkit/issues/22)): spreadsheet export and a blank [template](templates/call-sheet-template.csv). Printing to PDF works from the browser's print dialog
- [ ] Import an Analyze Video report (timestamps and frames) into a project's footage log or research notes. This lives in the [Analyze-Video-Skill repo](https://github.com/evillollive/Analyze-Video-Skill) ([tracked there](https://github.com/evillollive/Analyze-Video-Skill/issues/22)), not here: it writes a project file the toolkit tools already read

## Backlog

Everything else in the "Built here" section of [TOOLS.md](TOOLS.md), prioritized by what contributors ask for. Each planned tool has its own issue in the [Backlog milestone](https://github.com/open-filmmaker-toolkit/toolkit/milestone/6).

- [x] Subject tracker: possible subjects, access status, follow-ups and a contact log, added to the project when they agree ([#41](https://github.com/open-filmmaker-toolkit/toolkit/issues/41))
- [x] Research and archival log: archival leads tracked to ready to license and sent to the clearance log, plus research sources ([#42](https://github.com/open-filmmaker-toolkit/toolkit/issues/42))
- [x] Name supers list: names from the project, near-miss spellings flagged, changes since the last export to graphics, CSV export ([#71](https://github.com/open-filmmaker-toolkit/toolkit/issues/71))

Finding a third maintainer is on hold. Basil and Alex maintain the project for now ([#8](https://github.com/open-filmmaker-toolkit/toolkit/issues/8), closed).

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
