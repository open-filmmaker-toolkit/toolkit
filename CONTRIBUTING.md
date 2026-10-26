# Contributing

Thanks for helping build free tools for filmmakers. You don't need to write code to contribute: requests, templates and problem reports are just as useful.

> **Pre-launch.** The repo is private until we launch. Until it's public, contributions come from the maintainers and people we've invited.

By taking part, you agree to follow our [code of conduct](CODE_OF_CONDUCT.md).

## Contribute without writing code

Use the forms on the [new issue page](https://github.com/open-filmmaker-toolkit/toolkit/issues/new/choose):

- **Request a tool.** Describe a job you do by hand or pay for that a free tool could handle.
- **Submit a template.** Attach a form, sheet or document you use. A maintainer will clean it up, add it to the toolkit and credit you if you'd like. Remove real names, contact details, rates and anything else private first.
- **Report a problem.** Something in a tool or template is broken, wrong or confusing.

Never attach a real project file to an issue. Project files can hold private details about the people in your film. If we need one to reproduce a problem, we'll ask for a version with those details removed.

## Contribute code

If you're an AI agent, or you're working with one, also read [AGENTS.md](AGENTS.md).

Open an issue or comment on an existing one before starting anything bigger than a small fix, so we can agree on the approach first.

1. Create a branch from `main`.
2. Make your change and sign off every commit (see below).
3. Open a pull request and fill in the checklist.
4. A maintainer reviews it. Decisions follow [GOVERNANCE.md](GOVERNANCE.md).

### How tools are built

These rules are what make the toolkit free, private and easy to maintain. Pull requests that break them won't be merged.

- **One file per tool.** Each tool is a single self-contained `tools/<tool-name>/index.html` with its own `README.md`. No build step, no package installs, no frameworks.
- **No network requests.** No external scripts, stylesheets, fonts, analytics or APIs. A tool has to work offline, opened straight from a computer, and project data never leaves the person's machine. The one exception: a tool may offer a clearly labelled button that looks something up online, only if nothing is sent until the user clicks it and confirms, and the hosts are on the allowlist in `.github/scripts/validate_repo.py` (today: the call sheet's weather lookup).
- **Share the project file carefully.** Tools read and write the same `.oft.json` file. Follow the [version 1 schema](schemas/project-v1.schema.json) and [data model notes](schemas/README.md). Change only the parts your tool owns and keep everything else exactly as it was, including fields you don't recognize. Don't change `formatVersion` without an issue and a maintainer decision.
- **Plain language.** Sentence case. Buttons say what they do ("Save file," not "Submit"). Errors say what went wrong and how to fix it.
- **Usable by everyone.** Works with a keyboard, has visible focus and labels on every field, and works at phone width and in dark mode.
- **Fictional sample data only.** Files in `samples/` must never contain real people, productions or contracts.

### Before you open a pull request

- Open the tool in Chrome or Edge, and in Firefox or Safari. CI runs its automated checks only in Chromium, so this is the only check that a tool works in Firefox and Safari, as well as how it looks and feels.
- Load `samples/the-river-keeps.oft.json`, make a change, save, and reopen the saved file.
- Open that saved file in every other tool that uses it and check nothing was lost.
- Export each project collection to CSV and confirm the file contains all records, including fields the current tool does not edit.
- Open the same project in two tool tabs, save a change in one, then save in the other. Confirm it warns and offers reload, save a copy or explicit overwrite.
- If your tool prints, check the printed version on paper or in a PDF viewer. CI checks the print layout and renders a PDF, not a real printer.
- Check phone width and dark mode on a real phone, if you changed layout or colors. CI checks for overflow and contrast only.

## CI and runners

Two [GitHub Actions workflows](.github/workflows) run on pull requests, both on GitHub-hosted `ubuntu-latest` runners with read-only contents permission, a timeout, and actions pinned to commit SHAs (Dependabot keeps them current):

- **DCO** checks that every commit is signed off.
- **CI** validates the [project schema](schemas/project-v1.schema.json) against the sample files, checks that IDs and references in samples resolve, checks each tool has a README and makes no network requests, and checks templates are plain spreadsheets or Word files with no macros or external links.

