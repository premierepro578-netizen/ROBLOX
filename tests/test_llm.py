"""The Claude extractor's request/response handling, against a mock HTTP transport (no network, no key)."""

import json

import pytest

anthropic = pytest.importorskip("anthropic")
httpx2 = pytest.importorskip("httpx2")

from blueprint_engine.analysis.llm import ClaudeExtractor, is_grounded  # noqa: E402
from blueprint_engine.models import Document, Segment, Source  # noqa: E402

TRANSCRIPT = [
    Segment("Number one, add a daily reward streak so players come back tomorrow.", 65.0),
    Segment("Make the first upgrade visible within a minute.", 130.0),
]


def _client(captured, payload, stop_reason="end_turn"):
    def handler(request):
        captured.append(json.loads(request.content))
        body = {
            "id": "msg_test", "type": "message", "role": "assistant", "model": "claude-opus-5-5",
            "content": [{"type": "text", "text": json.dumps(payload)}],
            "stop_reason": stop_reason, "stop_sequence": None,
            "usage": {"input_tokens": 10, "output_tokens": 10},
        }
        return httpx2.Response(200, json=body)

    return anthropic.Anthropic(api_key="test-key", base_url="https://api.example.test",
                               http_client=httpx2.Client(transport=httpx2.MockTransport(handler)), max_retries=0)


def test_request_shape_and_grounding():
    payload = {"summary": "s", "insights": [
        {"pillar": "retention", "mechanic": "daily_rewards", "tactic": "Add a 7-day daily reward streak.",
         "rationale": "Players return to keep the streak.", "evidence_quote": "add a daily reward streak so players come back tomorrow",
         "timestamp_s": 65, "metrics": [], "risk": "none", "confidence": 0.9},
        {"pillar": "onboarding", "mechanic": "quick_win", "tactic": "Grant an upgrade in minute one.",
         "rationale": "not stated", "evidence_quote": "this sentence never appears in the transcript at all",
         "timestamp_s": -1, "metrics": [], "risk": "none", "confidence": 0.8},
    ]}
    captured = []
    ex = ClaudeExtractor(client=_client(captured, payload))
    src = Source("yt:x", "youtube", "https://www.youtube.com/watch?v=x", "Tips", "Chan", pillars=["retention"])
    out = ex.extract(src, Document("yt:x", "auto-captions", "en", TRANSCRIPT))

    req = captured[0]
    assert req["model"] == "claude-opus-5-5"
    assert req["thinking"] == {"type": "adaptive"}
    assert req["output_config"]["effort"] == "medium"
    assert req["output_config"]["format"]["type"] == "json_schema"
    assert req["fallbacks"] == "default"
    assert "[01:05] Number one" in req["messages"][0]["content"]
    assert "daily_rewards" in req["system"]  # taxonomy rendered into the cached system prompt

    assert out[0].tactic.startswith("Add a 7-day") and out[0].start == 65.0 and out[0].confidence == 0.9
    assert out[1].start is None and out[1].confidence == pytest.approx(0.4)  # ungrounded quote halved


def test_refusal_is_skipped_not_raised():
    captured = []
    ex = ClaudeExtractor(client=_client(captured, {"summary": "", "insights": []}, stop_reason="refusal"))
    src = Source("yt:y", "youtube", "u", "t")
    assert ex.extract(src, Document("yt:y", "auto-captions", "en", TRANSCRIPT)) == []


def test_is_grounded_tolerates_asr_drift():
    text = "so the first thing you want to do is give players a reward right away okay"
    assert is_grounded("The first thing you want to do is give players a reward right away.", text)
    assert not is_grounded("Monetize with loot boxes everywhere.", text)
