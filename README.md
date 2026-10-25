# Large-Print Tech Kit

Free, laminatable cheatsheets for helping a less techy relative.
Six one-page sheets with big type (16pt and up), written in plain,
warm English — plus a caregiver guide that tells you which sheet to
laminate and where to tape it.

**Privacy by design:** nothing leaves the home. The kit is plain HTML,
CSS, and Python. There are no accounts, no signups, no network calls,
and no data collection. You build the PDFs on your own computer.

Made with care by **Asdale Dynamics, LLC** — plain-English AI and
tech guides from Dylan Asdale (dylanasdale.github.io).

## The sheets

| # | Sheet | The one problem it solves |
|---|-------|---------------------------|
| 1 | Answer the Phone | Answer, speaker, end, missed calls, voicemail |
| 2 | Video Call the Grandkids | Two-tap video calling that you did not have to set up |
| 3 | Text a Photo | Send a picture in four taps |
| 4 | How to Spot a Scam | The five red flags, and what to do every time |
| 5 | Charge the Phone | Plug it in tonight, same outlet every night |
| 6 | Safe Habits on the Web | Five habits that cover almost everything |

The **Caregiver Guide** (extra page or two, for you, not them) tells
you which sheets to laminate first and how to hand them over well.

## How to build the PDFs

Requirements: Python 3.9+ and WeasyPrint.

```bash
pip install weasyprint
python3 build.py
```

PDFs appear in `build/pdf/`. One file per sheet, each exactly one page.

Options: `python3 build.py --outdir DIR` builds somewhere else;
`--clean` wipes the output directory first; `--quiet` prints only errors.
If a sheet ever overflows onto a second page, the build fails loudly —
one page is a rule, not a hope.

## Printing

Print on Letter paper at **100% scale** ("Actual size", not "Fit to
page"). Color and black-and-white both stay readable. Laminate 5-mil
pouches, or tape down sheet protectors.

## Running the tests

The tests run the real build script, then verify every PDF: valid
`%PDF` magic bytes and `%%EOF` trailer, parseable, real text inside,
and every sheet exactly one page.

```bash
pip install weasyprint pypdf pytest
python3 -m pytest tests/ -v
```

## How it fits together

```
css/print.css        shared large-print stylesheet (16pt+, Letter page)
sheets/*.html        the six one-page cheatsheets
guides/              the caregiver guide
build.py             HTML/CSS -> PDF build (WeasyPrint), enforces 1-page rules
tests/               pytest suite verifying every PDF
build/pdf/           built PDFs (generated, not committed)
```

To edit a sheet: open the HTML, keep every line of text 16pt or larger
(it is set once in `css/print.css`), run `python3 build.py`, and let the
tests tell you if the page overflowed.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
Free to print, laminate, share with your family, and hand out in the
waiting room. Not for resale as-is; see the license for full terms.

Health note: this kit covers everyday phone skills only. It is not
legal, financial, or medical advice — for real money or health
decisions, call the people whose names are in your contacts.
