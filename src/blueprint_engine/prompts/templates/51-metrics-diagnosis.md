---
name: metrics-diagnosis
title: Metrics diagnosis & experiment planner
stage: measure
inputs: current_metrics, recent_changes, evidence_retention, evidence_onboarding, evidence_monetization
description: Diagnoses a metrics problem from live data and plans the experiments that fix it.
---
Diagnose this game's metrics and plan the next experiments.

## Live metrics (cohorted where possible)
{{current_metrics}}

## Recent changes and their dates
{{recent_changes}}

## Research evidence
### Onboarding
{{evidence_onboarding}}

### Retention
{{evidence_retention}}

### Monetization
{{evidence_monetization}}

## Deliver
1. **Bottleneck** — the single biggest leak (funnel step, D1, D7, session length, conversion)
   and the data that shows it.
2. **Ranked hypotheses** — up to five causes, each with supporting/contradicting data and the
   research evidence that suggests it.
3. **Experiments** — for the top three: change, metric, expected direction, sample/runtime,
   and the result that would falsify it.
4. **What not to change yet** — systems that are working and must stay stable for attribution.
