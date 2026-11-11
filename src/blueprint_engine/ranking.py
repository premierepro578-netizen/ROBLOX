"""Performance scoring: which sources earned attention, and are on-topic.

For videos (components min-max normalised across the candidate set):

    performance = 0.55 * view velocity   log(views / max(age_days, 14)) - sustained demand
                + 0.25 * like rate       likes / views (capped)         - audience-rated usefulness
                + 0.20 * authority       log(channel followers)
    score       = performance * (0.25 + 0.75 * relevance)

Relevance (taxonomy hits in title/description/tags for the target pillars, scaled by a
developer-intent signal) is a multiplicative gate: a viral gameplay video that merely
matches keywords cannot outrank an on-topic design talk.
First-party docs get a fixed score; they are ground truth for APIs and policy.
"""

from __future__ import annotations

import math
import re
from datetime import date

from blueprint_engine.analysis.taxonomy import TAXONOMY, classify
from blueprint_engine.models import Source
from blueprint_engine.sources.youtube import age_days

WEIGHTS = {"velocity": 0.55, "like_rate": 0.25, "authority": 0.20}
RELEVANCE_FLOOR = 0.25
DOC_SCORE = 0.75
LIKE_RATE_CAP = 0.12


# Signals that a video teaches or analyses game making, rather than being gameplay
# entertainment that happens to match keywords ("I can't LEAVE this game!", "ranked").
_DEV_INTENT = re.compile(
    r"\b(?:how (?:to|i|we|the|roblox|games?)|tips?|tricks?|guide|tutorial|explained|explain|design(?:er|ers|ing)?|"
    r"develop(?:er|ers|ment|ing)?|devs?|devlog|studio|script(?:ing)?|mak(?:e|es|ing)|made|build(?:ing)?|"
    r"creat(?:e|ing|or|ors)|grow(?:ing|th)?|monetiz\w*|retention|retain|onboarding|ux|ui|gui|hud|algorithm|"
    r"lessons?|mistakes?|secrets?|strateg(?:y|ies)|what makes|core loops?|gameplay loops?|game loops?|"
    r"progression|econom(?:y|ies)|thumbnails?|ctr|gfx|player count|rdc|gdc|postmortem|analy[sz](?:is|ed|ing))\b",
    re.I,
)


def dev_intent(title: str, description: str) -> float:
    """1.0 if the title signals teaching/building, 0.6 if only the description does, else 0.15."""
    if _DEV_INTENT.search(title):
        return 1.0
    if _DEV_INTENT.search(description[:600]):
        return 0.6
    return 0.15


# Creator boilerplate ("turn on notifications", "use code X") matches design keywords.
_BOILERPLATE = re.compile(
    r"subscribe|notification|\bbell\b|use (?:my )?code|star ?code|become a member|patreon|discord|twitter|"
    r"instagram|tiktok\.com|merch|business (?:email|inquir)|https?://|leave a like|#\w+",
    re.I,
)


def clean_description(text: str) -> str:
    return " ".join(line for line in text.splitlines() if line.strip() and not _BOILERPLATE.search(line))


def relevance(title: str, description: str, pillars: list[str], tags: list[str] | tuple[str, ...] = ()) -> float:
    """0..1 topical relevance of title (weighted x2) + description + tags to ``pillars``.

    Tags count toward topic fit but not toward developer intent: gameplay channels tag
    videos with "how to"/"tips" phrases wholesale.
    """
    if not pillars:
        return 0.0
    desc = clean_description(description)
    text = f"{title} {title} {desc[:1500]} {' '.join(tags)}"
    scores = {c.pillar: c.score for c in classify(text[:3000], threshold=0.01)}
    best = max((scores.get(p, 0.0) for p in pillars), default=0.0)
    return round(min(best / 4.0, 1.0) * dev_intent(title, desc), 3)


def topical_relevance(title: str, text: str, min_title_score: float = 0.8) -> float:
    """0..1 best-pillar fit for developer-only venues (forums), where intent is a given.

    Long announcements mention every keyword somewhere, so the *title* must name a design
    topic (one strong or two weak taxonomy terms) before the body is considered at all.
    """
    title_scores = [c.score for c in classify(title, threshold=0.01)]
    if max(title_scores, default=0.0) < min_title_score:
        return 0.0
    scores = [c.score for c in classify(f"{title} {title} {text}"[:3000], threshold=0.01)]
    return round(min(max(scores, default=0.0) / 4.0, 1.0), 3)


def prescore(entry: dict, pillar: str) -> float:
    """Cheap score for flat search results (views + title relevance) used for shortlisting."""
    views = entry.get("view_count") or 0
    rel = relevance(entry.get("title", ""), entry.get("description", ""), [pillar])
    return math.log1p(views) / math.log1p(10_000_000) * 0.6 + rel * 0.4


def _minmax(values: list[float]) -> list[float]:
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        return [0.5 for _ in values]
    return [(v - lo) / (hi - lo) for v in values]


def score_sources(sources: list[Source], today: date | None = None) -> None:
    """Fill ``score`` and ``score_breakdown`` in place."""
    media = [s for s in sources if s.kind in ("youtube", "tiktok")]
    raw: dict[str, list[float]] = {k: [] for k in ("velocity", "like_rate", "authority")}
    for s in media:
        age = age_days(s.published, today)
        views = s.views or 0
        raw["velocity"].append(math.log1p(views / max(age if age is not None else 365, 14)))
        raw["like_rate"].append(min((s.likes or 0) / views, LIKE_RATE_CAP) if views else 0.0)
        raw["authority"].append(math.log10((s.followers or 0) + 10))
    norm = {k: _minmax(v) for k, v in raw.items()}

    for idx, s in enumerate(media):
        parts = {k: norm[k][idx] for k in norm}
        performance = sum(WEIGHTS[k] * v for k, v in parts.items())
        parts["relevance"] = relevance(s.title, s.description, s.pillars or list(TAXONOMY), s.tags)
        s.score = round(performance * (RELEVANCE_FLOOR + (1 - RELEVANCE_FLOOR) * parts["relevance"]), 4)
        s.score_breakdown = {k: round(v, 3) for k, v in parts.items()}

    forum = [s for s in sources if s.kind == "devforum"]
    likes = _minmax([math.log1p(s.likes or 0) for s in forum])
    for s, lk in zip(forum, likes):
        base = 0.3 + 0.4 * lk
        s.score = round(max(base, DOC_SCORE) if s.first_party else base, 4)
        s.score_breakdown = {"likes": round(lk, 3), "first_party": 1.0 if s.first_party else 0.0}

    for s in sources:
        if s.kind == "doc":
            s.score = DOC_SCORE
            s.score_breakdown = {"first_party": 1.0}
