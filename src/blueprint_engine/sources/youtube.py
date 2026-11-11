"""YouTube via yt-dlp: search, metadata and caption tracks.

Transcript strategy (in order):
1. Caption tracks listed by yt-dlp's own ``extract_info`` (manual subs first, then the
   original-language ASR track). This works from cloud IPs, where YouTube blocks the
   unauthenticated timedtext endpoints that most transcript libraries depend on.
2. ``youtube-transcript-api`` if installed, which works well from residential IPs.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

import requests

from blueprint_engine.models import Source
from blueprint_engine.net import RateLimiter, with_backoff
from blueprint_engine.sources import NoTranscript, SourceUnavailable
from blueprint_engine.sources.captions import parse_json3, parse_vtt
from blueprint_engine.sources.ytdlp_common import YDLPool

log = logging.getLogger(__name__)

WATCH = "https://www.youtube.com/watch?v={}"


def _lang_ok(code: str, languages: list[str]) -> bool:
    base = code.split("-")[0].lower()
    return any(base == lang.split("-")[0].lower() for lang in languages)


def _slim_tracks(tracks: dict[str, list[dict[str, Any]]] | None, languages: list[str]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    for code, fmts in (tracks or {}).items():
        if not _lang_ok(code, languages):
            continue
        keep = [{"ext": f["ext"], "url": f["url"]} for f in fmts if f.get("ext") in ("json3", "vtt") and f.get("url")]
        if keep:
            out[code] = keep
    return out


def slim_info(info: dict[str, Any], languages: list[str]) -> dict[str, Any]:
    """Keep only what ranking + transcripts need (full info dicts are ~1 MB)."""
    auto = info.get("automatic_captions") or {}
    orig = next((k for k in auto if k.endswith("-orig")), None)
    return {
        "id": info.get("id"),
        "title": info.get("title") or "",
        "channel": info.get("channel") or info.get("uploader") or "",
        "channel_id": info.get("channel_id"),
        "upload_date": info.get("upload_date"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "comment_count": info.get("comment_count"),
        "channel_follower_count": info.get("channel_follower_count"),
        "description": (info.get("description") or "")[:4000],
        "tags": (info.get("tags") or [])[:40],
        "language": info.get("language"),
        "asr_original_language": orig[: -len("-orig")] if orig else None,
        "subtitles": _slim_tracks(info.get("subtitles"), languages),
        "automatic_captions": _slim_tracks(auto, languages),
    }


def pick_track(slim: dict[str, Any], languages: list[str]) -> tuple[str, str, str, str] | None:
    """Return (url, ext, origin, lang) for the best caption track, or None.

    Machine-translated ASR tracks are rejected: an English ``en`` auto track on a video
    whose original ASR language is, say, Portuguese is a translation, not a transcript.
    """

    def best(fmts: list[dict[str, str]]) -> tuple[str, str] | None:
        for ext in ("json3", "vtt"):
            for f in fmts:
                if f["ext"] == ext:
                    return f["url"], ext
        return None

    for code, fmts in slim.get("subtitles", {}).items():
        if _lang_ok(code, languages) and (b := best(fmts)):
            return b[0], b[1], "manual-captions", code

    orig = slim.get("asr_original_language")
    if orig and not _lang_ok(orig, languages):
        return None
    auto = slim.get("automatic_captions", {})
    for code in sorted(auto, key=lambda c: (not c.endswith("-orig"), c)):
        if _lang_ok(code, languages) and (b := best(auto[code])):
            return b[0], b[1], "auto-captions", code
    return None


def to_source(slim: dict[str, Any]) -> Source:
    d = slim.get("upload_date")
    published = f"{d[:4]}-{d[4:6]}-{d[6:8]}" if d and len(d) == 8 else None
    return Source(
        id=f"yt:{slim['id']}",
        kind="youtube",
        url=WATCH.format(slim["id"]),
        title=slim.get("title", ""),
        author=slim.get("channel", ""),
        published=published,
        duration_s=int(slim["duration"]) if slim.get("duration") else None,
        views=slim.get("view_count"),
        likes=slim.get("like_count"),
        comments=slim.get("comment_count"),
        followers=slim.get("channel_follower_count"),
        description=slim.get("description", ""),
        tags=list(slim.get("tags") or []),
    )


def age_days(published: str | None, today: date | None = None) -> int | None:
    if not published:
        return None
    y, m, d = (int(x) for x in published.split("-"))
    return ((today or date.today()) - date(y, m, d)).days


class YouTubeClient:
    def __init__(self, limiter: RateLimiter, session: requests.Session, languages: list[str]):
        self.limiter = limiter
        self.session = session
        self.languages = languages
        self.pool = YDLPool()

    # -- discovery ---------------------------------------------------------
    def search(self, query: str, n: int) -> list[dict[str, Any]]:
        """Flat search results: id, title, channel, view_count, duration (no upload date)."""
        self.limiter.wait()

        def run() -> dict[str, Any]:
            return self.pool.get(flat=True).extract_info(f"ytsearch{n}:{query}", download=False) or {}

        try:
            res = with_backoff(run, attempts=3, what=f"search {query!r}")
        except Exception as exc:  # yt-dlp raises DownloadError for network/bot-wall problems
            raise SourceUnavailable(f"YouTube search failed for {query!r}: {exc}") from exc
        out = []
        for e in res.get("entries") or []:
            if not e or not e.get("id") or e.get("ie_key") not in (None, "Youtube"):
                continue
            if "/shorts/" in (e.get("url") or ""):
                continue
            out.append(
                {
                    "id": e["id"],
                    "title": e.get("title") or "",
                    "channel": e.get("channel") or e.get("uploader") or "",
                    "view_count": e.get("view_count"),
                    "duration": e.get("duration"),
                    "description": (e.get("description") or "")[:500],
                }
            )
        return out

    # -- metadata ----------------------------------------------------------
    def info(self, video_id: str) -> dict[str, Any]:
        self.limiter.wait()

        def run() -> dict[str, Any]:
            return self.pool.get(flat=False).extract_info(WATCH.format(video_id), download=False)

        try:
            info = with_backoff(run, attempts=3, what=f"info {video_id}")
        except Exception as exc:
            raise SourceUnavailable(f"metadata failed for {video_id}: {exc}") from exc
        return slim_info(info, self.languages)

    # -- transcripts -------------------------------------------------------
    def _download_track(self, url: str, ext: str) -> list[tuple[float, str]]:
        self.limiter.wait()
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        if ext == "json3":
            return parse_json3(resp.json())
        return parse_vtt(resp.text)

    def transcript(self, slim: dict[str, Any], refresh=None) -> tuple[list[tuple[float, str]], str, str]:
        """Return (tokens, origin, lang). ``refresh`` re-fetches metadata if signed URLs expired."""
        track = pick_track(slim, self.languages)
        if track:
            url, ext, origin, lang = track
            try:
                tokens = self._download_track(url, ext)
            except requests.HTTPError as exc:
                if refresh is None:
                    raise
                log.debug("caption URL rejected (%s); refreshing metadata for %s", exc, slim["id"])
                slim = refresh()
                track = pick_track(slim, self.languages)
                if not track:
                    raise NoTranscript(f"{slim['id']}: no caption track after refresh") from exc
                url, ext, origin, lang = track
                tokens = self._download_track(url, ext)
            if tokens:
                return tokens, origin, lang

        fallback = self._transcript_api(slim["id"])
        if fallback:
            return fallback
        raise NoTranscript(f"{slim['id']}: no usable {'/'.join(self.languages)} transcript")

    def _transcript_api(self, video_id: str) -> tuple[list[tuple[float, str]], str, str] | None:
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
        except ImportError:
            return None
        try:
            self.limiter.wait()
            fetched = YouTubeTranscriptApi().fetch(video_id, languages=self.languages)
            tokens = [(float(s.start), s.text) for s in fetched.snippets]
            origin = "auto-captions" if getattr(fetched, "is_generated", True) else "manual-captions"
            return tokens, f"{origin}(transcript-api)", getattr(fetched, "language_code", self.languages[0])
        except Exception as exc:  # RequestBlocked on cloud IPs, TranscriptsDisabled, ...
            log.debug("youtube-transcript-api fallback failed for %s: %s", video_id, type(exc).__name__)
            return None
