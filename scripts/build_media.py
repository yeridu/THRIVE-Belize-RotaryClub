"""Bring every video into the repository, small enough to play on a weak line.

The room has a poor connection and the two large videos were streaming from a
GitHub release at 33 MB and 35 MB. Streaming is what makes them stall: the
browser plays only as fast as the bytes arrive. The fix is to stop streaming.
Both are re-encoded to a fraction of the size and committed alongside the deck,
so the whole talk is one download and then nothing touches the network.

Re-encode settings are chosen for slide-and-narration video, not for film:
720p is kept because text on the frames must stay sharp, the rate factor is
raised until artefacts would begin to show on flat colour, and the audio drops
to mono at a speech bitrate.

    python scripts/build_media.py

Skips any download or encode whose output already exists.
"""

import re
import subprocess
import urllib.request
from pathlib import Path

import imageio_ffmpeg

DECK = Path(__file__).resolve().parent.parent
MEDIA = DECK / "media"
CACHE = DECK.parent / "_video_source"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

RELEASE = "https://github.com/yeridu/THRIVE-Belize-GuestLecture/releases/download/v1.0/"
SOURCES = ["Morales2026THRIVE-Belize.mp4", "Morales2026TheManBox.mp4"]


def duration_of(path: Path) -> float:
    out = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    if not m:
        raise SystemExit("could not read duration of {}".format(path))
    h, mm, ss = m.groups()
    return int(h) * 3600 + int(mm) * 60 + float(ss)


def fetch(name: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    target = CACHE / name
    if target.exists():
        print("{}: already downloaded".format(name))
        return target
    print("{}: downloading...".format(name))
    urllib.request.urlretrieve(RELEASE + name, target)
    print("{}: {:.1f} MB".format(name, target.stat().st_size / 1e6))
    return target


def shrink(source: Path, name: str) -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    out = MEDIA / name
    if out.exists():
        print("{}: already encoded".format(name))
        return
    subprocess.run([
        FFMPEG, "-y", "-i", str(source),
        "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "30", "-preset", "slow", "-maxrate", "500k", "-bufsize", "1000k",
        "-vf", "scale=1280:-2,fps=24",
        "-c:a", "aac", "-b:a", "64k", "-ac", "1", "-ar", "24000",
        # faststart puts the index at the front, so playback can begin on the
        # first bytes instead of waiting for the whole file.
        "-movflags", "+faststart",
        str(out),
    ], check=True, capture_output=True)
    before = source.stat().st_size / 1e6
    after = out.stat().st_size / 1e6
    print("{}: {:.1f} MB -> {:.1f} MB ({:.0f}% smaller), {:.0f}s".format(
        name, before, after, 100 * (1 - after / before), duration_of(out)))


def main() -> None:
    for name in SOURCES:
        shrink(fetch(name), name)
    total = sum(f.stat().st_size for f in MEDIA.glob("*.mp4")) / 1e6
    print("\nmedia/ now holds {:.1f} MB across {} videos".format(
        total, len(list(MEDIA.glob("*.mp4")))))


if __name__ == "__main__":
    main()
