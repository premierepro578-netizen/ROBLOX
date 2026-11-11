---
name: synthesize-blueprint
title: Cross-source synthesis -> execution blueprint
stage: synthesis
inputs: insights_json, research_summary
description: Turns extracted insights from many sources into a ranked, buildable blueprint.
---
Below are actionable insights extracted from multiple top-performing game-design sources
(videos, first-party docs, forum threads). Each has a pillar, mechanic, evidence quote,
source and timestamp.

<insights>
{{insights_json}}
</insights>

Context from the research run:
{{research_summary}}

Produce an execution blueprint:

1. **Consensus map** — for each pillar, the mechanics that independent sources agree on.
   Count distinct sources, not mentions. Separate first-party (Roblox docs) from creators.
2. **Conflicts** — where sources disagree (e.g. tutorial length, pricing), state both
   positions, who holds them, and the context in which each is right.
3. **Blueprint items** — for every P0/P1 mechanic: the player-facing behaviour, the system
   to build, its data and server responsibilities, the KPI it moves, and the evidence (cite).
4. **Sequencing** — a build order across pillars with dependencies (e.g. analytics funnel
   before onboarding iteration; core loop before monetization).
5. **Red flags** — tactics in the evidence that risk player trust or platform policy, and
   any advice contradicted by platform changes. Do not include these in the blueprint
   without a fair alternative.

Do not invent sources or numbers. If the evidence for an item is thin (one source), say so.
