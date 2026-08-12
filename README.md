# THRIVE-Belize | Rotary Club of Punta Gorda

**Live presentation: <https://yeridu.github.io/THRIVE-Belize-RotaryClub/>**

Share that address with the audience. It opens in any browser, on a phone or a laptop, with no login and nothing to install. Slide 13 shows the same address as a large QR code so the room can capture it during the talk.

A 14-slide talk for the Rotary Club of Punta Gorda, Toledo District, Belize, on the THRIVE-Belize adolescent life-skills feasibility study at Toledo Community College.

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

Every slide carries speaker notes with a running time budget. The deck is built for a **25-minute slot plus questions**. Confirm your slot with the club President before you start.

Slides fit the screen automatically. On a short projector the denser slides scale themselves down until every line is visible, so nothing falls below the fold and there is never anything to scroll mid-sentence. Verified at 1920x1080, 1600x900, 1366x768, 1280x720 and 1024x768.

## Slide order

| # | Slide | Video |
|---|-------|-------|
| 1 | Title, study at a glance, and the four project phases | |
| 2 | What this club has already built here | |
| 3 | The problem, as a chain: conditions, then research, then what TCC students reported | |
| 4 | The ten evidence-based elements of prevention that works, and how THRIVE answers each | Jewkes 2021 |
| 5 | Each module against the survey finding behind it, and the Rotary area of focus | |
| 6 | Phase 1: what it is, and recruitment to date | |
| 7 | How the scores are calculated, and the published stop criteria | |
| 8 | THRIVE-Belize in five minutes | Curriculum overview |
| 9 | The seven modules on one screen | |
| 10 | One module opened up: masculinities and boys' health | The Man Box |
| 11 | Four things to explore together, none needing a decision today | |
| 12 | Team and partners | |
| 13 | Close, with the QR code | |
| 14 | Sources (not presented) | |

Slides 8, 9 and 10 are one unit: the first video says what THRIVE is, slide 9 names the seven modules, and the second video opens one of them.

## Before you present

1. **Set the meeting date and confirm the President's name.** The date lives in one place only: the label on slide 1, marked with a comment in `index.html`. It currently reads 13 August 2026. The speaker notes prompt you to thank the President by name.
2. **Update the recruitment counts on slide 6.** They are a live count with the date printed beside them. Refresh both from the Phase 1 data-entry workbooks before presenting, or the slide will understate the study.
3. **Download the three videos.** From the [guest-lecture release](https://github.com/yeridu/THRIVE-Belize-GuestLecture/releases/tag/v1.0), take `Jewkes2021ElemOf_Video.mp4` (slide 4), `Morales2026THRIVE-Belize.mp4` (slide 8) and `Morales2026TheManBox.mp4` (slide 10), and place all three in the folder **directly above** this one. The deck tries the local file first, then streams from GitHub, and if neither is reachable it shows a short message instead of a dead player. Punta Gorda bandwidth is not reliable, so download them in advance. Slides 4 and 9 carry the same content as their videos in text, so the talk survives if a video will not play.
4. **Print the handout.** `handout.md` is a one-page leave-behind carrying the same URL and the contact details.

## Accuracy

Every factual claim on a slide is traceable from slide 14. Notably:

- The club's charter date and project list come from the club's own weblog, `pgrotary.wordpress.com`.
- Rotary's seven areas of focus, and the scope quoted on slide 5, are from The Rotary Foundation's **Areas of Focus Policy Statements (October 2020)**, including the two eligibility limits the slide names. **The mapping of THRIVE modules to areas of focus is the study team's, not Rotary's, and the deck says so on the slide.**
- Every percentage attributed to TCC students comes from the Phase 0 needs assessment: a census-style survey of Forms 1-3 in May 2025, 86.5% participation, 497 students analysed.
- The ten elements on slide 4 are Jewkes et al. 2021 (Int J Environ Res Public Health 18:12129), restated in plain language and grouped exactly as the paper groups them; the THRIVE line beside each element is the study team's.
- Study facts (curriculum structure, target sample sizes, progression criteria, safeguarding, approvals, registration) are from the study protocol.
- The recruitment counts on slide 6 come from the Phase 1 data-entry workbooks, with the count date printed on the slide.
- Poverty figures are from the Statistical Institute of Belize Multidimensional Poverty Index.
- No club officer name, membership figure, or club-specific commitment is asserted anywhere, because none could be verified. The only club-specific fact on a slide is the meeting date on slide 1, which comes from the speaker.

## Repository layout

```
index.html                              the deck
assets/css/styles.css                   styling
assets/js/deck.js                       navigation, speaker notes, auto-fit, video fallback
assets/qr-deck.svg                      QR code for the live URL (offline, no tracking)
photos/                                 partner and site photographs
handout.md                              one-page leave-behind
scripts/make_qr.py                      regenerates the QR code
scripts/build_offline.py                regenerates the single-file offline copy
THRIVE-Belize-RotaryClub-OFFLINE.html    single file, no network needed (videos excluded)
```

## Regenerating the build artefacts

After editing `index.html`, the stylesheet, the script or the photographs, rebuild the offline copy so the two do not drift apart:

```bash
python scripts/build_offline.py
```

If the published URL ever changes, regenerate `assets/qr-deck.svg` (requires the `qrcode` Python package) and update the address on slides 1 and 13:

```bash
python scripts/make_qr.py
```
