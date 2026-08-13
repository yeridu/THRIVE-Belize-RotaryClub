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

# Slide 8 -- how a score is built, and how the three sections combine.
SCORES = """
Here is how we turn what people tell us into a number, in plain terms.

Every question uses the same five point scale. One means strongly disagree.
Five means strongly agree. Three means not sure.

First, we take one person and one section of the survey. A student answering
the acceptability section answers four statements. We average those four
answers, and that gives us that student's acceptability score. In the example
on the screen, four plus five plus four plus three, divided by four, is four
point zero.

Second, we average those personal scores across everyone in the group. That
gives us one number for students, one for parents, one for teachers, and so on.

Now the part people usually expect us to do, and the part we deliberately do
not do. We never add the three sections together into a single overall score.
Acceptability, appropriateness and feasibility are read separately, each
against the same threshold, and the weakest of the three decides the colour.

The reason is simple. A high score in one section must not be allowed to hide
a low score in another. If everybody wants the curriculum, and it fits Belize,
but the school cannot realistically run it, that is not a green light. It is
an amber one, and what needs fixing is the running of it.

Three point five or above on all three, and the average person agreed. Below
three point zero on any one of them, and the average person was not sure or
worse. We wrote those lines down before we collected a single answer.
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
