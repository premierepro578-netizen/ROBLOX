"""Stage orchestration: discover -> fetch -> analyze -> synthesize.

Every network result is cached in the store, so stages are resumable and re-runs only
do new work. Network-bound steps run on a thread pool behind one shared rate limiter.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar

from blueprint_engine.analysis.extract import extract_insights
from blueprint_engine.analysis.segment import segments_from_tokens
from blueprint_engine.config import Config
from blueprint_engine.models import Document, Insight, Source, from_dict
from blueprint_engine.net import RateLimiter, make_session
from blueprint_engine.ranking import prescore, score_sources
from blueprint_engine.sources import NoTranscript, SourceUnavailable
from blueprint_engine.sources.devforum import DevForumClient
from blueprint_engine.sources.roblox_docs import RobloxDocsClient
from blueprint_engine.sources.tiktok import TikTokClient
from blueprint_engine.sources.youtube import YouTubeClient, age_days, pick_track, to_source
from blueprint_engine.store import Store

log = logging.getLogger(__name__)
T = TypeVar("T")
R = TypeVar("R")


@dataclass
class StageReport:
    stage: str
    seconds: float = 0.0
    counts: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def bump(self, key: str, n: int = 1) -> None:
        self.counts[key] = self.counts.get(key, 0) + n

    def summary(self) -> str:
        counts = ", ".join(f"{k}={v}" for k, v in sorted(self.counts.items()))
        return f"[{self.stage}] {self.seconds:.1f}s  {counts}"


def parallel(fn: Callable[[T], R], items: Iterable[T], workers: int) -> list[tuple[T, R | None, BaseException | None]]:
    """Map ``fn`` over ``items`` on a thread pool; never raises, returns (item, result, error)."""
    items = list(items)
    out: list[tuple[T, R | None, BaseException | None]] = []
    if not items:
        return out
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futs = {pool.submit(fn, it): it for it in items}
        for fut in as_completed(futs):
            it = futs[fut]
            try:
                out.append((it, fut.result(), None))
            except Exception as exc:  # noqa: BLE001 - per-item failures are reported, not fatal
                out.append((it, None, exc))
    return out


class Pipeline:
    def __init__(self, cfg: Config, data_dir: str | Path, *, workers: int | None = None, refresh: bool = False):
        self.cfg = cfg
        self.store = Store(data_dir)
        self.workers = workers or cfg.run.workers
        self.refresh = refresh
        self.limiter = RateLimiter(cfg.run.min_request_interval_s)
        self.docs_limiter = RateLimiter(0.2)
        self.session = make_session()
        langs = cfg.run.languages
        self.yt = YouTubeClient(self.limiter, self.session, langs)
        self.tt = TikTokClient(self.limiter, self.session, langs)
        self.docs = RobloxDocsClient(cfg.docs_base_url, self.docs_limiter, self.session)
        self.forum = DevForumClient(cfg.devforum.base_url, self.docs_limiter, self.session)

    # ------------------------------------------------------------------ discover
    def discover(self) -> StageReport:
        rep = StageReport("discover")
        t0 = time.monotonic()
        run = self.cfg.run
        jobs = [(pk, q) for pk, p in self.cfg.pillars.items() for q in p.queries]
        prev = self.store.get("state", "candidates", {}) if not self.refresh else {}
        yt: dict[str, dict[str, Any]] = prev.get("youtube", {})
        done_queries = set(prev.get("queries_done", []))
        todo = [j for j in jobs if f"{j[0]}::{j[1]}" not in done_queries]

        for (pillar, query), entries, err in parallel(lambda j: self.yt.search(j[1], run.results_per_query), todo, self.workers):
            if err:
                rep.bump("search_failed")
                rep.notes.append(f"search failed: {query!r}: {err}")
                continue
            rep.bump("searches")
            done_queries.add(f"{pillar}::{query}")
            for e in entries or []:
                dur = e.get("duration")
                if dur and not (run.min_duration_s <= dur <= run.max_duration_s):
                    rep.bump("filtered_duration")
                    continue
                c = yt.setdefault(e["id"], {**e, "queries": [], "pillars": [], "prescore": {}})
                c["view_count"] = e.get("view_count") or c.get("view_count")
                if query not in c["queries"]:
                    c["queries"].append(query)
                if pillar not in c["pillars"]:
                    c["pillars"].append(pillar)
                c["prescore"][pillar] = round(max(c["prescore"].get(pillar, 0.0), prescore(e, pillar)), 4)

        tiktok = set(prev.get("tiktok", [])) | set(self.cfg.tiktok.videos)
        for handle, urls, err in parallel(lambda h: self.tt.feed(h, self.cfg.tiktok.max_per_handle),
                                          self.cfg.tiktok.handles, self.workers):
            if err:
                rep.notes.append(f"tiktok feed failed: {handle}: {err}")
                rep.bump("tiktok_feed_failed")
                continue
            tiktok.update(urls or [])

        forum_topics: dict[str, list[str]] = prev.get("devforum", {})
        if self.cfg.devforum.queries:
            if self.forum.available():
                for q, ids, err in parallel(lambda q: self.forum.search_topics(q, self.cfg.devforum.topics_per_query),
                                            self.cfg.devforum.queries, 2):
                    if not err:
                        for tid in ids or []:
                            forum_topics.setdefault(str(tid), [])
                            if q not in forum_topics[str(tid)]:
                                forum_topics[str(tid)].append(q)
            else:
                rep.notes.append("DevForum unavailable (maintenance redirect or refused); skipped")

        self.store.put("state", "candidates", {
            "youtube": yt,
            "queries_done": sorted(done_queries),
            "tiktok": sorted(tiktok),
            "devforum": forum_topics,
        })
        rep.counts.update(youtube_candidates=len(yt), tiktok_candidates=len(tiktok), devforum_candidates=len(forum_topics),
                          doc_pages=len(self.cfg.docs))
        rep.seconds = time.monotonic() - t0
        return rep

    # --------------------------------------------------------------------- fetch
    def _cached(self, collection: str, key: str, fn: Callable[[], Any]) -> Any:
        if not self.refresh:
            hit = self.store.get(collection, key)
            if hit is not None:
                return hit
        val = fn()
        self.store.put(collection, key, val)
        return val

    def _yt_info(self, vid: str) -> dict[str, Any]:
        return self._cached("yt_info", vid, lambda: self.yt.info(vid))

    def _yt_transcript(self, src: Source, info: dict[str, Any]) -> Document:
        cached = None if self.refresh else self.store.get("documents", src.id)
        if cached:
            return Document.from_json(cached)

        def refresh() -> dict[str, Any]:
            fresh = self.yt.info(info["id"])
            self.store.put("yt_info", info["id"], fresh)
            return fresh

        tokens, origin, lang = self.yt.transcript(info, refresh=refresh)
        doc = Document(src.id, origin, lang, segments_from_tokens(tokens))
        if not doc.segments:
            raise NoTranscript(f"{src.id}: transcript was empty")
        self.store.put("documents", src.id, doc.to_dict())
        return doc

    def fetch(self) -> StageReport:
        rep = StageReport("fetch")
        t0 = time.monotonic()
        run = self.cfg.run
        cands = self.store.get("state", "candidates")
        if not cands:
            raise RuntimeError("no candidates yet - run `bpe discover` first")
        # Only candidates surfaced by queries still in the config (queries can be edited/removed).
        active = {(pk, q) for pk, p in self.cfg.pillars.items() for q in p.queries}
        yt = {}
        for vid, c in cands.get("youtube", {}).items():
            pillars = [pk for pk in c["pillars"] if any((pk, q) in active for q in c["queries"])]
            if pillars:
                yt[vid] = {**c, "pillars": pillars, "queries": [q for q in c["queries"] if any((pk, q) in active for pk in pillars)]}

        # 1. Shortlist per pillar on the cheap pre-score, then pull full metadata.
        shortlist: set[str] = set()
        for pillar in self.cfg.pillars:
            ranked = sorted((c for c in yt.values() if pillar in c["pillars"]),
                            key=lambda c: -c["prescore"].get(pillar, 0.0))
            shortlist.update(c["id"] for c in ranked[: run.shortlist_per_pillar])
        infos: dict[str, dict[str, Any]] = {}
        for vid, info, err in parallel(self._yt_info, sorted(shortlist), self.workers):
            if err:
                rep.bump("metadata_failed")
                log.debug("metadata failed %s: %s", vid, err)
            else:
                infos[vid] = info
        rep.counts["metadata"] = len(infos)

        # 2. Score every video that passes freshness/length filters.
        videos: list[Source] = []
        for vid, info in infos.items():
            src = to_source(info)
            src.queries = yt[vid]["queries"]
            src.pillars = yt[vid]["pillars"]
            age = age_days(src.published)
            if age is not None and age > run.max_age_days:
                rep.bump("filtered_stale")
                continue
            if src.duration_s and not (run.min_duration_s <= src.duration_s <= run.max_duration_s):
                rep.bump("filtered_duration")
                continue
            videos.append(src)
        score_sources(videos)
        ranked_all = list(videos)  # kept for the transparency log, including rejected ones
        videos = [v for v in videos if v.score_breakdown.get("relevance", 0.0) >= run.min_relevance]
        rep.counts["filtered_off_topic"] = len(ranked_all) - len(videos)

        # 3. Per pillar, take the best-scoring videos that have a usable caption track,
        #    over-fetching a little so transcript failures can be back-filled.
        want: dict[str, Source] = {}
        for pillar in self.cfg.pillars:
            ranked = sorted((v for v in videos if pillar in v.pillars), key=lambda v: -v.score)
            ranked = [v for v in ranked if pick_track(infos[v.id[3:]], run.languages)] or ranked
            for v in ranked[: run.top_per_pillar + 4]:
                want[v.id] = v
        docs_ok: dict[str, Document] = {}
        for src, doc, err in parallel(lambda s: self._yt_transcript(s, infos[s.id[3:]]), list(want.values()), self.workers):
            if err:
                rep.bump("transcript_failed")
                log.debug("transcript failed %s: %s", src.id, err)
            else:
                docs_ok[src.id] = doc
        selected: dict[str, Source] = {}
        for pillar in self.cfg.pillars:
            ranked = sorted((v for v in videos if pillar in v.pillars and v.id in docs_ok), key=lambda v: -v.score)
            for v in ranked[: run.top_per_pillar]:
                selected[v.id] = v
        for sid, src in selected.items():
            src.transcript_origin = docs_ok[sid].origin

        # 4. First-party docs, TikTok, DevForum.
        def fetch_doc(page) -> tuple[Source, Document]:
            key = f"doc:{page.path}"
            hit = None if self.refresh else self.store.get("doc_cache", key)
            if hit:
                return from_dict(Source, hit["source"]), Document.from_json(hit["document"])
            src, doc = self.docs.fetch(page.path)
            self.store.put("doc_cache", key, {"source": src.to_dict(), "document": doc.to_dict()})
            return src, doc

        for page, res, err in parallel(fetch_doc, self.cfg.docs, self.workers):
            if err:
                rep.bump("doc_failed")
                rep.notes.append(f"doc {page.path}: {err}")
                continue
            src, doc = res
            src.pillars = page.pillars
            selected[src.id] = src
            docs_ok[src.id] = doc
            rep.bump("docs")

        def fetch_tt(url: str) -> tuple[Source, Document]:
            hit = None if self.refresh else self.store.get("tt_cache", url)
            if hit:
                return from_dict(Source, hit["source"]), Document.from_json(hit["document"])
            src, doc = self.tt.fetch(url)
            self.store.put("tt_cache", url, {"source": src.to_dict(), "document": doc.to_dict()})
            return src, doc

        tiktok_sources = []
        for url, res, err in parallel(fetch_tt, cands.get("tiktok", []), self.workers):
            if err:
                rep.bump("tiktok_failed")
                continue
            src, doc = res
            tiktok_sources.append(src)
            selected[src.id] = src
            docs_ok[src.id] = doc
            rep.bump("tiktok_" + (src.transcript_origin or "unknown"))
        score_sources(tiktok_sources)

        forum_sources = []
        topics = cands.get("devforum", {})
        if topics:
            def fetch_topic(tid: str) -> tuple[Source, Document]:
                return self._cached_pair("df_cache", tid, lambda: self.forum.fetch_topic(int(tid)))

            for tid, res, err in parallel(fetch_topic, list(topics), 2):
                if err:
                    rep.bump("devforum_failed")
                    continue
                src, doc = res
                src.queries = topics[tid]
                forum_sources.append(src)
                selected[src.id] = src
                docs_ok[src.id] = doc
            score_sources(forum_sources)

        # 5. Persist the selection (plus the full ranking, for transparency in the report).
        #    The selection is replaced wholesale so re-ranking can drop sources.
        self.store.clear("sources")
        for sid, src in selected.items():
            self.store.put("sources", sid, src.to_dict())
            if not self.store.exists("documents", sid) or src.kind != "youtube":
                self.store.put("documents", sid, docs_ok[sid].to_dict())
        self.store.put("state", "ranking", {
            "generated": date.today().isoformat(),
            "videos": [
                {**v.to_dict(), "description": v.description[:300], "selected": v.id in selected}
                for v in sorted(ranked_all, key=lambda v: -v.score)
            ],
        })
        by_kind: dict[str, int] = {}
        for s in selected.values():
            by_kind[s.kind] = by_kind.get(s.kind, 0) + 1
        rep.counts.update({f"selected_{k}": n for k, n in by_kind.items()})
        rep.counts["words"] = sum(d.word_count for sid, d in docs_ok.items() if sid in selected)
        rep.seconds = time.monotonic() - t0
        return rep

    def _cached_pair(self, collection: str, key: str, fn: Callable[[], tuple[Source, Document]]) -> tuple[Source, Document]:
        hit = None if self.refresh else self.store.get(collection, key)
        if hit:
            return from_dict(Source, hit["source"]), Document.from_json(hit["document"])
        src, doc = fn()
        self.store.put(collection, key, {"source": src.to_dict(), "document": doc.to_dict()})
        return src, doc

    # ------------------------------------------------------------------- analyze
    def load_sources(self) -> dict[str, Source]:
        return {d["id"]: from_dict(Source, d) for _, d in self.store.items("sources")}

    def analyze(self, extractor: str = "heuristic", model: str | None = None, effort: str = "medium") -> StageReport:
        rep = StageReport(f"analyze:{extractor}")
        t0 = time.monotonic()
        sources = self.load_sources()
        if not sources:
            raise RuntimeError("no sources yet - run `bpe fetch` first")

        if extractor == "claude":
            from blueprint_engine.analysis.llm import DEFAULT_MODEL, ClaudeExtractor, FatalLLMError

            ex = ClaudeExtractor(model=model or DEFAULT_MODEL, effort=effort)

            def run_one(src: Source) -> list[Insight]:
                key = f"{src.id}.claude"
                hit = None if self.refresh else self.store.get("insights", key)
                if hit is not None:
                    return [from_dict(Insight, i) for i in hit]
                doc = Document.from_json(self.store.get("documents", src.id))
                found = ex.extract(src, doc)
                self.store.put("insights", key, [i.to_dict() for i in found])
                return found

            results = parallel(run_one, sources.values(), min(self.workers, 4))
            fatal = next((e for _, _, e in results if isinstance(e, FatalLLMError)), None)
            if fatal:
                raise fatal
        elif extractor == "heuristic":
            def run_one(src: Source) -> list[Insight]:
                doc = Document.from_json(self.store.get("documents", src.id))
                found = extract_insights(doc, kind=src.kind, hint_pillars=src.pillars)
                self.store.put("insights", f"{src.id}.heuristic", [i.to_dict() for i in found])
                return found

            results = [(s, *self._safe(run_one, s)) for s in sources.values()]
        else:
            raise ValueError(f"unknown extractor {extractor!r}")

        for src, found, err in results:
            if err:
                rep.bump("failed")
                rep.notes.append(f"{src.id}: {type(err).__name__}: {err}")
                continue
            rep.bump("sources")
            rep.bump("insights", len(found or []))
            for ins in found or []:
                rep.bump(f"pillar_{ins.pillar}")
        rep.seconds = time.monotonic() - t0
        return rep

    @staticmethod
    def _safe(fn: Callable[[T], R], arg: T) -> tuple[R | None, BaseException | None]:
        try:
            return fn(arg), None
        except Exception as exc:  # noqa: BLE001
            return None, exc

    def load_insights(self, extractor: str) -> list[Insight]:
        """``extractor`` = heuristic | claude | best (claude where present, else heuristic)."""
        per_source: dict[str, dict[str, list[Insight]]] = {}
        for key, items in self.store.items("insights"):
            stem, _, ex = key.rpartition(".")
            per_source.setdefault(stem, {})[ex] = [from_dict(Insight, i) for i in items]
        out: list[Insight] = []
        for by_ex in per_source.values():
            if extractor == "best":
                out.extend(by_ex.get("claude") or by_ex.get("heuristic") or [])
            else:
                out.extend(by_ex.get(extractor, []))
        return out

    # ---------------------------------------------------------------- synthesize
    def synthesize(self, reports_dir: str | Path, extractor: str = "best") -> StageReport:
        from blueprint_engine.synthesis.blueprint import build_blueprint
        from blueprint_engine.synthesis.framework import write_framework
        from blueprint_engine.synthesis.report import render_report

        rep = StageReport("synthesize")
        t0 = time.monotonic()
        sources = self.load_sources()
        insights = self.load_insights(extractor)
        if not insights:
            raise RuntimeError(f"no {extractor!r} insights yet - run `bpe analyze` first")
        documents = {sid: Document.from_json(self.store.get("documents", sid)) for sid in sources
                     if self.store.exists("documents", sid)}
        used = sorted({i.extractor for i in insights})
        bp = build_blueprint(self.cfg, sources, insights, documents, extractor="+".join(used))

        out = Path(reports_dir)
        out.mkdir(parents=True, exist_ok=True)
        import json

        (out / "blueprint.json").write_text(json.dumps(bp.to_dict(), ensure_ascii=False, indent=1), encoding="utf-8")
        (out / "evidence-report.md").write_text(render_report(bp), encoding="utf-8")
        written = write_framework(bp, out / "prompt-framework")
        rep.counts.update(
            sources=len(sources), insights=len(insights), prompts=len(written) - 1,
            p0=sum(1 for p in bp.pillars for f in p.mechanics if f.priority == "P0"),
            notices=len(bp.platform_notices),
        )
        rep.seconds = time.monotonic() - t0
        return rep
