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
- [x] A home page that shows our tools by stage, how they connect, search, and the directory of other tools: [`index.html`](index.html), served by GitHub Pages
- [x] Make the repo public, with the home page live at [open-filmmaker-toolkit.github.io/toolkit](https://open-filmmaker-toolkit.github.io/toolkit/) ([#12](https://github.com/open-filmmaker-toolkit/toolkit/issues/12))

## Milestone 2: The shared project file

- [x] Define the data model: people, locations, third-party elements, contracts, assets ([#13](https://github.com/open-filmmaker-toolkit/toolkit/issues/13))
- [x] Publish it as a JSON Schema with a sample project ([#14](https://github.com/open-filmmaker-toolkit/toolkit/issues/14))
- [x] Build save and load to a file on disk, with export to CSV ([#15](https://github.com/open-filmmaker-toolkit/toolkit/issues/15))
- [x] Decide how tools handle a file edited by two people: warn on conflict, with reload, save a copy or explicit overwrite ([#16](https://github.com/open-filmmaker-toolkit/toolkit/issues/16))
- [x] Work together on a file in a synced folder: a [guide](docs/sharing-a-project.md), a warning when someone else has the file open, merging two copies or your changes with the file's, and spotting conflicted copies ([#151](https://github.com/open-filmmaker-toolkit/toolkit/issues/151))
- [x] Record who changed each record and when ([#153](https://github.com/open-filmmaker-toolkit/toolkit/issues/153))

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
- [x] Chrome and Edge remember the open file, so the next tool opens it with one click ([#148](https://github.com/open-filmmaker-toolkit/toolkit/issues/148))
- [x] Open a project once on the home page and move between tools: each item on the dashboard opens its tool with the project, on that record ([#147](https://github.com/open-filmmaker-toolkit/toolkit/issues/147))
- [x] A project dashboard on the home page: what needs you across every tool, the next 60 days, revenue and impact, from the same rules the tools use ([#147](https://github.com/open-filmmaker-toolkit/toolkit/issues/147))
- [x] One calendar file for every date in the project, from the dashboard and from each tool with dates ([#149](https://github.com/open-filmmaker-toolkit/toolkit/issues/149))
- [x] Read-only summaries of chosen parts of the project to share, leaving out contact details, notes and fees unless you include them ([#152](https://github.com/open-filmmaker-toolkit/toolkit/issues/152))
- [ ] Install the hub as an app for offline use

## Backlog

Every tool in [TOOLS.md](TOOLS.md), built in the order contributors asked for. Each had its own issue in the [Backlog milestone](https://github.com/open-filmmaker-toolkit/toolkit/milestone/6). New requests go there too.

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
- [x] Location scout sheet: access, power, sound, light, parking, restrooms, signal and permits, with photos kept in the project file, linked to the place and its location release, and a printed scout report ([#55](https://github.com/open-filmmaker-toolkit/toolkit/issues/55))
- [x] Deal memos: filled in from the project and the shooting calendar, sent and signed with the signed copy kept, rates sent to the budget, the credit checked by the credits builder, and a printed memo to sign under a CC0 legal form ([#56](https://github.com/open-filmmaker-toolkit/toolkit/issues/56))
- [x] Gear list: gear by department, owned, borrowed or rented, with day and week rates, values and serial numbers, packages for each shoot day, a printed load-out checklist and insurance schedule, and CSV ([#57](https://github.com/open-filmmaker-toolkit/toolkit/issues/57))
- [x] COI and permit tracker: certificates requested and received for each vendor and location, with who's named on them, permits with the issuing office, dates and conditions, linked to locations and shoot days, what's missing or expiring flagged before each day, scans kept, and CSV ([#58](https://github.com/open-filmmaker-toolkit/toolkit/issues/58))
- [x] Travel sheet: trips from the shooting calendar with who's going, travel and places to stay for each person, local contacts, the emergency number and nearest hospital, and a printed sheet for everyone or one person ([#59](https://github.com/open-filmmaker-toolkit/toolkit/issues/59))
- [x] Risk and hostile-environment plans: hazards rated by likelihood and impact with what you'll do and who makes sure, emergency contacts, hospitals from call sheets, an evacuation plan, check-ins and what to do when one is missed, printed for the crew and for the insurer ([#60](https://github.com/open-filmmaker-toolkit/toolkit/issues/60))
- [x] Security checklist: devices, accounts, sources, footage, borders and physical security, ticked off for each person, with notes and extra items for a high-risk shoot, and print ([#61](https://github.com/open-filmmaker-toolkit/toolkit/issues/61))
- [x] Camera and sound reports: a report for each card with clips, codec, frame rate and lens notes, or files with their tracks, linked to the shoot day and call sheet, cards recorded as assets, print and CSV for the edit ([#62](https://github.com/open-filmmaker-toolkit/toolkit/issues/62))
- [x] Interview log: who, when, where and which cards, timestamped moments with favorites and story beats, the person's release status and the transcript, on the same interview records as interview prep, with print and CSV for the paper edit ([#63](https://github.com/open-filmmaker-toolkit/toolkit/issues/63))
- [x] Name supers list: names from the project, near-miss spellings flagged, changes since the last export to graphics, CSV export ([#71](https://github.com/open-filmmaker-toolkit/toolkit/issues/71))
- [x] Field journal: dated entries of what happened, what you learned and story ideas, tagged with people and locations, searchable, linked to a shoot day's call sheet, with Markdown export and print ([#66](https://github.com/open-filmmaker-toolkit/toolkit/issues/66))
- [x] Daily production report: recording each shoot day: call, meal and wrap times and hours for crew and talent, what was shot, and incidents and delays ([#64](https://github.com/open-filmmaker-toolkit/toolkit/issues/64))
- [x] Expense log: logging production expenses against budget accounts while keeping receipt files on your computer ([#65](https://github.com/open-filmmaker-toolkit/toolkit/issues/65))
- [x] Festival submission tracker: tracking festival submissions, with deadlines, fees, results and screening dates ([#78](https://github.com/open-filmmaker-toolkit/toolkit/issues/78))
- [x] Press list: outlets and the people who cover them by beat, screener links sent, screening RSVPs, coverage with links and dates, and CSV, on a screenings list shared with the partner CRM ([#81](https://github.com/open-filmmaker-toolkit/toolkit/issues/81))
- [x] Partner CRM: organizations and their contacts, commitments and next steps with due dates and who owes them, links to screenings, print and CSV ([#90](https://github.com/open-filmmaker-toolkit/toolkit/issues/90))
- [x] Discussion guide builder: screening-specific synopsis from the treatment, editable themes and questions, audience resources and selected partner organizations, credits from the project, and print to PDF ([#91](https://github.com/open-filmmaker-toolkit/toolkit/issues/91))
- [x] Archive log: copies of project assets with storage locations, copy dates, hash manifests, manually recorded read-back checks and CSV export ([#96](https://github.com/open-filmmaker-toolkit/toolkit/issues/96))
- [x] Footage log: clips imported from a folder, a CSV or the camera reports, tagged with people, locations and topics from the project, with notes, ratings, tagging several clips at once, print, and CSV for your editing app ([#67](https://github.com/open-filmmaker-toolkit/toolkit/issues/67))
- [x] Paper edit: SRT, VTT and timestamped text transcripts, bites picked and arranged into scenes with their source in and out timecodes, print, CSV, and a CMX 3600 edit list (EDL) for Premiere, Resolve or Avid ([#68](https://github.com/open-filmmaker-toolkit/toolkit/issues/68))
- [x] Structure board: scene cards with summaries and running times, dragged (or moved with buttons) into sequences and acts, colored by story thread or character, cards from the paper edit's scenes, print and CSV ([#69](https://github.com/open-filmmaker-toolkit/toolkit/issues/69))
- [x] Cut version tracker: cuts with date, running time and what changed, feedback screenings, notes tied to a time or range and a scene or shot, done, deferred or carried to a later cut, and the locked cut setting the project's cut version and running time ([#70](https://github.com/open-filmmaker-toolkit/toolkit/issues/70))
- [x] Budget-to-actuals: the budget against the expense log line by line, expenses assigned to lines, variance, estimate to complete and estimated final cost, a report date, print and CSV ([#72](https://github.com/open-filmmaker-toolkit/toolkit/issues/72))
- [x] Fair use log: the four factors for each element marked fair use in the clearance log, where the film will be shown with a note that fair use is a US doctrine, the attorney's review, and a printed draft memo with the not-legal-advice notice ([#73](https://github.com/open-filmmaker-toolkit/toolkit/issues/73))
- [x] License tracker: media, territory, term and dates for each archival and music license, payments and what's due, options and step deals with deadlines, expiring licenses and lapsing options flagged, linked both ways to the clearance log ([#74](https://github.com/open-filmmaker-toolkit/toolkit/issues/74))
- [x] Annotated-transcript clearance report: SRT, VTT, text or a paper edit transcript with timecode, marked references to people, places, products, quotes, music and archival material, each one's clearance from the clearance log and release tracker, names found from the project, and a printed report ([#75](https://github.com/open-filmmaker-toolkit/toolkit/issues/75))
- [x] Chain-of-title binder: underlying rights, agreements, copyright and title, releases and licenses in order, each linked to its document, what's missing flagged, and a printed index and cover sheets ([#76](https://github.com/open-filmmaker-toolkit/toolkit/issues/76))
- [x] Festival strategy map: festivals with tier, premiere rules, city, country and region, festival and notification dates, in date order, with a warning when an earlier festival would cost a premiere at a later one, which festivals to hear back from first, fees paid and still to pay, print and CSV ([#77](https://github.com/open-filmmaker-toolkit/toolkit/issues/77))
- [x] EPK and press notes builder: logline, synopses, director's statement and the production story, bios saved with each person, credits from the credits builder, accepted festivals and their screenings, technical details, stills with captions and photo credits kept in the project file, press contacts, and print to PDF ([#79](https://github.com/open-filmmaker-toolkit/toolkit/issues/79))
- [x] Stills library: production stills and key art with captions, photo credits, dates and the people pictured, checked against the release tracker, approvals, the full-resolution file on your computer, and a caption sheet to print or export ([#80](https://github.com/open-filmmaker-toolkit/toolkit/issues/80))
- [x] Awards and social calendars: awards with eligibility rules and windows checked against the first screening, entry deadlines, voting, nominations and ceremonies, social posts on one calendar with festival screenings and the release date, suggested posts around each accepted festival, a calendar file (.ics) and print ([#82](https://github.com/open-filmmaker-toolkit/toolkit/issues/82))
- [x] Rights availability matrix: distribution deals with territories, media, term, fee and exclusivity, a territory-by-media grid of sold, on hold and available rights as of any date, overlapping exclusive deals and rights reverting in the next six months flagged, print and CSV ([#83](https://github.com/open-filmmaker-toolkit/toolkit/issues/83))
- [x] Deliverables checklist: the usual delivery list of picture, sound, captions, artwork and legal paperwork, each with status, due date, who's responsible, specs and where the file is, what the rest of the project already has, items overdue or due soon, your own items, print and CSV ([#84](https://github.com/open-filmmaker-toolkit/toolkit/issues/84))
- [x] QC tracker: master versions, QC reports with their result, issues with timecode, severity, area, who fixes it, fix status and the version it was fixed in, a printed fix list for the editor, colorist or mixer, and CSV ([#85](https://github.com/open-filmmaker-toolkit/toolkit/issues/85))
- [x] Recoupment waterfall model: tiers in payment order (percentages off the top or of what's left, fixed amounts such as expenses, recoupment, premium and deferments, and a profit split), revenue scenarios with actual revenue from the revenue tracker, what each party receives, the break-even point, a printed summary and CSV ([#86](https://github.com/open-filmmaker-toolkit/toolkit/issues/86))
- [x] Revenue tracker: statements from distributors, sales agents and platforms with period, territory, media, gross receipts, fees, expenses, what's due and when it was paid, totals by source, territory, media, year or quarter, payments still to come, actual revenue for the waterfall model, print and CSV ([#87](https://github.com/open-filmmaker-toolkit/toolkit/issues/87))
- [x] Educational and theatrical booking trackers: educational licenses and theatrical and community bookings with the venue or institution, contact, dates, license or terms, fee or box office share, invoicing and payment, screening materials needed and sent, totals by month, quarter or year, print and CSV. It tracks bookings; it doesn't take them from the public or process payments ([#88](https://github.com/open-filmmaker-toolkit/toolkit/issues/88))
- [x] Theory of change builder: the goal, audiences, activities, short-, medium- and long-term outcomes and the indicators that measure them, with targets and how they're measured, gaps flagged, a one-page diagram to print in landscape, CSV, and indicators the impact report records results against ([#89](https://github.com/open-filmmaker-toolkit/toolkit/issues/89))
- [x] Screening kit builder: about the film from the press notes, hosting, tech specs and formats, promotion with approved stills and key art, the discussion guide, a host checklist by week with your own items, and print to PDF ([#92](https://github.com/open-filmmaker-toolkit/toolkit/issues/92))
- [x] Impact report: results against the theory of change's indicators with progress to each target, screenings and community and educational bookings in the period with their attendance, active partners, stories and quotes with permission to quote, a summary, print to PDF and CSV ([#93](https://github.com/open-filmmaker-toolkit/toolkit/issues/93))
- [x] Final cost report: budget against final cost from budget-to-actuals, by account, line, top sheet or a funder's categories from the budget converter, the date costs run to, draft or final, variance notes with large variances flagged, print and CSV ([#94](https://github.com/open-filmmaker-toolkit/toolkit/issues/94))
- [x] Grant final reports: a final report for each awarded grant in the grant calendar, with its due date and status, the narrative with answers from the grant narrative library, outcomes, deliverables, final costs in the funder's categories, the impact report, and print to PDF ([#95](https://github.com/open-filmmaker-toolkit/toolkit/issues/95))
- [x] Contract and release archive: every contract and release in the project, in folders by kind with a tab number, its signed copy, anything signed without a copy flagged, where the archive is kept and when it was checked, the index as CSV, a suggested folder layout as a text file, and a printed index ([#97](https://github.com/open-filmmaker-toolkit/toolkit/issues/97))

Finding a third maintainer is on hold. Basil and Alex maintain the project for now ([#8](https://github.com/open-filmmaker-toolkit/toolkit/issues/8), closed).

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
