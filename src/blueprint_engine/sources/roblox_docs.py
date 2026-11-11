"""First-party Roblox Creator Docs (create.roblox.com/docs).

Pages are statically rendered, so the article text is present in the HTML; the
embedded Next.js payload only carries compiled MDX, which is not worth parsing.
"""

from __future__ import annotations

from bs4 import BeautifulSoup

import requests

from blueprint_engine.analysis.segment import clean_text, segments_from_paragraphs
from blueprint_engine.models import Document, Source
from blueprint_engine.net import RateLimiter
from blueprint_engine.sources import SourceUnavailable

_BLOCKS = ("p", "li")


def parse_article(html: str) -> tuple[str, str, list[str]]:
    """Return (title, description, paragraphs) from a docs page."""
    soup = BeautifulSoup(html, "lxml")
    root = soup.select_one("article") or soup.select_one("main") or soup.body
    if root is None:
        return "", "", []
    # Code blocks are not prose; inline <code> (API names) is deliberately kept.
    for junk in root.select("pre, script, style, nav, aside, button, svg"):
        junk.decompose()

    h1 = root.find("h1") or soup.find("h1")
    title = clean_text(h1.get_text(" ")) if h1 else ""
    if not title and soup.title:
        title = clean_text(soup.title.get_text(" ")).split("|")[0].strip()
    meta = soup.find("meta", attrs={"name": "description"})
    description = clean_text(meta["content"]) if meta and meta.get("content") else ""

    paragraphs: list[str] = []
    seen: set[str] = set()
    for el in root.find_all(_BLOCKS):
        # A <li> that wraps <p> children would duplicate them; let the <p>s speak.
        if el.name == "li" and el.find("p"):
            continue
        # Nested list items are already part of their parent item's text.
        if el.name == "li" and el.find_parent("li") is not None:
            continue
        text = clean_text(el.get_text(" "))
        text = text.replace(" ,", ",").replace(" .", ".").replace("( ", "(").replace(" )", ")")
        if len(text.split()) < 4 or text in seen:
            continue
        seen.add(text)
        paragraphs.append(text)
    return title, description, paragraphs


class RobloxDocsClient:
    def __init__(self, base_url: str, limiter: RateLimiter, session: requests.Session):
        self.base_url = base_url.rstrip("/")
        self.limiter = limiter
        self.session = session

    def fetch(self, path: str) -> tuple[Source, Document]:
        url = f"{self.base_url}/{path.strip('/')}"
        self.limiter.wait()
        try:
            resp = self.session.get(url, timeout=30)
        except requests.RequestException as exc:
            raise SourceUnavailable(f"docs fetch failed for {url}: {exc}") from exc
        if "/maintenance" in resp.url:
            raise SourceUnavailable("Roblox docs are in maintenance")
        if resp.status_code == 404:
            raise SourceUnavailable(f"docs page not found: {url}")
        resp.raise_for_status()

        title, description, paragraphs = parse_article(resp.text)
        src = Source(
            id=f"doc:{path.strip('/')}",
            kind="doc",
            url=resp.url,
            title=title or path,
            author="Roblox Creator Docs",
            description=description,
            transcript_origin="html",
        )
        return src, Document(src.id, "html", "en", segments_from_paragraphs(paragraphs))
