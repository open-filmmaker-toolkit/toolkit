# Working on a shared project file

The toolkit has no accounts and no server. To work on a project with other people, keep the project file in a folder that a sync app shares between you: Google Drive for desktop, Dropbox, OneDrive or iCloud Drive. The tools open the file from that folder and save back to it, and the sync app copies it to everyone else.

## Set it up

1. Put the `.oft.json` file in a shared folder that the sync app keeps on your computer, not just in the cloud. In Google Drive for desktop, make the folder available offline. In Dropbox and OneDrive, don't use online-only mode for it.
2. Share the folder with the people you're working with.
3. In any tool, choose **Add your name** under the file buttons. Your name stays in this browser. The tools use it to note who has the file open and who changed each record.

Keep any files the project links to, such as scans and receipts, in the same folder, so the paths in the project file work for everyone.

## What works in each browser

| | Chrome and Edge | Firefox and Safari |
| --- | --- | --- |
| Save straight back to the file | Yes | No. Saving downloads a new copy. Move it into the shared folder in place of the old one |
| Remember the file, so the next tool can open it with one click | Yes | No |
| Warn when someone else has the file open | Yes | Only if the file you open has the note in it |
| Warn before overwriting someone else's changes | Yes | No. Check the shared folder for newer copies before you start |
| Merge two copies | Yes | Yes |
| Spot conflicted copies made by the sync app | Yes, once you choose the folder | No. Merge them by choosing each copy (see below) |

Chrome or Edge works best for a shared file.

## When two people edit at once

Sync apps copy whole files, so two people can't safely save the same file at the same moment. The tools help in three ways.

- **Who has it open.** When you open the file, the tool notes your name and the time in it. If someone else opens it within the next four hours, their tool shows "Ana has had this file open since 10:40". It's a warning, not a lock, because sync apps can take a minute to catch up. Your note is cleared when you save.
- **The save warning.** If the file changed after you opened it, the tool warns before saving. Choose **Merge both** to combine your changes with the ones in the file. Changes to different records, or different fields of the same record, are combined. If you both changed the same field, you choose which to keep.
- **Who changed what.** Records you change get your name and the date. Editors show "Changed by Ana, Nov 6", and merging uses it to explain each side's changes.

## Conflicted copies

When two people save before the sync app catches up, it keeps both, with a name like:

- `the-river-keeps (Ana's conflicted copy).oft.json` (Dropbox)
- `the-river-keeps (1).oft.json` (Google Drive)
- `the-river-keeps-ANAS-LAPTOP.oft.json` (OneDrive)
- `the-river-keeps 2.oft.json` (iCloud Drive)

In Chrome and Edge, choose **Add your name**, then **Choose the folder**, and pick the folder the project file is in. From then on, the tools look for conflicted copies when they open the file and offer to merge them.

In any browser, choose **Merge two copies**, then choose the file and the conflicted copy. The tool shows what each copy added, changed and removed, by tool, and asks you about anything both changed. The merged result is saved as a new file, so neither copy changes. Check it, then replace the original with it and delete the conflicted copy, so everyone works from one file again.

## Good habits

- Save often, and close the tool when you're done, so your note doesn't warn others for hours.
- Agree who owns which tools. Two people working in different tools rarely clash.
- Before a big change, such as locking the budget, save a copy of the file.
