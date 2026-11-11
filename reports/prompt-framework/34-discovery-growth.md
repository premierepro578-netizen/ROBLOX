<!-- Discovery & growth planner · stage: design · unfilled slots: game_concept, current_metrics -->

Plan discovery and growth for this game.

- **Concept & hook:** {{game_concept}}
- **Current metrics (impressions, CTR, play-through, D1/D7):** {{current_metrics}}

## Curated findings (close reading of first-party talks and docs)
- **How Recommended for You works:** retrieval narrows millions of games using engagement, retention and monetisation signals from *all* players. Ranking then personalises using engagement, return visits, Robux spend and co-play, measured only on players who found the game organically on Home. — [Roblox Creators, RFY @ 0:00](https://www.youtube.com/watch?v=K7jsk3bzmvE), [@ 0:40](https://www.youtube.com/watch?v=K7jsk3bzmvE&t=40s)
- **Retention and monetisation together earn the widest distribution.** If retention is low, fix the core game first; if it is strong, add thoughtful monetisation. Distribution is relative: if competitors improve, a game's impressions can fall even when its own metrics hold steady. — John Ciancutti (Roblox CGO), [DevForum: Boost Your Discovery](https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042)
- **Signal windows:** play days and playtime per user over D1, D2–D7 and D8–D28, plus intentional co-play days, qualified play sessions, spend days and Robux spend. Impressions typically drop *after* play-through rate and playtime drop. — [Docs: Discovery](https://create.roblox.com/docs/discovery)
- **Packaging requirements:** since 2026-10-19 Home recommendations require a custom thumbnail (16:9, ideally 1920×1080, up to five). Thumbnail personalisation averaged +8.5% qualified play-through in testing. — [DevForum: Custom thumbnail requirement](https://devforum.roblox.com/t/homepage-recommendation-eligibility-now-requires-a-custom-thumbnail/4945086), [Docs: Thumbnails](https://create.roblox.com/docs/production/publishing/thumbnails)
- **Home gameplay videos work:** Superstar Baseball saw +30% RFY plays and +31% RFY playtime; Notoriety +41% plays and +39% playtime. Show real, current footage of the core loop and avoid cinematic trailers, voice-overs and promo text. — [DevForum: Gameplay Videos on Home](https://devforum.roblox.com/t/gameplay-videos-on-home-help-your-games-get-discovered/4842601)
- **Paid acquisition as a measured test.** Ads showed a median 10% lift in D7-retained users; judge campaigns on return on ad spend. Small early ad spend mainly buys the recommender data. — [DevForum: Ads Manager RDC Recap](https://devforum.roblox.com/t/ads-manager-rdc-recap-earnings-roas-reporting-incrementality/4909790); AlvinBlox, [@ 8:51](https://www.youtube.com/watch?v=Y93DRfB-Deo&t=531s)
- **Design thumbnails for phones first.** "The most common mistake… a thumbnail that looks good on desktop but is very hard to see on mobile." Communicate what the player will *feel*. — Tizzy RBLX, [@ 5:39](https://www.youtube.com/watch?v=az7em1IoBhA&t=339s), [@ 8:42](https://www.youtube.com/watch?v=az7em1IoBhA&t=522s)

## What top-performing sources teach (mined evidence)
- **Recommendation algorithm** — P0, taught by 32 source(s), 15 first-party doc(s)
  - "But I always tell people you need to learn to make your own thumbnails because hiring artists takes time. And as you can see by this downward chart, in only the matter of less than a week here, my thumbnail went down by at least …" — CallMeDogey, “How to ACTUALLY Make High CTR Roblox Thumbnails” @ 0:36 <https://www.youtube.com/watch?v=SjjPGduApZU&t=36s>
  - "Because as I said before with high CTRGF effects, you want to make sure your colors are nice and bright and vibrant, but also bold and very clear of what sort of color they are." — gfxrhino, “How to Make HIGH CTR Roblox GFX” @ 10:27 <https://www.youtube.com/watch?v=GyoA8dHKdZw&t=627s>
  - Numbers cited: behavior of the 10 thousand daily players from; super fans from day one . You can; an average of 10 thousand daily players on; daily players on 25 thousand impressions from recommendations
- **Thumbnails, icons & titles** — P0, taught by 14 source(s), 7 first-party doc(s)
  - "And this is hugely, hugely important because when you're making your thumbnails, the most common mistake I see is devs make a thumbnail that looks good on desktop but is very hard to see on mobile." — Tizzy RBLX, “How I Make High Quality Roblox Thumbnails with AI” @ 5:39 <https://www.youtube.com/watch?v=az7em1IoBhA&t=339s>
  - "Ideally, you want to make sure it has a good CTR because that means lots of people click on it and it'll be cheaper later when you spend a lot to advertise." — CallMeDogey, “How to ACTUALLY Advertise Your Roblox Game” @ 6:21 <https://www.youtube.com/watch?v=7QfaQe4rsq8&t=381s>
  - Numbers cited: super fans from day one . You can; an average of 10 thousand daily players on; daily players on 25 thousand impressions from recommendations; acquires an additional 5 thousand daily players from
- **Paid acquisition** — P0, taught by 6 source(s), 3 first-party doc(s)
  - "so there's no longer ambiguity on why your game doesn't hit algo or why it dies, how much you should spend on ads, how often should you run ads?" — Tizzy RBLX, “The Roblox Algorithm Explained Like You're 5 Years Old” @ 0:22 <https://www.youtube.com/watch?v=inWzxY26NXo&t=22s>
  - "Before I ever fully advertise a game, I run a small ad to test the CTR, which means click-through rate of the icon {slash} thumbnail on the game." — CallMeDogey, “How to ACTUALLY Advertise Your Roblox Game” @ 6:13 <https://www.youtube.com/watch?v=7QfaQe4rsq8&t=373s>
  - Numbers cited: an average of 10 thousand daily players on; daily players on 25 thousand impressions from recommendations; acquires an additional 5 thousand daily players from; Sponsored sort, from 20 thousand impressions
- **External content & creators** — P1, taught by 6 source(s), 3 first-party doc(s)
  - "The best way to reach a lot of people at once is through YouTube shorts." — Burger, “I Went Viral on Roblox” @ 4:21 <https://www.youtube.com/watch?v=n3t6w9Kn75g&t=261s>
  - "Avoid cinematic trailers, dramatized gameplay, promotional text, real-life footage, voiceovers, narration, and music with lyrics." — Th3_avocad0, “Gameplay Videos on Home: Help Your Games Get Discovered” <https://devforum.roblox.com/t/gameplay-videos-on-home-help-your-games-get-discovered/4842601>

## Roblox implementation playbook
- **Recommendation algorithm**: Optimise the signals the recommender reads: play-through, play days and playtime per user (D1, D2-D7, D8-D28), co-play days, spend days and Robux spend. Fix first-play bounce before buying traffic; recommendations expand to cohorts that engage. Strength in both retention and monetisation earns broader distribution than either alone.
  - APIs: Creator Hub Analytics: Acquisition
  - Measure: Home impressions; Play-through rate; D1/D7 retention
- **Thumbnails, icons & titles**: Upload at least one custom 16:9 (1920x1080) thumbnail: since 2026-10-19 only games with one get Home recommendation impressions. Turn on thumbnail personalization (up to five thumbnails); Roblox reports +8.5% average qualified play-through in testing. Add a Home gameplay video of real, current footage of the core loop, readable in the first seconds. Check every thumbnail on a phone-sized preview; keep them accurate to the game.
  - APIs: Thumbnail personalization (Creator Hub), Gameplay videos on Home
  - Measure: Impressions -> click-through rate; Play-through rate
- **Paid acquisition**: Buy ads/sponsorships to test the funnel at scale once D1 retention is healthy.
  - APIs: Ads Manager (Creator Hub)
  - Measure: Cost per play; Paid-cohort D7 retention
- **External content & creators**: Seed short-form clips of the most shareable moment; give creators reasons to record (events, codes, secrets).
  - Measure: Traffic by source (Acquisition dashboard)

## Deliver
1. **Signal audit** — which recommendation signals (play-through, playtime, retention,
   co-play, monetisation) are weakest, and the in-game fix for each.
2. **Icon & thumbnail test plan** — three concepts, what each communicates in two seconds,
   and how you will judge them.
3. **Launch sequence** — what must be true (D1, funnel completion) before buying traffic.
4. **Creator & short-form plan** — the most clippable moment and how to make it recur.
