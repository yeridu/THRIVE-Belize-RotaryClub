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


async def render(text: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    speech = edge_tts.Communicate(" ".join(text.split()), VOICE, rate=RATE)
    await speech.save(str(target))
    print("wrote {} ({:.0f} KB)".format(target.name, target.stat().st_size / 1024))


async def main() -> None:
    await render(SCORES, OUT / "scores.mp3")


if __name__ == "__main__":
    asyncio.run(main())
