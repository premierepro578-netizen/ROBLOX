"""Caption-file parsers (YouTube json3, WebVTT) -> ``[(start_seconds, text), ...]`` tokens."""

from __future__ import annotations

import html
import re
from typing import Any

_VTT_TIME = re.compile(
    r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})\s+-->\s+(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{3})"
)
_TAG = re.compile(r"<[^>]+>")
_INLINE_TS = re.compile(r"<((?:\d+:)?\d{1,2}:\d{2}[.,]\d{3})>")


def parse_json3(data: dict[str, Any]) -> list[tuple[float, str]]:
    """YouTube's json3 format: events[] with tStartMs and segs[] (word-level for ASR)."""
    tokens: list[tuple[float, str]] = []
    for ev in data.get("events", []):
        segs = ev.get("segs")
        if not segs:
            continue
        t0 = float(ev.get("tStartMs", 0))
        for seg in segs:
            text = seg.get("utf8", "")
            if not text or not text.strip():
                continue
            tokens.append(((t0 + float(seg.get("tOffsetMs", 0))) / 1000.0, text.strip()))
    tokens.sort(key=lambda x: x[0])
    return tokens


def _ts(h: str | None, m: str, s: str, ms: str) -> float:
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_vtt(text: str) -> list[tuple[float, str]]:
    """WebVTT -> tokens. De-duplicates the rolling repeated lines of auto-generated VTT."""
    tokens: list[tuple[float, str]] = []
    last_line = ""
    cue_start: float | None = None
    for raw in text.splitlines():
        line = raw.strip()
        m = _VTT_TIME.search(line)
        if m:
            cue_start = _ts(*m.groups()[:4])
            continue
        if not line or cue_start is None or line.startswith(("WEBVTT", "NOTE", "Kind:", "Language:")):
            continue
        clean = html.unescape(_TAG.sub("", line)).strip()
        if not clean or clean == last_line:
            continue
        # Rolling auto-captions repeat the previous line as a prefix; keep only the new tail.
        if last_line and clean.startswith(last_line):
            clean = clean[len(last_line):].strip()
            if not clean:
                continue
        tokens.append((cue_start, clean))
        last_line = html.unescape(_TAG.sub("", line)).strip()
    return tokens
