# Roadmap

Each milestone below is a [GitHub milestone](https://github.com/open-filmmaker-toolkit/toolkit/milestones), and each item links to its issue.

## Milestone 0: Foundations (private)

- [x] Create the GitHub organization and private repo (#1)
- [x] Write README, ROADMAP, TOOLS and GOVERNANCE (#2)
- [ ] Lawyer reviews the planned licenses for code, templates and legal forms (#3)
- [ ] Add LICENSE files once approved (#4)
- [x] Write CONTRIBUTING.md with Developer Certificate of Origin (DCO) sign-off (#5)
- [x] Adopt a code of conduct (#6)
- [x] Add issue forms: "Request a tool," "Submit a template," "Report a problem" (#7)
- [ ] Find a third maintainer (#8)

## Milestone 1: The directory (public launch)

- [x] Verify every tool in [TOOLS.md](TOOLS.md): license, platforms, last release, still maintained (#9)
- [x] Add a one-line "use it for" note to each entry (#10)
- [x] Remove anything unmaintained or not actually open source (#11)
- [ ] Make the repo public (#12)

## Milestone 2: The shared project file

- [x] Define the data model: people, locations, third-party elements, contracts, assets (#13)
- [x] Publish it as a JSON Schema with a sample project (#14)
- [x] Build save and load to a file on disk, with export to CSV (#15)
- [x] Decide how tools handle a file edited by two people: warn on conflict, with reload, save a copy or explicit overwrite (#16)

## Milestone 3: The clearances core

Three tools on one data model. This is the documentary-specific gap.

- [ ] Release tracker: who signed what, linked to footage, with scans stored locally (#17)
- [ ] Clearance / E&O log: every third-party element, its source, license status and cost (#18)
- [ ] Credits builder: pulls names and roles from the project, flags contractually required credits (#19)
- [ ] Plain template versions of all three (#20)

## Milestone 4: Call sheet generator

- [x] Call sheet built from the project's people and locations (#21), first version with optional online weather lookup
- [ ] Plain template version (#22). Printing to PDF works from the browser's print dialog
- [ ] Import an Analyze Video report (timestamps and frames) into a project's footage log or research notes. This lives in the [Analyze-Video-Skill repo](https://github.com/evillollive/Analyze-Video-Skill), not here: it writes a project file the toolkit tools already read

## Backlog

Everything else in the "Built here" section of [TOOLS.md](TOOLS.md), prioritized by what contributors ask for.

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
