# THRIVE-Belize | Rotary Club of Punta Gorda

**Live presentation: <https://yeridu.github.io/rotary/>**

Share that address with the audience. It opens in any browser, on a phone or a laptop, with no login and nothing to install. Slide 15 shows the same address as a large QR code so the room can capture it during the talk.

A 16-slide talk for the Rotary Club of Punta Gorda, Toledo District, Belize, on the THRIVE-Belize adolescent life-skills feasibility study at Toledo Community College.

Adapted from the HPS 433 guest lecture deck ([THRIVE-Belize-GuestLecture](https://github.com/yeridu/THRIVE-Belize-GuestLecture)) for a service-club audience.

---

## Presenting

Open the live URL, or open `index.html` locally. Then:

| Key | Action |
|-----|--------|
| `→` / `Space` / `PageDown` | Next slide |
| `←` / `PageUp` | Previous slide |
| `Home` / `End` | First / last slide |
| `S` | Toggle speaker notes |
| `F` | Fullscreen |

Every slide carries speaker notes with a running time budget. The deck is built for a **20-minute slot plus questions**, which is the usual length of a Rotary guest-speaker segment. Confirm your slot with the club President before you start.

Slide layouts are verified to fit without scrolling at 1920x1080, 1600x900, 1366x768, 1280x720 and 1024x768.

## Before you present

1. **Confirm the meeting date and the President's name.** The deck deliberately carries no date; the speaker notes prompt you to thank the President by name.
2. **Optional video (slide 12).** Skip it by default. If you do want it, download `Morales2026THRIVE-Belize.mp4` from the [guest-lecture release](https://github.com/yeridu/THRIVE-Belize-GuestLecture/releases/tag/v1.0) and place it in the folder **directly above** this one. The deck tries the local file first, then streams from GitHub, and if neither is reachable it shows a short message instead of a dead player. Punta Gorda bandwidth is not reliable, so download it in advance.
3. **Print the handout.** `handout.md` is a one-page leave-behind carrying the same URL, the four asks, and the contact details.

## What changed from the guest-lecture version

The audience is not students who have never been to Belize; it is local business and community leaders who live in Punta Gorda. The adaptation reflects that:

- **Removed** the classroom apparatus: the three-video structure, pre-video prompts, the pair-share activity and countdown timer, the audio narration buttons, the Spotify player, and the map explaining where Belize is.
- **Added** slides built for this club: its own project record as the opening hook, a mapping of the seven THRIVE modules onto Rotary's seven areas of focus, the pre-specified stop criteria, the Four-Way Test applied to research ethics, the safeguarding response, four concrete asks, and a full sources slide.
- **Corrected** Mario Morales's title from PhD Candidate to Postdoctoral Research Associate, and team roles to the current composition.
- **Rewrote** every speaker note for a short civic slot rather than a 75-minute lecture.

## Accuracy

Every factual claim on a slide is traceable from slide 16. Notably:

- The club's charter date and project list come from the club's own weblog, `pgrotary.wordpress.com`. Its projects include furnishing the Hillside Healthcare Center, which is THRIVE-Belize's community health partner, and scholarships to Toledo high schools.
- Rotary's seven areas of focus, the Four-Way Test and the Interact age range are as published by Rotary International and The Rotary Foundation. **The mapping of THRIVE modules to areas of focus is the study team's, not Rotary's, and the deck says so on the slide.**
- Study facts (sample sizes, curriculum structure, progression criteria, safeguarding, approvals, registration) are taken from the BMJ Open protocol manuscript.
- Poverty figures are from the Statistical Institute of Belize Multidimensional Poverty Index.
- No meeting date, club officer name, membership figure, or club-specific commitment is asserted anywhere, because none could be verified at the time of writing.

One deliberate omission: the guest-lecture deck opened with a hand-drawn map of Belize. That was dropped rather than redrawn at district level, because presenting an approximate outline of Toledo to people who live there would be worse than showing no map at all. A study-at-a-glance panel takes its place.

## Repository layout

```
index.html              the deck
assets/css/styles.css   styling
assets/js/deck.js       navigation, speaker notes, video fallback
assets/qr-deck.svg      QR code for the live URL (offline, no tracking)
photos/                 partner and site photographs
handout.md              one-page leave-behind
```

## Regenerating the QR code

If the published URL ever changes, regenerate `assets/qr-deck.svg` (requires the `qrcode` Python package) and update the address on slides 1 and 15:

```bash
python scripts/make_qr.py
```
