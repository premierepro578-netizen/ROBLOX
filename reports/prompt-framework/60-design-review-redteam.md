<!-- Design review & red team · stage: review · unfilled slots: design_doc -->

Red-team this game design before it is built.

<design>
{{design_doc}}
</design>

Platform changes to check against:
- Effective July 24, 2025, the Engagement-Based Payouts program is deprecated and has been replaced by the Creator Rewards program. (https://create.roblox.com/docs/production/monetization/engagement-based-payouts)

Review it as four people: a veteran player, a 10-year-old new player on a phone, an exploiter,
and a Roblox policy reviewer. Report findings in a table: area, finding, severity
(blocker / major / minor), evidence or reasoning, fix.

Cover:
1. **Loop clarity** — can a new player state the loop after one minute? Where is it muddy?
2. **Onboarding friction** — every step between join and fun that does not teach or reward.
3. **Retention gaps** — what is the reason to come back tomorrow, next week, next month?
4. **Monetization fairness & policy** — pay-to-win, paid random items without odds or
   PolicyService handling, deceptive scarcity, pressure aimed at young players.
5. **Exploits** — client-trusted values, unvalidated remotes, duplication via rejoin/trade,
   non-idempotent purchase grants.
6. **Performance** — what will drop frames or memory on a low-end phone.
7. **Stale assumptions** — anything that relies on a deprecated platform program or API.
End with the three changes that most improve the design.
