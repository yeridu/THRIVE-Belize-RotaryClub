"""Regenerate the QR code shown on the closing slide.

The code is committed as a static SVG so the deck needs no internet access and
loads no third-party script -- important both for presenting in Punta Gorda and
for not leaking who scanned it.

Usage:  python scripts/make_qr.py [url]
Requires: pip install qrcode
"""

import sys
from pathlib import Path

import qrcode

DEFAULT_URL = "https://yeridu.github.io/THRIVE-Belize-RotaryClub/"
OUT = Path(__file__).resolve().parent.parent / "assets" / "qr-deck.svg"


def build_svg(url: str) -> str:
    # Highest error correction, so the code still scans from a projector screen
    # or from a printed handout that has been folded in a pocket.
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    size = len(matrix)

    # Merge horizontal runs of dark modules into single rects to keep the file small.
    rects = []
    for y, row in enumerate(matrix):
        x = 0
        while x < size:
            if row[x]:
                run = 1
                while x + run < size and row[x + run]:
                    run += 1
                rects.append(f'<rect x="{x}" y="{y}" width="{run}" height="1"/>')
                x += run
            else:
                x += 1

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'shape-rendering="crispEdges" role="img" '
        f'aria-label="QR code linking to {url}">'
        f'<rect width="{size}" height="{size}" fill="#FFFFFF"/>'
        f'<g fill="#111111">{"".join(rects)}</g></svg>'
    )


def main() -> None:
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    OUT.write_text(build_svg(url), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"Encodes: {url}")
    print("Scan it before presenting, and update the address on slides 1 and 15.")


if __name__ == "__main__":
    main()
