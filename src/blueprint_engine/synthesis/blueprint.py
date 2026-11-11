"""Cross-source synthesis: turn per-source insights into a prioritised blueprint.

For every (pillar, mechanic):
  support   = distinct sources that teach it (videos, docs, threads)
  weight    = sum over sources of (0.35 + source score) * best actionability * repetition bonus
  consensus = support / sources analysed for that pillar
  priority  = P0 (top-3 by weight with >=3 sources, or >=2 incl. first-party docs),
              P1 (>=2 sources or top-6), P2 otherwise
Evidence quotes are chosen for strength *and* diversity (one per source first).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from blueprint_engine.analysis.taxonomy import TAXONOMY, mechanic_label
from blueprint_engine.config import Config
from blueprint_engine.models import Document, Insight, Source
from blueprint_engine.synthesis.playbook import STALE_RULES, play_for

MAX_QUOTE_WORDS = 45


def excerpt(text: str, max_words: int = MAX_QUOTE_WORDS) -> str:
    words = text.split()
    return text if len(words) <= max_words else " ".join(words[:max_words]) + " …"


@dataclass
class Evidence:
    source_id: str
    title: str
    author: str
    kind: str
    link: str
    quote: str
    start: float | None
    actionability: float
    source_score: float
    metrics: list[str] = field(default_factory=list)
    tactic: str | None = None
    stale: str | None = None


@dataclass
class MechanicFinding:
    pillar: str
    mechanic: str
    label: str
    priority: str
    weight: float
    support: int
    media_support: int
    doc_support: list[str]
    consensus: float
    n_insights: int
    evidence: list[Evidence]
    metrics: list[str]
    playbook: dict[str, list[str]] | None
    stale_flags: list[str] = field(default_factory=list)


@dataclass
class PillarFinding:
    pillar: str
    label: str
    focus: bool
    sources_analyzed: int
    insights: int
    mechanics: list[MechanicFinding]


@dataclass
class Blueprint:
    generated_at: str
    extractor: str
    totals: dict[str, Any]
    sources: list[dict[str, Any]]
    pillars: list[PillarFinding]
    platform_notices: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def pillar(self, key: str) -> PillarFinding | None:
        return next((p for p in self.pillars if p.pillar == key), None)


def _evidence(ins: Insight, src: Source) -> Evidence:
    stale = next((r.notice for r in STALE_RULES if r.matches(ins.text) and src.kind != "doc"), None)
    return Evidence(
        source_id=src.id,
        title=src.title,
        author=src.author,
        kind=src.kind,
        link=src.link(ins.start),
        quote=excerpt(ins.text),
        start=ins.start,
        actionability=ins.actionability,
        source_score=src.score,
        metrics=ins.metrics[:6],
        tactic=ins.tactic,
        stale=stale,
    )


def _pick_evidence(items: list[tuple[Insight, Source]], k: int = 5) -> list[Evidence]:
    ranked = sorted(items, key=lambda x: -(x[0].actionability * (0.35 + x[1].score) + (0.05 if x[0].metrics else 0)))
    chosen: list[tuple[Insight, Source]] = []
    seen: set[str] = set()
    # Pass 1: best insight from each distinct media source; pass 2: one first-party doc line.
    for ins, src in ranked:
        if src.kind != "doc" and src.id not in seen and len(chosen) < k - 1:
            chosen.append((ins, src))
            seen.add(src.id)
    doc = next(((i, s) for i, s in ranked if s.kind == "doc"), None)
    if doc:
        chosen.append(doc)
    for ins, src in ranked:  # top up if few sources
        if len(chosen) >= k:
            break
        if (ins, src) not in chosen and src.id not in seen:
            chosen.append((ins, src))
            seen.add(src.id)
    return [_evidence(i, s) for i, s in chosen]


def platform_notices(sources: dict[str, Source], documents: dict[str, Document]) -> list[dict[str, str]]:
    """Deprecation / replacement sentences found in first-party docs."""
    import re

    pat = re.compile(r"\b(?:deprecated|replaced by|no longer (?:available|supported)|sunset|will be removed)\b", re.I)
    out = []
    for sid, doc in documents.items():
        src = sources.get(sid)
        if not src or src.kind != "doc":
            continue
        for seg in doc.segments:
            if pat.search(seg.text):
                out.append({"source_id": sid, "title": src.title, "url": src.url, "text": seg.text})
    return out


def build_blueprint(cfg: Config, sources: dict[str, Source], insights: list[Insight],
                    documents: dict[str, Document], extractor: str) -> Blueprint:
    by_pillar: dict[str, list[Insight]] = defaultdict(list)
    for ins in insights:
        if ins.source_id in sources and ins.pillar in cfg.pillars:
            by_pillar[ins.pillar].append(ins)

    pillars: list[PillarFinding] = []
    for pkey, pcfg in cfg.pillars.items():
        items = by_pillar.get(pkey, [])
        sources_in_pillar = {i.source_id for i in items} | {s.id for s in sources.values() if pkey in s.pillars}
        denom = max(len(sources_in_pillar), 1)

        groups: dict[str, list[tuple[Insight, Source]]] = defaultdict(list)
        for ins in items:
            for mech in ins.mechanics or ["other"]:
                groups[mech].append((ins, sources[ins.source_id]))

        findings: list[MechanicFinding] = []
        for mech, pairs in groups.items():
            per_source: dict[str, list[Insight]] = defaultdict(list)
            for ins, src in pairs:
                per_source[src.id].append(ins)
            weight = 0.0
            for sid, lst in per_source.items():
                best = max(i.actionability for i in lst)
                weight += (0.35 + sources[sid].score) * best * (1 + 0.15 * min(len(lst) - 1, 3))
            doc_titles = sorted({sources[sid].title for sid in per_source if sources[sid].kind == "doc"})
            metrics = list(dict.fromkeys(m for ins, _ in pairs for m in ins.metrics))[:12]
            play = play_for(pkey, mech)
            evidence = _pick_evidence(pairs)
            findings.append(MechanicFinding(
                pillar=pkey,
                mechanic=mech,
                label=mechanic_label(pkey, mech),
                priority="P2",
                weight=round(weight, 3),
                support=len(per_source),
                media_support=sum(1 for sid in per_source if sources[sid].kind != "doc"),
                doc_support=doc_titles,
                consensus=round(len(per_source) / denom, 3),
                n_insights=len(pairs),
                evidence=evidence,
                metrics=metrics,
                playbook={k: list(v) for k, v in asdict(play).items()} if play else None,
                stale_flags=sorted({e.stale for e in evidence if e.stale}),
            ))

        findings.sort(key=lambda f: -f.weight)
        for rank, f in enumerate(findings, 1):
            if rank <= 3 and (f.support >= 3 or (f.support >= 2 and f.doc_support)):
                f.priority = "P0"
            elif f.support >= 2 or rank <= 6:
                f.priority = "P1"
        pillars.append(PillarFinding(
            pillar=pkey,
            label=pcfg.label,
            focus=pcfg.focus,
            sources_analyzed=len(sources_in_pillar),
            insights=len(items),
            mechanics=findings,
        ))

    kinds: dict[str, int] = defaultdict(int)
    for s in sources.values():
        kinds[s.kind] += 1
    words = sum(d.word_count for sid, d in documents.items() if sid in sources)
    ranked_sources = sorted(sources.values(), key=lambda s: (s.kind == "doc", -s.score))
    return Blueprint(
        generated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        extractor=extractor,
        totals={
            "sources": len(sources),
            "by_kind": dict(kinds),
            "words_analyzed": words,
            "insights": len(insights),
            "transcript_origins": _count(s.transcript_origin or "n/a" for s in sources.values()),
        },
        sources=[
            {
                "id": s.id, "kind": s.kind, "title": s.title, "author": s.author, "url": s.url,
                "published": s.published, "views": s.views, "likes": s.likes, "followers": s.followers,
                "duration_s": s.duration_s, "score": s.score, "score_breakdown": s.score_breakdown,
                "pillars": s.pillars, "transcript_origin": s.transcript_origin,
                "insights": sum(1 for i in insights if i.source_id == s.id),
            }
            for s in ranked_sources
        ],
        pillars=pillars,
        platform_notices=platform_notices(sources, documents),
    )


def _count(values) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for v in values:
        out[v] += 1
    return dict(out)


__all__ = ["Blueprint", "PillarFinding", "MechanicFinding", "Evidence", "build_blueprint", "TAXONOMY"]
