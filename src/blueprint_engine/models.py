"""Plain dataclasses shared by every stage. All of them round-trip through JSON."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any, TypeVar

T = TypeVar("T")


def from_dict(cls: type[T], data: dict[str, Any]) -> T:
    """Build a dataclass from a dict, ignoring unknown keys (forward-compatible caches)."""
    names = {f.name for f in fields(cls)}  # type: ignore[arg-type]
    return cls(**{k: v for k, v in data.items() if k in names})


@dataclass
class Source:
    """One piece of content: a video, a doc page or a forum thread."""

    id: str  # "yt:<id>", "tt:<id>", "doc:<path>", "df:<topic id>"
    kind: str  # youtube | tiktok | doc | devforum
    url: str
    title: str
    author: str = ""
    published: str | None = None  # YYYY-MM-DD
    duration_s: int | None = None
    views: int | None = None
    likes: int | None = None
    comments: int | None = None
    followers: int | None = None
    description: str = ""
    tags: list[str] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)  # queries that surfaced it
    pillars: list[str] = field(default_factory=list)  # pillars those queries target
    score: float = 0.0
    score_breakdown: dict[str, float] = field(default_factory=dict)
    transcript_origin: str | None = None  # manual-captions | auto-captions | html | discourse | ...

    def link(self, start: float | None = None) -> str:
        """Deep link, with a timestamp where the platform supports one."""
        if start is not None and self.kind == "youtube":
            sep = "&" if "?" in self.url else "?"
            return f"{self.url}{sep}t={int(start)}s"
        return self.url

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Segment:
    """A sentence-sized unit of text; ``start`` is seconds into the media (None for pages)."""

    text: str
    start: float | None = None


@dataclass
class Document:
    source_id: str
    origin: str
    language: str
    segments: list[Segment]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Document":
        segs = [Segment(**s) for s in data.get("segments", [])]
        return cls(
            source_id=data["source_id"],
            origin=data.get("origin", ""),
            language=data.get("language", ""),
            segments=segs,
        )

    @property
    def word_count(self) -> int:
        return sum(len(s.text.split()) for s in self.segments)


@dataclass
class Insight:
    """One actionable claim pulled from a source, with its evidence."""

    source_id: str
    pillar: str
    mechanics: list[str]
    text: str  # evidence passage (verbatim, cleaned)
    start: float | None = None
    actionability: float = 0.0
    metrics: list[str] = field(default_factory=list)
    extractor: str = "heuristic"
    tactic: str | None = None  # normalized imperative (LLM extractor fills this)
    rationale: str | None = None
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
