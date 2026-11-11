<!-- Onboarding / FTUE designer · stage: design · unfilled slots: game_concept, target_devices -->

Design the first-time user experience (FTUE) for this game.

- **Concept & core loop:** {{game_concept}}
- **Target devices:** {{target_devices}}

## Curated findings (close reading of first-party talks and docs)
- **The FTUE is "arguably the single most important piece of content in a free-to-play game."** Keep it to a few minutes, and expect to keep iterating after launch. D1 retention measures it. — [Roblox Creators, Onboarding Essentials @ 0:51](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=51s), [@ 1:39](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=99s)
- **Teach only the essentials:** movement and interaction, then the core loop (what to do *and why*). Surface unusual controls on the HUD when they are relevant. Layer complexity after the first session. — [@ 3:46](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=226s), [@ 4:27](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=267s), [@ 5:09](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=309s)
- **Front-load progress.** Tune the level curve so players level up quickly in the first minutes, give starter items and some currency so they visit the shop, and make onboarding social, never isolated. — [@ 5:44](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=344s), [@ 7:07](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=427s)
- **End the first session with aspiration.** Show the full range of what is coming (mid- and long-term goals visible in a hub or on the HUD, not buried in menus). Close with a congratulatory call to action, ideally unlocking a new ability. — [@ 8:21](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=501s), [@ 9:36](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=576s), [@ 10:14](https://www.youtube.com/watch?v=XfxbdKtSbOI&t=614s)
- **Three guidance techniques:** visual elements (a subtle trail, or a highlighted UI element), contextual "just-in-time" tutorials triggered by play (e.g. when a player is two-thirds of the way to unlocking a feature), and timed hints shown only to players who take longer than most. — [Roblox Creators, Onboarding techniques @ 0:38](https://www.youtube.com/watch?v=dXqZC4x2Vn8&t=38s), [@ 1:14](https://www.youtube.com/watch?v=dXqZC4x2Vn8&t=74s), [@ 1:57](https://www.youtube.com/watch?v=dXqZC4x2Vn8&t=117s)
- **Protect the FTUE as the game grows.** "Don't mess with the first-time user experience." When adding seasons, make the first new items fun but balanced against starter gear. Test with genuinely new players, because veteran testers become entrenched. — Colin & Henry, [RDC 2025 Retention Playbook @ 31:24](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=1884s), [@ 30:39](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=1839s)
- **UI is communication.** Prioritise what players need *now* (use contextual buttons), steer attention with colour, size and space, keep the palette small and button styles consistent, follow conventions (red X closes; E to interact), and pick legible fonts. — [Roblox Creators, UI/UX Essentials @ 1:38](https://www.youtube.com/watch?v=lOOvOIJoMi4&t=98s), [@ 3:18](https://www.youtube.com/watch?v=lOOvOIJoMi4&t=198s), [@ 12:11](https://www.youtube.com/watch?v=lOOvOIJoMi4&t=731s)
- **Design UX for the real audience.** Very young players have less manual dexterity. Write user stories, draw flow diagrams, and remove pain points; for example, let players buy consumables in multiples instead of round-tripping to the shop. — [@ 10:53](https://www.youtube.com/watch?v=lOOvOIJoMi4&t=653s), [@ 15:05](https://www.youtube.com/watch?v=lOOvOIJoMi4&t=905s)
- **Measure, then segment.** Experiments can now target new players and break results down by segment (e.g. did the new onboarding help U18 more than 18+?). Difficulty can differ for new players without separate configs. — [DevForum: Evolving Experiments and Analytics](https://devforum.roblox.com/t/evolving-experiments-and-analytics-segmentation-experiment-targeting-early-access-program-and-more/4828462)

## What top-performing sources teach (mined evidence)
- **Tutorials & guidance** — P0, taught by 20 source(s), 5 first-party doc(s)
  - "Guide players through your world using visual indicators. Keep players focused with animated arrows pointing toward important targets." — Henrycooper9, “[RELEASE] OnBoard — Modern, Lightweight Onboarding & Tutorial Framework” <https://devforum.roblox.com/t/release-onboard-%E2%80%94-modern-lightweight-onboarding-tutorial-framework/4751478>
  - "But from this tutorial, you should be able to make all of this right here super easily." — Kingkade 3D, “How To Improve Your UI In Roblox Studio” @ 11:28 <https://www.youtube.com/watch?v=RPqIm0I_gsw&t=688s>
- **Onboarding funnel measurement & experiments** — P0, taught by 19 source(s), 13 first-party doc(s)
  - "Doing this helps make sure that the most amount of players can easily get through your onboarding funnel regardless of their skill level. By utilizing onboarding techniques, you can help direct players through your onboarding funnel smoothly so they can start playing and enjoying your …" — Roblox Creators, “What are onboarding techniques on Roblox?” @ 2:30 <https://www.youtube.com/watch?v=dXqZC4x2Vn8&t=150s>
  - "The steps before this screen already had you speaking instead of typing. So, out of 900-plus apps and websites, 22% of them throws a paywall during onboarding." — Mobbin, “I Studied 1,460 Onboarding Flows. Here's What I Found.” @ 4:42 <https://www.youtube.com/watch?v=Qsq-Sj_rojU&t=282s>
  - Numbers cited: still playing after 5 minutes decreased significantly week-on-week; for more than 180 days , their saved; possible, ideally in 5 minutes or less after; during the first 24 hours of your experiment
- **UI clarity & readability** — P0, taught by 16 source(s), 5 first-party doc(s)
  - "Whether you need to highlight UI elements, guide players toward world locations, or create a complete step-by-step tutorial, OnBoard provides everything needed to get started quickly." — Henrycooper9, “[RELEASE] OnBoard — Modern, Lightweight Onboarding & Tutorial Framework” <https://devforum.roblox.com/t/release-onboard-%E2%80%94-modern-lightweight-onboarding-tutorial-framework/4751478>
  - "Today's video is all about the user interface and user experience design principles and practices that you can use to better communicate with your players and give them a consistent and polished experience in your game." — Roblox Creators, “UI/UX Essentials” @ 0:10 <https://www.youtube.com/watch?v=lOOvOIJoMi4&t=10s>
  - Numbers cited: made in like 10 minutes consider this like
- **First session & first impression** — P1, taught by 13 source(s), 9 first-party doc(s)
  - "If your game includes a level based progression system, you can help players feel that success early by tuning your level curve such a that they level up quickly in the first few minutes of the game." — Roblox Creators, “Onboarding Essentials” @ 6:18 <https://www.youtube.com/watch?v=XfxbdKtSbOI&t=378s>
  - "For example, instead of one boss health value for everyone, you can set a lower value for new players, no separate configs required." — OrogeneIstari, “Evolving Experiments and Analytics: Segmentation, Experiment Targeting, Early Access Program, and More” <https://devforum.roblox.com/t/evolving-experiments-and-analytics-segmentation-experiment-targeting-early-access-program-and-more/4828462>
  - Numbers cited: Baseball had a 30% lift in RFY; plays and a 31% lift in RFY; possible, ideally in 5 minutes or less after; Day 1 Retention is gauged
- **Friction & cognitive load** — P1, taught by 13 source(s), 8 first-party doc(s)
  - "Make sure the metaphor that you pick is clear and helpful rather than confusing." — Roblox Creators, “UI/UX Essentials” @ 14:05 <https://www.youtube.com/watch?v=lOOvOIJoMi4&t=845s>
  - "Your best-selling products are always going to be the ones that solve a specific pain that your players are already feeling, not features that are nice to have, things that feel like must-haves because they're removing friction from the experience." — MoseyTube77, “My Roblox Game Made $43,292 (Here's Exactly How to Monetize Yours)” @ 3:05 <https://www.youtube.com/watch?v=-PoyiiGhoNo&t=185s>
  - Numbers cited: still playing after 5 minutes decreased significantly week-on-week; possible, ideally in 5 minutes or less after
- **Mobile & cross-platform input** — P1, taught by 7 source(s), 3 first-party doc(s)
  - "You want to upload your thumbnail and just see how it's going to look on mobile, on desktop, and on console." — Tizzy RBLX, “How I Make High Quality Roblox Thumbnails with AI” @ 6:19 <https://www.youtube.com/watch?v=az7em1IoBhA&t=379s>
  - "This beta builds on the base Character Controller Library, so it must be enabled for your experience first." — m0bsterlobster, “[Studio Beta] Expanding the Character Controller Library: New Default Abilities & Custom Abilities API” <https://devforum.roblox.com/t/studio-beta-expanding-the-character-controller-library-new-default-abilities-custom-abilities-api/4863739>

## Roblox implementation playbook
- **Tutorials & guidance**: Teach by doing: one instruction at a time, triggered by context, dismissed by completing it. Use world-space guidance (Beam arrow to the next objective, highlighted target) over modal text. A/B test guidance variants (e.g. dialogue vs arrow) with Experiments.
  - APIs: Beam + Attachment, Highlight, ProximityPrompt, Experiments (Creator Hub)
  - Measure: Per-step completion and time-to-complete; Tutorial skip rate
- **Onboarding funnel measurement & experiments**: Instrument every onboarding step with LogOnboardingFunnelStepEvent (ordered, one-time per player). Use LogFunnelStepEvent for recurring funnels (shop flow, quest chains) and Journeys for branching paths. Fix the largest drop-off first, then A/B test the fix with Experiments, broken down by player segment (new vs returning, U18 vs 18+).
  - APIs: AnalyticsService:LogOnboardingFunnelStepEvent, AnalyticsService:LogFunnelStepEvent, Analytics > Journeys, Experiments (segmentation & targeting)
  - Measure: Step-to-step conversion; Overall onboarding completion
- **UI clarity & readability**: Establish a visual hierarchy: one primary action per screen, secondary buttons visibly smaller. Size with Scale and constraints so layouts hold on phones, tablets, PC and console. Keep the HUD minimal during onboarding and reveal panels as they become relevant.
  - APIs: UDim2.fromScale, UIAspectRatioConstraint, UIScale, ScreenGui.ScreenInsets (safe areas)
  - Measure: Misclick / back-out rate on menus; Purchase prompt reach
- **First session & first impression**: Spawn new players directly into the core action; defer menus, lore and settings. Script the first 60 seconds: first action, first reward, first upgrade. Detect first-time players server-side and give them the guided path; skip it for returners.
  - APIs: AnalyticsService:LogOnboardingFunnelStepEvent, DataStoreService (hasCompletedTutorial flag)
  - Measure: Onboarding funnel step completion; First-play bounce rate; D1 retention
- **Friction & cognitive load**: Cut every step between join and fun that does not teach or reward; count clicks to first action. Introduce one concept at a time and confirm understanding through action.
  - Measure: Funnel drop-off per step
- **Mobile & cross-platform input**: Design for touch first: thumb-reachable buttons, no hover-only interactions. Bind actions once for all inputs and test on a real phone and gamepad.
  - APIs: ContextActionService, UserInputService.TouchEnabled / GamepadEnabled
  - Measure: Retention and playtime split by device

## Deliver
1. **First 120 seconds script** (table): time, what the player sees, what they do, how they
   are guided (world-space cue vs UI), the reward, and what is deliberately hidden.
2. **Funnel** — numbered onboarding steps for `AnalyticsService:LogOnboardingFunnelStepEvent`
   (step number, name, completion condition, logged on the server).
3. **Guidance devices** — which cues (beam/arrow, highlight, proximity prompt, NPC line) and
   when each is removed.
4. **HUD reveal plan** — which UI is visible at join, and when each panel appears.
5. **Device notes** — touch targets, thumb zones, text sizes, gamepad navigation.
6. **Returning players** — how the FTUE is skipped or shortened for them.
7. **Experiments** — two A/B tests on the largest expected drop-off steps.
