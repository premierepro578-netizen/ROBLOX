---
name: luau-implementation-spec
title: Blueprint item -> Luau implementation spec
stage: build
inputs: feature_spec, game_architecture
description: Turns one blueprint item into a server-authoritative Luau module spec with tests.
---
Turn this blueprint item into an implementation spec for a Roblox (Luau) codebase.

## Blueprint item
{{feature_spec}}

## Existing architecture (frameworks, data layer, folder layout; "greenfield" if none)
{{game_architecture}}

## Deliver
1. **Modules** — server / client / shared modules with one-line responsibilities and where
   each lives (ServerScriptService, ReplicatedStorage, StarterPlayerScripts).
2. **Data model** — persisted schema with types, defaults and a version field; migration
   from the previous version.
3. **Persistence** — read/write path: session-locked profile or `UpdateAsync`, save on leave
   and in `game:BindToClose`, retry/backoff, what happens on DataStore outage.
4. **Network API** — every RemoteEvent/RemoteFunction: direction, payload types, server-side
   validation (type, range, rate limit, ownership) and the exploit it prevents.
5. **Purchases** (if any) — `ProcessReceipt` flow: PurchaseId dedupe, persist-before-grant,
   return values, handling of player-left-mid-purchase.
6. **Analytics** — the exact `AnalyticsService` calls (funnel / economy / custom events).
7. **Edge cases** — rejoin, server hop, two servers at once, clock skew, partial failure.
8. **Tests** — unit tests for pure logic (reward math, streak rules) and a manual test script
   for Studio (with a multi-client test for replication).
9. **Code** — the core server module in Luau with `--!strict` types. Keep it idiomatic and
   commented only where intent is non-obvious.
