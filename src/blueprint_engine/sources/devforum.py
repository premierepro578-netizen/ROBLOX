"""Roblox DevForum through the standard Discourse JSON API.

When the forum is down for maintenance every route (JSON included) 302-redirects to
create.roblox.com/maintenance; ``available()`` detects that so the stage skips cleanly.
"""

from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from blueprint_engine.analysis.segment import clean_text, segments_from_paragraphs
from blueprint_engine.models import Document, Source
from blueprint_engine.net import RateLimiter
from blueprint_engine.sources import SourceUnavailable


def cooked_to_paragraphs(cooked: str) -> list[str]:
    soup = BeautifulSoup(cooked or "", "lxml")
    for junk in soup.select("pre, aside.quote, .lightbox-wrapper, img, svg"):
        junk.decompose()
    out = []
    for el in soup.find_all(["p", "li"]):
        if el.name == "li" and el.find("p"):
            continue
        text = clean_text(el.get_text(" "))
        if len(text.split()) >= 4:
            out.append(text)
    return out


def topic_to_document(topic: dict[str, Any], base_url: str, max_posts: int = 15) -> tuple[Source, Document]:
    posts = (topic.get("post_stream") or {}).get("posts") or []
    paragraphs: list[str] = []
    for post in posts[:max_posts]:
        paragraphs.extend(cooked_to_paragraphs(post.get("cooked", "")))
    first = posts[0] if posts else {}
    created = (topic.get("created_at") or "")[:10] or None
    group = (first.get("primary_group_name") or "").lower()
    staff = bool(first.get("staff") or first.get("admin") or "staff" in group or group.startswith("roblox"))
    src = Source(
        id=f"df:{topic['id']}",
        kind="devforum",
        url=f"{base_url.rstrip('/')}/t/{topic.get('slug', 'topic')}/{topic['id']}",
        title=topic.get("title") or "",
        author=first.get("username", ""),
        published=created,
        views=topic.get("views"),
        likes=topic.get("like_count"),
        comments=topic.get("posts_count"),
        tags=["first-party"] if staff else [],
        transcript_origin="discourse",
    )
    # Staff announcements: the platform's own post is the substance; replies are mostly reactions.
    if staff:
        paragraphs = cooked_to_paragraphs(first.get("cooked", ""))
    return src, Document(src.id, "discourse", "en", segments_from_paragraphs(paragraphs))


class DevForumClient:
    def __init__(self, base_url: str, limiter: RateLimiter, session: requests.Session):
        self.base_url = base_url.rstrip("/")
        self.limiter = limiter
        self.session = session

    def _get_json(self, path: str, **params: Any) -> dict[str, Any]:
        self.limiter.wait()
        try:
            resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30, allow_redirects=False)
        except requests.RequestException as exc:
            raise SourceUnavailable(f"DevForum request failed: {exc}") from exc
        if resp.is_redirect and "maintenance" in resp.headers.get("location", ""):
            raise SourceUnavailable("DevForum is redirecting to its maintenance page")
        if resp.status_code in (403, 429):
            raise SourceUnavailable(f"DevForum refused the request (HTTP {resp.status_code})")
        resp.raise_for_status()
        return resp.json()

    def available(self) -> bool:
        try:
            self._get_json("/latest.json")
            return True
        except SourceUnavailable:
            return False

    def search_topics(self, query: str, n: int) -> list[int]:
        data = self._get_json("/search.json", q=f"{query} order:likes")
        return [t["id"] for t in (data.get("topics") or [])[:n] if "id" in t]

    def fetch_topic(self, topic_id: int) -> tuple[Source, Document]:
        return topic_to_document(self._get_json(f"/t/{topic_id}.json"), self.base_url)
