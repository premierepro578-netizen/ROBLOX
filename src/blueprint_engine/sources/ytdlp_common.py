"""Shared yt-dlp plumbing: per-thread YoutubeDL instances and quiet logging."""

from __future__ import annotations

import logging
import threading
from typing import Any

log = logging.getLogger("blueprint_engine.ytdlp")


class _QuietLogger:
    def debug(self, msg: str) -> None:
        if not msg.startswith("[debug] "):
            log.debug(msg)

    def info(self, msg: str) -> None:
        log.debug(msg)

    def warning(self, msg: str) -> None:
        log.debug("yt-dlp warning: %s", msg)

    def error(self, msg: str) -> None:
        log.debug("yt-dlp error: %s", msg)


_BASE_OPTS: dict[str, Any] = {
    "quiet": True,
    "no_warnings": True,
    "skip_download": True,
    "noprogress": True,
    "socket_timeout": 30,
    "retries": 3,
    "extractor_retries": 2,
    "logger": _QuietLogger(),
}


class YDLPool:
    """yt-dlp's YoutubeDL is not thread-safe; keep one instance per (thread, mode)."""

    def __init__(self) -> None:
        self._local = threading.local()

    def get(self, flat: bool, playlist_end: int | None = None):
        from yt_dlp import YoutubeDL  # imported lazily: heavy module

        key = (flat, playlist_end)
        cache = getattr(self._local, "cache", None)
        if cache is None:
            cache = self._local.cache = {}
        if key not in cache:
            opts = dict(_BASE_OPTS)
            if flat:
                opts["extract_flat"] = "in_playlist"
            else:
                opts["noplaylist"] = True
            if playlist_end:
                opts["playlistend"] = playlist_end
            cache[key] = YoutubeDL(opts)
        return cache[key]
