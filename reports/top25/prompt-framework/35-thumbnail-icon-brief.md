<!-- Thumbnail & icon art-direction brief · stage: design · unfilled slots: game_concept, core_hook, brand_character -->

Write the art-direction brief for this Roblox game's Home thumbnails and icon.

- **Game & core loop:** {{game_concept}}
- **The single most exciting thing a player does or sees (the hook):** {{core_hook}}
- **Recurring character / mascot / brand colours (if any):** {{brand_character}}

## Research: what makes thumbnails work (MrBeast study + attention science)
- **One idea, readable in a glance.** People extract the gist of an image in as little as 13 ms per picture ([Potter et al. 2014](https://pubmed.ncbi.nlm.nih.gov/24374558/)). In MrBeast's 2022+ thumbnails (n = 99), images with 0–1 focal regions had a median outlier of ×1.14, against ×0.92 for 4+ (ρ = −0.27, p = 0.006). Crowded group shots (3+ faces) had ×0.83. — study: `reports/thumbnails/MRBEAST_THUMBNAIL_STUDY.md`
- **Show a contrast or a stake, not a scene.** "$1 vs $X" split-screens had a median ×1.38 (vs ×0.95), and cash-stake concepts ×1.16 (vs ×0.90). For Roblox, the equivalent is a visible progression or stakes contrast: level 1 vs level 100, a tiny pet vs a giant one, safe vs lava.
- **Text is a number, not a sentence.** MrBeast's overlay text is 1–2 tokens ("DAY 97", "$1M"); thumbnails with 1–2 OCR tokens had a median ×1.12, against ×0.92 with none. Text and faces attract gaze 11.1× and 16.6× more than matched regions ([Cerf et al. 2009](https://resolver.caltech.edu/CaltechAUTHORS:20130816-103355264)). Roblox asks for text sparingly and rejects promotional claims ("50% off", "Free UGC!") in video thumbnails ([Docs](https://create.roblox.com/docs/production/publishing/thumbnails)).
- **Faces: big, few and natural.** The median largest face is about 10% of the frame in MrBeast's recent thumbnails. He reported that closed-mouth versions won his YouTube A/B tests, which pick winners by **watch-time share, not CTR** ([YouTube Help](https://support.google.com/youtube/answer/13861714)). Across 300K videos, faces show no general CTR advantage and vary by niche ([SEJ](https://www.searchenginejournal.com/do-faces-help-youtube-thumbnails-heres-what-the-data-says/563944/)). Make the face earn its place: one expressive avatar, gaze toward the hook (gaze cues shift attention reflexively; [Friesen & Kingstone 1998](https://psych.unl.edu/mdodd/Psy498/FriesenKingstone.pdf)).
- **Saturated, bright mid-tones; avoid clutter.** MrBeast's 2022+ medians are colourfulness 78.5, saturation 0.40 and lightness 55 (out of 100). Dense perceptual detail ("feature complexity") lowers attention, while a deliberate composition raises it ([Pieters, Wedel & Batra 2010](https://repository.tilburguniversity.edu/items/3fddf97a-469e-4d38-9c26-8dbd00c750b2)).
- **Make it read at real size.** Roblox icons scale down to 150×150 and the docs say to preview them small ([Docs: Icons](https://create.roblox.com/docs/production/publishing/experience-icons)). "The most common mistake" is a thumbnail that works on desktop but not on mobile ([Tizzy RBLX @ 5:39](https://www.youtube.com/watch?v=az7em1IoBhA&t=339s)). Keep the bottom 15% clear for the player count.
- **Promise only what the game delivers.** MrBeast's production guide (leaked; authenticity unconfirmed) says the thumbnail must match the video ([Creator Handbook summary](https://www.creatorhandbook.net/leaked-document-allegedly-reveals-mrbeasts-secrets-to-youtube-success-the-key-takeaways/)). Roblox requires thumbnails that show what players should expect and avoid ambiguous imagery, and it ranks on *qualified* play-through, so a misleading click that bounces costs distribution.
- **Test variants like MrBeast.** His team reportedly drafts dozens of title/thumbnail concepts per video and A/B tests them ([Jon Youshaei interview recap](https://recapio.com/digest/why-every-mrbeast-video-gets-200m-views-interview-by-jon-youshaei)). On Roblox, keep 2–5 thumbnails active in personalisation (+8.5% average qualified play-through; some games +50%), test new ones with each update, and refresh when CTR decays ([CallMeDogey @ 0:36](https://www.youtube.com/watch?v=SjjPGduApZU&t=36s)).

## Research: Roblox discovery
- **How Recommended for You works:** retrieval narrows millions of games using engagement, retention and monetisation signals from *all* players. Ranking then personalises using engagement, return visits, Robux spend and co-play, measured only on players who found the game organically on Home. — [Roblox Creators, RFY @ 0:00](https://www.youtube.com/watch?v=K7jsk3bzmvE), [@ 0:40](https://www.youtube.com/watch?v=K7jsk3bzmvE&t=40s)
- **Retention and monetisation together earn the widest distribution.** If retention is low, fix the core game first; if it is strong, add thoughtful monetisation. Distribution is relative: if competitors improve, a game's impressions can fall even when its own metrics hold steady. — John Ciancutti (Roblox CGO), [DevForum: Boost Your Discovery](https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042)
- **Signal windows:** play days and playtime per user over D1, D2–D7 and D8–D28, plus intentional co-play days, qualified play sessions, spend days and Robux spend. Impressions typically drop *after* play-through rate and playtime drop. — [Docs: Discovery](https://create.roblox.com/docs/discovery)
- **Packaging requirements:** since 2026-10-19 Home recommendations require a custom thumbnail (16:9, ideally 1920×1080, up to five). Thumbnail personalisation averaged +8.5% qualified play-through in testing. — [DevForum: Custom thumbnail requirement](https://devforum.roblox.com/t/homepage-recommendation-eligibility-now-requires-a-custom-thumbnail/4945086), [Docs: Thumbnails](https://create.roblox.com/docs/production/publishing/thumbnails)
- **Home gameplay videos work:** Superstar Baseball saw +30% RFY plays and +31% RFY playtime; Notoriety +41% plays and +39% playtime. Show real, current footage of the core loop and avoid cinematic trailers, voice-overs and promo text. — [DevForum: Gameplay Videos on Home](https://devforum.roblox.com/t/gameplay-videos-on-home-help-your-games-get-discovered/4842601)
- **Paid acquisition as a measured test.** Ads showed a median 10% lift in D7-retained users; judge campaigns on return on ad spend. Small early ad spend mainly buys the recommender data. — [DevForum: Ads Manager RDC Recap](https://devforum.roblox.com/t/ads-manager-rdc-recap-earnings-roas-reporting-incrementality/4909790); AlvinBlox, [@ 8:51](https://www.youtube.com/watch?v=Y93DRfB-Deo&t=531s)
- **Design thumbnails for phones first.** "The most common mistake… a thumbnail that looks good on desktop but is very hard to see on mobile." Communicate what the player will *feel*. — Tizzy RBLX, [@ 5:39](https://www.youtube.com/watch?v=az7em1IoBhA&t=339s), [@ 8:42](https://www.youtube.com/watch?v=az7em1IoBhA&t=522s)

## Deliver
1. **The one-sentence promise** the thumbnail must make (what the player will *do and feel*),
   and the one thing it must never imply that the game does not deliver.
2. **Five thumbnail concepts** (16:9, 1920×1080), each a different *idea* so personalisation can
   learn which hook works for whom. Use these archetypes, adapted to the game:
   - Progression contrast (level 1 vs level 100, small vs giant, poor vs rich base)
   - Stakes moment (the hero one second before the threat lands)
   - Scale spectacle (one hero against something enormous)
   - Progress counter (the number that tells the story: day, level, size, count)
   - Signature mechanic close-up (the verb nobody else has)
   For each: focal subject, the hero's expression and **gaze direction (toward the hook)**,
   background (simple, contrasting value), palette (2–3 saturated hues + one accent), overlay
   text (0–2 tokens, a number where possible, no claims), what sits in the bottom 15% (nothing
   important), and why it should beat the others.
3. **Three icon concepts** (512×512, read at 150 px): one centred subject filling ~60% of the
   frame, a one-colour background with strong value contrast to the subject, no text or one
   short word, and consistency with the thumbnails' hero and palette.
4. **Capture plan in Studio:** freecam angles, lighting (rim light to separate the hero), avatar
   expression via dynamic heads, render resolution, and post-processing that stays faithful to
   the real game.
5. **Test plan:** which 2–5 thumbnails to activate first in thumbnail personalisation, what
   qualified play-through rate would retire one, and when to refresh (each update; CTR decay).
6. **QA checklist** to run with `bpe thumbs score <file> [--kind icon]` before upload.
