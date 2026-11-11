# Game Design Prompt Framework

Rendered from the research run of 2026-11-11 06:23 UTC. Each prompt below already contains the relevant
curated findings (close reading of first-party talks and docs), the automatically mined evidence (quotes
with deep links) and the curated Roblox playbook. `{{slots}}` that remain are
for you to fill in: your concept, metrics or spec.

**How to use:** paste `00-architect-system.md` as the system prompt, then one task prompt as the user
message. Chain them: concept → core loop → onboarding → retention → monetization → implementation spec
→ analytics → red-team review. Re-render after every research run: `bpe prompts render --all`.

| # | Prompt | Stage | You fill in |
|---|---|---|---|
| 00 | [System prompt — Game Design Architect](00-architect-system.md) — Base system prompt for every design session; pair it with any task prompt. | system | – |
| 10 | [Source -> actionable insight extraction](10-extract-insights.md) — System prompt for the Claude extractor. One source in, schema-constrained insights out. | analysis | – |
| 20 | [Cross-source synthesis -> execution blueprint](20-synthesize-blueprint.md) — Turns extracted insights from many sources into a ranked, buildable blueprint. | synthesis | `insights_json` |
| 30 | [Core loop designer](30-core-loop-designer.md) — Specifies the moment-to-moment, session and long-term loops with tuning numbers. | design | `game_concept`, `genre`, `target_session_minutes` |
| 31 | [Retention systems designer](31-retention-systems.md) — Maps D1/D7/D30 levers to concrete systems, data models and a live-ops calendar. | design | `game_concept`, `current_metrics` |
| 32 | [Onboarding / FTUE designer](32-onboarding-ftue.md) — Second-by-second first-session script with funnel instrumentation and UI rules. | design | `game_concept`, `target_devices` |
| 33 | [Monetization designer (fair by construction)](33-monetization-design.md) — Catalog, price ladder, placement moments, policy compliance and economy logging. | design | `game_concept`, `audience` |
| 34 | [Discovery & growth planner](34-discovery-growth.md) — Thumbnail/icon tests, recommendation signals and an acquisition plan. | design | `game_concept`, `current_metrics` |
| 35 | [Thumbnail & icon art-direction brief](35-thumbnail-icon-brief.md) — Turns the thumbnail research into 5 testable 16:9 thumbnail concepts and 3 icon concepts for a Roblox game. | design | `game_concept`, `core_hook`, `brand_character` |
| 40 | [Blueprint item -> Luau implementation spec](40-luau-implementation-spec.md) — Turns one blueprint item into a server-authoritative Luau module spec with tests. | build | `feature_spec`, `game_architecture` |
| 50 | [Analytics instrumentation plan](50-analytics-instrumentation.md) — Event taxonomy (funnels, economy, custom), dashboards and decision rules. | measure | `game_systems` |
| 51 | [Metrics diagnosis & experiment planner](51-metrics-diagnosis.md) — Diagnoses a metrics problem from live data and plans the experiments that fix it. | measure | `current_metrics`, `recent_changes` |
| 60 | [Design review & red team](60-design-review-redteam.md) — Critiques a design for loop clarity, friction, fairness, policy, exploits and mobile performance. | review | `design_doc` |
