<p align="center">
  <b>Hazards, a way out, and who to call.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Risk and hostile-environment plans

Plan for risk on a shoot, especially in hostile environments: each hazard rated by likelihood and impact with what you'll do about it, emergency contacts, the nearest hospitals, an evacuation plan, and a check-in schedule with what to do when someone misses one. Print one copy for the crew and one for your insurer.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#60](https://github.com/open-filmmaker-toolkit/toolkit/issues/60).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's plan, contacts and hospital are made up.

## What it does

- **A plan for each shoot or trip:** standard, higher risk or hostile environment, with dates, locations and the team picked from the project. Start one from an upcoming shoot day in the [shooting calendar](../shooting-calendar/) and it fills in the trip's dates, places and people.
- **A risk assessment by hazard.** Rate each hazard's likelihood and impact from 1 to 3; the rating is the two multiplied, from low to high. Write what you'll do about it and who makes sure. Pick a common hazard, such as water, heat, crowds or detention, for a starting point on what to do.
- **Emergency contacts and the nearest hospitals.** Add hospitals already listed on [call sheets](../call-sheet/) for the plan's locations.
- **Getting out:** a meeting point and an evacuation plan.
- **Check-ins:** when, with whom and how, and the steps to take when someone misses one, starting from a default you can change.
- **Flags** hazards rated high or with nothing planned, and plans with no contacts, hospital or check-ins. The side panel lists upcoming shoot days at a location no plan covers.
- **Prints for the crew:** contacts, hospitals, the way out, check-ins, and each hazard with what to do. **Prints for the insurer:** the production, dates, locations and team, the full risk assessment, the emergency plans and a line to sign. **Exports CSV** of the risk assessment. Also exports project data: project details, people, locations, third-party elements, contracts, assets, music cue sheet details or call sheets as separate CSV files.

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/risk-assessment-template.csv) with the same columns as the export.

This tool helps you write a plan down. It doesn't replace hostile-environment training, a security adviser or what your insurer requires.

- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/risk-assessment-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

`riskPlans`: each has an `id`, `title`, `level` (`standard`, `elevated` or `hostile`), and optional `startDate`, `endDate`, `author`, `locationIds`, `personIds` (the team), `hazards`, `contacts`, `hospitals`, `meetingPoint`, `evacuation`, `checkIns` and `notes`.

- Each hazard has an `id`, `hazard`, `likelihood` and `impact` (1 to 3), and optional `controls` (what you'll do) and `ownerId` (who makes sure, in `people`).
- Each contact has an `id` and optional `name`, `role`, `phone` and `notes`. Each hospital has an `id` and optional `name`, `address`, `phone` and `notes`.
- `checkIns` has optional `times` (separated by commas), `contact`, `method` and `escalation`, the steps in order, each with `after` and `action`.

It reads `people`, `locations`, `shootDays` and the hospitals on `callSheets`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- A check-in log during the shoot
- Medical details for each person, kept separately and privately
- Maps and routes
- Linking a plan to a trip on the travel sheet

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
