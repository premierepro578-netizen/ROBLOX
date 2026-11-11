"""Claude-backed insight extraction (``bpe analyze --extractor claude``).

One request per source. The system prompt (prompt template ``extract-insights`` plus
the taxonomy) is identical across sources, so it is cached; the transcript varies.
Output is constrained with a JSON schema, then every quote is checked against the
source text so an ungrounded "quote" cannot slip into the evidence base.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from blueprint_engine.analysis.taxonomy import TAXONOMY, Pillar
from blueprint_engine.models import Document, Insight, Source
from blueprint_engine.prompts import load_templates, render

log = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-opus-5-5"
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class FatalLLMError(RuntimeError):
    """Configuration problems (auth, unknown model, bad request) - stop the whole stage."""


def _fmt_ts(seconds: float | None) -> str:
    if seconds is None:
        return ""
    s = int(seconds)
    return f"[{s // 3600:d}:{s // 60 % 60:02d}:{s % 60:02d}] " if s >= 3600 else f"[{s // 60:02d}:{s % 60:02d}] "


def document_text(doc: Document) -> str:
    return "\n".join(f"{_fmt_ts(s.start)}{s.text}" for s in doc.segments)


def taxonomy_text(pillars: dict[str, Pillar]) -> str:
    lines = []
    for p in pillars.values():
        lines.append(f"- {p.key} ({p.label}):")
        lines.extend(f"    - {m.key}: {m.label}" for m in p.mechanics)
    return "\n".join(lines)


def output_schema(pillars: dict[str, Pillar]) -> dict[str, Any]:
    mechanics = sorted({m.key for p in pillars.values() for m in p.mechanics} | {"other"})
    insight = {
        "type": "object",
        "properties": {
            "pillar": {"type": "string", "enum": list(pillars)},
            "mechanic": {"type": "string", "enum": mechanics},
            "tactic": {"type": "string", "description": "Imperative, implementable instruction."},
            "rationale": {"type": "string", "description": "Why it works, as argued by the source; 'not stated' if absent."},
            "evidence_quote": {"type": "string", "description": "Verbatim contiguous excerpt, at most 40 words."},
            "timestamp_s": {"type": "integer", "description": "Seconds from the nearest preceding [mm:ss] marker; -1 if none."},
            "metrics": {"type": "array", "items": {"type": "string"}},
            "risk": {"type": "string", "description": "Player-trust or platform-policy risk; 'none' if none."},
            "confidence": {"type": "number", "description": "0-1: how clearly and specifically the source supports it."},
        },
        "required": ["pillar", "mechanic", "tactic", "rationale", "evidence_quote", "timestamp_s", "metrics", "risk", "confidence"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "insights": {"type": "array", "items": insight},
        },
        "required": ["summary", "insights"],
        "additionalProperties": False,
    }


_NORM = re.compile(r"[^a-z0-9 ]+")


def _norm(text: str) -> str:
    return " ".join(_NORM.sub(" ", text.lower()).split())


def is_grounded(quote: str, source_text: str, min_overlap: float = 0.75) -> bool:
    """True if ``quote`` appears (near-)verbatim in ``source_text``."""
    q, src = _norm(quote), _norm(source_text)
    if not q:
        return False
    if q in src:
        return True
    qw = q.split()
    if len(qw) < 4:
        return False
    # Sliding window token overlap tolerates ASR punctuation/casing drift.
    sw = src.split()
    want = set(qw)
    n = len(qw)
    best = 0.0
    for i in range(0, max(1, len(sw) - n + 1), max(1, n // 4)):
        window = set(sw[i: i + n + 4])
        best = max(best, len(want & window) / len(want))
        if best >= min_overlap:
            return True
    return False


class ClaudeExtractor:
    def __init__(self, model: str = DEFAULT_MODEL, effort: str = "medium", max_tokens: int = 16000,
                 client: Any = None, pillars: dict[str, Pillar] | None = None):
        self.model = model
        self.effort = effort
        self.max_tokens = max_tokens
        self.pillars = pillars or TAXONOMY
        if client is None:
            try:
                import anthropic
            except ImportError as exc:  # pragma: no cover - exercised only without the extra
                raise FatalLLMError("install the llm extra: pip install 'blueprint-engine[llm]'") from exc
            client = anthropic.Anthropic(max_retries=4)
        self.client = client
        template = load_templates()["extract-insights"]
        self.system_prompt, _ = render(template, {"taxonomy": taxonomy_text(self.pillars)})
        self.schema = output_schema(self.pillars)

    def _request(self, source: Source, doc: Document) -> dict[str, Any]:
        import anthropic

        header = (
            f"Source: {source.title}\nAuthor: {source.author}\nKind: {source.kind}\nURL: {source.url}\n"
            f"Pillars this source was found for: {', '.join(source.pillars) or 'unspecified'}\n"
        )
        user = f"{header}\n<source_text>\n{document_text(doc)}\n</source_text>"
        try:
            resp = self.client.beta.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                betas=[FALLBACK_BETA],
                fallbacks="default",  # re-run on a fallback model if a safety classifier declines
                thinking={"type": "adaptive"},
                output_config={"effort": self.effort, "format": {"type": "json_schema", "schema": self.schema}},
                cache_control={"type": "ephemeral"},
                system=self.system_prompt,
                messages=[{"role": "user", "content": user}],
            )
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.NotFoundError,
                anthropic.BadRequestError) as exc:
            raise FatalLLMError(f"{type(exc).__name__}: {exc}") from exc
        except TypeError as exc:
            # The SDK raises TypeError before sending when no credential source resolves.
            if "authentication" in str(exc).lower():
                raise FatalLLMError(
                    "no Anthropic credentials found: set ANTHROPIC_API_KEY (or log in with `ant auth login`)"
                ) from exc
            raise

        if resp.stop_reason == "refusal":
            category = getattr(resp.stop_details, "category", None) if resp.stop_details else None
            log.warning("model declined %s (category=%s); skipping", source.id, category)
            return {"summary": "", "insights": []}
        if resp.stop_reason == "max_tokens":
            raise RuntimeError(f"{source.id}: output hit max_tokens={self.max_tokens}")
        text = next((b.text for b in resp.content if b.type == "text"), "")
        return json.loads(text)

    def extract(self, source: Source, doc: Document) -> list[Insight]:
        data = self._request(source, doc)
        full_text = " ".join(s.text for s in doc.segments)
        out = []
        for item in data.get("insights", []):
            if item.get("pillar") not in self.pillars:
                continue
            quote = item.get("evidence_quote", "").strip()
            confidence = float(item.get("confidence") or 0.0)
            if not is_grounded(quote, full_text):
                log.debug("ungrounded quote from %s: %r", source.id, quote[:80])
                confidence *= 0.5
            rationale = item.get("rationale") or None
            risk = (item.get("risk") or "none").strip()
            if risk.lower() != "none":
                rationale = f"{rationale or ''} [risk: {risk}]".strip()
            ts = item.get("timestamp_s")
            out.append(Insight(
                source_id=source.id,
                pillar=item["pillar"],
                mechanics=[item.get("mechanic") or "other"],
                text=quote,
                start=float(ts) if isinstance(ts, (int, float)) and ts >= 0 else None,
                actionability=round(max(0.0, min(confidence, 1.0)), 3),
                metrics=list(item.get("metrics") or []),
                extractor="claude",
                tactic=item.get("tactic") or None,
                rationale=rationale,
                confidence=round(confidence, 3),
            ))
        return out
