# Roadmap

Each milestone below becomes a GitHub milestone, and each checkbox becomes an issue.

## Milestone 0: Foundations (private)

- [ ] Create the GitHub organization and private repo
- [ ] Write README, ROADMAP, TOOLS and GOVERNANCE
- [ ] Lawyer reviews the planned licenses for code, templates and legal forms
- [ ] Add LICENSE files once approved
- [ ] Write CONTRIBUTING.md with Developer Certificate of Origin (DCO) sign-off
- [ ] Adopt a code of conduct
- [ ] Add issue forms: "Request a tool," "Submit a template," "Report a problem"
- [ ] Find a third maintainer

## Milestone 1: The directory (public launch)

- [ ] Verify every tool in [TOOLS.md](TOOLS.md): license, platforms, last release, still maintained
- [ ] Add a one-line "use it for" note to each entry
- [ ] Remove anything unmaintained or not actually open source
- [ ] Make the repo public

## Milestone 2: The shared project file

- [ ] Define the data model: people, locations, third-party elements, contracts, assets
- [ ] Publish it as a JSON Schema with a sample project
- [ ] Build save and load to a file on disk, with export to CSV
- [ ] Decide how tools handle a file edited by two people (merge, warn, or last save wins)

## Milestone 3: The clearances core

Three tools on one data model. This is the documentary-specific gap.

- [ ] Release tracker: who signed what, linked to footage, with scans stored locally
- [ ] Clearance / E&O log: every third-party element, its source, license status and cost
- [ ] Credits builder: pulls names and roles from the project, flags contractually required credits
- [ ] Plain template versions of all three

## Milestone 4: Call sheet generator

- [ ] Call sheet built from the project's people and locations
- [ ] PDF export and a plain template version

## Backlog

Everything else in the "Built here" section of [TOOLS.md](TOOLS.md), prioritized by what contributors ask for.

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
