# Roblox Game Design — Implementation Report

*Research run of 2026-11-11 · produced with `bpe` (this repository) · curated synthesis on top of the
automatically mined evidence in [`evidence-report.md`](evidence-report.md) and [`blueprint.json`](blueprint.json).*

---

## 1. Executive summary

1. **Fun is the multiplier on everything else.** Every high-performing source puts the core loop
   first. Jailbreak's co-creator: *"if the game isn't fun, 2x of zero is still zero."* Retention
   systems, monetization and discovery all scale an existing fun loop; none of them can create one.
2. **Roblox's recommender rewards retention *and* monetization together.** Recommended for You
   ranks on engagement, return visits, Robux spend and co-play, measured only on players who
   found the game organically. Games strong in both retention and monetization get broader
   distribution than games strong in one. Discovery is therefore an *output* of the other three
   pillars, not a separate marketing task.
3. **The first session decides D1.** Roblox calls the FTUE *"arguably the single most important
   piece of content in a free-to-play game"*. Keep it to a few minutes: teach only movement,
   interaction and the core loop; front-load progress; make it social; and end on aspiration.
4. **Monetization is engagement when it is personal, early and fair.** Top studios (Adopt Me,
   SpongeBob Tower Defense) sell a cheap first purchase fast, personalize offers by player stage,
   sell speed and convenience rather than victory, and monetize every intended mechanic at launch
   so nothing is "taken away" later. Rewarded video ads reach the 80%+ who never pay.
5. **Measure in cohorts and change one thing at a time.** Instrument the onboarding funnel,
   economy flows and branching journeys from the server, then A/B test with segmented
   Experiments. Watch the silent majority's behaviour, not the loudest voices.

**Build order:** instrumentation → core loop vertical slice → FTUE → retention systems →
monetization → discovery and live-ops cadence (see §5).

---

## 2. Research base

| | |
|---|---|
| Sources analysed | **107**: 55 YouTube videos (17.8M combined views), 25 Roblox Creator Docs pages, 20 DevForum threads (12 by Roblox staff), 7 TikToks |
| Words analysed | **196,051** (47 auto-caption and 8 manual-caption transcripts, docs article text, forum posts) |
| Candidates screened | 203 videos from 26 queries → 115 shortlisted with full metadata → 12 dropped as stale → 103 scored → 14 dropped as off-topic → 55 selected; 49 forum threads → 20 kept |
| Insights extracted | **878** timestamped, attributed insights across 5 pillars and 39 mechanics |
| Close reading | RDC 2025 *Retention Playbook* and *Mastering Monetization*; Roblox Creators *Onboarding Essentials*, *UI/UX Essentials*, *Onboarding techniques*, *Core loops*, *Recommended for You*; Roblox staff posts on discovery, Journeys, Experiments, Ads, thumbnails, refunds |

**How sources were chosen.** Videos are ranked by performance × relevance, where
performance = 0.55 view-velocity + 0.25 like-rate + 0.20 channel authority and relevance gates
the score so that viral gameplay videos cannot outrank design content. First-party docs and staff
posts carry a fixed authority score. Every mechanic below is counted by **distinct sources**, not
by mentions.

**Limitations.** Popularity is not correctness, so first-party material is weighted in and
creator claims are checked against it (one stale claim found, §7). Creator figures (ARPPU by
genre, ad fill) are self-reported. TikTok contributed metadata only, because yt-dlp's TikTok search
is broken upstream and these TikToks had no captions. The automated extractor favours explicit
advice; the curated findings in [`config/key-findings.md`](../config/key-findings.md) cover what
it misses.

---

## 3. The strategic model

```
            ┌──────────── fun core loop ────────────┐
            ▼                                       │
  FTUE (first 5 min) ──► D1 ──► reasons to return ──► D7 / D30 ──► trust ──► spend
            ▲                                                         │
            │      Roblox RFY: engagement · return visits · Robux spend · co-play
            └────────── more Home impressions ◄──────────── (organic players only)
```

