# MrBeast's Thumbnails, the Science Behind Them, and a Roblox Thumbnail & Icon Playbook

*Study of 389 MrBeast thumbnails (2016–2026) measured with `bpe thumbs`, cross-checked against
published attention research, MrBeast's stated process, and Roblox's own thumbnail and icon
rules. Data: [`benchmark.json`](benchmark.json), [`dataset.json`](dataset.json). Images stay in
the local cache; they are MrBeast's, not ours to redistribute.*

---

## 1. The short version

| # | Principle | Evidence | Roblox translation |
|---|---|---|---|
| 1 | **One idea per image** | 0–1 focal regions: median ×1.14 vs ×0.92 for 4+ (2022+, ρ = −0.27, p = 0.006); gist is extracted in as little as 13 ms | One hero + one hook object, nothing else competing |
| 2 | **Show a contrast or a stake** | "$1 vs $X" split-screens ×1.38 vs ×0.95; cash-stake concepts ×1.16 vs ×0.90 | Level 1 vs level 100, tiny vs giant, safe vs lava, noob base vs pro base |
| 3 | **Text is a number, not a sentence** | 1–2 OCR tokens ×1.12 vs ×0.92 with none; text draws gaze 11× more than matched regions | 0–2 tokens, ideally a game number ("DAY 99", "LVL 1000"); never claims like "FREE" or "50% OFF" |
| 4 | **Faces: big, few, natural** | Largest face ≈10–13% of frame since 2022; 3+ faces ×0.83 vs ×1.05 for one; closed-mouth versions won his A/B tests | One expressive avatar, large, looking at the hook; no crowds |
| 5 | **Saturated, bright mid-tones** | 2022+ medians: colourfulness 78.5, saturation 0.40, lightness 55 | Rich colour with a value gap between subject and background |
| 6 | **Avoid clutter, keep it composed** | Dense detail lowers attention; designed composition raises it (Pieters et al. 2010) | Simple backgrounds, depth of field, rim light on the hero |
| 7 | **Design for the smallest size it appears at** | Roblox icons drop to 150×150; mobile legibility is "the most common mistake" | Run the squint test; keep the bottom 15% clear |
| 8 | **Promise only what you deliver** | Thumbnail must match the video (MrBeast guide); Roblox ranks on *qualified* play-through | Real in-game imagery of the real hook |
| 9 | **Generate many concepts, test, refresh** | Dozens of concepts per video and constant A/B tests; YouTube picks winners by watch time | 2–5 active thumbnails in personalisation (+8.5% avg); new set each update |

The single most important caveat: **inside MrBeast's catalog, low-level pixel statistics explain
very little.** The video *idea* drives outliers, and every thumbnail is already A/B-optimised. Copy
his *process* and *composition rules*, not his colour histogram.

---

## 2. Data and method

