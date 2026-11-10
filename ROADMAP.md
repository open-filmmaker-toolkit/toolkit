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

## Milestone 5: The hub

The home page becomes a place to work, not just a list. Each step gets an issue before work starts.

- [x] First version: every tool by stage and phase, workflows that show how the tools connect, search, and planned tools linked to their issues
- [x] Chrome and Edge remember the open file, so the next tool opens it with one click ([#148](https://github.com/open-filmmaker-toolkit/toolkit/issues/148))
- [x] Open a project once on the home page and move between tools: each item on the dashboard opens its tool with the project, on that record ([#147](https://github.com/open-filmmaker-toolkit/toolkit/issues/147))
- [x] A project dashboard on the home page: what needs you across every tool, the next 60 days, revenue and impact, from the same rules the tools use ([#147](https://github.com/open-filmmaker-toolkit/toolkit/issues/147))
- [x] One calendar file for every date in the project, from the dashboard and from each tool with dates ([#149](https://github.com/open-filmmaker-toolkit/toolkit/issues/149))
- [x] Import a filled-in spreadsheet template into the tool it matches, with columns matched by name, problems shown row by row, and nothing already there changed ([#150](https://github.com/open-filmmaker-toolkit/toolkit/issues/150))
- [x] Read-only summaries of chosen parts of the project to share, leaving out contact details, notes and fees unless you include them ([#152](https://github.com/open-filmmaker-toolkit/toolkit/issues/152))
- [x] Install the hub as an app for offline use ([#205](https://github.com/open-filmmaker-toolkit/toolkit/issues/205))
- [x] Open a project once and it stays open as you move between the home page and any tool in the same tab, with changes not saved yet, and no "leave this page?" question on the way
- [x] Say which browsers save straight back to the file, and in Firefox and Safari, how to save over the same file instead of collecting copies

## Milestone 6: Planned

Each item has [its own issue](https://github.com/open-filmmaker-toolkit/toolkit/milestone/8). None of it is built yet.

### Scripted productions

- [x] Script breakdown: scenes, cast, locations, props and other elements read from a Fountain script, ready for the schedule and the call sheet ([#167](https://github.com/open-filmmaker-toolkit/toolkit/issues/167))
- [x] Stripboard: scenes from the breakdown arranged into shoot days, with page counts and company moves ([#168](https://github.com/open-filmmaker-toolkit/toolkit/issues/168))
- [x] Day-out-of-days: each cast member's start, work, hold and finish days from the schedule ([#169](https://github.com/open-filmmaker-toolkit/toolkit/issues/169))
- [x] Sides: the day's scenes from the script, printed small for cast and crew ([#170](https://github.com/open-filmmaker-toolkit/toolkit/issues/170))
- [x] Shot list and storyboard for each scene, with your own frames kept in the project file ([#171](https://github.com/open-filmmaker-toolkit/toolkit/issues/171))
- [x] Scene and take numbers on the call sheet, daily production report and camera and sound reports ([#172](https://github.com/open-filmmaker-toolkit/toolkit/issues/172))

### Tools that share their work

- [x] Rental costs from the gear list, per diems and travel from the travel sheet, and permit fees go into the budget ([#173](https://github.com/open-filmmaker-toolkit/toolkit/issues/173))
- [x] Actual spending from the expense log against the plan in cash flow ([#174](https://github.com/open-filmmaker-toolkit/toolkit/issues/174))
- [x] Committed costs, such as signed deal memos and purchase orders, separate from what's spent, in budget-to-actuals ([#175](https://github.com/open-filmmaker-toolkit/toolkit/issues/175))
- [x] Release status shown in the clearance log and call sheet, and the clearance log linked to the release tracker's people and locations ([#176](https://github.com/open-filmmaker-toolkit/toolkit/issues/176))
- [x] The interview log's favorite moments as bites in the paper edit, and moments linked to clips in the camera reports ([#177](https://github.com/open-filmmaker-toolkit/toolkit/issues/177))
- [x] QC issues linked to the cut in the cut version tracker ([#178](https://github.com/open-filmmaker-toolkit/toolkit/issues/178))
- [x] Investors and broadcasters in the finance plan linked to their organizations in the funder CRM ([#179](https://github.com/open-filmmaker-toolkit/toolkit/issues/179))
- [x] Smaller links between tools, from the risk plan and travel sheet to bookings and screenings ([#180](https://github.com/open-filmmaker-toolkit/toolkit/issues/180))

### Fixes

- [x] Edit or remove a screening once it's added, in the partner CRM and press list ([#181](https://github.com/open-filmmaker-toolkit/toolkit/issues/181))

### Money

- [x] Currencies other than the project currency in the revenue tracker ([#182](https://github.com/open-filmmaker-toolkit/toolkit/issues/182))
- [x] Cost reports by period in budget-to-actuals, and comparing two cost reports or two final cost reports ([#183](https://github.com/open-filmmaker-toolkit/toolkit/issues/183))
- [x] Globals in the budget, such as a shoot length every line can refer to ([#184](https://github.com/open-filmmaker-toolkit/toolkit/issues/184))
- [x] Uneven cost spreads, such as a deposit and a final payment, and one-off items in cash flow ([#185](https://github.com/open-filmmaker-toolkit/toolkit/issues/185))
- [x] Cross-collateralization between territories and compound interest in the waterfall ([#186](https://github.com/open-filmmaker-toolkit/toolkit/issues/186))
- [x] Most-favored-nations terms across licenses in the license tracker ([#187](https://github.com/open-filmmaker-toolkit/toolkit/issues/187))
- [x] Union rates and rules, overtime, meal penalties and turnaround, timecards, and deal memos for cast and contributors ([#188](https://github.com/open-filmmaker-toolkit/toolkit/issues/188))

### Imports

- [x] Expenses from a bank or card statement into the expense log ([#189](https://github.com/open-filmmaker-toolkit/toolkit/issues/189))
- [x] Contacts from an address book (vCard) into the funder CRM, partner CRM, press list and subject tracker ([#190](https://github.com/open-filmmaker-toolkit/toolkit/issues/190))
- [x] Festivals from a submission platform's export, and grants from a funder database's export ([#191](https://github.com/open-filmmaker-toolkit/toolkit/issues/191))
- [x] QC reports from a QC house's file into the QC tracker, and hash manifests into the archive log ([#192](https://github.com/open-filmmaker-toolkit/toolkit/issues/192))
- [x] A budget from another budgeting program's own file ([#193](https://github.com/open-filmmaker-toolkit/toolkit/issues/193))

### Exports

- [ ] An Avid ALE from the footage log, FCPXML and AAF from the paper edit with drop-frame timecode, and QC markers for an editing app ([#194](https://github.com/open-filmmaker-toolkit/toolkit/issues/194))
- [x] Exports for titling tools and crawl services from name supers and the credits builder ([#195](https://github.com/open-filmmaker-toolkit/toolkit/issues/195))
- [x] The pitch deck as PowerPoint or Keynote, and the call sheet and treatment as Word documents ([#196](https://github.com/open-filmmaker-toolkit/toolkit/issues/196))
- [ ] Electronic cue sheet formats for performing rights organizations, series and episodes, and splitting a cue sheet by reel ([#197](https://github.com/open-filmmaker-toolkit/toolkit/issues/197))

### Versions and views

- [x] Several versions to compare in the treatment, structure board, theory of change, narrative library and impact report, and more than one delivery at a time ([#198](https://github.com/open-filmmaker-toolkit/toolkit/issues/198))
- [x] Month grids in the awards and social calendars and in the festival strategy map ([#199](https://github.com/open-filmmaker-toolkit/toolkit/issues/199))
- [x] Charts in the impact report, and comps side by side with charts in the comps tracker ([#200](https://github.com/open-filmmaker-toolkit/toolkit/issues/200))

### Trust and polish

- [x] Translations of the tools, starting with Spanish and French ([#201](https://github.com/open-filmmaker-toolkit/toolkit/issues/201))
- [x] A guided first run on the home page that points you to the tools you'll need first ([#202](https://github.com/open-filmmaker-toolkit/toolkit/issues/202))
- [x] Versioned project files with automatic backups ([#203](https://github.com/open-filmmaker-toolkit/toolkit/issues/203))
- [ ] Test by hand with VoiceOver and NVDA, and in Firefox and Safari ([#204](https://github.com/open-filmmaker-toolkit/toolkit/issues/204))
- [x] A simpler home page: the tools by stage, without the search box or "How the tools connect"

### Desktop app

An app that saves straight back to your project file on every computer, using the same tools as the website. See [desktop/](desktop/README.md).

- [x] A first build for testing on a Mac: open, save back to the same file, export, print, and carry the project between tools
- [ ] Sign it for Mac and Windows
- [ ] Windows and Linux installers
- [ ] Connect a project folder in the app
- [ ] Releases page, and a link from the home page

### Smaller items, tool by tool

From each tool's "Not yet" list.

- [x] Archive log: which assets have no off-site copy ([#207](https://github.com/open-filmmaker-toolkit/toolkit/issues/207))
- [x] Awards and social calendars: each award's full rules ([#208](https://github.com/open-filmmaker-toolkit/toolkit/issues/208))
- [x] Bookings: invoices to print and box office reports for split deals ([#209](https://github.com/open-filmmaker-toolkit/toolkit/issues/209))
- [x] Budget converter: funder forms with their own line items, split lines and more formats ([#210](https://github.com/open-filmmaker-toolkit/toolkit/issues/210))
- [x] Camera and sound reports: matching camera clips to sound files ([#211](https://github.com/open-filmmaker-toolkit/toolkit/issues/211))
- [x] Chain of title and deliverables: distributors' delivery schedules, one PDF of the documents, and checking agreement language ([#212](https://github.com/open-filmmaker-toolkit/toolkit/issues/212))
- [x] Clearance log: license files linked to each element ([#213](https://github.com/open-filmmaker-toolkit/toolkit/issues/213))
- [x] Clearance report: Word and PDF scripts, spans across lines, and adding to the clearance log from a mark ([#214](https://github.com/open-filmmaker-toolkit/toolkit/issues/214))
- [x] Certificates and permits: each vendor's insurance requirements ([#215](https://github.com/open-filmmaker-toolkit/toolkit/issues/215))
- [x] Contract archive: retention dates ([#216](https://github.com/open-filmmaker-toolkit/toolkit/issues/216))
- [x] Credits builder: where a required credit appears and its size ([#217](https://github.com/open-filmmaker-toolkit/toolkit/issues/217))
- [x] Cut version tracker: carried notes that follow scenes when they move ([#218](https://github.com/open-filmmaker-toolkit/toolkit/issues/218))
- [x] Daily production report: signatures on the printed report ([#219](https://github.com/open-filmmaker-toolkit/toolkit/issues/219))
- [x] Discussion guide: guides for different audiences and resource lists from outside ([#220](https://github.com/open-filmmaker-toolkit/toolkit/issues/220))
- [x] Fair use log: best practices links, clip timecodes, and marking fair use from here ([#221](https://github.com/open-filmmaker-toolkit/toolkit/issues/221))
- [x] Festival strategy map: each festival's premiere rules and deadline tiers with fees ([#222](https://github.com/open-filmmaker-toolkit/toolkit/issues/222))
- [x] Festival submissions: reminders, laurels, fees and travel, and a shared list of festivals ([#223](https://github.com/open-filmmaker-toolkit/toolkit/issues/223))
- [x] Field journal: photos and audio notes, your own tags, and rich text ([#224](https://github.com/open-filmmaker-toolkit/toolkit/issues/224))
- [x] Final cost report: an accountant's sign-off page ([#225](https://github.com/open-filmmaker-toolkit/toolkit/issues/225))
- [x] Footage log: moments inside a clip ([#226](https://github.com/open-filmmaker-toolkit/toolkit/issues/226))
- [x] Gear list: checking gear out and in, purchase records, and kits ([#227](https://github.com/open-filmmaker-toolkit/toolkit/issues/227))
- [x] Grant calendar: reminders and a shared list of funders ([#228](https://github.com/open-filmmaker-toolkit/toolkit/issues/228))
- [x] Grant final reports: interim reports and funders' own forms ([#229](https://github.com/open-filmmaker-toolkit/toolkit/issues/229))
- [x] Interview log: selects and string-outs across interviews ([#230](https://github.com/open-filmmaker-toolkit/toolkit/issues/230))
- [x] Interview prep: follow-up questions and a shared question bank ([#231](https://github.com/open-filmmaker-toolkit/toolkit/issues/231))
- [x] Location scout: the sun's path, linked photos and your own checklist ([#232](https://github.com/open-filmmaker-toolkit/toolkit/issues/232))
- [x] Grant narrative library: answers in more than one language and saved funder prompts ([#233](https://github.com/open-filmmaker-toolkit/toolkit/issues/233))
- [x] Paper edit: transcripts from Word and noScribe ([#234](https://github.com/open-filmmaker-toolkit/toolkit/issues/234))
- [x] Pitch deck: themes and a trailer link ([#235](https://github.com/open-filmmaker-toolkit/toolkit/issues/235))
- [x] Press list: follow-up reminders ([#236](https://github.com/open-filmmaker-toolkit/toolkit/issues/236))
- [x] EPK and press notes: an EPK folder to download and Q&A and quotes sections ([#237](https://github.com/open-filmmaker-toolkit/toolkit/issues/237))
- [x] Release tracker: blank forms, releases tied to footage, and group releases ([#238](https://github.com/open-filmmaker-toolkit/toolkit/issues/238))
- [x] Research log: citations in a standard style ([#239](https://github.com/open-filmmaker-toolkit/toolkit/issues/239))
- [x] Revenue tracker: audits against the deal terms ([#240](https://github.com/open-filmmaker-toolkit/toolkit/issues/240))
- [x] Rights matrix: holdbacks, language rights and sub-territories ([#241](https://github.com/open-filmmaker-toolkit/toolkit/issues/241))
- [x] Risk plan: a check-in log and private medical details ([#242](https://github.com/open-filmmaker-toolkit/toolkit/issues/242))
- [x] Screening kit: a kit for each host ([#243](https://github.com/open-filmmaker-toolkit/toolkit/issues/243))
- [x] Security checklist: country checklists and reminders before trips ([#244](https://github.com/open-filmmaker-toolkit/toolkit/issues/244))
- [x] Shooting calendar: times within a day, conflicts, and adding people and places ([#245](https://github.com/open-filmmaker-toolkit/toolkit/issues/245))
- [x] Stills library: a folder of stills at full size and releases for stills ([#246](https://github.com/open-filmmaker-toolkit/toolkit/issues/246))
- [x] Structure board: index cards to print ([#247](https://github.com/open-filmmaker-toolkit/toolkit/issues/247))
- [x] Theory of change: arrows, and assumptions and risks ([#248](https://github.com/open-filmmaker-toolkit/toolkit/issues/248))
- [x] Travel sheet: passport and visa details and time zones ([#249](https://github.com/open-filmmaker-toolkit/toolkit/issues/249))
- [x] Treatment builder: character counts ([#250](https://github.com/open-filmmaker-toolkit/toolkit/issues/250))

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
- [x] Money in several currencies, at exchange rates you type in ([#154](https://github.com/open-filmmaker-toolkit/toolkit/issues/154))
- [x] Budget lines with several fringes and capped fringes, and deal memos with several rates ([#155](https://github.com/open-filmmaker-toolkit/toolkit/issues/155))
- [x] Waterfall pari passu tiers, corridors and simple interest on recoupment ([#156](https://github.com/open-filmmaker-toolkit/toolkit/issues/156))
- [x] Import transcripts with timecodes into the interview log, shared with the paper edit ([#157](https://github.com/open-filmmaker-toolkit/toolkit/issues/157))
- [x] Import markers from the edit into name supers and the music cue sheet ([#158](https://github.com/open-filmmaker-toolkit/toolkit/issues/158))
- [x] Find archive and music in the edit from an edit list, in the clearance log ([#159](https://github.com/open-filmmaker-toolkit/toolkit/issues/159))

Finding a third maintainer is on hold. Basil and Alex maintain the project for now ([#8](https://github.com/open-filmmaker-toolkit/toolkit/issues/8), closed).

## Out of scope

- Real-time co-editing
- Anything that collects data from the public or takes payments: community screening requests, crowdfunding, audience surveys
- Heavy media processing (editing, color, mixing): the directory points to existing open-source tools instead
