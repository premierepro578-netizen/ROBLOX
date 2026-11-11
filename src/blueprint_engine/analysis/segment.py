"""Turn raw caption tokens / page text into sentence-sized segments.

YouTube auto-captions arrive as a stream of words with timestamps and (usually) no
punctuation. Sentence boundaries are therefore recovered from three signals:
terminal punctuation when present, speech pauses, and spoken discourse markers
("so", "now", "the next thing"...), with a hard cap so no segment runs on forever.
"""

from __future__ import annotations

import re

from blueprint_engine.models import Segment

_NOISE = re.compile(r"\[(?:music|applause|laughter|laughs|inaudible|__|silence)[^\]]*\]|>>|♪", re.I)
_WS = re.compile(r"\s+")
_TERMINAL = re.compile(r"[.!?…]['\")\]]*$")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])")
# Spoken markers that usually open a new thought in tutorial-style speech.
_MARKERS = (
    "so", "now", "next", "but", "also", "another", "first", "second", "third", "finally",
    "number", "step", "tip", "okay", "ok", "alright", "the next", "and then", "the first",
    "the second", "the third", "the last", "the biggest", "the most", "if you", "what you",
    "when you", "this is", "that's why", "because", "for example",
)
_MARKER_RE = re.compile(r"^(?:" + "|".join(re.escape(m) for m in sorted(_MARKERS, key=len, reverse=True)) + r")\b", re.I)


def clean_text(text: str) -> str:
    text = _NOISE.sub(" ", text)
    text = text.replace("​", " ").replace("&nbsp;", " ")
    return _WS.sub(" ", text).strip()


def is_punctuated(tokens: list[tuple[float, str]], min_ratio: float = 1 / 40) -> bool:
    words = sum(len(t.split()) for _, t in tokens) or 1
    terminals = sum(1 for _, t in tokens if _TERMINAL.search(t.strip()))
    return terminals / words >= min_ratio


def segments_from_tokens(
    tokens: list[tuple[float, str]],
    *,
    pause_s: float = 0.9,
    min_words: int = 6,
    soft_max_words: int = 22,
    hard_max_words: int = 40,
) -> list[Segment]:
    """Group timestamped caption tokens into sentence-like segments."""
    tokens = [(t, clean_text(x)) for t, x in tokens]
    tokens = [(t, x) for t, x in tokens if x]
    if not tokens:
        return []
    punctuated = is_punctuated(tokens)

    out: list[Segment] = []
    buf: list[str] = []
    start: float | None = None
    prev_t: float | None = None

    def flush() -> None:
        nonlocal buf, start
        text = clean_text(" ".join(buf))
        if text:
            out.append(Segment(text=text, start=round(start or 0.0, 2)))
        buf, start = [], None

    for t, text in tokens:
        n = sum(len(b.split()) for b in buf)
        if buf:
            gap = (t - prev_t) if prev_t is not None else 0.0
            if punctuated:
                boundary = n >= hard_max_words
            else:
                boundary = (
                    (gap >= pause_s and n >= min_words)
                    or (n >= soft_max_words and bool(_MARKER_RE.match(text)))
                    or (n >= 12 and gap >= pause_s * 0.6 and bool(_MARKER_RE.match(text)))
                    or n >= hard_max_words
                )
            if boundary:
                flush()
        if start is None:
            start = t
        buf.append(text)
        prev_t = t
        if punctuated and _TERMINAL.search(text) and sum(len(b.split()) for b in buf) >= 3:
            flush()
    flush()
    return out


def split_sentences(paragraph: str) -> list[str]:
    paragraph = clean_text(paragraph)
    if not paragraph:
        return []
    return [s.strip() for s in _SENT_SPLIT.split(paragraph) if s.strip()]


def segments_from_paragraphs(paragraphs: list[str]) -> list[Segment]:
    return [Segment(text=s) for p in paragraphs for s in split_sentences(p)]
