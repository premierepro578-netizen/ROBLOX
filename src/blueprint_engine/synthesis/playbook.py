"""Curated Roblox implementation playbook, keyed by (pillar, mechanic).

This is *not* mined evidence: it is the engineering half of each blueprint item (how to
build it on Roblox, what to measure, what goes wrong). The report labels it as curated.
API names were checked against create.roblox.com/docs pages when this file was written;
where the docs page was not available the entry names the feature, not a method.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Play:
    build: tuple[str, ...]
    apis: tuple[str, ...] = ()
    kpis: tuple[str, ...] = ()
    pitfalls: tuple[str, ...] = ()


P = Play

PLAYBOOK: dict[tuple[str, str], Play] = {
    # ------------------------------------------------------------ core loop
    ("core_loop", "loop_structure"): P(
        build=(
            "Write the loop as a single sentence (verb -> reward -> spend -> stronger verb) and make every system feed it.",
            "Keep the minute-to-minute action responsive on its own; the reward/upgrade layer amplifies a fun verb, it cannot replace one.",
            "Make one full loop completable within the first minute, then lengthen loops gradually.",
        ),
        apis=("DataStoreService (UpdateAsync) for currency/upgrade persistence", "RemoteEvents with server-side validation"),
        kpis=("Loops completed per session", "Average session length", "D1 retention"),
        pitfalls=("Rewards that do not change how the next loop plays", "Trusting client-reported rewards (exploitable)"),
    ),
    ("core_loop", "progression"): P(
        build=(
            "Model cost and reward curves in a spreadsheet first; target a predictable time-to-next-upgrade at each stage.",
            "Show the next unlock and progress toward it permanently on the HUD.",
            "Re-tune curves from analytics (progression/economy events), not intuition.",
        ),
        apis=("AnalyticsService:LogEconomyEvent", "AnalyticsService custom events for level-ups"),
        kpis=("Median time to each milestone", "Drop-off by level", "Sink/source ratio of soft currency"),
        pitfalls=("Exponential costs with linear rewards (a hidden wall)", "No visible next goal"),
    ),
    ("core_loop", "prestige"): P(
        build=(
            "Offer rebirth when progress slows, trading a reset for a permanent multiplier the player can see.",
            "Make the post-rebirth replay faster so the first rebirth feels like acceleration, not punishment.",
        ),
        apis=("DataStoreService (session-locked profile, e.g. ProfileStore pattern)",),
        kpis=("% of players reaching first rebirth", "Retention of rebirthed vs non-rebirthed cohorts"),
        pitfalls=("Rebirth before the loop is understood", "Multipliers that break economy balance"),
    ),
    ("core_loop", "goals"): P(
        build=(
            "Layer goals: seconds (next hit), minutes (next upgrade), session (next zone), week (collection/season).",
            "Always surface one short-term and one long-term goal on screen.",
        ),
        kpis=("Goal completion rate per layer", "Session length"),
        pitfalls=("Only long-term goals (players cannot see progress)", "Too many simultaneous goals"),
    ),
    ("core_loop", "game_feel"): P(
        build=(
            "Give every core action immediate feedback: sound, particle burst, number pop, small camera response.",
            "Animate rewards flying into the counter so the player sees cause and effect.",
            "Budget effects for low-end mobile; profile with the MicroProfiler.",
        ),
        apis=("TweenService", "ParticleEmitter", "SoundService / Sound", "BillboardGui for damage/coin pops"),
        kpis=("Actions per minute", "Early session drop-off"),
        pitfalls=("Effects that tank mobile frame rate", "Feedback spam that hides important information"),
    ),
    ("core_loop", "depth"): P(
        build=(
            "Add a decision to the loop (route, loadout, risk vs reward) so mastery has room to grow.",
            "Introduce new modifiers on the existing verb before adding new verbs.",
        ),
        kpis=("Playtime of veteran cohort", "D7/D30 retention"),
        pitfalls=("Variety via unrelated mini-games that dilute the core loop",),
    ),
    ("core_loop", "collection"): P(
        build=(
            "Give collections a visible index with silhouettes for missing items and a reward for completing sets.",
            "Tie collectibles back into the loop (stat boosts, cosmetics shown to others).",
        ),
        apis=("DataStoreService", "ViewportFrame for item previews"),
        kpis=("Index completion distribution", "Return visits driven by collection goals"),
        pitfalls=("Collections purchasable only through paid random items",),
    ),
    ("core_loop", "concept"): P(
        build=(
            "Validate the hook before building systems: can the idea be understood from the icon and title in 2 seconds?",
            "Study the top games in the genre; ship the genre's expected loop, then differentiate on one axis.",
        ),
        kpis=("Thumbnail click-through rate", "First-play bounce rate"),
        pitfalls=("Novelty with no repeatable loop", "Copying a trend after it has peaked"),
    ),
    # ------------------------------------------------------------ retention
    ("retention", "daily_rewards"): P(
        build=(
            "Track lastClaimDay and streak server-side in UTC days (os.time() // 86400); never trust client time.",
            "Escalate rewards across a 7-day cycle with a highlight on day 7; show tomorrow's reward to create intent.",
            "Use a forgiving streak (grace day or partial reset) so one missed day does not erase the habit.",
        ),
        apis=("DataStoreService:UpdateAsync (atomic claim)", "ExperienceNotificationService:PromptOptIn for 'reward ready' reminders"),
        kpis=("D1 / D7 retention", "Daily claim rate", "Streak length distribution"),
        pitfalls=("Double claims from a race between servers (use UpdateAsync)", "Rewards so large they distort the economy"),
    ),
    ("retention", "quests"): P(
        build=(
            "Rotate daily and weekly quests that point at the core loop and at under-used features.",
            "Use badges for one-time milestones that are visible on the profile.",
        ),
        apis=("BadgeService", "DataStoreService for quest state", "AnalyticsService:LogFunnelStepEvent for quest chains"),
        kpis=("Quest completion rate", "Feature adoption after quest exposure"),
        pitfalls=("Chores that pull players away from fun", "Quests that require purchases"),
    ),
    ("retention", "live_ops"): P(
        build=(
            "Publish a predictable update cadence and announce it in-game (update log board) and on the game page.",
            "Run time-boxed events with server-authoritative start/end times; schedule them as Experience Events.",
            "Measure each update's effect on returning-player counts, not only on new users.",
        ),
        apis=("Experience Events (Creator Hub)", "MessagingService for cross-server event starts", "MemoryStoreService for event state"),
        kpis=("Returning users on update day", "Event participation rate", "D7 retention of event cohort"),
        pitfalls=("Content droughts after launch", "Events that shut out new players"),
    ),
    ("retention", "social"): P(
        build=(
            "Reward playing with friends (shared bonuses, co-op objectives) and make inviting one tap.",
            "Give players something to show off to others in the same server.",
        ),
        apis=("SocialService:PromptGameInvite", "Players:GetFriendsAsync", "TextChatService"),
        kpis=("% sessions with a friend", "Invites sent per DAU", "Retention of social vs solo players"),
        pitfalls=("Invite spam prompts", "Trading without scam protection"),
    ),
    ("retention", "competition"): P(
        build=(
            "Combine an all-time leaderboard with seasonal or daily boards so new players can place.",
            "Show rank deltas and the next rival above the player.",
        ),
        apis=("OrderedDataStore (all-time)", "MemoryStoreService sorted maps (fast/seasonal boards)"),
        kpis=("Leaderboard view rate", "Session length of competitive players"),
        pitfalls=("Boards dominated by whales or exploiters", "No reachable tier for newcomers"),
    ),
    ("retention", "notifications"): P(
        build=(
            "Ask for notification opt-in right after a positive moment, never on first join.",
            "Send notifications only for things the player asked for (reward ready, event starting).",
        ),
        apis=("ExperienceNotificationService:CanPromptOptInAsync / PromptOptIn", "Open Cloud user notifications API"),
        kpis=("Opt-in rate", "Notification-attributed sessions"),
        pitfalls=("Prompting before the player is invested", "Clickbait notification copy"),
    ),
    ("retention", "scarcity"): P(
        build=(
            "Use limited-time content to create reasons to return, with clear end dates and earnable paths.",
            "Rotate items back later so scarcity drives timing, not exclusion.",
        ),
        kpis=("Return rate during limited windows",),
        pitfalls=("Fake or misleading countdowns", "Pressure tactics aimed at young players"),
    ),
    ("retention", "idle"): P(
        build=(
            "Credit offline earnings on rejoin (capped), calculated server-side from saved timestamps.",
            "Show an 'while you were away' summary that sends the player straight into spending it.",
        ),
        apis=("DataStoreService (last-seen timestamp)",),
        kpis=("Return frequency", "Session starts per DAU"),
        pitfalls=("Uncapped offline income breaking the economy",),
    ),
    ("retention", "reward_schedules"): P(
        build=(
            "Mix predictable rewards (progress) with occasional bonus rewards for performance or exploration.",
            "Keep any random reward earnable through play and its odds visible.",
        ),
        apis=("PolicyService:GetPolicyInfoForPlayerAsync (paid random item restrictions)",),
        kpis=("Session length", "Reward-claim rate"),
        pitfalls=("Slot-machine style loops monetised with paid randomness",),
    ),
    ("retention", "retention_kpis"): P(
        build=(
            "Track D1/D7/D30 by new-user cohort in the Retention dashboard; annotate every update date.",
            "Pair retention with playtime and funnel data to locate where players quit.",
        ),
        apis=("Creator Hub Analytics: Retention, Engagement", "AnalyticsService custom events"),
        kpis=("D1, D7, D30 retention", "Average playtime per DAU", "First-play bounce rate"),
        pitfalls=("Reading aggregate retention without cohorts", "Changing several systems at once (no attribution)"),
    ),
    # ----------------------------------------------------------- onboarding
    ("onboarding", "first_session"): P(
        build=(
            "Spawn new players directly into the core action; defer menus, lore and settings.",
            "Script the first 60 seconds: first action, first reward, first upgrade.",
            "Detect first-time players server-side and give them the guided path; skip it for returners.",
        ),
        apis=("AnalyticsService:LogOnboardingFunnelStepEvent", "DataStoreService (hasCompletedTutorial flag)"),
        kpis=("Onboarding funnel step completion", "First-play bounce rate", "D1 retention"),
        pitfalls=("Loading screens and text walls before play", "Same tutorial for returning players"),
    ),
    ("onboarding", "guidance"): P(
        build=(
            "Teach by doing: one instruction at a time, triggered by context, dismissed by completing it.",
            "Use world-space guidance (Beam arrow to the next objective, highlighted target) over modal text.",
            "A/B test guidance variants (e.g. dialogue vs arrow) with Experiments.",
        ),
        apis=("Beam + Attachment", "Highlight", "ProximityPrompt", "Experiments (Creator Hub)"),
        kpis=("Per-step completion and time-to-complete", "Tutorial skip rate"),
        pitfalls=("Unskippable long tutorials", "Teaching every system before the fun"),
    ),
    ("onboarding", "quick_win"): P(
        build=(
            "Grant a meaningful reward within the first minute and let the player spend it immediately.",
            "Make the first upgrade visibly change the core action.",
        ),
        kpis=("Time to first reward", "Time to first upgrade", "First-session length"),
        pitfalls=("Rewards the player cannot use yet",),
    ),
    ("onboarding", "ui_clarity"): P(
        build=(
            "Establish a visual hierarchy: one primary action per screen, secondary buttons visibly smaller.",
            "Size with Scale and constraints so layouts hold on phones, tablets, PC and console.",
            "Keep the HUD minimal during onboarding and reveal panels as they become relevant.",
        ),
        apis=("UDim2.fromScale", "UIAspectRatioConstraint", "UIScale", "ScreenGui.ScreenInsets (safe areas)"),
        kpis=("Misclick / back-out rate on menus", "Purchase prompt reach"),
        pitfalls=("Pixel-sized UI that breaks on mobile", "Shop buttons covering the play area"),
    ),
    ("onboarding", "platforms"): P(
        build=(
            "Design for touch first: thumb-reachable buttons, no hover-only interactions.",
            "Bind actions once for all inputs and test on a real phone and gamepad.",
        ),
        apis=("ContextActionService", "UserInputService.TouchEnabled / GamepadEnabled"),
        kpis=("Retention and playtime split by device",),
        pitfalls=("PC-only keybind hints", "Tiny touch targets"),
    ),
    ("onboarding", "friction"): P(
        build=(
            "Cut every step between join and fun that does not teach or reward; count clicks to first action.",
            "Introduce one concept at a time and confirm understanding through action.",
        ),
        kpis=("Funnel drop-off per step",),
        pitfalls=("Multiple currencies explained at once", "Popups stacking on join"),
    ),
    ("onboarding", "funnel"): P(
        build=(
            "Instrument every onboarding step with LogOnboardingFunnelStepEvent (ordered, one-time per player).",
            "Use LogFunnelStepEvent for recurring funnels (shop flow, quest chains).",
            "Fix the largest drop-off first, then re-measure.",
        ),
        apis=("AnalyticsService:LogOnboardingFunnelStepEvent", "AnalyticsService:LogFunnelStepEvent", "Experiments"),
        kpis=("Step-to-step conversion", "Overall onboarding completion"),
        pitfalls=("Too many steps to read the funnel", "Logging steps from the client"),
    ),
    # --------------------------------------------------------- monetization
    ("monetization", "passes"): P(
        build=(
            "Sell permanent quality-of-life or prestige perks (VIP area, 2x currency, extra slots) as passes.",
            "Check ownership on join with UserOwnsGamePassAsync and on PromptGamePassPurchaseFinished.",
            "Show what the pass does in-game at the moment it would help.",
        ),
        apis=("MarketplaceService:PromptGamePassPurchase", "MarketplaceService:UserOwnsGamePassAsync", "MarketplaceService.PromptGamePassPurchaseFinished"),
        kpis=("Pass conversion rate", "Revenue per pass", "Retention of buyers vs non-buyers"),
        pitfalls=("Pay-to-win power in competitive modes", "Not granting a pass bought outside the game"),
    ),
    ("monetization", "dev_products"): P(
        build=(
            "Sell consumables (boosts, currency packs, revives) as developer products.",
            "Grant inside MarketplaceService.ProcessReceipt and return PurchaseGranted only after the grant is saved; dedupe by PurchaseId.",
            "Offer products in context (revive on death, boost before a hard section).",
        ),
        apis=("MarketplaceService:PromptProductPurchase", "MarketplaceService.ProcessReceipt", "AnalyticsService:LogEconomyEvent"),
        kpis=("Payer conversion", "ARPPU", "Repeat purchase rate"),
        pitfalls=("Granting before persisting (lost purchases)", "Non-idempotent receipt handling (double grants)"),
    ),
    ("monetization", "random_items"): P(
        build=(
            "If you sell random items, disclose odds before purchase and keep items earnable through play.",
            "Check PolicyService for each player and offer a direct-purchase path where paid random items are restricted.",
        ),
        apis=("PolicyService:GetPolicyInfoForPlayerAsync (ArePaidRandomItemsRestricted)",),
        kpis=("Conversion vs refund/complaint signals", "Retention of payers"),
        pitfalls=("Undisclosed odds (policy violation)", "Ignoring regional restrictions"),
    ),
    ("monetization", "subscriptions"): P(
        build=(
            "Use subscriptions for recurring value (monthly currency stipend, daily perks), not one-time items.",
            "Check status server-side with GetUserSubscriptionStatusAsync and react to UserSubscriptionStatusChanged.",
        ),
        apis=("MarketplaceService:GetUserSubscriptionStatusAsync", "Players.UserSubscriptionStatusChanged", "MarketplaceService:GetSubscriptionProductInfoAsync"),
        kpis=("Subscriber count", "Churn / renewal rate"),
        pitfalls=("Subscription value that does not renew (players cancel after month one)",),
    ),
    ("monetization", "premium_payouts"): P(
        build=(
            "Engagement-based payouts were deprecated on 2025-07-24 and replaced by the Creator Rewards program - re-check any advice built on them.",
            "Premium benefits (Players.PlayerMembershipChanged, MarketplaceService:PromptPremiumPurchase) can still reward Premium members in-game.",
        ),
        apis=("MarketplaceService:PromptPremiumPurchase", "Player.MembershipType"),
        kpis=("Creator Rewards earnings (Creator Hub)",),
        pitfalls=("Optimising for a payout program that no longer exists",),
    ),
    ("monetization", "pricing"): P(
        build=(
            "Build a price ladder: a low-friction starter offer, core items, and premium bundles that anchor value.",
            "Use Price Optimization and Regional Pricing instead of guessing; re-test after major updates.",
        ),
        apis=("Price Optimization (Creator Hub)", "Regional pricing", "MarketplaceService:GetProductInfo"),
        kpis=("Conversion by price point", "Revenue per DAU"),
        pitfalls=("Only high price points (no first purchase)", "Constant discounts training players to wait"),
    ),
    ("monetization", "ads"): P(
        build=(
            "Treat rewarded ads as opt-in value exchanges placed at natural pauses.",
            "Use Ads Manager campaigns to buy acquisition only after onboarding converts well.",
        ),
        apis=("Ads Manager (Creator Hub)", "Immersive ads"),
        kpis=("Cost per acquired player vs their D7 value",),
        pitfalls=("Paying to acquire players into a leaky funnel",),
    ),
    ("monetization", "private_servers"): P(
        build=("Enable paid private servers for games where friends want an uncrowded space (roleplay, grinding, events).",),
        apis=("Private servers (game settings)", "TeleportService:ReserveServer for custom flows"),
        kpis=("Private server subscriptions", "Social session share"),
        pitfalls=("Private servers that remove the social reason to play",),
    ),
    ("monetization", "conversion"): P(
        build=(
            "Log every purchase and currency flow with LogEconomyEvent to see sources, sinks and paths to purchase.",
            "Increase conversion by placing offers where players feel the need, not by adding more offers.",
        ),
        apis=("AnalyticsService:LogEconomyEvent", "Creator Hub Analytics: Monetization"),
        kpis=("Payer conversion", "ARPDAU", "ARPPU"),
        pitfalls=("Optimising revenue while D7 retention falls",),
    ),
    ("monetization", "fairness"): P(
        build=(
            "Sell time savings, convenience and cosmetics; keep competitive outcomes skill-based.",
            "Make every paid advantage reachable through play, slower.",
        ),
        kpis=("Retention of non-payers", "Review / like ratio"),
        pitfalls=("Pay-to-win perception driving away the non-paying majority",),
    ),
    # ------------------------------------------------------------ discovery
    ("discovery", "thumbnails"): P(
        build=(
            "Use a custom thumbnail (required for Home recommendations) that shows the core action clearly at small sizes.",
            "Test icons/thumbnails against click-through and play-through; keep them accurate to the game.",
        ),
        apis=("Thumbnail personalization (Creator Hub)",),
        kpis=("Impressions -> click-through rate", "Play-through rate"),
        pitfalls=("Misleading thumbnails (hurt play-through and trust)",),
    ),
    ("discovery", "algorithm"): P(
        build=(
            "Optimise the signals the recommender reads: play-through, playtime, retention, co-play and monetisation.",
            "Fix first-play bounce before buying traffic; recommendations expand to cohorts that engage.",
        ),
        apis=("Creator Hub Analytics: Acquisition",),
        kpis=("Home impressions", "Play-through rate", "D1/D7 retention"),
        pitfalls=("Chasing impressions with a game that does not retain",),
    ),
    ("discovery", "external"): P(
        build=(
            "Seed short-form clips of the most shareable moment; give creators reasons to record (events, codes, secrets).",
        ),
        kpis=("Traffic by source (Acquisition dashboard)",),
        pitfalls=("Spikes from content that the game cannot retain",),
    ),
    ("discovery", "paid_acquisition"): P(
        build=("Buy ads/sponsorships to test the funnel at scale once D1 retention is healthy.",),
        apis=("Ads Manager (Creator Hub)",),
        kpis=("Cost per play", "Paid-cohort D7 retention"),
        pitfalls=("Scaling spend before onboarding works",),
    ),
}


def play_for(pillar: str, mechanic: str) -> Play | None:
    return PLAYBOOK.get((pillar, mechanic))


@dataclass(frozen=True)
class StaleRule:
    """Advice that conflicts with a documented platform change."""

    key: str
    pattern: str
    notice: str
    doc_source_id: str
    _re: re.Pattern[str] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_re", re.compile(self.pattern, re.I))

    def matches(self, text: str) -> bool:
        return bool(self._re.search(text))


STALE_RULES: tuple[StaleRule, ...] = (
    StaleRule(
        key="engagement_payouts_deprecated",
        pattern=r"premium payouts?|engagement[- ]based payouts?|premium (?:players?|members?) (?:pay|earn)",
        notice="Engagement-Based Payouts were deprecated effective 2025-07-24 and replaced by Creator Rewards.",
        doc_source_id="doc:production/monetization/engagement-based-payouts",
    ),
)
