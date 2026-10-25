#!/usr/bin/env python3
"""Tests for the Large-Print Tech Kit.

Each test verifies that every sheet in the kit builds a valid, one-page
PDF with real content, using the real build script.

Run with:
    python3 -m pytest tests/ -v
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent.parent
BUILD_PY = ROOT / "build.py"
DEFAULT_OUTDIR = ROOT / "build" / "pdf"

SHEET_SOURCES = [
    "sheets/01-answer-the-phone.html",
    "sheets/02-video-call-grandkids.html",
    "sheets/03-text-a-photo.html",
    "sheets/04-spot-a-scam.html",
    "sheets/05-charge-the-phone.html",
    "sheets/06-safe-web-habits.html",
]

# A phrase that must appear in the extracted text of each built PDF.
EXPECTED_TEXT = {
    "01-answer-the-phone.pdf": "Answer the Phone",
    "02-video-call-grandkids.pdf": "Video Call the Grandkids",
    "03-text-a-photo.pdf": "Text a Photo",
    "04-spot-a-scam.pdf": "Five red flags",
    "05-charge-the-phone.pdf": "Charge the Phone",
    "06-safe-web-habits.pdf": "Safe Habits on the Web",
    "caregiver-guide.pdf": "Caregiver Guide",
}


@pytest.fixture(scope="session")
def build_output(tmp_path_factory) -> Path:
    """Run the real build script into a temporary directory once per session."""
    outdir = tmp_path_factory.mktemp("build") / "pdf"
    result = subprocess.run(
        ["python3", str(BUILD_PY), "--outdir", str(outdir), "--quiet"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.fail(f"build.py failed:\n{result.stdout}\n{result.stderr}")
    return outdir


def _pdf_reader(name: str, build_output: Path) -> PdfReader:
    path = build_output / name
    assert path.is_file(), f"missing built PDF: {name}"
    return PdfReader(str(path))


@pytest.mark.parametrize("src", SHEET_SOURCES)
def test_every_sheet_source_exists(src: str):
    assert (ROOT / src).is_file(), f"missing source HTML: {src}"


@pytest.mark.parametrize("name", sorted(EXPECTED_TEXT.keys()))
def test_pdf_is_valid(name: str, build_output: Path):
    """Every built PDF: real file, %PDF magic bytes, parseable by pypdf."""
    path = build_output / name
    assert path.is_file(), f"expected built PDF: {name}"
    data = path.read_bytes()
    assert data[:5] == b"%PDF-", f"{name} is not a PDF (bad magic bytes)"
    assert b"%%EOF" in data[-1024:], f"{name} has no %%EOF trailer"
    # pypdf must parse it and report at least one page
    reader = PdfReader(str(path))
    assert len(reader.pages) >= 1
    assert path.stat().st_size > 1024, f"{name} is suspiciously small"


@pytest.mark.parametrize("name", ["01-answer-the-phone.pdf",
                                  "02-video-call-grandkids.pdf",
                                  "03-text-a-photo.pdf",
                                  "04-spot-a-scam.pdf",
                                  "05-charge-the-phone.pdf",
                                  "06-safe-web-habits.pdf"])
def test_sheet_is_exactly_one_page(name: str, build_output: Path):
    reader = _pdf_reader(name, build_output)
    assert len(reader.pages) == 1, f"{name} must be a one-page cheatsheet"


@pytest.mark.parametrize("name", sorted(EXPECTED_TEXT.keys()))
def test_pdf_contains_expected_text(name: str, build_output: Path):
    """The rendered PDF must contain the sheet's real content, not blank pages."""
    phrase = EXPECTED_TEXT[name]
    reader = _pdf_reader(name, build_output)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    assert phrase.lower() in text.lower(), f"expected '{phrase}' in the text of {name}"


def test_page_counts_match_declaration(build_output: Path):
    """Page counts must not exceed the limits declared in build.py."""
    import sys

    sys.path.insert(0, str(ROOT))
    import build  # noqa: E402  (local import: adds ROOT to sys.path)

    for src_rel, out_name, max_pages in build.SOURCES:
        reader = _pdf_reader(out_name, build_output)
        assert len(reader.pages) <= max_pages, (
            f"{src_rel} renders {len(reader.pages)} pages, limit is {max_pages}"
        )


def test_default_build_directory_has_full_kit():
    """A human-facing check: the default build/ directory holds complete PDFs."""
    reader = None
    if DEFAULT_OUTDIR.is_dir():
        names = {p.name for p in DEFAULT_OUTDIR.glob("*.pdf")}
        missing = set(EXPECTED_TEXT) - names
        if missing:
            pytest.fail(f"build/pdf is missing: {sorted(missing)} (run: python3 build.py)")
        for name in EXPECTED_TEXT:
            reader = PdfReader(str(DEFAULT_OUTDIR / name))
            assert len(reader.pages) >= 1
    else:
        pytest.skip("no default build/pdf directory yet (run: python3 build.py)")
