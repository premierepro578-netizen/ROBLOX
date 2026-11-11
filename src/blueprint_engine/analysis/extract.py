"""Heuristic (offline, deterministic) extraction of actionable insights.

A sentence becomes an insight when it (a) maps to a design pillar via the taxonomy and
(b) reads like advice: directives ("you need to", "make sure"), imperatives ("add a
daily reward"), causal reasoning ("because", "which means") or concrete numbers.
Adjacent qualifying sentences are merged into one evidence passage.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from blueprint_engine.analysis.segment import clean_text
from blueprint_engine.analysis.taxonomy import TAXONOMY, Pillar, classify
from blueprint_engine.models import Document, Insight, Segment

_DIRECTIVE_STRONG = [re.compile(p, re.I) for p in (
    r"\byou(?:'ll| will)? (?:need|want|have|should|must|gotta|got to|wanna|shouldn'?t|can'?t afford)\b",
    r"\bmake sure\b", r"\btry (?:to|and)\b", r"\bfocus on\b", r"\bstart (?:with|by)\b",
    r"\bthe (?:key|secret|trick|goal|point|biggest mistake|most important thing) (?:is|here|to)\b",
    r"\bwhat you (?:want|need|should)\b", r"\b(?:best|easiest|simplest|fastest) way\b",
    r"\bi (?:highly )?(?:recommend|suggest|advise)\b", r"\bit'?s (?:better|best|a good idea|important|crucial) to\b",
    r"\bbest practices?\b", r"\b(?:should|must) (?:be|have|always|never|not)\b", r"\bneeds? to be\b",
    r"\binstead of\b", r"\bgive (?:players|the player|them|people|your players|users)\b",
    r"\blet (?:players|them|the player|users)\b", r"\bdon'?t (?:make|let|put|add|give|forget|overwhelm|force)\b",
    r"\bavoid\b", r"\bconsider\b", r"\bremember to\b", r"\bmistake\b",
)]
_DIRECTIVE_WEAK = [re.compile(p, re.I) for p in (
    r"\bshould\b", r"\bmust\b", r"\bnever\b", r"\balways\b", r"\bimportant\b", r"\bcrucial\b", r"\bessential\b",
    r"\byou can\b", r"\bhelps?\b", r"\bkeeps? (?:players|them|people|users)\b", r"\bencourag(?:e|es|ing)\b",
)]
_IMPERATIVE = re.compile(
    r"^(?:so,? |and |now,? |then,? |also,? |just |first,? |next,? |finally,? )?"
    r"(?:add|make|give|use|put|create|design|let|keep|show|reward|build|test|track|measure|offer|limit|set|place|"
    r"introduce|teach|avoid|remove|reduce|increase|focus|think about|consider|start|study|look at|check|release|"
    r"price|sell|include|display|highlight|guide|encourage|allow|prompt|grant|award|unlock|space out|playtest)\b",
    re.I,
)
_CAUSAL = re.compile(
    r"\b(?:because|so that|which means|that'?s why|this (?:makes|keeps|gets|causes|means|will)|in order to|"
    r"the reason|leads? to|results? in|that way)\b",
    re.I,
)
_METRIC = re.compile(
    r"(?:\b\d+(?:[.,]\d+)?\s?(?:%|percent\b|x\b|seconds?\b|secs?\b|minutes?\b|mins?\b|hours?\b|days?\b|robux\b|ccu\b|"
    r"visits\b|players\b|k\b|million\b|thousand\b))|\bd(?:1|7|30)\b|\bday (?:one|1|seven|7|thirty|30)\b|"
    r"\b(?:retention|conversion rate|ctr|arppu|arpdau|playtime|session length|concurrent)\b",
    re.I,
)
_NOISE = re.compile(
    r"\b(?:subscribe|like (?:and|the|this) (?:video|subscribe)|comment (?:below|down)|patreon|my discord|"
    r"join (?:the|my|our) discord|links? (?:is |are )?in (?:the |my )?description|sponsor(?:ed)? by|"
    r"this video is sponsored|smash (?:that|the)|notification bell|merch|use (?:my )?code|"
    r"(?:in|on) (?:this|today'?s|the next|my last) video|thanks for watching|see you (?:in the next|next time)|"
    r"creator code|star ?code|discount code|promo code|my (?:course|academy|program|coaching|mentorship)|"
    r"developer academy|check out my|link (?:down )?below|comment section|let me know in the comments|contact me|"
    r"my apologies|free (?:ui )?packs? (?:that )?i make|join (?:my|our) group)\b",
    re.I,
)
# Click-path instructions ("go to the Experiences tab and click Create") are procedure, not design.
_PROCEDURE = re.compile(
    r"\b(?:click(?:ing)? (?:on|the)|(?:the|this) \w+ tab|go to (?:the )?(?:creator (?:hub|dashboard)|settings|home|"
    r"explorer|properties|toolbox)|navigate to|scroll down|right[- ]click|drag (?:it|this|that)|toolbox|"
    r"explorer (?:window|panel)|properties (?:window|panel)|insert object|press (?:the )?\w+ (?:key|button))\b",
    re.I,
)
# Principles and definitions ("a core loop consists of...", "for example, in Jailbreak...").
_PRINCIPLE = [re.compile(p, re.I) for p in (
    r"\bcan be (?:broken down|divided|split) into\b", r"\bconsists? of\b", r"\b(?:for example|as an example|such as)\b",
    r"\bthe (?:core|game(?:play)?|primary) loop (?:is|in|of)\b",
    r"\b(?:well-designed|successful|great|good|best|top|popular) (?:games?|experiences?|loops?|onboarding)\b",
    r"\bthe (?:goal|purpose|job) of\b", r"\b(?:works?|worked) because\b", r"\bplayers? (?:want|love|hate|need|expect)\b",
)]


_LEAD_IN = re.compile(
    r"^(?:(?:so|and|okay|ok|alright),? )?(?:number (?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)|"
    r"tip (?:number )?\w+|step \w+|first(?:ly)?|second(?:ly)?|third(?:ly)?|next(?: up)?|finally|"
    r"the (?:first|second|third|next|last|biggest) (?:thing|tip|step|mistake|reason))\b",
    re.I,
)


@dataclass
class ExtractConfig:
    min_actionability: float = 0.45
    min_actionability_docs: float = 0.3
    min_words: int = 7
    max_passage_words: int = 75
    max_insights_per_pillar_per_source: int = 20


_NUMERIC = re.compile(r"\d|\bd(?:1|7|30)\b|\bday (?:one|seven|thirty)\b", re.I)


def metric_mentions(text: str) -> list[str]:
    """Each *numeric* metric with a few words of context: '40% D1 retention'.

    Bare metric words ("retention") raise actionability but are not numbers worth citing.
    """
    out = []
    for m in _METRIC.finditer(text):
        if not _NUMERIC.search(m.group(0)):
            continue
        left = text[: m.start()].split()[-3:]
        right = text[m.end():].split()[:3]
        out.append(" ".join([*left, m.group(0), *right]).strip(" ,.;:"))
    return list(dict.fromkeys(out))


def actionability(text: str, pillar_score: float, *, first_party: bool = False) -> float:
    """0..1: how much a sentence reads like transferable design advice.

    Directives, imperatives, causal reasoning, numbers and stated principles raise it;
    click-path procedure lowers it. First-party text gets a bonus because its plain
    declarative statements ("discounts on subscriptions are not eligible") are facts.
    """
    strong = sum(1 for r in _DIRECTIVE_STRONG if r.search(text))
    weak = sum(1 for r in _DIRECTIVE_WEAK if r.search(text))
    directive = min(strong + 0.5 * weak, 1.5)
    causal = bool(_CAUSAL.search(text))
    a = directive * 0.4
    a += 0.25 if _IMPERATIVE.search(text) else 0.0
    a += 0.15 if causal else 0.0
    a += 0.15 if _METRIC.search(text) else 0.0
    a += min(pillar_score, 3.0) / 3.0 * 0.2
    a += min(sum(1 for r in _PRINCIPLE if r.search(text)), 2) * 0.12
    if first_party:
        a += 0.15
    if _PROCEDURE.search(text) and not causal:
        a -= 0.35
    return round(max(0.0, min(a, 1.0)), 3)


_FILLER = re.compile(r"\b(?:um+|uh+|like|you know|okay|ok|so yeah|kind of|sort of|i mean|basically|literally)\b", re.I)


def readability(text: str) -> float:
    """0.5..1.0 - how well a passage stands alone as a quote (used to rank evidence)."""
    words = text.split()
    n = len(words) or 1
    q = 1.0
    if not text[:1].isupper() and not text[:1].isdigit():
        q -= 0.15  # starts mid-sentence (typical of unpunctuated ASR)
    if not re.search(r"[.!?…\"')]$", text.strip()):
        q -= 0.1  # trails off
    if n < 10 or n > 70:
        q -= 0.1
    q -= min(len(_FILLER.findall(text)) / n * 4, 0.25)
    return round(max(q, 0.5), 3)


def _jaccard(a: str, b: str) -> float:
    sa, sb = set(a.lower().split()), set(b.lower().split())
    return len(sa & sb) / (len(sa | sb) or 1)


def extract_insights(
    doc: Document,
    *,
    kind: str,
    hint_pillars: list[str] | tuple[str, ...] = (),
    cfg: ExtractConfig | None = None,
    pillars: dict[str, Pillar] | None = None,
) -> list[Insight]:
    cfg = cfg or ExtractConfig()
    pillars = pillars or TAXONOMY
    threshold = cfg.min_actionability_docs if kind == "doc" else cfg.min_actionability
    # Re-clean: cached documents may predate a cleaning rule.
    segs: list[Segment] = [Segment(t, s.start) for s in doc.segments if (t := clean_text(s.text))]

    # Score every sentence once.
    scored = []
    for i, seg in enumerate(segs):
        words = len(seg.text.split())
        if words < cfg.min_words or _NOISE.search(seg.text):
            scored.append(None)
            continue
        cls = classify(seg.text, hint_pillars=hint_pillars, pillars=pillars)
        if not cls:
            scored.append(None)
            continue
        best = cls[0]
        a = actionability(seg.text, best.score, first_party=kind == "doc")
        # Strongly on-topic statements clear a lower bar than passing remarks.
        bar = threshold - 0.1 if best.score >= 2.5 else threshold
        scored.append((cls, a) if a >= bar else None)

    # Merge consecutive qualifying sentences that share a top pillar into passages.
    passages: list[tuple[int, int]] = []
    last_end = -1
    i = 0
    while i < len(segs):
        if scored[i] is None:
            i += 1
            continue
        start = i
        # Absorb a short lead-in ("Number one is daily rewards.") that names the topic.
        prev = segs[i - 1].text if i > 0 else ""
        if i - 1 > last_end and prev and len(prev.split()) <= 10 and not _NOISE.search(prev):
            prev_cls = classify(prev, hint_pillars=hint_pillars, pillars=pillars, threshold=0.4)
            if _LEAD_IN.search(prev) or any(c.pillar == scored[i][0][0].pillar for c in prev_cls):
                start = i - 1
        j = i
        words = sum(len(s.text.split()) for s in segs[start: i + 1])
        while (
            j + 1 < len(segs)
            and scored[j + 1] is not None
            and scored[j + 1][0][0].pillar == scored[i][0][0].pillar
            and words + len(segs[j + 1].text.split()) <= cfg.max_passage_words
        ):
            j += 1
            words += len(segs[j].text.split())
        # A short qualifying sentence ("Daily rewards are key:") needs its explanation.
        if j == i and j + 1 < len(segs) and (words < 14 or segs[i].text.rstrip().endswith(":")):
            nxt = segs[j + 1].text
            if not _NOISE.search(nxt) and words + len(nxt.split()) <= cfg.max_passage_words:
                j += 1
        passages.append((start, j))
        last_end = j
        i = j + 1

    insights: list[Insight] = []
    for i, j in passages:
        text = " ".join(s.text for s in segs[i: j + 1])
        cls = classify(text, hint_pillars=hint_pillars, pillars=pillars)
        if not cls:
            continue
        a = max(sc[1] for sc in scored[i: j + 1] if sc is not None)
        metrics = metric_mentions(text)
        # One insight per qualifying pillar (a tip can be both onboarding and retention).
        top = cls[0].score
        for c in cls:
            if c.score < max(1.0, 0.5 * top):
                continue
            insights.append(Insight(
                source_id=doc.source_id,
                pillar=c.pillar,
                mechanics=[k for k, _ in c.mechanics],
                text=text,
                start=segs[i].start,
                actionability=a,
                metrics=metrics,
                extractor="heuristic",
            ))

    # Drop near-duplicates and cap per pillar so one long video cannot dominate.
    kept: list[Insight] = []
    for ins in sorted(insights, key=lambda x: -x.actionability):
        same = [k for k in kept if k.pillar == ins.pillar]
        if len(same) >= cfg.max_insights_per_pillar_per_source:
            continue
        if any(_jaccard(k.text, ins.text) > 0.8 for k in same):
            continue
        kept.append(ins)
    return sorted(kept, key=lambda x: (x.start is None, x.start or 0.0, x.pillar))
