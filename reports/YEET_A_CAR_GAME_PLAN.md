# Yeet a Car — Game Design & Build Plan

*Built from the top 25 Roblox dev videos plus 8 genre videos ([watch notes](top25/WATCH_NOTES.md)),
the earlier 107-source design research ([IMPLEMENTATION_REPORT](IMPLEMENTATION_REPORT.md)), the MrBeast
thumbnail study ([thumbnails/](thumbnails/MRBEAST_THUMBNAIL_STUDY.md)) and the Roblox docs. Assumed
concept: **launch a car off a ramp and destroy it.** Anything marked *(assumption)* should be checked
against your own design.*

---

## 1. The pitch

> **Launch a car off a ridiculous ramp, smash it into something huge, and watch the numbers explode.
> Then build a bigger ramp and do it again.**

The fantasy: a big, satisfying crash plus escalating numbers, shareable in five seconds. That matches
what top developers say wins:
- **"Simple scales, fancy fails":** one simple mechanic with a lot of depth and a clear cause and
  effect ([Tizzy RBLX @ 14:47](https://www.youtube.com/watch?v=LZOohZHsJus&t=887s)).
- **Make it clippable:** YouTubers cover games whose funniest moments film well, and ragdoll flings
  are their go-to ([@ 16:48](https://www.youtube.com/watch?v=LZOohZHsJus&t=1008s)).
- **Pair a known theme with an original loop:** Shred a Brain Rot reached 30K concurrent players in
  7 days by making destruction the loop
  ([Laugh @ 2:23](https://www.youtube.com/watch?v=WFyrlstSDe4&t=143s)).

## 2. The market: what already exists in your genre

| Game (seen via YouTubers) | Core loop | What we copy | What we do differently |
|---|---|---|---|
| Distance-launch game ([RoBros, "Flying 8,129,364 FEET"](https://www.youtube.com/watch?v=ODtajhhnw5c)) | Launch → distance → cash → cars, ramps, engine/weight upgrades, nitrous | Escalating numbers as the hook, an upgrade station next to the car, friends visiting each other's ramps | It has no destruction payoff; the run just ends |
| Mega ramp ([FoltynPlays, "MEGA RAMP for Lucky Blocks"](https://www.youtube.com/watch?v=G9Ws9Rmi_4M)) | Timing meter → distance zones multiply rewards → lucky blocks → vehicles → rebirth | **Launch-timing meter**, distance zones with multipliers, **a giant goal visible from spawn**, vehicle ladder from bike to jet | Its rewards are paid-random lucky blocks; ours are earned destruction |
| Car Crash Studio ([Sketch](https://www.youtube.com/watch?v=GNs6wgwoZLM)) | Sandbox: spawn traffic, set speed, stage crashes | Creator-friendly chaos (spawn buses, stack cars); YouTubers invent challenges | It has no progression, players complain there's no tutorial, and it lags with many vehicles |
| BeamNG-style crash copies ([velvet4k](https://www.youtube.com/watch?v=uJZ7yUo9LUQ)) | Soft-body crashes | Readable, chunky damage | Its physics are client-side only, so it's effectively single-player. Ours must be visible to friends |

**Positioning:** *distance + destruction + progression + friends watching.* The distance games lack
the payoff, and the crash sandboxes lack the reason to come back. Yeet a Car is both.

## 3. Core loop

Roblox's three-layer model ([Docs: Core loops](https://create.roblox.com/docs/production/game-design/core-loops)):

| Layer | Yeet a Car |
|---|---|
| **Minute to minute** | Drive down the ramp → **timing meter** at the lip (green = Perfect Launch bonus) → mid-air **tilt and boost** → **smash** into targets (crate walls, bus stacks, a giant tower) → slow-motion and damage-number pop |
| **Most repeated action** | Each run pays **Distance + Destruction (+ combo)** cash → spend it at the upgrade station next to the car → the next run is visibly further or bigger |
| **Engine (long term)** | **Zones** every N studs (farm → city → desert → ocean → space, with multipliers), a **car index** (each car changes play), **rebirth** for a permanent multiplier, and **giant boss targets** visible from spawn (a skyscraper, a dam, a giant robot) |

**Depth through decisions, not grind** (the lesson from [Superstitic's 2,000-hour tower-defense game](https://www.youtube.com/watch?v=T5OH2F6_ik0&t=95s)):
- **Car choice is a trade-off:** a heavy truck smashes more but flies shorter; a light kart flies far
  but barely dents things. Each car has a real reason to be used, not just a higher number.
- **Ramp tuning:** angle (distance vs height) and launch speed are choices, not only upgrades.
- **Skill:** a Perfect Launch, mid-air control and a precise landing on the target matter at every
  level. A tiny car flown well should still be competitive.
- **Combos:** the multiplier grows with chained hits (crates → bus → tower) and flips. That's where
  clippable chaos comes from.

**Build on what's proven:**
- **Loop shape:** fight → earn → upgrade is the shape every viral breakdown shared
  ([janisjanis01 @ 2:18](https://www.youtube.com/watch?v=fjlOaEALWmg&t=138s)).
- **Big numbers:** the distance-game YouTubers literally title videos with the number they reached.
  Show distance and damage prominently, and let them grow by orders of magnitude.

## 4. The first five minutes

The FTUE is "arguably the single most important piece of content" (Roblox), and players should be
**doing something within 10 seconds** ([Dumbledore @ 6:58](https://www.youtube.com/watch?v=b715CMdnbSI&t=418s)).

| Time | What happens | Why |
|---|---|---|
| 0–8 s | Optional, skippable **5-second intro**: a car flies off the mega ramp and obliterates the giant tower, then the camera snaps back to the player sitting in a car at the top of a small ramp | A cutscene cut bounce rate from 22% to 15–16% ([Tizzy @ 18:43](https://www.youtube.com/watch?v=LZOohZHsJus&t=1123s)); shows the end goal first |
| 8–15 s | One huge **GO** button (hold to accelerate). Nothing else on the HUD | Teach only the essentials; one action at a time |
| 15–30 s | The timing meter appears once: "Release on GREEN." The first launch is tuned to hit a crate wall even without a Perfect | A guaranteed first win; never fail the first try |
| 30–45 s | **Slow-motion crash**, parts fly, damage number pops, cash flies into the counter | The payoff, the clip, the cause and effect |
| 45–70 s | The **Upgrade Ramp** button glows; it costs exactly the first payout. The second run visibly flies further and hits the next target | First upgrade inside a minute; progress you can see |
| 1–3 min | Quests panel appears (3 easy quests); car #2 unlock teased; distance signposts toward the giant tower on the horizon; other players' launches visible | Mid and long-term goals in view; social from minute one |
| 3–5 min | First zone milestone ("CITY at 5,000 studs"), congratulations, and a notification opt-in after the big crash | End the first session on aspiration with a call to action |

**Rules for the first session:**
- **Controls:** key bindings and touch/console button hints stay visible. Never show them for 3
  seconds and hide them (the anti-pattern from the [criticism video](https://www.youtube.com/watch?v=1VRu8LKq-Aw&t=466s)).
- **Platforms:** test **console and mobile** from day one. At Tizzy's game 30% of players were on
  console, and fixing console onboarding raised D1.
- **Readable pacing:** dialogue never auto-advances. Every item has an icon and every objective has
  a marker.
- **Measure it:** instrument the funnel server-side with `AnalyticsService:LogOnboardingFunnelStepEvent`:
  joined → first GO → first crash → first upgrade → second run → quest 1 → first zone.

## 5. Retention

| System | Design | Evidence |
|---|---|---|
| **Daily return** | Daily fuel or boost reward plus a **daily target** (e.g. "Today: the ice-cream truck tower"), previewing tomorrow's reward | A reason to return tomorrow; personalise to what the player needs |
| **Quests** | "Destroy 3 buses", "Fly 10,000 studs", "5 Perfect Launches", rotating daily and weekly | Points players at under-used cars and zones |
| **Social flex** | Friends' best-distance flags in your world, visiting friends' ramps, **party launches** (everyone fires at the same target), cosmetic car paints, trails and explosion colours | Nearly every top game has a social flex ([Tizzy @ 16:11](https://www.youtube.com/watch?v=LZOohZHsJus&t=971s)); co-play is a ranking signal |
| **Leaderboards** | Daily, weekly and all-time **distance** and **destruction**; the daily board resets so newcomers can place | Competition without a locked top |
| **Live ops** | Weekly update day, each **feeling like an event** (new target, car or zone), **admin-abuse events** on update days, and sneak peeks during the week | Admin abuse took one game from 1,000 to 3,000 concurrent players ([janisjanis01 @ 9:03](https://www.youtube.com/watch?v=fjlOaEALWmg&t=543s)); weekly cadence wins (Adopt Me, Jailbreak) |
| **Long term** | Rebirth multiplier, car index, zone chain, seasonal giant targets (Halloween pumpkin tower), and later a **challenge editor** where players build destruction setups and share them | Player-made challenges extend replayability (Superstitic) and feed creators |
| **Creator mode** *(later)* | A sandbox server type: spawn traffic, set speed, stack buses | Car Crash Studio's success is creators inventing challenges |

Pace content (one car or target per week rather than ten at once), and watch the first 48 hours of
every update for physics exploits.

## 6. Monetization: fair, sold as speed and spectacle

Lessons that apply directly:
- **Monetization is engagement:** a cheap first purchase early (RDC 2025).
- **Pay to speed, not to win:** don't gatekeep basics (SpongeBob Tower Defense).
- **Developer products are most of the revenue** in a destruction game. Laugh's 72-hour split was
  662K products, 100K private servers and 87K passes, with no Robux gambling.

| Offer | Type | Notes |
|---|---|---|
| **Starter Pack** (≈ 49–99 Robux, first sessions only) | Developer product | A car with a different playstyle + fuel + a paint; best value in the game |
| **Nitrous / Rocket Fuel** | Developer product (consumable) | Extra boost on the next runs, the genre's proven seller. Allow buying several at once |
| **Mega Bomb** | Developer product | The next crash's explosion is 3× bigger, which is cosmetic spectacle more than progression power |
| **2× Cash**, **Auto-Return**, **Bigger Garage** | Passes | Permanent quality-of-life and speed |
| **Paint, trails, explosion colours, wreck effects** | Passes / products | Cosmetic social flex; very clippable |
| **Private servers** | Private server | Friends-only launch parties (a real revenue line in Laugh's numbers) |
| **Rewarded video ad** | Rewarded ad | Free nitrous between runs (a natural break); reaches the 80%+ who never pay |

**Guardrails:**
- **No Robux gambling.** Crates and spins, if any, open only with earned currency, and their odds
  are shown. Respect `PolicyService` restrictions.
- **Keep the competitive boards fair.** Show daily boards with boosts disabled, or season boards
  that reset, so paying players don't own the top forever. The genre's videos are full of "pay to
  win!" accusations between friends.
- **Monetize every intended mechanic at launch,** so nothing is ever "taken away" from free players
  later.

## 7. Discovery and launch

1. **Packaging:** the thumbnail set in [`designs/yeet-a-car/`](../designs/yeet-a-car/README.md).
   Recreate **v5 / v3 / v2** in Studio with real assets, activate them for personalisation, and use
   the **v5 icon**. Add a **Home gameplay video** of a real crash (+30–41% plays in Roblox's
   examples).
2. **Never advertise an unfinished build.** Dumbledore's ads sent players into a broken version.
3. **Ads ramp:** 8 credits a day for 2 days, then 16 a day for 2 days, with 2–3 thumbnails. Stop
   once 50+ players stay organically and put effort into the first update
   ([janisjanis01 @ 6:00](https://www.youtube.com/watch?v=fjlOaEALWmg&t=360s)). Benchmark:
   $11 → 81,000 impressions → 1,300 plays.
4. **Short-form clips:** crash clips for TikTok and Shorts. YouTubers start covering games at about
   1,000 concurrent players, so make crashes clip-ready (slow-motion button, a photo/replay camera).
5. **Expect a slow start.** A rushed 24-hour tycoon peaked at 158 players and 37K Robux. Polish and
   cadence are what compound.

## 8. Technical build notes

| Area | Approach |
|---|---|
| **Car** | A small assembly of **8–20 welded body parts** (not hundreds). Drive with a `VehicleSeat` (`Throttle`, `Steer`, `MaxSpeed`, `Torque`), or constraint-driven wheels (`HingeConstraint` motors + `SpringConstraint` suspension) |
| **Launch** | At the ramp lip, apply the launch on the server with `BasePart:ApplyImpulse` / `AssemblyLinearVelocity`, scaled by upgrades × the timing-meter result |
| **Destruction** | On impact, spawn an `Explosion` (tuned `BlastRadius`, `BlastPressure`) with **`DestroyJointRadiusPercent = 0`** so players' joints stay safe, as in the docs' "non lethal explosions" sample. In `Explosion.Hit`, break the **car's own** `WeldConstraint`s yourself (only parts inside the car model) and add fling impulses. Eject the driver into a ragdoll launch first, since it's the most clippable moment. Remove debris with `Debris:AddItem(part, 4–6)` |
| **Performance** | Anchor the map ("a lagging nightmare" otherwise). Cap simultaneous wrecks and pool debris. Turn on **StreamingEnabled**. Test on a low-end phone. Crash sandboxes lag at scale |
| **Anti-cheat / fairness** | Distance is the economy, so **never trust a client-reported distance.** Use **Server Authority** (`Workspace.AuthorityMode = Server`; core logic in `RunService:BindToSimulation()`; built-in prediction and rollback; Roblox ships a **Racing template**), or at minimum compute distance and cash on the server from a server-owned car. Make predicted crash effects undoable, because a misprediction can roll them back ([Docs](https://create.roblox.com/docs/projects/server-authority)) |
| **What others see** | Replicate a lightweight version of each crash (a few big chunks plus VFX) so friends see your yeet. Client-only soft-body crashes made one competitor effectively single-player |
| **Saving** | Use a session-locked profile (ProfileStore pattern) and versioned data. A rushed save system duplicated items in the 24-hour tycoon |
| **Purchases** | Grant in `ProcessReceipt`, persist before returning `PurchaseGranted`, dedupe by `PurchaseId`, and handle the Transaction Refunded webhook |
| **Analytics** | Funnel events for the FTUE, `LogEconomyEvent` for every cash source and sink, custom events for launch distance, Perfect Launch rate and crash combos |
| **Look** | Use the realistic lighting style with a little glare and a darker haze. Keep it bright and saturated so it matches the thumbnails |
| **AI tools** | Claude, Codex and Studio's assistant speed up prototypes and UI (Dumbledore, GuideRealm, Ditchy). Still learn the fundamentals (BrawlDev's series, *All of Luau in 21 Minutes*), and **don't buy templates** (Tizzy's $600 template flopped) |

## 9. Roadmap

| Phase | Build | Exit criteria |
|---|---|---|
| **1 · Find the fun** (week 1) | Grey-box: one ramp, one car, timing meter, distance, one crate wall, cash, one upgrade | Friends replay it without being asked. "If the game isn't fun, 2× of zero is still zero" |
| **2 · First session** (week 2) | Crash juice (slow-mo, parts, numbers), 3 cars with different trade-offs, 2 zones, the 5-minute FTUE, funnel events, mobile + console pass, saving, Starter Pack + Nitrous + 2× Cash | New testers hit their first upgrade inside 60 seconds; no funnel step loses an outsized share of players |
| **3 · Launch** (week 3) | Studio renders of the thumbnails and icon, a Home gameplay video, private servers, daily reward, quests, leaderboards | Ads ramp per §7; first-play bounce and D1 tracked by cohort |
| **4 · Live** (week 4+) | Weekly update day with admin abuse, a new car/target/zone each week, rebirth, then party launches and the creator/challenge mode | D7 and playtime trending up; update days lift returning players |

## 10. Numbers to watch

| Metric | Why | Reference point |
|---|---|---|
| Time to first launch | The 10-second hook | Under 10 s |
| First-play bounce | The cutscene and onboarding test | Tizzy: 22% → 15–16% after a cutscene |
| D1 / D7 | Fun and reason to return | Compare against your Creator Analytics benchmarks |
| Average playtime | Depth | Shred a Brain Rot: about 17 min (called "average") |
| Perfect Launch rate | Skill depth (too high = too easy) | Tune toward a learnable 30–60% *(assumption)* |
| Payer conversion, ARPPU | Monetization health | Roll back any change that drops D7 |
| Qualified play-through rate (QPTR) | Whether the thumbnails promise what the game delivers | Test with personalisation |

---

*Want to go deeper on one part? The prompt framework can generate detailed specs:
`bpe prompts render core-loop-designer`, `onboarding-ftue`, `retention-systems`,
`monetization-design`, `luau-implementation-spec`, `thumbnail-icon-brief`. Paste a section of this
plan as `--var game_concept="…"`.*
