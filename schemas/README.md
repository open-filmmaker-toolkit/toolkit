# Shared project file

`project-v1.schema.json` describes the version 1 `.oft.json` project file. The existing [sample project](../samples/the-river-keeps.oft.json) demonstrates the format and can be used to test tools.

## Data model

The file is a JSON object with a `project` record and collections for reusable entities. Each entity has an `id` unique within its collection. References are IDs in the collection named by the field: contracts can refer to `personIds`, `locationIds`, `thirdPartyElementIds` and `assetIds`; a third-party element can refer back through `contractIds`.

| Collection | Purpose |
| --- | --- |
| `subjects` | People you might film, kept by the [subject tracker](../tools/subject-tracker/README.md#what-it-adds-to-the-project-file) until they're added to `people`; `personId` points to the person they became |
| `people` | Cast, crew, subjects and other contributors. `onCamera` marks someone who needs a release |
| `locations` | Places involved in production. `onCamera` marks a place that's filmed |
| `sources` | Archival leads and research sources, kept by the [research and archival log](../tools/research-log/README.md#what-it-adds-to-the-project-file); `elementId` points to the third-party element a lead became |
| `comps` | Comparable films, kept by the [comps tracker](../tools/comps-tracker/README.md#what-it-adds-to-the-project-file); each figure carries its `source` |
| `thirdPartyElements` | Archival material, music, artwork, logos and other clearances |
| `contracts` | Releases, licenses and other agreements; references the people, locations, elements and assets they cover. See [Releases](#releases) |
| `callSheets` | Shoot days: date, call and wrap times, a location, weather, schedule, and crew with call times; references `locations` and `people`. `locations` may also carry `latitude` and `longitude` |
| `assets` | Project materials such as footage, scans and documents; `relativePath`, when present, is relative to the project file. The [Archive log](../tools/archive-log/README.md#what-it-adds-to-the-project-file) adds `archiveCopies` to an asset for storage locations, copy dates, hash manifests and manually recorded read-back checks. The [footage log](../tools/footage-log/README.md#what-it-adds-to-the-project-file) keeps clips as assets with `type` "clip", tagged with `personIds`, `locationIds` and `topics` |
| `treatment` | The film's treatment: text by section, word targets and saved versions. A record rather than a collection; see the [treatment builder](../tools/treatment-builder/README.md#what-it-adds-to-the-project-file) |
| `grants` | Grants and funds, kept by the [grant calendar](../tools/grant-calendar/README.md#what-it-adds-to-the-project-file): deadline, amounts, materials and status |
| `narratives` | Grant application answers in versions by length, kept by the [grant narrative library](../tools/narrative-library/README.md#what-it-adds-to-the-project-file). Each version's `uses` records who got it and when, pointing to `grants` by `grantId` or naming the `funder` |
| `budget` | The production budget: accounts, detail lines, fringes, percentages such as contingency, and saved versions. A record rather than a collection; lines refer to accounts by `accountId` and fringes by `fringeId`. See the [budget](../tools/budget/README.md#what-it-adds-to-the-project-file) |
| `budgetFormats` | Funders' budget categories and how the budget's accounts, lines and percentages map to them, kept by the [budget converter](../tools/budget-converter/README.md#what-it-adds-to-the-project-file) |
| `financePlan` | Sources of money with status, terms and payment dates, kept by the [finance plan](../tools/finance-plan/README.md#what-it-adds-to-the-project-file); sources can follow a grant in `grants` by `grantId`. A record rather than a collection |
| `funders` | Funders, investors, broadcasters and other organizations, kept by the [funder CRM](../tools/funder-crm/README.md#what-it-adds-to-the-project-file): the people there, a log of meetings, calls and emails, next steps, and `grantIds` pointing to `grants` |
| `cashFlow` | When the budget's costs are paid, kept by the [cash flow](../tools/cash-flow/README.md#what-it-adds-to-the-project-file): budget account, line and percentage ids mapped to a date range, deferred or in-kind. A record rather than a collection |
| `shootDays` | Shoot days, travel days and holds, kept by the [shooting calendar](../tools/shooting-calendar/README.md#what-it-adds-to-the-project-file); refer to `locations`, `people` and the `callSheets` started from them |
| `interviews` | Interviews, planned in [interview prep](../tools/interview-prep/README.md#what-it-adds-to-the-project-file) (research, story beats and questions in order) and logged in the [interview log](../tools/interview-log/README.md#what-it-adds-to-the-project-file) (cards, moments and the transcript); refer to `people`, `shootDays`, `locations`, `mediaReports` and `assets` |
| `dailyReports` | Daily production reports, one per shoot day, kept by the [daily production report](../tools/daily-production-report/README.md#what-it-adds-to-the-project-file): call, lunch and wrap times, crew hours, what was shot (linked `mediaReports`), incidents and notes. Refer to `shootDays`, `callSheets` and `people`. |
| `expenses` | Expenses, per diems and petty cash, kept by the [expense log](../tools/expense-log/README.md#what-it-adds-to-the-project-file); each points to a budget account, and receipts are `assets` of type `receipt` (the file stays on your computer). |
| `festivals` | Festival submissions with status, deadline, fee, waiver code and screening dates, kept by the [festival submission tracker](../tools/festival-submissions/README.md#what-it-adds-to-the-project-file). |
| `journal` | Dated field journal entries, kept by the [field journal](../tools/field-journal/README.md#what-it-adds-to-the-project-file): `kind` (`happened`, `learned` or `idea`), `title`, `text`, and tags that refer to `people` and `locations` by `personIds` and `locationIds`, plus a `callSheetId` linking the entry to a shoot day in `callSheets` |
| `screenings` | Screenings and events, shared by the [press list](../tools/press-list/README.md#what-it-adds-to-the-project-file) and the [partner CRM](../tools/partner-crm/README.md#what-it-adds-to-the-project-file), which both add and link them; may refer to a `location` |
| `pressOutlets` | Press outlets with contacts by beat, screeners sent, RSVPs and coverage, kept by the [press list](../tools/press-list/README.md#what-it-adds-to-the-project-file); RSVPs refer to `screenings` |
| `partners` | Outreach partners with contacts and commitments, kept by the [partner CRM](../tools/partner-crm/README.md#what-it-adds-to-the-project-file); `screeningIds` refer to `screenings` |
| `discussionGuide` | Screening-specific synopsis, themes, questions, resource notes and selected partners, kept by the [discussion guide builder](../tools/discussion-guide/README.md#what-it-adds-to-the-project-file); credits and partner details remain in their source records |
| `scouts` | Location scouts, kept by the [location scout sheet](../tools/location-scout/README.md#what-it-adds-to-the-project-file); each points to a place in `locations`, and its photos are `assets` with the image in `data` |
| `gear` | Gear by department, owned, borrowed or rented, and the packages for each shoot day, kept by the [gear list](../tools/gear-list/README.md#what-it-adds-to-the-project-file). Packages refer to `shootDays` and to gear by `itemIds`. A record rather than a collection |
| `mediaReports` | Camera and sound reports, one for each card or roll, kept by [camera and sound reports](../tools/camera-sound-reports/README.md#what-it-adds-to-the-project-file); refer to `shootDays`, `callSheets` and `people`, and the card itself is an `asset` |
| `trips` | Trips, kept by the [travel sheet](../tools/travel-sheet/README.md#what-it-adds-to-the-project-file): who's going, travel and places to stay for each person, local contacts and emergency details; refer to `people`, `locations` and a trip in `shootDays` by `block` |
| `riskPlans` | Risk assessments and emergency plans, kept by the [risk and hostile-environment plans](../tools/risk-plan/README.md#what-it-adds-to-the-project-file): hazards, contacts, hospitals, evacuation and check-ins; refer to `people` and `locations` |
| `security` | The [security checklist](../tools/security-checklist/README.md#what-it-adds-to-the-project-file): who's on it, your own items, and which items each person has done. A record rather than a collection |
| `paperEdit` | Transcripts and the scenes of bites picked from them, kept by the [paper edit](../tools/paper-edit/README.md#what-it-adds-to-the-project-file). Transcripts refer to `interviews`, `people` and clips in `assets`. A record rather than a collection |
| `structure` | Acts, sequences, scene cards and story threads, kept by the [structure board](../tools/structure-board/README.md#what-it-adds-to-the-project-file); cards can point to scenes in `paperEdit`, and threads to `people`. A record rather than a collection |
| `cuts` | Cuts with their feedback screenings and notes, kept by the [cut version tracker](../tools/cut-tracker/README.md#what-it-adds-to-the-project-file); notes can point to cards in `structure`. Locking a cut sets `project.cutVersion` and `project.runningTime` |
| `costReport` | Estimates to complete and the report date, kept by [budget-to-actuals](../tools/budget-to-actuals/README.md#what-it-adds-to-the-project-file), which also adds `budgetLineId` to `expenses`. A record rather than a collection |
| `clearanceReport` | Scripts and transcripts with marked references, kept by the [annotated-transcript clearance report](../tools/clearance-report/README.md#what-it-adds-to-the-project-file); marks refer to `people`, `locations` and `thirdPartyElements`. A record rather than a collection |
| `chainOfTitle` | Links, statuses and your own items for the [chain-of-title binder](../tools/chain-of-title/README.md#what-it-adds-to-the-project-file); refers to `contracts` and `assets`. A record rather than a collection |
| `festivalStrategy` | Where the film is from, for the [festival strategy map](../tools/festival-strategy/README.md#what-it-adds-to-the-project-file), which also adds tier, premiere rules, place and dates to `festivals`. A record rather than a collection |
| `pressNotes` | Press notes sections, bios, stills and contacts, kept by the [EPK and press notes builder](../tools/press-notes/README.md#what-it-adds-to-the-project-file); refers to `people` and to stills in `assets`. A record rather than a collection |
| `awards` and `socialPosts` | Awards campaigns and planned posts, kept by the [awards and social calendars](../tools/awards-social/README.md#what-it-adds-to-the-project-file) |
| `deliverables` | Who you are delivering to, when, and the items you have changed or added, kept by the [deliverables checklist](../tools/deliverables/README.md#what-it-adds-to-the-project-file). A record rather than a collection |
| `qc` | Master versions and QC reports with their issues, kept by the [QC tracker](../tools/qc-tracker/README.md#what-it-adds-to-the-project-file); issues refer to versions. A record rather than a collection |
| `waterfall` | Tiers in payment order and revenue scenarios, kept by the [recoupment waterfall model](../tools/waterfall/README.md#what-it-adds-to-the-project-file). A record rather than a collection |
| `revenueStatements` | Statements from distributors, sales agents and platforms, kept by the [revenue tracker](../tools/revenue-tracker/README.md#what-it-adds-to-the-project-file); `contractId` points to a distribution deal in `contracts` |
| `bookings` | Educational licenses and theatrical and community bookings, kept by the [booking trackers](../tools/bookings/README.md#what-it-adds-to-the-project-file) |
| `theoryOfChange` | The campaign's goal, audiences, activities, outcomes and indicators, kept by the [theory of change builder](../tools/theory-of-change/README.md#what-it-adds-to-the-project-file). A record rather than a collection |
| `screeningKit` | The screening kit for hosts, kept by the [screening kit builder](../tools/screening-kit/README.md#what-it-adds-to-the-project-file); refers to stills in `assets`. A record rather than a collection |
| `impactReport` | The impact report: the period, a summary, results by indicator and stories and quotes, kept by the [impact report](../tools/impact-report/README.md#what-it-adds-to-the-project-file); refers to `theoryOfChange`. It also adds `attendance` to `screenings` and `bookings`. A record rather than a collection |
| `finalCostReport` | The date costs run to, whether it is final, and variance notes, kept by the [final cost report](../tools/final-cost-report/README.md#what-it-adds-to-the-project-file). A record rather than a collection |
| `grantReports` | Final reports for awarded grants, kept by the [grant final reports](../tools/grant-reports/README.md#what-it-adds-to-the-project-file); `grantId` points to `grants` |
| `contractArchive` | Where the archive is kept, when it was checked, and notes by contract, kept by the [contract and release archive](../tools/contract-archive/README.md#what-it-adds-to-the-project-file). A record rather than a collection |
| `pitchDeck` | A pitch deck or lookbook: page size, slides in order, and the images, resized and stored as data URLs. A record rather than a collection; see the [pitch deck builder](../tools/pitch-deck/README.md#what-it-adds-to-the-project-file) |
| `credits` | The end credits, in order. A record rather than a collection; see [Credits](#credits) |
| `supers` | On-screen names and titles (supers and lower thirds), and the list as it was last exported for graphics. A record rather than a collection; entries refer to `people` by `personId`, whose `name` is the spelling used. See the [name supers list](../tools/name-supers/README.md#what-it-adds-to-the-project-file) |

Tools should add only fields they own and preserve unknown fields and collections when saving. New collections and their fields are optional in version 1, so existing tools can continue to open files that do not use them. A tool that consumes references should report missing targets rather than silently discarding them. JSON Schema checks field shapes; tools remain responsible for ensuring IDs are unique within collections and references point to existing records.

## Releases

The release tracker treats a contract as a release when its `type` contains "release". It writes `appearance release`, `location release`, `materials release` and `other release`, with a `status` of `pending`, `signed` or `declined`, and dates as YYYY-MM-DD. A release is expired when it's signed and its `expirationDate` has passed.

- A person needs a release when `onCamera` is true, or when it's unset and an appearance or other release names them.
- A location needs a release when `onCamera` is true, or when it's unset and a call sheet or a location or other release names it.
- `onCamera: false` takes someone or somewhere off the list even if a release or call sheet names them.
- Materials releases cover clearance-log items through `thirdPartyElementIds`; each item records the release in `contractIds`. They don't cover a person's appearance.
- Certificates of insurance and permits are contracts too, with `type` "certificate of insurance" or "permit", and refer to `locations` and `shootDays`. See the [COI and permit tracker](../tools/coi-permit-tracker/README.md#what-it-adds-to-the-project-file).
- Licenses are contracts with `type` "license". The [license tracker](../tools/license-tracker/README.md#what-it-adds-to-the-project-file) adds their terms, payments and options, and links them to `thirdPartyElements` both ways. The [fair use log](../tools/fair-use-log/README.md#what-it-adds-to-the-project-file) adds `fairUse` to elements marked fair use.
- Deal memos are contracts too, with `type` "deal memo"; they aren't releases. See the [deal memos](../tools/deal-memos/README.md#what-it-adds-to-the-project-file) for their fields.
- Signed copies are `assets` with `type` "release scan" and a `relativePath` under `releases/`, relative to the project file.

## CSV exports

Each tool can export one project record or collection at a time to its own CSV file: `project`, `people`, `locations`, `thirdPartyElements`, `contracts`, `assets`, `musicCueSheet` and `callSheets`. Each property becomes a column; nested arrays and objects are encoded as JSON in a cell. The export includes all records in that collection, not only records visible under a tool's current filters.

## Credits

The credits builder keeps the end credits in a `credits` record: `entries` in the order they roll, and `notCredited`, the IDs of people left out on purpose so they aren't flagged as missing.

- Each entry has an `id` and a `kind`: `credit` (a `role`, with `personIds` from `people` and `names` for anyone not in the project), `heading`, `text`, `music` or `archival`.
- `music` and `archival` entries don't store their lines. They're built from the clearance log and music cue sheet each time, and store only a `heading` and the `excluded` keys of songs or sources left out. A key is the song title, or the source's name, in lowercase with accents and punctuation removed.
- A contract's `requiredCredit` is the on-screen credit it requires, word for word. The credits meet it when a line contains that wording, ignoring capitals and punctuation.
- Credits aren't one of the CSV exports. The credits builder exports them as text for the crawl.

## Money in several currencies

`project.currency` is the project currency. Any money record can carry its own `currency` (a three-letter code): budget lines, finance plan sources, contracts such as licenses, and expenses. Totals convert to the project currency at `project.exchangeRates`, which the user types in and the tools never fetch: each has a `currency`, a `rate` (what one unit is worth in the project currency) and an optional `date` it applies from. An amount with no currency is in the project currency, so older files keep working. The conversion is shared code, copied from [`shared/money.js`](../shared/money.js).

Budget lines can have several fringes in `fringeIds`; `fringeId` stays the first, for tools that read one. A fringe's optional `cap` limits it to wages up to that amount for each person on a line (the line's multiplier). A deal memo's other `rates`, such as prep or travel days, each keep their own budget line in `budgetLineId`. The budget math is shared code, copied from [`shared/budget.js`](../shared/budget.js).

## Concurrent edits

When a browser supports direct file access, a tool compares the opened file with the last version it read or saved before writing. If the file changed, the user can reload the latest version, save their edits to a separate copy, or explicitly overwrite the newer file. The user can also merge: records are matched by `id`, changes to different records or fields are combined, and fields changed on both sides are shown for the user to choose. The check cannot lock the file against a simultaneous write, so teams should save in one tool at a time. See [Working on a shared file](../docs/sharing-a-project.md).

Two optional fields support shared files. Every tool shares this code, copied from [`shared/tool.js`](../shared/tool.js):

- `openBy` at the top level lists who has the file open: each entry has a `name`, `since` (date and time) and the `tool` slug. A tool adds the user's entry when it opens the file (only if the user has added their name), removes it on save, and ignores entries older than four hours.
- `changedBy` and `changedAt` on any record with an `id`, set when a user who has added their name saves a change to that record. Merging uses them to explain each side's changes, and editors show "Changed by Ana, Nov 6". Download-based save flows cannot check the source file and instead produce a new download; users should open the latest shared copy before continuing.

Do not change `formatVersion` or make a breaking change to this model without a maintainer decision. Additive fields and collections can be introduced in version 1 while they remain optional and compatible with tools that preserve unknown data.

## License

The schema is code, under GPL-3.0-or-later. These notes are documentation, under CC BY-SA 4.0. See [Licenses](../README.md#licenses).
