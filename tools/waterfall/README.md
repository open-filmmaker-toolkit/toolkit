<p align="center">
  <b>Who gets paid, in what order, at any level of revenue.</b>
</p>

<p align="center">
  <img alt="Runs offline" src="https://img.shields.io/badge/runs-offline-2ea44f" />
  <img alt="No network requests" src="https://img.shields.io/badge/network%20requests-none-2ea44f" />
  <img alt="No dependencies" src="https://img.shields.io/badge/dependencies-none-2ea44f" />
  <img alt="Status: first version" src="https://img.shields.io/badge/status-first%20version-d29922" />
</p>

# Recoupment waterfall model

Model who gets paid, and in what order, from the film's revenue. Set up the tiers from your agreements, try revenue scenarios, and see what each party receives and when the investors are paid back.

Part of the [Open Filmmaker Toolkit](../../README.md). Tracking issue: [#86](https://github.com/open-filmmaker-toolkit/toolkit/issues/86).

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

- **Tiers in order:** a percentage of gross receipts off the top (such as a sales agent's fee), a percentage of what's left, a fixed amount paid until it's paid in full (expenses, investor recoupment and premium, deferments), or a split of what's left between parties. Reorder them with the arrows.
- **Start from the usual tiers** and change them to match your agreements.
- **Revenue scenarios:** try any amount of gross receipts, save scenarios, or choose actual revenue from the [revenue tracker](../revenue-tracker/).
- **Territory pools and cross-collateralization.** Group territories into pools, such as North America and the rest of the world. Actual revenue goes to the pool its territory is in, or try an amount for each pool. A fixed tier can say how much each pool recoups: without cross-collateralization, each pool recoups only from its own revenue, and a shortfall in one isn't made up from another; ticked as cross-collateralized, it is. Under each tier, the results say how the payment was split between the pools.
- **Compound interest.** A fixed tier's interest can be simple, or compounded monthly or yearly, and the results say how much interest is included.
- **What each party receives** at each tier and in total, with what's still owed on fixed tiers.
- **Break-even:** the gross receipts at which every fixed tier is paid in full.
- **Prints a summary** with every scenario side by side, and **exports CSV.**

For anyone who doesn't use the tool, there's a [spreadsheet template](../../templates/waterfall-template.csv) with the same columns as the export.

A model, not an accounting or legal advice. Your agreements decide the order and the amounts. See [Not legal advice](../../README.md#not-legal-advice).

- **Pari passu tiers, corridors and interest.** Several parties can share one tier at once, pro rata to what each is owed or by set shares. A corridor pays a party a share of gross receipts, from a set point, alongside the tiers. A fixed tier, such as recoupment, can earn simple interest from a date. The break-even and the printed summary account for all three.

## Saving and file conflicts

Chrome and Edge can save straight back to the file you opened. If it changed on disk since you opened it, the tool warns before saving. You can reload the latest version, save your edits as a separate copy, or explicitly overwrite the changed file. Safari and Firefox download a new copy instead.

Choose **Merge both** in that warning to combine your changes with the ones in the file instead. Chrome and Edge also remember the file you opened, so the next tool can open it with one click. To work on the file with other people, choose **Add your name**: the tools then note who has the file open and who changed each record, and **Merge two copies** combines copies made by a sync app. See [Working on a shared file](../../docs/sharing-a-project.md).

If you close the tab without saving, the page keeps a recovery copy in this browser and offers to restore it next time.

## What it adds to the project file

A `waterfall` record with `tiers`, in payment order (`name`, `kind` of `gross`, `percent`, `fixed`, `pari`, `split` or `corridor`, `party`, `percent`, `amount`, `splits` with `party` and `share`, and `note`), and `scenarios` (`name` and `gross`). A `fixed` tier can have `interest` (a yearly percentage), `interestFrom` (a date) and `compound` (`monthly` or `yearly`; simple when missing), and `byPool` (the amount each territory pool recoups) with `crossed` (true when cross-collateralized). `pools` lists the territory pools, each with `id`, `name` and `territories`. A `pari` tier has `parties`, each with `party`, `amount` and, when `shareBy` is `share`, a `share`. A `corridor` has `percent` and `from`, the gross receipts it starts at; corridors are paid alongside the tiers, wherever they sit in the list.

It reads `revenueStatements`. Everything else in the file is preserved. See the [data model notes](../../schemas/README.md).

## Not yet

Nothing planned right now. If something you need is missing, [open an issue](https://github.com/open-filmmaker-toolkit/toolkit/issues).

## License

GPL-3.0-or-later, like all the toolkit's code. See [Licenses](../../README.md#licenses).
