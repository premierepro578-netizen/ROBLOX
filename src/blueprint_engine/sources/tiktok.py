"""TikTok via yt-dlp.

yt-dlp's TikTok *search/tag* extractors are marked broken upstream, so discovery runs
from creator handles (user feeds work) or explicit video URLs. Most TikToks expose no
caption track; those fall back to their title/description as a metadata-only document.
"""

from __future__ import annotations

import logging
from typing import Any

import requests

from blueprint_engine.analysis.segment import segments_from_paragraphs, segments_from_tokens
from blueprint_engine.models import Document, Source
from blueprint_engine.net import RateLimiter, with_backoff
from blueprint_engine.sources import SourceUnavailable
from blueprint_engine.sources.captions import parse_vtt
from blueprint_engine.sources.ytdlp_common import YDLPool

log = logging.getLogger(__name__)


class TikTokClient:
    def __init__(self, limiter: RateLimiter, session: requests.Session, languages: list[str]):
        self.limiter = limiter
        self.session = session
        self.languages = languages
        self.pool = YDLPool()

    def feed(self, handle: str, n: int) -> list[str]:
        handle = handle if handle.startswith("@") else f"@{handle}"
        self.limiter.wait()

        def run() -> dict[str, Any]:
            return self.pool.get(flat=True, playlist_end=n).extract_info(
                f"https://www.tiktok.com/{handle}", download=False
            ) or {}

        try:
            res = with_backoff(run, attempts=2, what=f"tiktok feed {handle}")
        except Exception as exc:
            raise SourceUnavailable(f"TikTok feed {handle} failed: {exc}") from exc
        urls = []
        for e in (res.get("entries") or [])[:n]:
            url = e.get("url") or e.get("webpage_url")
            if url:
                urls.append(url)
        return urls

    def fetch(self, url: str) -> tuple[Source, Document]:
        self.limiter.wait()

        def run() -> dict[str, Any]:
            return self.pool.get(flat=False).extract_info(url, download=False)

        try:
            info = with_backoff(run, attempts=2, what=f"tiktok {url}")
        except Exception as exc:
            raise SourceUnavailable(f"TikTok video {url} failed: {exc}") from exc

        d = info.get("upload_date")
        src = Source(
            id=f"tt:{info['id']}",
            kind="tiktok",
            url=info.get("webpage_url") or url,
            title=(info.get("title") or "")[:200],
            author=info.get("uploader") or info.get("channel") or "",
            published=f"{d[:4]}-{d[4:6]}-{d[6:8]}" if d and len(d) == 8 else None,
            duration_s=int(info["duration"]) if info.get("duration") else None,
            views=info.get("view_count"),
            likes=info.get("like_count"),
            comments=info.get("comment_count"),
            followers=info.get("channel_follower_count"),
            description=(info.get("description") or "")[:2000],
        )

        for code, fmts in (info.get("subtitles") or {}).items():
            if not any(code.lower().startswith(lang.lower()) for lang in self.languages) and not code.lower().startswith("eng"):
                continue
            for f in fmts:
                if f.get("ext") == "vtt" and f.get("url"):
                    try:
                        self.limiter.wait()
                        r = self.session.get(f["url"], timeout=30)
                        r.raise_for_status()
                        segs = segments_from_tokens(parse_vtt(r.text))
                        if segs:
                            src.transcript_origin = "captions"
                            return src, Document(src.id, "captions", code, segs)
                    except requests.RequestException as exc:
                        log.debug("tiktok caption download failed for %s: %s", url, exc)

        src.transcript_origin = "metadata-only"
        text = [p for p in (src.title, src.description) if p]
        return src, Document(src.id, "metadata-only", self.languages[0], segments_from_paragraphs(text))
