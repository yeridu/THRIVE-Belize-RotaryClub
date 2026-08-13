"""Generate the spoken narration for the deck.

Uses Microsoft neural voices through edge-tts, not the Windows SAPI voices,
because SAPI sounds robotic and this is played to a room of people.

Run from anywhere:

    python scripts/build_narration.py
"""

import asyncio
from pathlib import Path

import edge_tts

DECK = Path(__file__).resolve().parent.parent
OUT = DECK / "assets" / "audio"

VOICE = "en-US-AndrewNeural"
RATE = "-6%"   # a little slower than default; this is an explanation, not an advert

# Slide 9 -- how the scoring works. Kept short on purpose: the earlier cut ran
# over a minute and a half, which is longer than a room will hold still for.
SCORES = """
Here is how the scoring works, in under a minute.

Every question uses the same five point scale. One is strongly disagree.
Five is strongly agree.

We average one person's answers within one section. We then average those
across everyone in the group. That gives one number per group.

Now the part that matters. We score three things separately: do you want it,
does it fit here, and can the school run it. We never add them together,
because a high score in one must not hide a low score in another. The weakest
of the three decides the colour.

Three point five or above on all three means the average person agreed, and we
go ahead. Below three point zero on any one of them means we stop.

We wrote those lines down before we collected a single answer.
"""


# Slide 3 -- the club's own projects, and how THRIVE connects to them.
# Neither presenter is comfortable delivering this one, so it is written to be
# played to the room as it stands, not read over.
ROTARY_LINK = """
For those who do not know this club's record, here is a little of it, and why
it brought us to you.

Since the club was chartered in two thousand and eight, the Rotary Club of
Punta Gorda has furnished the dormitory at Hillside Health Care, working with
the Rotary Club of Columbus, Indiana. It has paid scholarships that send local
students through high school. It has given dictionaries, run school feeding
programmes, renovated the library, and built water systems, a wastewater
garden at the hospital, and solar latrines in villages that flood.

Look at that list and a pattern shows up. Almost all of it is about young
people, and almost all of it removes something that stops a child learning.
Hunger. Distance from clean water. School fees. No book to read.

THRIVE-Belize starts where that work leaves off. Hillside, the clinic you
furnished, is our health partner: it is where a student who needs care
actually goes. The scholarships you pay send students to Toledo Community
College, which is the school we work in. The villages your water projects
reach are the villages those students come from.

So we are not arriving with something unconnected. You have spent years
building the things young people here need, and we would like to work with you
on the part that comes next, which is teaching them the skills to use it.

Everything in that list comes from the club's own weblog, and every link is on
the final slide.
"""


async def render(text: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    speech = edge_tts.Communicate(" ".join(text.split()), VOICE, rate=RATE)
    await speech.save(str(target))
    print("wrote {} ({:.0f} KB)".format(target.name, target.stat().st_size / 1024))


async def main() -> None:
    await render(SCORES, OUT / "scores.mp3")
    await render(ROTARY_LINK, OUT / "rotary-link.mp3")


if __name__ == "__main__":
    asyncio.run(main())
