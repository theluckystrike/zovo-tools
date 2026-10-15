# Zovo browser tools

Source for the calculators, generators, converters, and utilities at
[tools.zovo.one](https://tools.zovo.one/). Each tool has its own directory.

## Find the code

- `index.html` is the tool catalog.
- `<tool-directory>/index.html` contains a tool page, usually with inline CSS and JavaScript.
- Some directories also contain a `service-worker.js`.
- `CNAME` names the hosted domain; `robots.txt` and `sitemap.xml` describe crawl routes.

Check the individual page's scripts and network requests before making claims about
its dependencies or data handling. There is no root `package.json` or build command.

## Preview a page locally

From the repository root, serve the existing files:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/barcode-generator/` directly. Some navigation links use
`/free-tools/` deployment paths, so they may not resolve under this local server.
External fonts or scripts can still require a network connection.

## Propose a change

Keep the patch scoped to the relevant tool directory. Include:

- The page path, exact input, expected result, and observed result.
- Browser/version, viewport size, and any console errors.
- A narrow-screen and keyboard check; inspect the actual file if the page exports one.

For example, a contrast-calculation regression check can use foreground `#000000`
and background `#FFFFFF`, with an expected WCAG contrast ratio of `21:1`.
Record what the page actually returns; this expected value is not a passing test report.

## Known issues (15 October 2026)

The `color-contrast-checker/` and `baby-name-generator/` application scripts currently
fail to parse in both this source snapshot and the hosted pages. Rendering the HTML
is not a functional pass; the contrast example above is a reproduction check.

## Optional: related AI workflow quickstarts

These ToolRoutine guides describe separate AI tools, their inputs, limits, and host setup.
Each guide includes a dated public Claude listing check; account access can differ.
Their features and review evidence do not certify the browser implementations in this repository.

| Browser source directory and task | Related AI guide and task |
|---|---|
| [barcode-generator/](barcode-generator/) — generate barcodes | [BarSmith](https://toolroutine.com/plugins/barcode-maker/) — create barcode files |
| [color-contrast-checker/](color-contrast-checker/) — inspect color contrast | [HueCheck](https://toolroutine.com/plugins/contrast-checker/) — check contrast and nearby colors |
| [ics-calendar-generator/](ics-calendar-generator/) — make calendar files | [InviteKit](https://toolroutine.com/plugins/calendar-invite/) — create event files and time-zone views |
| [pomodoro-timer/](pomodoro-timer/) — run focus intervals | [Tomatick](https://toolroutine.com/plugins/focus-timer/) — use a focus timer in chat |
| [random-picker/](random-picker/) — pick names or teams | [SpinPick](https://toolroutine.com/plugins/name-wheel/) — make a random pick or teams |
| [baby-name-generator/](baby-name-generator/) — generate name ideas | [NameTrend](https://toolroutine.com/plugins/baby-names/) — compare US name popularity, not generate names |
