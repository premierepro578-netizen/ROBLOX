---
name: analytics-instrumentation
title: Analytics instrumentation plan
stage: measure
inputs: game_systems, evidence_onboarding, evidence_retention
description: Event taxonomy (funnels, economy, custom), dashboards and decision rules.
---
Write the analytics instrumentation plan for these systems:

{{game_systems}}

## Research evidence on what to measure
### Onboarding
{{evidence_onboarding}}

### Retention
{{evidence_retention}}

## Deliver
1. **Onboarding funnel** — ordered steps for `LogOnboardingFunnelStepEvent` (one-time per
   player) with completion conditions.
2. **Recurring funnels** — `LogFunnelStepEvent` funnels (shop flow, quest chain, event) with
   funnel session ids.
3. **Economy** — `LogEconomyEvent` sources and sinks per currency, with transaction types and
   item SKUs.
4. **Custom events** — the few custom events worth tracking and the question each answers.
5. **Dashboards** — the weekly review: D1/D7/D30 by cohort, funnel conversion, playtime,
   payer conversion; what "good" and "alarming" look like for this game.
6. **Decision rules** — for each metric, the threshold that triggers an investigation and
   the first hypothesis to test.
All events are logged from the server; the client never reports its own progress.
