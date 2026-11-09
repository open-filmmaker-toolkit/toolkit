<p align="center">
  <b>Every booking, its terms, and whether it has been paid.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Educational and theatrical booking trackers

Track educational licenses and theatrical and community bookings: who booked, when, on what terms, and whether they've paid. It tracks bookings you've agreed; it doesn't take requests from the public or process payments.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#88](https://github.com/open-filmmaker-toolkit/toolkit/issues/88).

## Contents

- [Use it](#use-it)
- [What it does](#what-it-does)
- [Saving and file conflicts](#saving-and-file-conflicts)
- [What it adds to the project file](#what-it-adds-to-the-project-file)
- [Not yet](#not-yet)
- [License](#license)

## Use it

Open `index.html` in a browser. It's one self-contained file with no installs, no accounts and no network requests.

To try it with data, click **Open file** and choose [`samples/the-river-keeps.oft.json`](../../samples/the-river-keeps.oft.json) from the top of the repo. The sample's data is made up.

## What it does

- **Bookings** with the venue or institution, kind (educational, theatrical or community), contact, city, dates and status: inquiry, confirmed, done or cancelled.
- **License or terms:** one screening, one- or three-year or lifetime educational licenses, a digital site license, a flat fee, a box office split with your share, or no fee.
- **Invoicing and payment,** with invoices more than 30 days old flagged.
- **Prints an invoice** for a booking: **Save and print the invoice** numbers it (such as INV-2026-001), dates it today with payment due in 30 days unless you set another date, marks it invoiced, and prints who it's to, what it's for, the amount and how to pay. How to pay is filled in from your last invoice.
- **Box office reports for split deals.** Enter each night's or week's admissions and gross from the venue, and the taxes and fees taken off first, and it works out your share. **Save and print the box office report** prints the lines, the totals and the split; a split deal's invoice is for your share, with the report attached.
- **Screening materials:** what each booking needs (DCP, Blu-ray, a file or link, artwork, the discussion guide or the screening kit) and when each was sent. Confirmed bookings in the next 30 days still waiting on something are listed.
- **Fees** paid, invoiced and not invoiced, and **totals by month, quarter or year.**
- **Prints** the list and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/bookings-template.csv) with the same columns as the export.

- **A calendar file of every date in the project**, gathered from every tool: choose **Calendar of every date** under the file buttons and pick which kinds of dates to include. Importing a newer file updates the same events instead of adding them twice.
- **Imports from a spreadsheet:** choose **Import from a spreadsheet** under the file buttons and pick a CSV file. One with the columns of the [spreadsheet template](../../templates/bookings-template.csv) imports as it is; match any other columns once and the tool remembers. Problems, such as a date it can't read, show row by row before anything is added, and importing only adds.
- **Links a booking to its screening** from the [press list](../press-list/) and [partner CRM](../partner-crm/).

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `bookings` collection: `venue`, `kind`, `contact`, `email`, `city`, `startDate`, `endDate`, `status`, `license`, `fee`, `splitPercent`, `payment` (`unpaid`, `invoiced` or `paid`), `invoicedDate`, `paidDate`, `materialsNeeded`, `materials` (the date each was sent), `notes`, `boxOffice` (each line with `date`, `admissions` and `gross`), `boxOfficeTaxes`, `invoiceNumber`, `invoiceDue` and `invoicePayment`.

A booking can have a `screeningId`, in `screenings`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