- **Corpus:** the 400 most recent long-form uploads on [@MrBeast](https://www.youtube.com/@MrBeast/videos)
  (526M subscribers; listing fetched 2026-11-11), of which 389 were analysed. Thumbnails were
  downloaded at 1280×720 where available.
- **Performance = outlier ratio:** a video's views ÷ the median views of its 20 chronological
  neighbours. This controls for channel growth, so a 2018 video is judged against 2018. Videos
  under 30 days old are excluded (387 eligible; 99 from 2022+).
- **Features** (see `src/blueprint_engine/visual/features.py`):
  - CIELAB lightness and RMS contrast
  - HSV saturation
  - Hasler–Süsstrunk colourfulness
  - k-means palette
  - Canny edge density and JPEG size (visual-complexity proxies)
  - An attention map averaging spectral-residual (Hou & Zhang 2007) and frequency-tuned
    (Achanta et al. 2009) saliency, from which focal regions, concentration and the
    bottom-strip share are computed
  - Haar face detection
  - Tesseract OCR on white/yellow text masks
  - Contrast after a heavy blur ("squint contrast")
- **Statistics:** Spearman correlation with log₂(outlier), with permutation p-values (10,000
  shuffles), plus bucket medians. Eighteen features were tested, so single results near
  p = 0.05 are weak. A strict Holm correction is applied in the text.
- **Visual coding:** the top and bottom 16 performers of 2022+ were reviewed by eye for concept,
  composition, text and expression.
- **Detector limits:** face detection misses profiles and some stylised faces; OCR misses some
  stylised lettering and adds occasional noise. Treat face and text numbers as approximate.

---

## 3. What MrBeast's thumbnails look like, and how they changed

| Era | n | Colourfulness | Saturation | Lightness | Has a face | Largest face (median) | Edge density | Text present |
|---|---|---|---|---|---|---|---|---|
| 2016–2018 | 151 | 51 | 0.28 | 51 | 45% | 0% | 0.065 | 58% |
| 2019–2021 | 139 | 74 | 0.35 | 56 | 73% | 3.5% | 0.106 | 51% |
| 2022–2024 | 54 | 77 | 0.38 | 57 | 76% | 10.1% | 0.121 | 59% |
| 2025–2026 | 45 | 79 | 0.42 | 54 | 93% | 12.8% | 0.135 | 53% |

The house style converged on a **large single face (10–13% of the frame) in front of a
richly detailed, saturated, evenly lit set**, with **short, heavy white text that is usually a
number**. Colour went from muted (colourfulness 51) to vivid (79). The face went from absent to
dominant. Backgrounds got more detailed (edge density doubled), yet each image still reads as one
idea, because the detail sits in the background and the subject is separated by lightness, scale
and focus.

---

## 4. What tracked performance (2022+, n = 99)

### Concept (from titles)

| Concept | n | Median outlier with | Without |
|---|---|---|---|
| Price contrast ("$1 vs $X") | 12 | **×1.38** | ×0.95 |
| Cash stakes ("Win $…", "for $…") | 54 | **×1.16** | ×0.90 |
| Endurance (days, survive, trapped) | 33 | ×1.01 | ×0.97 |
| Philanthropy | 5 | ×0.91 | ×1.01 |
| Crowds ("50 YouTubers", "every country") | 11 | ×0.96 | ×1.01 |

### Composition (measured)

| Feature | Buckets (median outlier) | ρ, p |
|---|---|---|
| Focal regions | 0–1: **×1.14** (17) · 2–3: ×1.01 (44) · 4+: ×0.92 (38) | −0.27, 0.006 |
| Faces detected | 0: ×1.15* (16) · 1: ×1.05 (44) · 2: ×1.01 (17) · 3+: **×0.83** (22) | −0.19, 0.061 |
| Overlay text tokens | 0: ×0.92 (43) · 1–2: **×1.12** (50) · 3+: ×1.10 (6) | text area +0.30, 0.003 |
| Squint contrast | higher contrast slightly *worse* | −0.20, 0.049 |

\*"0 faces" includes faces the detector missed (profiles, faces in motion).

**Reading this honestly.** These are within-channel correlations on 99 videos. The three
strongest (text area, focal regions, squint contrast) agree with each other and with the visual
review, but none clears a strict multiple-comparison correction. Across all eras (n = 387) no
feature exceeds |ρ| = 0.11. The size of these effects is smaller than the concept effect.

### What the eye sees (top 16 vs bottom 16, 2022+)

- **Top performers** are one idea in one glance:
  - Split-screen **contrasts** with only "$1" and "$1M" as text:
    [hotel](https://www.youtube.com/watch?v=iogcY_4xGjo), [yacht](https://www.youtube.com/watch?v=48h57PspBec), [plane](https://www.youtube.com/watch?v=1WEAJ-DFkHE)
  - A **progress counter** on a suffering hero ("DAY 201", "DAY 97"):
    [grocery store](https://www.youtube.com/watch?v=plN7JMbadRg), [island](https://www.youtube.com/watch?v=erLbbextvlY), [trapped](https://www.youtube.com/watch?v=9RhWXPcKBI8)
  - An **instantly recognisable reference**:
    [Squid Game mask](https://www.youtube.com/watch?v=0e3GPea1Tyg) (×3.93, 982M views), [Wonka factory](https://www.youtube.com/watch?v=Hwybp38GnZw), [Ronaldo head-to-head](https://www.youtube.com/watch?v=0BjlBnfHcHM)
  - Stakes shown **on the body**: dirt, sweat, chains, a hand reaching at the camera.
- **Bottom performers** ask the eye to do more work:
  - **Crowds of faces**: [5 YouTubers](https://www.youtube.com/watch?v=x9TQ6culXIA), [rows of flags](https://www.youtube.com/watch?v=J_z-W4UVHkw), [three explorers](https://www.youtube.com/watch?v=bn0Kh9c4Zv4)
  - **Multi-object scenes**: [money pile + tanks](https://www.youtube.com/watch?v=7ESeQBeikKs), [dominoes + arrow + store](https://www.youtube.com/watch?v=vBpQ1SlfVtU)
  - Even these drew 100–300M views. "Bottom" means relative to MrBeast.

---

## 5. MrBeast's stated process

- **Packaging comes first.** The leaked onboarding guide *How to Succeed in MrBeast Production*
  (authenticity unconfirmed) names CTR, average view duration and average view percentage as the
  core metrics. It describes the creative process starting from the title and thumbnail, and it
  says the video must deliver what the thumbnail promises
  ([Creator Handbook](https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/),
  [Simon Willison](https://simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production/)).
- **Many concepts, then test.** Interview recaps describe the team drafting dozens of
  title/thumbnail variations per video (figures of ~40–50 are reported second-hand), testing big
  swings first and then refining
  ([Jon Youshaei interview recap](https://recapio.com/digest/why-every-mrbeast-video-gets-200m-views-interview-by-jon-youshaei)).
- **The closed-mouth result.** On 6 Sept 2023 he posted: *"I closed my mouth on all my thumbnails
  and the watch time went up on every video lol… Now that I can actually A/B test thumbnails I
  don't have to guess."* No metrics were published
  ([Creative Bloq](https://www.creativebloq.com/news/youtube-thumbnails),
  [Creator Handbook](https://www.creatorhandbook.net/mrbeast-claims-closing-his-mouth-in-thumbnails-is-better-for-views/)).
- **What "winning" means on YouTube.** Test & Compare chooses winners by **watch-time share, not
  click-through rate**, because a pure CTR winner can attract clicks that don't watch
  ([YouTube Help](https://support.google.com/youtube/answer/13861714)). Roblox's personalisation
  likewise optimises **qualified play-through rate**, not raw clicks. On both platforms the
  thumbnail must earn the click *and* set the right expectation.

---

## 6. The science behind it

| Mechanism | Finding | Design consequence |
|---|---|---|
| **Gist in milliseconds** | People can detect a named picture's meaning at 13 ms per picture in rapid sequences ([Potter et al. 2014](https://pubmed.ncbi.nlm.nih.gov/24374558/)) | Feed decisions are near-instant: one readable idea beats an intricate scene |
| **Faces and text grab gaze** | Viewers fixated faces 16.6× and text 11.1× more than size- and position-matched regions, even when it cost them on the task ([Cerf, Frady & Koch 2009](https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264)) | Every face and word is spent attention. Use few, make them big, make them count |
| **Gaze steers attention** | Seen gaze direction shifts observers' attention reflexively, even when uninformative ([Friesen & Kingstone 1998](https://psych.unl.edu/mdodd/Psy498/FriesenKingstone.pdf); Driver et al. 1999) | Point the hero's eyes (or body) at the hook object |
| **Emotion prioritises** | Emotional stimuli get privileged processing via amygdala feedback to sensory cortex ([Vuilleumier 2005](https://archive-ouverte.unige.ch/unige:10486)) | A clear expression (determination, awe, joy) on one face. MrBeast found closed-mouth expressions won on watch time |
| **Two kinds of complexity** | Dense perceptual detail ("feature complexity") lowers attention to the message, while an elaborate but organised design raises it ([Pieters, Wedel & Batra 2010](https://repository.tilburguniversity.edu/items/3fddf97a-469e-4d38-9c26-8dbd00c750b2)). A 1% rise in JPEG file size cut brand attention by about 0.5%, per the authors' summary | Detailed worlds are fine if the subject is separated; random clutter is not |
| **Curiosity gap** | Curiosity arises from a perceived gap in knowledge, and needs some initial knowledge to form ([Loewenstein 1994](https://www.cmu.edu/dietrich/sds/docs/loewenstein/PsychofCuriosity.pdf)) | Show the setup and the stakes ("DAY 97", one second before the wave hits) but not the outcome |
| **Faces aren't magic** | Across 300K viral videos, thumbnails with and without faces performed similarly, varying by niche ([Search Engine Journal](https://www.searchenginejournal.com/do-faces-help-youtube-thumbnails-heres-what-the-data-says/563944/)) | A face helps when it carries the emotion of the hook. For many Roblox games the hook object is the star |

---

## 7. Roblox playbook: thumbnails (16:9) and icon (square)

### 7.1 Hard requirements (Roblox docs)

| | Thumbnail | Icon |
|---|---|---|
| Size | 16:9, ideally **1920×1080**, under 3 MB; non-16:9 uploads are stretched | Square, at least **512×512**; shown down to **~150×150** |
| Count | Up to 10 on the detail page; **2–5 active** for Home personalisation | One per locale |
| Placement | Keep essential content out of the **bottom strip** (player count overlay) | Preview at small sizes |
| Content | Unique, relevant imagery of what players will get; avoid ambiguous graphics. For videos: real gameplay, no claims like "50% off" or "Free UGC!" | Express theme, tone and genre; unique and relevant |
| Required for Home | Since 2026-10-19, only games with a **custom thumbnail** get Home recommendation impressions | — |

Sources: [Thumbnails](https://create.roblox.com/docs/production/publishing/thumbnails),
[Icons](https://create.roblox.com/docs/production/publishing/experience-icons),
[DevForum: custom thumbnail requirement](https://devforum.roblox.com/t/homepage-recommendation-eligibility-now-requires-a-custom-thumbnail/4945086).

### 7.2 Five thumbnail archetypes (MrBeast patterns, Roblox-native)

Make one of each and activate them together in personalisation. Each tests a different *reason
to click*, which is what personalisation needs to learn whom each one works for.

| Archetype | MrBeast original | Roblox version | Text (≤2 tokens) |
|---|---|---|---|
| **Progression contrast** | $1 vs $1M hotel (split screen) | Starter base vs maxed base; level-1 pet vs mythic pet, same pose | "LVL 1" / "LVL 1000" |
| **Stakes moment** | Hand reaching at camera, island "DAY 6" | Hero one beat before the hazard lands (tsunami, boss swing, lava rise) | none, or the timer |
| **Scale spectacle** | Ronaldo head-to-head; giant yacht | Small avatar vs the enormous thing (titan boss, mega-pet, tower) | none |
| **Progress counter** | "DAY 201" grocery store | Survivor after night 99, base on wave 50, stacked rebirths | "NIGHT 99" |
| **Signature mechanic** | Squid Game mask (instantly recognisable) | Close-up of the one verb only your game has, mid-action | none |

**Composition rules for every archetype:**
- **One hero avatar**, about 10–15% of the frame for the face/head (MrBeast's median is 10–13%).
  Use an expressive dynamic-head expression, and closed-mouth determination or awe rather than a
  default face. **Aim the gaze at the hook.**
- **One hook object**, the second-largest element. Nothing else competes; push the background
  back with depth of field, haze or darker values.
- **Value separation:** a rim light or bright subject on a darker background (or the reverse) so
  the image survives the squint test.
- **Palette:** 2–3 saturated hues plus one accent. MrBeast's 2022+ benchmark is colourfulness
  ≥ 65 (25th percentile), saturation ≥ 0.33 and lightness around 50–60.
- **Text:** 0–2 tokens, heavy weight with an outline, top third, ideally a game number. No "FREE",
  "ROBUX", "50% OFF", "ADMIN", "UGC". Sparse descriptive context is fine; claims are not.
- **Bottom 15% empty** of anything that matters.
- **Authentic:** render it from the real game (Studio freecam, real assets). If the thumbnail
  over-promises, qualified play-through drops and so does distribution.

### 7.3 Icon rules

- **One subject, centred and large** (start around 60% of the frame): your hero, mascot or the hook object.
  Icons are squares that shrink to 150 px, so a split screen or a scene will not read.
- **One-colour or simple gradient background** with a strong value contrast to the subject. Use
  saturated colours from the thumbnail palette so icon and thumbnails feel like one brand.
- **No text, or one short word.** Small lettering vanishes at 150 px; check it in the preview sheet.
- **Silhouette test:** fill the subject black on white. If you can still tell what it is, the icon
  works at 64–150 px.
- **Keep it stable** across updates so returning players recognise it (design judgement). Rotate
  thumbnails freely; change icons rarely.

### 7.4 Workflow

1. Write the one-sentence promise: what the player *does and feels* in the first five minutes.
2. Brainstorm 15–20 thumbnail concepts across the five archetypes (MrBeast drafts dozens), then
   sketch the best five as quick paint-overs.
3. Capture in Studio: freecam, a hero pose with expression, rim light, and real assets at 1920×1080.
4. QA each file:
   ```bash
   bpe thumbs score thumb_progression.png                 # 16:9 checks + preview sheet
   bpe thumbs score icon_v1.png --kind icon               # square, centred, 150/100/64 px previews
   ```
   Fix every FAIL and decide on each WARN. Open the preview sheet: does it read at 160×90 and
   in greyscale?
5. Upload all five and activate them for personalisation. Leave them for at least a few days;
   Roblox recommends not removing an early loser too soon, because rankings shift.
6. With each update, replace the weakest one or two with new concepts. Refresh when CTR decays,
   which creator data shows can happen within a week.

### 7.5 Pre-upload checklist

- [ ] 1920×1080 (thumbnail) or ≥512×512 square (icon); under 3 MB
- [ ] One idea; 1–2 focal regions; hero + hook only
- [ ] Hero's face large and expressive, looking at the hook; no crowds
- [ ] 0–2 text tokens, a number if possible, no promotional claims
- [ ] Reads at 160×90 / 150×150, in the squint test and in greyscale
- [ ] Bottom 15% clear
- [ ] Shows real gameplay and a real hook that the first session delivers
- [ ] Icon and thumbnails share the hero and palette
- [ ] Five archetype variants ready for personalisation

---

## 8. Tools in this repository

| Command | What it does |
|---|---|
| `bpe thumbs score <file> [--kind icon]` | Roblox format checks, benchmark comparison (MrBeast 2022+ percentiles), composition warnings, promotional-text check, and a preview sheet at real display sizes with squint and greyscale tests |
| `bpe thumbs study --channel <url>` | Re-runs this study on any channel. Point it at a successful Roblox-game YouTube channel to build a genre-specific benchmark |
| `bpe prompts render thumbnail-icon-brief --var game_concept=… --var core_hook=… --var brand_character=…` | A research-grounded art-direction brief: five thumbnail concepts, three icon concepts, a capture plan and a test plan |

---

## 9. Limitations

- **One channel**, whose thumbnails are all A/B-tested winners (survivorship), and whose current
  thumbnail may differ from the one at launch.
- **Correlations only.** Concepts and thumbnails are confounded (a "$1 vs $1M" video comes with
  a split-screen thumbnail), so treat the patterns as hypotheses to test in personalisation.
- **YouTube is not Roblox.** Roblox Home tiles are smaller, users scroll a game grid rather than
  a video feed, and the success metric is qualified play-through. The principles transfer; the
  exact numbers do not.
- **Second-hand MrBeast sources.** Interview figures and the production guide come from
  secondary reports (the guide's authenticity is unconfirmed). Per-video watch pages were behind a
  YouTube bot check during this run, so his own interviews were not transcribed.
