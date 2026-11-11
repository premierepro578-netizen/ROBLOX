# Watch notes: top Roblox dev videos + the car-crash/ramp genre

*33 videos, transcripts read 2026-11-11. Selected with `bpe top-videos --spec config/roblox-top-videos.toml`:
Roblox developer content from the last 3 years, ranked by **views per day**, long-form, with an English
transcript. The automated extraction is in [`evidence-report.md`](evidence-report.md); these notes are the
close reading. Applied to the game in [`../YEET_A_CAR_GAME_PLAN.md`](../YEET_A_CAR_GAME_PLAN.md).*

## Top 25 Roblox dev / Studio videos (by views per day)

| # | Video | Views/day | What I took from it |
|---|---|---|---|
| 1 | [Superstitic: I Spent 2 Years Building the Roblox Tower Defense Game I Wanted](https://www.youtube.com/watch?v=T5OH2F6_ik0) | 15,771 | Don't let the grind *become* the gameplay; reward decisions. Give each upgrade path a distinct role. Use limited perk loadouts (strategy, not permanent power). Replayability comes from rotating events, global leaderboards, endless mode and a player-made challenge editor. Expect to rebuild the code more than once. |
| 2 | [Rickmonas90: This Roblox Developer Can't Take Criticism](https://www.youtube.com/watch?v=1VRu8LKq-Aw) | 11,160 | A list of first-session anti-patterns: auto-advancing dialogue, unclear objective locations, a first quest that's too hard, a key binding shown for 3 seconds and never again, inventory items without icons, grind walls, and banning players who report bugs. |
| 3 | [Dumbledore: Can Opus 5.5 Make A Viral Roblox Game In 24 Hours](https://www.youtube.com/watch?v=b715CMdnbSI) | 9,515 | AI agents (Claude, sub-agents, the Blender connection) for prototyping. A tutorial-or-play choice that has players **doing something within 10 seconds**. Packaging research (the Roblox game grid behaves like YouTube thumbnails). **$11 of ads → 81,000 impressions → 1,300 plays (~1 in 60).** Running ads on an unfinished build wasted spend. Shows odds on a spin wheel. A rewarding end-of-round screen. |
| 4 | [Starter Story: I Spent 24 Hours With Roblox Millionaires](https://www.youtube.com/watch?v=8xgnm6SynH4) | 7,740 | "Clickable, social and replayable." Ship something that works early. Brands are moving to interactive Roblox experiences. |
| 5 | [Reckless: How To Make a Roblox Game on Mobile](https://www.youtube.com/watch?v=KXAYJ5TnKH4) | 5,425 | Beginner path; claims a title change alone can bring players (low evidence). |
| 6 | [GuideRealm: How To Make An Entire Roblox Game With AI](https://www.youtube.com/watch?v=ltbZzXRrDF8) | 4,946 | Connecting Codex to Studio. Tune upgrade prices and income so progression feels rewarding, neither too easy nor too slow. Polish after the core works. |
| 7 | [BrawlDev: Roblox Studio Basics (Scripting #1)](https://www.youtube.com/watch?v=9MUgLaF22Yo) | 4,431 | Start of the most-watched scripting series. Code along; watching alone isn't enough. |
| 8 | [Serge: I made a scary game on Roblox in 24 hours](https://www.youtube.com/watch?v=J6JBEsGL0Qw) | 3,526 | Sketch the map on paper first. A deliberate confusing layout fits horror. Tune NPC speed against the player. |
| 9 | [Tizzy RBLX: My Roblox Game Makes $119,300/mo (38K CCU)](https://www.youtube.com/watch?v=LZOohZHsJus) | 3,116 | **Success is 80% idea plus execution, 20% data tuning. "Simple scales, fancy fails":** one simple mechanic with depth and a clear cause and effect. **30% of their players were on console**, and fixing console onboarding raised D1. Have a reason to return tomorrow plus a **social flex**. **Make it clippable** (ragdoll flings get free YouTube coverage). Nine tutorial versions, patches daily. **A cutscene cut bounce rate from 22% to 15–16%.** Don't buy templates. |
| 10 | [GDBLOOX: How to Create a Roblox Game From Scratch 2026](https://www.youtube.com/watch?v=8vxhtY2v0O4) | 2,770 | Using Studio's AI assistant; publishing basics; set genre and subgenre. |
| 11 | [CodeBro29: How to make your FIRST Roblox Game](https://www.youtube.com/watch?v=-QSmtYVMRH4) | 2,724 | Obby fundamentals (checkpoints, stages). |
| 12 | [DitchyDevelopments: First Roblox Game in 2026 (With AI)](https://www.youtube.com/watch?v=v8vby3iOOX4) | 2,554 | Describe systems in plain English to AI; AI UI generators keep you focused on finishing. |
| 13 | [Duckable: Can I Make a VIRAL TYCOON in 24 HOURS?](https://www.youtube.com/watch?v=F9sfnpkzcPw) | 2,340 | Reality check: **158 concurrent players and 37K Robux** after a month. **Smooth physics projectiles needed client ownership.** A rushed save system kept duplicating items. "Fancy effects" made it feel good. Index and starter pack. |
| 14 | [BinzuDev: How I Learned To Make Roblox Games in a Week](https://www.youtube.com/watch?v=vUN2cJD4mUk) | 2,123 | Learn by building something fun. DataStores for high scores. |
| 15 | [Duckable: How FAST Can I Make a Roblox Game?](https://www.youtube.com/watch?v=Dp7vw20e-fA) | 1,747 | Kits are great for prototypes. If you're learning to code, don't lean on AI for everything. |
| 16 | [KatanaBladeHD: All Of Roblox Lua (Luau) in 21 Minutes](https://www.youtube.com/watch?v=LWL5QUdSQiA) | 1,645 | The fastest language overview (tasks, timers, cancellable threads). |
| 17 | [script_ing: You CAN Script. Let me PROVE IT](https://www.youtube.com/watch?v=H4X8L5namhA) | 1,593 | Pause-and-try exercises; loops and properties. |
| 18 | [MikoLikesHat: How to ACTUALLY Learn to Script (5 Steps)](https://www.youtube.com/watch?v=GE6Z1n57yDU) | 1,543 | Treat tutorials as a guide, not the learning itself; apply each concept immediately in small projects. |
| 19 | [janisjanis01: How I Made a Viral Roblox Game](https://www.youtube.com/watch?v=fjlOaEALWmg) | 1,396 | **The idea decides your fate.** Take what works and add a twist. Loop: fight → earn → upgrade. Plan monetization (cash packs, starter pack, limited items). Prototype ugly, test with friends. **Ads: 8 credits a day × 2 days, then 16 a day × 2, with 2–3 thumbnails; stop at >50 organic players.** **"Admin abuse" events on update days took him from 1,000 to 3,000 concurrent players.** Tease updates. YouTubers start covering a game at about 1,000 concurrent players. |
| 20 | [Laugh: I Accidentally Made a Viral Roblox Game](https://www.youtube.com/watch?v=WFyrlstSDe4) | 1,327 | **A trending theme plus an original destruction loop** (Shred a Brain Rot: 30K peak, built in 7 days). Average playtime 17 minutes. **Revenue in 72 hours: 662K developer products, 100K private servers, 87K passes, plus ~450K Creator Rewards.** No Robux gambling: loot boxes open only with earned cash. Original thumbnails won his A/B tests. |
| 21 | [DeHapy: I Tried Learning Roblox Scripting In 7 Days](https://www.youtube.com/watch?v=UE_4mNwcXco) | 1,318 | Leaderstats then currency then systems; customise a tutorial into your own game. |
| 22 | [Develuper: Make Your Roblox Game Look 10x Better With Lighting](https://www.youtube.com/watch?v=vkEXLmRAQgs) | 1,231 | Use the realistic lighting style, a little light glare and a darker haze, and keep effects from showing through walls. |
| 23 | [RoBuilder: ABSOLUTE Beginner Basics](https://www.youtube.com/watch?v=-5OOovmkJss) | 1,219 | **Anchor your builds** or face "a lagging nightmare" as the map grows. Lock the floor while building. |
| 24 | [waveshine: Watch this before making ROBLOX Games](https://www.youtube.com/watch?v=xnlaYLnCtFc) | 1,215 | First games flop; his first hit came from progression, leaderboards and something to grind for. Feedback fuels you. Don't let the player count set your mood. |
| 25 | [VuukStudios: How To Make A Combat System](https://www.youtube.com/watch?v=Ht6ZfibXpDs) | 1,180 | Input → animation → hit detection pipeline (R6 combo system). |

## The genre: car-crash and ramp games YouTubers play

| Video | Views/day | What it shows about the market |
|---|---|---|
| [Sketch: Car Crash Studio is Diabolical](https://www.youtube.com/watch?v=GNs6wgwoZLM) | 15,576 | A crash sandbox (spawn NPC traffic, set start speed, ramps, bridges). The YouTuber invents MrBeast-style challenges ("how many buses to stop a train?"). Complaints: no tutorial, and lag with too many vehicles. |
| [FoltynPlays: Roblox MEGA RAMP for Lucky Blocks](https://www.youtube.com/watch?v=G9Ws9Rmi_4M) | 10,592 | A **launch-timing meter** ("99%!") and distance zones multiplying rewards (20× → 120× luck). Vehicles from bike to Lambo to jet to a Robux galaxy fighter. Treadmill "training", rebirths, and **a giant prize visible from spawn as the end goal**. |
| [velvet4k: Playing BeamNG Copies on Roblox](https://www.youtube.com/watch?v=uJZ7yUo9LUQ) | 3,596 | Soft-body crash physics impress, **but they run client-side only, so it's effectively single-player.** |
| [RoBros: Flying 8,129,364 FEET in Roblox](https://www.youtube.com/watch?v=ODtajhhnw5c) | 2,650 | **Almost exactly the Yeet a Car loop:** distance (studs) → cash → new cars, more ramps, engine/weight upgrades, nitrous. Robux shortcuts ("800 Robux nitrous", "1,500 Robux for 250 ramps"), free and paid spins, mystery boxes, visiting friends' ramps, car cosmetics. **Numbers escalate to billions, and the number is the content.** |
| [Elitelupus: I Drive a Truck Off the BIGGEST Ramp](https://www.youtube.com/watch?v=aFtWlNEGGdE) | 1,738 | Suspension and speed matter; mid-air failure is the funny moment. |
| [AwstynC: Roblox Car Crash Studio Is HILARIOUS](https://www.youtube.com/watch?v=_0JHT4BivZc) | 975 | Semis, buses and ramps; chaos with NPCs is the comedy. |
| [bunhat: I Tried Roblox's CAR CRASH STUDIO](https://www.youtube.com/watch?v=JRqac84Ckcg) | 792 | Property editing on spawned items; testing small before going big. |
| [rdvarney22: Making A Roblox Slot Car in 15 Minutes](https://www.youtube.com/watch?v=xuHKFOv4g8I) | 507 | Car modelling basics (body meshes, decals, color matching to references). |

*The "car tech" search didn't surface recent, well-viewed vehicle **scripting** tutorials, so the technical
guidance in the game plan comes from the Roblox docs (Explosion, VehicleSeat, network ownership, Server Authority).*
