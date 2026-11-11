"""Typed view over ``config/research.toml``."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class RunConfig:
    workers: int = 4
    results_per_query: int = 12
    # Full metadata is pulled for this many candidates per pillar (ranked by a cheap
    # pre-score); transcripts are kept for the best ``top_per_pillar`` of those.
    shortlist_per_pillar: int = 24
    top_per_pillar: int = 12
    min_duration_s: int = 90
    max_duration_s: int = 3600
    languages: list[str] = field(default_factory=lambda: ["en"])
    min_request_interval_s: float = 0.4
    max_age_days: int = 2200  # ignore stale advice (~6 years); Roblox changes fast
    min_relevance: float = 0.3  # never back-fill a pillar with off-topic videos


@dataclass
class PillarConfig:
    key: str
    label: str
    queries: list[str]
    focus: bool = True  # False = supporting pillar (reported, but not a primary focus)


@dataclass
class DocPage:
    path: str
    pillars: list[str]


@dataclass
class TikTokConfig:
    handles: list[str] = field(default_factory=list)
    videos: list[str] = field(default_factory=list)
    max_per_handle: int = 8


@dataclass
class DevForumConfig:
    base_url: str = "https://devforum.roblox.com"
    queries: list[str] = field(default_factory=list)
    topics_per_query: int = 5


@dataclass
class Config:
    run: RunConfig
    pillars: dict[str, PillarConfig]
    docs_base_url: str
    docs: list[DocPage]
    tiktok: TikTokConfig
    devforum: DevForumConfig

    @property
    def focus_pillars(self) -> list[str]:
        return [k for k, p in self.pillars.items() if p.focus]


def _build(cls, data: dict[str, Any] | None):
    data = data or {}
    allowed = cls.__dataclass_fields__.keys()
    unknown = set(data) - set(allowed)
    if unknown:
        raise ValueError(f"unknown {cls.__name__} keys: {sorted(unknown)}")
    return cls(**data)


def load_config(path: str | Path) -> Config:
    with Path(path).open("rb") as fh:
        raw = tomllib.load(fh)

    pillars = {}
    for key, p in raw.get("pillars", {}).items():
        pillars[key] = PillarConfig(
            key=key,
            label=p.get("label", key),
            queries=list(p.get("queries", [])),
            focus=bool(p.get("focus", True)),
        )
    if not pillars:
        raise ValueError("config needs at least one [pillars.<name>] table")

    docs_raw = raw.get("docs", {})
    docs = [DocPage(path=d["path"], pillars=list(d.get("pillars", []))) for d in docs_raw.get("pages", [])]
    for d in docs:
        bad = set(d.pillars) - set(pillars)
        if bad:
            raise ValueError(f"doc page {d.path} references unknown pillars {sorted(bad)}")

    return Config(
        run=_build(RunConfig, raw.get("run")),
        pillars=pillars,
        docs_base_url=docs_raw.get("base_url", "https://create.roblox.com/docs"),
        docs=docs,
        tiktok=_build(TikTokConfig, raw.get("tiktok")),
        devforum=_build(DevForumConfig, raw.get("devforum")),
    )
