---
name: retention-systems
title: Retention systems designer
stage: design
inputs: game_concept, current_metrics, evidence_retention, playbook_retention
description: Maps D1/D7/D30 levers to concrete systems, data models and a live-ops calendar.
---
Design the retention systems for this game.

- **Concept & core loop:** {{game_concept}}
- **Current metrics (D1/D7/D30, session length, playtime; "pre-launch" if none):** {{current_metrics}}

## Curated findings (close reading of first-party talks and docs)
{{key_findings_retention}}

## What top-performing sources teach (mined evidence)
{{evidence_retention}}

## Roblox implementation playbook
{{playbook_retention}}

## Deliver
1. **Lever map** (table): which mechanic targets D1, D7 and D30, and why — cite evidence.
2. **Three systems to build first**, each with: player-facing behaviour, server data model
   (fields + types), claim/reset rules in UTC, edge cases (rejoin, server hop, two servers at
   once), and its KPI.
3. **Social hooks** — how playing with friends is rewarded, and the invite moment.
4. **Live-ops calendar** — 8 weeks of updates/events with cadence, content scope and the
   metric each one should move.
5. **Re-engagement** — notification opt-in moment and the 2-3 notifications worth sending.
6. **Experiments** — the first three A/B tests, each with hypothesis, variant, metric and
   minimum runtime.
7. **Anti-patterns avoided** — pressure tactics you deliberately did not use, and why.
