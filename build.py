#!/usr/bin/env python3
"""Build the Large-Print Tech Kit: HTML/CSS cheatsheets -> PDFs.

Every sheet in sheets/ and the caregiver guide are rendered to PDF with
WeasyPrint, into the build output directory (default: build/pdf/).

The build verifies:
  * every declared source renders without error
  * sheets are exactly one page (overflow fails the build)

Usage:
    python3 build.py                 # build everything into build/pdf/
    python3 build.py --outdir DIR    # build into a different directory
    python3 build.py --quiet         # only report failures

No network access, no accounts, no data collection. Fully offline.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    from weasyprint import HTML
except ImportError:  # pragma: no cover
    sys.exit(
        "WeasyPrint is required. Install it with:\n"
        "  pip install weasyprint\n"
        "See https://doc.courtbouillon.org/weasyprint/ for system dependencies."
    )

ROOT = Path(__file__).resolve().parent

# (relative source path, output PDF name, max allowed pages)
SOURCES: list[tuple[str, str, int]] = [
    ("sheets/01-answer-the-phone.html", "01-answer-the-phone.pdf", 1),
    ("sheets/02-video-call-grandkids.html", "02-video-call-grandkids.pdf", 1),
    ("sheets/03-text-a-photo.html", "03-text-a-photo.pdf", 1),
    ("sheets/04-spot-a-scam.html", "04-spot-a-scam.pdf", 1),
    ("sheets/05-charge-the-phone.html", "05-charge-the-phone.pdf", 1),
    ("sheets/06-safe-web-habits.html", "06-safe-web-habits.pdf", 1),
    ("guides/caregiver-guide.html", "caregiver-guide.pdf", 2),
]


def build_sheet(src_rel: str, out_name: str, max_pages: int, outdir: Path, quiet: bool) -> int:
    """Render one HTML file to PDF. Returns the number of pages produced."""
    src = ROOT / src_rel
    if not src.is_file():
        raise FileNotFoundError(f"Missing source file: {src_rel}")

    out_path = outdir / out_name
    doc = HTML(filename=str(src)).render()
    pages = len(doc.pages)
    if pages > max_pages:
        raise RuntimeError(
            f"{src_rel} rendered to {pages} pages, but the limit is {max_pages}. "
            "Trim the content or shorten the text so it fits one page."
        )
    doc.write_pdf(str(out_path))
    doc_file_pages = out_path.stat().st_size
    if doc_file_pages < 1024:
        raise RuntimeError(f"{out_name} is suspiciously small ({doc_file_pages} bytes).")
    if not quiet:
        print(f"  built {out_name} ({pages} page{'s' if pages != 1 else ''}, {doc_file_pages:,} bytes)")
    return pages


def main() -> int:
    parser = argparse.ArgumentParser(description="Build all large-print cheatsheets to PDF.")
    parser.add_argument("--outdir", default="build/pdf", help="output directory (default: build/pdf)")
    parser.add_argument("--clean", action="store_true", help="remove the output directory first")
    parser.add_argument("--quiet", action="store_true", help="only report failures")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    if not outdir.is_absolute():
        outdir = ROOT / outdir
    if args.clean and outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not args.quiet:
        print(f"Building Large-Print Tech Kit -> {outdir}")

    total_pages = 0
    try:
        for src_rel, out_name, max_pages in SOURCES:
            total_pages += build_sheet(src_rel, out_name, max_pages, outdir, args.quiet)
    except Exception as exc:
        print(f"BUILD FAILED: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"Done. {len(SOURCES)} PDFs, {total_pages} pages total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
