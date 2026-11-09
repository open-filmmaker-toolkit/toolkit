<p align="center">
  <b>Crew deal memos, filled in from the project, signed, and in the budget.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Deal memos

Write down what you agreed with each crew member, cast member or contributor: role, dates, rate, kit fee, overtime, credit and payment terms. Print it to sign, track it from sent to signed, keep the signed copy, and send the rate to the budget. Check rates against union minimums and work out timecards from the daily reports.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#56](https://github.com/open-filmmaker-toolkit/toolkit/issues/56).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's deal memos and rates are made up.

## What it does

- **One deal memo for each crew member,** filled in from the project: their role comes from the people list, and the dates and number of days from the [shooting calendar](../shooting-calendar/) if they're on shoot days there. Add someone new and they're added to the project.
- **The terms crews agree to:** rate by the day, week, hour or flat fee, the guaranteed days or weeks and what that comes to, a kit fee, overtime and hours, payment terms, credit and anything else.
- **Tracks status:** draft, sent, signed or declined, with the dates. The side panel lists memos waiting for a signature, and crew on a call sheet or shoot day who don't have one yet.
- **Keeps the signed copy.** Attach the signed PDF or photo. In Chrome and Edge, connect the project folder and it's copied into a `deal-memos` folder next to your project file; otherwise the tool records the file name, and you keep the file there.
- **Sends the rate to the [budget](../budget/).** Pick an account and fringe, and saving adds the rate and guarantee as a budget line, and the kit fee as a second line. Lines already in the budget keep their account and name, and take the memo's rate and length when you save. A line that no longer matches is flagged.
- **The credit counts.** The credit wording is saved where the [credits builder](../credits-builder/) checks required credits, so it flags a deal memo's credit that's missing from the end credits.
- **Prints a deal memo to sign,** with the not-legal-advice notice and where the form was written for at the top, and lines for both signatures. **Exports CSV.** Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a blank [deal memo form](../../templates/legal-forms/deal-memo-template.docx) to fill in and sign, under CC0, and a [spreadsheet template](../../templates/deal-memos-template.csv) with the same columns as the export.

This is not legal advice. Deal memos are contracts, and what they need differs from place to place and with union rules. Have a lawyer licensed where you work review your form before anyone signs it. See [Not legal advice](../../README.md#not-legal-advice).

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/deal-memos-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Several rates in one memo,** such as prep, shoot and travel days. Each goes on its own budget line, and the printed memo lists them all.
- **Cast and contributors too.** Choose who a memo is for: crew, cast, or a contributor such as a composer, writer or consultant. The printed memo is headed to match, and someone new added for a cast memo is marked as on camera.
- **Minimum rates by role.** Under **Rates and rules**, list the minimum for each role and the agreement it comes from, or load them from a CSV with the columns of the [union rates template](../../templates/union-rates-template.csv). A memo whose rate is below the minimum for its role is flagged.
- **Timecards.** **Open timecards** works out each person's week from the call, meal and wrap times in the [daily production reports](../daily-production-report/): hours, overtime, double time, meal penalties and rest cut short between days. Set the rules under **Rates and rules**. Pay comes from each person's deal memo. Print the timecards to sign, or export a payroll summary as a CSV to hand to your payroll company.

The timecards are there to help you check hours and catch problems early. They don't replace a payroll service: the tool doesn't withhold taxes, pay anyone, file anything or know every rule in your agreement. Have your payroll company run the actual numbers.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md). Each time you save, this browser keeps a copy: **Earlier versions** shows the last few, what restoring each would undo, and restores one. See [Keeping your project safe](../../docs/backups.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

Deal memos are `contracts` with `type` "deal memo", a `status` (`draft`, `sent`, `signed` or `declined`) and `personIds` naming the crew member, and optional `role`, `startDate`, `endDate`, `rate`, `rateUnit` (`day`, `week`, `hour` or `flat`), `guarantee`, `kitFee`, `kitFeeUnit`, `overtime`, `paymentTerms`, `requiredCredit`, `otherTerms`, `writtenFor`, `notes`, `sentDate`, `signedDate`, `assetIds` (the signed copy, an asset with `type` "signed deal memo") and `budgetLineIds` (the lines in `budget` it keeps up to date, rate first, then kit fee).

A new crew member is added to `people`, with the role. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Different overtime and meal rules for each union in the same project
- Sixth and seventh day rates, night premiums and other premiums beyond overtime, meals and turnaround

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
