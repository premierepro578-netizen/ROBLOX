<!-- Core loop designer · stage: design · unfilled slots: game_concept, genre, target_session_minutes -->

Design the core gameplay loop for this game.

- **Concept:** {{game_concept}}
- **Genre / references:** {{genre}}
- **Target session length:** {{target_session_minutes}} minutes

## Curated findings (close reading of first-party talks and docs)
- **Fun is the multiplier everything else scales.** "If you find a way to 2x your retention… if the game isn't fun, 2x of zero is still zero." Test the core loop early with real players and follow the fun before optimising systems. — Alex (Jailbreak), [RDC 2025 Retention Playbook @ 5:42](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=342s)
- **A core loop has three layers:** the minute-to-minute interaction, the most repeated set of actions, and the engine that powers progress. Jailbreak: explore → complete objective → power up, for both police and criminals. — [Roblox Creators, What's a core loop? @ 0:13](https://www.youtube.com/watch?v=gkFKF9A-snY&t=13s), [@ 0:59](https://www.youtube.com/watch?v=gkFKF9A-snY&t=59s)
- **Bake retention into the loop instead of bolting it on.** You have the player's focus for roughly 15 minutes; set the goal and reward it fast. Pick one or two meta systems (streak, collection, leaderboard) that surface on every loop. Stacking many makes the loop long and noisy. — Leon Fernandes, [Gamesforum @ 0:49](https://www.youtube.com/watch?v=61BjLzI490g&t=49s), [@ 5:43](https://www.youtube.com/watch?v=61BjLzI490g&t=343s)
- **Hide depth behind gates and keep the entry simple.** Bee Swarm Simulator still opens like it did in 2018; complexity unlocks deeper in. Games that bloat force new players through "the first 90% of the game [that] is irrelevant" and collapse. — Onett (Bee Swarm Simulator), [RDC 2025 Retention Playbook @ 32:33](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=1953s), [@ 33:42](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=2022s)
- **Design the economy as taps, drains and converters.** Taps add resources, drains remove them (and can add risk), converters force decisions. Power-creep feedback loops need a counterweight. — [Game Maker's Toolkit @ 1:54](https://www.youtube.com/watch?v=Zrf1cou_yVo&t=114s), [@ 4:44](https://www.youtube.com/watch?v=Zrf1cou_yVo&t=284s), [@ 11:01](https://www.youtube.com/watch?v=Zrf1cou_yVo&t=661s)
- **Every paid multiplier is an economy decision.** A 2x offline-earnings product means long-term progression must compensate. — Tizzy RBLX, [Monetization Explained @ 8:17](https://www.youtube.com/watch?v=zoz3PSMqets&t=497s)

## What top-performing sources teach (mined evidence)
- **Progression & pacing** — P0, taught by 3 source(s)
  - "You can also adjust the upgrade prices and income rates to make sure progression feels rewarding without becoming too easy or too slow." — GuideRealm, “How To Make An ENTIRE Roblox Game With AI - Full Guide” @ 7:32 <https://www.youtube.com/watch?v=ltbZzXRrDF8&t=452s>
  - "Make a starter pack that helps with progression. Add some limited-time items." — janisjanis01, “How I Made a Viral Roblox Game” @ 3:02 <https://www.youtube.com/watch?v=fjlOaEALWmg&t=182s>
- **Action -> reward -> upgrade cycle** — P1, taught by 2 source(s)
  - "If you're making a simulator, make sure the gameplay loop works. Or even for a horror game, just start small and then expand." — DitchyDevelopments, “How To Make Your First Roblox Game in 2026 (With AI)” @ 2:16 <https://www.youtube.com/watch?v=v8vby3iOOX4&t=136s>
  - "And you need to be original. You need to make an original gameplay loop, something to stand out." — Laugh, “I Accidentally Made a Viral Roblox Game” @ 9:51 <https://www.youtube.com/watch?v=WFyrlstSDe4&t=591s>
- **Concept & hook** — P1, taught by 2 source(s)
  - "And you need to be original. You need to make an original gameplay loop, something to stand out." — Laugh, “I Accidentally Made a Viral Roblox Game” @ 9:51 <https://www.youtube.com/watch?v=WFyrlstSDe4&t=591s>

## Roblox implementation playbook
- **Progression & pacing**: Model cost and reward curves in a spreadsheet first; target a predictable time-to-next-upgrade at each stage. Show the next unlock and progress toward it permanently on the HUD. Re-tune curves from analytics (progression/economy events), not intuition.
  - APIs: AnalyticsService:LogEconomyEvent, AnalyticsService custom events for level-ups
  - Measure: Median time to each milestone; Drop-off by level; Sink/source ratio of soft currency
- **Action -> reward -> upgrade cycle**: Write the loop as a single sentence (verb -> reward -> spend -> stronger verb) and make every system feed it. Keep the minute-to-minute action responsive on its own; the reward/upgrade layer amplifies a fun verb, it cannot replace one. Make one full loop completable within the first minute, then lengthen loops gradually.
  - APIs: DataStoreService (UpdateAsync) for currency/upgrade persistence, RemoteEvents with server-side validation
  - Measure: Loops completed per session; Average session length; D1 retention
- **Concept & hook**: Validate the hook before building systems: can the idea be understood from the icon and title in 2 seconds? Study the top games in the genre; ship the genre's expected loop, then differentiate on one axis.
  - Measure: Thumbnail click-through rate; First-play bounce rate

## Deliver
1. **Loop sentence** — one line: verb -> reward -> spend -> stronger verb.
2. **Loop stack** (table): moment-to-moment (seconds), short loop (1-3 min), session loop,
   long-term loop (days/weeks). For each: player action, feedback, reward, what it unlocks.
3. **First loop in 60 seconds** — exactly how a new player completes one full loop within
   the first minute.
4. **Progression curve** — starting cost/reward table for the first 10 upgrades and the
   first rebirth/prestige (if any), with the target time-to-next-upgrade at each step.
5. **Juice list** — the feedback (sound, VFX, UI motion) on every core action, with a
   mobile performance budget.
6. **Depth** — the decision or skill that keeps veterans engaged after hour five.
7. **Instrumentation** — the events and KPIs that tell you the loop works.
8. **Risks** — where the loop could feel grindy or exploitable, and the mitigation.
