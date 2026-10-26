# Instructions for AI agents

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. It has the rules for how tools are built, what to check before a pull request, and how to sign off commits. This file adds what agents tend to miss.

## Keep the docs true to the code

Do this in the same pull request as the change, not later:

- **Roadmap.** Check off the item in [ROADMAP.md](ROADMAP.md) when the work is done, and add a line for anything you built that isn't listed. Read the roadmap before starting so you don't build something that is already done.
- **Issues.** Check the acceptance list of the issue you are working on against what is on `main`. Close an issue, with a comment saying what completes it, only when every item is met. Put `Closes #N` in the pull request description, once for each issue. `Closes #15 and #16` closes only the first.
- **READMEs.** Update the tool's `README.md`, including its "Not yet" list, and [schemas/README.md](schemas/README.md) if the project file changed.
- **Stale items.** If you notice an open issue or an unchecked roadmap item that is already done, say so in your pull request or fix it. Don't assume the tracker is right.

## Test in real browsers

CI runs [tests/browser_tools.py](tests/browser_tools.py) in Chromium, twice: `chromium`, and `chromium-fallback`, which takes the download-and-upload path Firefox and Safari use. Firefox and WebKit were dropped from CI because their installs kept hanging. Run both modes locally before you push (setup is in [CONTRIBUTING.md](CONTRIBUTING.md)), along with `python3 .github/scripts/validate_repo.py`.

- Static checks and Node harnesses are not enough. A browser test found a real bug that both missed: a dialog that stayed open after a successful export.
- Add a check to `tests/browser_tools.py` for any new behavior, including new buttons, dialogs and exports.
- Don't claim you tested phone width, dark mode, printing or another browser unless a test or a manual check actually did. CI doesn't run Firefox or Safari. In the pull request, tick only what you did and say what you didn't run.

## Pull requests

- Branch from `main`, and base the pull request on `main`. Don't stack a pull request on another pull request's branch: when the first one merges, GitHub may not retarget the second, and its changes never reach `main`. If you must stack, say so in the description and check that `main` has the changes after merging.
- Use the [pull request template](.github/pull_request_template.md) and keep its headings and order. Tick only what you did.
- Sign off every commit with `git commit -s`.
- Run the local checks first and open one pull request per change. CI is shared and limited, so avoid extra pushes while a run is in progress. See "CI and runners" in [CONTRIBUTING.md](CONTRIBUTING.md).
- Wait for all checks to pass on the latest commit before you say a pull request is ready.
- Don't merge a pull request unless the person you are working with has said you may. If merging is blocked by the workspace, don't work around it. Tell them to use the merge button or change the setting.

## Don't

- Don't add network requests, external scripts, fonts or dependencies to a tool, or a build step. See "How tools are built" in [CONTRIBUTING.md](CONTRIBUTING.md).
- Don't put real people, productions or contracts in `samples/`.
- Don't change `formatVersion` or remove fields a tool doesn't recognize.
- Don't file issues or make changes in other repositories without asking first.
