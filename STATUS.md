# STATUS — Large-Print Tech Kit

Last updated: 2026-10-25

## What was built

A free, laminatable large-print cheatsheet kit for helping a less
techy relative — plain HTML/CSS sources with a scripted PDF build,
so anyone can rebuild the kit on their own machine with no accounts
and nothing leaving the home. Asdale Dynamics, LLC.

- **Six one-page sheets** (16pt+ type throughout, US Letter):
  1. `01-answer-the-phone` — answer, speaker, end, missed calls, voicemail
  2. `02-video-call-grandkids` — two-tap video calling, lighting, frozen screens
  3. `03-text-a-photo` — take/send a photo in four taps, confirm delivery
  4. `04-spot-a-scam` — five red flags plus what to do every time
  5. `05-charge-the-phone` — nightly habit, flip-over cables, red battery
  6. `06-safe-web-habits` — bookmarks, pop-ups, fake "verify" links, lock icon
- **Caregiver guide** (2 pages, `guides/caregiver-guide.html`): which
  sheet to laminate first (default: 4 + 5), where to tape them,
  handover tips, print settings.
- **Build script** (`build.py`): renders every source with WeasyPrint
  into `build/pdf/`, exits nonzero if a sheet overflows past its
  one-page rule.
- **Test suite** (`tests/test_build.py`, pytest): runs the real build,
  then validates each PDF.
- **README.md** (usage, printing, structure) and **MIT LICENSE**
  (Copyright (c) 2026 Asdale Dynamics, LLC).

## How to run it

```bash
pip install weasyprint          # build-time rendering
python3 build.py                # -> build/pdf/*.pdf
pip install pypdf pytest        # test-time parsing
python3 -m pytest tests/ -v     # 28 tests
```

Options: `--outdir DIR`, `--clean`, `--quiet`.

## Verification results

- `python3 build.py --clean` — **passes**: 7 PDFs, 8 pages total
  (6 sheets at exactly 1 page each; caregiver guide at 2 of 2 allowed).
- `python3 -m pytest tests/ -q` — **28 passed** in ~3s.
  Tests verify every PDF has `%PDF` magic bytes and an `%%EOF`
  trailer, parses with pypdf, contains its expected text, is
  non-trivially sized, and every sheet is exactly one page
  (page overflow fails as an error).
- Spot-checked rendered text via pypdf extraction (real content,
  Letter page size 612 x 792 pt).
- Iteration history: sheets 4, 5, 6, and the caregiver guide
  initially overflowed to 2–3 pages and were rewritten tighter until
  the one-page rule held; the build script caught each failure.

## How to refresh it later

Edit a sheet in `sheets/*.html` (body copy stays 16pt via
`css/print.css`), run `python3 build.py`, and let `pytest tests/`
catch any page that no longer fits.

## Known gaps

- **A4 not verified.** Layout targets US Letter; A4 printers would
  need the `@page size` in `css/print.css` changed and reflow
  re-checked by hand.
- **Page density is not measured.** The build guarantees no sheet
  spills to page 2, but nothing automatically proves rendered text
  stayed >= 16pt; type size is fixed centrally in one stylesheet, so
  the residual risk is a stray inline style overriding it.
- **Generic icon wording by design.** Sheets say "green circle / red
  circle" rather than naming Android vs iPhone, so screens of specific
  phones differ; embedding UI screenshots is out of scope on purpose
  (keeps the kit text-only, offline, and license-clean).
- **English only.** Translations are welcome as additional files;
  non-Latin scripts would need a font update in `css/print.css`.
- **WeasyPrint >= 60 required**; there is no vendored fallback
  renderer.
- Content covers everyday phone skills only — it is education, not
  legal, financial, or medical advice.
