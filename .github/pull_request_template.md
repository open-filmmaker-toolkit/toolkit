## What this changes



## How you tested it

CI runs the browser tests in Chromium, once as Chrome and once the way Firefox and Safari save files, including phone width, dark mode and print. It doesn't run Firefox or Safari themselves on pull requests; a weekly check covers the basics in both. Tick these when you checked by hand, for example on a real device.

- [ ] Opened the tool in Chrome or Edge
- [ ] Opened it in Firefox or Safari
- [ ] Loaded the sample project, saved, and reopened the saved file
- [ ] Opened the saved file in the other tools and checked nothing was lost
- [ ] Checked phone width and dark mode
- [ ] Checked the printed version, if the tool prints

## Checklist

- [ ] Every commit is signed off (`git commit -s`)
- [ ] No network requests, external scripts, stylesheets or fonts
- [ ] No real people, productions or contracts in sample files

Refs #
