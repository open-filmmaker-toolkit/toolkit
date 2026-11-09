# Translations

The toolkit's pages can be read in more than one language. Each language is a spreadsheet in this folder, so you can add or improve a translation without writing code.

| Language | File | What's translated |
| --- | --- | --- |
| Spanish | [es.csv](es.csv) | The home page, the call sheet and release tracker, the parts every tool shares, and printed screening kits |
| French | [fr.csv](fr.csv) | The same |

Pick a language from the menu next to the toolkit's name at the top of any tool, or at the bottom of the home page. The browser remembers it. If your browser is set to a language there's a translation for, that's used until you pick another. Anything not translated yet stays in English.

## Improve a translation

Open the language's file in a spreadsheet app or a text editor. The first column is the English, exactly as it appears in the tool; the second is the translation. Change the second column, save it as CSV (UTF-8), and send a pull request.

- Translate a whole sentence or label at a time, the way it's split in the file.
- Keep `<b>`, `<code>` and `<a>` around the same words, translated. They stand for bold text, code and links, and the tool puts the link's address back. You can move them within the sentence.
- Keep `{company}`, `{title}` and other words in braces as they are.
- Leave the second column empty for anything you'd rather leave in English.

## Add a language

1. Add a line to [languages.csv](languages.csv) with the language's code (such as `pt` for Portuguese), its name in that language, and the word for "Language" in it.
2. Copy `es.csv` to a new file named after the code, such as `pt.csv`, and replace the second column.
3. Run `python3 .github/scripts/sync_shared.py`. It copies the translations each page uses into that page, so the tools still work offline as single files.
4. Run `python3 .github/scripts/validate_repo.py`, which checks the files, and send a pull request.

To translate more of a tool, add rows: put its English text in the first column exactly as it appears on the page, with any bold, code or links written as `<b>`, `<code>` or `<a>` without their addresses. Text the tools write while you work, such as counts and messages, is translated when it matches a row exactly.

Your project file isn't translated: names, notes and everything you type stay as you wrote them. A screening kit can print its headings, checklist and our starting wording in another language; choose it next to **Print the kit**.
