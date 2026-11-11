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
- **Pricing, bundles & offers** — P0, taught by 25 source(s), 13 first-party doc(s)
  - "So, for example, if you're selling a game pass for 100 Robux and if someone buys it, you get 70 Robux instead of 100 because what's 30% of 100 is 70." — Insightspeep, “How To Create & Publish A Gamepass! [Roblox]” @ 2:36 <https://www.youtube.com/watch?v=WT_FGN4usok&t=156s>
  - "So you can price this to be whatever you want. I can just price it to be 100 just to keep it simple." — BrawlDev, “Gamepasses (One-Time Robux Pass & DataStore Receipt) - Roblox Advanced Scripting #21 (2024)” @ 6:01 <https://www.youtube.com/watch?v=nh7MYYL5CGE&t=361s>
  - Numbers cited: would buy a 400 Robux developer product, you’d; the equivalent of 1 Robux worth of soft; There is a 30 day escrow hold for; the sale for 30 days , starting from
  - WARNING (platform change): Engagement-Based Payouts were deprecated effective 2025-07-24 and replaced by Creator Rewards.
- **Conversion & revenue KPIs** — P0, taught by 27 source(s), 18 first-party doc(s)
  - "So, for example, if you're selling a game pass for 100 Robux and if someone buys it, you get 70 Robux instead of 100 because what's 30% of 100 is 70." — Insightspeep, “How To Create & Publish A Gamepass! [Roblox]” @ 2:36 <https://www.youtube.com/watch?v=WT_FGN4usok&t=156s>
  - "That's what developer products are in Roblox. And the more that you can design your monetization around consumables, the more money that you can make per player, instead of depending entirely on new players coming in." — MoseyTube77, “My Roblox Game Made $43,292 (Here's Exactly How to Monetize Yours)” @ 1:39 <https://www.youtube.com/watch?v=-PoyiiGhoNo&t=99s>
  - Numbers cited: back $100, that’s 100% ROAS. [See here; during the first 24 hours of your experiment; also update every 5 minutes so you can; There is a 30 day escrow hold for
- **Developer products (consumables)** — P0, taught by 24 source(s), 16 first-party doc(s)
  - "Just don't make the mistake of turning things that could be consumables into game passes. 2x offline earnings, for example, way more valuable as a developer product because players will buy it over and over every time they log back in." — MoseyTube77, “My Roblox Game Made $43,292 (Here's Exactly How to Monetize Yours)” @ 4:55 <https://www.youtube.com/watch?v=-PoyiiGhoNo&t=295s>
  - "Check results is not just did I make more Robux. You want to also see, did this dev product absolutely cook my playtime?" — Tizzy RBLX, “Roblox Game Monetization Explained Like You're 5” @ 14:38 <https://www.youtube.com/watch?v=zoz3PSMqets&t=878s>
  - Numbers cited: would buy a 400 Robux developer product, you’d; coins, a permanent 2x multiplier, or a; underused but sticky: 82% of users skip; yet it has 0% churn
- **Passes (permanent perks)** — P1, taught by 15 source(s), 6 first-party doc(s)
  - "So, for example, if you're selling a game pass for 100 Robux and if someone buys it, you get 70 Robux instead of 100 because what's 30% of 100 is 70." — Insightspeep, “How To Create & Publish A Gamepass! [Roblox]” @ 2:36 <https://www.youtube.com/watch?v=WT_FGN4usok&t=156s>
  - "You should not use game pass service because not only is it a deprecated feature but also marketplace service has everything that game pass service does but in a more modern and safe way." — BrawlDev, “Gamepasses (One-Time Robux Pass & DataStore Receipt) - Roblox Advanced Scripting #21 (2024)” @ 7:45 <https://www.youtube.com/watch?v=nh7MYYL5CGE&t=465s>
  - Numbers cited: coins, a permanent 2x multiplier, or a; into game passes. 2x offline earnings, for; pass can cost 100 Robux; game pass for 100 Robux and if someone
- **Ads (rewarded, immersive, sponsored)** — P1, taught by 9 source(s), 5 first-party doc(s)
  - "Ideally, you want to make sure it has a good CTR because that means lots of people click on it and it'll be cheaper later when you spend a lot to advertise." — CallMeDogey, “How to ACTUALLY Advertise Your Roblox Game” @ 6:21 <https://www.youtube.com/watch?v=7QfaQe4rsq8&t=381s>
  - "so there's no longer ambiguity on why your game doesn't hit algo or why it dies, how much you should spend on ads, how often should you run ads?" — Tizzy RBLX, “The Roblox Algorithm Explained Like You're 5 Years Old” @ 0:22 <https://www.youtube.com/watch?v=inWzxY26NXo&t=22s>
  - Numbers cited: back $100, that’s 100% ROAS. [See here; for example " 50% off" or "Free
- **Subscriptions** — P1, taught by 11 source(s), 10 first-party doc(s)
  - "Subscriptions that provide access to the game, i.e. you can't play if you don't pay, and subscriptions that provide benefits, such as additional player slots, higher level caps, or monthly in-game currency allowances, but didn't give you the boot when you stopped paying." — Extra Credits, “Monetization Madness - How Games Make Money - Extra Credits” @ 3:00 <https://www.youtube.com/watch?v=qX3xW6nO4zw&t=180s>
  - "Offer items, passes, developer products, subscriptions, or rewarded video ads that are clear, useful, and connected to how people play." — GoGrowGoGoGo, “Boost Your Discovery by Building Games People Want to Play” <https://devforum.roblox.com/t/boost-your-discovery-by-building-games-people-want-to-play/4779042>
  - Numbers cited: that sells for 100 Robux , assess the; or equal to 49 Robux . Regional Pricing; Robux once every 60 days . For price; receive at least 30 days ' notice from

## Roblox implementation playbook
- **Pricing, bundles & offers**: Build a price ladder: a low-friction starter offer, core items, and premium bundles that anchor value. Use Price Optimization and Regional Pricing instead of guessing; re-test after major updates. Read prices with GetProductInfo on the client so price-optimisation tests show each player their price. Sell the first purchase cheaply (tens of Robux); many small payers beat one big spender for retention and discovery.
  - APIs: Price Optimization (Creator Hub), Regional pricing, MarketplaceService:GetProductInfo
  - Measure: Conversion by price point; Revenue per DAU
- **Conversion & revenue KPIs**: Log every purchase and currency flow with LogEconomyEvent to see sources, sinks and paths to purchase. Increase conversion by placing offers where players feel the need, not by adding more offers.
  - APIs: AnalyticsService:LogEconomyEvent, Creator Hub Analytics: Monetization
  - Measure: Payer conversion; ARPDAU; ARPPU
- **Developer products (consumables)**: Sell consumables (boosts, currency packs, revives) as developer products. Grant inside MarketplaceService.ProcessReceipt and return PurchaseGranted only after the grant is saved; dedupe by PurchaseId. Offer products in context (revive on death, boost before a hard section) and allow buying several consumables at once. Order the shop per player with the product intelligence APIs (RankProductsAsync once at join; RecommendTopProductsAsync via task.spawn). Subscribe to the Transaction Refunded webhook and claw back refunded developer-product grants in your own data.
  - APIs: MarketplaceService:PromptProductPurchase, MarketplaceService.ProcessReceipt, RankProductsAsync / RecommendTopProductsAsync, Transaction Refunded webhook, AnalyticsService:LogEconomyEvent
  - Measure: Payer conversion; ARPPU; Repeat purchase rate; Refund rate
- **Passes (permanent perks)**: Sell permanent quality-of-life or prestige perks (VIP area, 2x currency, extra slots) as passes. Check ownership on join with UserOwnsGamePassAsync and on PromptGamePassPurchaseFinished. Show what the pass does in-game at the moment it would help.
  - APIs: MarketplaceService:PromptGamePassPurchase, MarketplaceService:UserOwnsGamePassAsync, MarketplaceService.PromptGamePassPurchaseFinished
  - Measure: Pass conversion rate; Revenue per pass; Retention of buyers vs non-buyers
- **Ads (rewarded, immersive, sponsored)**: Treat rewarded ads as opt-in value exchanges placed at natural pauses. Use Ads Manager campaigns to buy acquisition only after onboarding converts well.
  - APIs: Ads Manager (Creator Hub), Immersive ads
  - Measure: Cost per acquired player vs their D7 value
- **Subscriptions**: Use subscriptions for recurring value (monthly currency stipend, daily perks), not one-time items. Check status server-side with GetUserSubscriptionStatusAsync and react to UserSubscriptionStatusChanged.
  - APIs: MarketplaceService:GetUserSubscriptionStatusAsync, Players.UserSubscriptionStatusChanged, MarketplaceService:GetSubscriptionProductInfoAsync
  - Measure: Subscriber count; Churn / renewal rate

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
