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
- **Screening materials:** what each booking needs (DCP, Blu-ray, a file or link, artwork, the discussion guide or the screening kit) and when each was sent. Confirmed bookings in the next 30 days still waiting on something are listed.
- **Fees** paid, invoiced and not invoiced, and **totals by month, quarter or year.**
- **Prints** the list and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/bookings-template.csv) with the same columns as the export.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `bookings` collection: `venue`, `kind`, `contact`, `email`, `city`, `startDate`, `endDate`, `status`, `license`, `fee`, `splitPercent`, `payment` (`unpaid`, `invoiced` or `paid`), `invoicedDate`, `paidDate`, `materialsNeeded`, `materials` (the date each was sent) and `notes`.

Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

- Invoices to print
- Linking bookings to screenings in the press list and partner CRM
- Box office reports for split deals

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
