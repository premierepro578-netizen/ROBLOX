"""Find the top N videos for a set of searches, ranked by views per day, and fetch transcripts.

Unlike the pillar pipeline (which balances sources across design pillars), this answers a
simpler question: "what are the best-performing recent videos about X?" Results are written
into a store in the same shape the pipeline uses (``sources`` + ``documents``), so the normal
``bpe analyze`` / ``bpe synthesize`` stages run on them unchanged.

Ranking: views / max(age_days, 14) among videos that are (a) recent (``max_age_days``),
(b) long-form (``min_duration_s``..``max_duration_s``), (c) on-topic (``require`` regex on
title/description/channel) and (d) teaching or analysing rather than gameplay entertainment
(developer-intent signal from ``ranking.dev_intent``), and that have an English transcript.
"""

from __future__ import annotations

import logging
import math
import re
import tomllib
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from blueprint_engine.analysis.segment import segments_from_tokens
from blueprint_engine.models import Document, Source
from blueprint_engine.net import RateLimiter, make_session
from blueprint_engine.pipeline import parallel
from blueprint_engine.ranking import clean_description, dev_intent
from blueprint_engine.sources.youtube import YouTubeClient, age_days, pick_track, to_source
from blueprint_engine.store import Store

log = logging.getLogger(__name__)


@dataclass
class Group:
    name: str
    n: int
    queries: list[str]
    require: str = r"roblox|\brbx\b|\bluau\b"


@dataclass
class Spec:
    groups: list[Group]
    results_per_query: int = 20
    shortlist: int = 70
    max_age_days: int = 1095
    min_duration_s: int = 180
    max_duration_s: int = 3600
    min_dev_intent: float = 0.6
    workers: int = 3
    request_interval_s: float = 0.8
    languages: list[str] = field(default_factory=lambda: ["en"])


def load_spec(path: str | Path) -> Spec:
    raw = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    run = raw.get("run", {})
    groups = [Group(name=k, n=int(v["n"]), queries=list(v["queries"]), require=v.get("require", Group.require))
              for k, v in raw.get("groups", {}).items()]
    if not groups:
        raise ValueError("spec needs at least one [groups.<name>] table")
    return Spec(groups=groups, **run)


def run_top_videos(spec: Spec, data_dir: str | Path, today: date | None = None) -> dict[str, Any]:
    store = Store(data_dir)
    yt = YouTubeClient(RateLimiter(spec.request_interval_s), make_session(), spec.languages)
    report: dict[str, Any] = {"groups": {}}
    taken: set[str] = set()
    selected_all: list[Source] = []

    for grp in spec.groups:
        req = re.compile(grp.require, re.I)
        cands: dict[str, dict[str, Any]] = {}
        for q, entries, err in parallel(lambda q: yt.search(q, spec.results_per_query), grp.queries, spec.workers):
            if err:
                log.warning("search failed %r: %s", q, err)
                continue
            for e in entries or []:
                dur = e.get("duration")
                if dur and not (spec.min_duration_s <= dur <= spec.max_duration_s):
                    continue
                c = cands.setdefault(e["id"], {**e, "queries": []})
                c["queries"].append(q)

        # Cheap pre-filter on the snippet, then full metadata for the most-viewed shortlist.
        pre = [c for c in cands.values() if req.search(f"{c['title']} {c.get('description', '')} {c.get('channel', '')}")]
        pre.sort(key=lambda c: -(c.get("view_count") or 0))
        shortlist = [c for c in pre if c["id"] not in taken][: spec.shortlist]

        def meta(c: dict[str, Any]) -> dict[str, Any]:
            hit = store.get("yt_info", c["id"])
            if hit:
                return hit
            info = yt.info(c["id"])
            store.put("yt_info", c["id"], info)
            return info

        rows = []
        for c, info, err in parallel(meta, shortlist, spec.workers):
            if err:
                log.debug("metadata failed %s: %s", c["id"], err)
                continue
            src = to_source(info)
            age = age_days(src.published, today)
            desc = clean_description(src.description)
            if age is None or age > spec.max_age_days:
                continue
            if not req.search(f"{src.title} {desc} {src.author} {' '.join(src.tags)}"):
                continue
            intent = dev_intent(src.title, desc)
            if intent < spec.min_dev_intent:
                continue
            if not pick_track(info, spec.languages):
                continue
            vpd = (src.views or 0) / max(age, 14)
            src.queries = c["queries"]
            src.tags = [grp.name] + src.tags[:10]
            src.score_breakdown = {"views_per_day": round(vpd, 1), "age_days": age, "dev_intent": intent}
            rows.append((vpd, src, info))
        rows.sort(key=lambda r: -r[0])

        chosen: list[Source] = []
        for vpd, src, info in rows:
            if len(chosen) >= grp.n:
                break
            cached = store.get("documents", src.id)
            try:
                if cached:
                    doc = Document.from_json(cached)
                else:
                    tokens, origin, lang = yt.transcript(info)
                    doc = Document(src.id, origin, lang, segments_from_tokens(tokens))
                    store.put("documents", src.id, doc.to_dict())
            except Exception as exc:  # noqa: BLE001 - skip and back-fill from the ranking
                log.debug("transcript failed %s: %s", src.id, exc)
                continue
            src.transcript_origin = doc.origin
            chosen.append(src)
            taken.add(src.id[3:])

        # Score for synthesis weighting: normalised log views/day within the group (0.3..1.0).
        if chosen:
            logs = [math.log1p(s.score_breakdown["views_per_day"]) for s in chosen]
            lo, hi = min(logs), max(logs)
            for s, lv in zip(chosen, logs):
                s.score = round(0.3 + 0.7 * ((lv - lo) / (hi - lo) if hi > lo else 1.0), 4)
        selected_all.extend(chosen)
        report["groups"][grp.name] = {
            "candidates": len(cands), "roblox_shortlist": len(shortlist), "eligible": len(rows),
            "selected": [{"rank": i + 1, "id": s.id, "title": s.title, "channel": s.author, "views": s.views,
                          "published": s.published, **s.score_breakdown, "url": s.url}
                         for i, s in enumerate(chosen)],
        }

    store.clear("sources")
    for s in selected_all:
        store.put("sources", s.id, s.to_dict())
    store.put("state", "top_videos", report)
    return report
