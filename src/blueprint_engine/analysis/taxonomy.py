"""Game-design taxonomy: pillars -> mechanics -> lexical patterns.

``strong`` patterns are specific to the mechanic; ``weak`` ones only count as
supporting evidence (they are common in unrelated speech, e.g. "update", "steps").
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import cached_property

STRONG = 1.0
WEAK = 0.4


@dataclass(frozen=True)
class Mechanic:
    key: str
    label: str
    strong: tuple[str, ...] = ()
    weak: tuple[str, ...] = ()

    @cached_property
    def _strong_re(self) -> list[re.Pattern[str]]:
        return [re.compile(rf"\b(?:{p})\b", re.I) for p in self.strong]

    @cached_property
    def _weak_re(self) -> list[re.Pattern[str]]:
        return [re.compile(rf"\b(?:{p})\b", re.I) for p in self.weak]

    def score(self, text: str) -> float:
        s = sum(min(len(r.findall(text)), 2) * STRONG for r in self._strong_re)
        s += sum(min(len(r.findall(text)), 2) * WEAK for r in self._weak_re)
        return s


@dataclass(frozen=True)
class Pillar:
    key: str
    label: str
    mechanics: tuple[Mechanic, ...] = field(default_factory=tuple)

    def mechanic(self, key: str) -> Mechanic:
        return next(m for m in self.mechanics if m.key == key)


M = Mechanic

TAXONOMY: dict[str, Pillar] = {
    "core_loop": Pillar("core_loop", "Core gameplay loop", (
        M("loop_structure", "Action -> reward -> upgrade cycle",
          strong=(r"core (?:game(?:play)? )?loops?", r"gameplay loops?", r"game loops?", r"compulsion loops?",
                  r"(?:action|actions)\W+(?:\w+\W+){0,4}rewards?", r"rewards?\W+(?:\w+\W+){0,4}upgrades?"),
          weak=(r"loops?", r"cycles?", r"repeat(?:ed|ing)?", r"rewards?", r"minute[- ]to[- ]minute")),
        M("progression", "Progression & pacing",
          strong=(r"progression", r"level(?:s|ing)? up", r"xp", r"experience points", r"power curve",
                  r"difficulty curve", r"pacing", r"unlock(?:s|ed|ing)? (?:new|more|the next)"),
          weak=(r"progress", r"unlock(?:s|ed|ing)?", r"upgrades?", r"tiers?", r"stronger", r"levels?")),
        M("prestige", "Rebirth / prestige resets",
          strong=(r"rebirths?", r"rebirthing", r"prestige", r"reset (?:your|their|the) progress", r"ascen(?:d|sion)")),
        M("goals", "Short- and long-term goals",
          strong=(r"short[- ]term goals?", r"long[- ]term goals?", r"milestones?", r"something to work towards?",
                  r"(?:clear|next) goals?"),
          weak=(r"goals?", r"objectives?", r"work towards?")),
        M("game_feel", "Game feel & feedback (juice)",
          strong=(r"juic(?:e|y|iness)", r"game ?feel", r"screen ?shake", r"camera ?shake", r"particles?",
                  r"sound effects?", r"sfx", r"satisfying"),
          weak=(r"feedback", r"tween(?:s|ing)?", r"animations?", r"polish(?:ed)?", r"effects?")),
        M("depth", "Variety, skill & mastery",
          strong=(r"mastery", r"skill ceiling", r"skill[- ]based", r"meaningful (?:choices?|decisions?)",
                  r"repetitive", r"monoton(?:y|ous)"),
          weak=(r"variety", r"skills?", r"depth", r"strateg(?:y|ic)", r"decisions?", r"boring")),
        M("collection", "Collection & inventory",
          strong=(r"collect(?:ion|ing|ibles?)", r"pets?", r"inventory", r"index", r"rarit(?:y|ies)"),
          weak=(r"collect", r"skins?", r"cards?")),
        M("concept", "Concept & hook",
          strong=(r"game ideas?", r"(?:the|your|a) concept", r"unique (?:idea|twist|mechanic)", r"genre",
                  r"simulators?", r"tycoons?", r"obb(?:y|ies)", r"tower defen[cs]e", r"battlegrounds?"),
          weak=(r"ideas?", r"trend(?:s|ing)?", r"hook", r"unique", r"original")),
    )),
    "retention": Pillar("retention", "Retention mechanics", (
        M("daily_rewards", "Daily rewards & streaks",
          strong=(r"daily (?:rewards?|logins?|bonus(?:es)?|spins?|quests?|challenges?|chests?)", r"login (?:rewards?|streaks?|bonus)",
                  r"streaks?", r"come back (?:tomorrow|every day|daily|the next day)"),
          weak=(r"daily", r"every day")),
        M("quests", "Quests, tasks & achievements",
          strong=(r"quests?", r"missions?", r"achievements?", r"badges?", r"challenges?"),
          weak=(r"tasks?", r"objectives?")),
        M("live_ops", "Updates, events & live ops",
          strong=(r"live ?ops", r"limited[- ]time (?:events?|items?|offers?|modes?)", r"seasonal", r"seasons?",
                  r"update (?:schedule|cadence|logs?)", r"weekly updates?", r"new content", r"admin abuse",
                  r"(?:in-?game|live|special|holiday) events?"),
          weak=(r"updates?", r"updating", r"weekly", r"events?")),
        M("social", "Social play & friends",
          strong=(r"friends?", r"social", r"trad(?:e|es|ing)", r"clans?", r"guilds?", r"parties", r"party",
                  r"invit(?:e|es|ing)", r"multiplayer", r"play(?:ing)? together", r"co-?op"),
          weak=(r"community", r"groups?", r"teams?")),
        M("competition", "Competition & leaderboards",
          strong=(r"leaderboards?", r"compet(?:e|itive|ition)", r"top players?", r"pvp", r"tournaments?", r"ranked"),
          weak=(r"rank(?:s|ing)?",)),
        M("notifications", "Notifications & re-engagement",
          strong=(r"notifications?", r"remind(?:er|ers)", r"re-?engag(?:e|ement)"),
          weak=(r"notify", r"push")),
        M("scarcity", "Scarcity & FOMO",
          strong=(r"fomo", r"fear of missing out", r"exclusive", r"scarc(?:e|ity)", r"only available", r"limited"),
          weak=(r"rare",)),
        M("idle", "Idle / offline progress",
          strong=(r"offline (?:progress|earnings|rewards|income)", r"afk", r"idle")),
        M("reward_schedules", "Reward schedules & anticipation",
          strong=(r"variable rewards?", r"random rewards?", r"dopamine", r"anticipation", r"surprise"),
          weak=(r"rewarding",)),
        M("retention_kpis", "Retention KPIs & churn",
          strong=(r"retention", r"d1", r"d7", r"d30", r"day (?:one|1|seven|7|thirty|30)", r"churn",
                  r"playtime", r"session (?:length|time)s?", r"average session", r"returning players?",
                  r"come back", r"coming back"),
          weak=(r"return(?:ing)?", r"quit(?:ting)?", r"leave the game", r"stick around")),
    )),
    "onboarding": Pillar("onboarding", "Onboarding & first-time UX", (
        M("first_session", "First session & first impression",
          strong=(r"first (?:few )?(?:seconds|minutes?|session|impressions?|time user|time experience)",
                  r"new players?", r"when (?:a )?players? (?:first )?(?:join|spawn)s?", r"ftue", r"first[- ]time",
                  r"first (?:30|60|thirty|sixty)"),
          weak=(r"spawn(?:s|ing)?", r"join(?:s|ing)? the game")),
        M("guidance", "Tutorials & guidance",
          strong=(r"tutorials?", r"guid(?:e|ed|ance|ing) (?:the )?(?:player|players|them|new)", r"arrows?", r"beams?",
                  r"waypoints?", r"tool ?tips?", r"hand[- ]?hold(?:ing)?",
                  r"walk(?:s)? (?:them|you|players|the player) through", r"show (?:the )?(?:player|players|them) (?:where|how|what)"),
          weak=(r"hints?", r"guide", r"teach(?:es|ing)?", r"explain")),
        M("quick_win", "Early wins & instant gratification",
          strong=(r"quick wins?", r"early (?:wins?|rewards?|success)", r"instant gratification",
                  r"within (?:the first|seconds|a minute)", r"hook (?:them|players|the player)"),
          weak=(r"instant(?:ly)?", r"right away", r"immediately", r"quickly")),
        M("ui_clarity", "UI clarity & readability",
          strong=(r"ui", r"ux", r"user interface", r"hud", r"clutter(?:ed)?", r"readab(?:le|ility)", r"visual hierarchy"),
          weak=(r"buttons?", r"menus?", r"icons?", r"fonts?", r"layout", r"screens?")),
        M("platforms", "Mobile & cross-platform input",
          strong=(r"mobile", r"phones?", r"tablets?", r"touch ?screens?", r"controllers?", r"consoles?", r"cross[- ]platform"),
          weak=(r"touch", r"small screens?")),
        M("friction", "Friction & cognitive load",
          strong=(r"confus(?:e|ed|ing|ion)", r"overwhelm(?:ed|ing)?", r"friction", r"cognitive load", r"intuitive"),
          weak=(r"too (?:many|much)", r"simpl(?:e|ify|icity)", r"understand")),
        M("funnel", "Onboarding funnel measurement",
          strong=(r"funnels?", r"drop[- ]?offs?", r"onboarding", r"completion rates?"),
          weak=(r"steps?", r"conversion")),
    )),
    "monetization": Pillar("monetization", "Monetization", (
        M("passes", "Passes (permanent perks)",
          strong=(r"game ?pass(?:es)?", r"gamepass(?:es)?", r"vip", r"2x", r"double (?:coins|cash|money|xp|speed|luck)",
                  r"permanent (?:perks?|upgrades?|boosts?)"),
          weak=(r"pass(?:es)?", r"perks?")),
        M("dev_products", "Developer products (consumables)",
          strong=(r"developer products?", r"dev products?", r"consumables?", r"(?:gem|coin|cash|currency) packs?",
                  r"boosts?", r"potions?", r"revives?", r"skips?"),
          weak=(r"currency",)),
        M("random_items", "Paid random items (eggs, crates)",
          strong=(r"eggs?", r"crates?", r"loot ?box(?:es)?", r"gacha", r"odds", r"random items?", r"paid random"),
          weak=(r"spins?", r"rolls?", r"cases?")),
        M("subscriptions", "Subscriptions",
          strong=(r"subscriptions?", r"recurring (?:revenue|benefits?|payments?)"),
          weak=(r"monthly",)),
        M("premium_payouts", "Engagement-based (Premium) payouts",
          strong=(r"premium (?:payouts?|players?|members?|subscribers?|benefits?|users?)", r"engagement[- ]based"),
          weak=(r"premium",)),
        M("pricing", "Pricing, bundles & offers",
          strong=(r"pric(?:e|es|ing)", r"price points?", r"starter (?:packs?|bundles?)", r"bundles?", r"discounts?",
                  r"regional pricing", r"price optimization", r"anchor(?:ing)?"),
          weak=(r"robux", r"cheap(?:er)?", r"expensive", r"deals?", r"sales?", r"offers?")),
        M("ads", "Ads (rewarded, immersive, sponsored)",
          strong=(r"rewarded (?:video )?ads?", r"immersive ads?", r"ads? manager", r"sponsor(?:ed|ships?)?",
                  r"ad credits?", r"advertis(?:e|ing|ements?)"),
          weak=(r"ads?",)),
        M("private_servers", "Private servers",
          strong=(r"private servers?", r"vip servers?")),
        M("conversion", "Conversion & revenue KPIs",
          strong=(r"conversion rates?", r"payers?", r"paying (?:players|users|customers)", r"arppu", r"arpdau",
                  r"revenue", r"whales?", r"monetiz(?:e|ation|ing)", r"spenders?"),
          weak=(r"spend(?:ing)?", r"buy(?:s|ing)?", r"purchases?", r"sell(?:s|ing)?")),
        M("fairness", "Fairness & player trust",
          strong=(r"pay[- ]to[- ]win", r"p2w", r"predatory", r"cash grab", r"greedy", r"scams?", r"fair(?:ness)?"),
          weak=(r"trust", r"kids?", r"children")),
    )),
    "discovery": Pillar("discovery", "Discovery & growth", (
        M("thumbnails", "Thumbnails, icons & titles",
          strong=(r"thumbnails?", r"game icons?", r"click[- ]?through(?: rates?)?", r"ctr", r"impressions?"),
          weak=(r"icons?", r"titles?")),
        M("algorithm", "Recommendation algorithm",
          strong=(r"algorithm", r"recommend(?:ed|ations?)", r"home ?page", r"discovery", r"front page",
                  r"qualified play", r"charts?", r"sorts?"),
          weak=(r"discover(?:ed)?",)),
        M("external", "External content & creators",
          strong=(r"tiktoks?", r"youtubers?", r"influencers?", r"content creators?", r"viral", r"trailers?", r"shorts"),
          weak=(r"marketing", r"promot(?:e|ion|ing)", r"videos?")),
        M("paid_acquisition", "Paid acquisition",
          strong=(r"sponsor(?:ed|ships?)?", r"ad credits?", r"ads manager", r"cpm", r"cost per"),
          weak=(r"ads?", r"advertis(?:e|ing)")),
    )),
}


@dataclass
class Classification:
    pillar: str
    score: float
    mechanics: list[tuple[str, float]]  # sorted desc


def classify(text: str, *, hint_pillars: list[str] | tuple[str, ...] = (), threshold: float = 1.0,
             hint_bonus: float = 0.3, pillars: dict[str, Pillar] | None = None) -> list[Classification]:
    """Score ``text`` against every pillar; return qualifying pillars (best first)."""
    pillars = pillars or TAXONOMY
    out: list[Classification] = []
    for key, pillar in pillars.items():
        mech = [(m.key, m.score(text)) for m in pillar.mechanics]
        mech = sorted(((k, s) for k, s in mech if s > 0), key=lambda x: -x[1])
        total = sum(s for _, s in mech)
        if total <= 0:
            continue
        if key in hint_pillars:
            total += hint_bonus
        if total >= threshold:
            # Keep mechanics with real support; always keep the single best one.
            strong = [(k, s) for k, s in mech if s >= 0.8] or mech[:1]
            out.append(Classification(key, round(total, 2), strong))
    return sorted(out, key=lambda c: -c.score)


def mechanic_label(pillar: str, mechanic: str) -> str:
    try:
        return TAXONOMY[pillar].mechanic(mechanic).label
    except (KeyError, StopIteration):
        return mechanic.replace("_", " ")
