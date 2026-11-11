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
- **Recommendation algorithm** — P0, taught by 4 source(s)
  - "By now, your game should be in the algorithm. Your stats should slowly improve and the game will start to earn its first money." — janisjanis01, “How I Made a Viral Roblox Game” @ 8:20 <https://www.youtube.com/watch?v=fjlOaEALWmg&t=500s>
  - "to be greedy instead of wanting to make a fun experience and from what I've heard the Roblox algorithm seems to push games that make a lot of money which in turn makes the game more popular and thus makes more money regardless of if …" — BinzuDev, “How I Learned To Make Roblox Games in a Week” @ 37:09 <https://www.youtube.com/watch?v=vUN2cJD4mUk&t=2229s>
- **Paid acquisition** — P1, taught by 1 source(s)
- **External content & creators** — P1, taught by 1 source(s)
  - "Uh, no. If we want our game to go viral, we need to make sure it feels good to play." — Duckable, “Can I Make a VIRAL TYCOON in 24 HOURS?” @ 14:31 <https://www.youtube.com/watch?v=F9sfnpkzcPw&t=871s>

## Roblox implementation playbook
- **Recommendation algorithm**: Optimise the signals the recommender reads: play-through, play days and playtime per user (D1, D2-D7, D8-D28), co-play days, spend days and Robux spend. Fix first-play bounce before buying traffic; recommendations expand to cohorts that engage. Strength in both retention and monetisation earns broader distribution than either alone.
  - APIs: Creator Hub Analytics: Acquisition
  - Measure: Home impressions; Play-through rate; D1/D7 retention
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
