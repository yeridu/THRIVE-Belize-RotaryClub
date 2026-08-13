# THRIVE-Belize | Rotary Club of Punta Gorda

**Live presentation: <https://yeridu.github.io/THRIVE-Belize-RotaryClub/>**

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

Every slide carries speaker notes with a running time budget. The deck is built for a **25-minute slot plus questions**. Confirm your slot with the club President before you start.

Text is sized to be read from about six metres. Slides fit the screen automatically. On a short projector the denser slides scale themselves down until every line is visible, so nothing falls below the fold and there is never anything to scroll mid-sentence. Verified at 1920x1080, 1600x900, 1366x768, 1280x720 and 1024x768.

## Slide order

| # | Slide | Media |
|---|-------|-------|
| 1 | Title, the name spelled out, study at a glance | |
| 2 | The four phases | |
| 3 | The connection between Rotary and THRIVE | **audio** |
| 4 | What 497 TCC students told us, ranked | |
| 5 | Risks do not arrive one at a time | charts |
| 6 | Pain without help, and what we changed | charts |
| 7 | Ten elements of prevention that works, and our answer to each | video, 2:56 |
| 8 | Seven modules across four of Rotary's causes | |
| 9 | Phase 1: what it is, and recruitment to date | |
| 10 | How the scores work, and the published stop criteria | **audio** |
| 11 | THRIVE-Belize in five minutes | video |
| 12 | One module opened up: masculinities and boys' health | video |
| 13 | Gratitude | |
| 14 | Team and partners | |
| 15 | Thank you, acknowledgements, QR code | |
| 16 | Sources (not presented) | |

Slides 3 and 10 carry recorded narration. Press Listen and let it play; it stops by itself when you move on.

## Before you present

1. **Set the meeting date and confirm the President's name.** The date lives in one place only: the label on slide 1, marked with a comment in `index.html`. It currently reads 13 August 2026. The speaker notes prompt you to thank the President by name.
2. **Update the recruitment counts on slide 9.** They are a live count with the date printed beside them. Refresh both from the Phase 1 data-entry workbooks before presenting, or the slide will understate the study.
3. **Nothing to download, but do open it locally.** All three videos live in `media/` inside this repository, about 17 MB in total, and nothing streams from anywhere. On a weak connection, do not present from the live URL: download the repository once (green Code button, Download ZIP), unzip it, and open `index.html` from disk. Then no part of the talk touches the network.

4. **Print the handout.** `handout.md` is a one-page leave-behind carrying the same URL and the contact details.

## Accuracy

Every factual claim on a slide is traceable from slide 16. Notably:

- The club's charter date and project list come from the club's own weblog, `pgrotary.wordpress.com`.
- Rotary's seven areas of focus, and the scope quoted on slide 8, are from The Rotary Foundation's **Areas of Focus Policy Statements (October 2020)**, including the two eligibility limits the slide names. **The mapping of THRIVE modules to areas of focus is the study team's, not Rotary's, and the deck says so on the slide.**
- Every percentage attributed to TCC students comes from the Phase 0 needs assessment: a census-style survey of Forms 1-3 in May 2025, 86.5% participation, 497 students analysed.
- The ten elements in the slide 7 video are Jewkes et al. 2021 (Int J Environ Res Public Health 18:12129), restated in plain language and grouped exactly as the paper groups them; the THRIVE line beside each element is the study team's.
- Study facts (curriculum structure, target sample sizes, progression criteria, safeguarding, approvals, registration) are from the study protocol.
- The recruitment counts on slide 9 come from the four Phase 1 data-entry workbooks, consolidated into `tccphase1data0_summary.xlsx`, with the count date printed on the slide.
- Poverty figures are from the Statistical Institute of Belize Multidimensional Poverty Index.
- No club officer name, membership figure, or club-specific commitment is asserted anywhere, because none could be verified. The only club-specific fact on a slide is the meeting date on slide 1, which comes from the speaker.

## Repository layout

```
index.html                              the deck
assets/css/styles.css                   styling
assets/js/deck.js                       navigation, speaker notes, auto-fit, video fallback
assets/qr-deck.svg                      QR code for the live URL (offline, no tracking)
photos/                                 partner and site photographs
media/                                  all three videos, about 17 MB, no streaming
assets/audio/                           slide 3 and slide 10 narration
handout.md                              one-page leave-behind
scripts/make_qr.py                      regenerates the QR code
scripts/build_offline.py                regenerates the single-file offline copy
scripts/build_narration.py              regenerates the slide 8 narration (edge-tts)
scripts/build_video.py                  regenerates the slide 7 video (Chrome + edge-tts + ffmpeg)
scripts/build_media.py                  re-encodes the two large videos into media/
THRIVE-Belize-RotaryClub-OFFLINE.html    single file, no network needed (videos excluded)
```

## Regenerating the build artefacts

After editing `index.html`, the stylesheet, the script or the photographs, rebuild the offline copy so the two do not drift apart:

```bash
python scripts/build_offline.py
```

If the published URL ever changes, regenerate `assets/qr-deck.svg` (requires the `qrcode` Python package) and update the address on slides 1 and 15:

```bash
python scripts/make_qr.py
```
