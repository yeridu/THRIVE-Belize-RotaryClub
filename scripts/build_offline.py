"""Build the single-file offline copy of the deck.

Punta Gorda bandwidth is not reliable and a meeting room may have no internet
at all, so the deck ships as one self-contained HTML file with the stylesheet,
the script, the photographs and the QR code all embedded. The three videos are
NOT embedded -- they are roughly 100 MB together, which would make the file
unusable. Download them separately (see the README); the deck degrades to a
short message on a video slide if none of the sources is reachable.

Run from anywhere:

    python scripts/build_offline.py
"""

import base64
import mimetypes
import re
from pathlib import Path

DECK = Path(__file__).resolve().parent.parent
SOURCE = DECK / "index.html"
TARGET = DECK / "THRIVE-Belize-RotaryClub-OFFLINE.html"


def data_uri(path: Path) -> str:
    """Return path's bytes as a data: URI, guessing the media type."""
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        mime = "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return "data:{};base64,{}".format(mime, payload)


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")

    # Stylesheet -> inline <style>
    css = (DECK / "assets" / "css" / "styles.css").read_text(encoding="utf-8")
    html = re.sub(
        r'<link rel="stylesheet" href="assets/css/styles\.css">',
        "<style>\n" + css + "\n</style>",
        html,
    )

    # Script -> inline <script>
    js = (DECK / "assets" / "js" / "deck.js").read_text(encoding="utf-8")
    html = re.sub(
        r'<script src="assets/js/deck\.js"></script>',
        "<script>\n" + js + "\n</script>",
        html,
    )

    # Every local image reference -> data: URI
    embedded = 0
    for src in sorted(set(re.findall(r'(?:src|href)="((?:photos|assets)/[^"]+)"', html))):
        asset = DECK / src
        if not asset.is_file():
            raise SystemExit("missing asset referenced by the deck: {}".format(src))
        html = html.replace('"{}"'.format(src), '"{}"'.format(data_uri(asset)))
        embedded += 1

    leftover = re.findall(r'(?:src|href)="(?!https?:|data:|#)([^"]+)"', html)
    if leftover:
        raise SystemExit("still referencing external files: {}".format(sorted(set(leftover))))

    TARGET.write_text(html, encoding="utf-8")
    print("wrote {} ({:.0f} KB, {} assets embedded)".format(
        TARGET.name, TARGET.stat().st_size / 1024, embedded))


if __name__ == "__main__":
    main()
