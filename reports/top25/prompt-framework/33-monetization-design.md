<!-- Monetization designer (fair by construction) · stage: design · unfilled slots: game_concept, audience -->

Design the monetization for this game.

- **Concept, core loop and economy:** {{game_concept}}
- **Audience (age range, regions, platforms):** {{audience}}

## Curated findings (close reading of first-party talks and docs)
- **"Monetization is engagement."** Ten players spending 100 Robux beats one spending 1,000 for longevity and for discovery, so get new players to a first purchase fast. — Jesse (Adopt Me), [RDC 2025 Mastering Monetization @ 22:37](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1357s)
- **Personalise by player stage.** New players get a cheap starter pack; casual players an item that deepens engagement; high spenders exclusive, limited offers. SpongeBob Tower Defense runs six escalating starter bundles from a 25–99 Robux entry point, then elite bundles. — Roblox, [@ 3:17](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=197s); Zach (SpongeBob Tower Defense), [@ 21:23](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1283s)
- **Sell speed and convenience, not victory.** "Extremely free to play, but it's pay to speed." A free taste (2x speed for joining the group) converted a 3x product. Never gatekeep basics like movement. — Zach, [@ 20:52](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1252s), [@ 25:02](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1502s)
- **Monetise every intended mechanic at launch.** Adding a paid tier later feels like taking something away, and late monetisation draws "here comes pay-to-win" backlash. Avoid high-priced offers to brand-new players. — Zach, [@ 23:11](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1391s), [@ 30:48](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1848s)
- **Make spending plannable.** Adopt Me uses a templatised cadence, e.g. a known 1,000-Robux legendary pet each event week, plus value-adds (fly/ride potions) for engaged players. — Jesse, [@ 14:21](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=861s)
- **Rewarded video ads reach the 80%+ of players who never pay.** Place them in high-traffic areas (lobby, shop) and natural breaks (between levels), teach players about them, and make the reward meaningful. SpongeBob TD gives tiered soft currency plus a tradable cosmetic after 10 ads, and older, superseded passes as ad milestones, reporting 90%+ fill. — Roblox, [@ 7:45](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=465s), [@ 9:17](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=557s); Zach, [@ 15:34](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=934s), [@ 18:07](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1087s)
- **Let the platform price.** Price Optimization finds prices "at no engagement loss", and Regional Pricing (5,000+ experiences) raised monetisation *and* engagement. Item titles and descriptions now feed personalised item ranking, so write them well. — Roblox, [@ 4:01](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=241s), [@ 4:44](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=284s), [@ 5:22](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=322s)
- **Prefer consumables for repeatable value.** Turning would-be consumables (e.g. 2x offline earnings) into game passes caps revenue. Best sellers remove a pain players already feel. — MoseyTube77, [@ 4:55](https://www.youtube.com/watch?v=-PoyiiGhoNo&t=295s), [@ 3:05](https://www.youtube.com/watch?v=-PoyiiGhoNo&t=185s). Place developer products where foot traffic is, and judge them on playtime as well as Robux. — Tizzy RBLX, [@ 11:13](https://www.youtube.com/watch?v=zoz3PSMqets&t=673s), [@ 14:38](https://www.youtube.com/watch?v=zoz3PSMqets&t=878s)
- **Genre sets the ceiling.** One studio estimates ARPPU around $2 in hyper-casual "brainrot" games versus around $20 in tower defense with deeper mechanics. Selling exclusive units can hurt one and strengthen the other's trade economy. — Zach, [@ 29:11](https://www.youtube.com/watch?v=MJ-zYfL10Ew&t=1751s)
- **Platform mechanics to build against (first-party):** grant developer products in `ProcessReceipt` (Listed products sold outside the game need it implemented correctly); personalise the shop with `RankProductsAsync` / `RecommendTopProductsAsync`; handle the Transaction Refunded webhook; developer subscriptions in Robux (with promotional pricing) were announced at RDC 2025 for 2026. Engagement-Based Payouts were **deprecated on 2025-07-24** (replaced by Creator Rewards). — [Docs: Developer Products](https://create.roblox.com/docs/production/monetization/developer-products), [DevForum: Refund webhook](https://devforum.roblox.com/t/new-transaction-refunded-webhook-notifies-when-a-purchase-is-cancelled/4890339), [Docs: Engagement-based payouts](https://create.roblox.com/docs/production/monetization/engagement-based-payouts)

## What top-performing sources teach (mined evidence)
- **Pricing, bundles & offers** — P0, taught by 5 source(s)
  - "You can also adjust the upgrade prices and income rates to make sure progression feels rewarding without becoming too easy or too slow." — GuideRealm, “How To Make An ENTIRE Roblox Game With AI - Full Guide” @ 7:32 <https://www.youtube.com/watch?v=ltbZzXRrDF8&t=452s>
  - "I'm going to set mine to be 20 Robux. Really cheap, but uh don't make it too expensive, otherwise people won't buy it." — CodeBro29, “How to make your FIRST Roblox Game (Make Robux)” @ 25:30 <https://www.youtube.com/watch?v=-QSmtYVMRH4&t=1530s>
  - Numbers cited: mine to be 20 Robux . Really cheap
- **Paid random items (eggs, crates)** — P1, taught by 2 source(s)
  - "So, right now, the eggs don't work right. And I think what I need to do is tell the client to throw the eggs instead of the server. In non stupid nerd words, we need to give the player's device control over the eggs so …" — Duckable, “Can I Make a VIRAL TYCOON in 24 HOURS?” @ 10:08 <https://www.youtube.com/watch?v=F9sfnpkzcPw&t=608s>
  - "We are perfectly engineering this to make sure there is no way to somehow pay Robux and buy these loot boxes." — Laugh, “I Accidentally Made a Viral Roblox Game” @ 11:41 <https://www.youtube.com/watch?v=WFyrlstSDe4&t=701s>
- **Developer products (consumables)** — P1, taught by 1 source(s)
  - Numbers cited: if you skip 10 seconds you might miss
- **Ads (rewarded, immersive, sponsored)** — P1, taught by 1 source(s)
- **Conversion & revenue KPIs** — P1, taught by 1 source(s)
  - "You need to understand marketing, game design, retention, monetization, balancing, psychology, and more. It's not a get-richqu scheme." — waveshine, “Watch this before making ROBLOX Games” @ 1:05 <https://www.youtube.com/watch?v=xnlaYLnCtFc&t=65s>
- **Fairness & player trust** — P1, taught by 1 source(s)
  - "to be greedy instead of wanting to make a fun experience and from what I've heard the Roblox algorithm seems to push games that make a lot of money which in turn makes the game more popular and thus makes more money regardless of if …" — BinzuDev, “How I Learned To Make Roblox Games in a Week” @ 37:09 <https://www.youtube.com/watch?v=vUN2cJD4mUk&t=2229s>

## Roblox implementation playbook
- **Pricing, bundles & offers**: Build a price ladder: a low-friction starter offer, core items, and premium bundles that anchor value. Use Price Optimization and Regional Pricing instead of guessing; re-test after major updates. Read prices with GetProductInfo on the client so price-optimisation tests show each player their price. Sell the first purchase cheaply (tens of Robux); many small payers beat one big spender for retention and discovery.
  - APIs: Price Optimization (Creator Hub), Regional pricing, MarketplaceService:GetProductInfo
  - Measure: Conversion by price point; Revenue per DAU
- **Paid random items (eggs, crates)**: If you sell random items, disclose odds before purchase and keep items earnable through play. Check PolicyService for each player and offer a direct-purchase path where paid random items are restricted.
  - APIs: PolicyService:GetPolicyInfoForPlayerAsync (ArePaidRandomItemsRestricted)
  - Measure: Conversion vs refund/complaint signals; Retention of payers
- **Developer products (consumables)**: Sell consumables (boosts, currency packs, revives) as developer products. Grant inside MarketplaceService.ProcessReceipt and return PurchaseGranted only after the grant is saved; dedupe by PurchaseId. Offer products in context (revive on death, boost before a hard section) and allow buying several consumables at once. Order the shop per player with the product intelligence APIs (RankProductsAsync once at join; RecommendTopProductsAsync via task.spawn). Subscribe to the Transaction Refunded webhook and claw back refunded developer-product grants in your own data.
  - APIs: MarketplaceService:PromptProductPurchase, MarketplaceService.ProcessReceipt, RankProductsAsync / RecommendTopProductsAsync, Transaction Refunded webhook, AnalyticsService:LogEconomyEvent
  - Measure: Payer conversion; ARPPU; Repeat purchase rate; Refund rate
- **Ads (rewarded, immersive, sponsored)**: Treat rewarded ads as opt-in value exchanges placed at natural pauses. Use Ads Manager campaigns to buy acquisition only after onboarding converts well.
  - APIs: Ads Manager (Creator Hub), Immersive ads
  - Measure: Cost per acquired player vs their D7 value
- **Conversion & revenue KPIs**: Log every purchase and currency flow with LogEconomyEvent to see sources, sinks and paths to purchase. Increase conversion by placing offers where players feel the need, not by adding more offers.
  - APIs: AnalyticsService:LogEconomyEvent, Creator Hub Analytics: Monetization
  - Measure: Payer conversion; ARPDAU; ARPPU
- **Fairness & player trust**: Sell time savings, convenience and cosmetics; keep competitive outcomes skill-based. Make every paid advantage reachable through play, slower.
  - Measure: Retention of non-payers; Review / like ratio

## Deliver
1. **Catalog** (table): item, type (pass / developer product / subscription / private
   server), what it does, starting price in Robux, placement moment (when the player feels
   the need), and whether it is earnable through play.
2. **Price ladder** — the first-purchase offer, core range and anchor bundle, with the
   reasoning; how Price Optimization / Regional Pricing will be used to tune it.
3. **Purchase flow** — server-side grant path: `ProcessReceipt` with PurchaseId dedupe and
   persist-before-grant; pass ownership checks on join and on purchase.
4. **Policy & fairness** — paid random items (odds disclosure, `PolicyService` handling),
   competitive fairness, and what you will not sell.
5. **Economy instrumentation** — `LogEconomyEvent` sources and sinks for each currency.
6. **KPIs and guardrails** — payer conversion, ARPPU, ARPDAU, and the retention signal that
   would make you roll back a monetization change.