- **Retrieval** draws on engagement, retention and monetization from *all* players (ads,
  featuring and links included). **Ranking** personalises using organic Home players only.
  ([RFY @ 0:40](https://www.youtube.com/watch?v=K7jsk3bzmvE&t=40s))
- The recommender reads **D1, D2–D7 and D8–D28** windows of play days and playtime, plus co-play
  days, qualified play sessions, spend days and Robux spend. Impressions typically fall *after*
  play-through and playtime fall. ([Docs: Discovery](https://create.roblox.com/docs/discovery))
- Distribution is **relative**: if competitors engage players better, impressions can drop while
  your own metrics hold steady. ([Roblox CGO, DevForum](https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042))
- Roblox's decision rule: if retention is low, make the core game more fun, clear and rewarding;
  if retention is strong, add thoughtful monetization that adds value.

---

## 4. Pillar blueprints

Priority tiers come from cross-source consensus (`P0` = top weight with ≥3 sources, or ≥2
including first-party). The full evidence with deep links is in
[`evidence-report.md`](evidence-report.md).

### 4.1 Core gameplay loop

| Priority | Mechanic | Sources |
|---|---|---|
| P0 | Action → reward → upgrade cycle | 21 (12 creators / 9 first-party) |
| P0 | Progression & pacing | 15 |
| P0 | Variety, skill & mastery | 5 |
| P1 | Game feel (juice), concept & hook, collection, goals | 3–5 each |

**What the evidence says**
- A loop has three layers: minute-to-minute interaction, the most repeated actions, and the
  engine that powers progress. Jailbreak's is explore → complete objective → power up.
  ([Roblox Creators](https://www.youtube.com/watch?v=gkFKF9A-snY&t=59s))
- Bake retention into the loop. Players give you about 15 minutes of focus, so surface one or two
  meta systems on every loop (streak, collection, rank) rather than stacking many.
  ([Leon Fernandes @ 5:43](https://www.youtube.com/watch?v=61BjLzI490g&t=343s))
- Keep the entry simple and hide depth behind gates. Games that bloat make *"the first 90% of the
  game irrelevant"* and collapse. ([Onett @ 33:42](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=2022s))
- Model the economy as taps, drains and converters, and counter power-creep loops.
  ([Game Maker's Toolkit](https://www.youtube.com/watch?v=Zrf1cou_yVo&t=114s))

**Build spec**
1. Write the loop as one sentence and a three-layer table (seconds / minutes / days). Reject
   features that do not feed it.
2. **First loop inside 60 seconds** for a new player: act → reward → spend → visibly stronger.
3. Economy sheet before code: every tap, drain and converter, with time-to-next-upgrade targets for
   the first 10 upgrades. Persist currency and upgrades server-side with `DataStoreService`
   (`UpdateAsync`) or a session-locked profile; validate every `RemoteEvent` on the server.
4. Juice on every core action (`TweenService`, `ParticleEmitter`, sound, number pops), on a
   low-end-phone performance budget.
5. Gate complexity: zones or levels that unlock new verbs, plus at least one decision (route,
   loadout, risk) so mastery has room.

**Measure:** loops completed per session, session length, time to each milestone, D1.
**Prompt:** [`30-core-loop-designer.md`](prompt-framework/30-core-loop-designer.md)

### 4.2 Onboarding & first-time UX

| Priority | Mechanic | Sources |
|---|---|---|
| P0 | Tutorials & guidance | 20 (15 / 5) |
| P0 | Funnel measurement & experiments | 19 (6 / 13) |
| P0 | UI clarity & readability | 16 |
| P1 | First session, friction, mobile input, early wins | 2–14 each |

**What the evidence says** ([Onboarding Essentials](https://www.youtube.com/watch?v=XfxbdKtSbOI), [Onboarding techniques](https://www.youtube.com/watch?v=dXqZC4x2Vn8), [UI/UX Essentials](https://www.youtube.com/watch?v=lOOvOIJoMi4))
- Teach only the essentials (move, interact, the core loop and *why*) and layer depth after the
  first session.
- Level players up quickly in the first minutes, give starter items and some currency, make it
  social, and end with visible mid- and long-term goals plus a congratulatory call to action.
- Use guidance in three forms: subtle visual elements (trails, highlights), contextual
  just-in-time tutorials, and timed hints only for players who struggle.
- "Don't mess with the FTUE." When seasons add content, make the first new items fun but balanced
  against starter gear, and test with genuinely new players
  ([@ 31:24](https://www.youtube.com/watch?v=YgyfcMfxQcI&t=1884s)).
- UI is communication: contextual buttons, attention through colour, size and space, a small
  palette, conventional controls (red X closes, E to interact), legible fonts, and touch-friendly
  sizes for young players.

**Build spec — first 120 seconds**

| Time | Player does | Guidance | Reward / reveal |
|---|---|---|---|
| 0–10 s | Spawns *in* the action (no menus, no lore wall) | Trail or `Beam` to the first target | — |
| 10–40 s | First core action | Contextual prompt (`ProximityPrompt` / HUD hint) | Juicy feedback + currency |
| 40–70 s | First purchase/upgrade with starter currency | Highlight the one button that matters | Visible power jump; first level-up |
| 70–120 s | Second loop, nearby players visible | Timed hint only if stalled | Goals panel appears: next unlock + long-term goal |
| End | Tutorial completes | Congratulatory call to action | New ability unlocked; hub shows what's ahead |

- Log each step server-side with `AnalyticsService:LogOnboardingFunnelStepEvent` (ordered,
  one-time per player). Skip or shorten the FTUE for returning players (persisted flag).
- UI: `UDim2.fromScale` + `UIAspectRatioConstraint`/`UIScale`, safe areas, one primary action per
  screen, and consumables purchasable in multiples.
- Iterate with **Experiments** targeted at new players and broken down by segment (e.g. U18 vs 18+);
  Roblox's example lowers boss health for new players only.
  ([DevForum](https://devforum.roblox.com/t/evolving-experiments-and-analytics-segmentation-experiment-targeting-early-access-program-and-more/4828462))

**Measure:** step-to-step conversion, time to first reward/upgrade, first-play bounce, D1.
**Prompts:** [`32-onboarding-ftue.md`](prompt-framework/32-onboarding-ftue.md), [`50-analytics-instrumentation.md`](prompt-framework/50-analytics-instrumentation.md)

### 4.3 Retention mechanics

| Priority | Mechanic | Sources |
|---|---|---|
| P0 | Retention KPIs & churn | 30 (13 / 17) |
| P0 | Social play & friends | 20 (6 / 14) |
| P0 | Updates, events & live ops | 18 (7 / 11) |
| P1 | Scarcity, daily rewards & streaks, quests, leaderboards, notifications, idle | 6–14 each |

**What the evidence says** ([RDC 2025 Retention Playbook](https://www.youtube.com/watch?v=YgyfcMfxQcI))
- **Cadence beats volume.** Pace content (one gun a week for ten weeks rather than ten at once),
  use season passes to unlock large drops progressively, launch with content held back, and use
  holidays as a default live-ops calendar. Adopt Me ships every Friday, 52 weeks a year.
- **Trust is retention.** Long-lived games protect their vision instead of chasing trends that
  make them "top-heavy".
- **Operate updates.** Watch the first 48 hours for misuse, curate community feedback, run a
  community QA group, and watch what the silent majority does.
- **Personalise rewards** to the player's current friction point and show tomorrow's reward
  ([Leon Fernandes @ 4:13](https://www.youtube.com/watch?v=61BjLzI490g&t=253s)).
- Co-play is a ranking signal, so social play is both a retention lever and a discovery lever.

**Build spec — first three systems**
1. **Daily return loop:** 7-day escalating reward with a visible preview of tomorrow, claimed
   atomically with `UpdateAsync` on server UTC days, a forgiving streak (grace day), and rewards
   personalised to need (hard vs soft currency). Offer notification opt-in
   (`ExperienceNotificationService:PromptOptIn`) *after* a positive moment.
2. **Social hooks:** co-op bonuses for playing with friends, one-tap invites
   (`SocialService:PromptGameInvite`), and show-off moments for other players in the server.
3. **Live-ops pipeline:** weekly or bi-weekly content cadence, a season pass that drip-unlocks, a
   holiday calendar, server-authoritative event windows (`MessagingService`/`MemoryStoreService`),
   Experience Events for announcements, and a 48-hour post-update watch.

**Measure:** D1/D7/D30 by cohort, play days per user (D2–D7, D8–D28), co-play share, event
participation, returning users on update day. Use Analytics → Journeys for branching paths.
**Prompt:** [`31-retention-systems.md`](prompt-framework/31-retention-systems.md)

### 4.4 Monetization

| Priority | Mechanic | Sources |
|---|---|---|
| P0 | Pricing, bundles & offers | 25 (11 / 13) |
| P0 | Conversion & revenue KPIs | 27 (8 / 18) |
| P0 | Developer products (consumables) | 24 (7 / 16) |
| P1 | Passes, ads, subscriptions, fairness, random items, private servers | 5–15 each |

**What the evidence says** ([RDC 2025 Mastering Monetization](https://www.youtube.com/watch?v=MJ-zYfL10Ew))
- *"Monetization is engagement"*: ten players spending 100 Robux beats one spending 1,000 for
  longevity and discovery, so get new players to a first purchase fast (Adopt Me).
- Personalise by stage: starter pack → engagement-deepening item → exclusive, limited high-tier
  offer. SpongeBob TD runs six escalating starter bundles from a 25–99 Robux entry, then elite
  bundles and private offers.
- Pay-to-speed, not pay-to-win. A free taste (2x speed for joining the group) converted a 3x
  product. Never gatekeep basics like movement.
- Monetise every intended mechanic at launch; late monetization draws backlash.
- Prefer consumables where value repeats (MoseyTube77) and place offers where foot traffic is
  (Tizzy RBLX).
- Rewarded video ads: high-traffic placements and natural breaks, a meaningful reward, and
  older superseded passes as ad milestones (SpongeBob TD reports 90%+ fill).
- Let the platform price: Price Optimization ("at no engagement loss") and Regional Pricing (5,000+
  experiences; raised monetization *and* engagement). Item titles and descriptions feed
  personalised ranking.

**Build spec — catalog skeleton**

| Stage | Offer | Type | Rule |
|---|---|---|---|
| New player | Starter pack (tens of Robux, best value in the game, time-limited) | Developer product | Shown only to new players; one per player |
| Casual | Speed/convenience tiers, inventory slots, 2x currency | Passes (permanent) + consumables (boosts) | Earnable more slowly through play |
| Engaged | Value-adds on items they already own; event-week headline item at a known price | Products / limited | Templatised cadence players can plan for |
| Non-payer | Rewarded ads at natural breaks → soft currency tiers, cosmetic at milestone | Rewarded video | Never the only path to progress |
| Fan | Subscription with recurring value (stipend, daily perk) | Subscription | Promotional first-month pricing |

- **Purchase path:** grant inside `MarketplaceService.ProcessReceipt`, persist before returning
  `PurchaseGranted`, and dedupe by `PurchaseId`. Listed products sold outside the game need this
  implemented correctly. Check pass ownership with `UserOwnsGamePassAsync` on join and on
  `PromptGamePassPurchaseFinished`. Handle the **Transaction Refunded** webhook for developer
  products.
- **Personalised shop:** `RankProductsAsync` once at join (strict rate limit) and
  `RecommendTopProductsAsync` via `task.spawn` (needs a sale in the last 28 days).
  ([Docs](https://create.roblox.com/docs/production/monetization/developer-products))
- **Policy:** disclose odds for paid random items and honour
  `PolicyService:GetPolicyInfoForPlayerAsync` restrictions; read prices on the client so price
  tests show each player their price.
- **Economy logging:** `AnalyticsService:LogEconomyEvent` for every source and sink.

**Measure:** payer conversion, time to first purchase, ARPPU, ARPDAU, refund rate, **and**
D7 retention as the guardrail. Roll back any monetization change that lowers D7.
**Prompt:** [`33-monetization-design.md`](prompt-framework/33-monetization-design.md)

### 4.5 Discovery & growth (supporting)

| Priority | Mechanic | Sources |
|---|---|---|
| P0 | Recommendation algorithm | 32 (17 / 15) |
| P0 | Thumbnails, icons & titles | 14 |
| P0 | Paid acquisition | 6 |

- **Required since 2026-10-19:** a custom thumbnail (16:9, ideally 1920×1080; up to five) to get
  any Home recommendation impressions. Thumbnail personalisation averaged **+8.5% qualified
  play-through** in testing.
  ([DevForum](https://devforum.roblox.com/t/homepage-recommendation-eligibility-now-requires-a-custom-thumbnail/4945086), [Docs](https://create.roblox.com/docs/production/publishing/thumbnails))
- **Home gameplay videos:** Superstar Baseball saw +30% RFY plays and +31% playtime; Notoriety
  +41% plays and +39% playtime. Use real current footage of the core loop, not cinematic trailers.
  ([DevForum](https://devforum.roblox.com/t/gameplay-videos-on-home-help-your-games-get-discovered/4842601))
- **Ads:** median 10% lift in D7-retained users; judge on ROAS. Buy traffic only once onboarding
  converts. ([DevForum](https://devforum.roblox.com/t/ads-manager-rdc-recap-earnings-roas-reporting-incrementality/4909790))
- Design thumbnails for phones first and communicate the feeling of play
  ([Tizzy RBLX @ 5:39](https://www.youtube.com/watch?v=az7em1IoBhA&t=339s)).

**Prompt:** [`34-discovery-growth.md`](prompt-framework/34-discovery-growth.md)

---

## 5. Phased execution roadmap

Exit criteria are relative on purpose. Set absolute targets from the benchmark comparison in your
own Creator Analytics dashboard, not from internet folklore.

| Phase | Build | Exit criteria |
|---|---|---|
| **0 · Instrument** | Onboarding funnel steps, economy events, custom events, journeys; server-side logging; a dashboard (D1/D7/D30 by cohort, funnel, playtime, payer conversion) | Every planned step and currency flow appears in Analytics |
| **1 · Core loop slice** | One complete loop with juice, economy sheet, persistence, server validation | Friends-and-family playtest: new players complete a loop inside 60 s and choose to keep playing |
| **2 · FTUE** | 120-second script, guidance devices, returning-player skip, HUD reveal plan, mobile pass | No single funnel step loses a disproportionate share of players; D1 improves cohort over cohort |
| **3 · Retention** | Daily return loop, social hooks, quests and goals panel, notification opt-in, live-ops pipeline | D7 and play days per user (D2–D7) trend up; update days lift returning users |
| **4 · Monetization** | Starter pack, pass/consumable ladder, receipts and refunds, personalised shop, rewarded ads, price optimisation | Payer conversion and time to first purchase improve **without** a D7 drop |
| **5 · Discovery & live ops** | Custom thumbnails plus personalisation, Home gameplay video, ad tests on ROAS, weekly or bi-weekly cadence | Home impressions and play-through rise; cadence sustained for 8+ weeks |

Run a red-team review ([`60-design-review-redteam.md`](prompt-framework/60-design-review-redteam.md))
at the end of phases 1, 2 and 4.

---

## 6. Instrumentation plan (minimum viable)

| Event | API | When |
|---|---|---|
| Onboarding steps 1…N | `AnalyticsService:LogOnboardingFunnelStepEvent` | Each FTUE milestone, once per player |
| Shop / quest / event funnels | `AnalyticsService:LogFunnelStepEvent` | Each step, with a funnel session id |
| Currency sources and sinks | `AnalyticsService:LogEconomyEvent` | Every grant, spend and purchase |
| Key moments | `AnalyticsService` custom events | Level-up, rebirth, first co-op session |
| Branching paths | Analytics → Journeys | Shop vs match vs power-up routes |
| A/B tests | Experiments (targeting + segmentation) | One change at a time; new players only for FTUE tests |

All events are logged from the server. The client never reports its own progress or purchases.

---

## 7. Platform changes and stale advice

- **Engagement-Based Payouts were deprecated on 2025-07-24** and replaced by Creator Rewards
  ([Docs](https://create.roblox.com/docs/production/monetization/engagement-based-payouts)).
  The pipeline flags any creator advice that still optimises for Premium payouts (⚠️ in the
  evidence report).
- Custom thumbnails became mandatory for Home recommendations on 2026-10-19.
- `GamePassService` is deprecated in favour of `MarketplaceService`
  ([BrawlDev](https://www.youtube.com/watch?v=nh7MYYL5CGE)).
- Developer subscriptions in Robux with promotional pricing were announced at RDC 2025 for 2026.
  Check the live docs before relying on availability.

---

## 8. Guardrails

Roblox's audience skews young, and Roblox's own guidance asks for monetization that is *"fair and
transparent"*, with offers integrated into progression *"rather than interrupting gameplay or
putting enjoyment behind a paywall"* ([CGO post](https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042)).
In practice:

- **No deceptive urgency.** Creator advice that treats FOMO as *"the ultimate retention weapon"*
  is flagged in the evidence. Use real end dates, earnable paths and rotations back in.
- **No pay-to-win in competitive play.** Sell speed, convenience and cosmetics, and keep every
  paid advantage reachable through play.
- **Paid random items:** disclose odds and honour `PolicyService` restrictions per player.
- **No pop-up spam.** One relevant offer at a natural moment beats three at once (SpongeBob TD).
- **Security:** server authority over currency, rewards and purchases; validated remotes;
  idempotent receipts; refund handling.

These are also commercial rules. The same sources show trust, long-term retention and broad,
low-ticket conversion are what the recommender rewards.

---

## 9. The prompt framework

[`prompt-framework/`](prompt-framework/README.md) contains 12 prompts. Each is pre-filled with the
curated findings, the mined evidence (with deep links) and the Roblox playbook for its pillar;
only the designer-specific slots (`{{game_concept}}`, `{{current_metrics}}`, …) remain.

| Stage | Prompt | Use |
|---|---|---|
| System | `00-architect-system` | System prompt for every session: evidence-first, server-authoritative, measured, fair |
| Analysis | `10-extract-insights`, `20-synthesize-blueprint` | Power the Claude extractor; synthesise new research |
| Design | `30` core loop → `32` FTUE → `31` retention → `33` monetization → `34` discovery | Chain in this order; each output feeds the next prompt's `game_concept` |
| Build | `40-luau-implementation-spec` | One blueprint item → modules, data model, remotes, receipts, tests, `--!strict` Luau |
| Measure | `50-analytics-instrumentation`, `51-metrics-diagnosis` | Event plan; diagnose live metrics into ranked experiments |
| Review | `60-design-review-redteam` | Four-persona red team: veteran, 10-year-old on a phone, exploiter, policy reviewer |

Render one prompt with your inputs:

```bash
bpe prompts render onboarding-ftue --var game_concept="co-op pet battler" --var target_devices="phone first, PC"
```

---

## 10. Re-running and extending the research

```bash
pip install -e '.[dev]'          # yt-dlp, requests, bs4, lxml
bpe run                          # discover → fetch → analyze → synthesize (cached, resumable)
bpe analyze --extractor claude   # optional: schema-constrained Claude extraction (needs credentials)
bpe synthesize                   # rebuild reports and prompts
```

- Add queries, doc pages, TikTok handles or forum searches in
  [`config/research.toml`](../config/research.toml). Re-runs fetch only new items.
- Update [`config/key-findings.md`](../config/key-findings.md) after a close reading. It flows
  into every pillar prompt.
- Network hosts needed: `www.youtube.com`, `youtube.com`, `www.tiktok.com`, `create.roblox.com`,
  `devforum.roblox.com`. From cloud IPs, transcripts come from yt-dlp caption tracks
  (`youtube-transcript-api` is blocked there but works from residential IPs).
