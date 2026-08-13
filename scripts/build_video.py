"""Build the slide-4 video: what the evidence says, and what we did about it.

Replaces the 6:58 NotebookLM overview with a roughly three-minute version that
does the one job the slide needs: name the ten elements Jewkes and colleagues
found in successful violence-prevention programmes, and after each one say what
it made THRIVE-Belize do. Every element line matches slide 5 word for word, so
the video and the deck cannot drift apart.

Pipeline, all local except the voice: frames rendered by headless Chrome,
narration from Microsoft neural voices via edge-tts, assembly by the ffmpeg
binary bundled with imageio-ffmpeg. No NotebookLM, no install steps.

    python scripts/build_video.py

Output: Jewkes2021ElemOf_Video.mp4 in the folder ABOVE the deck, which is where
index.html looks for a local copy.
"""

import asyncio
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import edge_tts
import imageio_ffmpeg

DECK = Path(__file__).resolve().parent.parent
TARGET = DECK.parent / "Jewkes2021ElemOf_Video.mp4"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

VOICE = "en-US-AndrewNeural"
RATE = "+8%"
GAP = 0.7          # seconds of silence after each beat
W, H = 1280, 720

# kicker, headline, the THRIVE answer (None on framing beats), narration
BEATS = [
    ("Toledo Community College, Belize",
     "What actually makes prevention work",
     None,
     "Before we designed anything for Toledo Community College, we asked a "
     "simpler question. What separates a prevention programme that works from "
     "one that does not?"),

    ("The evidence",
     "Ten elements, from one review of what worked",
     None,
     "The best answer we found comes from Jewkes and colleagues, writing in "
     "twenty twenty-one. They looked across the What Works to Prevent Violence "
     "global programme and identified ten elements shared by the interventions "
     "that succeeded. Four are about design. Two are about implementation. Four "
     "more matter whenever the approach calls for them. Here they are, and after "
     "each one, what it made us do."),

    ("Design &middot; 1 of 10",
     "A plan built on a clear theory of change, fitted to the local context",
     "Designed from a survey of TCC's own students, with school climate as the mechanism",
     "One. A plan built on a clear theory of change, fitted to the local context. "
     "So we did not import a curriculum. We surveyed the students at this school "
     "first, and built the modules around what they reported."),

    ("Design &middot; 2 of 10",
     "Address several drivers of violence together",
     "Seven modules working as one system, not a single topic",
     "Two. Address several drivers of violence together, because they do not "
     "arrive one at a time. That is why THRIVE has seven modules working as one "
     "system rather than a single topic taught once."),

    ("Design &middot; 3 of 10",
     "Support for survivors",
     "The NSPCC 4Rs, a suicide-risk response pathway, and referrals agreed in advance",
     "Three. Support for survivors. If you ask young people about violence, some "
     "will tell you something serious. We follow the NSPCC four Rs, we have a "
     "defined response when a student discloses thoughts of suicide, and referral "
     "routes are agreed with local services before we ever walk into a classroom."),

    ("Design &middot; 4 of 10",
     "Work with men and women, boys and girls",
     "Whole-class delivery, plus a module on masculinities and boys' health",
     "Four. Work with men and women, boys and girls. Programmes that speak only "
     "to girls put the whole burden on them. THRIVE is taught to whole classes, "
     "and one of the seven modules is about masculinities and boys' health."),

    ("Implementation &middot; 5 of 10",
     "Enough intensity for people to reflect and practise",
     "Thirty sessions of forty minutes plus a booster, across the school year",
     "Five. Enough intensity for people to reflect and practise. A single "
     "assembly changes nothing. THRIVE is thirty sessions of forty minutes plus "
     "a booster, spread across the school year."),

    ("Implementation &middot; 6 of 10",
     "Enough well-selected, trained and supported staff",
     "At least two trained facilitators in year one, then teachers trained the year after",
     "Six. Enough well-selected, trained and supported staff. This is the element "
     "still under discussion. Our original plan was to train the teachers from the "
     "start. Best practice points the other way: bring in at least two trained "
     "facilitators for the first year, then train the teachers the year after, so "
     "the school can carry it without us. That choice is not settled, and it is one "
     "of the things the feasibility study is asking about."),

    ("Where relevant &middot; 7 of 10",
     "Group activities that build empowerment and good relationships",
     "Every session is activity-based, not a lecture",
     "Seven. Group activities that build empowerment and good relationships. "
     "Every THRIVE session is built around an activity rather than a lecture."),

    ("Where relevant &middot; 8 of 10",
     "Participatory learning: critical reflection and communication skills",
     "Debates, role-play and storytelling in each module",
     "Eight. Participatory learning, with critical reflection and communication "
     "skills. In practice that means debates, role-play and storytelling in "
     "every module."),

    ("Where relevant &middot; 9 of 10",
     "A clear, user-friendly manual, followed systematically",
     "A written facilitator manual covering all thirty sessions",
     "Nine. A clear, user-friendly manual, followed systematically, so that what "
     "is delivered is the thing that was designed. Ours is written and covers all "
     "thirty sessions."),

    ("Where relevant &middot; 10 of 10",
     "Age-appropriate design with an engaging pedagogy",
     "Written for Forms 1 to 4, ages twelve to seventeen",
     "Ten. Age-appropriate design, with a pedagogy that actually engages young "
     "people. THRIVE is written for Forms one to four, ages twelve to seventeen."),

    ("Where this leaves us",
     "We checked ourselves against all ten",
     None,
     "Ten elements, and an answer to each one. That is the standard we hold "
     "ourselves to, and it is a fair standard to hold us to as well. Whether the "
     "curriculum is right for Toledo is a separate question, and it is the one "
     "the feasibility study is asking now."),
]