Run the CI checks locally first:

- `pip install jsonschema` then `python3 .github/scripts/validate_repo.py`
- `pip install playwright pypdf`, `playwright install chromium`, then `python3 tests/browser_tools.py chromium` and `python3 tests/browser_tools.py chromium-fallback`. To try the real engines, `playwright install firefox webkit` and run with `firefox` or `webkit`

CI runs `tests/browser_tools.py` in headless Chromium on every pull request, twice: as Chrome, and as `chromium-fallback`, with the file access API turned off so it saves by download and opens by upload, the way Firefox and Safari do. Firefox and WebKit (Safari's engine) were dropped from CI because their installs kept hanging on GitHub's runners. For the same reason, CI runs the Chromium tests in the Google Chrome that GitHub's runners come with, by setting `PLAYWRIGHT_CHANNEL=chrome`, instead of downloading Playwright's own Chromium. It opens the sample, saves, exports every CSV, checks phone width (390px, no sideways scrolling) and light and dark mode contrast, and checks the print layout. The `chromium` run also renders a real PDF and tests the save-conflict warning. A change to a tool that breaks any of these fails the matching "Browser tests" check.

CI can't judge how a tool looks and feels, can't drive a real printer or phone, and doesn't qualify a release. Do the manual checks above for anything you changed visually, and for new behavior the tests don't cover; add a check to `tests/browser_tools.py` when you add a feature. While the repo is private on a free plan, branch protection isn't available, so reviewers should confirm all four checks (DCO, schema, and the two Chromium runs) are green before merging.

- Finish related changes as one candidate and run local checks before triggering CI. Where a CI check has a local equivalent, use the same check.
- Avoid overlapping runs and extra pushes while a candidate is being qualified. A passing result applies only to the commit it checked; a later commit needs its own passing run.
- If a run fails, inspect its logs and diagnose the cause before rerunning. Don't retry an unchanged failure. Rerun after a fix or a confirmed transient runner failure.
- Keep release evidence together: if artifacts belong to a specific run attempt, produce a complete set from one successful run rather than combining outputs from different attempts.
- Prefer fresh GitHub-hosted runners. Keep workflow permissions minimal, check out the exact commit being evaluated, and never put real project files or secrets in runner inputs or logs. If a check is intentionally non-blocking, label it clearly and don't present it as release qualification.

## Sign off your commits

Every commit needs a sign-off, under the [Developer Certificate of Origin](https://developercertificate.org/) (DCO). It's a statement that you wrote the change or have the right to contribute it. There's no form to sign and you keep the copyright to your work. An automatic check on each pull request flags commits that aren't signed off.

To sign off, add `-s` when you commit:

```sh
git commit -s -m "Add festival deadline import"
```

That adds a line with the name and email from your git settings:

```text
Signed-off-by: Jordan Lee <jordan@example.com>
```

The email has to match the commit's author email. GitHub's private `noreply` address is fine if that's what you commit with.

If you forgot:

```sh
# Just the last commit
git commit --amend --no-edit --signoff

# Every commit on your branch
git rebase --signoff main

# Then update your pull request
git push --force-with-lease
```

If you edit a file on the GitHub website, the repository adds the sign-off for you.

### What you're agreeing to

By signing off, you certify the following (DCO version 1.1):

```text
Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

## Licenses

Your contribution is published under the license for the kind of work it is: GPL-3.0-or-later for code, CC BY-SA 4.0 for templates, guides and documentation, and CC0 for legal forms. The [README](README.md#licenses) lists which folders each one covers. You keep the copyright to your work.

There's no contributor license agreement. Nobody, including the maintainers, gets the right to relicense your work.

If you contribute a legal form, such as a release:

- Say where it was written for: the country, and the state or province if it matters.
- Put the [not legal advice](README.md#not-legal-advice) notice at the top of the form.
- Know that CC0 gives up your rights to it, so anyone can adapt it without credit.
