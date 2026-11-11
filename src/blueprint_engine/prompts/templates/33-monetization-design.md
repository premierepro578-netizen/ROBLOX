---
name: monetization-design
title: Monetization designer (fair by construction)
stage: design
inputs: game_concept, audience, evidence_monetization, playbook_monetization
description: Catalog, price ladder, placement moments, policy compliance and economy logging.
---
Design the monetization for this game.

- **Concept, core loop and economy:** {{game_concept}}
- **Audience (age range, regions, platforms):** {{audience}}

## Curated findings (close reading of first-party talks and docs)
{{key_findings_monetization}}

## What top-performing sources teach (mined evidence)
{{evidence_monetization}}

## Roblox implementation playbook
{{playbook_monetization}}

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
