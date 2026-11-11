<!-- Analytics instrumentation plan · stage: measure · unfilled slots: game_systems -->

Write the analytics instrumentation plan for these systems:

{{game_systems}}

## Research evidence on what to measure
### Onboarding
- **Tutorials & guidance** — P0, taught by 5 source(s)
  - "If you want to redo something, you can either click this arrow right here or you can click control shift Z and that'll redo what you just did." — CodeBro29, “How to make your FIRST Roblox Game (Make Robux)” @ 3:24 <https://www.youtube.com/watch?v=-QSmtYVMRH4&t=204s>
  - "In my opinion, if you're a beginner, you should start with YouTube tutorials as a guide." — MikoLikesHat, “How to ACTUALLY LEARN to Script in Roblox Studio (5 Steps to learn)” @ 5:21 <https://www.youtube.com/watch?v=GE6Z1n57yDU&t=321s>
- **UI clarity & readability** — P1, taught by 2 source(s)
  - "Instead of switching between different design tools or trying to learn complex software just to make UI elements, you can simply describe what you want, like a coin icon, a shop menu, or even a full UI style, and Forge" — DitchyDevelopments, “How To Make Your First Roblox Game in 2026 (With AI)” @ 4:33 <https://www.youtube.com/watch?v=v8vby3iOOX4&t=273s>
- **Onboarding funnel measurement & experiments** — P1, taught by 2 source(s)
  - "Uh, and I'm just going to walk you through step by step everything you need to know, and by the end of the game or end of the video, you'll have made the game that I just showed you at" — CodeBro29, “How to make your FIRST Roblox Game (Make Robux)” @ 6:33 <https://www.youtube.com/watch?v=-QSmtYVMRH4&t=393s>
- **Friction & cognitive load** — P1, taught by 2 source(s)
  - "Every little feature you add needs to feel intuitive, and there needs to be a a very clear cause and effect, okay?" — Tizzy RBLX, “My Roblox Game Makes $119,300/mo (38K CCU, here's how)” @ 14:34 <https://www.youtube.com/watch?v=LZOohZHsJus&t=874s>
- **Mobile & cross-platform input** — P1, taught by 1 source(s)
- **First session & first impression** — P1, taught by 1 source(s)
  - "So, I will explain this in the easiest way possible because this may be a little complex for you, especially if it's your first time." — MikoLikesHat, “How to ACTUALLY LEARN to Script in Roblox Studio (5 Steps to learn)” @ 3:06 <https://www.youtube.com/watch?v=GE6Z1n57yDU&t=186s>

### Retention
- **Retention KPIs & churn** — P0, taught by 4 source(s)
  - "All right? You want to have a strong curiosity hook, strong reason to come back tomorrow." — Tizzy RBLX, “My Roblox Game Makes $119,300/mo (38K CCU, here's how)” @ 16:05 <https://www.youtube.com/watch?v=LZOohZHsJus&t=965s>
  - "You need to understand marketing, game design, retention, monetization, balancing, psychology, and more. It's not a get-richqu scheme." — waveshine, “Watch this before making ROBLOX Games” @ 1:05 <https://www.youtube.com/watch?v=xnlaYLnCtFc&t=65s>
  - Numbers cited: Day one retention is how; Day seven retention is how; then come back 7 days later
- **Social play & friends** — P0, taught by 3 source(s)
  - "So, yeah, I need to be clickable, social, and replayable. That's the formula I could give you, but it's probably going to take you a few attempts anyway to get a hit game if you want to hit a game." — Starter Story, “I Spent 24 Hours With Roblox Millionaires” @ 13:18 <https://www.youtube.com/watch?v=8xgnm6SynH4&t=798s>
  - "Make sure to test it out with your friends and see if it's any fun." — janisjanis01, “How I Made a Viral Roblox Game” @ 3:24 <https://www.youtube.com/watch?v=fjlOaEALWmg&t=204s>
  - Numbers cited: to give you 5 Seconds you can go
- **Quests, tasks & achievements** — P0, taught by 3 source(s)
  - "But even then, the point is that this is too hard for the first quest in the game." — Rickmonas90, “This Roblox Developer Can't Take Criticism” @ 5:01 <https://www.youtube.com/watch?v=1VRu8LKq-Aw&t=301s>
  - "I knew that there was only one way to try and recover this challenge." — Duckable, “Can I Make a VIRAL TYCOON in 24 HOURS?” @ 13:17 <https://www.youtube.com/watch?v=F9sfnpkzcPw&t=797s>
- **Competition & leaderboards** — P1, taught by 2 source(s)
  - "Over [bell] the coming months, development will focus on story mode, new champions, additional enemies, ranked endless mode, and balancing in preparation for larger playtests." — Superstitic, “I Spent 2 Years Building the Roblox Tower Defense Game I Wanted to Play” @ 9:20 <https://www.youtube.com/watch?v=T5OH2F6_ik0&t=560s>
  - "Think of it like a ranked match just with the difference that you actually gain experience instead of just a rank." — MikoLikesHat, “How to ACTUALLY LEARN to Script in Roblox Studio (5 Steps to learn)” @ 8:18 <https://www.youtube.com/watch?v=GE6Z1n57yDU&t=498s>
- **Scarcity & FOMO** — P1, taught by 2 source(s)
  - "Make a starter pack that helps with progression. Add some limited-time items." — janisjanis01, “How I Made a Viral Roblox Game” @ 3:02 <https://www.youtube.com/watch?v=fjlOaEALWmg&t=182s>
- **Daily rewards & streaks** — P1, taught by 2 source(s)
  - "All right? You want to have a strong curiosity hook, strong reason to come back tomorrow." — Tizzy RBLX, “My Roblox Game Makes $119,300/mo (38K CCU, here's how)” @ 16:05 <https://www.youtube.com/watch?v=LZOohZHsJus&t=965s>
  - "Day one retention is how many people play the game and then come back the next day." — Laugh, “I Accidentally Made a Viral Roblox Game” @ 7:18 <https://www.youtube.com/watch?v=WFyrlstSDe4&t=438s>
  - Numbers cited: Day one retention is how

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
