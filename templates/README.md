# Plain templates

Blank versions of the toolkit's tools, for people who'd rather work in a spreadsheet, a word processor or on paper. Download the one you need. There's nothing to install.

Part of the [Open Filmmaker Toolkit](../README.md).

| Template | Spreadsheet | Document | Matches the tool |
| --- | --- | --- | --- |
| Subject tracker | [subject-tracker-template.csv](subject-tracker-template.csv) | | [Subject tracker](../tools/subject-tracker/) |
| Research and archival log | [research-log-template.csv](research-log-template.csv) | | [Research and archival log](../tools/research-log/) |
| Comps tracker | [comps-tracker-template.csv](comps-tracker-template.csv) | | [Comps tracker](../tools/comps-tracker/) |
| Treatment | | [treatment-template.docx](treatment-template.docx) | [Treatment builder](../tools/treatment-builder/) |
| Pitch deck | | [pitch-deck-template.docx](pitch-deck-template.docx) | [Pitch deck builder](../tools/pitch-deck/) |
| Call sheet | [call-sheet-template.csv](call-sheet-template.csv) | | [Call sheet](../tools/call-sheet/) |
| Clearance log | [clearance-log-template.csv](clearance-log-template.csv) | [clearance-log-template.docx](clearance-log-template.docx) | [Clearance log](../tools/clearance-log/) |
| Release log | [release-log-template.csv](release-log-template.csv) | [release-log-template.docx](release-log-template.docx) | [Release tracker](../tools/release-tracker/) |
| Music cue sheet | [music-cue-sheet-template.csv](music-cue-sheet-template.csv) | [music-cue-sheet-template.docx](music-cue-sheet-template.docx) | [Music cue sheet](../tools/music-cue-sheet/) |
| End credits | [end-credits-template.csv](end-credits-template.csv) | [end-credits-template.docx](end-credits-template.docx) | [Credits builder](../tools/credits-builder/) |
| Name supers | [name-supers-template.csv](name-supers-template.csv) | | [Name supers list](../tools/name-supers/) |

## What's in each one

- **Subject tracker.** One row for each possible subject: who they are, how you found them, contact details, access status and the next follow-up.
- **Research and archival log.** One row for each archival lead or research source: what it is, where it's from, rights holder, contact, estimated cost, status and notes.
- **Comps tracker.** One row for each comparable film: year, running time, premiere, distributor, where it played, figures with their sources, tags and why it's comparable.
- **Treatment.** The sections of a treatment, from logline to team, each with a note on what goes in it and a typical word target.
- **Pitch deck.** An outline with one heading per slide, from title and logline to contact, each with a note on what goes on it and a line for its images.
- **Clearance log.** One row for each piece of third-party material: what it is, where it's used, who holds the rights, what you need, status and cost. The document adds a box for the film's details and a key to the types and statuses.
- **Release log.** One row for each release: what kind, who or what it covers, when it was signed and where the signed copy is. The document adds a list of everyone on camera and every place you film, so you can see who still needs a release. It's a log, not a release form.
- **Music cue sheet.** One row for each cue, in the order it plays, with timings, usage and the composers, authors and publishers with their society and share. The document adds the production details distributors ask for and a key to the usage and role codes.
- **Name supers.** One row for each on-screen name and title, in the order they appear, with the timecode where each first appears.
- **End credits.** Credits in the usual order, with placeholders to replace, and music, archival, thanks and copyright lines. The document adds a table of the credits your contracts require, to tick off before you lock, and a checklist.

## Using them

- **Spreadsheets** (`.csv`) open in Excel, Numbers, Google Sheets (**File > Import**) and LibreOffice. Save a copy as `.xlsx` from there if you need that format.
- **Documents** (`.docx`) open in Word, Google Docs, Pages and LibreOffice. They're US Letter; switch to A4 in your page setup if you need to. To add a row to a table, put the cursor in the last cell and press Tab. To fill them in by hand, print them; the logs repeat their column headings on every page.
- **Same columns as the tools.** The subject tracker, research and archival log, comps tracker, clearance log, release log, music cue sheet and name supers spreadsheets have the same columns, in the same order, as each tool's CSV export, and the call sheet matches the call sheet's spreadsheet export. Some exports add columns the tool works out for you, such as a cue's duration in seconds or what's still missing.

These templates are working records, not legal advice, and you use them at your own risk: see [Not legal advice](../README.md#not-legal-advice). Check what your distributor, broadcaster and E&O insurer need. Blank release forms aren't here yet.

## Contributing

Have a template that works better? Share it from the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose) with **Submit a template**. Remove real names, contact details, rates and anything private first.

If you change a tool's CSV export, update its template here too. CI checks that each template's columns appear in the tool's export, in the same order. Edit the `.docx` files in Word or LibreOffice. Don't add macros, linked images or other external links: the validator rejects them.

## License

CC BY-SA 4.0, like all the toolkit's templates and guides. See [Licenses](../README.md#licenses).