FRAME = """<!doctype html>
<html><head><meta charset="utf-8"><style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{
  font-family: "Segoe UI", Arial, sans-serif;
  background: #FFFFFF; color: #111111;
  display: flex; flex-direction: column; justify-content: center;
  padding: 76px 90px;
}}
.rule {{ position: absolute; top: 0; left: 0; height: 7px; width: {pct}%; background: #E8630A; }}
.kicker {{
  font-size: 17px; font-weight: 700; letter-spacing: 0.2em;
  text-transform: uppercase; color: #E8630A; margin-bottom: 22px;
}}
h1 {{ font-size: {size}px; font-weight: 700; line-height: 1.13; letter-spacing: -0.02em; }}
.answer {{
  margin-top: 34px; padding: 20px 26px; background: #F5F5F5;
  border-left: 6px solid #E8630A; border-radius: 0 12px 12px 0;
}}
.answer .lbl {{
  display: block; font-size: 15px; font-weight: 700; letter-spacing: 0.16em;
  text-transform: uppercase; color: #888; margin-bottom: 7px;
}}
.answer p {{ font-size: 27px; line-height: 1.4; color: #333; }}
.foot {{
  position: absolute; left: 90px; bottom: 44px;
  font-size: 15px; color: #AAAAAA;
}}
</style></head><body>
<div class="rule"></div>
<div class="kicker">{kicker}</div>
<h1>{headline}</h1>
{answer}
<div class="foot">{foot}</div>
</body></html>
"""

ANSWER = '<div class="answer"><span class="lbl">What we did</span><p>{}</p></div>'
FOOT = ("Jewkes R, Willan S, Heise L, et al. Int J Environ Res Public Health 2021;18:12129 "
        "&middot; THRIVE-Belize")


def duration_of(path: Path) -> float:
    """Seconds, read back out of ffmpeg's own report on the file."""
    out = subprocess.run([FFMPEG, "-i", str(path)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", out)
    if not m:
        raise SystemExit("could not read duration of {}".format(path))
    h, mm, ss = m.groups()
    return int(h) * 3600 + int(mm) * 60 + float(ss)


def render_frames(work: Path) -> list:
    frames = []
    for i, (kicker, headline, answer, _) in enumerate(BEATS):
        html = FRAME.format(
            w=W, h=H,
            pct=round(100 * (i + 1) / len(BEATS), 2),
            size=54 if answer else 62,
            kicker=kicker,
            headline=headline,
            answer=ANSWER.format(answer) if answer else "",
            foot=FOOT,
        )
        page = work / "frame{:02d}.html".format(i)
        page.write_text(html, encoding="utf-8")
        png = work / "frame{:02d}.png".format(i)
        subprocess.run([
            str(CHROME), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--window-size={},{}".format(W, H), "--virtual-time-budget=2000",
            "--screenshot={}".format(png), page.as_uri(),
        ], capture_output=True)
        if not png.exists():
            raise SystemExit("Chrome did not render {}".format(png.name))
        frames.append(png)
        print("frame {:02d} rendered".format(i))
    return frames


async def render_audio(work: Path) -> list:
    clips = []
    for i, (_, _, _, script) in enumerate(BEATS):
        mp3 = work / "beat{:02d}.mp3".format(i)
        speech = edge_tts.Communicate(" ".join(script.split()), VOICE, rate=RATE)
        await speech.save(str(mp3))
        clips.append(mp3)
        print("audio {:02d} rendered ({:.1f}s)".format(i, duration_of(mp3)))
    return clips


def main() -> None:
    if not CHROME.exists():
        raise SystemExit("Chrome not found at {}".format(CHROME))

    work = Path(tempfile.mkdtemp(prefix="thrive_video_"))
    try:
        frames = render_frames(work)
        clips = asyncio.run(render_audio(work))

        # A short silence after each beat, so the narration does not run on.
        silence = work / "gap.mp3"
        subprocess.run([
            FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
            "-t", str(GAP), "-q:a", "9", str(silence),
        ], capture_output=True)

        audio_list = work / "audio.txt"
        video_list = work / "video.txt"
        with audio_list.open("w", encoding="utf-8") as af, video_list.open("w", encoding="utf-8") as vf:
            total = 0.0
            for png, mp3 in zip(frames, clips):
                hold = duration_of(mp3) + GAP
                total += hold
                af.write("file '{}'\nfile '{}'\n".format(mp3.as_posix(), silence.as_posix()))
                vf.write("file '{}'\nduration {:.3f}\n".format(png.as_posix(), hold))
            # concat's demuxer ignores the final duration unless the file repeats
            vf.write("file '{}'\n".format(frames[-1].as_posix()))

        subprocess.run([
            FFMPEG, "-y",
            "-f", "concat", "-safe", "0", "-i", str(video_list),
            "-f", "concat", "-safe", "0", "-i", str(audio_list),
            "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-r", "24", "-vf", "scale={}:{}".format(W, H),
            "-c:a", "aac", "-b:a", "96k", "-ac", "1",
            "-shortest", "-movflags", "+faststart", str(TARGET),
        ], check=True, capture_output=True)

        mins, secs = divmod(duration_of(TARGET), 60)
        print("\nwrote {}".format(TARGET))
        print("{:d}:{:04.1f}, {:.1f} MB (narration totalled {:.1f}s)".format(
            int(mins), secs, TARGET.stat().st_size / 1e6, total))
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
