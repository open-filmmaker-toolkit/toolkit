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

- [x] Verify every tool in the [directory](docs/other-tools.md): license, platforms, last release, still maintained ([#9](https://github.com/open-filmmaker-toolkit/toolkit/issues/9))
- [x] Add a one-line "use it for" note to each entry ([#10](https://github.com/open-filmmaker-toolkit/toolkit/issues/10))
- [x] Remove anything unmaintained or not actually open source ([#11](https://github.com/open-filmmaker-toolkit/toolkit/issues/11))
- [x] Move the directory of other people's tools to [its own page](docs/other-tools.md), so [TOOLS.md](TOOLS.md) lists only the tools we build
- [x] A home page that shows our tools by stage, how they connect, search, and the directory of other tools: [`index.html`](index.html), served by GitHub Pages once Pages is turned on
- [ ] Make the repo public ([#12](https://github.com/open-filmmaker-toolkit/toolkit/issues/12))

## Milestone 2: The shared project file

- [x] Define the data model: people, locations, third-party elements, contracts, assets ([#13](https://github.com/open-filmmaker-toolkit/toolkit/issues/13))
- [x] Publish it as a JSON Schema with a sample project ([#14](https://github.com/open-filmmaker-toolkit/toolkit/issues/14))
- [x] Build save and load to a file on disk, with export to CSV ([#15](https://github.com/open-filmmaker-toolkit/toolkit/issues/15))
- [x] Decide how tools handle a file edited by two people: warn on conflict, with reload, save a copy or explicit overwrite ([#16](https://github.com/open-filmmaker-toolkit/toolkit/issues/16))

## Milestone 3: The clearances core

Three tools on one data model. This is the documentary-specific gap.

- [x] Release tracker: who signed what, linked to the people and locations in the project, with scans stored locally and anyone on camera without a release flagged ([#17](https://github.com/open-filmmaker-toolkit/toolkit/issues/17)). Linking to specific footage is listed under the tool's "Not yet"
- [x] Clearance log (E&O log): every third-party element, its source, license status and cost ([#18](https://github.com/open-filmmaker-toolkit/toolkit/issues/18))
- [x] Music cue sheet: built from the music in the clearance log, with credits, share checks and a printable sheet ([#24](https://github.com/open-filmmaker-toolkit/toolkit/issues/24))
- [x] Credits builder: pulls names and roles from the project, adds music and archival credits from the clearance log and cue sheet, flags contractually required credits, and exports the crawl as text ([#19](https://github.com/open-filmmaker-toolkit/toolkit/issues/19))
- [x] Plain template versions ([#20](https://github.com/open-filmmaker-toolkit/toolkit/issues/20)): a spreadsheet and a Word document for the release tracker, clearance log and credits builder, plus the music cue sheet, in [templates](templates/)

## Milestone 4: Call sheet generator

- [x] Call sheet built from the project's people and locations ([#21](https://github.com/open-filmmaker-toolkit/toolkit/issues/21)), first version with optional online weather lookup
- [x] Plain template version ([#22](https://github.com/open-filmmaker-toolkit/toolkit/issues/22)): spreadsheet export and a blank [template](templates/call-sheet-template.csv). Printing to PDF works from the browser's print dialog
- [ ] Import an Analyze Video report (timestamps and frames) into a project's footage log or research notes. This lives in the [Analyze-Video-Skill repo](https://github.com/evillollive/Analyze-Video-Skill) ([tracked there](https://github.com/evillollive/Analyze-Video-Skill/issues/22)), not here: it writes a project file the toolkit tools already read

## Milestone 5: The hub

The home page becomes a place to work, not just a list. Each step gets an issue before work starts.

- [x] First version: every tool by stage and phase, workflows that show how the tools connect, search, and planned tools linked to their issues
- [ ] Open a project once in the hub and move between tools without opening and saving the file in each
- [ ] Show what's in the open project, such as "14 cues, no clearance items yet", from the tools' own checks
- [ ] Install the hub as an app for offline use

## Backlog

Everything else in [TOOLS.md](TOOLS.md), prioritized by what contributors ask for. Each planned tool has its own issue in the [Backlog milestone](https://github.com/open-filmmaker-toolkit/toolkit/milestone/6).

- [x] Subject tracker: possible subjects, access status, follow-ups and a contact log, added to the project when they agree ([#41](https://github.com/open-filmmaker-toolkit/toolkit/issues/41))
- [x] Research and archival log: archival leads tracked to ready to license and sent to the clearance log, plus research sources ([#42](https://github.com/open-filmmaker-toolkit/toolkit/issues/42))
- [x] Comps tracker: comparable films with a source for every figure, tags, and a printed comps page ([#43](https://github.com/open-filmmaker-toolkit/toolkit/issues/43))
- [x] Treatment builder: sections with word targets, subjects and team from the project, saved versions to compare, and print, Markdown and text export ([#44](https://github.com/open-filmmaker-toolkit/toolkit/issues/44))
- [x] Pitch deck builder (a pitch deck or lookbook): slides drafted from the project, your own stills kept in the project file, team and comps that follow the project, and print to PDF in widescreen or letter ([#45](https://github.com/open-filmmaker-toolkit/toolkit/issues/45))
- [x] Grant calendar: deadlines, amounts, eligibility, a checklist of materials and status, in list and month views, with a calendar file (.ics) and CSV export, linked to the answers each application used ([#46](https://github.com/open-filmmaker-toolkit/toolkit/issues/46))
- [x] Grant narrative library: answers in versions by word or character limit, counted as you write, pulled together for one application to copy or download, with who got which version and when ([#47](https://github.com/open-filmmaker-toolkit/toolkit/issues/47))
- [x] Budget: detail lines by account with units, rates and fringes, contingency, insurance and fees as percentages, a top sheet that updates as you type, versions to compare, and print and CSV ([#51](https://github.com/open-filmmaker-toolkit/toolkit/issues/51))
- [x] Budget converter: accounts and lines mapped to a funder's categories and saved for next time, unmapped lines and total differences flagged, common formats to start from, format files to reuse, and print and CSV ([#48](https://github.com/open-filmmaker-toolkit/toolkit/issues/48))
- [x] Finance plan: sources with amount, status and terms, grants linked from the grant calendar, totals and the gap against the budget, payments by month, and a printed plan ([#49](https://github.com/open-filmmaker-toolkit/toolkit/issues/49))
- [x] Funder CRM: organizations and the people there, a log of meetings, calls and emails, next steps with the overdue ones first, links to the grant calendar, and CSV ([#50](https://github.com/open-filmmaker-toolkit/toolkit/issues/50))
- [x] Cash flow: budget accounts and lines spread across months or weeks, deferred and in-kind costs left out, income from the finance plan, the running balance with shortfalls flagged, and CSV ([#52](https://github.com/open-filmmaker-toolkit/toolkit/issues/52))
- [x] Shooting calendar: shoot days, travel days and holds in month and list views, linked to people and locations, call sheets started from a day, a calendar file and a printed month view ([#53](https://github.com/open-filmmaker-toolkit/toolkit/issues/53))
- [x] Interview prep: research notes, story beats, questions in order with must-asks marked, linked to the person and the shoot day, and a one-page guide to print ([#54](https://github.com/open-filmmaker-toolkit/toolkit/issues/54))
- [x] Name supers list: names from the project, near-miss spellings flagged, changes since the last export to graphics, CSV export ([#71](https://github.com/open-filmmaker-toolkit/toolkit/issues/71))

Finding a third maintainer is on hold. Basil and Alex maintain the project for now ([#8](https://github.com/open-filmmaker-toolkit/toolkit/issues/8), closed).

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
