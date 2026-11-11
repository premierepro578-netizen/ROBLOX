---
name: onboarding-ftue
title: Onboarding / FTUE designer
stage: design
inputs: game_concept, target_devices, evidence_onboarding, playbook_onboarding
description: Second-by-second first-session script with funnel instrumentation and UI rules.
---
Design the first-time user experience (FTUE) for this game.

- **Concept & core loop:** {{game_concept}}
- **Target devices:** {{target_devices}}

## What top-performing sources teach (research evidence)
{{evidence_onboarding}}

## Roblox implementation playbook
{{playbook_onboarding}}

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
