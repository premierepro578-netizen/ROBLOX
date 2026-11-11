---
name: core-loop-designer
title: Core loop designer
stage: design
inputs: game_concept, genre, target_session_minutes, evidence_core_loop, playbook_core_loop
description: Specifies the moment-to-moment, session and long-term loops with tuning numbers.
---
Design the core gameplay loop for this game.

- **Concept:** {{game_concept}}
- **Genre / references:** {{genre}}
- **Target session length:** {{target_session_minutes}} minutes

## Curated findings (close reading of first-party talks and docs)
{{key_findings_core_loop}}

## What top-performing sources teach (mined evidence)
{{evidence_core_loop}}

## Roblox implementation playbook
{{playbook_core_loop}}

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
